# Physical AI Textbook Backend

This is the backend service for the Physical AI & Humanoid Robotics AI-Native Textbook Platform. It provides the core RAG (Retrieval-Augmented Generation) functionality for the textbook, including document ingestion, embedding generation using Cohere, vector storage in Qdrant, and metadata storage in Neon Serverless Postgres.

## Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and configure the .env file**:
   ```bash
   cp .env.example .env
   ```

   Then edit `.env` to add your actual API keys and database URLs:
   ```
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_HOST=your_qdrant_host_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   NEON_DB_URL=your_neon_db_url_here
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

1. **Start the FastAPI server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Verify the API is running**:
   Visit `http://localhost:8000/health` to check the health endpoint.

## Content Ingestion

1. **Run the ingestion script**:
   ```bash
   cd scripts
   python ingest_docs.py
   ```

2. **Source documents**:
   The script processes MDX files from `docs/chapters/` directory.

3. **Verify ingestion**:
   ```bash
   python verify_ingestion.py
   ```

## Configuration

The backend requires the following environment variables:

- `COHERE_API_KEY`: Your Cohere API key for embedding generation
- `QDRANT_HOST`: Host URL for your Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant authentication
- `NEON_DB_URL`: Connection string for your Neon Serverless Postgres database

Refer to `.env.example` for the complete list of required variables.

## Project Structure

```
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── health.py
│   │   └── rag.py
│   ├── services/
│   │   ├── embedding_service.py
│   │   ├── qdrant_service.py
│   │   └── neon_service.py
│   └── core/
│       └── config.py
├── scripts/
│   ├── ingest_docs.py
│   ├── verify_ingestion.py
│   └── README.md
├── requirements.txt
├── .env.example
└── README.md
```

## Next Steps

This completes Phase 1 of the implementation, focusing on the content ingestion pipeline. Phase 2 will implement the RAG Query API endpoints to enable question answering functionality based on the ingested textbook content.