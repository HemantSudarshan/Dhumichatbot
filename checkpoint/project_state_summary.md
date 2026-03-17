# Complete Project State: Intermarq US Insurance Chatbot
**Exported Context for New Chat/LLM Handoff**

This document serves as an exhaustive brain-dump of the entire project scope, architecture, resolved bugs, and current state of the Intermarq US Insurance Chatbot project. It is designed to be fed as context to a fresh LLM session to instantly catch it up.

---

## 1. Project Overview
Intermarq is a California-based insurance agency. The goal was to build a dual-layer AI application:
1. **Frontend:** A structured, high-converting, mobile-friendly Chatbot with a strict 7-step guided flow, heavily branded (black, gold, glassmorphic UI). Built currently in pure HTML/JS as a prototype (`demo/index.html`), but intended to be rebuilt via Lovable.dev into a React application (`lovable_frontend_prompt.md`).
2. **Backend:** A robust, hardened Python/FastAPI backend utilizing a LiteLLM gateway (Groq, OpenRouter, Ollama fallbacks) to process free-chat questions via RAG (Retrieval-Augmented Generation) against a local ChromaDB vector store.

### Core Value Props:
* Provide quotes and information for Mortgage Protection, Term Life, and Final Expense.
* Operate under strict compliance (CA SB 263, NIPR registration, no unauthorized products).
* Defend against prompt injections, sycophancy, competitor mentioning, and PII leakage.
* Capture leads and seamlessly route to humans via Calendly scheduling.

---

## 2. Architecture Details

### The Backend (`app/`)
* **Framework:** FastAPI (`app/main.py`) running via Docker Compose alongside the frontend.
* **LLM Orchestration:** `app/rag/generator.py` uses `litellm` to route requests to primary models (like Llama 3.3 70B via Groq/OpenRouter) with built-in retries.
* **Vector Store & Retrieval:** ChromaDB (`app/rag/retriever.py`) using `sentence-transformers/all-MiniLM-L6-v2`. Embeds documents from the `knowledge/` directory.
* **Guardrails (`app/guardrails/constitution.py`):**
  * **System Prompt:** Instructs the LLM to *only* answer using retrieved context, add CA SB 263 disclaimers, refuse out-of-bounds topics (auto insurance, politics), and never output raw JSON.
  * **Input Filters:** Regex patterns blocking "ignore previous instructions", "act as a...", etc.
  * **Output Filters:** Redacts PII (`[REDACTED PHONE/EMAIL]`) and checks for sycophancy (e.g., agreeing that Intermarq is "bad" or agreeing with negative statements).
* **Endpoints:**
  * `POST /api/v1/chat`: Handles RAG questions. Expects `question` and `language` ("en" or "es"). Returns answer, sources, and a `fallback` toggle.
  * `POST /api/v1/lead`: (Stubbed) Ingests lead data and simulates a TXLife 103 ACORD submission.

### The Frontend (`demo/index.html`)
* **State Machine:** A rigid 7-step flow (Intent, Coverage, Age, Tobacco, State, Price calculation, Lead Form) that completely locks the free-text input until explicitly needed.
* **Fuzzy Logic Validation:** In Step 5, it uses Levenshtein distance filtering (`isCaliforniaInput()`) to accept "CA", "Cali", "Calfornia" (typos) while rejecting "NY", "Texas", etc. Non-CA users are hit with a soft rejection ("Notify me when you expand").
* **API Rate Limiting:** `let freeTextCount = 0; const MAX_FREE_CHATS = 3;`. Users get exactly 3 free-chat RAG queries. Once exhausted, the chat locks permanently, and an inline popup forces a "📅 Schedule 10-min Call" (Calendly bypass).
* **Bilingual Support (EN/ES):** Full toggling capability. If switched mid-chat, a `confirm()` dialog fires; if accepted, it *completely wipes all state* (Step=0, Limiter=0, clears messages) to prevent cross-language context bleed.

### The Knowledge Base (`knowledge/`)
9 JSON files containing dictionaries of responses, scripts, FAQs, and objections:
* `agency.json` / `products.json` / `pricing.json` / `faq.json` / `compliance.json`
* **`scripts.json`:** The step-by-step UI script.
* **`hooks.json`:** Psychological trust-builders and conversational filler.
* **`objections.json`:** Deterministic keyword triggers for things like "Already have insurance" or "Too expensive", pre-empting the LLM RAG search entirely.

---

## 3. Critical Fixes Applied in the Final Sessions
A rigorous testing phase using `tests/chatbot-test-suite.md` and `run_red_team_tests.py` uncovered several bugs, which have all been fixed:

1. **RAG JSON Dumping Bug:** The LLM was occasionally regurgitating raw `definition_en: "..."` keys instead of prose. 
   - *Fix:* Added Rule 11 to `constitution.py` explicitly ordering the LLM to synthesize data and never output code/JSON keys. Updated `generator.py`'s `_match_objection` to format strings purely as conversational text.
2. **"Chat More" Loophole:** The 3-Chat Limiter originally supplied a "Chat More" button that bypassed the restriction. 
   - *Fix:* Removed the "Chat More" option from the limiter block in `demo/index.html` and `lovable_frontend_prompt.md`. Once 3 chats are burned, the *only* option is Calendly. 
3. **Ghost Language State Bug:** Switching the language from EN to ES mid-chat previously caused weird mixed-language responses. 
   - *Fix:* `setLang()` in `demo/index.html` now thoroughly resets all variables (`STEP`, `freeTextCount`, `ANSWERS`) and wipes the `MSGS.innerHTML` so the chat restarts clean. Checked all JSON files (especially `compliance.json` and `scripts.json`) to ensure all `_es` variations were populated.
4. **Pre-RAG Objection Routing:** RAG vector similarity sometimes grabbed the wrong chunk for objections. 
   - *Fix:* Implemented `_match_objection()` in `generator.py`. It explicitly checks user input against `objections.json` first, and if a match is found, returns that hardcoded response *instantly* instead of invoking the LLM. 

---

## 4. Current Deployment & Run State
* **To build & run:** `docker-compose down ; docker-compose up --build -d`
* **Test the Prototype:** Open `http://localhost:8080/demo/index.html` (the Nginx container).
* **Test the API Health:** `curl http://localhost:8000/api/v1/health`
* **Test the RAG:** `curl -X POST http://localhost:8000/api/v1/chat -H "Content-Type: application/json" -d '{"question":"What is final expense?","language":"en"}'`

## 5. Next Steps / LOVABLE.DEV Handoff
The primary goal moving forward is to port the prototype `demo/index.html` into a production-grade React application leveraging `shadcn/ui` and deep glassmorphism.
* The file `lovable_frontend_prompt.md` is fully up to date and contains EVERY logic rule (the 7 steps, the state lockouts, the 3-chat limiter, the language reset, and the CA state fuzzy match). 
* **The user should directly copy `lovable_frontend_prompt.md` into Lovable.dev to generate the React application.**
