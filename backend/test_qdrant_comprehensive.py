#!/usr/bin/env python3
"""
Comprehensive test script for QdrantService
Tests all methods and error handling of the Qdrant service implementation.
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add the backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    # Load .env file from the same directory as this script
    dotenv_path = Path(__file__).parent / ".env"
    if dotenv_path.exists():
        load_dotenv(dotenv_path)
        print(f"✓ Loaded environment variables from {dotenv_path}")
    else:
        print(f"⚠ Warning: .env file not found at {dotenv_path}")
except ImportError:
    print("⚠ Warning: python-dotenv not installed, skipping .env loading")

from app.services.qdrant_service import QdrantService


async def test_service_initialization():
    """Test that the service can be initialized properly."""
    print("\n=== Testing Service Initialization ===")

    # Check if environment variables are set
    qdrant_host = os.getenv("QDRANT_HOST")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_host or not qdrant_api_key:
        print("⚠ QDRANT_HOST or QDRANT_API_KEY environment variables are not set")
        print("Setting up test environment variables for local testing...")

        # For testing purposes, use a local Qdrant instance if available
        os.environ["QDRANT_HOST"] = "localhost:6333"  # Local Qdrant default port
        os.environ["QDRANT_API_KEY"] = "local-test-key"  # Local test key

        # Override environment for testing
        qdrant_host = "localhost:6333"
        qdrant_api_key = "local-test-key"

    try:
        # Initialize service with test collection name
        test_collection = "test_textbook_chapters_" + str(hash("test"))[:8]
        qdrant_service = QdrantService(collection_name=test_collection)
        print(f"✓ Service initialized successfully with collection: {test_collection}")
        return qdrant_service, test_collection
    except ValueError as e:
        print(f"✗ Service initialization error: {e}")
        return None, None
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return None, None


async def test_create_collection(service):
    """Test the create_collection method."""
    print("\n=== Testing Create Collection ===")

    try:
        result = await service.create_collection(vector_size=1536)  # Using 1536 for OpenAI embeddings or 1024 for Cohere
        if result:
            print("✓ Collection created successfully")
            return True
        else:
            print("✗ Collection creation failed")
            return False
    except ValueError as e:
        print(f"✗ Collection creation error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during collection creation: {e}")
        return False


async def test_upsert_vectors(service):
    """Test the upsert_vectors method with sample data."""
    print("\n=== Testing Upsert Vectors ===")

    # Sample vector data (simulating embeddings)
    sample_vectors = [
        [0.1, 0.2, 0.3, 0.4, 0.5] * 205,  # 1025-dimensional vector (close to 1024)
        [0.6, 0.7, 0.8, 0.9, 1.0] * 205,
        [0.2, 0.4, 0.6, 0.8, 1.0] * 205
    ]

    # Sample payloads with metadata
    sample_payloads = [
        {
            "chapter_title": "Introduction to AI",
            "section": "1.1",
            "content": "Artificial Intelligence is a fascinating field...",
            "source_file": "chapter1.md"
        },
        {
            "chapter_title": "Machine Learning Basics",
            "section": "2.1",
            "content": "Machine Learning involves training algorithms...",
            "source_file": "chapter2.md"
        },
        {
            "chapter_title": "Deep Learning Concepts",
            "section": "3.1",
            "content": "Deep Learning uses neural networks with multiple layers...",
            "source_file": "chapter3.md"
        }
    ]

    sample_ids = ["doc_1", "doc_2", "doc_3"]

    try:
        result = await service.upsert_vectors(sample_vectors, sample_payloads, sample_ids)
        if result:
            print("✓ Vectors upserted successfully")
            return True
        else:
            print("✗ Vector upsert failed")
            return False
    except ValueError as e:
        print(f"✗ Vector upsert error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during vector upsert: {e}")
        return False


async def test_search_vectors(service):
    """Test the search_vectors method."""
    print("\n=== Testing Search Vectors ===")

    # Query vector (should be same dimension as stored vectors)
    query_vector = [0.15, 0.25, 0.35, 0.45, 0.55] * 205  # Same dimension as upserted vectors

    try:
        results = await service.search_vectors(query_vector, limit=2)

        if isinstance(results, list) and len(results) > 0:
            print(f"✓ Search successful, found {len(results)} results")

            # Print first result as example
            first_result = results[0]
            print(f"  First result score: {first_result.get('score', 'N/A')}")
            print(f"  First result payload keys: {list(first_result.get('payload', {}).keys())}")

            # Verify result structure
            for i, result in enumerate(results):
                if not isinstance(result, dict):
                    print(f"✗ Result {i} is not a dictionary")
                    return False
                if 'payload' not in result or 'score' not in result:
                    print(f"✗ Result {i} missing required keys (payload, score)")
                    return False

            return True
        else:
            print("✓ Search returned no results (may be expected if no data)")
            return True

    except ValueError as e:
        print(f"✗ Vector search error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during vector search: {e}")
        return False


async def test_error_handling():
    """Test error handling in various scenarios."""
    print("\n=== Testing Error Handling ===")

    # Test initialization without required environment variables
    original_host = os.environ.get("QDRANT_HOST")
    original_key = os.environ.get("QDRANT_API_KEY")

    # Temporarily remove environment variables to test error handling
    if "QDRANT_HOST" in os.environ:
        del os.environ["QDRANT_HOST"]
    if "QDRANT_API_KEY" in os.environ:
        del os.environ["QDRANT_API_KEY"]

    try:
        service = QdrantService("test_error_collection")
        print("✗ Should have raised ValueError for missing environment variables")
        error_test_passed = False
    except ValueError as e:
        if "QDRANT_HOST" in str(e):
            print("✓ Correctly raised ValueError for missing QDRANT_HOST")
            error_test_passed = True
        else:
            print(f"✗ Wrong error message: {e}")
            error_test_passed = False
    except Exception as e:
        print(f"✗ Unexpected error during error handling test: {e}")
        error_test_passed = False

    # Restore environment variables
    if original_host:
        os.environ["QDRANT_HOST"] = original_host
    if original_key:
        os.environ["QDRANT_API_KEY"] = original_key

    return error_test_passed


async def run_comprehensive_tests():
    """Run all comprehensive tests for the Qdrant service."""
    print("🧪 Starting Comprehensive Qdrant Service Tests...\n")

    # Track test results
    test_results = {}

    # Test 1: Service initialization
    service, collection_name = await test_service_initialization()
    test_results['initialization'] = service is not None

    if service is None:
        print("\n❌ Cannot proceed with further tests - service initialization failed")
        return test_results

    try:
        # Test 2: Create collection
        test_results['create_collection'] = await test_create_collection(service)

        if test_results['create_collection']:
            # Test 3: Upsert vectors
            test_results['upsert_vectors'] = await test_upsert_vectors(service)

            if test_results['upsert_vectors']:
                # Test 4: Search vectors
                test_results['search_vectors'] = await test_search_vectors(service)
            else:
                test_results['search_vectors'] = False  # Can't test search without upserted data
        else:
            test_results['upsert_vectors'] = False
            test_results['search_vectors'] = False

    finally:
        # Test 5: Error handling (always run)
        test_results['error_handling'] = await test_error_handling()

    # Print summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)

    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name.replace('_', ' ').title()}")

    # Overall result
    all_passed = all(test_results.values())
    overall_status = "🎉 ALL TESTS PASSED!" if all_passed else "💥 SOME TESTS FAILED"
    print(f"\n{'='*50}")
    print(f"🎯 OVERALL RESULT: {overall_status}")
    print(f"{'='*50}")

    return test_results


if __name__ == "__main__":
    # Run the comprehensive tests
    results = asyncio.run(run_comprehensive_tests())

    # Exit with appropriate code
    all_passed = all(results.values())
    sys.exit(0 if all_passed else 1)