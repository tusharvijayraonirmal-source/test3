from pathlib import Path


def load_skill(skill_name: str) -> str:

    project_root = Path(__file__).resolve().parent.parent

    skill_file = (
        project_root
        / "skills"
        / skill_name
        / "SKILL.md"
    )

    if not skill_file.exists():
        raise FileNotFoundError(
            f"Skill not found: {skill_file}"
        )

    return skill_file.read_text(
        encoding="utf-8"
    )

    CODE_REVIEW_SKILL = load_skill("code-review")

    def review_code(
    diff: str,
    repository: str,
    pr_number: int
    ):

            skill = load_skill("code-review")

            prompt = f"""
        You must perform this task using the following skill.

        ==============================
        SKILL
        ==============================

        {skill}

        ==============================
        PULL REQUEST CONTEXT
        ==============================

        Repository:
        {repository}

        Pull Request:
        #{pr_number}

        ==============================
        GIT DIFF
        ==============================

        {diff}

        ==============================

        Follow the skill instructions exactly.

        Return ONLY the JSON format specified
        by the skill.
        """