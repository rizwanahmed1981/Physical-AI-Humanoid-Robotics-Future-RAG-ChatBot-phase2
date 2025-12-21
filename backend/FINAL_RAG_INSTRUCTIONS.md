# Final RAG Query API Implementation Guide

## Overview

This document provides complete instructions for running and testing the finalized RAG Query API with Google Gemini LLM integration.

## System Architecture

The RAG system consists of:
1. **FastAPI Backend** - Handles API requests and routing
2. **Cohere Embedding Service** - Converts queries to embeddings
3. **Qdrant Vector Database** - Stores and searches vector embeddings
4. **Neon PostgreSQL Database** - Stores textbook metadata
5. **Google Gemini LLM** - Generates contextual answers

## Setup Instructions

### 1. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
# Cohere API Configuration
COHERE_API_KEY=your_cohere_api_key_here

# Qdrant Cloud Configuration
QDRANT_HOST=your_qdrant_cloud_host_here
QDRANT_API_KEY=your_qdrant_cloud_api_key_here

# Neon Serverless Postgres Database
NEON_DB_URL=postgresql://user:password@host:port/database_name

# Google API Configuration
GOOGLE_API_KEY=your_google_api_key_here
```

### 2. Install Dependencies

All dependencies are already included in `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Running the Server

Start the FastAPI server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing the API

### Test Endpoint

The RAG endpoint is available at:
```
POST /rag/ask
```

### Sample Request

```bash
curl -X POST http://localhost:8000/rag/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Physical AI?", "chapter_filter": null, "selected_text": null}'
```

### Expected Response

```json
{
  "answer": "Physical AI is an emerging field that combines artificial intelligence with physical systems...",
  "sources": [
    {
      "chapter_id": "chapter_1",
      "title": "Introduction to Physical AI",
      "file_path": "/docs/chapter1.md",
      "chunk_text_preview": "Physical AI is an emerging field that combines artificial intelligence with physical systems...",
      "score": 0.95
    }
  ]
}
```

## Key Features

- **Dependency Injection**: Services are properly injected for clean architecture
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **Contextual Grounding**: Answers are generated only from retrieved textbook content
- **Source Attribution**: All answers include relevant source information
- **Modular Design**: Clean separation of concerns across services

## Implementation Details

### API Routes
- `/rag/ask` (POST): Main RAG query endpoint

### Services Used
- `CohereEmbeddingService`: For query embedding generation
- `QdrantService`: For vector similarity search
- `NeonDBService`: For metadata retrieval
- `RAGService`: Orchestrates the complete RAG pipeline

### Error Handling
- HTTP 500 Internal Server Error for RAG service errors
- HTTP 500 Internal Server Error for general exceptions
- Proper logging of errors for debugging

## Troubleshooting

### Missing API Keys
Ensure all API keys are properly configured in `.env` file.

### Service Connection Issues
Verify that:
- Qdrant host and API key are correct
- Neon database URL is accessible
- Cohere API key is valid
- Google API key is valid

### LLM Not Responding
The LLM integration will work once you have valid API keys. The service will return an error message if the API call fails.

## Next Steps

1. Configure your API keys in `.env`
2. Run the server with `uvicorn app.main:app --reload`
3. Test with sample queries using curl or Postman
4. Integrate with your frontend application

## Production Considerations

- Monitor API response times
- Implement rate limiting for production use
- Add proper logging for production monitoring
- Consider caching for frequently asked questions
- Implement health checks for service monitoring

## License

This implementation is provided for demonstration purposes and follows the project's licensing terms.