from fastapi import FastAPI
from app.api.health import health_router
from app.api.rag import rag_router
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.core import logging_config

# Initialize structured logging
logging_config.setup_logging()

app = FastAPI(
    title="Physical AI RAG Backend",
    description="Backend API for Physical AI Humanoid Robotics Future RAG ChatBot project. This API provides health checks and RAG (Retrieval Augmented Generation) capabilities for textbook content.",
    version="1.0.0",
    contact={
        "name": "Physical AI Development Team",
        "url": "https://github.com/ecomw/Physical-AI-Humanoid-Robotics-Future-RAG-ChatBot",
        "email": "development@physical-ai.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Add error handling middleware
app.add_middleware(ErrorHandlerMiddleware)

# Include health router
app.include_router(health_router, prefix="/health", tags=["Health"])

# Include RAG router
app.include_router(rag_router)

@app.get("/",
         summary="Root endpoint",
         description="Returns a welcome message indicating that the Physical AI RAG Backend is running.")
async def root():
    logger = logging_config.get_logger(__name__)
    logger.info("Root endpoint accessed")
    return {"message": "Physical AI RAG Backend is running"}