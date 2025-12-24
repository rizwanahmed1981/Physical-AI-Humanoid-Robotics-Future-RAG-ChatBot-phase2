from fastapi import APIRouter, Depends
from app.services.qdrant_service import QdrantService
from app.services.neon_service import NeonDBService
from app.services.embedding_service import CohereEmbeddingService
from google import genai
import os

health_router = APIRouter(
    tags=["Health"]
)

# Dependency injection functions for health check services
async def get_cohere_service() -> CohereEmbeddingService:
    return CohereEmbeddingService()

async def get_qdrant_service() -> QdrantService:
    return QdrantService()

async def get_neon_service() -> NeonDBService:
    # IMPORTANT: NeonDBService's get_metadata_by_embedding_id is synchronous
    # If you wish to make it truly async, you'd wrap it in an executor.
    # For hackathon simplicity, we'll use it directly, but be aware of blocking.
    return NeonDBService()

@health_router.get("/",
                   summary="Check overall application and dependency health",
                   description="Returns the current operational status of the FastAPI application and its integrated services (Qdrant, Neon, Cohere, Gemini).",
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
async def health_check(
    cohere_service: CohereEmbeddingService = Depends(get_cohere_service),
    qdrant_service: QdrantService = Depends(get_qdrant_service),
    neon_service: NeonDBService = Depends(get_neon_service)
):
    # Basic health check
    health_status = {"status": "ok", "checks": {}}

    # Check Qdrant connection
    try:
        # Try to list collections to verify connection
        collections = qdrant_service.client.get_collections()
        health_status["checks"]["qdrant"] = {"status": "healthy", "message": "Connected successfully"}
    except Exception as e:
        health_status["checks"]["qdrant"] = {"status": "unhealthy", "message": f"Connection failed: {str(e)}"}
        health_status["status"] = "unhealthy"

    # Check Neon connection
    try:
        # Try to get a connection to verify database connectivity
        conn = neon_service._get_connection()
        conn.close()
        health_status["checks"]["neon"] = {"status": "healthy", "message": "Connected successfully"}
    except Exception as e:
        health_status["checks"]["neon"] = {"status": "unhealthy", "message": f"Connection failed: {str(e)}"}
        health_status["status"] = "unhealthy"

    # Check Cohere connection
    try:
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

        # Initialize client with the new SDK
        client = genai.Client(api_key=google_api_key)

        # Try to get model info to verify availability (lightweight check)
        model = client.models.get(model='gemini-2.5-pro')
        health_status["checks"]["gemini"] = {"status": "healthy", "message": "Connected successfully"}
    except Exception as e:
        health_status["checks"]["gemini"] = {"status": "unhealthy", "message": f"Connection failed: {str(e)}"}
        health_status["status"] = "unhealthy"

    return health_status