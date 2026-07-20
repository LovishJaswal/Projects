from src.embeddings import get_embedding_model
from src.vector_db import load_vector_db


def find_similar_issues(query, k=5):
    print("Finding similar issues...")

    embedding_model = get_embedding_model()
    vectorstore = load_vector_db(embedding_model)

    results = vectorstore.similarity_search_with_score(
        query=query,
        k=k,
    )

    print(f"Found {len(results)} similar issues.")

    return results