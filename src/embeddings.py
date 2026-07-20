from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():
    print("Loading embedding model...")

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )