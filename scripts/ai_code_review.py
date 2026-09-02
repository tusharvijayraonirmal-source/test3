import argparse
import requests
import json


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--diff", required=True)
    parser.add_argument("--api-url", required=True)
    parser.add_argument("--pr-number", required=True)
    parser.add_argument("--repository", required=True)

    args = parser.parse_args()

    with open(args.diff, "r", encoding="utf-8") as f:
        diff = f.read()

    payload = {
        "repository": args.repository,
        "pull_request": int(args.pr_number),
        "diff": diff
    }

    response = requests.post(
        args.api_url,
        json=payload,
        timeout=900
    )

    response.raise_for_status()

    review = response.json()

    with open(
        "review_result.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            review,
            f,
            indent=2
        )

    print(json.dumps(review, indent=2))


if __name__ == "__main__":
    main()