from langchain_community.vectorstores import Chroma
from .embeddings import embeddings
import os

PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")

def get_vectorstore():
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="incident_knowledge"
    )

def add_documents(docs):
    """Add runbook/knowledge docs to vector store (pre‑ingestion)."""
    vs = get_vectorstore()
    vs.add_documents(docs)
    vs.persist()

def retrieve_context(query: str, k: int = 3):
    vs = get_vectorstore()
    return vs.similarity_search(query, k=k)