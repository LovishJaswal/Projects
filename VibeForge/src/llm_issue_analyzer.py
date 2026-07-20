from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPEN_ROUTER_BASE_URL"),
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
)


def analyze_issue(query: str):
    print("Analyzing issue...")

    prompt = f"""
        You are an experienced open-source software engineer and GitHub maintainer.

        Your task is to analyze ONLY the issue information provided by the user.

        Rules:
        - Do NOT invent missing details.
        - Do NOT assume the programming language, framework, library, or repository unless explicitly mentioned.
        - If the input is too short or lacks enough context (for example, only an issue number, a title, or random text), clearly state that there is insufficient information.
        - Base every conclusion only on the provided issue description.

        Issue Description:
        {query}

        Respond ONLY in Markdown using exactly the following format.

        # Issue Analysis

        ## Summary
        Write a concise 2–3 sentence summary.
        If there is insufficient information, state that explicitly.

        ## Category
        Choose exactly one:
        - Bug
        - Feature Request
        - Documentation
        - Performance
        - Refactor
        - Question
        - Other

        If uncertain, choose **Other**.

        ## Severity
        Choose exactly one:
        - Low
        - Medium
        - High
        - Critical

        If severity cannot be determined, write:
        Unknown

        ## Possible Root Cause
        Explain the most likely cause using only the provided information.
        If it cannot be inferred, write:
        Not enough information.

        ## Suggested Labels
        Return 2–5 GitHub labels as bullet points.
        If insufficient information, return:
        - needs-information

        ## Recommended Next Step
        Provide exactly one actionable recommendation.
        If insufficient information, ask the reporter to provide a reproducible example or more details.
        """

    response = client.chat.completions.create(
        model="google/gemini-2.5-flash-lite",
        messages=[
            {
                "role": "system",
                "content": "You are an expert GitHub issue analyzer."
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        max_tokens=500,
    )

    print("Issue analysis completed.")

    return response.choices[0].message.content