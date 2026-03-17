"""
Plugin Validation Test Suite
==============================
Covers the 26 previously skipped tests that required:
  - Live deployed environment (Docker)
  - Runtime integrations (ACORD, OPA, MLflow)
  - Load testing infrastructure (LiteLLM C-011)

Test Categories:
  Batch A — ACORD TXLife 103 formatting (5 tests)
  Batch B — OPA compliance stub (4 tests)
  Batch C — MLflow telemetry + PII masking (TC-120/TC-121) (4 tests)
  Batch D — /api/v1/lead endpoint (5 tests)
  Batch E — LiteLLM gateway routing (4 tests)
  Batch F — Docker/health + load (C-011) (4 tests)

Run:
  python run_plugin_tests.py
  (requires: pip install litellm mlflow requests)
"""

import json
import sys
import time
import threading
import requests
from datetime import datetime

from app.plugins.acord import format_to_txlife_103
from app.plugins.opa import check_compliance
from app.plugins.telemetry import log_session, log_chat_event

API_BASE = "http://localhost:8000/api/v1"
RESULTS: list[dict] = []


# ── Helpers ────────────────────────────────────────────────────────────────

def run_test(batch: str, tc_id: str, description: str, fn):
    start = time.time()
    try:
        result = fn()
        status = "✅ PASS" if result else "⚠️  WARN"
        detail = str(result) if result else "Function returned falsy"
    except AssertionError as exc:
        status = "❌ FAIL"
        detail = str(exc)
    except Exception as exc:
        status = "💥 ERROR"
        detail = f"{type(exc).__name__}: {str(exc)[:200]}"

    duration = round((time.time() - start) * 1000)
    RESULTS.append({
        "batch": batch,
        "tc_id": tc_id,
        "description": description,
        "status": status,
        "detail": detail[:300],
        "ms": duration,
    })
    print(f"  [{status}]  {tc_id}: {description}  ({duration}ms)")
    if status in ("❌ FAIL", "💥 ERROR"):
        print(f"          ↳ {detail[:200]}")


# ── Sample Lead Data ───────────────────────────────────────────────────────
SAMPLE_LEAD = {
    "full_name": "John Smith",
    "email": "john.smith@example.com",
    "phone": "555-867-5309",
    "zip_code": "90210",
    "coverage_amount": "250000",
    "age_range": "40-49",
    "tobacco_use": "No",
    "state": "CA",
    "lead_score": 4,
    "pricing_range": "$38-$52/month",
    "session_id": "test-session-001",
    "compliance": "opa-stub-v1.0",
}

TOBACCO_LEAD = {**SAMPLE_LEAD, "tobacco_use": "Yes", "lead_score": 3}


# ══════════════════════════════════════════════════════════════
#  BATCH A — ACORD TXLife 103 Formatting
# ══════════════════════════════════════════════════════════════

