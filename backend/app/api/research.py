
from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.research_agent import research

router = APIRouter(prefix="/research")

class TopicRequest(BaseModel):
    topic: str

@router.post("/topic")
async def run(request: TopicRequest):
    try:
        result = await research(request.topic)
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
