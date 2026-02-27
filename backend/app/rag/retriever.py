
from app.vectorstore.faiss_store import load_store

def retrieve_docs(query):
    store = load_store("data/vectorstore")
    return store.similarity_search(query, k=4)
