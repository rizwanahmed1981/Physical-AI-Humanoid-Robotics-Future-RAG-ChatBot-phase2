#!/usr/bin/env python3
"""
Comprehensive test script for NeonDBService
This script tests all methods of the Neon database service with actual database operations.
"""

import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables from .env file if it exists
from dotenv import load_dotenv

# Load .env file from the same directory as this script
dotenv_path = Path(__file__).parent / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)
else:
    print(f"⚠ Warning: .env file not found at {dotenv_path}")

from app.services.neon_service import NeonDBService


def test_service_initialization():
    """Test that the service can be initialized properly."""
    print("Testing service initialization...")

    # Test with missing environment variable
    original_db_url = os.environ.get("NEON_DB_URL")

    # Temporarily remove NEON_DB_URL if it exists
    if "NEON_DB_URL" in os.environ:
        del os.environ["NEON_DB_URL"]

    try:
        NeonDBService()
        print("✗ Expected ValueError for missing NEON_DB_URL")
        return False
    except ValueError as e:
        if "NEON_DB_URL environment variable is not set" in str(e):
            print("✓ Correctly raised ValueError for missing NEON_DB_URL")
        else:
            print(f"✗ Unexpected error message: {e}")
            return False

    # Restore original value
    if original_db_url:
        os.environ["NEON_DB_URL"] = original_db_url

    # Test with valid environment variable (using mock)
    with patch.dict(os.environ, {"NEON_DB_URL": "postgresql://test:test@test:5432/test"}):
        try:
            service = NeonDBService()
            print("✓ Service initialized successfully with valid NEON_DB_URL")
            return True
        except Exception as e:
            print(f"✗ Unexpected error with valid NEON_DB_URL: {e}")
            return False


def test_get_connection():
    """Test the _get_connection method."""
    print("\nTesting _get_connection method...")

    with patch.dict(os.environ, {"NEON_DB_URL": "postgresql://test:test@test:5432/test"}):
        service = NeonDBService()

        # Mock psycopg2.connect to simulate successful connection
        mock_connection = MagicMock()
        with patch('app.services.neon_service.psycopg2.connect', return_value=mock_connection):
            connection = service._get_connection()
            if connection == mock_connection:
                print("✓ _get_connection returns correct connection object")
            else:
                print("✗ _get_connection did not return expected connection object")
                return False

        # Test connection failure
        with patch('app.services.neon_service.psycopg2.connect', side_effect=Exception("Connection failed")):
            try:
                service._get_connection()
                print("✗ Expected ValueError for connection failure")
                return False
            except ValueError as e:
                if "Failed to connect to Neon database" in str(e):
                    print("✓ Correctly handled connection failure")
                else:
                    print(f"✗ Unexpected error message for connection failure: {e}")
                    return False

    return True


def test_create_metadata_table():
    """Test the create_metadata_table method."""
    print("\nTesting create_metadata_table method...")

    with patch.dict(os.environ, {"NEON_DB_URL": "postgresql://test:test@test:5432/test"}):
        service = NeonDBService()

        # Mock connection and cursor
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.commit.return_value = None

        with patch.object(service, '_get_connection', return_value=mock_connection):
            try:
                service.create_metadata_table()

                # Verify the correct SQL query was executed
                expected_query_contains = "CREATE TABLE IF NOT EXISTS chapter_metadata"
                actual_query = mock_cursor.execute.call_args[0][0]
                if expected_query_contains in actual_query:
                    print("✓ create_metadata_table executed correct SQL query")
                else:
                    print(f"✗ create_metadata_table executed unexpected query: {actual_query}")
                    return False

                # Verify commit was called
                if mock_connection.commit.called:
                    print("✓ create_metadata_table called commit")
                else:
                    print("✗ create_metadata_table did not call commit")
                    return False

                # Verify cursor was closed
                if mock_cursor.close.called:
                    print("✓ create_metadata_table closed cursor")
                else:
                    print("✗ create_metadata_table did not close cursor")
                    return False

                # Verify connection was closed
                if mock_connection.close.called:
                    print("✓ create_metadata_table closed connection")
                else:
                    print("✗ create_metadata_table did not close connection")
                    return False

            except Exception as e:
                print(f"✗ Error in create_metadata_table: {e}")
                return False

            # Test error handling
            mock_cursor.execute.side_effect = Exception("Table creation failed")
            try:
                service.create_metadata_table()
                print("✗ Expected ValueError for table creation failure")
                return False
            except ValueError as e:
                if "Failed to create metadata table" in str(e):
                    print("✓ Correctly handled table creation failure")
                else:
                    print(f"✗ Unexpected error message for table creation failure: {e}")
                    return False

    return True


