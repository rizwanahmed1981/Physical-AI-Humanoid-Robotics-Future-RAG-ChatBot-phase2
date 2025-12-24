from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time

class RequestLogger(BaseHTTPMiddleware):
    """
    Request logging middleware for the FastAPI application.
    Logs incoming requests and outgoing responses with timing information.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        print(f"LOG: {request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
        return response