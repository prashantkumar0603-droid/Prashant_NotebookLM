
import logging
from fastapi import APIRouter
from app.llm.loader import LLMManager

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health")
def health():
    status = {
        "backend": "ok",
        "ollama": "unknown"
    }
    
    try:
        # Test Ollama connection with a simple request
        llm = LLMManager().get_llm()
        # This will attempt to connect to Ollama
        llm.invoke("Hello")
        status["ollama"] = "ok"
    except Exception as e:
        logger.warning(f"Ollama health check failed: {str(e)}")
        status["ollama"] = f"error: {str(e)}"
    
    return status
