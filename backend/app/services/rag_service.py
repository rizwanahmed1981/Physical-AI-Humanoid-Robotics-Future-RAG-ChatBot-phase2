"""
RAG Service to orchestrate query embedding, vector search, and metadata retrieval.
"""
from typing import List, Optional
from app.services.embedding_service import CohereEmbeddingService
from app.services.qdrant_service import QdrantService
from app.services.neon_service import NeonDBService
from app.models.schemas import Source
import google.generativeai as genai
import os


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

        # Initialize Gemini client
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")

        genai.configure(api_key=google_api_key)
        self.llm_model = genai.GenerativeModel('gemini-pro')

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
        try:
            # Step 1: Generate embedding for the query
            # Using input_type="search_query" for query embeddings (as opposed to "search_document" for documents)
            query_embedding = await self.cohere_service.get_embeddings([query])
            query_vector = query_embedding[0]  # Get the first (and only) embedding

            # Step 2: Search for similar vectors in Qdrant
            search_results = await self.qdrant_service.search_vectors(query_vector, limit=limit)

            # Step 3: Retrieve metadata from Neon DB and format sources
            sources = []
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

            return sources

        except Exception as e:
            # Handle any errors in the RAG process
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

            # Call the Gemini API
            response = self.llm_model.generate_content(prompt)

            # Extract the generated answer
            answer = response.text.strip()
            return answer

        except Exception as e:
            raise ValueError(f"Error generating answer with LLM: {str(e)}")