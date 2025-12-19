"""
Test script to demonstrate RAGService usage
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.rag_service import RAGService
from app.services.embedding_service import CohereEmbeddingService
from app.services.qdrant_service import QdrantService
from app.services.neon_service import NeonDBService


async def test_rag_service():
    """
    Test the RAGService with a sample query
    """
    print("Testing RAGService...")

    try:
        # Initialize the services
        cohere_service = CohereEmbeddingService()
        qdrant_service = QdrantService()
        neon_service = NeonDBService()

        # Create the RAG service
        rag_service = RAGService(cohere_service, qdrant_service, neon_service)

        # Test query
        query = "What is physical AI?"

        # Retrieve relevant chunks
        sources = await rag_service.retrieve_relevant_chunks(query, limit=3)

        print(f"Found {len(sources)} relevant sources for query: '{query}'")

        for i, source in enumerate(sources, 1):
            print(f"\nSource {i}:")
            print(f"  Chapter ID: {source.chapter_id}")
            print(f"  Title: {source.title}")
            print(f"  File Path: {source.file_path}")
            print(f"  Preview: {source.chunk_text_preview[:150]}...")
            print(f"  Score: {source.score}")

        if not sources:
            print("\nNo relevant sources found. This is expected if the database is empty.")
            print("You need to run the ingestion script first to populate the databases.")

    except Exception as e:
        print(f"Error during RAG service test: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_rag_service())