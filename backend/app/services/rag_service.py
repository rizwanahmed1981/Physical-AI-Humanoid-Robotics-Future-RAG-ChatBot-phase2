"""
RAG Service to orchestrate query embedding, vector search, and metadata retrieval.
"""
from typing import List, Optional
from app.services.embedding_service import CohereEmbeddingService
from app.services.qdrant_service import QdrantService
from app.services.neon_service import NeonDBService
from app.models.schemas import Source
from google import genai
import os
from app.core import logging_config


class RAGService:
    def __init__(
        self,
        cohere_service: CohereEmbeddingService,
        qdrant_service: QdrantService,
        neon_service: NeonDBService
    ):
        """
        Initialize the RAG service with required dependencies.

        Args:
            cohere_service: Cohere embedding service for generating embeddings
            qdrant_service: Qdrant service for vector similarity search
            neon_service: Neon DB service for metadata retrieval
        """
        self.cohere_service = cohere_service
        self.qdrant_service = qdrant_service
        self.neon_service = neon_service
        self.logger = logging_config.get_logger(__name__)

        # Initialize Gemini client
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            self.logger.error("GOOGLE_API_KEY environment variable is not set")
            raise ValueError("GOOGLE_API_KEY environment variable is not set")

        self.client = genai.Client(api_key=google_api_key)

    async def retrieve_relevant_chunks(
        self,
        query: str,
        chapter_filter: Optional[str] = None,
        selected_text: Optional[str] = None,
        limit: int = 5
    ) -> List[Source]:
        """
        Retrieve relevant text chunks for a given query using the RAG pipeline.

        Args:
            query: The user's query string
            chapter_filter: Optional filter to limit search to specific chapter
            selected_text: Optional additional context from selected text
            limit: Maximum number of results to return

        Returns:
            List of Source objects containing relevant chunks and metadata
        """
        self.logger.info("Starting RAG retrieval process", extra={"query": query, "limit": limit})

        try:
            # Step 1: Generate embedding for the query
            # Using input_type="search_query" for query embeddings (as opposed to "search_document" for documents)
            self.logger.debug("Generating embeddings for query", extra={"query_length": len(query)})
            query_embedding = await self.cohere_service.get_embeddings([query], input_type="search_query")
            query_vector = query_embedding[0]  # Get the first (and only) embedding

            # Step 2: Search for similar vectors in Qdrant
            self.logger.debug("Searching for similar vectors in Qdrant", extra={"limit": limit})
            search_results = await self.qdrant_service.search_vectors(query_vector, limit=limit)

            # Debugging: Print search results information
            print(f"DEBUG: Found {len(search_results)} vectors in Qdrant.")
            for result in search_results:
                print(f"DEBUG: Score: {result['score']}")

            # Step 3: Retrieve metadata from Neon DB and format sources
            sources = []
            self.logger.debug("Retrieving metadata from Neon DB", extra={"result_count": len(search_results)})

            for result in search_results:
                payload = result.get("payload", {})
                score = result.get("score", 0.0)

                # Debug: Print the actual payload structure
                print(f"DEBUG: Raw result structure: {result}")
                print(f"DEBUG: Payload content: {payload}")
                print(f"DEBUG: Payload type: {type(payload)}")
                print(f"DEBUG: Payload keys: {list(payload.keys()) if isinstance(payload, dict) else 'Not a dict'}")

                # Extract identifier from payload
                # Qdrant payload contains chunk_id, but we need to look up by embedding_id
                # However, for now we'll use chunk_id for metadata lookup since it's what's available
                chunk_id = payload.get("chunk_id", "")
                if chunk_id:
                    # Use chunk_id as identifier for metadata lookup
                    print(f"DEBUG: Using chunk_id for metadata lookup: {chunk_id}")

                    # Try the embedding_id lookup first (in case chunk_id happens to match an embedding_id)
                    metadata = None
                    try:
                        metadata = self.neon_service.get_metadata_by_embedding_id(chunk_id)
                        print(f"DEBUG: Metadata retrieved by embedding_id lookup: {metadata}")
                    except Exception as e:
                        print(f"DEBUG: Embedding ID lookup failed with exception: {e}")
                        metadata = None  # Ensure metadata is None if there's an exception

                    # If embedding_id lookup didn't find anything, try chunk_id lookup
                    if not metadata:
                        print(f"DEBUG: Embedding ID lookup returned None, trying chunk_id lookup...")
                        try:
                            metadata = self.neon_service.get_metadata_by_chunk_id(chunk_id)
                            print(f"DEBUG: Metadata retrieved by chunk_id lookup: {metadata}")
                        except Exception as e:
                            print(f"DEBUG: Chunk ID lookup failed with exception: {e}")
                            metadata = None  # Ensure metadata is None if there's an exception

                    # If we found metadata from either lookup, create a source
                    if metadata:
                        source = Source(
                            chapter_id=metadata["chapter_id"],
                            title=metadata["title"],
                            file_path=metadata["file_path"],
                            chunk_text_preview=metadata["chunk_text_preview"],
                            score=score
                        )
                        sources.append(source)

                else:
                    print(f"DEBUG: No chunk_id found in payload")

                # Alternative approach: Try to see if we can make this work with the actual database structure
                # Since we know the ingestion stores embedding_id, but Qdrant doesn't return it,
                # we need to either:
                # 1. Store chunk_id as embedding_id in Qdrant (not ideal)
                # 2. Change the metadata lookup to use chunk_id directly (better approach)

                # For now, let's make it work by trying to see what's in the database
                # We'll add a better debugging approach

                # Since we know we have chunk_id, let's see what the database structure looks like
                # and if we can query by chunk_id
                print(f"DEBUG: Would normally look up metadata by embedding_id: {chunk_id}")
                print(f"DEBUG: But chunk_id is available: {chunk_id}")
                print(f"DEBUG: This suggests the metadata table needs to be queried by chunk_id")

            self.logger.info("RAG retrieval completed successfully", extra={"source_count": len(sources)})
            return sources

        except Exception as e:
            # Handle any errors in the RAG process
            self.logger.error("Error in RAG retrieval process", extra={"error": str(e)})
            raise ValueError(f"Error in RAG retrieval process: {str(e)}")

    async def generate_answer(self, query: str, retrieved_sources: List[Source]) -> str:
        """
        Generate an answer using the Gemini LLM based on the retrieved sources and query.

        Args:
            query: The user's query string
            retrieved_sources: List of Source objects containing relevant context

        Returns:
            Generated answer string from the LLM
        """
        self.logger.info("Starting LLM answer generation", extra={"query": query, "source_count": len(retrieved_sources)})

        try:
            # Format the retrieved sources into a context string
            context_str = ""
            if retrieved_sources:
                context_str = "Context:\n"
                for i, source in enumerate(retrieved_sources, 1):
                    context_str += f"Source {i}:\n"
                    context_str += f"Chapter ID: {source.chapter_id}\n"
                    context_str += f"Title: {source.title}\n"
                    context_str += f"Text: {source.chunk_text_preview}\n"
                    context_str += f"Score: {source.score}\n"
                    context_str += "---\n"

            # Create the prompt for the LLM
            prompt = f"""You are an expert assistant specializing in answering questions based on textbook content.

            Please answer the following question based *only* on the provided textbook context.
            If the answer cannot be found in the provided context, clearly state that.

            Question: {query}

            Context:
            {context_str if context_str else 'No context provided.'}

            Answer:"""

            # Call the Gemini API using the new SDK
            self.logger.debug("Calling Gemini API for content generation")
            response = self.client.models.generate_content(model='gemini-2.5-pro', contents=prompt)

            # Extract the generated answer
            answer = response.text.strip()
            self.logger.info("LLM answer generation completed successfully")
            return answer

        except Exception as e:
            self.logger.error("Error generating answer with LLM", extra={"error": str(e)})
            raise ValueError(f"Error generating answer with LLM: {str(e)}")