#!/usr/bin/env python3
"""
Quick Qdrant Status Check

This script provides a quick check of the Qdrant server status,
collections, and vector data presence.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / "backend" / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from qdrant_client import QdrantClient


def quick_qdrant_check():
    """Perform a quick check of Qdrant server status."""
    print("Quick Qdrant Status Check")
    print("=" * 30)

    # Get environment variables
    host = os.getenv("QDRANT_HOST", "localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY", "local-test-key")

    print(f"Host: {host}")

    try:
        # Create client
        if host.startswith("http://") or host.startswith("https://"):
            client = QdrantClient(url=host, api_key=api_key)
        else:
            if ":" in host:
                host_parts = host.split(":")
                host_addr = host_parts[0]
                port = int(host_parts[1])
                client = QdrantClient(host=host_addr, port=port, api_key=api_key)
            else:
                client = QdrantClient(host=host, api_key=api_key)

        # Test connection by getting collections
        collections = client.get_collections()
        if hasattr(collections, 'collections'):
            collection_list = collections.collections
            collection_names = [getattr(col, 'name', str(col)) for col in collection_list]
        else:
            collection_list = list(collections) if not isinstance(collections, list) else collections
            collection_names = [getattr(col, 'name', str(col)) for col in collection_list]

        print(f"✅ Connected successfully")
        print(f"📊 Collections: {len(collection_names)}")

        for name in collection_names:
            print(f"   - {name}")

            # Check if collection has vectors
            try:
                scroll_result = client.scroll(
                    collection_name=name,
                    limit=1,
                    with_payload=False,
                    with_vectors=False
                )

                if isinstance(scroll_result, tuple):
                    points, _ = scroll_result
                else:
                    points = scroll_result

                vector_count = len(points) if points else 0
                status = "✅ Has vectors" if vector_count > 0 else "📭 Empty"
                print(f"     {status}")

            except Exception:
                print(f"     ❌ Error checking vectors")

        print("\n✅ Qdrant server is operational")
        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


if __name__ == "__main__":
    success = quick_qdrant_check()
    sys.exit(0 if success else 1)