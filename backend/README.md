# Physical AI & Humanoid Robotics Textbook API

AI-Native Backend using FastAPI, Google Gemini 2.5 Pro, Qdrant, and Neon Postgres.

## Prerequisites

- Python 3.11+

## Setup Instructions

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**:
   - Copy `.env.example` to `.env`: `cp .env.example .env`
   - Edit `.env` to add your actual API keys and database URLs:
     ```
     GOOGLE_API_KEY=your_google_api_key_here
     COHERE_API_KEY=your_cohere_api_key_here
     QDRANT_HOST=your_qdrant_host_here
     QDRANT_API_KEY=your_qdrant_api_key_here
     NEON_DB_URL=your_neon_db_url_here
     ```

## Data Ingestion

The database starts empty. To populate it with textbook content:

1. Run the ingestion script:
   ```bash
   python scripts/ingest_docs.py
   ```

## Running the Server

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

- `POST /rag/ask`: Main RAG endpoint. Example JSON body: `{"query": "What is Physical AI?"}`
- `GET /health`: System health check (verifies Gemini, Qdrant, Neon)
- `GET /docs`: Swagger UI

## Tech Stack

- **FastAPI**: Web framework for building APIs
- **Google Gemini 2.5 Pro**: Large language model for RAG
- **Qdrant**: Vector database for semantic search
- **Neon Postgres**: Serverless PostgreSQL for metadata storage
- **Cohere**: Embedding generation for text vectors
- **Python 3.11+**: Programming language

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
│   │   ├── neon_service.py
│   │   └── rag_service.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── cors.py
│   │   ├── error_handler.py
│   │   └── request_logger.py
│   └── core/
│       └── logging_config.py
├── scripts/
│   ├── ingest_docs.py
│   └── __init__.py
├── requirements.txt
├── .env.example
└── README.md
```