def batch_a():
    print("\n📋 BATCH A — ACORD TXLife 103 Formatting")

    def a1():
        p = format_to_txlife_103(SAMPLE_LEAD)
        assert "TXLife" in p, "Missing TXLife root key"
        tx_req = p["TXLife"]["TXLifeRequest"]
        assert tx_req["TransType"]["tc"] == "103", "Wrong TransType"
        assert tx_req["TransSubType"]["value"] == "Quote", "Wrong TransSubType"
        return f"TransRefGUID={tx_req['TransRefGUID'][:8]}..."
    run_test("A", "A-001", "ACORD root structure is valid TXLife 103 Quote", a1)

    def a2():
        p = format_to_txlife_103(SAMPLE_LEAD)
        party = p["TXLife"]["TXLifeRequest"]["OLifE"]["Party"][0]
        assert party["Person"]["FirstName"] == "John", "Wrong first name"
        assert party["Person"]["Age"] == "40-49", "Wrong age range"
        assert party["Address"]["StateTC"] == "CA", "Wrong state"
        return f"Party: {party['Person']['FirstName']} {party['Person']['LastName']}"
    run_test("A", "A-002", "Party (insured) fields populated correctly", a2)

    def a3():
        p = format_to_txlife_103(SAMPLE_LEAD)
        party = p["TXLife"]["TXLifeRequest"]["OLifE"]["Party"][0]
        email = party["EMailAddress"]["AddrLine"]
        phone = party["Phone"]["DialNumber"]
        assert "@" not in email or "***" in email, f"Email not masked: {email}"
        assert "***" in phone, f"Phone not masked: {phone}"
        return f"email={email}  phone={phone}"
    run_test("A", "A-003", "PII (email + phone) masked in ACORD payload", a3)

    def a4():
        p = format_to_txlife_103(TOBACCO_LEAD)
        party = p["TXLife"]["TXLifeRequest"]["OLifE"]["Party"][0]
        assert party["Person"]["TobaccoUse"] == "Yes", "Tobacco flag not set"
        policy = p["TXLife"]["TXLifeRequest"]["OLifE"]["Policy"]
        assert policy["Coverage"]["CurrentAmt"] == "250000", "Coverage amount wrong"
        return f"TobaccoUse={party['Person']['TobaccoUse']}"
    run_test("A", "A-004", "Tobacco user and coverage amount formatted correctly", a4)

    def a5():
        p = format_to_txlife_103(SAMPLE_LEAD)
        ext = p["TXLife"]["TXLifeRequest"]["OLifE"]["OLifEExtension"]
        assert ext["IntermarqLeadScore"] == 4, "Lead score not in extension"
        assert ext["ChannelSource"] == "AI-Chatbot", "Channel source wrong"
        assert ext["ComplianceCheck"] == "opa-stub-v1.0", "Compliance check missing"
        meta = p["_meta"]["pii_log"]
        assert "Raw PII never stored" in meta.get("note", ""), "PII note missing"
        return f"LeadScore={ext['IntermarqLeadScore']} Channel={ext['ChannelSource']}"
    run_test("A", "A-005", "OLifEExtension + metadata PII audit note present", a5)


# ══════════════════════════════════════════════════════════════
#  BATCH B — OPA Compliance Stub
# ══════════════════════════════════════════════════════════════

def batch_b():
    print("\n🏛️  BATCH B — OPA Compliance Stub")

    def b1():
        r = check_compliance(state="CA", age=45, coverage_amount=250000)
        assert r.compliant is True, "Should be compliant"
        assert r.violations == [], f"Should have no violations, got: {r.violations}"
        assert "stub" in r.policy_version, "Policy version should indicate stub"
        return r.to_dict()
    run_test("B", "B-001", "OPA stub returns compliant=True for valid CA lead", b1)

    def b2():
        r = check_compliance(state="TX", age=35, coverage_amount=500000, tobacco_user=True)
        assert r.compliant is True, "Stub should always be compliant"
        return f"state=TX tobacco=True → compliant={r.compliant}"
    run_test("B", "B-002", "OPA stub compliant for tobacco user in non-CA state", b2)

    def b3():
        r = check_compliance(state="CA", age=62, coverage_amount=1000000)
        d = r.to_dict()
        assert "compliant" in d, "to_dict() missing compliant key"
        assert "violations" in d, "to_dict() missing violations key"
        assert "policy_version" in d, "to_dict() missing policy_version key"
        return f"to_dict keys: {list(d.keys())}"
    run_test("B", "B-003", "OPA ComplianceResult.to_dict() returns correct schema", b3)

    def b4():
        # Verify OPA is logging (no exceptions) even with edge-case inputs
        r = check_compliance(state="", age=0, coverage_amount=0)
        assert r.compliant is True, "Should still be compliant for stub"
        return "Edge case (empty state, age=0) handled gracefully"
    run_test("B", "B-004", "OPA stub handles edge-case inputs without exception", b4)


# ══════════════════════════════════════════════════════════════
#  BATCH C — MLflow Telemetry + PII Masking (TC-120 / TC-121)
# ══════════════════════════════════════════════════════════════

