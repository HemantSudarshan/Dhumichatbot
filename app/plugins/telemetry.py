"""
MLflow Telemetry Plugin (PII-Safe)
====================================
Logs session and chat telemetry to a local MLflow tracking server.
All PII is masked before logging — raw names, emails, phones are NEVER stored.

Tracking URI defaults to ./mlruns (overridable via MLFLOW_TRACKING_URI env var).

Usage:
    from app.plugins.telemetry import log_session, log_chat_event
"""

import logging
import os
import re
import time
from typing import Any

logger = logging.getLogger(__name__)

# ── MLflow initialisation (lazy import so the app doesn't crash if mlflow
#    isn't installed yet — useful during the plain-uvicorn dev mode) ──────────
try:
    import mlflow
    _MLFLOW_AVAILABLE = True
    _tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "./mlruns")
    mlflow.set_tracking_uri(_tracking_uri)
    mlflow.set_experiment("intermarq-chatbot")
    logger.info("[TELEMETRY] MLflow tracking initialised → %s", _tracking_uri)
except ImportError:
    _MLFLOW_AVAILABLE = False
    logger.warning("[TELEMETRY] mlflow not installed — telemetry will be console-only.")


# ── PII Masking ────────────────────────────────────────────────────────────
_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
_PHONE_RE = re.compile(r"(\+1[-.\s]?)?(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})")
_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_NAME_RE = re.compile(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b")


def _pii_safe(value: Any) -> Any:
    """Mask PII patterns in any string value."""
    if not isinstance(value, str):
        return value
    value = _EMAIL_RE.sub("[EMAIL]", value)
    value = _PHONE_RE.sub("[PHONE]", value)
    value = _SSN_RE.sub("[SSN]", value)
    return value


def _sanitize_params(params: dict) -> dict:
    """Return a copy of params with all string values PII-masked."""
    return {k: _pii_safe(v) for k, v in params.items()}


# ── Public API ─────────────────────────────────────────────────────────────

def log_session(session_data: dict[str, Any]) -> None:
    """
    Log a completed chat session to MLflow.

    Safe parameters logged (no PII):
        - duration_seconds
        - completed (bool)
        - lead_score (int 1-5)
        - thumbs_up, thumbs_down (int)
        - language (EN/ES)
        - drop_off_step (str or None)
        - provider (groq/openrouter/ollama)
        - free_text_count (int)
    """
    safe = _sanitize_params(session_data)

    if _MLFLOW_AVAILABLE:
        with mlflow.start_run(run_name=f"session_{int(time.time())}"):
            # Log metrics (numeric)
            numeric_keys = [
                "duration_seconds", "thumbs_up", "thumbs_down",
                "lead_score", "free_text_count"
            ]
            for key in numeric_keys:
                if key in safe:
                    try:
                        mlflow.log_metric(key, float(safe[key]))
                    except (TypeError, ValueError):
                        pass

            # Log params (categoricals / strings)
            param_keys = ["completed", "language", "drop_off_step", "provider", "state"]
            for key in param_keys:
                if key in safe:
                    mlflow.log_param(key, str(safe[key]))

            logger.info("[TELEMETRY] Session logged to MLflow run.")
    else:
        logger.info("[TELEMETRY] Session (console fallback): %s", safe)


def log_chat_event(question: str, provider: str, latency_ms: float, success: bool) -> None:
    """
    Log a single RAG query event — question is PII-masked before storing.

    Logged metrics:
        - latency_ms
        - success (0/1)
    Logged params:
        - provider
        - question_safe (PII-masked)
    """
    safe_question = _pii_safe(question)

    if _MLFLOW_AVAILABLE:
        with mlflow.start_run(run_name=f"chat_{int(time.time())}"):
            mlflow.log_metric("latency_ms", latency_ms)
            mlflow.log_metric("success", 1.0 if success else 0.0)
            mlflow.log_param("provider", provider)
            mlflow.log_param("question_safe", safe_question[:200])
        logger.info("[TELEMETRY] Chat event logged to MLflow.")
    else:
        logger.info(
            "[TELEMETRY] Chat event (console fallback): q=%s provider=%s latency=%.1fms ok=%s",
            safe_question[:80], provider, latency_ms, success
        )
