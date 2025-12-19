"""
Test script for RAG API functionality
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.api.rag import rag_ask
from app.models.schemas import QueryRequest

async def test_rag_functionality():
    """
    Test the RAG functionality with a sample query
    """
    print("Testing RAG functionality...")

    # Create a sample query request
    query_request = QueryRequest(
        query="What is physical AI?",
        chapter_filter=None,
        selected_text=None
    )

    try:
        # Call the rag_ask function directly
        response = await rag_ask(query_request)
        print(f"Response received:")
        print(f"Answer: {response.answer}")
        print(f"Number of sources: {len(response.sources)}")

        for i, source in enumerate(response.sources, 1):
            print(f"Source {i}:")
            print(f"  Chapter ID: {source.chapter_id}")
            print(f"  Title: {source.title}")
            print(f"  File Path: {source.file_path}")
            print(f"  Preview: {source.chunk_text_preview[:100]}...")
            print(f"  Score: {source.score}")
            print()

    except Exception as e:
        print(f"Error during RAG test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_rag_functionality())