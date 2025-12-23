from app.core.config import get_settings
import os

settings = get_settings()
print(f"Settings Key Len: {len(settings.GEMINI_API_KEY)}")
print(f"Env Var Key Len: {len(os.getenv('GEMINI_API_KEY', ''))}")
