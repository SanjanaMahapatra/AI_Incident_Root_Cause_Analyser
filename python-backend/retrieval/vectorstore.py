import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
load_dotenv()

PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR")

api_key=os.getenv("OPENAI_API_KEY")

chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=api_key,
    model_name="text-embedding-ada-002"
)

def get_collection():
    return chroma_client.get_or_create_collection(
        name="incident_knowledge",
        embedding_function=openai_ef
    )

def retrieve_context(query: str, k: int = 3):
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=k)
    from langchain_core.documents import Document
    documents = []
    if results['documents']:
        for i, doc in enumerate(results['documents'][0]):
            documents.append(Document(
                page_content=doc,
                metadata={"id": results['ids'][0][i] if results['ids'] else {}}
            ))
    return documents

def add_documents(docs):
    """Add documents to the vector store."""
    collection = get_collection()
    for doc in docs:
        collection.add(
            documents=[doc.page_content],
            metadatas=[doc.metadata],
            ids=[doc.metadata.get("id", str(hash(doc.page_content)))]
        )