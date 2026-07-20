from langchain_core.documents import Document
from pathlib import Path
import json

PROCESSED_DATA_PATH = Path("data/02_github_issues_processed.json")


def create_documents():
    print("Creating documents...")

    documents = []

    with open(PROCESSED_DATA_PATH, "r", encoding="utf-8") as f:
        processed = json.load(f)

    print(f"Loaded {len(processed)} issues.")

    for issue in processed:
        text = (
            f"Title: {issue['title']}\n\n"
            f"Labels: {', '.join(issue['labels'])}\n\n"
            f"Body:\n{issue['body']}"
        )

        document = Document(
            page_content=text,
            metadata={
                "number": issue["number"],
                "author": issue["author"],
                "state": issue["state"],
                "comments": issue["comments"],
                "created_at": issue["created_at"],
                "updated_at": issue["updated_at"],
                "html_url": issue["html_url"],
            },
        )

        documents.append(document)

    print(f"Created {len(documents)} documents.")

    return documents