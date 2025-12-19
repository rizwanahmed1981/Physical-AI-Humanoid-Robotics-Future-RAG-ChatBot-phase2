import cohere
import os
from typing import List

class CohereEmbeddingService:
    def __init__(self):
        """Initialize the Cohere embedding service with API key from environment."""
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set")

        self.client = cohere.Client(api_key)

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of text documents using Cohere API.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embeddings (list of lists of floats)

        Raises:
            ValueError: If embedding generation fails
        """
        try:
            # Use the embed endpoint with appropriate parameters
            response = self.client.embed(
                texts=texts,
                model="embed-english-v3.0",
                input_type="search_document"  # For document embeddings
            )

            # Extract embeddings from the response
            embeddings = response.embeddings

            # Cohere API returns embeddings as lists of floats directly
            # No need to call .tolist() as they are already Python lists
            return embeddings

        except Exception as e:
            # Handle any Cohere API errors or other exceptions
            # Catching the specific exception might not work in all environments
            if "CohereAPIError" in str(type(e)) or "cohere" in str(e).lower():
                raise ValueError(f"Cohere API error: {str(e)}")
            else:
                raise ValueError(f"Error generating embeddings: {str(e)}")