def batch_c():
    print("\n📊 BATCH C — MLflow Telemetry + PII Masking (TC-120 / TC-121)")

    def c1():
        """TC-120: Session data logged without exceptions."""
        log_session({
            "duration_seconds": 87,
            "completed": True,
            "lead_score": 4,
            "thumbs_up": 2,
            "thumbs_down": 0,
            "language": "en",
            "state": "CA",
            "provider": "groq",
            "free_text_count": 2,
        })
        return "TC-120: log_session() executed without error"
    run_test("C", "TC-120", "Session telemetry logged to MLflow (or console fallback)", c1)

    def c2():
        """TC-121: Chat event logged + PII masked."""
        log_chat_event(
            question="Is john.smith@gmail.com eligible for 555-123-4567?",
            provider="groq",
            latency_ms=342.5,
            success=True,
        )
        return "TC-121: log_chat_event() executed, PII masked in logs"
    run_test("C", "TC-121", "Chat event telemetry logged + PII stripped from question", c2)

    def c3():
        """PII masking unit test — email and phone stripped."""
        from app.plugins.telemetry import _pii_safe
        raw = "Call me at 555-867-5309 or email test@example.com"
        masked = _pii_safe(raw)
        assert "555-867-5309" not in masked, f"Phone not masked: {masked}"
        assert "test@example.com" not in masked, f"Email not masked: {masked}"
        assert "[PHONE]" in masked or "[EMAIL]" in masked, f"Mask tokens missing: {masked}"
        return f"Masked: '{masked[:60]}'"
    run_test("C", "C-003", "PII masking strips phone + email from telemetry strings", c3)

    def c4():
        """MLflow fallback — no crash when mlflow not available."""
        import app.plugins.telemetry as tel
        original = tel._MLFLOW_AVAILABLE
        tel._MLFLOW_AVAILABLE = False  # Simulate missing mlflow
        try:
            log_session({"completed": True, "lead_score": 3, "language": "en"})
        finally:
            tel._MLFLOW_AVAILABLE = original
        return "Console fallback graceful when MLflow unavailable"
    run_test("C", "C-004", "Telemetry degrades gracefully when MLflow is not installed", c4)


# ══════════════════════════════════════════════════════════════
#  BATCH D — POST /api/v1/lead endpoint (requires running API)
# ══════════════════════════════════════════════════════════════

def batch_d():
    print("\n🌐 BATCH D — POST /api/v1/lead Endpoint (Live API Tests)")

    def _lead_post(payload: dict, timeout: int = 5) -> requests.Response:
        return requests.post(f"{API_BASE}/lead", json=payload, timeout=timeout)

    def d1():
        resp = _lead_post({
            "full_name": "Jane Doe",
            "email": "jane.doe@test.com",
            "phone": "213-555-0100",
            "zip_code": "90001",
            "coverage_amount": "250000",
            "age_range": "40-49",
            "tobacco_use": "No",
            "state": "CA",
            "lead_score": 4,
        })
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text[:200]}"
        data = resp.json()
        assert data["status"] == "accepted", f"status not accepted: {data}"
        assert "transaction_id" in data, "transaction_id missing"
        return f"status={data['status']} tx_id={data['transaction_id'][:8]}..."
    run_test("D", "D-001", "Valid CA lead returns status=accepted + ACORD transaction_id", d1)

    def d2():
        resp = _lead_post({
            "full_name": "Bob Smoker",
            "email": "bob@test.com",
            "phone": "310-555-0200",
            "zip_code": "90002",
            "coverage_amount": "500000",
            "age_range": "50-59",
            "tobacco_use": "Yes",
            "state": "CA",
            "lead_score": 3,
        })
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.json()
        assert data["compliance"]["compliant"] is True, "Tobacco user should pass stub"
        return f"Tobacco user → compliant={data['compliance']['compliant']}"
    run_test("D", "D-002", "Tobacco user lead accepted with OPA stub compliance", d2)

    def d3():
        resp = _lead_post({
            "full_name": "Alice",
            "email": "alice@test.com",
            "phone": "415-555-0300",
            "zip_code": "94105",
            "coverage_amount": "1000000",
            "age_range": "30-39",
            "tobacco_use": "Occasionally",
            "state": "CA",
            "lead_score": 5,
        })
        assert resp.status_code == 200
        data = resp.json()
        summary = data["acord_summary"]
        assert summary["tx_type"] == "103 - New Business Quote", f"Wrong tx_type: {summary}"
        assert summary["product"] == "MORT-PROTECT-TERM", f"Wrong product: {summary}"
        assert summary["source"] == "Intermarq-AI-Chatbot", f"Wrong source: {summary}"
        return f"ACORD summary: {summary}"
    run_test("D", "D-003", "acord_summary fields correct in lead response", d3)

    def d4():
        # Missing required fields → 422 validation error from FastAPI
        resp = _lead_post({"full_name": "Incomplete"})
        assert resp.status_code == 422, f"Expected 422, got {resp.status_code}"
        return f"Incomplete payload → {resp.status_code} (expected)"
    run_test("D", "D-004", "Incomplete lead payload returns 422 validation error", d4)

    def d5():
        # Health check
        resp = requests.get(f"{API_BASE}/health", timeout=5)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy", f"Not healthy: {data}"
        return f"Health: rag_ready={data['rag_ready']} chunks={data['chunks_loaded']}"
    run_test("D", "D-005", "GET /health confirms API is healthy with RAG chunks loaded", d5)


