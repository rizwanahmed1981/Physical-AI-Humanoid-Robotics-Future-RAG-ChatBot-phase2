#!/usr/bin/env python3
"""
Test script for ingest_docs.py
This script verifies the ingestion script structure and imports.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all required imports work."""
    try:
        # Test imports
        from app.services.embedding_service import CohereEmbeddingService
        from app.services.qdrant_service import QdrantService
        from app.services.neon_service import NeonDBService

        print("✓ All service imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during import test: {e}")
        return False

def test_constants():
    """Test that constants are defined."""
    try:
        from scripts.ingest_docs import DOCS_PATH
        print(f"✓ DOCS_PATH constant defined: {DOCS_PATH}")
        return True
    except Exception as e:
        print(f"✗ Error with constants: {e}")
        return False

def test_functions_exist():
    """Test that key functions exist."""
    try:
        import scripts.ingest_docs as ingest_module

        # Check that required functions exist
        required_functions = ['parse_and_chunk_mdx', 'ingest_document', 'main']

        for func_name in required_functions:
            if hasattr(ingest_module, func_name):
                print(f"✓ Function '{func_name}' exists")
            else:
                print(f"✗ Function '{func_name}' missing")
                return False

        print("✓ All required functions present")
        return True
    except Exception as e:
        print(f"✗ Error checking functions: {e}")
        return False

if __name__ == "__main__":
    print("Testing ingest_docs.py script structure...")
    print()

    success1 = test_imports()
    print()
    success2 = test_constants()
    print()
    success3 = test_functions_exist()

    if success1 and success2 and success3:
        print("\n✓ All tests passed - script structure is correct!")
    else:
        print("\n✗ Some tests failed")

    sys.exit(0 if (success1 and success2 and success3) else 1)