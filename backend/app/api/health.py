from fastapi import APIRouter
from app.services.qdrant_service import QdrantService
from app.services.neon_service import NeonDBService
from app.services.embedding_service import CohereEmbeddingService
import google.generativeai as genai
import os

health_router = APIRouter(prefix="/health", tags=["Health"])

@health_router.get("/",
                   summary="Health check endpoint",
                   description="Performs health checks on all system dependencies including Qdrant, Neon, Cohere, and Gemini services.",
                   responses={
                       200: {
                           "description": "Health check completed successfully",
                           "content": {
                               "application/json": {
                                   "example": {
                                       "status": "ok",
                                       "checks": {
                                           "qdrant": {
                                               "status": "healthy",
                                               "message": "Connected successfully"
                                           },
                                           "neon": {
                                               "status": "healthy",
                                               "message": "Connected successfully"
                                           },
                                           "cohere": {
                                               "status": "healthy",
                                               "message": "Connected successfully"
                                           },
                                           "gemini": {
                                               "status": "healthy",
                                               "message": "Connected successfully"
                                           }
                                       }
                                   }
                               }
                           }
                       }
                   })
async def health_check():
    # Basic health check
    health_status = {"status": "ok", "checks": {}}

    # Check Qdrant connection
    try:
        qdrant_service = QdrantService()
        # Try to list collections to verify connection
        collections = qdrant_service.client.get_collections()
        health_status["checks"]["qdrant"] = {"status": "healthy", "message": "Connected successfully"}
    except Exception as e:
        health_status["checks"]["qdrant"] = {"status": "unhealthy", "message": f"Connection failed: {str(e)}"}
        health_status["status"] = "unhealthy"

    # Check Neon connection
    try:
        neon_service = NeonDBService()
        # Try to get a connection to verify database connectivity
        conn = neon_service._get_connection()
        conn.close()
        health_status["checks"]["neon"] = {"status": "healthy", "message": "Connected successfully"}
    except Exception as e:
        health_status["checks"]["neon"] = {"status": "unhealthy", "message": f"Connection failed: {str(e)}"}
        health_status["status"] = "unhealthy"

    # Check Cohere connection
    try:
        cohere_service = CohereEmbeddingService()
        # Try a simple API call to verify connection (using a minimal embedding request)
        test_response = cohere_service.client.embed(
            texts=["health check"],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        health_status["checks"]["cohere"] = {"status": "healthy", "message": "Connected successfully"}
    except Exception as e:
        health_status["checks"]["cohere"] = {"status": "unhealthy", "message": f"Connection failed: {str(e)}"}
        health_status["status"] = "unhealthy"

    # Check Gemini connection
    try:
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")

        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel('gemini-pro')

        # Try a simple API call to verify connection
        response = model.generate_content("Say 'health check' in one word")
        health_status["checks"]["gemini"] = {"status": "healthy", "message": "Connected successfully"}
    except Exception as e:
        health_status["checks"]["gemini"] = {"status": "unhealthy", "message": f"Connection failed: {str(e)}"}
        health_status["status"] = "unhealthy"

    return health_status