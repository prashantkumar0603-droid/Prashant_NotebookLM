
import asyncio
import logging
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from app.rag.pipeline import run_rag

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat")

class QuestionRequest(BaseModel):
    question: str
    selectedFiles: Optional[List[str]] = None

@router.post("/ask")
async def ask(request: QuestionRequest):
    logger.info(f"Chat request received: {request.question}")
    if request.selectedFiles:
        logger.info(f"Using selected files: {request.selectedFiles}")
    
    try:
        # Run RAG with timeout of 35 seconds (LLM has 30 second timeout + buffer)
        result = await asyncio.wait_for(
            run_rag(request.question, selected_files=request.selectedFiles),
            "answer": result.get("answer", "No answer generated"),
            "citations": result.get("citations", []),
            "success": result.get("success", True)
        }
    except asyncio.TimeoutError:
        logger.error("Chat request timed out after 35 seconds")
        return {
            "answer": "Request timed out. Make sure Ollama service is running and responsive.",
            "citations": [],
            "success": False
        }
    except Exception as e:
        logger.error(f"Chat request error: {str(e)}", exc_info=True)
        return {
            "answer": f"Error: {str(e)}",
            "citations": [],
            "success": False
        }
