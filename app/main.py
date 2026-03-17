"""
Intermarq Agency — FastAPI Backend

Endpoints:
  POST /api/v1/chat     → RAG-powered free-text Q&A
  POST /api/v1/lead     → Lead capture + ACORD formatting + OPA compliance
  POST /api/v1/feedback  → User thumbs up/down
  GET  /api/v1/health    → Health check

Run:
  uvicorn app.main:app --reload --port 8000
"""

import os
import json
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel

from app.models.schemas import (
    ChatRequest, ChatResponse,
    FeedbackRequest, FeedbackResponse,
    HealthResponse,
)
from app.rag.retriever import init_retriever, get_chunk_count
from app.rag.generator import generate_answer

# ── Plugin imports ──────────────────────────────────────────
from app.plugins.acord import format_to_txlife_103
from app.plugins.opa import check_compliance
from app.plugins.telemetry import log_session

logger = logging.getLogger(__name__)

# Load .env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# ── In-memory feedback store (no PII) ──────────────────────
_feedback_log: list[dict] = []


# ── Lead request / response schemas ────────────────────────
class LeadRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    zip_code: str
    coverage_amount: str = "250000"
    age_range: str = "Unknown"
    tobacco_use: str = "No"
    state: str = "CA"
    lead_score: int = 3
    pricing_range: str = ""
    session_id: str = ""


class LeadResponse(BaseModel):
    status: str
    transaction_id: str
    compliance: dict
    acord_summary: dict


# ── Lifespan: load model once at startup ───────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load embedding model and ChromaDB at startup."""
    print("🚀 Starting Intermarq RAG backend...")
    try:
        chunk_count = init_retriever()
        print(f"✅ Retriever loaded: {chunk_count} chunks")
    except Exception as e:
        print(f"⚠️  Retriever init failed: {e}")
        print("   Run 'python -m app.rag.embed_knowledge' first to build the index.")
    yield
    # Cleanup
    print("👋 Shutting down...")
    if _feedback_log:
        feedback_path = os.path.join(os.path.dirname(__file__), "feedback_log.json")
        with open(feedback_path, "w", encoding="utf-8") as f:
            json.dump(_feedback_log, f, indent=2)
        print(f"📊 Saved {len(_feedback_log)} feedback entries to {feedback_path}")


# ── App ────────────────────────────────────────────────────
app = FastAPI(
    title="Intermarq Insurance Assistant API",
    version="2.0.0",
    description="RAG-powered chatbot — Plugin Edition (Docker + LiteLLM + MLflow + ACORD + OPA)",
    lifespan=lifespan,
)

# CORS
cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:8080").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins + ["https://*.railway.app"],
    allow_origin_regex=r"https://.*\.railway\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Endpoints ──────────────────────────────────────────────

@app.get("/api/v1/health", response_model=HealthResponse)
async def health():
    """Health check — returns RAG readiness status."""
    chunks = get_chunk_count()
    return HealthResponse(
        status="healthy",
        rag_ready=chunks > 0,
        chunks_loaded=chunks,
        model_name=os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
    )


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    RAG-powered chat endpoint.
    Routes through LiteLLM gateway (Groq → OpenRouter → Ollama fallback).
    """
    start = time.time()
    try:
        response = generate_answer(
            question=request.question,
            language=request.language,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

    latency = round((time.time() - start) * 1000)
    logger.info(
        "[CHAT] latency=%dms fallback=%s sources=%d lang=%s",
        latency, response.fallback, len(response.sources), response.language
    )
    return response


@app.post("/api/v1/lead", response_model=LeadResponse)
async def submit_lead(request: LeadRequest):
    """
    Lead capture endpoint — full plugin pipeline:
      1. OPA compliance check (stub → always passes for MVP)
      2. ACORD TXLife 103 payload formatting
      3. MLflow session telemetry (PII-masked)

    In production: push ACORD payload to CRM after step 2.
    """
    lead_data = request.model_dump()

    # ── Step 1: OPA Compliance ─────────────────────────────
    age_range_str = str(lead_data.get("age_range", "40"))
    try:
        age_int = int(age_range_str.split("-")[0])
    except (ValueError, IndexError):
        age_int = 40

    coverage_str = str(lead_data.get("coverage_amount", "250000")).replace(",", "")
    try:
        coverage_int = int(coverage_str)
    except ValueError:
        coverage_int = 250000

    tobacco_val = lead_data.get("tobacco_use", "No")
    is_tobacco = isinstance(tobacco_val, str) and tobacco_val.lower() in ("yes", "sí", "occasionally")

    compliance = check_compliance(
        state=str(lead_data.get("state", "CA")),
        age=age_int,
        coverage_amount=coverage_int,
        tobacco_user=is_tobacco,
    )

    if not compliance.compliant:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Compliance check failed",
                "violations": compliance.violations,
                "policy_version": compliance.policy_version,
            },
        )

    # ── Step 2: ACORD TXLife 103 Format ───────────────────
    lead_data["compliance"] = compliance.policy_version
    acord_payload = format_to_txlife_103(lead_data)
    tx_id = acord_payload["TXLife"]["TXLifeRequest"]["TransRefGUID"]

    # ── Step 3: MLflow Telemetry (PII-safe) ───────────────
    log_session({
        "duration_seconds": 0,
        "completed": True,
        "lead_score": lead_data.get("lead_score", 3),
        "thumbs_up": 0,
        "thumbs_down": 0,
        "language": "en",
        "state": lead_data.get("state", "CA"),
        "provider": "lead-form",
        "free_text_count": 0,
    })

    logger.info("[LEAD] tx_id=%s compliance=%s", tx_id, compliance.policy_version)

    return LeadResponse(
        status="accepted",
        transaction_id=tx_id,
        compliance=compliance.to_dict(),
        acord_summary={
            "tx_type": "103 - New Business Quote",
            "product": "MORT-PROTECT-TERM",
            "coverage": lead_data.get("coverage_amount"),
            "state": lead_data.get("state"),
            "source": "Intermarq-AI-Chatbot",
        },
    )


@app.post("/api/v1/feedback", response_model=FeedbackResponse)
async def feedback(request: FeedbackRequest):
    """Record user feedback (thumbs up/down). No PII stored."""
    _feedback_log.append({
        "session_id": request.session_id,
        "message_index": request.message_index,
        "vote": request.vote,
        "timestamp": time.time(),
    })
    logger.info(
        "[FEEDBACK] session=%s... msg=%d vote=%s",
        request.session_id[:8], request.message_index, request.vote
    )
    return FeedbackResponse(status="ok")


# ── Static file serving (production single-container mode) ──
import pathlib
from fastapi.staticfiles import StaticFiles

_base = pathlib.Path(__file__).resolve().parent.parent
_demo_dir = _base / "demo"
_knowledge_dir = _base / "knowledge"

if _demo_dir.is_dir():
    app.mount("/demo", StaticFiles(directory=str(_demo_dir), html=True), name="demo")
if _knowledge_dir.is_dir():
    app.mount("/knowledge", StaticFiles(directory=str(_knowledge_dir)), name="knowledge")
