import os
import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from document import Document
from config import settings
from pdf_processor import extract_text_from_pdf

class DocumentService:
    @staticmethod
    async def save_document(file: UploadFile, db: Session):
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        file_name, file_extension = os.path.splitext(file.filename)
        unique_name = f"{file_name}_{uuid.uuid4().hex}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_name)
        
        try:
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            text_content = extract_text_from_pdf(file_path)
            
            db_document = Document(
                filename=unique_name,
                filepath=file_path,
                text_content=text_content
            )
            db.add(db_document)
            db.commit()
            db.refresh(db_document)
            
            return db_document
        
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_document(document_id: int, db: Session):
        return db.query(Document).filter(Document.id == document_id).first()

    @staticmethod
    def get_all_documents(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Document).offset(skip).limit(limit).all()


