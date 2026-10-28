# scripts/send_review_email.py

import argparse
import json
import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--review-file", required=True)
    parser.add_argument("--pr-number", required=True)
    parser.add_argument("--repository", required=True)

    args = parser.parse_args()

    with open(args.review_file) as f:
        review = json.load(f)

    status = review["status"]

    subject = (
        f"[AI CODE REVIEW] "
        f"PR #{args.pr_number} - {status}"
    )

    body = f"""
Repository: {args.repository}

Pull Request: #{args.pr_number}

Status:
{status}

Score:
{review["score"]}/10

Summary:
{review["summary"]}

Findings:
"""

    for finding in review.get("findings", []):

        body += f"""

    [{finding.get("severity", "UNKNOWN")}]
    {finding.get("issue", "Code review finding")}

    File:
    {finding.get("file", "unknown")}

    Line:
    {finding.get("line", "unknown")}

    Description:
    {finding.get("explanation", "No explanation provided.")}

    Suggestion:
    {finding.get("suggested_fix", "No suggestion provided.")}


"""

    message = MIMEMultipart()

    message["From"] = os.environ["SMTP_USERNAME"]
    message["To"] = os.environ["REVIEWER_EMAIL"]
    message["Subject"] = subject

    message.attach(
        MIMEText(body, "plain")
    )

    with smtplib.SMTP(
        os.environ["SMTP_HOST"],
        int(os.environ["SMTP_PORT"])
    ) as server:

        server.starttls()

        server.login(
            os.environ["SMTP_USERNAME"],
            os.environ["SMTP_PASSWORD"]
        )

        server.send_message(message)


if __name__ == "__main__":
    main()