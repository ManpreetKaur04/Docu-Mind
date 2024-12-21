# PDF Question & Answer System

A full-stack application that allows users to upload PDF documents and ask questions about their content using natural language processing.

## Features

- PDF document upload and management
- Natural language question answering based on PDF content
- Real-time processing and response
- Intuitive user interface with error handling
- Document selection and management


┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Frontend     │     │    Backend      │     │    Storage      │
│    (React.js)   │────▶│    (FastAPI)    │────▶│   (SQL)         │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                              │
                              │
                        ┌─────▼─────┐
                        │  PDF Store│
                        │ (Uploads) │
                        └───────────┘

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React.js
- **Database**: SQLite
- **NLP Processing**: LangChain with OpenAI
- **PDF Processing**: PyMuPDF
- **Vector Store**: Chroma
- **UI Components**: shadcn/ui

## Prerequisites

1. Python 3.8+
2. Node.js 14+
3. Google Gemini Api Key
4. Git

## Setup Instructions

### Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install requirements.txt

3. Set your OpenAI API key:
```bash
.env
OPENAI_API_KEY='your-api-key-here'
```

4. Start the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory and install dependencies:
```bash
cd frontend
npm install
```

2. Install required UI components:
```bash
npm install @radix-ui/react-alert-dialog lucide-react
```

3. Start the development server:
```bash
npm start
```


### API Endpoints

#### POST /upload/
Uploads a PDF document and processes it for question answering.

**Request:**
- Content-Type: multipart/form-data
- Body: PDF file

**Response:**
```json
{
  "filename": "string",
  "file_id": "string"
}
```

#### POST /ask/{document_id}
Asks a question about a specific document.

**Request:**
```json
{
  "question": "string",
  "file_id": "string",
  "chat_history": []
}

```

**Response:**
```json
{
  "answer": "string",
  "document": "string"
}
```

## Architecture Overview

### Backend Architecture
- FastAPI handles HTTP requests and serves the API
- SQLite database stores document metadata
- LangChain processes PDFs and handles question answering
- Chroma vector store manages document embeddings
- File system stores uploaded PDFs

### Frontend Architecture
- React components for UI rendering
- State management using React hooks
- Responsive design using React-Bootstrap CSS
- Error handling and loading states
- File upload and document management




## Troubleshooting

Common issues and solutions:

1. **PDF Upload Fails**
   - Check file size limits
   - Verify PDF format
   - Check storage permissions

2. **Question Answering Issues**
   - Verify OpenAI API key
   - Check PDF text extraction
   - Verify vector store initialization

3. **Performance Issues**
   - Check document size
   - Monitor memory usage
   - Verify database indexes



## API Documentation

Once the server is running, visit http://localhost:8000/docs for the complete API documentation.
