# import argparse
# import sys
# import requests
# import json


# MAX_DIFF_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB


# def read_input(path):
#     """Read diff content from a file path or stdin when path is '-'."""
#     if path == "-":
#         return sys.stdin.read()

#     try:
#         with open(path, "r", encoding="utf-8") as f:
#             diff = f.read()
#     except OSError as exc:
#         raise RuntimeError(
#             f"Could not read review input: {exc}"
#         ) from exc

#     size = len(diff.encode("utf-8"))
#     if size > MAX_DIFF_SIZE_BYTES:
#         print(
#             f"Warning: diff file is {size // (1024 * 1024)} MB, "
#             f"which may cause high memory usage."
#         )

#     return diff


# def validate_skills(raw):
#     """Parse and deduplicate a comma-separated skill list."""
#     skills = [
#         skill.strip()
#         for skill in raw.split(",")
#         if skill.strip()
#     ]

#     if not skills:
#         raise RuntimeError(
#             "No review skills were selected."
#         )

#     return list(dict.fromkeys(skills))


# def build_payload(args, diff, skills):
#     """Construct the JSON payload for the backend API."""
#     return {
#         "repository": args.repository,
#         "pull_request": args.pr_number,
#         "review_mode": args.review_mode,
#         "skills": skills,
#         "diff": diff,
#         "repository_context": args.repository_context,
#     }


# def print_request_summary(args, skills, quiet=False):
#     """Print the review request configuration to stdout."""
#     if quiet:
#         return

#     print()
#     print("======================================")
#     print("AI CODE REVIEW REQUEST")
#     print("======================================")
#     print(f"Repository       : {args.repository}")
#     print(f"Pull Request     : #{args.pr_number}")
#     print(f"Review Mode      : {args.review_mode}")
#     print("Selected Skills  :")

#     for skill in skills:
#         print(f"  - {skill}")

#     print("======================================")
#     print()
#     print("Sending review request to backend...")
#     print(f"API URL: {args.api_url}")


# # def call_backend(api_url, payload):
# #     """Send the review request and return the response object."""
# #     try:
# #         response = requests.post(
# #             api_url,
# #             json=payload,
# #             timeout=900,
# #         )
# #         response.raise_for_status()
# #     except requests.exceptions.Timeout:
# #         raise RuntimeError(
# #             "AI Code Review backend request timed out."
# #         ) from None
# #     except requests.exceptions.ConnectionError:
# #         raise RuntimeError(
# #             "Could not connect to AI Code Review backend."
# #         ) from None
# #     except requests.exceptions.HTTPError as exc:
# #         status = exc.response.status_code if exc.response is not None else "unknown"
# #         body = exc.response.text if exc.response is not None else "no response body"
# #         print(f"Backend returned an HTTP error (status {status}).")
# #         print(f"Response: {body}")
# #         raise RuntimeError(
# #             "AI Code Review backend request failed."
# #         ) from exc
# #     except requests.exceptions.RequestException as exc:
# #         raise RuntimeError(
# #             f"AI Code Review request failed: {exc}"
# #         ) from exc

# #     return response
# def call_backend(api_url, payload):
#     """Send the review result to the backend completion endpoint."""

#     try:
#         response = requests.post(
#             api_url,
#             json=payload,
#             timeout=900,
#         )
#         response.raise_for_status()

#     except requests.exceptions.Timeout:
#         raise RuntimeError(
#             "AI Code Review backend request timed out."
#         ) from None

#     except requests.exceptions.ConnectionError:
#         raise RuntimeError(
#             "Could not connect to AI Code Review backend."
#         ) from None

#     except requests.exceptions.HTTPError as exc:
#         status = (
#             exc.response.status_code
#             if exc.response is not None
#             else "unknown"
#         )
#         body = (
#             exc.response.text
#             if exc.response is not None
#             else "no response body"
#         )

#         print(f"Backend returned an HTTP error (status {status}).")
#         print(f"Response: {body}")

#         raise RuntimeError(
#             "AI Code Review backend request failed."
#         ) from exc

#     except requests.exceptions.RequestException as exc:
#         raise RuntimeError(
#             f"AI Code Review request failed: {exc}"
#         ) from exc

#     return response


# def parse_response(response, quiet=False):
#     """Parse and return the JSON review from the backend response."""
#     content_type = response.headers.get("Content-Type", "")

