
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from app.agents.research_agent import research

router = APIRouter(prefix="/research")

class TopicRequest(BaseModel):
    topic: str
    selectedFiles: Optional[List[str]] = None

@router.post("/topic")
async def run(request: TopicRequest):
    try:
        if request.selectedFiles:
            print(f"Research using selected files: {request.selectedFiles}")
        result = await research(request.topic, selected_files=request.selectedFiles)
        return {
            "result": result.get("research", result),
            "topic": request.topic,
            "success": result.get("success", True) if isinstance(result, dict) else True
        }
    except Exception as e:
        return {
            "result": f"Error: {str(e)}",
            "topic": request.topic,
            "success": False
        }
