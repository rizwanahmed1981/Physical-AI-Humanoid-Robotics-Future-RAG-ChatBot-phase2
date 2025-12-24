# Tasks for Phase 2: API Integration

## Overview
This phase focuses on connecting the ChatWidget UI to the backend RAG API to enable real functionality.

## Phase 2: API Integration

### Goal
Connect the ChatWidget component to the backend RAG API endpoint to enable real question-answering functionality.

### Independent Test Criteria
Each API integration task should be independently testable through:
- Network request simulation
- Response parsing validation
- Error handling verification
- UI updates confirmation

### Tasks

- [ ] T001 [US1] Remove mock logic and setTimeout simulation from src/components/ChatWidget/index.js
- [ ] T002 [US1] [P] Implement async fetch function to POST to http://localhost:8000/rag/ask in src/components/ChatWidget/index.js
- [ ] T003 [US1] Handle API response parsing and update messages state with answer and sources in src/components/ChatWidget/index.js
- [ ] T004 [US1] Update UI to display citation sources below bot messages in src/components/ChatWidget/index.js
- [ ] T005 [US1] Implement error handling for failed API requests in src/components/ChatWidget/index.js
- [ ] T006 [US1] Create .env.local file for Docusaurus frontend API URL configuration

## Final Phase: Polish & Cross-Cutting Concerns

### Tasks

- [ ] T007 [US1] Add environment variable validation in src/components/ChatWidget/index.js
- [ ] T008 [US1] Implement loading state improvements during API calls in src/components/ChatWidget/index.js
- [ ] T009 [US1] Add user-friendly error messages for different API error types in src/components/ChatWidget/index.js
- [ ] T010 [US1] Document API integration in src/components/ChatWidget/README.md