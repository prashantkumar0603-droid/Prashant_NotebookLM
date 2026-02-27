
from app.parsers.pdf_parser import parse_pdf
from app.rag.pipeline import run_rag
from app.vectorstore.faiss_store import create_store
from langchain_text_splitters import RecursiveCharacterTextSplitter

async def process_document(file):
    text = parse_pdf(file.file)
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    docs = splitter.create_documents([text])
    store = create_store(docs)
    store.save_local("data/vectorstore")
    return {"status": "indexed"}
