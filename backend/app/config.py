
import os

DATA_DIR = "data"
VECTOR_DIR = "data/vectorstore"
DOCS_DIR = "data/documents"

# LLM Configuration
# Set to 'ollama' to use Ollama, 'mock' for development without external services
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
