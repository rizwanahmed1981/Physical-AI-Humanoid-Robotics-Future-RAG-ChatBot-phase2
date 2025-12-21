import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, Filter, FieldCondition
from typing import List, Dict, Any
from app.core import logging_config

class QdrantService:
    def __init__(self, collection_name: str = "textbook_chapters"):
        """Initialize the Qdrant service with client and collection name."""
        self.logger = logging_config.get_logger(__name__)

        # Get environment variables
        host = os.getenv("QDRANT_HOST")
        api_key = os.getenv("QDRANT_API_KEY")

        # Validate required environment variables
        if not host:
            self.logger.error("QDRANT_HOST environment variable is not set")
            raise ValueError("QDRANT_HOST environment variable is not set")
        if not api_key:
            self.logger.error("QDRANT_API_KEY environment variable is not set")
            raise ValueError("QDRANT_API_KEY environment variable is not set")

        # Initialize Qdrant client based on whether host contains protocol
        if host.startswith("http://") or host.startswith("https://"):
            # For cloud instances with full URL
            self.client = QdrantClient(url=host, api_key=api_key)
        else:
            # For local instances with host:port format
            if ":" in host:
                # Split host:port format
                host_parts = host.split(":")
                host_addr = host_parts[0]
                port = int(host_parts[1])
                self.client = QdrantClient(host=host_addr, port=port, api_key=api_key)
            else:
                # Just host, assume default port
                self.client = QdrantClient(host=host, api_key=api_key)

        self.collection_name = collection_name

    async def create_collection(self, vector_size: int = 1024) -> bool:
        """
        Create a Qdrant collection with the specified vector size.

        Args:
            vector_size: Size of the vectors (default 1024 for Cohere embeddings)

        Returns:
            True if collection was created successfully, False otherwise
        """
        self.logger.info("Creating Qdrant collection", extra={"collection_name": self.collection_name, "vector_size": vector_size})

        try:
            # Create collection with cosine distance
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            self.logger.info("Qdrant collection created successfully")
            return True
        except Exception as e:
            self.logger.error("Failed to create Qdrant collection", extra={"error": str(e)})
            raise ValueError(f"Failed to create collection: {str(e)}")

    async def upsert_vectors(self, vectors: List[List[float]], payloads: List[Dict[str, Any]], ids: List[str] = None) -> bool:
        """
        Insert or update vectors in the Qdrant collection.

        Args:
            vectors: List of vector embeddings
            payloads: List of metadata dictionaries corresponding to each vector
            ids: Optional list of IDs for the vectors

        Returns:
            True if upsert was successful, False otherwise
        """
        self.logger.info("Upserting vectors to Qdrant", extra={"collection_name": self.collection_name, "vector_count": len(vectors)})

        try:
            # Prepare points for upsert
            points = []
            for i, (vector, payload) in enumerate(zip(vectors, payloads)):
                # Use integer IDs or provided IDs (ensuring they're proper format)
                point_id = ids[i] if ids and i < len(ids) else i  # Use integer instead of str(i)
                points.append({
                    "id": point_id,
                    "vector": vector,
                    "payload": payload
                })

            # Perform upsert operation
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            self.logger.info("Vectors upserted successfully to Qdrant")
            return True
        except Exception as e:
            self.logger.error("Failed to upsert vectors to Qdrant", extra={"error": str(e)})
            raise ValueError(f"Failed to upsert vectors: {str(e)}")

    async def search_vectors(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the Qdrant collection.

        Args:
            query_vector: The vector to search for
            limit: Maximum number of results to return

        Returns:
            List of dictionaries containing payload and score for each match
        """
        self.logger.info("Searching vectors in Qdrant", extra={"collection_name": self.collection_name, "limit": limit})

        try:
            # Perform search operation using query_points (replaces deprecated search method)
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit
            )

            # Format results - query_points returns QueryResponse with points attribute
            formatted_results = []
            for result in results.points:  # Access the points from the QueryResponse object
                formatted_results.append({
                    "payload": result.payload,
                    "score": result.score
                })

            self.logger.info("Vector search completed successfully", extra={"result_count": len(formatted_results)})
            return formatted_results
        except Exception as e:
            self.logger.error("Failed to search vectors in Qdrant", extra={"error": str(e)})
            raise ValueError(f"Failed to search vectors: {str(e)}")