#     if "application/json" not in content_type:
#         print("Backend returned non-JSON response:")
#         print(f"Content-Type: {content_type}")
#         print(f"Body: {response.text[:500]}")
#         raise RuntimeError(
#             "AI Code Review backend returned non-JSON response."
#         )

#     try:
#         return response.json()
#     except json.JSONDecodeError as exc:
#         print("Backend returned invalid JSON:")
#         print(response.text)
#         raise RuntimeError(
#             "AI Code Review backend returned invalid JSON."
#         ) from exc


# def save_result(review, output_path):
#     """Write the review result to the output file."""
#     try:
#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(review, f, indent=2, ensure_ascii=False)
#     except OSError as exc:
#         raise RuntimeError(
#             f"Could not write review result to {output_path}: {exc}"
#         ) from exc


# def print_result(review, output_path, quiet=False):
#     """Print the review result summary to stdout."""
#     if quiet:
#         return

#     print()
#     print("======================================")
#     print("AI CODE REVIEW COMPLETED")
#     print("======================================")
#     print(json.dumps(review, indent=2, ensure_ascii=False))
#     print()
#     print(f"Review saved to: {output_path}")


# def parse_args():
#     """Build and return the argument parser."""
#     parser = argparse.ArgumentParser(
#         description="AI Code Review Client"
#     )

#     # Core arguments
#     parser.add_argument(
#         "--diff",
#         default="-",
#         help=(
#             "Path to PR diff or review context file. "
#             "Use '-' to read from stdin."
#         )
#     )

#     parser.add_argument(
#         "--api-url",
#         required=True,
#         help="AI Code Review backend API URL"
#     )

#     parser.add_argument(
#         "--pr-number",
#         type=int,
#         default=0,
#         help="GitHub Pull Request number"
#     )

#     parser.add_argument(
#         "--repository",
#         required=True,
#         help="GitHub repository name"
#     )

#     parser.add_argument(
#     "--instance-id",
#     required=True,
#     help="Ephemeral runner instance ID",
#     )

#     # Review mode
#     parser.add_argument(
#         "--review-mode",
#         default="PR",
#         choices=["PR", "FULL_CODEBASE"],
#         help=(
#             "Review mode. "
#             "PR reviews the Pull Request diff. "
#             "FULL_CODEBASE reviews the complete repository."
#         )
#     )

#     # Selectable skills
#     parser.add_argument(
#         "--skills",
#         required=True,
#         help=(
#             "Comma-separated skill IDs selected by the user. "
#             "Example: code-review,security-review"
#         )
#     )

#     # Optional repository context
#     parser.add_argument(
#         "--repository-context",
#         default="",
#         help=(
#             "Optional additional repository context "
#             "for FULL_CODEBASE reviews."
#         )
#     )

#     # Output options
#     parser.add_argument(
#         "--output",
#         "-o",
#         default="review_result.json",
#         help="Output file path for the review result (default: review_result.json)"
#     )

#     parser.add_argument(
#         "--quiet",
#         "-q",
#         action="store_true",
#         help="Suppress stdout output; only write the result file."
#     )

#     return parser.parse_args()


# def main():
#     args = parse_args()

#     # Validate PR number early when not using the default
#     if args.pr_number < 0:
#         raise RuntimeError(
#             f"PR number must be non-negative, got: {args.pr_number}"
#         )

#     # Read diff input (file or stdin)
#     diff = read_input(args.diff)

#     # Validate and deduplicate skills
#     skills = validate_skills(args.skills)

#     # Summarize what we're about to send
#     print_request_summary(args, skills, quiet=args.quiet)

#     # Build and send the payload
#     payload = build_payload(args, diff, skills)
#     completion_url = (
#     f"{args.api_url.rstrip('/')}"
#     f"/api/ephemeral-runner/{args.instance_id}/complete"
#     )

#     print(f"Sending review result to backend: {completion_url}")

#     response = call_backend(completion_url, payload)
#     #response = call_backend(args.api_url, payload)

#     # Parse and persist the result
#     review = parse_response(response, quiet=args.quiet)
#     save_result(review, args.output)
#     print_result(review, args.output, quiet=args.quiet)


# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from claude_api import review_code

