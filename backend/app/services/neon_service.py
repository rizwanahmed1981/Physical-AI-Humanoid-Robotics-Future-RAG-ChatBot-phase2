import os
import psycopg2
from psycopg2.extras import Json
from typing import Dict, Optional, Any
from app.core import logging_config

class NeonDBService:
    def __init__(self):
        """Initialize the Neon database service with connection URL from environment."""
        self.logger = logging_config.get_logger(__name__)

        # Get database URL from environment variable
        self.db_url = os.getenv("NEON_DB_URL")

        # Validate required environment variable
        if not self.db_url:
            self.logger.error("NEON_DB_URL environment variable is not set")
            raise ValueError("NEON_DB_URL environment variable is not set")

    def _get_connection(self):
        """
        Establish and return a psycopg2 connection to the Neon database.

        Returns:
            psycopg2.connection: Database connection object

        Raises:
            ValueError: If connection fails
        """
        self.logger.debug("Attempting to connect to Neon database")
        try:
            connection = psycopg2.connect(self.db_url)
            self.logger.info("Successfully connected to Neon database")
            return connection
        except Exception as e:
            self.logger.error("Failed to connect to Neon database", extra={"error": str(e)})
            raise ValueError(f"Failed to connect to Neon database: {str(e)}")

    def create_metadata_table(self):
        """
        Create the chapter_metadata table if it doesn't exist.

        Raises:
            ValueError: If table creation fails
        """
        self.logger.info("Creating metadata table in Neon database")
        connection = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()

            # Create table with specified schema
            create_table_query = """
            CREATE TABLE IF NOT EXISTS chapter_metadata (
                id SERIAL PRIMARY KEY,
                chapter_id VARCHAR(255) NOT NULL,
                title TEXT,
                file_path VARCHAR(255) NOT NULL,
                chunk_id VARCHAR(255) NOT NULL,
                chunk_text_preview TEXT,
                embedding_id VARCHAR(255) UNIQUE NOT NULL
            );
            """

            cursor.execute(create_table_query)
            connection.commit()
            self.logger.info("Metadata table created successfully")

        except Exception as e:
            self.logger.error("Failed to create metadata table", extra={"error": str(e)})
            raise ValueError(f"Failed to create metadata table: {str(e)}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def insert_metadata(self, chapter_id: str, title: str, file_path: str, chunk_id: str, chunk_text_preview: str, embedding_id: str):
        """
        Insert metadata record into the chapter_metadata table.

        Args:
            chapter_id: ID of the chapter
            title: Title of the chapter
            file_path: Path to the chapter file
            chunk_id: ID of the text chunk
            chunk_text_preview: Preview of the chunk text
            embedding_id: ID of the associated embedding

        Raises:
            ValueError: If insertion fails
        """
        self.logger.info("Inserting metadata record", extra={"chapter_id": chapter_id, "embedding_id": embedding_id})
        connection = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()

            # Insert metadata record
            insert_query = """
            INSERT INTO chapter_metadata
            (chapter_id, title, file_path, chunk_id, chunk_text_preview, embedding_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (
                chapter_id,
                title,
                file_path,
                chunk_id,
                chunk_text_preview,
                embedding_id
            ))

            connection.commit()
            self.logger.info("Metadata record inserted successfully")

        except Exception as e:
            self.logger.error("Failed to insert metadata", extra={"error": str(e)})
            raise ValueError(f"Failed to insert metadata: {str(e)}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def get_metadata_by_embedding_id(self, embedding_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve metadata record by embedding ID.

        Args:
            embedding_id: ID of the embedding to search for

        Returns:
            Dictionary containing metadata or None if not found

        Raises:
            ValueError: If retrieval fails
        """
        self.logger.debug("Retrieving metadata by embedding ID", extra={"embedding_id": embedding_id})
        connection = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()

            # Query metadata by embedding_id
            select_query = """
            SELECT id, chapter_id, title, file_path, chunk_id, chunk_text_preview, embedding_id
            FROM chapter_metadata
            WHERE embedding_id = %s
            """

            cursor.execute(select_query, (embedding_id,))
            result = cursor.fetchone()

            if result:
                # Convert to dictionary
                metadata = {
                    "id": result[0],
                    "chapter_id": result[1],
                    "title": result[2],
                    "file_path": result[3],
                    "chunk_id": result[4],
                    "chunk_text_preview": result[5],
                    "embedding_id": result[6]
                }
                self.logger.debug("Metadata retrieved successfully", extra={"metadata_keys": list(metadata.keys())})
                return metadata
            else:
                self.logger.debug("No metadata found for embedding ID", extra={"embedding_id": embedding_id})
                return None

        except Exception as e:
            self.logger.error("Failed to retrieve metadata", extra={"error": str(e), "embedding_id": embedding_id})
            raise ValueError(f"Failed to retrieve metadata: {str(e)}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def get_metadata_by_chunk_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve metadata record by chunk ID.

        Args:
            chunk_id: ID of the text chunk

        Returns:
            Dictionary containing metadata or None if not found

        Raises:
            ValueError: If retrieval fails
        """
        self.logger.debug("Retrieving metadata by chunk ID", extra={"chunk_id": chunk_id})
        connection = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()

            # Query metadata by chunk_id instead of embedding_id
            select_query = """
            SELECT id, chapter_id, title, file_path, chunk_id, chunk_text_preview, embedding_id
            FROM chapter_metadata
            WHERE chunk_id = %s
            """

            cursor.execute(select_query, (chunk_id,))
            result = cursor.fetchone()

            if result:
                # Convert to dictionary
                metadata = {
                    "id": result[0],
                    "chapter_id": result[1],
                    "title": result[2],
                    "file_path": result[3],
                    "chunk_id": result[4],
                    "chunk_text_preview": result[5],
                    "embedding_id": result[6]
                }
                self.logger.debug("Metadata retrieved successfully", extra={"metadata_keys": list(metadata.keys())})
                return metadata
            else:
                self.logger.debug("No metadata found for chunk ID", extra={"chunk_id": chunk_id})
                return None

        except Exception as e:
            self.logger.error("Error retrieving metadata by chunk ID", extra={"error": str(e), "chunk_id": chunk_id})
            raise ValueError(f"Error retrieving metadata by chunk ID: {str(e)}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    def clear_metadata_table(self):
        """
        Clear all records from the chapter_metadata table.

        Raises:
            ValueError: If clearing the table fails
        """
        self.logger.info("Clearing metadata table in Neon database")
        connection = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()

            # Clear all records from the table
            clear_table_query = "TRUNCATE TABLE chapter_metadata;"

            cursor.execute(clear_table_query)
            connection.commit()
            self.logger.info("Metadata table cleared successfully")

        except Exception as e:
            self.logger.error("Failed to clear metadata table", extra={"error": str(e)})
            # If TRUNCATE fails, try DELETE as an alternative
            try:
                clear_table_query = "DELETE FROM chapter_metadata;"
                cursor.execute(clear_table_query)
                connection.commit()
                self.logger.info("Metadata table cleared successfully using DELETE")
            except Exception as delete_error:
                self.logger.error("Failed to clear metadata table with DELETE", extra={"error": str(delete_error)})
                raise ValueError(f"Failed to clear metadata table: {str(delete_error)}")
        finally:
            if connection:
                cursor.close()
                connection.close()