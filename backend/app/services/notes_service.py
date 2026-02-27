
from datetime import datetime
from typing import List, Dict

notes: List[Dict] = []

async def create_note(text: str):
    note = {
        "id": str(len(notes) + 1),
        "text": text,
        "timestamp": datetime.now().isoformat()
    }
    notes.append(note)
    return {"status": "saved", "note": note}

async def get_notes():
    return notes
