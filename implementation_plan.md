# Revised Implementation Plan — Demo-First MVP

> **Key insight:** The knowledge base is solid (81/107 tests pass, 26 skipped by design — require runtime/integration). The gap is **no runnable chatbot**. Fix this before adding AI complexity.

## Priority Order

| # | Deliverable | Dependencies | Effort |
|---|-------------|-------------|--------|
| **1** | `demo/index.html` — Browser chatbot UI | None (reads JSONs) | Medium |
| **2** | `demo/chatbot_demo.py` — Terminal chatbot | None (pure Python) | Small |
| **3** | Data patches — agency config, psychology scripts | Existing JSONs | Small |
| **4** | `app/rag/` — RAG layer (Phase 2, optional) | ChromaDB + LLM | Large |

---

## Deliverable 1 — Browser Chatbot UI

**Skill:** No framework needed — pure HTML/CSS/JS. `04-frontend/react-best-practices` deferred to Phase 2.

### What It Does
A single-page, standalone chatbot that mimics production:
- Opens with greeting hook ("Most homeowners can qualify...")
- Shows 7-step qualification flow with **exact DOCX buttons** (no free text = no hallucination)
- Calculates lead score from answers
- Shows estimated pricing from [pricing.json](file:///c:/Projects/DHUMI%20Projects/US%20insurance%20chatbot/knowledge/pricing.json)
- Displays appointment booking CTA
- Handles all 5 objections with exact DOCX responses
- Bilingual EN/ES toggle
- AI disclosure banner ("You're chatting with an AI assistant")

### Data Sources (existing, no changes)
```
knowledge/scripts.json     → 7-step flow + buttons
knowledge/hooks.json       → greeting, trust, offline, CTA, closing
knowledge/objections.json  → 5 objection handlers
knowledge/pricing.json     → rate tables by age
knowledge/products.json    → product descriptions
knowledge/compliance.json  → disclaimers
```

### Anti-Hallucination Mechanism
- Steps 1–4, 6: **Button-only** (user cannot type)
- Step 5 (state): Text input → **normalized fuzzy match** (accepts `California`, `CA`, [calif](file:///c:/Projects/DHUMI%20Projects/US%20insurance%20chatbot/data_pipeline/test_chatbot_flow.py#70-77), case-insensitive, trimmed) → routing response
- Step 7: Form fields only (name, email, phone, zip)
- Objections: Pattern-matched to JSON triggers → exact JSON response
- Everything else: "A licensed agent can help with that"

### Design
- Modern glassmorphism card UI
- Chat bubble layout (bot left, user right)
- Smooth typing animations
- Mobile-responsive
- Dark header with agency branding placeholder
- `🟢 Online` / `🔴 Offline` indicator
- `EN | ES` language toggle

### How to Run

> [!IMPORTANT]
> Opening `index.html` directly as `file://` will fail — browsers block `fetch()` to local files (CORS). You **must** serve it locally:
> ```bash
> cd "c:\Projects\DHUMI Projects\US insurance chatbot"
> python -m http.server 8080
> # Open http://localhost:8080/demo/index.html
> ```

### File

#### [NEW] `demo/index.html`
Single file containing HTML + CSS + JS. Loads JSON via `fetch()` with UTF-8 encoding. Served via `python -m http.server`.

---

## Deliverable 2 — Terminal Chatbot

**Skill:** `03-backend/python-pro`

### What It Does
Interactive terminal conversation using exact DOCX text. Zero dependencies.

```
$ python demo/chatbot_demo.py

🤖 Most homeowners can qualify for mortgage protection
   coverage in under 2 minutes.

🤖 What would you like to protect today?
   [1] My Mortgage
   [2] My Family
   [3] Final Expenses
   [4] Business Protection
   [5] Just exploring

You: 1

🤖 How much coverage are you considering?
   ...
```

At the end: lead score → price estimate → appointment CTA → "Lead routed to CRM ✅"

### File

#### [NEW] `demo/chatbot_demo.py`
Pure Python, reads JSONs with `open(..., encoding='utf-8')`, `while` loop through steps.

---

## Deliverable 3 — Data Patches

### 3a. Agency Config

#### [NEW] `knowledge/agency.json`
```json
{
  "name": "Intermarq Agency",
  "license_ca": "PLACEHOLDER-DOI-LICENSE",
  "npn": "PLACEHOLDER-NPN",
  "phone": "(XXX) XXX-XXXX",
  "email": "info@intermarqagency.com",
  "website": "https://intermarqagency.com",
  "calendly_url": "https://calendly.com/intermarq-agency/10min",
  "hours": "Mon–Fri 9am–5pm PT",
  "address": "California, USA"
}
```

### 3b. Psychology-Based Triggers

#### [MODIFY] [knowledge/hooks.json](file:///c:/Projects/DHUMI%20Projects/US%20insurance%20chatbot/knowledge/hooks.json)
Add the 5 psychology triggers referenced in DOCX:

| Trigger | Psychology | When |
|---------|-----------|------|
| Urgency | "Rates increase with age — lock in today's rate" | After pricing display |
| Social proof | "Over 500 California families have protected their mortgages" | During flow |
| Loss aversion | "What would happen to your family's home if something happened to you?" | Step 1 reframe |
| Reciprocity | "Let me get you a free personalized quote" | Before lead capture |
| Scarcity | "Limited appointment slots available this week" | Booking CTA |

### 3c. CRM/Calendar Mock

Integration simulation in the demo UI:
- Step 7 submit → "Lead sent to Intermarq CRM" toast (**no raw PII in console** — log only `"lead_submitted: true"`)
- Appointment CTA → Opens Calendly link (or mock alert)
- Email notification → "📧 Confirmation sent" toast (**mask email**: show `h***@gmail.com`, never log raw)

> [!WARNING]
> **PII Logging Ban:** Never log raw name, email, phone, or zip to `console.log()` or analytics. Use masked values only (e.g., `J*** D***`, `h***@example.com`). This applies to both browser console and terminal output.

---

## Deliverable 4 — RAG Layer (Phase 2)

**Skills:** `01-ai-core/rag-engineer`, `02-data/embedding-strategies`, `03-backend/fastapi-pro`

> [!IMPORTANT]
> Only build this AFTER Deliverables 1-3 are working. The button-based flow covers 90% of the user journey. RAG is only needed for free-text questions ("What's the difference between term life and whole life?").

### Architecture
```
Free-text question → Input filter → ChromaDB retrieval → LLM with constitution → Output filter → Response + citation
```

### Stack
| Component | Tech |
|-----------|------|
| Embeddings | `all-MiniLM-L6-v2` |
| Vector DB | ChromaDB (local) |
| LLM | GPT-4o-mini |
| Backend | FastAPI |
| Guardrails | Constitutional system prompt |

### Files
```
app/
├── main.py
├── rag/embed_knowledge.py
├── rag/retriever.py
├── rag/generator.py
├── guardrails/constitution.py
├── guardrails/filters.py
└── models/schemas.py
```

---

## Verification Plan

### Deliverable 1 (Browser UI)
- Open `demo/index.html` in browser
- Complete full 7-step flow in English
- Switch to Spanish, complete flow again
- Trigger each objection ("I already have insurance" etc.)
- Verify pricing matches [pricing.json](file:///c:/Projects/DHUMI%20Projects/US%20insurance%20chatbot/knowledge/pricing.json)
- Verify all text matches DOCX exactly
- Try typing in free-text → verify it's blocked/handled
- Check mobile responsiveness

### Deliverable 2 (Terminal)
- Run `python demo/chatbot_demo.py`
- Complete flow with different answer combinations
- Verify lead scoring outputs
- Verify UTF-8 characters render correctly

### Deliverable 3 (Data Patches)
- Verify `agency.json` loads in both demos
- Verify psychology hooks appear at correct positions
- Run `python data_pipeline/run_test_suites.py` → still 81/107 passed (26 skipped by design)

### Security
- Snyk scan on all new files
- XSS test on HTML input fields
- Verify no PII logged to console
