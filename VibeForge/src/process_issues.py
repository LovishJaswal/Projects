from pathlib import Path
import json

RAW_DATA_PATH = Path("data/01_github_raw.json")
PROCESSED_DATA_PATH = Path("data/02_github_issues_processed.json")


def process_raw_data():
    print("Processing issues...")

    with open(RAW_DATA_PATH, "r", encoding="UTF-8") as f:
        issues = json.load(f)

    print(f"Loaded {len(issues)} issues.")

    processed = []

    for issue in issues:
        if issue.get("pull_request"):
            continue

        processed.append(clean_issue(issue))

    with open(PROCESSED_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=4)

    print(f"Processed {len(processed)} issues.")


def clean_issue(issue):
    processed_issue = {
        "number": issue["number"],
        "title": issue["title"],
        "body": issue["body"] or "",
        "state": issue["state"],
        "author": issue["user"]["login"],
        "labels": [label["name"] for label in issue["labels"]],
        "comments": issue["comments"],
        "created_at": issue["created_at"],
        "updated_at": issue["updated_at"],
        "html_url": issue["html_url"],
        "assignees": [assignee["login"] for assignee in issue["assignees"]],
        "milestone": issue["milestone"]["title"] if issue["milestone"] else None,
        "repository": issue["repository_url"].split("/")[-1],
    }

    return processed_issue