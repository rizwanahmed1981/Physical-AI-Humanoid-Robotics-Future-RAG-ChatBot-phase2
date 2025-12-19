import os
import asyncio
import glob
import uuid
from typing import List, Dict, Any

# Import the services
from ..app.services.embedding_service import CohereEmbeddingService
from ..app.services.qdrant_service import QdrantService
from ..app.services.neon_service import NeonDBService

# Constants
DOCS_PATH = "../../docs/chapters/"

async def parse_and_chunk_mdx(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse an MDX file and split it into chunks.

    Args:
        file_path: Path to the MDX file

    Returns:
        List of dictionaries containing chunk text and metadata
    """
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Get the filename without extension for chapter_id
        filename = os.path.basename(file_path)
        chapter_id = os.path.splitext(filename)[0]

        # Simple chunking by double newlines
        chunks = content.split('\n\n')

        # Filter out empty chunks and chunks that are too short
        filtered_chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 50]

        # Create chunk metadata
        result = []
        for i, chunk_text in enumerate(filtered_chunks):
            chunk_id = f"{chapter_id}_chunk_{i}"

            # Create metadata for this chunk
            metadata = {
                "chapter_id": chapter_id,
                "title": chapter_id.replace('_', ' ').title(),
                "chunk_id": chunk_id,
                "file_path": file_path
            }

            result.append({
                "text": chunk_text,
                "metadata": metadata
            })

        return result

    except Exception as e:
        print(f"Error parsing {file_path}: {str(e)}")
        return []

async def ingest_document(file_path: str, cohere_service: CohereEmbeddingService,
                         qdrant_service: QdrantService, neon_service: NeonDBService):
    """
    Ingest a single document by parsing, embedding, and storing in Qdrant and Neon.

    Args:
        file_path: Path to the MDX file to ingest
        cohere_service: Cohere embedding service instance
        qdrant_service: Qdrant service instance
        neon_service: Neon database service instance
    """
    try:
        print(f"Processing document: {file_path}")

        # Parse and chunk the document
        chunks = await parse_and_chunk_mdx(file_path)
        if not chunks:
            print(f"No chunks found in {file_path}")
            return

        # Prepare vectors and payloads
        texts = [chunk["text"] for chunk in chunks]
        embeddings = []

        # Generate embeddings for all texts
        try:
            embeddings = await cohere_service.get_embeddings(texts)
        except Exception as e:
            print(f"Error generating embeddings for {file_path}: {str(e)}")
            return

        # Prepare Qdrant payloads and metadata
        qdrant_payloads = []
        neon_metadata_list = []

        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Generate unique embedding ID
            embedding_id = uuid.uuid4().hex

            # Prepare Qdrant payload
            qdrant_payload = {
                "chapter_id": chunk["metadata"]["chapter_id"],
                "title": chunk["metadata"]["title"],
                "chunk_id": chunk["metadata"]["chunk_id"],
                "file_path": chunk["metadata"]["file_path"],
                "text_preview": chunk["text"][:100] + "..." if len(chunk["text"]) > 100 else chunk["text"]
            }
            qdrant_payloads.append(qdrant_payload)

            # Prepare Neon metadata
            neon_metadata = {
                "chapter_id": chunk["metadata"]["chapter_id"],
                "title": chunk["metadata"]["title"],
                "file_path": chunk["metadata"]["file_path"],
                "chunk_id": chunk["metadata"]["chunk_id"],
                "chunk_text_preview": chunk["text"][:200] + "..." if len(chunk["text"]) > 200 else chunk["text"],
                "embedding_id": embedding_id
            }
            neon_metadata_list.append(neon_metadata)

        # Store embeddings in Qdrant
        try:
            await qdrant_service.upsert_vectors(embeddings, qdrant_payloads)
            print(f"Successfully stored {len(embeddings)} vectors in Qdrant for {file_path}")
        except Exception as e:
            print(f"Error storing vectors in Qdrant for {file_path}: {str(e)}")
            return

        # Store metadata in Neon
        try:
            for metadata in neon_metadata_list:
                neon_service.insert_metadata(
                    chapter_id=metadata["chapter_id"],
                    title=metadata["title"],
                    file_path=metadata["file_path"],
                    chunk_id=metadata["chunk_id"],
                    chunk_text_preview=metadata["chunk_text_preview"],
                    embedding_id=metadata["embedding_id"]
                )
            print(f"Successfully stored metadata for {len(neon_metadata_list)} chunks in Neon for {file_path}")
        except Exception as e:
            print(f"Error storing metadata in Neon for {file_path}: {str(e)}")
            return

        print(f"Completed processing: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")

async def main():
    """Main ingestion function."""
    try:
        print("Starting document ingestion...")

        # Initialize services
        cohere_service = CohereEmbeddingService()
        qdrant_service = QdrantService()
        neon_service = NeonDBService()

        # Create metadata table if it doesn't exist
        try:
            neon_service.create_metadata_table()
            print("Metadata table created successfully")
        except Exception as e:
            print(f"Error creating metadata table: {str(e)}")
            return

        # Find all MDX files
        search_pattern = os.path.join(DOCS_PATH, "*.mdx")
        mdx_files = glob.glob(search_pattern)

        if not mdx_files:
            print("No MDX files found in the docs/chapters directory")
            return

        print(f"Found {len(mdx_files)} MDX files to process")

        # Process each file
        for file_path in mdx_files:
            await ingest_document(file_path, cohere_service, qdrant_service, neon_service)

        print("Document ingestion completed successfully!")

    except Exception as e:
        print(f"Error in main ingestion process: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())