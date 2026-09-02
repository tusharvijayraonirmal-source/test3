import os
import json
import argparse

from dotenv import load_dotenv
from anthropic import Anthropic


# Load local .env file when running locally
load_dotenv()


MODEL = "claude-sonnet-5"
ANTHROPIC_AUTH_TOKEN  = os.getenv("ANTHROPIC_AUTH_TOKEN")



if not ANTHROPIC_AUTH_TOKEN:
    raise RuntimeError(
        "ANTHROPIC_AUTH_TOKEN  environment variable is not configured."
    )


if not MODEL:
    raise RuntimeError(
        "CLAUDE_MODEL environment variable is not configured."
    )


client = Anthropic(
    api_key=ANTHROPIC_AUTH_TOKEN 
)


def review_code(
    diff: str,
    repository: str,
    pr_number: int
):

    prompt = f"""
You are an expert senior software engineer performing
a Pull Request code review.

Repository:
{repository}

Pull Request:
#{pr_number}

Review the following Git diff.

Your objectives:

1. Identify correctness issues.
2. Identify security vulnerabilities.
3. Identify performance problems.
4. Identify maintainability issues.
5. Identify error-handling problems.
6. Identify missing or inadequate tests.
7. Identify potential breaking changes.
8. Do not report purely stylistic issues unless they
   materially affect maintainability.
9. Do not invent files, functions, requirements, or
   business rules.
10. Only report findings supported by the supplied code.

For every finding provide:

- file
- line
- severity
- category
- issue
- explanation
- suggested_fix

Severity must be one of:

CRITICAL
HIGH
MEDIUM
LOW

Return ONLY valid JSON.

Expected structure:

{{
  "status": "APPROVED" or "CHANGES_REQUESTED",
  "summary": "Short review summary",
  "score": 0,
  "findings": [
    {{
      "file": "path/to/file.py",
      "line": 10,
      "severity": "HIGH",
      "category": "SECURITY",
      "issue": "Description of the issue",
      "explanation": "Why this is a problem",
      "suggested_fix": "Recommended fix"
    }}
  ]
}}

If there are no significant findings, return:

{{
  "status": "APPROVED",
  "summary": "No significant issues found.",
  "score": 10,
  "findings": []
}}

Git diff:

{diff}
"""

    print(f"Calling Claude model: {MODEL}")

    # response = client.messages.create(
    #     model=MODEL,
    #     max_tokens=4096,
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ]
    # )
    response = client.messages.create(
    model=MODEL,
    max_tokens=8192,
    thinking={
        "type": "disabled"
    },
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
    if response.stop_reason == "max_tokens":
        raise RuntimeError(
            "Claude response was truncated (hit max_tokens limit). "
            "Increase max_tokens or reduce diff size."
        )
    # text = response.content[0].text.strip()
    text = ""

    for block in response.content:
        if getattr(block, "type", None) == "text":
            text += block.text

    text = text.strip()

    if not text:
        raise RuntimeError(
            "Claude returned no text content. "
            f"Response content types: "
            f"{[getattr(b, 'type', type(b).__name__) for b in response.content]}"
        )

    # Remove Markdown code fences if Claude returns them
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    try:
        review = json.loads(text)
    except json.JSONDecodeError as exc:
        print("Claude returned invalid JSON:")
        print(text)

        raise RuntimeError(
            "Claude response was not valid JSON."
        ) from exc

    # ---------------------------------------------
    # Add Claude token usage
    # ---------------------------------------------

    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    review["token_usage"] = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }

    print()
    print("======================================")
    print("CLAUDE TOKEN USAGE")
    print("======================================")
    print(f"Input tokens : {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Total tokens : {input_tokens + output_tokens}")

    return review    
    # except json.JSONDecodeError as exc:
    #     print("Claude returned invalid JSON:")
    #     print(text)

    #     raise RuntimeError(
    #         "Claude response was not valid JSON."
    #     ) from exc

    # return review


def main():

    parser = argparse.ArgumentParser(
        description="Claude AI Pull Request Code Review"
    )

    parser.add_argument(
        "--diff",
        required=True,
        help="Path to PR diff file"
    )

    parser.add_argument(
        "--pr-number",
        required=True,
        type=int,
        help="GitHub Pull Request number"
    )

    parser.add_argument(
        "--repository",
        required=True,
        help="GitHub repository name"
    )

    args = parser.parse_args()

    # ---------------------------------------------
    # Read diff
    # ---------------------------------------------

    with open(
        args.diff,
        "r",
        encoding="utf-8"
    ) as f:

        diff = f.read()

    # ---------------------------------------------
    # Handle empty diff
    # ---------------------------------------------

    if not diff.strip():

        print("WARNING: PR diff is empty.")

        review = {
            "status": "APPROVED",
            "summary": "No code changes detected.",
            "score": 10,
            "findings": []
        }

    else:

        review = review_code(
            diff=diff,
            repository=args.repository,
            pr_number=args.pr_number
        )

    # ---------------------------------------------
    # Save result
    # ---------------------------------------------

    output_file = "review_result.json"

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            review,
            f,
            indent=2
        )

    print()
    print("======================================")
    print("CLAUDE AI CODE REVIEW RESULT")
    print("======================================")

    print(
        json.dumps(
            review,
            indent=2
        )
    )

    print()
    print(f"Review saved to: {output_file}")


if __name__ == "__main__":
    main()