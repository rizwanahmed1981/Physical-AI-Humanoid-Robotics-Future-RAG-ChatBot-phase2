from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.health import health_router
from app.api.rag import rag_router
from app.middleware.cors import setup_cors
from app.middleware.error_handler import GlobalErrorHandler
from app.middleware.request_logger import RequestLogger
from app.core.logging_config import setup_logging, get_logger

# Load environment variables from .env file
load_dotenv()

# Initialize structured logging
setup_logging()

app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="AI-Native Backend for RAG-based textbook interaction.",
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

# Setup CORS middleware
setup_cors(app)

# Add request logging middleware
app.add_middleware(RequestLogger)

# Add error handling middleware
app.add_middleware(GlobalErrorHandler)

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