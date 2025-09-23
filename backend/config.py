import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Real-Time Chat API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Use SQLite for development
    DATABASE_URL = "sqlite:///./chat.db"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

settings = Settings()