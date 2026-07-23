from openai import OpenAI
from dotenv import load_dotenv
import os
 
from src.embeddings import get_embedding_model
from src.vector_db import load_vector_db
 
load_dotenv()
 
client = OpenAI(
    base_url=os.getenv("OPEN_ROUTER_BASE_URL"),
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
)
 
HYDE_WORD_THRESHOLD = 20
 
 
def is_query_too_vague(query: str) -> bool:
    """
    Returns True if the user's issue description is too short
    to perform reliable duplicate detection.
    """
    query = query.strip()
 
    if len(query) < 15:
        return True
 
    if len(query.split()) < 3:
        return True
 
    return False
 
 
def is_query_already_detailed(query: str) -> bool:
    """
    Returns True if the query already reads like a full issue description
    (title + body, several sentences, etc.), in which case we should embed
    it directly instead of rewriting it via HyDE.
    """
    return len(query.strip().split()) >= HYDE_WORD_THRESHOLD
 
 
def hyde_query(query: str) -> str:
    """
    Generate a hypothetical GitHub issue to improve semantic retrieval.
    """
 
    print("Generating HyDE query...")
 
    prompt = f"""
        You are helping retrieve similar GitHub issues.
        
        Given the user's issue, write the GitHub issue that would most likely exist in
        an open-source repository.
        
        Rules:
        - Preserve the user's intent.
        - Do NOT invent unrelated features.
        - Do NOT assume a language, framework, or repository unless explicitly mentioned.
        - Expand the description naturally.
        - Mention expected behavior, current behavior, possible technical context, and
        relevant terminology only if supported by the user's input.
        - Keep it between 100 and 180 words.
        - Output ONLY the hypothetical GitHub issue.
        
        User Issue:
        {query}
        """
 
    response = client.chat.completions.create(
        model="google/gemini-2.5-flash-lite",
        messages=[
            {
                "role": "system",
                "content": "You generate hypothetical GitHub issues for semantic retrieval."
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        max_tokens=300,
    )
 
    return response.choices[0].message.content.strip()
 
 
def find_similar_issues(query: str, k: int = 10):
    print("Finding similar issues...")
 
    if is_query_too_vague(query):
        print("Issue description is too vague for duplicate detection.")
        return None
 
    if is_query_already_detailed(query):
        print("Query is already detailed; skipping HyDE expansion.")
        search_query = query
    else:
        search_query = hyde_query(query)
 
    print("\n================ ORIGINAL QUERY ================\n")
    print(query)
 
    print("\n================ SEARCH QUERY ====================\n")
    print(search_query)
 
    embedding_model = get_embedding_model()
    vectorstore = load_vector_db(embedding_model)
 
    results = vectorstore.similarity_search_with_score(
        query=search_query,
        k=k,
    )
 
    print(f"\nFound {len(results)} similar issues.\n")
 
    for i, (doc, score) in enumerate(results, start=1):
        print(
            f"{i}. Issue #{doc.metadata.get('number')} | "
            f"Score: {score:.4f} | "
            f"{doc.metadata.get('title', '')}"
        )
 
    return results