# Phase 2: Core RAG Query API - Tasks

## Setup Tasks

- [ ] T001 Create API directory structure for RAG endpoints
- [ ] T002 Install additional dependencies for RAG functionality (if needed)

## Foundational Tasks

- [ ] T003 Define API schemas for RAG requests and responses
- [ ] T004 Set up OpenAPI documentation for RAG endpoints
- [ ] T005 Create basic RAG endpoint structure in backend/app/api/rag.py

## User Story 1: RAG Query API Endpoint (Priority: P1)

### Goal
Implement a RESTful API endpoint that accepts user queries and returns RAG-generated answers grounded in textbook content.

### Independent Test
Can be tested by sending a query to the RAG endpoint and verifying it returns a response with proper citations.

### Implementation Tasks

- [ ] T010 [US1] Define RAG query request schema with fields: question (str), context (str, optional)
- [ ] T011 [US1] Define RAG response schema with fields: answer (str), sources (list), confidence_score (float)
- [ ] T012 [US1] Implement POST endpoint at /rag/query in backend/app/api/rag.py
- [ ] T013 [US1] Add input validation for query parameters
- [ ] T014 [US1] Implement basic response structure with placeholder content

## User Story 2: Query Embedding and Vector Search (Priority: P1)

### Goal
Integrate Cohere for query embedding generation and Qdrant for vector similarity search to find relevant textbook passages.

### Independent Test
Can be tested by sending a query and verifying that relevant vectors are found in Qdrant.

### Implementation Tasks

- [ ] T020 [US2] Integrate CohereEmbeddingService for query embedding generation
- [ ] T021 [US2] Implement query vectorization in RAG endpoint
- [ ] T022 [US2] Integrate QdrantService for vector search
- [ ] T023 [US2] Implement vector search with top-k results (e.g., k=5)
- [ ] T024 [US2] Add error handling for embedding and search failures

## User Story 3: Metadata Retrieval and Response Formatting (Priority: P1)

### Goal
Retrieve metadata from Neon DB and format responses with proper citations and sources.

### Independent Test
Can be tested by verifying that metadata is correctly retrieved and included in responses.

### Implementation Tasks

- [ ] T030 [US3] Integrate NeonDBService for metadata retrieval
- [ ] T031 [US3] Implement metadata fetching by embedding IDs
- [ ] T032 [US3] Format response with sources and citations
- [ ] T033 [US3] Add confidence scoring based on similarity scores
- [ ] T034 [US3] Implement response formatting with proper markdown/html

## User Story 4: RAG Process Orchestration (Priority: P1)

### Goal
Orchestrate the complete RAG process: query embedding → vector search → metadata retrieval → response generation.

### Independent Test
Can be tested by running a complete RAG query and verifying all components work together.

### Implementation Tasks

- [ ] T040 [US4] Implement complete RAG orchestration pipeline
- [ ] T041 [US4] Connect all components: embedding → search → metadata → response
- [ ] T042 [US4] Add logging for debugging and monitoring
- [ ] T043 [US4] Implement fallback mechanisms for missing data
- [ ] T044 [US4] Add performance metrics collection

## Testing Tasks

- [ ] T050 Test RAG endpoint with sample queries
- [ ] T051 Verify embedding generation works correctly
- [ ] T052 Verify vector search retrieves relevant results
- [ ] T053 Verify metadata retrieval from Neon DB
- [ ] T054 Test response formatting with sources and citations
- [ ] T055 Document API usage and examples

## Polish & Cross-Cutting Concerns

- [ ] T060 Update README.md with RAG API usage instructions
- [ ] T061 Add comprehensive error handling and logging
- [ ] T062 Validate API documentation is complete and accurate
- [ ] T063 Ensure all services are properly initialized and configured
- [ ] T064 Add performance optimization considerations