import gradio as gr

from src.github_client import fetch_issues
from src.process_issues import process_raw_data
from src.create_documents import create_documents
from src.embeddings import get_embedding_model
from src.vector_db import create_vector_db

from src.find_similar_issues import find_similar_issues
from src.llm_issue_analyzer import analyze_issue
from src.llm_duplicate_analyzer import analyze_duplicates


def build_repository(repo_name):
    try:
        fetch_issues(repo_name)

        process_raw_data()

        documents = create_documents()

        embedding_model = get_embedding_model()

        create_vector_db(documents, embedding_model)

        return """
# ✅ Repository Indexed Successfully!

Your repository is ready for analysis.

### What's next?

➡️ Open the **Issue Analyzer** tab.

There you can:
- 📝 Analyze GitHub issues
- 🔍 Find similar issues
- 🤖 Detect possible duplicates
"""

    except Exception as e:
        return f"❌ {e}"


def analyze(query):
    if not query.strip():
        return (
            """
# 👋 No Issue Description

Please enter a GitHub issue description and click **Analyze**.
""",
            "",
        )

    issue_analysis = analyze_issue(query)

    retrieved_issues = find_similar_issues(query, k=3)

    duplicate_analysis = analyze_duplicates(query, retrieved_issues)

    return issue_analysis, duplicate_analysis


with gr.Blocks(title="VibeForge") as demo:

    gr.Markdown(
        """
# 🚀 VibeForge

### Helping Open Source Move Faster.

Index a public GitHub repository and analyze issues using AI.
"""
    )

    with gr.Tab("📦 Repository Setup"):

        gr.Markdown(
            """
Enter the GitHub repository in the format:

`owner/repository`
"""
        )

        repo = gr.Textbox(
            label="Repository",
            placeholder="owner/repository",
        )

        setup_btn = gr.Button(
            "🚀 Index Repository",
            variant="primary",
        )

        setup_output = gr.Markdown(
            """
### Ready to Index

Enter a repository name above and click **Index Repository**.

⚠️ **Note:** Creating embeddings and the vector database may take a few minutes depending on the repository size.
"""
        )

        setup_btn.click(
            fn=build_repository,
            inputs=repo,
            outputs=setup_output,
            show_progress="full",
        )

    with gr.Tab("🔍 Issue Analyzer"):

        gr.Markdown(
            """
Describe a GitHub issue below and click **Analyze**.

VibeForge will:
- 📝 Analyze the issue
- 🔍 Search for similar issues
- 🤖 Detect possible duplicates
"""
        )

        query = gr.Textbox(
            lines=8,
            label="Issue Description",
            placeholder="Describe the GitHub issue...",
        )

        analyze_btn = gr.Button(
            "🔎 Analyze",
            variant="primary",
        )

        issue_output = gr.Markdown(label="Issue Analysis")

        duplicate_output = gr.Markdown(label="Duplicate Analysis")

        analyze_btn.click(
            fn=analyze,
            inputs=query,
            outputs=[
                issue_output,
                duplicate_output,
            ],
            show_progress="full",
        )


if __name__ == "__main__":
    demo.launch()