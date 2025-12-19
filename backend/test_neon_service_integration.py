#!/usr/bin/env python3
"""
Integration test script for NeonDBService
This script tests the Neon database service with actual database operations if a real database is configured.
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


def test_full_integration_flow():
    """Test the complete integration flow of NeonDBService."""
    print("Testing full integration flow for NeonDBService...")

    # Check if we have a real database URL
    db_url = os.getenv("NEON_DB_URL")

    if not db_url:
        print("No NEON_DB_URL found, testing with mock database connection...")

        # Test with mocked real database operations
        with patch.dict(os.environ, {"NEON_DB_URL": "postgresql://test:test@test:5432/test"}):
            service = NeonDBService()

            # Mock a real database connection for integration testing
            mock_connection = MagicMock()
            mock_cursor = MagicMock()
            mock_connection.cursor.return_value = mock_cursor
            mock_connection.commit.return_value = None

            with patch('app.services.neon_service.psycopg2.connect', return_value=mock_connection):

                # Test 1: Create metadata table
                try:
                    service.create_metadata_table()
                    print("✓ Table creation flow completed successfully")
                except Exception as e:
                    print(f"✗ Table creation flow failed: {e}")
                    return False

                # Test 2: Insert metadata
                try:
                    service.insert_metadata(
                        chapter_id="test_chapter_1",
                        title="Test Chapter 1",
                        file_path="/docs/test_chapter_1.md",
                        chunk_id="chunk_001",
                        chunk_text_preview="This is a sample text chunk for testing purposes.",
                        embedding_id="embed_test_001"
                    )
                    print("✓ Metadata insertion flow completed successfully")

                    # Verify the insert query was called correctly
                    assert mock_cursor.execute.called
                    insert_call_args = mock_cursor.execute.call_args[0]
                    assert "INSERT INTO chapter_metadata" in insert_call_args[0]
                    assert len(insert_call_args[1]) == 6  # 6 parameters
                    print("✓ Insert query has correct structure and parameters")

                except Exception as e:
                    print(f"✗ Metadata insertion flow failed: {e}")
                    return False

                # Test 3: Retrieve metadata
                try:
                    # Mock a result for the select query
                    mock_cursor.fetchone.return_value = (
                        1, "test_chapter_1", "Test Chapter 1",
                        "/docs/test_chapter_1.md", "chunk_001",
                        "This is a sample text chunk for testing purposes.",
                        "embed_test_001"
                    )

                    result = service.get_metadata_by_embedding_id("embed_test_001")

                    expected_result = {
                        "id": 1,
                        "chapter_id": "test_chapter_1",
                        "title": "Test Chapter 1",
                        "file_path": "/docs/test_chapter_1.md",
                        "chunk_id": "chunk_001",
                        "chunk_text_preview": "This is a sample text chunk for testing purposes.",
                        "embedding_id": "embed_test_001"
                    }

                    if result == expected_result:
                        print("✓ Metadata retrieval flow completed successfully with correct result")
                    else:
                        print(f"✗ Metadata retrieval returned incorrect result: {result}")
                        return False

                except Exception as e:
                    print(f"✗ Metadata retrieval flow failed: {e}")
                    return False

                # Test 4: Handle non-existent record
                try:
                    mock_cursor.fetchone.return_value = None
                    result = service.get_metadata_by_embedding_id("non_existent")

                    if result is None:
                        print("✓ Non-existent record handled correctly (returned None)")
                    else:
                        print(f"✗ Non-existent record not handled correctly: {result}")
                        return False

                except Exception as e:
                    print(f"✗ Non-existent record handling failed: {e}")
                    return False

        print("✓ Mock integration flow completed successfully")
        return True
    else:
        print(f"Found NEON_DB_URL, attempting real database connection...")

        try:
            # Initialize service with real database URL
            service = NeonDBService()

            # Test creating the table
            print("Creating metadata table...")
            service.create_metadata_table()
            print("✓ Metadata table created/verified successfully")

            # Generate unique test values to avoid conflicts
            import uuid
            unique_id = str(uuid.uuid4())[:8]  # Short unique identifier

            # Test inserting metadata
            print("Inserting test metadata...")
            service.insert_metadata(
                chapter_id=f"integration_test_{unique_id}",
                title=f"Integration Test Chapter {unique_id}",
                file_path=f"/test/integration_{unique_id}.md",
                chunk_id=f"chunk_{unique_id}",
                chunk_text_preview=f"This is an integration test chunk with ID {unique_id}.",
                embedding_id=f"embed_integration_{unique_id}"
            )
            print("✓ Test metadata inserted successfully")

            # Test retrieving the inserted metadata
            print("Retrieving test metadata...")
            result = service.get_metadata_by_embedding_id(f"embed_integration_{unique_id}")

            if result and result['chapter_id'] == f"integration_test_{unique_id}":
                print("✓ Test metadata retrieved successfully")
                print(f"  Retrieved: {result}")
            else:
                print(f"✗ Failed to retrieve test metadata: {result}")
                return False

            # Test retrieving non-existent metadata
            print("Testing non-existent metadata retrieval...")
            non_existent_result = service.get_metadata_by_embedding_id(f"non_existent_{unique_id}")
            if non_existent_result is None:
                print("✓ Non-existent metadata correctly returned None")
            else:
                print(f"✗ Non-existent metadata returned unexpected result: {non_existent_result}")
                return False

            print("✓ Real database integration flow completed successfully")
            return True

        except Exception as e:
            print(f"✗ Real database integration failed: {e}")
            print("Note: This might be expected if the database is not accessible or credentials are invalid")
            return False


def test_error_handling_comprehensive():
    """Test comprehensive error handling scenarios."""
    print("\nTesting comprehensive error handling...")

    # Test initialization without DB URL
    original_db_url = os.environ.get("NEON_DB_URL")
    if "NEON_DB_URL" in os.environ:
        del os.environ["NEON_DB_URL"]

    try:
        NeonDBService()
        print("✗ Should have raised ValueError for missing DB URL")
        return False
    except ValueError as e:
        if "NEON_DB_URL environment variable is not set" in str(e):
            print("✓ Properly handles missing NEON_DB_URL")
        else:
            print(f"✗ Incorrect error message for missing DB URL: {e}")
            return False

    # Restore original value
    if original_db_url:
        os.environ["NEON_DB_URL"] = original_db_url

    # Test with mocked connection failures
    with patch.dict(os.environ, {"NEON_DB_URL": "postgresql://test:test@test:5432/test"}):
        service = NeonDBService()

        # Test connection failure
        with patch('app.services.neon_service.psycopg2.connect', side_effect=Exception("Connection failed")):
            try:
                service.create_metadata_table()
                print("✗ Should have raised ValueError for connection failure")
                return False
            except ValueError as e:
                if "Failed to connect to Neon database" in str(e):
                    print("✓ Properly handles connection failures")
                else:
                    print(f"✗ Incorrect error message for connection failure: {e}")
                    return False

        # Test operation failures
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor

        with patch('app.services.neon_service.psycopg2.connect', return_value=mock_connection):
            # Test table creation failure
            mock_cursor.execute.side_effect = Exception("Table creation failed")
            try:
                service.create_metadata_table()
                print("✗ Should have raised ValueError for table creation failure")
                return False
            except ValueError as e:
                if "Failed to create metadata table" in str(e):
                    print("✓ Properly handles table creation failures")
                else:
                    print(f"✗ Incorrect error message for table creation failure: {e}")
                    return False

            # Test insert failure
            mock_cursor.execute.side_effect = Exception("Insert failed")
            try:
                service.insert_metadata(
                    chapter_id="test", title="Test", file_path="/test",
                    chunk_id="test", chunk_text_preview="test", embedding_id="test"
                )
                print("✗ Should have raised ValueError for insert failure")
                return False
            except ValueError as e:
                if "Failed to insert metadata" in str(e):
                    print("✓ Properly handles insert failures")
                else:
                    print(f"✗ Incorrect error message for insert failure: {e}")
                    return False

            # Test query failure
            mock_cursor.execute.side_effect = Exception("Query failed")
            try:
                service.get_metadata_by_embedding_id("test")
                print("✗ Should have raised ValueError for query failure")
                return False
            except ValueError as e:
                if "Failed to retrieve metadata" in str(e):
                    print("✓ Properly handles query failures")
                else:
                    print(f"✗ Incorrect error message for query failure: {e}")
                    return False

    print("✓ Comprehensive error handling tests passed")
    return True


def main():
    """Main test runner."""
    print("Running integration tests for NeonDBService...\n")

    success1 = test_full_integration_flow()
    success2 = test_error_handling_comprehensive()

    if success1 and success2:
        print("\n✓ All integration tests passed - NeonDBService is ready for production!")
        return True
    else:
        print("\n✗ Some integration tests failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)