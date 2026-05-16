from langchain_core.documents import Document
from .vectorstore import get_vectorstore

def ingest_runbook(title: str, content: str):
    """Add a runbook or knowledge document to the vector store."""
    doc = Document(page_content=content, metadata={"title": title})
    vs = get_vectorstore()
    vs.add_documents([doc])
    vs.persist()