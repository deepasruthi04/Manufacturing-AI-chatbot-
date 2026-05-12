from pydantic_settings import BaseSettings
import os
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Manufacturing Copilot"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    ORG_KEY: str = os.getenv("ORG_KEY", "ADM")
    
    # OpenAI / LLM (Assuming Gemini or similar based on previous context, but I'll make it generic)
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # RAG
    CHROMA_PERSIST_DIRECTORY: str = str(Path(__file__).parent.parent.parent / "chroma_db")
    DOCUMENTS_PATH: str = str(Path(__file__).parent.parent.parent.parent / "Rag_documents")

    class Config:
        case_sensitive = True

settings = Settings()
