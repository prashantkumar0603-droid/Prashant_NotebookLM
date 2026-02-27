
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_store(docs):
    return FAISS.from_documents(docs, embeddings)

def load_store(path):
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
