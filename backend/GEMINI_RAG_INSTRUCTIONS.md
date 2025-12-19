# Enhanced RAG Query API with Google Gemini LLM Integration

## Overview

This document explains how to set up and use the enhanced RAG (Retrieval-Augmented Generation) Query API that now includes Google Gemini LLM integration.

## What's New

The RAG service has been enhanced with:
1. **LLM Integration**: Uses Google Gemini Pro to generate contextual answers
2. **Context-Aware Responses**: Answers are grounded in textbook content
3. **Proper Grounding**: LLM is instructed to only use provided context
4. **Improved Error Handling**: Better error management throughout the pipeline

## Setup Instructions

### 1. Configure Environment Variables

First, copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Then edit `.env` and add your API keys:

```env
# Google API Configuration
GOOGLE_API_KEY=your_actual_google_api_key_here
```

### 2. Install Dependencies

The google-generativeai package should already be in requirements.txt. If not, run:

```bash
pip install google-generativeai
```

### 3. Start the Server

```bash
uvicorn app.main:app --reload
```

## Usage

### API Endpoint

The RAG endpoint is available at:
```
POST /rag/ask
```

### Request Format

```json
{
  "query": "What is Physical AI?",
  "chapter_filter": null,
  "selected_text": null
}
```

### Response Format

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

## How It Works

1. **Query Processing**: The user query is converted to an embedding using Cohere
2. **Vector Search**: Similar vectors are found in Qdrant using cosine similarity
3. **Metadata Retrieval**: Relevant textbook metadata is fetched from Neon DB
4. **LLM Generation**: The retrieved context is sent to Google Gemini Pro with a prompt that enforces grounding
5. **Response**: Gemini generates a concise, contextual answer

## Key Features

- **Grounded Answers**: Gemini is instructed to only use provided context
- **Source Attribution**: Sources are returned with each answer
- **Error Handling**: Graceful handling of missing context or API errors
- **Modular Design**: Clean separation of concerns

## Testing

You can test the API with curl:

```bash
curl -X POST http://localhost:8000/rag/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is physical AI?"}'
```

## Troubleshooting

### Missing API Keys
If you get an error about missing API keys, make sure your `.env` file contains:
- `COHERE_API_KEY`
- `QDRANT_HOST` and `QDRANT_API_KEY`
- `NEON_DB_URL`
- `GOOGLE_API_KEY`

### LLM Not Responding
The LLM integration will work once you have valid API keys. The service will return an error message if the API call fails.

## Implementation Details

The enhancement includes:
- **Enhanced RAGService**: Added `generate_answer` method using Gemini
- **Gemini Client**: Initialized with API key validation
- **Prompt Engineering**: Carefully crafted prompt for grounding
- **Model Selection**: Uses `gemini-pro` model
- **Error Handling**: Comprehensive error handling for all components

## Next Steps

1. Configure your Google API key in `.env`
2. Run the server with `uvicorn app.main:app --reload`
3. Test the `/rag/ask` endpoint with sample queries
4. Integrate with your frontend application