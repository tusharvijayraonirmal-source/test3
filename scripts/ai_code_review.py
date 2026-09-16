
import argparse
import sys
import requests
import json


MAX_DIFF_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB


def read_input(path):
    """Read diff content from a file path or stdin when path is '-'."""
    if path == "-":
        return sys.stdin.read()

    try:
        with open(path, "r", encoding="utf-8") as f:
            diff = f.read()
    except OSError as exc:
        raise RuntimeError(
            f"Could not read review input: {exc}"
        ) from exc

    size = len(diff.encode("utf-8"))
    if size > MAX_DIFF_SIZE_BYTES:
        print(
            f"Warning: diff file is {size // (1024 * 1024)} MB, "
            f"which may cause high memory usage."
        )

    return diff


def validate_skills(raw):
    """Parse and deduplicate a comma-separated skill list."""
    skills = [
        skill.strip()
        for skill in raw.split(",")
        if skill.strip()
    ]

    if not skills:
        raise RuntimeError(
            "No review skills were selected."
        )

    return list(dict.fromkeys(skills))


def build_payload(args, diff, skills):
    """Construct the JSON payload for the backend API."""
    return {
        "repository": args.repository,
        "pull_request": args.pr_number,
        "review_mode": args.review_mode,
        "skills": skills,
        "diff": diff,
        "repository_context": args.repository_context,
    }


def print_request_summary(args, skills, quiet=False):
    """Print the review request configuration to stdout."""
    if quiet:
        return

    print()
    print("======================================")
    print("AI CODE REVIEW REQUEST")
    print("======================================")
    print(f"Repository       : {args.repository}")
    print(f"Pull Request     : #{args.pr_number}")
    print(f"Review Mode      : {args.review_mode}")
    print("Selected Skills  :")

    for skill in skills:
        print(f"  - {skill}")

    print("======================================")
    print()
    print("Sending review request to backend...")
    print(f"API URL: {args.api_url}")


def call_backend(api_url, payload):
    """Send the review request and return the response object."""
    try:
        response = requests.post(
            api_url,
            json=payload,
            timeout=900,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError(
            "AI Code Review backend request timed out."
        ) from None
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not connect to AI Code Review backend."
        ) from None
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        body = exc.response.text if exc.response is not None else "no response body"
        print(f"Backend returned an HTTP error (status {status}).")
        print(f"Response: {body}")
        raise RuntimeError(
            "AI Code Review backend request failed."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"AI Code Review request failed: {exc}"
        ) from exc

    return response


def parse_response(response, quiet=False):
    """Parse and return the JSON review from the backend response."""
    content_type = response.headers.get("Content-Type", "")

    if "application/json" not in content_type:
        print("Backend returned non-JSON response:")
        print(f"Content-Type: {content_type}")
        print(f"Body: {response.text[:500]}")
        raise RuntimeError(
            "AI Code Review backend returned non-JSON response."
        )

    try:
        return response.json()
    except json.JSONDecodeError as exc:
        print("Backend returned invalid JSON:")
        print(response.text)
        raise RuntimeError(
            "AI Code Review backend returned invalid JSON."
        ) from exc


def save_result(review, output_path):
    """Write the review result to the output file."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(review, f, indent=2, ensure_ascii=False)
    except OSError as exc:
        raise RuntimeError(
            f"Could not write review result to {output_path}: {exc}"
        ) from exc


def print_result(review, output_path, quiet=False):
    """Print the review result summary to stdout."""
    if quiet:
        return

    print()
    print("======================================")
    print("AI CODE REVIEW COMPLETED")
    print("======================================")
    print(json.dumps(review, indent=2, ensure_ascii=False))
    print()
    print(f"Review saved to: {output_path}")


def parse_args():
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="AI Code Review Client"
    )

    # Core arguments
    parser.add_argument(
        "--diff",
        default="-",
        help=(
            "Path to PR diff or review context file. "
            "Use '-' to read from stdin."
        )
    )

    parser.add_argument(
        "--api-url",
        required=True,
        help="AI Code Review backend API URL"
    )

    parser.add_argument(
        "--pr-number",
        type=int,
        default=0,
        help="GitHub Pull Request number"
    )

    parser.add_argument(
        "--repository",
        required=True,
        help="GitHub repository name"
    )

    # Review mode
    parser.add_argument(
        "--review-mode",
        default="PR",
        choices=["PR", "FULL_CODEBASE"],
        help=(
            "Review mode. "
            "PR reviews the Pull Request diff. "
            "FULL_CODEBASE reviews the complete repository."
        )
    )

    # Selectable skills
    parser.add_argument(
        "--skills",
        required=True,
        help=(
            "Comma-separated skill IDs selected by the user. "
            "Example: code-review,security-review"
        )
    )

    # Optional repository context
    parser.add_argument(
        "--repository-context",
        default="",
        help=(
            "Optional additional repository context "
            "for FULL_CODEBASE reviews."
        )
    )

    # Output options
    parser.add_argument(
        "--output",
        "-o",
        default="review_result.json",
        help="Output file path for the review result (default: review_result.json)"
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress stdout output; only write the result file."
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Validate PR number early when not using the default
    if args.pr_number < 0:
        raise RuntimeError(
            f"PR number must be non-negative, got: {args.pr_number}"
        )

    # Read diff input (file or stdin)
    diff = read_input(args.diff)

    # Validate and deduplicate skills
    skills = validate_skills(args.skills)

    # Summarize what we're about to send
    print_request_summary(args, skills, quiet=args.quiet)

    # Build and send the payload
    payload = build_payload(args, diff, skills)
    response = call_backend(args.api_url, payload)

    # Parse and persist the result
    review = parse_response(response, quiet=args.quiet)
    save_result(review, args.output)
    print_result(review, args.output, quiet=args.quiet)


if __name__ == "__main__":
    main()

