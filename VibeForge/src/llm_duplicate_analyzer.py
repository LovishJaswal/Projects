from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPEN_ROUTER_BASE_URL"),
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
)


def analyze_duplicates(query, retrieved_issues):
    print("Analyzing duplicate issues...")

    context = []

    for doc, score in retrieved_issues:
        issue_text = doc.page_content[:1200]

        context.append(
            f"""
            Issue #{doc.metadata["number"]}
            Similarity Score: {score:.4f}

            {issue_text}

            State: {doc.metadata["state"]}
            Comments: {doc.metadata["comments"]}
            URL: {doc.metadata["html_url"]}
            """
        )

    context = "\n\n".join(context)

    print(f"Sending {len(retrieved_issues)} issues to the LLM...")

    prompt = f"""
        You are an experienced GitHub maintainer responsible for triaging issues.

        User Issue:
        {query}

        Retrieved Candidate Issues:
        {context}

        Your task is to determine which retrieved issues are likely duplicates.

        Rules:
        - Compare ONLY against the retrieved candidate issues.
        - Never invent issue numbers.
        - Never mention issues that are not present in the retrieved context.
        - If none of the retrieved issues are sufficiently similar, report zero duplicates.
        - Base your reasoning on problem similarity, not identical wording.

        Respond ONLY in Markdown using exactly the following format.

        # Duplicate Analysis

        ## Total Likely Duplicates
        <number>

        ## Likely Duplicates

        ### Issue #<number>

        **Confidence:** High | Medium | Low

        **Reason:**
        Explain in 2–3 sentences why this candidate is or is not a likely duplicate.

        (repeat for every likely duplicate)

        If there are no likely duplicates, respond exactly as:

        # Duplicate Analysis

        ## Total Likely Duplicates
        0

        No likely duplicates were found.
        """

    response = client.chat.completions.create(
        model="gemini-2.5-flash-lite",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at identifying duplicate GitHub issues.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        max_tokens=500,
    )

    print("Duplicate analysis completed.")

    return response.choices[0].message.content