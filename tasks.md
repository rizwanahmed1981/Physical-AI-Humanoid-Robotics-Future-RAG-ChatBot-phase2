# Phase 1: Core RAG Ingestion - Tasks

## Setup Tasks

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Install and configure dependencies in requirements.txt
- [ ] T003 Configure environment variables in .env.example

## Foundational Tasks

- [ ] T004 Set up FastAPI application structure (main.py)
- [ ] T005 Implement health check endpoint (health.py)
- [ ] T006 Implement Cohere embedding service (embedding_service.py)
- [ ] T007 Implement Qdrant service (qdrant_service.py)
- [ ] T008 Set up Neon Serverless DB connection
- [ ] T009 Implement content ingestion script (ingest_docs.py)

## User Story 1: Content Ingestion Pipeline (Priority: P1)

### Goal
A content administrator needs to ingest new textbook chapters or updates to existing chapters into the RAG system.

### Independent Test
Can be fully tested by running the ingestion script with markdown files and verifying content appears in the vector database.

### Implementation Tasks

- [ ] T010 [US1] Create ingestion script to read MDX files from docs/chapters/
- [ ] T011 [US1] Implement content parsing from MDX files
- [ ] T012 [US1] Integrate Cohere service for text-to-embedding conversion
- [ ] T013 [US1] Store embeddings in Qdrant Cloud via Qdrant service
- [ ] T014 [US1] Store metadata in Neon Serverless Postgres
- [ ] T015 [US1] Implement error handling for ingestion process

## User Story 2: RAG System Foundation (Priority: P1)

### Goal
Establish the core infrastructure for RAG processing with proper service integration.

### Independent Test
Can be tested by running ingestion pipeline with sample content and verifying all services are properly connected.

### Implementation Tasks

- [ ] T016 [US2] Integrate embedding service with ingestion pipeline
- [ ] T017 [US2] Integrate Qdrant service with ingestion pipeline
- [ ] T018 [US2] Integrate Neon DB service with ingestion pipeline
- [ ] T019 [US2] Implement progress tracking for large content ingestion
- [ ] T020 [US2] Implement basic logging and monitoring for ingestion

## Testing Tasks

- [ ] T021 Test ingestion on sample textbook chapters
- [ ] T022 Verify embeddings are stored in Qdrant Cloud
- [ ] T023 Verify metadata is stored in Neon DB
- [ ] T024 Test content retrieval functionality
- [ ] T025 Document any issues or improvements needed

## Polish & Cross-Cutting Concerns

- [ ] T026 Update README.md with setup instructions
- [ ] T027 Validate all environment variables work correctly
- [ ] T028 Ensure all services are properly configured
- [ ] T029 Create troubleshooting guide for ingestion process