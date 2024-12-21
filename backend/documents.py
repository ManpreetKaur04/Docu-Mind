from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from document_service import DocumentService
from database import get_db
import logging

router = APIRouter()

logging.basicConfig(level=logging.DEBUG)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        logging.debug(f"Received file: {file.filename}")
        document = await DocumentService.save_document(file, db)
        return document.to_dict()
    except Exception as e:
        logging.error(f"Error during file upload: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    try:
        logging.debug(f"Fetching document with ID: {document_id}")
        document = DocumentService.get_document(document_id, db)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return document.to_dict()
    except Exception as e:
        logging.error(f"Error fetching document: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/")
def get_documents(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    documents = DocumentService.get_all_documents(db, skip, limit)
    return [doc.to_dict() for doc in documents]
