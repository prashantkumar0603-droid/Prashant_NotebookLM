
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import documents, chat, research, notes, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="Enterprise NotebookLM Local")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(research.router, prefix="/api")
app.include_router(notes.router, prefix="/api")
app.include_router(health.router, prefix="/api")
