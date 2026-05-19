from langchain_core.documents import Document
from retrieval.vectorstore import add_documents

def ingest_runbook(title: str, content: str):
    """Add a runbook or knowledge document to the vector store."""
    doc = Document(page_content=content, metadata={"title": title})
    add_documents([doc])