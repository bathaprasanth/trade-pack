from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

# Explicitly load .env file
load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Trade Opportunities API"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Security
    SECRET_KEY: str = "supersecretkeyshouldbechangedinproduction" # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        extra = "ignore" # Ignore extra fields

@lru_cache()
def get_settings():
    # Debug print to check if key is loaded (masked)
    key = os.getenv("GEMINI_API_KEY", "")
    print(f"DEBUG: Loaded GEMINI_API_KEY: {'Found' if key else 'Not Found'} - Length: {len(key)}")
    return Settings()
