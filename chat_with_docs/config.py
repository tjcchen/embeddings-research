import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # OpenAI API configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Model configurations
    EMBEDDING_MODEL = "text-embedding-ada-002"
    CHAT_MODEL = "gpt-3.5-turbo"
    
    # Text processing configurations
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Vector database configurations
    VECTOR_DB_PATH = "./vector_store"
    
    # File upload configurations
    UPLOAD_DIR = "./uploads"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Supported file types
    SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.txt', '.html', '.md']
    
    # Retrieval configurations
    TOP_K_RESULTS = 4
    SIMILARITY_THRESHOLD = 0.7
