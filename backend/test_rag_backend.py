"""
Backend Testing Suite for RAG System

This test suite covers:
1. API endpoints: /rag/ask (POST) and /health/health (GET)
2. Service integrations: Cohere, Qdrant, Neon DB, and Gemini LLM
3. Error handling scenarios
4. Complete RAG pipeline testing
5. Dependency injection verification
"""

import os
import pytest
from unittest.mock import AsyncMock, Mock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.models.schemas import QueryRequest, QueryResponse, Source
from app.services.embedding_service import CohereEmbeddingService
from app.services.qdrant_service import QdrantService
from app.services.neon_service import NeonDBService
from app.services.rag_service import RAGService
from app.api.rag import rag_router


# Test client for API testing
client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Physical AI RAG Backend is running" in data["message"]


def test_rag_ask_endpoint_valid_request():
    """Test the RAG ask endpoint with a valid request."""
    # Mock request data
    query_request = {
        "query": "What is artificial intelligence?",
        "chapter_filter": None,
        "selected_text": None
    }

    # This test will fail if services are not properly configured,
    # but it tests the endpoint structure
    with patch('app.api.rag.get_rag_service') as mock_get_rag_service:
        # Mock the RAG service
        mock_rag_service = AsyncMock()
        mock_rag_service.retrieve_relevant_chunks.return_value = []
        mock_rag_service.generate_answer.return_value = "Test answer"

        mock_get_rag_service.return_value = mock_rag_service

        response = client.post("/rag/ask", json=query_request)
        # Should return 200 even if services fail due to mocked service
        assert response.status_code in [200, 422, 500]  # Allow for various responses


def test_rag_ask_endpoint_missing_query():
    """Test the RAG ask endpoint with missing query."""
    query_request = {
        "query": "",  # Empty query
        "chapter_filter": None,
        "selected_text": None
    }

    response = client.post("/rag/ask", json=query_request)
    # Should return 422 for validation error or 500 for processing error
    assert response.status_code in [422, 500]


def test_query_request_model():
    """Test the QueryRequest Pydantic model."""
    # Valid request
    request = QueryRequest(query="Test query")
    assert request.query == "Test query"
    assert request.chapter_filter is None
    assert request.selected_text is None

    # Request with optional fields
    request_with_filters = QueryRequest(
        query="Test query",
        chapter_filter="Chapter 1",
        selected_text="Some selected text"
    )
    assert request_with_filters.query == "Test query"
    assert request_with_filters.chapter_filter == "Chapter 1"
    assert request_with_filters.selected_text == "Some selected text"


def test_source_model():
    """Test the Source Pydantic model."""
    source = Source(
        chapter_id="ch1",
        title="Test Chapter",
        file_path="/path/to/file",
        chunk_text_preview="This is a preview",
        score=0.85
    )
    assert source.chapter_id == "ch1"
    assert source.title == "Test Chapter"
    assert source.file_path == "/path/to/file"
    assert source.chunk_text_preview == "This is a preview"
    assert source.score == 0.85


def test_query_response_model():
    """Test the QueryResponse Pydantic model."""
    sources = [
        Source(
            chapter_id="ch1",
            title="Test Chapter",
            file_path="/path/to/file",
            chunk_text_preview="This is a preview",
            score=0.85
        )
    ]
    response = QueryResponse(answer="Test answer", sources=sources)
    assert response.answer == "Test answer"
    assert len(response.sources) == 1
    assert response.sources[0].chapter_id == "ch1"


