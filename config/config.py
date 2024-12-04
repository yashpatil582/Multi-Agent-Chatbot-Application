import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_ID = os.getenv("ASTRA_DB_ID")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
    
    # Model Configuration
    MODEL_NAME = "togethercomputer/llama-2-70b-chat"
    
    # Vector Store Configuration
    COLLECTION_NAME = "multi_agent_searches"
    EMBEDDING_DIMENSION = 384
    
    # Cache Configuration
    CACHE_EXPIRY = 3600  # 1 hour 