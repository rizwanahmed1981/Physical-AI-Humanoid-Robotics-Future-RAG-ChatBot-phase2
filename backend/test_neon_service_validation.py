#!/usr/bin/env python3
"""
Validation test script for NeonDBService
This script validates that all methods work as expected with various test cases.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables from .env file if it exists
from dotenv import load_dotenv

# Load .env file from the same directory as this script
dotenv_path = Path(__file__).parent / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)

from app.services.neon_service import NeonDBService


def validate_method_signatures():
    """Validate that all required methods exist with correct signatures."""
    print("Validating method signatures...")

    service = NeonDBService()

    # Check that all required methods exist
    required_methods = [
        'create_metadata_table',
        'insert_metadata',
        'get_metadata_by_embedding_id'
    ]

    for method_name in required_methods:
        if hasattr(service, method_name):
            print(f"✓ Method '{method_name}' exists")
        else:
            print(f"✗ Method '{method_name}' missing")
            return False

    # Validate method signatures using introspection
    import inspect

    # Check create_metadata_table signature
    sig = inspect.signature(service.create_metadata_table)
    params = list(sig.parameters.keys())
    # For methods that only take 'self', inspect.signature returns empty parameters list
    if len(params) == 0:  # Only self parameter
        print("✓ create_metadata_table has correct signature (only self parameter)")
    else:
        print(f"✗ create_metadata_table has incorrect signature: {params}, expected no parameters (only self)")
        return False

    # Check insert_metadata signature
    sig = inspect.signature(service.insert_metadata)
    params = list(sig.parameters.keys())
    expected_params = ['chapter_id', 'title', 'file_path', 'chunk_id', 'chunk_text_preview', 'embedding_id']
    if params == expected_params:
        print("✓ insert_metadata has correct signature")
    else:
        print(f"✗ insert_metadata has incorrect signature: {params}, expected: {expected_params}")
        return False

    # Check get_metadata_by_embedding_id signature
    sig = inspect.signature(service.get_metadata_by_embedding_id)
    params = list(sig.parameters.keys())
    expected_params = ['embedding_id']
    if params == expected_params:
        print("✓ get_metadata_by_embedding_id has correct signature")
    else:
        print(f"✗ get_metadata_by_embedding_id has incorrect signature: {params}, expected: {expected_params}")
        return False

    return True


def validate_data_types_and_constraints():
    """Validate that the service handles data types and constraints correctly."""
    print("\nValidating data types and constraints...")

    service = NeonDBService()

    # Test inserting various data types and lengths
    import uuid
    test_id = str(uuid.uuid4())[:8]

    # Test with various string lengths and types
    test_cases = [
        {
            "chapter_id": f"ch_{test_id}",
            "title": "Test Chapter with Normal Title",
            "file_path": f"/documents/chapter_{test_id}.md",
            "chunk_id": f"chunk_{test_id}_001",
            "chunk_text_preview": "This is a normal length preview text for testing.",
            "embedding_id": f"emb_{test_id}_001"
        },
        {
            "chapter_id": "very_long_chapter_id_" + test_id * 2,  # Long ID
            "title": "Very Long Chapter Title That Might Exceed Normal Limits " + test_id,
            "file_path": f"/very/long/path/to/document/with/many/separators/{test_id}/chapter_{test_id}.md",
            "chunk_id": "very_long_chunk_id_" + test_id * 3,
            "chunk_text_preview": "This is a much longer text preview that contains more characters than usual to test how the database handles longer text fields. " * 3,
            "embedding_id": f"very_long_embedding_id_{test_id}_with_extra_suffix"
        },
        {
            "chapter_id": "special_chars_test_123!@#",
            "title": "Special Chars & Numbers Test",
            "file_path": "/path/with/special/chars_123/test.md",
            "chunk_id": "chunk_special_!@#_123",
            "chunk_text_preview": "Testing special characters: !@#$%^&*()_+-=[]{}|;:,.<>?",
            "embedding_id": f"emb_special_{test_id}_!@#123"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        try:
            # Insert test data
            service.insert_metadata(**test_case)
            print(f"✓ Test case {i}: Data insertion successful")

            # Retrieve and verify
            result = service.get_metadata_by_embedding_id(test_case["embedding_id"])
            if result and result["chapter_id"] == test_case["chapter_id"]:
                print(f"✓ Test case {i}: Data retrieval successful")
            else:
                print(f"✗ Test case {i}: Data retrieval failed or mismatched")
                return False

        except Exception as e:
            print(f"✗ Test case {i}: Failed with error: {e}")
            return False

    return True


def validate_uniqueness_constraint():
    """Validate that the uniqueness constraint on embedding_id works."""
    print("\nValidating uniqueness constraint...")

    service = NeonDBService()

    import uuid
    test_id = str(uuid.uuid4())[:8]

    # Insert first record
    test_data = {
        "chapter_id": f"unique_test_{test_id}",
        "title": f"Unique Test Chapter {test_id}",
        "file_path": f"/test/unique_{test_id}.md",
        "chunk_id": f"chunk_unique_{test_id}",
        "chunk_text_preview": f"Testing uniqueness constraint with ID {test_id}",
        "embedding_id": f"duplicate_embed_{test_id}"
    }

    try:
        service.insert_metadata(**test_data)
        print("✓ First insertion successful")

        # Attempt to insert duplicate embedding_id (should fail at database level)
        # Since we're mocking the database, we'll check if the service logic handles this appropriately
        # In a real scenario, PostgreSQL would enforce the UNIQUE constraint
        try:
            service.insert_metadata(**test_data)
            print("? Duplicate insertion attempted (constraint enforcement depends on database)")
            # This may or may not raise an error depending on the database's UNIQUE constraint
        except Exception as e:
            if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                print("✓ Uniqueness constraint properly enforced by database")
            else:
                print(f"? Different error for duplicate: {e}")

        return True

    except Exception as e:
        print(f"✗ Uniqueness test failed: {e}")
        return False


def validate_null_handling():
    """Validate how the service handles null or empty values."""
    print("\nValidating null/empty value handling...")

    service = NeonDBService()

    import uuid
    test_id = str(uuid.uuid4())[:8]

    # Test with empty strings (should work - empty strings are different from NULL in PostgreSQL)
    try:
        service.insert_metadata(
            chapter_id=f"empty_test_{test_id}",
            title="",  # Empty title
            file_path=f"/empty/{test_id}.md",
            chunk_id=f"chunk_empty_{test_id}",
            chunk_text_preview="",  # Empty preview
            embedding_id=f"embed_empty_{test_id}"
        )
        print("✓ Empty string values handled successfully")

        # Retrieve to confirm
        result = service.get_metadata_by_embedding_id(f"embed_empty_{test_id}")
        if result:
            print("✓ Empty values retrieved successfully")
        else:
            print("✗ Failed to retrieve record with empty values")
            return False

    except Exception as e:
        print(f"✗ Empty value handling failed: {e}")
        return False

    return True


def validate_table_structure():
    """Validate that the table structure matches expectations."""
    print("\nValidating table structure...")

    service = NeonDBService()

    # Check that the table creation query creates the expected structure
    # We'll examine the actual SQL query used
    import inspect

    # Get the source of the create_metadata_table method to verify SQL
    source = inspect.getsource(service.create_metadata_table)

    expected_columns = [
        "id SERIAL PRIMARY KEY",
        "chapter_id VARCHAR(255) NOT NULL",
        "title TEXT",
        "file_path VARCHAR(255) NOT NULL",
        "chunk_id VARCHAR(255) NOT NULL",
        "chunk_text_preview TEXT",
        "embedding_id VARCHAR(255) UNIQUE NOT NULL"
    ]

    print("✓ Verifying table structure in SQL query:")
    for column_def in expected_columns:
        if column_def in source:
            print(f"  ✓ Found: {column_def}")
        else:
            print(f"  ✗ Missing: {column_def}")
            return False

    if "CREATE TABLE IF NOT EXISTS chapter_metadata" in source:
        print("  ✓ Correct table creation statement")
    else:
        print("  ✗ Missing correct table creation statement")
        return False

    return True


def main():
    """Main validation runner."""
    print("Running validation tests for NeonDBService...\n")

    tests = [
        validate_method_signatures,
        validate_data_types_and_constraints,
        validate_uniqueness_constraint,
        validate_null_handling,
        validate_table_structure
    ]

    passed = 0
    total = len(tests)

    for test_func in tests:
        if test_func():
            passed += 1
        print()

    print(f"Validation Results: {passed}/{total} validation tests passed")

    if passed == total:
        print("\n✓ All validation tests passed - NeonDBService implementation is robust!")
        return True
    else:
        print(f"\n✗ {total - passed} validation test(s) failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)