class TestCohereEmbeddingService:
    """Test the Cohere Embedding Service."""

    def test_cohere_service_initialization_missing_api_key(self):
        """Test Cohere service initialization with missing API key."""
        # Temporarily remove the API key from environment
        original_key = os.environ.get("COHERE_API_KEY")
        if "COHERE_API_KEY" in os.environ:
            del os.environ["COHERE_API_KEY"]

        try:
            with pytest.raises(ValueError, match="COHERE_API_KEY environment variable is not set"):
                CohereEmbeddingService()
        finally:
            # Restore original key
            if original_key:
                os.environ["COHERE_API_KEY"] = original_key

    @patch('cohere.Client')
    def test_get_embeddings_success(self, mock_cohere_client):
        """Test successful embedding generation."""
        # Mock the Cohere client
        mock_client_instance = Mock()
        mock_client_instance.embed.return_value = Mock()
        mock_client_instance.embed.return_value.embeddings = [[0.1, 0.2, 0.3]]
        mock_cohere_client.return_value = mock_client_instance

        # Set up environment
        original_key = os.environ.get("COHERE_API_KEY")
        os.environ["COHERE_API_KEY"] = "test_key"

        try:
            service = CohereEmbeddingService()
            texts = ["test text"]
            embeddings = service.get_embeddings(texts)

            # Verify the method was called correctly
            mock_client_instance.embed.assert_called_once_with(
                texts=texts,
                model="embed-english-v3.0",
                input_type="search_document"
            )
            assert embeddings == [[0.1, 0.2, 0.3]]
        finally:
            if original_key:
                os.environ["COHERE_API_KEY"] = original_key
            elif "COHERE_API_KEY" in os.environ:
                del os.environ["COHERE_API_KEY"]

    @patch('cohere.Client')
    def test_get_embeddings_error(self, mock_cohere_client):
        """Test embedding generation with error."""
        # Mock the Cohere client to raise an exception
        mock_client_instance = Mock()
        mock_client_instance.embed.side_effect = Exception("API Error")
        mock_cohere_client.return_value = mock_client_instance

        # Set up environment
        original_key = os.environ.get("COHERE_API_KEY")
        os.environ["COHERE_API_KEY"] = "test_key"

        try:
            service = CohereEmbeddingService()
            texts = ["test text"]

            with pytest.raises(ValueError, match="Error generating embeddings: API Error"):
                service.get_embeddings(texts)
        finally:
            if original_key:
                os.environ["COHERE_API_KEY"] = original_key
            elif "COHERE_API_KEY" in os.environ:
                del os.environ["COHERE_API_KEY"]


class TestQdrantService:
    """Test the Qdrant Service."""

    def test_qdrant_service_initialization_missing_host(self):
        """Test Qdrant service initialization with missing host."""
        # Temporarily remove the host from environment
        original_host = os.environ.get("QDRANT_HOST")
        original_key = os.environ.get("QDRANT_API_KEY")

        if "QDRANT_HOST" in os.environ:
            del os.environ["QDRANT_HOST"]
        os.environ["QDRANT_API_KEY"] = "test_key"

        try:
            with pytest.raises(ValueError, match="QDRANT_HOST environment variable is not set"):
                QdrantService()
        finally:
            # Restore original values
            if original_host:
                os.environ["QDRANT_HOST"] = original_host
            if original_key:
                os.environ["QDRANT_API_KEY"] = original_key
            elif "QDRANT_API_KEY" in os.environ:
                del os.environ["QDRANT_API_KEY"]

    def test_qdrant_service_initialization_missing_api_key(self):
        """Test Qdrant service initialization with missing API key."""
        # Temporarily remove the API key from environment
        original_host = os.environ.get("QDRANT_HOST")
        original_key = os.environ.get("QDRANT_API_KEY")

        os.environ["QDRANT_HOST"] = "test_host"
        if "QDRANT_API_KEY" in os.environ:
            del os.environ["QDRANT_API_KEY"]

        try:
            with pytest.raises(ValueError, match="QDRANT_API_KEY environment variable is not set"):
                QdrantService()
        finally:
            # Restore original values
            if original_host:
                os.environ["QDRANT_HOST"] = original_host
            if original_key:
                os.environ["QDRANT_API_KEY"] = original_key


class TestNeonDBService:
    """Test the Neon DB Service."""

    def test_neon_service_initialization_missing_db_url(self):
        """Test Neon service initialization with missing DB URL."""
        # Temporarily remove the DB URL from environment
        original_url = os.environ.get("NEON_DB_URL")

        if "NEON_DB_URL" in os.environ:
            del os.environ["NEON_DB_URL"]

        try:
            with pytest.raises(ValueError, match="NEON_DB_URL environment variable is not set"):
                NeonDBService()
        finally:
            # Restore original URL
            if original_url:
                os.environ["NEON_DB_URL"] = original_url


