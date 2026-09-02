# # scripts/publish_review.py

# import argparse
# import json
# import os
# import subprocess


# def comment(pr_number, body):

#     subprocess.run(
#         [
#             "gh",
#             "pr",
#             "comment",
#             str(pr_number),
#             "--body",
#             body
#         ],
#         check=True
#     )


# def main():

#     parser = argparse.ArgumentParser()

#     parser.add_argument("--pr-number", required=True)
#     parser.add_argument("--review-file", required=True)

#     args = parser.parse_args()

#     with open(args.review_file) as f:
#         review = json.load(f)

#     body = f"""
# ## 🤖 Claude AI Code Review

# ### Status

# **{review["status"]}**

# ### Score

# **{review["score"]}/10**

# ### Summary

# {review["summary"]}

# """

#     findings = review.get("findings", [])

#     if findings:

#         for finding in findings:
#             body += f"""
#         #### {finding.get("severity", "UNKNOWN")}: {finding.get("issue", "Code review finding")}

#         **File:** `{finding.get("file", "unknown")}`  
#         **Line:** `{finding.get("line", "unknown")}`

#         {finding.get("explanation", "No explanation provided.")}

#         **Suggested change:**

#         {finding.get("suggested_fix", "No suggestion provided.")}

#         ---
#         """

#     else:

#         body += """
# ### Findings

# No issues detected by the AI reviewer.
# """

#     comment(args.pr_number, body)


# if __name__ == "__main__":
#     main()

import argparse
import json
import os
import urllib.error
import urllib.request


def comment(pr_number: str, body: str) -> None:
    """Publish the AI review as a GitHub PR comment."""

    token = os.environ.get("GITHUB_TOKEN")
    repository = os.environ.get("GITHUB_REPOSITORY")

    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable is not set")

    if not repository:
        raise RuntimeError("GITHUB_REPOSITORY environment variable is not set")

    url = (
        f"https://api.github.com/repos/"
        f"{repository}/issues/{pr_number}/comments"
    )

    payload = json.dumps({
        "body": body
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "AI-Code-Review",
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            if response.status not in (200, 201):
                raise RuntimeError(
                    f"GitHub API returned HTTP {response.status}"
                )

            print("✅ AI review successfully published to GitHub PR")


    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")

        raise RuntimeError(
            f"GitHub API error: HTTP {exc.code}\n{error_body}"
        ) from exc


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pr-number",
        required=True,
        help="GitHub Pull Request number",
    )

    parser.add_argument(
        "--review-file",
        required=True,
        help="Path to AI review JSON file",
    )

    args = parser.parse_args()

    with open(args.review_file, "r", encoding="utf-8") as f:
        review = json.load(f)

    body = f"""## 🤖 Claude AI Code Review

### Status

**{review.get("status", "UNKNOWN")}**

### Score

**{review.get("score", "N/A")}/10**

### Summary

{review.get("summary", "No summary provided.")}

"""

    findings = review.get("findings", [])

    if findings:

        body += "### Findings\n\n"

        for finding in findings:

            severity = finding.get("severity", "UNKNOWN")
            issue = finding.get(
                "issue",
                "Code review finding",
            )

            file_name = finding.get(
                "file",
                "unknown",
            )

            line = finding.get(
                "line",
                "unknown",
            )

            explanation = finding.get(
                "explanation",
                "No explanation provided.",
            )

            suggested_fix = finding.get(
                "suggested_fix",
                "No suggestion provided.",
            )

            body += f"""#### {severity}: {issue}

**File:** `{file_name}`  
**Line:** `{line}`

{explanation}

**Suggested change:**

{suggested_fix}

---

"""

    else:

        body += """### Findings

No issues detected by the AI reviewer.
"""

    comment(
        pr_number=args.pr_number,
        body=body,
    )


if __name__ == "__main__":
    main()
