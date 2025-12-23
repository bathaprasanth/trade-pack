from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 5, window: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Only rate limit the analyze endpoint
        if request.url.path.startswith("/analyze"):
            client_ip = request.client.host if request.client else "unknown"
            current_time = time.time()
            
            # Clean up old requests
            self.requests[client_ip] = [t for t in self.requests[client_ip] if current_time - t < self.window]
            
            if len(self.requests[client_ip]) >= self.limit:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded. Try again later."}
                )
            
            self.requests[client_ip].append(current_time)

        response = await call_next(request)
        return response
