from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag_service import RAGService
from app.services.embedding_service import CohereEmbeddingService
from app.services.qdrant_service import QdrantService
from app.services.neon_service import NeonDBService

# Create the RAG router with prefix and tags
rag_router = APIRouter(prefix="/rag", tags=["RAG"])

# Dependency injection functions
async def get_cohere_service() -> CohereEmbeddingService:
    return CohereEmbeddingService()

async def get_qdrant_service() -> QdrantService:
    return QdrantService()

async def get_neon_service() -> NeonDBService:
    # IMPORTANT: NeonDBService's get_metadata_by_embedding_id is synchronous
    # If you wish to make it truly async, you'd wrap it in an executor.
    # For hackathon simplicity, we'll use it directly, but be aware of blocking.
    return NeonDBService()

async def get_rag_service(
    cohere_service: CohereEmbeddingService = Depends(get_cohere_service),
    qdrant_service: QdrantService = Depends(get_qdrant_service),
    neon_service: NeonDBService = Depends(get_neon_service)
) -> RAGService:
    return RAGService(cohere_service, qdrant_service, neon_service)

@rag_router.post("/ask",
                 summary="Ask a question using RAG",
                 description="Submit a query to the RAG system to retrieve relevant information from the textbook and generate an answer using the LLM.",
                 responses={
                     200: {
                         "description": "Successfully retrieved relevant information and generated an answer",
                         "content": {
                             "application/json": {
                                 "example": {
                                     "answer": "The answer to your question based on the textbook content.",
                                     "sources": [
                                         {
                                             "chapter_id": "ch_01",
                                             "title": "Introduction to Robotics",
                                             "file_path": "/path/to/chapter1.pdf",
                                             "chunk_text_preview": "Preview of the relevant text chunk...",
                                             "score": 0.85
                                         }
                                     ]
                                 }
                             }
                         }
                     },
                     500: {
                         "description": "Internal server error occurred during RAG processing"
                     }
                 })
async def rag_ask(
    query_request: QueryRequest,
    rag_service: RAGService = Depends(get_rag_service)
) -> QueryResponse:
    """
    Handle RAG query requests.

    Args:
        query_request: The query request containing the user's question and optional filters
        rag_service: The RAG service instance (injected via dependency injection)

    Returns:
        QueryResponse: The RAG response with answer and sources
    """
    try:
        # Retrieve relevant chunks using the RAG service
        retrieved_sources = await rag_service.retrieve_relevant_chunks(
            query=query_request.query,
            chapter_filter=query_request.chapter_filter,
            selected_text=query_request.selected_text,
            limit=5
        )

        # Generate answer using LLM based on retrieved sources
        if retrieved_sources:
            answer = await rag_service.generate_answer(query_request.query, retrieved_sources)
        else:
            answer = f"I couldn't find relevant information in the textbook for your query: '{query_request.query}'. Please try rephrasing your question."

        response = QueryResponse(
            answer=answer,
            sources=retrieved_sources
        )

        return response

    except ValueError as e:
        # Handle specific errors from the RAG service
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        # Handle any other errors in the RAG process
        error_msg = f"Error processing RAG query: {str(e)}"
        print(error_msg)  # Log the error

        # Return a response with an error message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sorry, I encountered an error while processing your query: {str(e)}"
        )