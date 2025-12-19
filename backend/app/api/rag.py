from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
from app.services.rag_service import RAGService
from app.services.embedding_service import CohereEmbeddingService
from app.services.qdrant_service import QdrantService
from app.services.neon_service import NeonDBService
import os

# Create the RAG router with prefix and tags
rag_router = APIRouter(prefix="/rag", tags=["RAG"])

@rag_router.post("/ask")
async def rag_ask(query_request: QueryRequest) -> QueryResponse:
    """
    Handle RAG query requests.

    Args:
        query_request: The query request containing the user's question and optional filters

    Returns:
        QueryResponse: The RAG response with answer and sources
    """
    try:
        # Initialize individual services
        embedding_service = CohereEmbeddingService()
        qdrant_service = QdrantService()
        neon_service = NeonDBService()

        # Create the RAG service with the initialized services
        rag_service = RAGService(embedding_service, qdrant_service, neon_service)

        # Retrieve relevant chunks using the RAG service
        sources = await rag_service.retrieve_relevant_chunks(
            query=query_request.query,
            chapter_filter=query_request.chapter_filter,
            selected_text=query_request.selected_text,
            limit=5
        )

        # Generate answer using LLM based on retrieved sources
        if sources:
            answer = await rag_service.generate_answer(query_request.query, sources)
        else:
            answer = f"I couldn't find relevant information in the textbook for your query: '{query_request.query}'. Please try rephrasing your question."

        response = QueryResponse(
            answer=answer,
            sources=sources
        )

        return response

    except Exception as e:
        # Handle any errors in the RAG process
        error_msg = f"Error processing RAG query: {str(e)}"
        print(error_msg)  # Log the error

        # Return a response with an error message
        response = QueryResponse(
            answer=f"Sorry, I encountered an error while processing your query: {str(e)}",
            sources=[]
        )

        return response