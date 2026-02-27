
from fastapi import APIRouter, UploadFile
from app.services.document_service import process_document

router = APIRouter(prefix="/documents")

@router.post("/upload")
async def upload(file: UploadFile):
    return await process_document(file)
