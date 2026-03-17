"""
Pydantic schemas for all API request/response models.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ── Chat (RAG) ──────────────────────────────────────────

class ChatRequest(BaseModel):
    """Free-text question sent to the RAG pipeline."""
    question: str = Field(..., min_length=1, max_length=2000,
                          description="User's free-text question")
    language: str = Field(default="en", pattern="^(en|es)$")
    session_id: Optional[str] = Field(default=None,
                                       description="Session ID for telemetry")


class SourceCitation(BaseModel):
    """A source document used to generate the answer."""
    file: str = Field(..., description="Knowledge file name")
    chunk_id: str = Field(..., description="Chunk identifier")
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")


class ChatResponse(BaseModel):
    """RAG-generated answer with citations."""
    answer: str
    sources: list[SourceCitation] = []
    language: str = "en"
    fallback: bool = Field(default=False,
                           description="True if answer was a guardrail fallback")


# ── Feedback ────────────────────────────────────────────

class FeedbackRequest(BaseModel):
    """User feedback on a bot response."""
    session_id: str
    message_index: int = Field(..., ge=0)
    vote: str = Field(..., pattern="^(up|down)$")


class FeedbackResponse(BaseModel):
    """Confirmation of feedback submission."""
    status: str = "ok"


# ── Health ──────────────────────────────────────────────

class HealthResponse(BaseModel):
    """API health check response."""
    status: str = "healthy"
    rag_ready: bool = False
    chunks_loaded: int = 0
    model_name: str = ""