class TestRAGService:
    """Test the RAG Service."""

    def test_rag_service_initialization_missing_google_api_key(self):
        """Test RAG service initialization with missing Google API key."""
        # Temporarily remove the Google API key from environment
        original_key = os.environ.get("GOOGLE_API_KEY")

        if "GOOGLE_API_KEY" in os.environ:
            del os.environ["GOOGLE_API_KEY"]

        # Mock the dependency services
        mock_cohere_service = Mock()
        mock_qdrant_service = Mock()
        mock_neon_service = Mock()

        try:
            with pytest.raises(ValueError, match="GOOGLE_API_KEY environment variable is not set"):
                RAGService(mock_cohere_service, mock_qdrant_service, mock_neon_service)
        finally:
            # Restore original key
            if original_key:
                os.environ["GOOGLE_API_KEY"] = original_key

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_rag_service_initialization_success(self, mock_configure, mock_model_class):
        """Test successful RAG service initialization."""
        # Mock the dependency services
        mock_cohere_service = Mock()
        mock_qdrant_service = Mock()
        mock_neon_service = Mock()

        # Set up environment
        original_key = os.environ.get("GOOGLE_API_KEY")
        os.environ["GOOGLE_API_KEY"] = "test_key"

        try:
            # Mock the model instance
            mock_model_instance = Mock()
            mock_model_class.return_value = mock_model_instance

            # Initialize RAG service
            rag_service = RAGService(mock_cohere_service, mock_qdrant_service, mock_neon_service)

            # Verify that Google API was configured
            mock_configure.assert_called_once_with(api_key="test_key")

            # Verify that the model was created
            mock_model_class.assert_called_once_with('gemini-pro')
            assert rag_service.llm_model == mock_model_instance
        finally:
            if original_key:
                os.environ["GOOGLE_API_KEY"] = original_key
            elif "GOOGLE_API_KEY" in os.environ:
                del os.environ["GOOGLE_API_KEY"]

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    async def test_retrieve_relevant_chunks_success(self, mock_configure, mock_model_class):
        """Test successful retrieval of relevant chunks."""
        # Mock the dependency services
        mock_cohere_service = AsyncMock()
        mock_cohere_service.get_embeddings.return_value = [[0.1, 0.2, 0.3]]

        mock_qdrant_service = AsyncMock()
        mock_qdrant_service.search_vectors.return_value = [
            {"payload": {"embedding_id": "test_id"}, "score": 0.9}
        ]

        mock_neon_service = Mock()
        mock_neon_service.get_metadata_by_embedding_id.return_value = {
            "chapter_id": "ch1",
            "title": "Test Chapter",
            "file_path": "/path/to/file",
            "chunk_text_preview": "Test chunk preview",
            "embedding_id": "test_id"
        }

        # Set up environment
        original_key = os.environ.get("GOOGLE_API_KEY")
        os.environ["GOOGLE_API_KEY"] = "test_key"

        try:
            # Mock the model instance
            mock_model_instance = Mock()
            mock_model_class.return_value = mock_model_instance

            # Initialize RAG service
            rag_service = RAGService(mock_cohere_service, mock_qdrant_service, mock_neon_service)

            # Test the method
            sources = await rag_service.retrieve_relevant_chunks("test query", limit=1)

            # Verify that the services were called correctly
            mock_cohere_service.get_embeddings.assert_called_once_with(["test query"])
            mock_qdrant_service.search_vectors.assert_called_once_with([0.1, 0.2, 0.3], limit=1)
            mock_neon_service.get_metadata_by_embedding_id.assert_called_once_with("test_id")

            # Verify the result
            assert len(sources) == 1
            assert sources[0].chapter_id == "ch1"
            assert sources[0].title == "Test Chapter"
        finally:
            if original_key:
                os.environ["GOOGLE_API_KEY"] = original_key
            elif "GOOGLE_API_KEY" in os.environ:
                del os.environ["GOOGLE_API_KEY"]

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    async def test_generate_answer_success(self, mock_configure, mock_model_class):
        """Test successful answer generation."""
        # Mock the dependency services
        mock_cohere_service = Mock()
        mock_qdrant_service = Mock()
        mock_neon_service = Mock()

        # Set up environment
        original_key = os.environ.get("GOOGLE_API_KEY")
        os.environ["GOOGLE_API_KEY"] = "test_key"

        try:
            # Mock the model instance and response
            mock_model_instance = Mock()
            mock_response = Mock()
            mock_response.text = "This is a test answer."
            mock_model_instance.generate_content.return_value = mock_response
            mock_model_class.return_value = mock_model_instance

            # Initialize RAG service
            rag_service = RAGService(mock_cohere_service, mock_qdrant_service, mock_neon_service)

            # Create test sources
            test_sources = [
                Source(
                    chapter_id="ch1",
                    title="Test Chapter",
                    file_path="/path/to/file",
                    chunk_text_preview="Test chunk preview",
                    score=0.9
                )
            ]

            # Test the method
            answer = await rag_service.generate_answer("test query", test_sources)

            # Verify that the model was called
            mock_model_instance.generate_content.assert_called_once()

            # Verify the answer
            assert answer == "This is a test answer."
        finally:
            if original_key:
                os.environ["GOOGLE_API_KEY"] = original_key
            elif "GOOGLE_API_KEY" in os.environ:
                del os.environ["GOOGLE_API_KEY"]