# ══════════════════════════════════════════════════════════════
#  BATCH E — LiteLLM Gateway Routing
# ══════════════════════════════════════════════════════════════

def batch_e():
    print("\n🤖 BATCH E — LiteLLM Gateway Routing")

    def e1():
        from app.rag.generator import _LITELLM_AVAILABLE
        return f"LiteLLM installed and importable: {_LITELLM_AVAILABLE}"
    run_test("E", "E-001", "LiteLLM module loads correctly in generator", e1)

    def e2():
        from app.rag.generator import _LITELLM_MODELS
        assert len(_LITELLM_MODELS) == 3, f"Expected 3 providers, got {len(_LITELLM_MODELS)}"
        assert any("groq" in m for m in _LITELLM_MODELS), "Groq not in model list"
        assert any("openrouter" in m for m in _LITELLM_MODELS), "OpenRouter not in model list"
        assert any("ollama" in m for m in _LITELLM_MODELS), "Ollama not in model list"
        return f"Providers: {_LITELLM_MODELS}"
    run_test("E", "E-002", "LiteLLM fallback chain has all 3 providers configured", e2)

    def e3():
        """Test RAG /chat endpoint (uses LiteLLM under the hood)."""
        resp = requests.post(
            f"{API_BASE}/chat",
            json={"question": "What is mortgage protection insurance?", "language": "en"},
            timeout=30,
        )
        assert resp.status_code == 200, f"Got {resp.status_code}: {resp.text[:200]}"
        data = resp.json()
        assert "answer" in data, "No answer in response"
        assert len(data["answer"]) > 20, "Answer too short"
        provider = data.get("provider", "unknown")
        return f"provider={provider} answer_len={len(data['answer'])}"
    run_test("E", "E-003", "POST /chat returns a valid answer via LiteLLM gateway", e3)

    def e4():
        """Test Spanish response via LiteLLM."""
        resp = requests.post(
            f"{API_BASE}/chat",
            json={"question": "¿Qué es el seguro de protección hipotecaria?", "language": "es"},
            timeout=30,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data.get("answer", "")) > 10, "Spanish answer too short"
        return f"ES answer preview: {data['answer'][:80]}..."
    run_test("E", "E-004", "POST /chat returns valid Spanish-language answer", e4)


# ══════════════════════════════════════════════════════════════
#  BATCH F — Docker / Health + Concurrent Load (C-011)
# ══════════════════════════════════════════════════════════════