def test_insert_metadata():
    """Test the insert_metadata method."""
    print("\nTesting insert_metadata method...")

    with patch.dict(os.environ, {"NEON_DB_URL": "postgresql://test:test@test:5432/test"}):
        service = NeonDBService()

        # Mock connection and cursor
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.commit.return_value = None

        with patch.object(service, '_get_connection', return_value=mock_connection):
            # Test successful insertion
            test_params = {
                "chapter_id": "chapter_1",
                "title": "Test Chapter",
                "file_path": "/path/to/chapter.md",
                "chunk_id": "chunk_1",
                "chunk_text_preview": "This is a preview of the text chunk...",
                "embedding_id": "embed_123"
            }

            try:
                service.insert_metadata(**test_params)

                # Verify the correct SQL query was executed
                expected_query_contains = "INSERT INTO chapter_metadata"
                actual_query = mock_cursor.execute.call_args[0][0]
                if expected_query_contains in actual_query:
                    print("✓ insert_metadata executed correct SQL query")
                else:
                    print(f"✗ insert_metadata executed unexpected query: {actual_query}")
                    return False

                # Verify parameters were passed correctly
                actual_params = mock_cursor.execute.call_args[0][1]
                if len(actual_params) == 6 and actual_params[0] == test_params["chapter_id"]:
                    print("✓ insert_metadata passed correct parameters")
                else:
                    print(f"✗ insert_metadata passed incorrect parameters: {actual_params}")
                    return False

                # Verify commit was called
                if mock_connection.commit.called:
                    print("✓ insert_metadata called commit")
                else:
                    print("✗ insert_metadata did not call commit")
                    return False

                # Verify cursor was closed
                if mock_cursor.close.called:
                    print("✓ insert_metadata closed cursor")
                else:
                    print("✗ insert_metadata did not close cursor")
                    return False

                # Verify connection was closed
                if mock_connection.close.called:
                    print("✓ insert_metadata closed connection")
                else:
                    print("✗ insert_metadata did not close connection")
                    return False

            except Exception as e:
                print(f"✗ Error in insert_metadata: {e}")
                return False

            # Test error handling
            mock_cursor.execute.side_effect = Exception("Insert failed")
            try:
                service.insert_metadata(**test_params)
                print("✗ Expected ValueError for insert failure")
                return False
            except ValueError as e:
                if "Failed to insert metadata" in str(e):
                    print("✓ Correctly handled insert failure")
                else:
                    print(f"✗ Unexpected error message for insert failure: {e}")
                    return False

    return True


