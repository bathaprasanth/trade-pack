from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.core.config import get_settings
from app.core.rate_limit_middleware import RateLimitMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)

# Set up Rate Limiting
app.add_middleware(RateLimitMiddleware, limit=5, window=60)

# Mount Static Files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include Router
app.include_router(api_router)

@app.get("/")
async def root():
    return FileResponse('app/static/index.html')
