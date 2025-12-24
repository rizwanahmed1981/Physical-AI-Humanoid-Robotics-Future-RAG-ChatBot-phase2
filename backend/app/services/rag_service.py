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
            query_embedding = await self.cohere_service.get_embeddings([query])
            query_vector = query_embedding[0]  # Get the first (and only) embedding

            # Step 2: Search for similar vectors in Qdrant
            self.logger.debug("Searching for similar vectors in Qdrant", extra={"limit": limit})
            search_results = await self.qdrant_service.search_vectors(query_vector, limit=limit)

            # Step 3: Retrieve metadata from Neon DB and format sources
            sources = []
            self.logger.debug("Retrieving metadata from Neon DB", extra={"result_count": len(search_results)})

            for result in search_results:
                payload = result["payload"]
                score = result["score"]

                # Extract embedding_id from payload to get detailed metadata
                embedding_id = payload.get("embedding_id", "")
                if embedding_id:
                    metadata = self.neon_service.get_metadata_by_embedding_id(embedding_id)
                    if metadata:
                        source = Source(
                            chapter_id=metadata["chapter_id"],
                            title=metadata["title"],
                            file_path=metadata["file_path"],
                            chunk_text_preview=metadata["chunk_text_preview"],
                            score=score
                        )
                        sources.append(source)

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
            response = self.client.models.generate_content(model='gemini-1.5-flash', contents=prompt)

            # Extract the generated answer
            answer = response.text.strip()
            self.logger.info("LLM answer generation completed successfully")
            return answer

        except Exception as e:
            self.logger.error("Error generating answer with LLM", extra={"error": str(e)})
            raise ValueError(f"Error generating answer with LLM: {str(e)}")