import requests


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def read_text_file(file_path: str) -> str:
    """
    Read a UTF-8 text file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    content = path.read_text(encoding="utf-8")

    if not content.strip():
        raise ValueError(
            f"File is empty: {file_path}"
        )

    return content


def parse_skills(skills_value: str | None) -> list[str]:
    """
    Convert comma-separated skills into a list.

    Examples:
        security,quality,performance
        security, quality, performance
    """
    if not skills_value:
        return []

    return [
        skill.strip()
        for skill in skills_value.split(",")
        if skill.strip()
    ]


def build_payload(
    args: argparse.Namespace,
    diff: str,
) -> dict[str, Any]:
    """
    Build the payload sent to the AI review backend.
    """
    return {
        "repository": args.repository,
        "pull_request": int(args.pr_number),
        "review_mode": args.review_mode,
        "skills": parse_skills(args.skills),
        "diff": diff,
        "repository_context": args.repository_context or "",
    }


# def validate_api_url(api_url: str) -> str:
#     """
#     Validate and normalize the AI review API URL.

#     The URL must point to the actual FastAPI POST review endpoint.

#     Example:
#         http://192.168.1.100:8000/api/code-review

#     Invalid example:
#         http://192.168.1.100:8000
#     """
#     if not api_url or not api_url.strip():
#         raise ValueError(
#             "API URL is not configured. "
#             "Pass --api-url or set API_URL."
#         )

#     normalized_url = api_url.strip().rstrip("/")

#     parsed_url = urlparse(normalized_url)

#     if parsed_url.scheme not in {"http", "https"}:
#         raise ValueError(
#             "API URL must start with http:// or https://. "
#             f"Received: {normalized_url}"
#         )

#     if not parsed_url.netloc:
#         raise ValueError(
#             f"Invalid API URL: {normalized_url}"
#         )

#     # Prevent accidentally posting to the backend root.
#     if parsed_url.path in {"", "/"}:
#         raise ValueError(
#             "API_URL points to the backend root. "
#             "Configure the complete AI review POST endpoint. "
#             "For example: "
#             "http://backend-host:8000/api/code-review. "
#             f"Current value: {normalized_url}"
#         )

#     if parsed_url.path.endswith("/docs"):
#         raise ValueError(
#             "API_URL points to Swagger documentation. "
#             "Use the actual POST review endpoint instead."
#         )

#     if parsed_url.path.endswith("/openapi.json"):
#         raise ValueError(
#             "API_URL points to the OpenAPI schema. "
#             "Use the actual POST review endpoint instead."
#         )

#     return normalized_url


# def call_review_backend(
#     api_url: str,
#     payload: dict[str, Any],
# ) -> dict[str, Any]:
#     """
#     Call the AI code review API.

#     api_url must be the complete POST endpoint.

#     Do not pass:
#         http://localhost:8000

#     Do not pass:
#         /api/ephemeral-runner/{instance_id}/complete
#     """
#     api_url = validate_api_url(api_url)

#     logger.info("Sending review request to backend")
#     logger.info("Review API URL: %s", api_url)

#     try:
#         response = requests.post(
#             api_url,
#             json=payload,
#             timeout=900,
#         )

#         logger.info(
#             "Backend response status: %s",
#             response.status_code,
#         )

#         if response.status_code == 405:
#             response_text = response.text[:2000]

#             raise RuntimeError(
#                 "Backend returned HTTP 405 Method Not Allowed. "
#                 "The configured API_URL does not support POST. "
#                 "Check that it points to the actual AI review endpoint. "
#                 f"URL: {api_url}. "
#                 f"Response: {response_text}"
#             )

#         if response.status_code == 404:
#             response_text = response.text[:2000]

#             raise RuntimeError(
#                 "Backend returned HTTP 404 Not Found. "
#                 "Check the FastAPI review route. "
#                 f"URL: {api_url}. "
#                 f"Response: {response_text}"
#             )

#         response.raise_for_status()

#     except requests.exceptions.Timeout as exc:
#         logger.exception(
#             "Review backend request timed out"
#         )

#         raise RuntimeError(
#             "Review backend request timed out after 900 seconds"
#         ) from exc

#     except requests.exceptions.ConnectionError as exc:
#         logger.exception(
#             "Could not connect to review backend"
#         )

#         raise RuntimeError(
#             f"Could not connect to review backend: {api_url}"
#         ) from exc

#     except requests.exceptions.HTTPError as exc:
#         response_text = ""

