from pydantic import BaseModel
from typing import Optional, List

class QueryRequest(BaseModel):
    """Model for RAG query request."""
    query: str
    chapter_filter: Optional[str] = None
    selected_text: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the ethical considerations of humanoid robotics?",
                "chapter_filter": "Chapter 5",
                "selected_text": "The development of AI raises complex ethical questions."
            }
        }

class Source(BaseModel):
    """Model for source information."""
    chapter_id: str
    title: str
    file_path: str
    chunk_text_preview: str
    score: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "chapter_id": "chapter-5-ethics",
                "title": "Ethical AI and Robotics",
                "file_path": "docs/chapters/chapter-5.mdx",
                "chunk_text_preview": "Ethical considerations include bias, accountability, and job displacement.",
                "score": 0.87
            }
        }

class QueryResponse(BaseModel):
    """Model for RAG query response."""
    answer: str
    sources: List[Source]

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "According to Chapter 5, the ethical considerations of humanoid robotics include bias in AI systems, accountability for AI actions, and the potential for job displacement.",
                "sources": [
                    {
                        "chapter_id": "chapter-5-ethics",
                        "title": "Ethical AI and Robotics",
                        "file_path": "docs/chapters/chapter-5.mdx",
                        "chunk_text_preview": "Ethical considerations include bias, accountability, and job displacement.",
                        "score": 0.87
                    }
                ]
            }
        }