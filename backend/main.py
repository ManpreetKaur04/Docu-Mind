import os
from typing import Optional, List
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import google.generativeai as genai
from config import settings
from pdf_processor import extract_text_from_pdf
from qa_service import QAService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create required directories
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True)

# Initialize Google AI
genai.configure(api_key=settings.GOOGLE_API_KEY)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize QA service
qa_service = QAService()

class QuestionRequest(BaseModel):
    question: str
    file_id: str
    chat_history: Optional[List] = []

@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Extract text
        text = extract_text_from_pdf(file_path)
        
        # Split text into chunks
        text_chunks = [text[i:i+settings.CHUNK_SIZE] for i in range(0, len(text), settings.CHUNK_SIZE)]
        
        # Create vector store
        vector_store_path = await qa_service.create_vector_store(text_chunks, file_id)
        
        return {
            "message": "Document processed successfully",
            "file_id": file_id,
            "chars_extracted": len(text),
            "vector_store_path": vector_store_path
        }
    
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/qa/ask")
async def ask_question(request: QuestionRequest):
    try:
        logger.info(f"Received request: {request}")
        result = await qa_service.get_answer(
            question=request.question,
            file_id=request.file_id,
            chat_history=request.chat_history
        )
        return result
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Vector store not found. Please upload the document first."
        )
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        if "Developer instruction is not enabled" in str(e):
            return {
                "answer": "Error: Gemini Pro API access needs to be enabled for your project. Please visit the Google AI Studio to enable it.",
                "error": str(e),
                "sources": []
            }
        return {
            "answer": "I encountered an error while processing your question.",
            "error": str(e),
            "sources": []
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)