#         if exc.response is not None:
#             response_text = exc.response.text[:2000]

#         status_code = (
#             exc.response.status_code
#             if exc.response is not None
#             else "unknown"
#         )

#         logger.error(
#             "Review backend returned HTTP error: %s",
#             response_text,
#         )

#         raise RuntimeError(
#             f"Review backend HTTP error: {status_code}. "
#             f"Response: {response_text}"
#         ) from exc

#     except requests.exceptions.RequestException as exc:
#         logger.exception(
#             "Review backend request failed"
#         )

#         raise RuntimeError(
#             "Review backend request failed"
#         ) from exc

#     try:
#         result = response.json()

#     except ValueError as exc:
#         logger.error(
#             "Backend returned invalid JSON: %s",
#             response.text[:2000],
#         )

#         raise RuntimeError(
#             "Review backend returned invalid JSON"
#         ) from exc

#     if not isinstance(result, dict):
#         raise RuntimeError(
#             "Review backend response must be a JSON object"
#         )

#     return result


def validate_review_result(
    review: dict[str, Any],
) -> None:
    """
    Validate the minimum expected review response structure.
    """
    required_fields = [
        "status",
        "score",
        "summary",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in review
    ]

    if missing_fields:
        raise ValueError(
            "Review response is missing required fields: "
            + ", ".join(missing_fields)
        )

    if "findings" in review and not isinstance(
        review["findings"],
        list,
    ):
        raise ValueError(
            "Review response field 'findings' must be a list"
        )


def save_review_result(
    review: dict[str, Any],
    output_file: str,
) -> None:
    """
    Save review response to review_result.json.
    """
    output_path = Path(output_file)

    output_path.write_text(
        json.dumps(
            review,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    logger.info(
        "Review result saved to %s",
        output_path.resolve(),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run AI code review and save the review result"
        )
    )

    parser.add_argument(
        "--diff",
        required=True,
        help="Path to diff or full-code input file",
    )

    parser.add_argument(
        "--api-url",
        default=os.getenv("API_URL"),
        help=(
            "Complete AI review POST endpoint. "
            "Can also be provided using API_URL."
        ),
    )

    parser.add_argument(
        "--pr-number",
        required=True,
        help=(
            "Pull request number. "
            "Use 0 for full codebase review."
        ),
    )

    parser.add_argument(
        "--repository",
        required=True,
        help="GitHub repository in owner/name format",
    )

    parser.add_argument(
        "--review-mode",
        default=os.getenv("REVIEW_MODE", "PR"),
        choices=[
            "PR",
            "FULL_CODEBASE",
        ],
        help="Review mode",
    )

    parser.add_argument(
        "--skills",
        default=os.getenv("REVIEW_SKILLS", ""),
        help="Comma-separated review skills",
    )

    parser.add_argument(
        "--repository-context",
        default=os.getenv("REPOSITORY_CONTEXT", ""),
        help="Branch or repository context",
    )

    parser.add_argument(
        "--output-file",
        default="review_result.json",
        help="Output JSON file",
    )

    args = parser.parse_args()

    try:
        diff = read_text_file(args.diff)

        payload = build_payload(
            args=args,
            diff=diff,
        )

        logger.info(
            "Starting AI review. mode=%s repository=%s pr=%s",
            args.review_mode,
            args.repository,
            args.pr_number,
        )

        # review = call_review_backend(
        #     api_url=args.api_url,
        #     payload=payload,
        # )
        selected_skills = parse_skills(args.skills)

        review = review_code(
            diff=diff,
            repository=args.repository,
            pr_number=int(args.pr_number),
            review_mode=args.review_mode,
            skills=selected_skills,
            repository_context=args.repository_context or "",
        )
        validate_review_result(review)

        save_review_result(
            review=review,
            output_file=args.output_file,
        )

        print(
            json.dumps(
                review,
                indent=2,
                ensure_ascii=False,
            )
        )

        return 0

    except Exception as exc:
        logger.exception(
            "AI code review failed: %s",
            exc,
        )

        error_result = {
            "status": "ERROR",
            "score": 0,
            "summary": str(exc),
            "findings": [],
        }

        try:
            save_review_result(
                review=error_result,
                output_file=args.output_file,
            )

        except Exception:
            logger.exception(
                "Could not save error review result"
            )

        return 1


if __name__ == "__main__":
    sys.exit(main())