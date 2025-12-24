#!/usr/bin/env python3
"""
Qdrant Testing Script - Robust Version

This script tests the Qdrant server to check collection status and see if any vectors have been stored.
It handles compatibility issues between different Qdrant client and server versions.
"""
import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import json

# Load environment variables
env_path = Path(__file__).parent / "backend" / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    print("Warning: .env file not found in backend directory")

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from qdrant_client import QdrantClient
from app.services.qdrant_service import QdrantService


def get_qdrant_client():
    """Create and return a Qdrant client based on environment variables."""
    host = os.getenv("QDRANT_HOST", "localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY", "local-test-key")

    print(f"Attempting to connect to Qdrant at: {host}")

    try:
        if host.startswith("http://") or host.startswith("https://"):
            # For cloud instances with full URL
            client = QdrantClient(url=host, api_key=api_key)
        else:
            # For local instances with host:port format
            if ":" in host:
                # Split host:port format
                host_parts = host.split(":")
                host_addr = host_parts[0]
                port = int(host_parts[1])
                client = QdrantClient(host=host_addr, port=port, api_key=api_key)
            else:
                # Just host, assume default port
                client = QdrantClient(host=host, api_key=api_key)

        return client
    except Exception as e:
        print(f"Failed to create Qdrant client: {e}")
        return None


async def test_qdrant_connection():
    """Test basic connection to Qdrant server."""
    print("\n=== Testing Qdrant Connection ===")

    client = get_qdrant_client()
    if not client:
        print("❌ Failed to create Qdrant client")
        return False

    try:
        # Test connection by getting collections (simple API call to check connection)
        collections_response = client.get_collections()
        print(f"✅ Connected to Qdrant server successfully")
        print(f"   Server is accessible and responding")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


async def test_collections_basic():
    """Test collection listing - basic version without detailed config parsing."""
    print("\n=== Testing Collections (Basic) ===")

    client = get_qdrant_client()
    if not client:
        return False

    try:
        # List all collections
        collections_response = client.get_collections()

        # Handle the response based on its type
        if hasattr(collections_response, 'collections'):
            # Newer API response format
            collections_list = collections_response.collections
            collection_names = [getattr(col, 'name', str(col)) for col in collections_list]
        else:
            # Older API response format - it might be a direct list
            collections_list = list(collections_response) if not isinstance(collections_response, list) else collections_response
            collection_names = [getattr(col, 'name', str(col)) for col in collections_list]

        print(f"✅ Found {len(collection_names)} collections:")
        for name in collection_names:
            print(f"   - {name}")

        # For each collection, try to get basic info without parsing complex config
        for collection_name in collection_names:
            try:
                # For now, just try to get basic info without complex parsing
                # The main goal is to confirm the collection exists and get basic stats
                try:
                    collection_info = client.get_collection(collection_name)
                    # Instead of accessing detailed config, just get the core attributes that are likely to work
                    if hasattr(collection_info, '__dict__'):
                        info_dict = collection_info.__dict__
                        points_count = info_dict.get('points_count', 'unknown') if isinstance(info_dict, dict) else 'unknown'
                        indexed_count = info_dict.get('indexed_vector_count', 'unknown') if isinstance(info_dict, dict) else 'unknown'
                        print(f"     {collection_name}: {points_count} points, {indexed_count} indexed")
                    else:
                        print(f"     {collection_name}: (info format not dict-like)")
                except Exception as config_e:
                    print(f"     {collection_name}: (config parsing error: {str(config_e)[:50]}...)")

            except Exception as e:
                print(f"     {collection_name}: (error getting details: {e})")

        return True
    except Exception as e:
        print(f"❌ Collection test failed: {e}")
        return False


async def test_collection_health_manual():
    """Test collection health by checking if vectors exist using direct HTTP calls."""
    print("\n=== Testing Collection Health (Manual Check) ===")

    client = get_qdrant_client()
    if not client:
        return False

    # Get list of collections
    collections_response = client.get_collections()
    if hasattr(collections_response, 'collections'):
        collections_list = collections_response.collections
        collection_names = [getattr(col, 'name', str(col)) for col in collections_list]
    else:
        collections_list = list(collections_response) if not isinstance(collections_response, list) else collections_response
        collection_names = [getattr(col, 'name', str(col)) for col in collections_list]

    # Check each collection for vector content
    vectors_found = False
    for collection_name in collection_names:
        try:
            # Use scroll API to check if there are any vectors
            scroll_result = client.scroll(
                collection_name=collection_name,
                limit=1,  # Just get 1 point to check if any exist
                with_payload=True,
                with_vectors=False
            )

            if isinstance(scroll_result, tuple):
                points, next_page = scroll_result
            else:
                points = scroll_result

            if points:
                point = points[0]
                print(f"✅ Collection '{collection_name}' has vectors stored!")
                print(f"   Sample point ID: {getattr(point, 'id', 'unknown')}")

                # Show payload structure if available
                if hasattr(point, 'payload') and point.payload:
                    payload_keys = list(point.payload.keys())
                    print(f"   Payload keys: {payload_keys}")

                vectors_found = True
            else:
                print(f"   Collection '{collection_name}' is empty (no vectors)")
        except Exception as e:
            print(f"   Could not check {collection_name}: {e}")

    if vectors_found:
        print(f"📊 Vectors found in at least one collection!")
        return True
    else:
        print(f"📭 No vectors found in any collection")
        return False


