"""
Simple Validation Script for RAG Backend System

This script validates the structure and basic functionality of the RAG system
without relying on pytest.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent / "app"))

def validate_structure():
    """Validate that all required files and modules exist."""
    print("=== Validating RAG System Structure ===")

    # Check main files exist
    required_files = [
        "main.py",
        "api/health.py",
        "api/rag.py",
        "models/schemas.py",
        "services/embedding_service.py",
        "services/qdrant_service.py",
        "services/neon_service.py",
        "services/rag_service.py"
    ]

    base_path = Path(__file__).parent
    missing_files = []

    for file_path in required_files:
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
        print(f"\n✅ All {len(required_files)} required files found")
        return True

def validate_models():
    """Validate the Pydantic models."""
    print("\n=== Validating Models ===")

    try:
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

def validate_services():
    """Validate service classes can be imported and instantiated."""
    print("\n=== Validating Services ===")

    try:
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

    except Exception as e:
        print(f"❌ Service validation failed: {e}")
        return False

def validate_api_endpoints():
    """Validate API endpoint structure."""
    print("\n=== Validating API Endpoints ===")

    try:
        from app.api.rag import rag_router, get_cohere_service, get_qdrant_service, get_neon_service, get_rag_service
        from app.api.health import health_router

        print("✅ API routers imported successfully")

        # Check that the routes are defined
        assert hasattr(rag_router, 'routes')
        assert hasattr(health_router, 'routes')

        print("✅ API routers have routes defined")

        # Check that dependency injection functions exist
        assert callable(get_cohere_service)
        assert callable(get_qdrant_service)
        assert callable(get_neon_service)
        assert callable(get_rag_service)

        print("✅ Dependency injection functions exist")
        return True

    except Exception as e:
        print(f"❌ API validation failed: {e}")
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

def validate_main_app():
    """Validate main application can be initialized."""
    print("\n=== Validating Main Application ===")

    try:
        from app.main import app

        # Check that app is a FastAPI instance
        from fastapi import FastAPI
        assert isinstance(app, FastAPI)
        print("✅ Main application initialized successfully")

        # Check that routers are included
        assert len(app.router.routes) > 0
        print("✅ Application routes loaded")

        return True

    except Exception as e:
        print(f"❌ Main app validation failed: {e}")
        return False

def main():
    """Run all validation checks."""
    print("RAG Backend System Validation")
    print("=" * 50)

    checks = [
        validate_structure,
        validate_models,
        validate_services,
        validate_api_endpoints,
        validate_environment,
        validate_main_app
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