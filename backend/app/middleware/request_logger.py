from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging_config import get_logger
import time

# Get logger instance
logger = get_logger("request_logger")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log incoming requests and outgoing responses with processing time.
    """

    async def dispatch(self, request: Request, call_next):
        # Log the incoming request
        client_host = request.client.host if request.client else "unknown"
        logger.info(
            "Incoming request",
            extra={
                "method": request.method,
                "url": str(request.url),
                "client_host": client_host,
                "headers": dict(request.headers)
            }
        )

        # Record start time
        start_time = time.time()

        try:
            # Process the request
            response = await call_next(request)
        except Exception as e:
            # Even if there's an exception, log the request
            processing_time = time.time() - start_time
            logger.error(
                "Request processing failed",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "client_host": client_host,
                    "processing_time_seconds": processing_time,
                    "status_code": 500,
                    "error": str(e)
                }
            )
            raise  # Re-raise the exception

        # Calculate processing time
        processing_time = time.time() - start_time

        # Log the outgoing response
        logger.info(
            "Outgoing response",
            extra={
                "method": request.method,
                "url": str(request.url),
                "client_host": client_host,
                "status_code": response.status_code,
                "processing_time_seconds": processing_time
            }
        )

        return response