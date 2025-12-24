#!/usr/bin/env python3
"""
Database connection validation script for the RAG backend.
This script validates that all database services (Qdrant and Neon) are accessible.
"""

import os
import sys
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
import psycopg2
from app.core import logging_config

# Set up logging
logger = logging_config.get_logger(__name__)

def validate_environment_variables():
    """Validate that all required environment variables are set."""
    required_vars = [
        "QDRANT_HOST",
        "QDRANT_API_KEY",
        "NEON_DB_URL",
        "COHERE_API_KEY",
        "GOOGLE_API_KEY"
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        return False

    logger.info("All required environment variables are set")
    return True

def test_qdrant_connection():
    """Test Qdrant database connection."""
    try:
        # Get environment variables
        host = os.getenv("QDRANT_HOST")
        api_key = os.getenv("QDRANT_API_KEY")

        # Validate required environment variables
        if not host:
            logger.error("QDRANT_HOST environment variable is not set")
            return False
        if not api_key:
            logger.error("QDRANT_API_KEY environment variable is not set")
            return False

        # Initialize Qdrant client based on whether host contains protocol
        if host.startswith("http://") or host.startswith("https://"):
            # For cloud instances with full URL
            client = QdrantClient(url=host, api_key=api_key)
        else:
            # For local instances with host:port format
            if ":" in host:
                # Split host:port format
                host_parts = host.split(":")
                host_addr = host_parts[0]
                port = int(host_parts[1])
                client = QdrantClient(host=host_addr, port=port, api_key=api_key)
            else:
                # Just host, assume default port
                client = QdrantClient(host=host, api_key=api_key)

        # Test connection by listing collections
        collections = client.get_collections()
        logger.info("Qdrant connection successful")
        logger.info(f"Available collections: {[c.name for c in collections.collections]}")
        return True

    except Exception as e:
        logger.error(f"Qdrant connection failed: {str(e)}")
        return False

def test_neon_connection():
    """Test Neon database connection."""
    try:
        # Get database URL from environment variable
        db_url = os.getenv("NEON_DB_URL")

        # Validate required environment variable
        if not db_url:
            logger.error("NEON_DB_URL environment variable is not set")
            return False

        # Test connection
        connection = psycopg2.connect(db_url)
        cursor = connection.cursor()

        # Test a simple query
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        logger.info("Neon database connection successful")
        return True

    except Exception as e:
        logger.error(f"Neon database connection failed: {str(e)}")
        return False

def main():
    """Main function to validate all database connections."""
    logger.info("Starting database connection validation...")

    # Validate environment variables
    if not validate_environment_variables():
        logger.error("Environment variable validation failed")
        return 1

    # Test Qdrant connection
    qdrant_ok = test_qdrant_connection()

    # Test Neon connection
    neon_ok = test_neon_connection()

    if qdrant_ok and neon_ok:
        logger.info("All database connections validated successfully!")
        return 0
    else:
        logger.error("Some database connections failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())