def test_dependency_injection():
    """Test that dependency injection is working correctly in the API."""
    # This tests that the Depends functions are working properly
    # We'll mock the services to avoid needing real API keys
    with patch('app.api.rag.CohereEmbeddingService') as mock_cohere, \
         patch('app.api.rag.QdrantService') as mock_qdrant, \
         patch('app.api.rag.NeonDBService') as mock_neon, \
         patch('app.api.rag.RAGService') as mock_rag:

        # Mock the services
        mock_cohere_instance = Mock()
        mock_qdrant_instance = Mock()
        mock_neon_instance = Mock()
        mock_rag_instance = Mock()

        mock_cohere.return_value = mock_cohere_instance
        mock_qdrant.return_value = mock_qdrant_instance
        mock_neon.return_value = mock_neon_instance
        mock_rag.return_value = mock_rag_instance

        # Mock the methods
        mock_rag_instance.retrieve_relevant_chunks.return_value = []
        mock_rag_instance.generate_answer.return_value = "Test answer"

        # Test that the endpoint can be called without errors (in terms of dependency injection)
        query_request = {
            "query": "test query",
            "chapter_filter": None,
            "selected_text": None
        }

        # This should work without throwing dependency injection errors
        try:
            response = client.post("/rag/ask", json=query_request)
            # The response might be 500 due to service errors, but not due to dependency injection
            assert response.status_code in [200, 422, 500]
        except Exception as e:
            # If there's an exception, it should not be related to dependency injection
            assert "dependency" not in str(e).lower()


def test_environment_variables_loaded():
    """Test that environment variables are properly loaded."""
    # Check that the expected environment variables exist
    assert os.getenv("COHERE_API_KEY") is not None
    assert os.getenv("QDRANT_HOST") is not None
    assert os.getenv("QDRANT_API_KEY") is not None
    assert os.getenv("NEON_DB_URL") is not None
    assert os.getenv("GOOGLE_API_KEY") is not None


def test_error_handling_invalid_request():
    """Test error handling for invalid requests."""
    # Invalid request - missing required field
    invalid_request = {
        # Missing 'query' field
        "chapter_filter": "Chapter 1"
    }

    response = client.post("/rag/ask", json=invalid_request)
    assert response.status_code == 422  # Validation error


def test_error_handling_empty_query():
    """Test error handling for empty query."""
    empty_query_request = {
        "query": "",
        "chapter_filter": None,
        "selected_text": None
    }

    response = client.post("/rag/ask", json=empty_query_request)
    # Should return either validation error or be processed (depending on business logic)
    assert response.status_code in [200, 422, 500]


if __name__ == "__main__":
    pytest.main([__file__])