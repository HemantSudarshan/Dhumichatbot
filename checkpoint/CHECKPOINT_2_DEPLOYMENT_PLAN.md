# 📋 Checkpoint 2 — Conceptual MVP: Demo-First Approach

> **Date:** March 16, 2026  
> **Status:** REVISED — demo-first, RAG deferred to Phase 2  
> **Previous:** `CHECKPOINT_A_TO_Z.md`

---

## What Exists ✅ vs What's Missing ❌

| Layer | Status |
|-------|--------|
| 8 JSON knowledge files (bilingual EN/ES) | ✅ Solid |
| 15/15 DOCX alignment checks | ✅ Verified |
| 107 test specs (81 pass, 26 skipped) | ✅ Comprehensive |
| Data pipeline (stream + normalize) | ✅ Working |
| **Runnable chatbot interface** | ❌ **Nothing exists** |
| **Backend API** | ❌ Not built |
| **RAG / embeddings** | ❌ Not built |

**Key insight:** You prevent hallucinations by constraining the UI (buttons only) and using deterministic state machine logic — not by adding more complex AI.

---

## Revised Priority Order

| # | Deliverable | What | Dependencies |
|---|-------------|------|-------------|
| **1** | `demo/index.html` | Browser chatbot — stakeholder demo | None |
| **2** | `demo/chatbot_demo.py` | Terminal chatbot — dev testing | None |
| **3** | Data patches | Agency config + psychology hooks | Existing JSONs |
| **4** | `app/rag/` (Phase 2) | RAG for free-text questions | ChromaDB + LLM |

---

## Deliverable 1 — Browser UI (`demo/index.html`)

**Highest priority.** Single standalone HTML file, no server needed.

### Features
- Greeting hook → 7-step qualification → lead score → pricing → appointment CTA
- **Button-only** for Steps 1–4, 6 (no free text = no hallucination)
- Text input for Step 5 (state) and Step 7 (lead capture form)
- Bilingual EN/ES toggle
- All 5 objection handlers with exact DOCX responses
- AI disclosure banner
- Modern glassmorphism design, mobile-responsive
- CRM mock (console.log + toast), Calendly link placeholder

### Data Sources
- `scripts.json` → questions + buttons
- `hooks.json` → greeting, trust, CTA, closing
- `objections.json` → 5 handlers
- `pricing.json` → rate tables
- `agency.json` → identity (new)

---

## Deliverable 2 — Terminal Demo (`demo/chatbot_demo.py`)

Pure Python, zero dependencies. Interactive `while` loop with numbered choices.

```
🤖 What would you like to protect today?
   [1] My Mortgage  [2] My Family  [3] Final Expenses ...
You: 1
```

At the end: lead score → price estimate → CTA → "✅ Lead routed to CRM"

---

## Deliverable 3 — Data Patches

| Patch | File |
|-------|------|
| Agency identity (NPN, license, contact) | `[NEW] knowledge/agency.json` |
| 5 psychology triggers (urgency, social proof, loss aversion, reciprocity, scarcity) | `[MODIFY] knowledge/hooks.json` |
| CRM/Calendar mock config | Built into demo UI |

---

## Deliverable 4 — RAG Layer (Phase 2, Optional)

> Only needed for free-text questions like "What's the difference between term and whole life?" The button-based flow covers 90% of the journey without any AI.

| Component | Tech |
|-----------|------|
| Embeddings | `all-MiniLM-L6-v2` |
| Vector DB | ChromaDB |
| LLM | GPT-4o-mini |
| Backend | FastAPI |
| Guardrails | Constitutional system prompt |

---

## Skills Used

| Deliverable | Skills from `skills/` |
|-------------|----------------------|
| Browser UI | _Pure HTML/JS — no skill needed_ |
| Terminal demo | `03-backend/python-pro` |
| Data patches | `01-ai-core/prompt-engineering` (psychology hooks) |
| RAG (Phase 2) | `01-ai-core/rag-engineer`, `02-data/embedding-strategies`, `03-backend/fastapi-pro` |

---

## Anti-Hallucination Strategy

```
┌────────────────────────────┐
│ Steps 1-4, 6: BUTTONS ONLY │  ← User cannot type = bot cannot hallucinate
├────────────────────────────┤
│ Step 5: Text → exact match  │  ← "California" ✅ / anything else → fallback
├────────────────────────────┤
│ Step 7: Form fields only    │  ← Name, email, phone, zip — no free text Q&A
├────────────────────────────┤
│ Objections: Pattern match   │  ← Exact trigger words → exact JSON response
├────────────────────────────┤
│ Everything else: Fallback   │  ← "A licensed agent can help with that"
└────────────────────────────┘
```

**Result: 100% deterministic. Zero hallucination risk in the button-based flow.**

---

## UTF-8 Note

The JSON files contain proper Unicode (en dash, em dash, accents, stars ⭐). Both demos must:
- Python: `open(..., encoding='utf-8')`
- JavaScript: `fetch(...).then(r => r.json())` (UTF-8 by default)
- PowerShell: `Get-Content -Encoding UTF8`

---

## What's NOT Changing

| Item | Status |
|------|--------|
| `knowledge/*.json` (8 files) | ✅ Untouched |
| `data_pipeline/` (8 scripts) | ✅ Untouched |
| `tests/` (3 specs) | ✅ Untouched |
| 81/81 test results | ✅ Still passing |
