from pydantic import BaseModel
from typing import Optional, List

class QueryRequest(BaseModel):
    """Model for RAG query request."""
    query: str
    chapter_filter: Optional[str] = None
    selected_text: Optional[str] = None

class Source(BaseModel):
    """Model for source information."""
    chapter_id: str
    title: str
    file_path: str
    chunk_text_preview: str
    score: Optional[float] = None

class QueryResponse(BaseModel):
    """Model for RAG query response."""
    answer: str
    sources: List[Source]