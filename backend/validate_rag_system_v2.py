"""
Simple Validation Script for RAG Backend System

This script validates the structure and basic functionality of the RAG system
without relying on pytest.
"""

import os
import sys
from pathlib import Path

def validate_structure():
    """Validate that all required files and modules exist."""
    print("=== Validating RAG System Structure ===")

    # Check main files exist in the project root
    base_path = Path(__file__).parent

    # Define expected structure
    expected_files = [
        "main.py",
        "app/api/health.py",
        "app/api/rag.py",
        "app/models/schemas.py",
        "app/services/embedding_service.py",
        "app/services/qdrant_service.py",
        "app/services/neon_service.py",
        "app/services/rag_service.py"
    ]

    missing_files = []
    for file_path in expected_files:
        full_path = base_path / file_path
        if not full_path.exists():
            missing_files.append(file_path)
            print(f"❌ Missing file: {file_path}")
        else:
            print(f"✅ Found file: {file_path}")

    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} files")
        return False
    else:
        print(f"\n✅ All {len(expected_files)} required files found")
        return True

def validate_models():
    """Validate the Pydantic models."""
    print("\n=== Validating Models ===")

    try:
        # Add the backend directory to Python path
        sys.path.insert(0, str(Path(__file__).parent))

        from app.models.schemas import QueryRequest, QueryResponse, Source

        # Test QueryRequest model
        req = QueryRequest(query="Test query")
        print("✅ QueryRequest model works")

        # Test Source model
        src = Source(
            chapter_id="ch1",
            title="Test Chapter",
            file_path="/path/to/file",
            chunk_text_preview="Preview text"
        )
        print("✅ Source model works")

        # Test QueryResponse model
        resp = QueryResponse(answer="Test answer", sources=[src])
        print("✅ QueryResponse model works")

        return True
    except Exception as e:
        print(f"❌ Model validation failed: {e}")
        return False

def validate_environment():
    """Validate environment variables are defined."""
    print("\n=== Validating Environment Variables ===")

    required_env_vars = [
        "COHERE_API_KEY",
        "QDRANT_HOST",
        "QDRANT_API_KEY",
        "NEON_DB_URL",
        "GOOGLE_API_KEY"
    ]

    missing_vars = []

    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            print(f"⚠️  Missing environment variable: {var}")
        else:
            print(f"✅ Found environment variable: {var}")

    if missing_vars:
        print(f"\n⚠️  Missing {len(missing_vars)} environment variables")
        return False
    else:
        print(f"\n✅ All {len(required_env_vars)} environment variables found")
        return True

def validate_service_imports():
    """Validate that service classes can be imported."""
    print("\n=== Validating Service Imports ===")

    try:
        # Add the backend directory to Python path
        sys.path.insert(0, str(Path(__file__).parent))

        # Import services
        from app.services.embedding_service import CohereEmbeddingService
        from app.services.qdrant_service import QdrantService
        from app.services.neon_service import NeonDBService
        from app.services.rag_service import RAGService

        print("✅ All service classes imported successfully")

        # Test that we can access the classes (basic validation)
        assert hasattr(CohereEmbeddingService, '__init__')
        assert hasattr(QdrantService, '__init__')
        assert hasattr(NeonDBService, '__init__')
        assert hasattr(RAGService, '__init__')

        print("✅ All service classes have required methods")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Service validation failed: {e}")
        return False

def main():
    """Run all validation checks."""
    print("RAG Backend System Validation")
    print("=" * 50)

    checks = [
        validate_structure,
        validate_models,
        validate_environment,
        validate_service_imports
    ]

    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"❌ Check {check.__name__} failed with exception: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    for i, (check, result) in enumerate(zip(checks, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check.__name__}")

    print(f"\nOverall: {passed}/{total} checks passed")

    if passed == total:
        print("🎉 All validations passed! RAG system structure is valid.")
        return 0
    else:
        print("⚠️  Some validations failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())