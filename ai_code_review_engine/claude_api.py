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
# Response normalization
# ============================================================

def _default_score(findings: list[Any]) -> int:
    """Derive a 0-10 score when the model omits one."""
    return max(0, 10 - 2 * len(findings))


def normalize_review_response(
    review: Any,
) -> dict[str, Any]:
    """
    Coerce Claude's reply into the expected shape:
    {"status", "score", "summary", "findings"}.

    Some model endpoints return a bare list of findings or omit the
    top-level fields even when asked for a specific format. Instead of
    hard-failing the workflow, fill in sensible defaults so downstream
    steps (publish, merge, email) always receive a usable result.
    """
    findings: list[Any] = []

    if isinstance(review, list):
        # Model returned a bare findings list.
        findings = list(review)
        review = {}

    if not isinstance(review, dict):
        logger.warning(
            "Review response was %s; using an empty review.",
            type(review).__name__,
        )
        review = {}
        if not isinstance(findings, list):
            findings = []

    if "findings" in review:
        raw_findings = review["findings"]
        if isinstance(raw_findings, list):
            findings = raw_findings
        elif raw_findings in (None, ""):
            findings = []
        else:
            findings = [raw_findings]
            logger.warning(
                "'findings' was %s; wrapped into a list.",
                type(raw_findings).__name__,
            )
        review["findings"] = findings
    else:
        review["findings"] = findings

    if "status" not in review or not str(
        review.get("status") or ""
    ).strip():
        review["status"] = (
            "CHANGES_REQUESTED" if findings else "APPROVED"
        )

    if "score" not in review or review.get("score") is None:
        review["score"] = _default_score(findings)

    if "summary" not in review or not str(
        review.get("summary") or ""
    ).strip():
        if findings:
            review["summary"] = (
                f"AI review reported {len(findings)} finding(s); "
                "the model did not provide a summary."
            )
        else:
            review["summary"] = (
                "AI review found no significant issues."
            )

    return review

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

Return ONLY valid JSON. No prose, no markdown fences, no code blocks.

The top-level JSON object MUST include these keys:
- "status": "APPROVED" or "CHANGES_REQUESTED"
- "score": an integer from 0 to 10
- "summary": a short review summary string
- "findings": a list (empty list if there are no findings)

Never return a bare array. Never omit any required key.
"""

    logger.info(f"Calling Claude model: {MODEL}")

    response = client.messages.create(
        model=MODEL,
        max_tokens=8192,
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

    # Remove Markdown JSON fences if Claude returns them
    if text.startswith("```json"):
        text = text[len("```json"):].strip()

    if text.startswith("```"):
        text = text[3:].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

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

    return normalize_review_response(review)
