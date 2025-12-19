from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse
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
    # Initialize services
    embedding_service = CohereEmbeddingService()
    qdrant_service = QdrantService()
    neon_service = NeonDBService()

    try:
        # Step 1: Generate embedding for the query
        query_embedding = await embedding_service.get_embeddings([query_request.query])
        query_vector = query_embedding[0]  # Get the first (and only) embedding

        # Step 2: Search for similar vectors in Qdrant
        search_results = await qdrant_service.search_vectors(query_vector, limit=5)

        # Step 3: Retrieve metadata from Neon DB and format sources
        sources = []
        for result in search_results:
            payload = result["payload"]
            score = result["score"]

            # Extract embedding_id from payload to get detailed metadata
            embedding_id = payload.get("embedding_id", "")
            if embedding_id:
                metadata = neon_service.get_metadata_by_embedding_id(embedding_id)
                if metadata:
                    from app.models.schemas import Source
                    source = Source(
                        chapter_id=metadata["chapter_id"],
                        title=metadata["title"],
                        file_path=metadata["file_path"],
                        chunk_text_preview=metadata["chunk_text_preview"],
                        score=score
                    )
                    sources.append(source)

        # Step 4: For now, return a simple response based on the retrieved sources
        # In a real implementation, you would send the sources to an LLM to generate the answer
        if sources:
            answer = f"Based on the textbook content, I found {len(sources)} relevant sources for your query: '{query_request.query}'. Here's what I found:"
            for i, source in enumerate(sources, 1):
                answer += f"\n\n{i}. {source.title}: {source.chunk_text_preview[:200]}..."
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