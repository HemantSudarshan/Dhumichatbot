"""
RAG Generator — LiteLLM Edition
================================
All LLM calls now route through LiteLLM, which provides:
  - Unified API across 100+ providers
  - Automatic fallback (Groq → OpenRouter → Ollama)
  - Rate-limit retry logic
  - Load balancing (used by C-011 concurrent user test)

Environment variables:
  GROQ_API_KEY         — Groq API key
  OPENROUTER_API_KEY   — OpenRouter API key  (set as OPENROUTER_API_KEY)
  OLLAMA_URL           — Ollama base URL     (default: http://localhost:11434)
  GROQ_MODEL           — override Groq model
  OPENROUTER_MODEL     — override OpenRouter model
  OLLAMA_MODEL         — override Ollama model
"""

import os
import logging
import time

from app.guardrails.constitution import (
    SYSTEM_PROMPT, filter_input, filter_output,
    FALLBACK_MESSAGES
)
from app.rag.retriever import retrieve
from app.models.schemas import ChatResponse, SourceCitation
from app.plugins.telemetry import log_chat_event

logger = logging.getLogger(__name__)

# ── LiteLLM import (lazy — falls back to direct requests if not installed) ──
try:
    import litellm
    litellm.drop_params = True          # Ignore unsupported params per provider
    litellm.set_verbose = False
    _LITELLM_AVAILABLE = True
    logger.info("[LLM] LiteLLM gateway loaded ✅")
except ImportError:
    _LITELLM_AVAILABLE = False
    import requests                      # type: ignore
    logger.warning("[LLM] litellm not installed — using direct requests fallback")

MAX_CONTEXT_CHUNKS = 5
REQUEST_TIMEOUT = 30

# ── Pre-RAG Objection Matcher ────────────────────────────────────────────────
# Loads objections.json at startup and matches user input deterministically
# before the vector search can pull wrong chunks (Fix T4-005, T3-006)
import json as _json

_OBJECTIONS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "objections.json"
)
# Try to load from knowledge/ directory as well
if not os.path.exists(_OBJECTIONS_PATH):
    _OBJECTIONS_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "knowledge", "objections.json"
    )

_OBJECTIONS: dict = {}
try:
    with open(_OBJECTIONS_PATH, "r", encoding="utf-8") as _f:
        _OBJECTIONS = _json.load(_f)
    logger.info("[OBJECTIONS] Loaded %d objection handlers", len(_OBJECTIONS))
except FileNotFoundError:
    logger.warning("[OBJECTIONS] objections.json not found at %s", _OBJECTIONS_PATH)


def _match_objection(question: str, language: str = "en") -> ChatResponse | None:
    """
    Deterministic keyword match against objections.json triggers.
    Runs BEFORE vector search to prevent semantic mis-routing.
    Returns a ChatResponse if matched, None otherwise.
    """
    lower = question.lower()
    lang_key = "response_es" if language == "es" else "response_en"
    followup_key = "follow_up_es" if language == "es" else "follow_up_en"

    for obj_key, obj_data in _OBJECTIONS.items():
        triggers = obj_data.get("triggers", [])
        for trigger in triggers:
            if trigger.lower() in lower:
                response = obj_data.get(lang_key, "")
                followup = obj_data.get(followup_key, "")
                # Build clean conversational answer — never expose raw JSON keys
                answer = response
                if followup:
                    answer += f" {followup}"
                logger.info("[OBJECTION] Matched '%s' via trigger '%s'", obj_key, trigger)
                return ChatResponse(
                    answer=answer,
                    sources=[],
                    language=language,
                    fallback=False,
                )
    return None


# ── LiteLLM model routing order ─────────────────────────────────────────────
_LITELLM_MODELS = [
    f"groq/{os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile')}",
    f"openrouter/{os.environ.get('OPENROUTER_MODEL', 'meta-llama/llama-3.3-70b-instruct:free')}",
    f"ollama/{os.environ.get('OLLAMA_MODEL', 'llama3.2')}",
]

# ── Legacy direct-requests config (fallback when litellm not installed) ──────
_LEGACY_PROVIDERS = [
    {
        "name": "groq",
        "base_url": "https://api.groq.com/openai/v1/chat/completions",
        "api_key_env": "GROQ_API_KEY",
        "model": os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
    },
    {
        "name": "openrouter",
        "base_url": "https://openrouter.ai/api/v1/chat/completions",
        "api_key_env": "OPENROUTER_API_KEY",
        "model": os.environ.get("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free"),
    },
]


# ── LiteLLM call ─────────────────────────────────────────────────────────────
def _call_via_litellm(messages: list[dict]) -> tuple[str, str]:
    """
    Route through LiteLLM with automatic fallback across providers.
    Returns (response_text, provider_name).
    """
    errors = []
    for model_str in _LITELLM_MODELS:
        provider = model_str.split("/")[0]
        try:
            # Pass API keys via standard env vars that LiteLLM recognises:
            #   GROQ_API_KEY, OPENROUTER_API_KEY, OLLAMA_API_BASE
            kwargs: dict = {
                "model": model_str,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 300,
                "timeout": REQUEST_TIMEOUT,
            }
            if provider == "ollama":
                kwargs["api_base"] = os.environ.get("OLLAMA_URL", "http://localhost:11434")
            if provider == "openrouter":
                kwargs["api_key"] = os.environ.get("OPENROUTER_API_KEY", "")
                kwargs["extra_headers"] = {
                    "HTTP-Referer": "https://intermarq.agency",
                    "X-Title": "Intermarq Insurance Assistant",
                }

            resp = litellm.completion(**kwargs)
            text = resp.choices[0].message.content or ""
            if text:
                logger.info("[LLM] ✅ LiteLLM → %s", model_str)
                return text, provider
        except Exception as exc:
            msg = f"{model_str}: {type(exc).__name__}: {str(exc)[:120]}"
            errors.append(msg)
            logger.warning("[LLM] ⚠️  %s", msg)

    raise ConnectionError("All LiteLLM providers failed:\n" + "\n".join(errors))


