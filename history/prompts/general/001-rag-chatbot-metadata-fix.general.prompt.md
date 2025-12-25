---
ID: 001
TITLE: RAG Chatbot Metadata Lookup Fix
STAGE: green
DATE_ISO: 2025-12-25
SURFACE: agent
MODEL: unspecified
FEATURE: none
BRANCH: main
USER: ecomw
COMMAND: /sp.phr
LABELS: ["rag", "metadata", "lookup", "fix", "qdrant", "neon", "chatbot"]
LINKS_SPEC: null
LINKS_TICKET: null
LINKS_ADR: null
LINKS_PR: null
---

# RAG Chatbot Metadata Lookup Fix

## Prompt Text
--title "RAG Chatbot Metadata Lookup Fix" --stage "green"

## Response Summary
Successfully fixed the RAG chatbot metadata lookup issue that was causing `source_count: 0` despite successful vector searches in Qdrant. The problem was that the ingestion process stored both `chunk_id` and `embedding_id` but the RAG service was incorrectly trying to look up metadata using `embedding_id` when only `chunk_id` was available from Qdrant.

## Outcome & Impact
The fix enables the RAG system to properly retrieve metadata and return relevant sources for question answering. Previously, `source_count: 0` was returned even though Qdrant correctly found 3 relevant vectors with good similarity scores (0.698, 0.681, 0.650). Now the system correctly finds 3 sources with proper metadata.

## Tests Summary
- Verified chunk_id based lookup works in neon_service.py
- Tested that rag_service.py now properly handles fallback from embedding_id to chunk_id lookup
- Confirmed successful metadata retrieval from database with proper chunk_id values

## Files Summary
- Modified `backend/app/services/rag_service.py` to implement proper fallback logic
- Verified `backend/app/services/neon_service.py` already contained `get_metadata_by_chunk_id` method

## Next Prompts
- Test full end-to-end RAG pipeline with actual question answering
- Verify the fix works with different query types
- Monitor for any edge cases in metadata retrieval

## Reflection Note
The issue was a classic data flow mismatch where the system architecture assumed embedding_id availability but Qdrant only stored chunk_id. The solution required updating the lookup logic to gracefully fall back from embedding_id to chunk_id when the former wasn't found.