# Physical AI Textbook RAG Backend

## Running the Application

To run the FastAPI application:

1. **Start the development server:**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Middleware Functionality

The backend now includes three key middleware components:

### 1. Global Error Handling Middleware
- Catches unhandled exceptions and returns consistent JSON error responses
- Logs errors with full traceback information
- Returns HTTP 500 for internal server errors

### 2. Structured Logging
- All application logs are formatted as structured JSON
- Logs include timestamp, level, logger name, message, and contextual information
- Console output is formatted for easy parsing and analysis

### 3. Request/Response Logging Middleware
- Logs incoming requests with method, URL, and client IP
- Logs outgoing responses with status code and processing time
- Provides detailed timing information for performance monitoring

## Testing Middleware Functionality

### Testing Error Handling
1. Make a request to a non-existent endpoint to trigger a 404 error
2. Make a request that causes an internal server error (e.g., by triggering an exception in code)

### Testing Request/Response Logging
1. Start the server with `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
2. Make any API request (e.g., `curl http://localhost:8000/health/`)
3. Observe the structured JSON logs in the console output

Example log entry:
```json
{
  "timestamp": "2023-01-01T12:00:00.123456Z",
  "level": "INFO",
  "logger": "request_logger",
  "message": "Incoming request",
  "module": "request_logger",
  "function": "dispatch",
  "line": 15,
  "method": "GET",
  "url": "http://localhost:8000/health/",
  "client_host": "127.0.0.1",
  "headers": {
    "host": "localhost:8000",
    "user-agent": "curl/7.68.0",
    "accept": "*/*"
  }
}
```

## OpenAPI/Swagger Documentation Improvements

The following enhancements have been made to the OpenAPI/Swagger documentation:

### Application Metadata
- **Title**: "Physical AI Textbook RAG Backend"
- **Description**: "A FastAPI backend for the Physical AI & Humanoid Robotics AI-Native Textbook Platform, featuring RAG-based question answering using Cohere, Qdrant, Neon, and Google Gemini."
- **Version**: "0.1.0"

### Router Documentation
- **Health Router**: Added summary and description for health monitoring endpoints
- **RAG Router**: Added summary and description for RAG query endpoints

### Endpoint Documentation
- **GET /health/**: Added detailed summary and description for health check endpoint
- **POST /rag/ask**: Added detailed summary and description for RAG query endpoint

### Schema Examples
- **QueryRequest**: Added example payload with sample query and filters
- **Source**: Added example payload with sample source information
- **QueryResponse**: Added example payload with sample answer and sources

The improved documentation provides clear context for developers and enables better API discovery through the interactive Swagger UI.