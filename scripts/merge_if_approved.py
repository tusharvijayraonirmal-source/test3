# scripts/merge_if_approved.py

import argparse
import json
import subprocess


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--review-file", required=True)
    parser.add_argument("--pr-number", required=True)

    args = parser.parse_args()

    with open(args.review_file) as f:
        review = json.load(f)

    if review["status"] != "APPROVED":

        print(
            "AI review did not approve PR. "
            "Merge skipped."
        )

        return

    print(
        f"AI approved PR #{args.pr_number}. "
        "Attempting merge."
    )

    subprocess.run(
        [
            "gh",
            "pr",
            "merge",
            args.pr_number,
            "--squash",
            "--auto"
        ],
        check=True
    )


if __name__ == "__main__":
    main()