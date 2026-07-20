from pathlib import Path
import shutil

from langchain_chroma import Chroma

CHROMA_DB_PATH = Path("data/chroma_db")


def create_vector_db(documents, embedding_model):
    print("Creating vector database...")

    if CHROMA_DB_PATH.exists():
        shutil.rmtree(CHROMA_DB_PATH)
        print("Removed old database.")

    print("Generating embeddings and indexing documents... This may take a minute.")

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=str(CHROMA_DB_PATH),
    )

    print("Vector database created.")

    return vectorstore


def load_vector_db(embedding_model):
    print("Loading vector database...")

    vectorstore = Chroma(
        persist_directory=str(CHROMA_DB_PATH),
        embedding_function=embedding_model,
    )

    print("Vector database loaded.")

    return vectorstore