import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-3.5-turbo"
    OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
    
    # Pinecone Configuration
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1-aws")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "mcp-docs")
    
    # Server Configuration
    HOST = os.getenv("HOST", "localhost")
    PORT = int(os.getenv("PORT", 8000))
    
    # RAG Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    TOP_K_RESULTS = 5
    
    # Data paths
    DATA_DIR = "data"
    DOCUMENTATION_FILE = os.path.join(DATA_DIR, "mcp_documentation.json")
    
    # Validation
    @classmethod
    def validate(cls):
        """Validate required settings"""
        required_settings = [
            ("OPENAI_API_KEY", cls.OPENAI_API_KEY),
            ("PINECONE_API_KEY", cls.PINECONE_API_KEY),
        ]
        
        missing_settings = []
        for name, value in required_settings:
            if not value:
                missing_settings.append(name)
        
        if missing_settings:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_settings)}")
        
        return True

# Create global settings instance
settings = Settings() 