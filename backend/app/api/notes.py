
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.notes_service import create_note, get_notes

router = APIRouter(prefix="/notes")

class NoteRequest(BaseModel):
    text: str

@router.post("/create")
async def create(request: NoteRequest):
    try:
        result = await create_note(request.text)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e), "success": False}

@router.get("/list")
async def list_notes():
    try:
        notes = await get_notes()
        return notes
    except Exception as e:
        return {"error": str(e), "success": False}
