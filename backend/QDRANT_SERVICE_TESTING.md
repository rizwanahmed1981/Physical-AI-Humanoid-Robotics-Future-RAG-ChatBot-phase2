# Qdrant Service Testing Guide

This document explains how to test the Qdrant service implementation in the backend.

## Test Files

1. `test_qdrant_unit.py` - Unit tests for the Qdrant service (no Qdrant instance required)
2. `test_qdrant_comprehensive.py` - Comprehensive tests requiring a Qdrant instance
3. `test_qdrant_service.py` - Basic tests included in the project

## Running Unit Tests

The unit tests validate the structure and implementation of the Qdrant service without requiring an actual Qdrant instance:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python test_qdrant_unit.py
```

## Running Comprehensive Tests

The comprehensive tests require a running Qdrant instance:

### Option 1: Local Qdrant with Docker

```bash
# Start Qdrant container
docker-compose -f docker-compose.qdrant.yml up -d

# Run comprehensive tests
source venv/bin/activate
python test_qdrant_comprehensive.py
```

### Option 2: Qdrant Cloud

Set up your environment variables:
```bash
export QDRANT_HOST="https://your-cluster-url.cloud.qdrant.io:6333"
export QDRANT_API_KEY="your-api-key"
```

Then run:
```bash
source venv/bin/activate
python test_qdrant_comprehensive.py
```

## Qdrant Service Features Tested

### 1. Initialization
- Environment variable validation
- Proper client initialization for both local and cloud instances
- Protocol handling (URL vs host:port)

### 2. Collection Management
- `create_collection()` method
- Vector size configuration
- Cosine distance setup

### 3. Vector Operations
- `upsert_vectors()` method for inserting/updating vectors
- Payload handling with metadata
- ID management

### 4. Search Operations
- `search_vectors()` method for similarity search
- Query vector processing
- Result formatting

### 5. Error Handling
- Exception wrapping for meaningful error messages
- Graceful failure handling
- Validation of inputs

## Service Implementation Details

The QdrantService class provides:

- **Asynchronous methods** for non-blocking operations
- **Environment-based configuration** for flexibility
- **Proper error handling** with meaningful messages
- **Type hints** for better code documentation
- **Flexible initialization** supporting both local and cloud instances

## Configuration

The service expects these environment variables:
- `QDRANT_HOST`: The host URL or host:port combination
- `QDRANT_API_KEY`: The API key for authentication

For local development:
```bash
QDRANT_HOST=localhost:6333
QDRANT_API_KEY=local-test-key
```

For cloud instances:
```bash
QDRANT_HOST=https://your-cluster.cloud.qdrant.io:6333
QDRANT_API_KEY=your-api-key
```

## Architecture Notes

The Qdrant service is designed to:
- Integrate with the Cohere embedding pipeline
- Store textbook chapter embeddings for RAG operations
- Support scalable vector search operations
- Handle metadata for proper content attribution
- Provide reliable error handling for production use