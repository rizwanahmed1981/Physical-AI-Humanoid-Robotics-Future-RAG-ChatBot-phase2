from fastapi import Request, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class GlobalErrorHandler(BaseHTTPMiddleware):
    """
    Global error handler middleware for the FastAPI application.
    Catches all exceptions and returns a standardized JSON error response.
    """

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            print(f"Error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error", "message": str(e)}
            )