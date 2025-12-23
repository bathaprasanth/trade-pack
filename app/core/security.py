from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.core.config import get_settings

settings = get_settings()

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    # For demonstration, we essentially accept any non-empty key if strict auth isn't required by the user prompt's "simple auth"
    # But a proper way is to match against an expected key.
    # Let's say we expect a key "secret-token" or similar, or just presence.
    # User said "simple auth/JWT/guest auth - your choice".
    # I will enforce a static key 'gemini-trade-api' for simplicity, or just check presence.
    
    if api_key_header == "gemini-trade-api":
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Could not validate credentials"
        )