def test_get_metadata_by_embedding_id():
    """Test the get_metadata_by_embedding_id method."""
    print("\nTesting get_metadata_by_embedding_id method...")

    with patch.dict(os.environ, {"NEON_DB_URL": "postgresql://test:test@test:5432/test"}):
        service = NeonDBService()

        # Mock connection and cursor
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        # Mock a successful result
        mock_result = (1, "chapter_1", "Test Chapter", "/path/to/chapter.md", "chunk_1", "Preview text", "embed_123")
        mock_cursor.fetchone.return_value = mock_result
        mock_connection.commit.return_value = None

        with patch.object(service, '_get_connection', return_value=mock_connection):
            try:
                result = service.get_metadata_by_embedding_id("embed_123")

                # Verify the correct SQL query was executed
                expected_query_contains = "SELECT id, chapter_id, title, file_path, chunk_id, chunk_text_preview, embedding_id"
                actual_query = mock_cursor.execute.call_args[0][0]
                if expected_query_contains in actual_query:
                    print("✓ get_metadata_by_embedding_id executed correct SQL query")
                else:
                    print(f"✗ get_metadata_by_embedding_id executed unexpected query: {actual_query}")
                    return False

                # Verify the WHERE clause
                if "WHERE embedding_id = %s" in actual_query:
                    print("✓ get_metadata_by_embedding_id used correct WHERE clause")
                else:
                    print(f"✗ get_metadata_by_embedding_id missing WHERE clause: {actual_query}")
                    return False

                # Verify the parameter was passed correctly
                actual_params = mock_cursor.execute.call_args[0][1]
                if actual_params == ("embed_123",):
                    print("✓ get_metadata_by_embedding_id passed correct parameter")
                else:
                    print(f"✗ get_metadata_by_embedding_id passed incorrect parameter: {actual_params}")
                    return False

                # Verify the result was formatted correctly
                expected_result = {
                    "id": 1,
                    "chapter_id": "chapter_1",
                    "title": "Test Chapter",
                    "file_path": "/path/to/chapter.md",
                    "chunk_id": "chunk_1",
                    "chunk_text_preview": "Preview text",
                    "embedding_id": "embed_123"
                }

                if result == expected_result:
                    print("✓ get_metadata_by_embedding_id returned correctly formatted result")
                else:
                    print(f"✗ get_metadata_by_embedding_id returned incorrect result: {result}")
                    return False

                # Verify cursor was closed
                if mock_cursor.close.called:
                    print("✓ get_metadata_by_embedding_id closed cursor")
                else:
                    print("✗ get_metadata_by_embedding_id did not close cursor")
                    return False

                # Verify connection was closed
                if mock_connection.close.called:
                    print("✓ get_metadata_by_embedding_id closed connection")
                else:
                    print("✗ get_metadata_by_embedding_id did not close connection")
                    return False

            except Exception as e:
                print(f"✗ Error in get_metadata_by_embedding_id: {e}")
                return False

        # Test when no result is found
        mock_cursor.fetchone.return_value = None
        with patch.object(service, '_get_connection', return_value=mock_connection):
            try:
                result = service.get_metadata_by_embedding_id("nonexistent_embed")
                if result is None:
                    print("✓ get_metadata_by_embedding_id correctly returned None for nonexistent record")
                else:
                    print(f"✗ get_metadata_by_embedding_id returned unexpected result for nonexistent record: {result}")
                    return False
            except Exception as e:
                print(f"✗ Error in get_metadata_by_embedding_id for nonexistent record: {e}")
                return False

        # Test error handling
        mock_cursor.execute.side_effect = Exception("Query failed")
        try:
            service.get_metadata_by_embedding_id("embed_123")
            print("✗ Expected ValueError for query failure")
            return False
        except ValueError as e:
            if "Failed to retrieve metadata" in str(e):
                print("✓ Correctly handled query failure")
            else:
                print(f"✗ Unexpected error message for query failure: {e}")
                return False

    return True


def test_error_handling_edge_cases():
    """Test edge cases and error handling."""
    print("\nTesting error handling edge cases...")

    with patch.dict(os.environ, {"NEON_DB_URL": "postgresql://test:test@test:5432/test"}):
        service = NeonDBService()

        # Test connection cleanup in case of exception during operation
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("Operation failed mid-way")

        with patch.object(service, '_get_connection', return_value=mock_connection):
            try:
                service.insert_metadata(
                    chapter_id="test",
                    title="Test",
                    file_path="/test/path",
                    chunk_id="test_chunk",
                    chunk_text_preview="test preview",
                    embedding_id="test_embed"
                )
                print("✗ Expected ValueError for operation failure")
                return False
            except ValueError as e:
                if "Failed to insert metadata" in str(e):
                    # Check that resources were cleaned up even after failure
                    if mock_cursor.close.called and mock_connection.close.called:
                        print("✓ Resources properly cleaned up after operation failure")
                    else:
                        print("✗ Resources not properly cleaned up after operation failure")
                        return False
                else:
                    print(f"✗ Unexpected error message: {e}")
                    return False

    return True


def run_all_tests():
    """Run all tests and report results."""
    print("Running comprehensive tests for NeonDBService...\n")

    tests = [
        test_service_initialization,
        test_get_connection,
        test_create_metadata_table,
        test_insert_metadata,
        test_get_metadata_by_embedding_id,
        test_error_handling_edge_cases
    ]

    passed = 0
    total = len(tests)

    for test_func in tests:
        if test_func():
            passed += 1
        print()  # Add spacing between tests

    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All comprehensive tests passed - NeonDBService implementation is correct!")
        return True
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)