async def test_qdrant_service_creation():
    """Test QdrantService class creation and basic functionality."""
    print("\n=== Testing Qdrant Service Creation ===")

    try:
        # Try to create QdrantService instance
        qdrant_service = QdrantService()
        print("✅ QdrantService initialized successfully")

        # Test that it can list collections through the service
        client = get_qdrant_client()
        if client:
            try:
                collections_response = client.get_collections()
                if hasattr(collections_response, 'collections'):
                    collection_count = len(collections_response.collections)
                else:
                    collection_count = len(list(collections_response))

                print(f"✅ Service can access {collection_count} collections through client")
            except Exception as e:
                print(f"⚠️  Service client access issue: {e}")

        return True
    except Exception as e:
        print(f"❌ Qdrant service creation test failed: {e}")
        return False


async def test_vector_search_basic():
    """Test basic vector search functionality."""
    print("\n=== Testing Vector Search (Basic) ===")

    client = get_qdrant_client()
    if not client:
        return False

    # Get list of collections
    collections_response = client.get_collections()
    if hasattr(collections_response, 'collections'):
        collections_list = collections_response.collections
        collection_names = [getattr(col, 'name', str(col)) for col in collections_list]
    else:
        collections_list = list(collections_response) if not isinstance(collections_response, list) else collections_response
        collection_names = [getattr(col, 'name', str(col)) for col in collections_list]

    # Try search on each collection that has vectors
    search_success = False
    for collection_name in collection_names:
        try:
            # First, try to get a sample vector from the collection
            scroll_result = client.scroll(
                collection_name=collection_name,
                limit=1,
                with_payload=True,
                with_vectors=True
            )

            if isinstance(scroll_result, tuple):
                points, next_page = scroll_result
            else:
                points = scroll_result

            if points and hasattr(points[0], 'vector') and points[0].vector:
                sample_vector = points[0].vector
                print(f"   Testing search on {collection_name}...")

                # Perform a search with the sample vector
                search_results = client.search(
                    collection_name=collection_name,
                    query_vector=sample_vector,
                    limit=1
                )

                if search_results:
                    print(f"✅ Search successful on {collection_name}")
                    print(f"   Returned {len(search_results)} results")
                    search_success = True
                else:
                    print(f"⚠️  Search returned no results on {collection_name}")
            else:
                print(f"⚠️  No vectors available in {collection_name} for search test")

        except Exception as e:
            print(f"⚠️  Search test failed on {collection_name}: {e}")

    if search_success:
        print("✅ Vector search functionality is working")
        return True
    else:
        print("⚠️  Could not perform search tests (no collections with vectors found)")
        return False


async def comprehensive_test():
    """Run all Qdrant tests."""
    print("Qdrant Server Testing - Robust Version")
    print("=" * 50)

    tests = [
        ("Connection Test", test_qdrant_connection),
        ("Collections Test (Basic)", test_collections_basic),
        ("Collection Health Test (Manual)", test_collection_health_manual),
        ("Service Creation Test", test_qdrant_service_creation),
        ("Vector Search Test (Basic)", test_vector_search_basic)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")

    print(f"\nOverall: {passed}/{total} tests passed")

    # Provide summary of findings
    print("\n" + "=" * 50)
    print("QDRANT SERVER STATUS SUMMARY")
    print("=" * 50)

    if passed > 0:
        print("✅ Qdrant server is accessible and operational")

        # Check if collections exist
        client = get_qdrant_client()
        if client:
            try:
                collections_response = client.get_collections()
                if hasattr(collections_response, 'collections'):
                    collection_names = [getattr(col, 'name', str(col)) for col in collections_response.collections]
                else:
                    collection_names = [getattr(col, 'name', str(col)) for col in list(collections_response)]

                print(f"✅ Found {len(collection_names)} collection(s): {', '.join(collection_names)}")

                # Check if vectors exist
                vectors_exist = False
                for name in collection_names:
                    try:
                        scroll_result = client.scroll(collection_name=name, limit=1, with_payload=False, with_vectors=False)
                        if isinstance(scroll_result, tuple):
                            points, _ = scroll_result
                        else:
                            points = scroll_result
                        if points:
                            vectors_exist = True
                            break
                    except:
                        continue

                if vectors_exist:
                    print("✅ Vector data is present in at least one collection")
                else:
                    print("⚠️  No vector data found in collections")
            except:
                print("⚠️  Could not determine collection status")
    else:
        print("❌ Qdrant server is not accessible or has major issues")

    if passed == total:
        print("\n🎉 All Qdrant tests passed! Server is operational.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} out of {total} tests failed, but core functionality may still be working.")
        return 1


def test_environment():
    """Test if required environment variables are set."""
    print("=== Testing Environment Variables ===")

    required_vars = ["QDRANT_HOST", "QDRANT_API_KEY"]
    all_set = True

    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:10]}..." if len(value) > 10 else f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: NOT SET")
            all_set = False

    return all_set


if __name__ == "__main__":
    # Test environment first
    env_ok = test_environment()

    if not env_ok:
        print("\n⚠️  Environment variables not properly set. Using defaults.")
        os.environ.setdefault("QDRANT_HOST", "localhost:6333")
        os.environ.setdefault("QDRANT_API_KEY", "local-test-key")

    # Run comprehensive tests
    exit_code = asyncio.run(comprehensive_test())
    sys.exit(exit_code)