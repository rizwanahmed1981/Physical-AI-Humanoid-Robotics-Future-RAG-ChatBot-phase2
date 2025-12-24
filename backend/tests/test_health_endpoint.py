"""
Automated test suite for the enhanced health endpoint.
This test suite verifies the structure and functionality of the /health endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def test_client():
    """Provide a test client for the FastAPI application."""
    client = TestClient(app)
    return client


def test_health_endpoint_success(test_client):
    """
    Test that the health endpoint returns the expected structure and status.

    This test verifies:
    1. The endpoint returns a 200 OK status
    2. The response has the expected top-level structure
    3. All required service checks are present
    4. Each service check has the expected status
    """
    # Make a GET request to the health endpoint
    response = test_client.get("/health/")

    # Verify the response status code
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    # Parse the JSON response
    data = response.json()

    # Verify the top-level structure
    assert "status" in data, "Response should contain a 'status' field"
    assert "checks" in data, "Response should contain a 'checks' dictionary"

    # Verify the main status is present (could be "ok", "degraded", "error", or "unhealthy")
    assert data["status"] in ["ok", "degraded", "error", "unhealthy"], f"Unexpected status value: {data['status']}"

    # Verify that all required service checks are present
    required_services = ["qdrant", "neon", "cohere", "gemini"]
    checks = data["checks"]

    for service in required_services:
        assert service in checks, f"Missing check for service: {service}"
        assert "status" in checks[service], f"Missing 'status' field for {service}"
        assert "message" in checks[service], f"Missing 'message' field for {service}"

        # Verify each service check has a valid status
        assert checks[service]["status"] in ["healthy", "unhealthy"], f"Invalid status for {service}: {checks[service]['status']}"


def test_health_endpoint_structure():
    """
    Additional structural test for the health endpoint.
    """
    # Test that the endpoint exists and responds
    try:
        client = TestClient(app)
        response = client.get("/health/")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, dict)

        # Check for required top-level keys
        assert "status" in data
        assert "checks" in data
        assert isinstance(data["checks"], dict)

    except Exception as e:
        pytest.fail(f"Health endpoint test failed with error: {str(e)}")


if __name__ == "__main__":
    # This allows running the tests directly with pytest
    pytest.main([__file__, "-v"])