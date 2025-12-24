from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.health import health_router
from app.api.rag import rag_router
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.middleware.request_logger import RequestLoggingMiddleware
from app.core.logging_config import setup_logging, get_logger

# Load environment variables from .env file
load_dotenv()

# Initialize structured logging
setup_logging()

app = FastAPI(
    title="Physical AI Textbook RAG Backend",
    description="A FastAPI backend for the Physical AI & Humanoid Robotics AI-Native Textbook Platform, featuring RAG-based question answering using Cohere, Qdrant, Neon, and Google Gemini.",
    version="0.1.0",
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

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Include health router
app.include_router(health_router, prefix="/health", tags=["Health"])

# Include RAG router
app.include_router(rag_router)

@app.get("/",
         summary="Root endpoint",
         description="Returns a welcome message indicating that the Physical AI RAG Backend is running.")
async def root():
    logger = get_logger(__name__)
    logger.info("Root endpoint accessed")
    return {"message": "Physical AI RAG Backend is running"}