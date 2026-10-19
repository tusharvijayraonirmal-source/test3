import os
import json
import logging
from pathlib import Path
from typing import Any

import anthropic
from json_repair import repair_json

logger = logging.getLogger(__name__)


# ============================================================
# Claude configuration
# ============================================================

MODEL = (
    os.getenv("ANTHROPIC_MODEL", "").strip()
    or os.getenv("CLAUDE_MODEL", "").strip()
    or "claude-sonnet-4-20250514"
)

api_key = (
    os.getenv("ANTHROPIC_AUTH_TOKEN", "").strip()
    or os.getenv("ANTHROPIC_API_KEY", "").strip()
    or os.getenv("ANTHROPIC_TOKEN", "").strip()
)

base_url = (
    os.getenv("ANTHROPIC_BASE_URL", "").strip()
    or "https://api.anthropic.com"
)


# ============================================================
# Validate configuration
# ============================================================

if not api_key:
    raise RuntimeError(
        "ANTHROPIC_AUTH_TOKEN is not set. "
        "Configure it in GitHub Actions secrets."
    )

if not base_url.startswith(("http://", "https://")):
    raise RuntimeError(
        f"Invalid ANTHROPIC_BASE_URL: {base_url!r}"
    )

if not MODEL:
    raise RuntimeError(
        "Claude model is not configured."
    )


logger.info(
    "Claude configuration: model=%s base_url=%s",
    MODEL,
    base_url,
)


# ============================================================
# Claude client
# ============================================================

client = anthropic.Anthropic(
    api_key=api_key,
    base_url=base_url.rstrip("/"),
)

# # Build client kwargs conditionally to avoid
# # passing empty values to newer SDK versions.
# client_kwargs: dict[str, Any] = {}

# if api_key:
#     client_kwargs["api_key"] = api_key

# if base_url:
#     client_kwargs["base_url"] = base_url.rstrip("/")

# client = anthropic.Anthropic(**client_kwargs)


def load_skill(skill_name: str) -> str:
    project_root = Path(__file__).resolve().parent.parent

    # Try standard skills dir first
    skill_file = (
        project_root
        / "skills"
        / skill_name
        / "skills.md"
    )

    if not skill_file.exists():
        # Fall back to custom skills dir
        skill_file = (
            project_root
            / "skills"
            / "custom"
            / skill_name
            / "skills.md"
        )

    if not skill_file.exists():
        raise FileNotFoundError(
            f"Skill not found: {skill_file}"
        )

    return skill_file.read_text(
        encoding="utf-8"
    )


def review_code(
    diff: str,
    repository: str,
    pr_number: int,
    selected_skills: list[str] | None = None,
    review_mode: str = "PR",
    repository_context: str = "",
    **kwargs: Any,
):
    # Load ONLY the skills selected by the user
    skills_content = []

    # Support both 'selected_skills' and 'skills' param names
    if selected_skills is None:
        selected_skills = kwargs.get("skills") or []

    selected_skills = selected_skills or []

    for skill_name in selected_skills:
        skill_name = skill_name.strip()

        if not skill_name:
            continue

        skill = load_skill(skill_name)

        skills_content.append(
            f"""
==============================
SKILL: {skill_name}
==============================
{skill}
"""
        )

    # If no skill was selected, use code-review as default
    if not skills_content:
        skills_content.append(
            f"""
==============================
SKILL: code-review
==============================
{load_skill("code-review")}
"""
        )

    combined_skills = "\n".join(skills_content)

    prompt = f"""
You must perform this task using the following selected skills.

{combined_skills}

==============================
REVIEW CONTEXT
==============================
Repository:
{repository}

Review Mode:
{review_mode}

Pull Request:
#{pr_number}

Repository Context:
{repository_context}

==============================
CODE / DIFF
==============================
{diff}

==============================
INSTRUCTIONS
==============================
Follow all selected skill instructions exactly.

Return ONLY the JSON format specified
by the applicable skill instructions.
"""

    logger.info(f"Calling Claude model: {MODEL}")

    # Full-codebase reviews embed the whole repository in the prompt, so the
    # JSON output can be far larger than a PR diff. 8192 truncates mid-object
    # and produces an unparseable response; 32768 covers a full repo review
    # with room for many findings.
    response = client.messages.create(
        model=MODEL,
        max_tokens=32768,
        thinking={
        "type": "disabled"
    },
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    # A truncated response is the main cause of "Claude response was not valid
    # JSON." Detect it up front so the failure message names the real problem
    # instead of surfacing a generic parse error.
    if getattr(response, "stop_reason", None) == "max_tokens":
        raise RuntimeError(
            "Claude response hit the max_tokens limit and was truncated "
            "before the JSON was complete. Reduce the diff size, split the "
            "review, or raise max_tokens."
        )

    text_parts = []

    for block in response.content:
        if getattr(block, "type", None) == "text":
            text_parts.append(block.text)

    text = "\n".join(text_parts).strip()

    if not text:
        raise RuntimeError(
            "Claude returned no text content. "
            f"Response blocks: "
            f"{[getattr(b, 'type', type(b).__name__) for b in response.content]}"
        )

    # Strip Markdown JSON fences. Match case-insensitively and allow leading
    # whitespace — a capitalized ```JSON or a blank line before the fence
    # previously defeated both checks and left backticks inside the JSON.
    stripped = text.lstrip()
    if stripped.lower().startswith("```json"):
        stripped = stripped[len("```json"):].lstrip()
    elif stripped.startswith("```"):
        stripped = stripped[3:].lstrip()

    if stripped.endswith("```"):
        stripped = stripped[:-3]

    text = stripped.strip()

    try:
        review = json.loads(text)
    except json.JSONDecodeError:
        logger.warning(
            "Primary JSON parse failed, "
            "attempting repair..."
        )
        try:
            repaired = repair_json(text)
            review = json.loads(repaired)
        except Exception as exc:
            logger.info("Claude returned invalid JSON:")
            logger.info(text[:5000])
            raise RuntimeError(
                "Claude response was not valid JSON."
            ) from exc

    return review
