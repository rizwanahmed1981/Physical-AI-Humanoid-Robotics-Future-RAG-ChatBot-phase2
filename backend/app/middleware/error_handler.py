from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable, Any
import traceback
import logging
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Global error handling middleware to catch unhandled exceptions and return consistent error responses.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Any:
        try:
            response = await call_next(request)
            return response
        except HTTPException as e:
            # Re-raise HTTP exceptions as they are already properly formatted
            logger.error(f"HTTPException occurred: {e.status_code} - {e.detail}")
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "error": {
                        "type": "HTTPException",
                        "message": e.detail,
                        "status_code": e.status_code
                    }
                }
            )
        except Exception as e:
            # Log the full traceback for debugging
            logger.error(f"Unhandled exception occurred: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            # Return a consistent error response for unhandled exceptions
            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "type": "InternalServerError",
                        "message": "An internal server error occurred. Please contact the administrator.",
                        "status_code": 500
                    }
                }
            )