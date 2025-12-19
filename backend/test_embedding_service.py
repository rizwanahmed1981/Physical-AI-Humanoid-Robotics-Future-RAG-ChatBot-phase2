#!/usr/bin/env python3
"""
Test script for CohereEmbeddingService
This script demonstrates how to use the embedding service.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables from .env file if it exists
from dotenv import load_dotenv

# Load .env file from the same directory as this script
dotenv_path = Path(__file__).parent / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    print(f"⚠ Warning: .env file not found at {dotenv_path}")

from app.services.embedding_service import CohereEmbeddingService

async def test_embedding_service():
    """Test the embedding service with sample text."""

    # Check if environment variables are set
    if not os.getenv("COHERE_API_KEY"):
        print("⚠ Warning: COHERE_API_KEY environment variable is not set")
        print("To test this service, please:")
        print("1. Create a .env file in the backend directory with:")
        print("   COHERE_API_KEY=your_actual_cohere_api_key_here")
        print("2. Then run:")
        print("   python test_embedding_service.py")
        return True

    try:
        # Initialize the embedding service
        embedding_service = CohereEmbeddingService()
        print("✓ Embedding service initialized successfully")

        # Sample texts to embed
        sample_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Machine learning is a subset of artificial intelligence.",
            "Python is a popular programming language for data science."
        ]

        # Generate embeddings
        embeddings = await embedding_service.get_embeddings(sample_texts)

        print(f"✓ Generated {len(embeddings)} embeddings")
        print(f"✓ Each embedding has dimension: {len(embeddings[0])}")

        # Print first embedding as example
        print("\nFirst embedding (first 10 values):")
        print(embeddings[0][:10])

        return True

    except ValueError as e:
        print(f"✗ Value Error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_embedding_service())
    sys.exit(0 if success else 1)