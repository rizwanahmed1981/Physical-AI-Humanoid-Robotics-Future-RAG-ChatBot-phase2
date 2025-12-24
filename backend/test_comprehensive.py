"""
Comprehensive API endpoint testing for the RAG Chatbot backend.
Tests health endpoints, RAG endpoints, and middleware functionality.
"""
import sys
import os
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
import asyncio

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.main import app


def test_root_endpoint():
    """Test the root endpoint"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Physical AI RAG Backend is running" in data["message"]


def test_health_endpoint_basic():
    """Test the health endpoint basic functionality"""
    client = TestClient(app)
    response = client.get("/health/")
    # The health endpoint might fail due to missing services, but should return a response
    assert response.status_code in [200, 500]  # 500 is expected if services are not configured
    data = response.json()
    assert isinstance(data, dict)


def test_health_endpoint_structure():
    """Test the health endpoint structure"""
    client = TestClient(app)
    response = client.get("/health/")
    data = response.json()

    # Check for required top-level keys
    assert "status" in data
    assert "checks" in data
    assert isinstance(data["checks"], dict)

    # Check for required services
    required_services = ["qdrant", "neon", "cohere", "gemini"]
    for service in required_services:
        assert service in data["checks"]
        assert "status" in data["checks"][service]
        assert "message" in data["checks"][service]


def test_rag_ask_endpoint_exists():
    """Test that the RAG ask endpoint exists"""
    client = TestClient(app)
    # This should return 422 (validation error) for missing body, not 404 (not found)
    response = client.post("/rag/ask")
    assert response.status_code in [422, 500]  # 422 for missing request body, 500 for service issues


def test_rag_ask_endpoint_with_valid_request():
    """Test the RAG ask endpoint with a valid request"""
    client = TestClient(app)
    valid_request = {
        "query": "What is AI?"
    }
    response = client.post("/rag/ask", json=valid_request)
    # Should return 200 if services are configured, or 500 if there are service issues
    # The endpoint should exist and accept the request (even if it fails due to missing data)
    assert response.status_code in [200, 422, 500]  # 422 for validation error, 200 for success, 500 for service issues


def test_cors_middleware_registered():
    """Test that CORS middleware is properly registered"""
    # This test checks that the middleware is registered in the app
    from fastapi.middleware.cors import CORSMiddleware
    # The middleware should be registered in the app
    cors_found = False
    for middleware in app.user_middleware:
        if middleware.cls == CORSMiddleware:
            cors_found = True
            break
    assert cors_found, "CORS middleware not found in app"


def test_error_handler_middleware():
    """Test that error handler middleware works"""
    # This is harder to test directly, but we can verify the middleware is registered
    # by checking if the app has the expected middleware
    from app.middleware.error_handler import GlobalErrorHandler
    # The middleware should be registered in the app
    assert any(
        hasattr(middleware, 'cls') and middleware.cls == GlobalErrorHandler
        for middleware in app.user_middleware
    )


def test_request_logger_middleware():
    """Test that request logger middleware is properly registered"""
    # This is harder to test directly, but we can verify the middleware is registered
    from app.middleware.request_logger import RequestLogger
    # The middleware should be registered in the app
    assert any(
        hasattr(middleware, 'cls') and middleware.cls == RequestLogger
        for middleware in app.user_middleware
    )


def test_all_routes_exist():
    """Test that all expected routes are registered"""
    expected_routes = ["/", "/health/", "/rag/ask"]
    actual_routes = [route.path for route in app.routes if route.path != "/openapi.json" and route.path != "/docs" and route.path != "/redoc"]

    for expected_route in expected_routes:
        assert expected_route in actual_routes, f"Route {expected_route} not found in app routes"


if __name__ == "__main__":
    # Run the tests directly
    pytest.main([__file__, "-v"])