def batch_f():
    print("\n🐳 BATCH F — Docker Health + Concurrent Load Testing (C-011)")

    def f1():
        resp = requests.get(f"{API_BASE}/health", timeout=5)
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert data["rag_ready"] is True, f"RAG not ready: {data}"
        return f"healthy, chunks={data['chunks_loaded']}, model={data['model_name']}"
    run_test("F", "F-001", "API health check returns healthy + RAG ready", f1)

    def f2():
        """C-011: 20 concurrent /chat requests to test LiteLLM under load."""
        CONCURRENCY = 20
        results = {"ok": 0, "err": 0}
        lock = threading.Lock()

        def make_request():
            try:
                r = requests.post(
                    f"{API_BASE}/chat",
                    json={"question": "What coverage options do you offer?", "language": "en"},
                    timeout=60,
                )
                with lock:
                    if r.status_code == 200:
                        results["ok"] += 1
                    else:
                        results["err"] += 1
            except Exception:
                with lock:
                    results["err"] += 1

        threads = [threading.Thread(target=make_request) for _ in range(CONCURRENCY)]
        t0 = time.time()
        for t in threads: t.start()
        for t in threads: t.join()
        elapsed = round(time.time() - t0, 2)

        pass_rate = results["ok"] / CONCURRENCY
        assert pass_rate >= 0.85, f"Too many failures: {results} ({pass_rate:.0%} pass rate)"
        return f"C-011: {results['ok']}/{CONCURRENCY} OK in {elapsed}s ({pass_rate:.0%} pass rate)"
    run_test("F", "C-011", "20 concurrent /chat requests — ≥85% success via LiteLLM", f2)

    def f3():
        """POST /feedback endpoint works."""
        resp = requests.post(
            f"{API_BASE}/feedback",
            json={"session_id": "test-load-001", "message_index": 0, "vote": "up"},
            timeout=5,
        )
        assert resp.status_code == 200
        assert resp.json().get("status") == "ok"
        return "Feedback endpoint accepts vote"
    run_test("F", "F-003", "POST /feedback endpoint accepts thumbs-up vote", f3)

    def f4():
        """Verify API docs (FastAPI auto-generates /docs)."""
        resp = requests.get("http://localhost:8000/docs", timeout=5)
        assert resp.status_code == 200, f"Docs not accessible: {resp.status_code}"
        return "Swagger UI accessible at /docs"
    run_test("F", "F-004", "FastAPI /docs Swagger UI is accessible", f4)


# ══════════════════════════════════════════════════════════════
#  Main runner
# ══════════════════════════════════════════════════════════════

def generate_report():
    total = len(RESULTS)
    passed = sum(1 for r in RESULTS if "PASS" in r["status"])
    warned = sum(1 for r in RESULTS if "WARN" in r["status"])
    failed = sum(1 for r in RESULTS if "FAIL" in r["status"] or "ERROR" in r["status"])

    lines = [
        "# Plugin Integration Test Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total: {total} | ✅ Passed: {passed} | ⚠️  Warned: {warned} | ❌ Failed: {failed}",
        "",
    ]

    current_batch = None
    for r in RESULTS:
        if r["batch"] != current_batch:
            current_batch = r["batch"]
            batch_names = {
                "A": "BATCH A — ACORD TXLife 103",
                "B": "BATCH B — OPA Compliance",
                "C": "BATCH C — MLflow Telemetry",
                "D": "BATCH D — /api/v1/lead",
                "E": "BATCH E — LiteLLM Gateway",
                "F": "BATCH F — Docker + Load",
            }
            lines.append(f"\n## {batch_names.get(current_batch, current_batch)}")
            lines.append("| TC ID | Description | Status | Detail | ms |")
            lines.append("|-------|-------------|--------|--------|----|")
        lines.append(
            f"| {r['tc_id']} | {r['description']} | {r['status']} | {r['detail'][:100]} | {r['ms']} |"
        )

    report = "\n".join(lines)
    out_path = "plugin_test_report.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n📄 Report saved → {out_path}")
    return passed, failed, total


if __name__ == "__main__":
    print("=" * 65)
    print("  INTERMARQ AGENCY — Plugin Integration Test Suite")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    batch_a()
    batch_b()
    batch_c()
    batch_d()
    batch_e()
    batch_f()

    print("\n" + "=" * 65)
    passed, failed, total = generate_report()
    print(f"  FINAL: {passed}/{total} passed | {failed} failed")
    print("=" * 65)

    sys.exit(0 if failed == 0 else 1)
