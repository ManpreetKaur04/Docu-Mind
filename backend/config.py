from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = ""
    UPLOAD_DIR: str = "uploads"
    VECTOR_STORE_DIR: str = "vector_store"
    MODEL_NAME: str = "gemini-1.5-pro"
    EMBEDDING_MODEL: str = "models/embedding-001"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    class Config:
        env_file = ".env"

settings = Settings()