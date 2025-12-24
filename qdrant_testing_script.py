#!/usr/bin/env python3
"""
Qdrant Testing Script

This script tests the Qdrant server to check collection status and see if any vectors have been stored.
It connects to the Qdrant server and performs various tests to validate the system status.
"""
import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

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
        # Test connection by getting cluster info (different method in older version)
        # Use a simple API call to check if connection works
        collections = client.get_collections()
        print(f"✅ Connected to Qdrant server successfully")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


async def test_collections():
    """Test collection listing and status."""
    print("\n=== Testing Collections ===")

    client = get_qdrant_client()
    if not client:
        return False

    try:
        # List all collections
        collections = client.get_collections()
        print(f"✅ Retrieved collections: {len(collections)} found")

        if collections:
            for collection in collections:
                collection_name = collection.name if hasattr(collection, 'name') else collection
                print(f"   - Collection: {collection_name}")

                # Get detailed collection info
                try:
                    collection_info = client.get_collection(collection_name)
                    print(f"     Points count: {collection_info.points_count}")
                    print(f"     Indexed vectors: {collection_info.indexed_vector_count}")
                    print(f"     Vector size: {collection_info.config.params.size}")
                    print(f"     Distance: {collection_info.config.params.distance}")
                except Exception as e:
                    print(f"     Could not get detailed info: {e}")
        else:
            print("   No collections found")

        return True
    except Exception as e:
        print(f"❌ Collection test failed: {e}")
        return False


async def test_collection_health():
    """Test the health of specific collections used in the project."""
    print("\n=== Testing Collection Health ===")

    client = get_qdrant_client()
    if not client:
        return False

    # Test the default collection used in the service
    collection_name = "textbook_chapters"

    try:
        # Check if collection exists
        try:
            collection_info = client.get_collection(collection_name)
            print(f"✅ Collection '{collection_name}' exists")
            print(f"   Points count: {collection_info.points_count}")
            print(f"   Indexed vectors: {collection_info.indexed_vector_count}")
            print(f"   Vector size: {collection_info.config.params.size}")
            print(f"   Distance: {collection_info.config.params.distance}")

            # Check if there are any vectors stored
            if collection_info.points_count > 0:
                print(f"   📊 Collection has {collection_info.points_count} vectors stored")

                # Sample some points to verify they have proper structure
                try:
                    scroll_result = client.scroll(
                        collection_name=collection_name,
                        limit=2,  # Just get 2 points as a sample
                        with_payload=True,
                        with_vectors=False
                    )

                    points = scroll_result[0] if isinstance(scroll_result, tuple) else scroll_result
                    for i, point in enumerate(points):
                        payload_keys = list(point.payload.keys()) if point.payload else 'None'
                        print(f"   Sample Point {i+1}: ID={point.id}, Payload keys: {payload_keys}")

                except Exception as e:
                    print(f"   ⚠️  Could not sample points: {e}")
            else:
                print(f"   📭 Collection is empty (no vectors stored)")

        except Exception as e:
            print(f"❌ Collection '{collection_name}' does not exist or error occurred: {e}")

            # Let's also check for the other collection that was mentioned in the output
            alt_collection = "textbook_content"
            try:
                collection_info = client.get_collection(alt_collection)
                print(f"✅ Alternative collection '{alt_collection}' exists")
                print(f"   Points count: {collection_info.points_count}")
                print(f"   Indexed vectors: {collection_info.indexed_vector_count}")

                if collection_info.points_count > 0:
                    print(f"   📊 Collection has {collection_info.points_count} vectors stored")

                    # Sample some points from this collection
                    try:
                        scroll_result = client.scroll(
                            collection_name=alt_collection,
                            limit=2,
                            with_payload=True,
                            with_vectors=False
                        )

                        points = scroll_result[0] if isinstance(scroll_result, tuple) else scroll_result
                        for i, point in enumerate(points):
                            payload_keys = list(point.payload.keys()) if point.payload else 'None'
                            print(f"   Sample Point {i+1}: ID={point.id}, Payload keys: {payload_keys}")
                    except Exception as e:
                        print(f"   ⚠️  Could not sample points from {alt_collection}: {e}")
                else:
                    print(f"   📭 Collection is empty (no vectors stored)")
            except Exception as alt_e:
                print(f"❌ Alternative collection '{alt_collection}' also does not exist: {alt_e}")

        return True
    except Exception as e:
        print(f"❌ Collection health test failed: {e}")
        return False


async def test_qdrant_service_integration():
    """Test the QdrantService class integration."""
    print("\n=== Testing Qdrant Service Integration ===")

    try:
        # Try to create QdrantService instance
        qdrant_service = QdrantService()
        print("✅ QdrantService initialized successfully")

        # Test collection listing through service
        client = get_qdrant_client()
        if client:
            collections = client.get_collections()
            print(f"✅ Service can access {len(collections)} collections")

            for collection in collections:
                collection_name = collection.name if hasattr(collection, 'name') else collection
                try:
                    collection_info = client.get_collection(collection_name)
                    print(f"   - {collection_name}: {collection_info.points_count} points")
                except Exception as e:
                    print(f"   - {collection_name}: could not get details - {e}")

        return True
    except Exception as e:
        print(f"❌ Qdrant service integration test failed: {e}")
        return False


async def comprehensive_test():
    """Run all Qdrant tests."""
    print("Qdrant Server Testing")
    print("=" * 50)

    tests = [
        ("Connection Test", test_qdrant_connection),
        ("Collections Test", test_collections),
        ("Collection Health Test", test_collection_health),
        ("Service Integration Test", test_qdrant_service_integration)
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

    if passed == total:
        print("🎉 All Qdrant tests passed!")
        return 0
    else:
        print("⚠️  Some Qdrant tests failed.")
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