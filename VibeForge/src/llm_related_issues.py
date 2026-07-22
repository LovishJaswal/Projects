from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPEN_ROUTER_BASE_URL"),
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
)


def analyze_related_issues(query, retrieved_issues):
    print("Analyzing related issues...")

    if retrieved_issues is None:
        return """
# Related Issues Analysis

The issue description is too brief to analyze related issues.

Please provide more details about:
- What happened
- Expected behavior
- Actual behavior
- Steps to reproduce (if applicable)
"""

    context = []

    for rank, (doc, score) in enumerate(retrieved_issues, start=1):
        issue_text = doc.page_content[:1500]

        context.append(
            f"""
Candidate Rank: {rank}

Issue #{doc.metadata["number"]}

Vector Distance: {score:.4f}

{issue_text}

State: {doc.metadata["state"]}
Comments: {doc.metadata["comments"]}
URL: {doc.metadata["html_url"]}
"""
        )

    context = "\n\n".join(context)

    print(f"Sending {len(retrieved_issues)} issues to the LLM...")

    prompt = f"""
You are an experienced open-source software engineer and GitHub maintainer.

================ USER ISSUE ================

{query}

================ RETRIEVED ISSUES ================

{context}

Your task is to analyze ONLY the retrieved issues and identify the most relevant related issues.

RULES:

1. Use ONLY the retrieved issues.
2. Never invent issue numbers.
3. Never invent URLs.
4. Never mention issues not provided above.
5. Ignore the vector distance except as a retrieval hint.
6. Rank issues based on semantic relevance.
7. Explain WHY each issue is related.
8. Do not include issues that only share superficial keywords.
9. Return at most THREE related issues.
10. If no issues are meaningfully related, say so.
11. Do NOT include the queried issue itself.

Return EXACTLY this format.

# Related Issues Analysis

## Total Related Issues
<number>

If none:

No related issues found.

Otherwise:

### Issue #<number>

**Relevance:** High | Medium | Low

**URL:** <url>

**Reason:**
Explain in 2-4 sentences why this issue is related to the user's issue.
Mention common behavior, affected component, feature, bug pattern, or similar context.

Repeat for the remaining related issues.
"""

    response = client.chat.completions.create(
        model="google/gemini-2.5-flash-lite",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an experienced GitHub maintainer. "
                    "Given a user issue and retrieved GitHub issues, "
                    "identify the most relevant related issues and explain why they are related. "
                    "Never invent issue numbers or URLs."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        max_tokens=900,
    )

    print("Related issue analysis completed.")

    return response.choices[0].message.content