# ── Legacy direct-requests fallback ──────────────────────────────────────────
def _call_via_requests(messages: list[dict]) -> tuple[str, str]:
    """Direct HTTP calls — used only if litellm is not installed."""
    errors = []
    for prov in _LEGACY_PROVIDERS:
        api_key = os.environ.get(prov["api_key_env"], "")
        if not api_key:
            errors.append(f"{prov['name']}: no API key")
            continue
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            if prov["name"] == "openrouter":
                headers.update({
                    "HTTP-Referer": "https://intermarq.agency",
                    "X-Title": "Intermarq Insurance Assistant",
                })
            resp = requests.post(
                prov["base_url"],
                headers=headers,
                json={"model": prov["model"], "messages": messages,
                      "temperature": 0.3, "max_tokens": 300},
                timeout=REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            text = resp.json()["choices"][0]["message"]["content"]
            if text:
                logger.info("[LLM] ✅ direct/%s", prov["name"])
                return text, prov["name"]
        except Exception as exc:
            msg = f"{prov['name']}: {type(exc).__name__}: {str(exc)[:100]}"
            errors.append(msg)
            logger.warning("[LLM] ⚠️  %s", msg)

    raise ConnectionError("All providers failed:\n" + "\n".join(errors))


def _call_llm(messages: list[dict]) -> tuple[str, str]:
    """Gateway: prefer LiteLLM, fall back to direct requests."""
    if _LITELLM_AVAILABLE:
        return _call_via_litellm(messages)
    return _call_via_requests(messages)


# ── Main entry point ──────────────────────────────────────────────────────────
def generate_answer(question: str, language: str = "en") -> ChatResponse:
    """
    Full RAG pipeline: filter → retrieve → generate → filter output.

    Args:
        question: User's free-text question
        language: "en" or "es"

    Returns:
        ChatResponse with answer, sources, fallback flag, and provider used
    """
    t0 = time.time()

    # ── Step 1: Input filter ────────────────────────────────────────
    input_check = filter_input(question)

    if not input_check["passed"]:
        reason = input_check["reason"]
        return ChatResponse(
            answer=FALLBACK_MESSAGES.get(reason, FALLBACK_MESSAGES["no_context"])[language],
            sources=[],
            language=language,
            fallback=True,
        )

    if input_check["escalate"]:
        return ChatResponse(
            answer=FALLBACK_MESSAGES["escalation"][language],
            sources=[],
            language=language,
            fallback=True,
        )

    # ── Step 1.5: Pre-RAG objection matcher ─────────────────────────
    # Deterministic keyword match against objections.json triggers
    # before the vector search can pull wrong chunks (Fix T4-005)
    objection_match = _match_objection(question, language)
    if objection_match:
        return objection_match


    # ── Step 2: Retrieve relevant chunks ────────────────────────────
    chunks = retrieve(question, top_k=MAX_CONTEXT_CHUNKS, threshold=0.3)

    if not chunks:
        return ChatResponse(
            answer=FALLBACK_MESSAGES["no_context"][language],
            sources=[],
            language=language,
            fallback=True,
        )

    context = "\n\n---\n\n".join([
        f"[Source: {c['source']} | {c['id']}]\n{c['text']}"
        for c in chunks
    ])
    sources = [
        SourceCitation(file=c["source"], chunk_id=c["id"], score=c["score"])
        for c in chunks
    ]

    # ── Step 3: Build messages ──────────────────────────────────────
    system_prompt = SYSTEM_PROMPT.format(context=context)
    if language == "es":
        system_prompt += "\n\nIMPORTANT: Respond in Spanish (Español)."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    # ── Step 4: Call LLM (via LiteLLM gateway) ─────────────────────
    provider = "unknown"
    try:
        raw_answer, provider = _call_llm(messages)
    except ConnectionError as exc:
        logger.error("[ERROR] All providers failed: %s", exc)
        # NEVER dump raw chunk text to the user — return a clean fallback
        fallback_msg = {
            "en": "I'm not sure about that, but a licensed Intermarq agent can clarify during your free 10-minute consultation.",
            "es": "No estoy seguro de eso, pero un agente licenciado de Intermarq puede aclararlo durante su consulta gratuita de 10 minutos."
        }
        return ChatResponse(
            answer=fallback_msg.get(language, fallback_msg["en"]),
            sources=sources,
            language=language,
            fallback=True,
        )

    # ── Step 5: Output filter ───────────────────────────────────────
    clean_answer = filter_output(raw_answer)
    source_line = ", ".join(set(c["source"].replace(".json", "") for c in chunks[:3]))
    clean_answer += f"\n\n_Sources: {source_line} | via {provider}_"

    # ── Step 6: Log telemetry (PII-safe) ────────────────────────────
    latency_ms = (time.time() - t0) * 1000
    log_chat_event(
        question=question,
        provider=provider,
        latency_ms=latency_ms,
        success=True,
    )

    return ChatResponse(
        answer=clean_answer,
        sources=sources,
        language=language,
        fallback=False,
        provider=provider,
    )
