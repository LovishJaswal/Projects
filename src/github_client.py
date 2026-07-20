import requests
from pathlib import Path
import json
from dotenv import load_dotenv
import os

load_dotenv()

PAT = os.getenv("PAT")

DATA_PATH = Path("data/01_github_raw.json")


def fetch_issues(repo: str):
    print(f"Fetching issues from {repo}...")

    page = 1
    all_issues = []

    headers = {
        "Authorization": f"Bearer {PAT}",
        "Accept": "application/vnd.github+json",
    }

    while True:
        try:
            url = f"https://api.github.com/repos/{repo}/issues?page={page}&per_page=100"

            response = requests.get(
                url,
                headers=headers,
                timeout=30,
            )

            response.raise_for_status()

            issues = response.json()

            if not issues:
                break

            all_issues.extend(issues)

            print(f"Fetched page {page} ({len(all_issues)} issues so far)")

            page += 1

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch issues: {e}")

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(all_issues, f, indent=4)

    print(f"Saved {len(all_issues)} issues.")
    print("Done fetching issues.")

    return len(all_issues)