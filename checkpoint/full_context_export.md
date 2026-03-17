# Complete Project State: Intermarq US Insurance Chatbot
**Exported Context for New Chat/LLM Handoff**

This document serves as an exhaustive brain-dump of the entire project scope, architecture, resolved bugs, and current state of the Intermarq US Insurance Chatbot project. It is designed to be fed as context to a fresh LLM session to instantly catch it up.

---

## 1. Project Overview
Intermarq is a California-based insurance agency. The goal was to build a dual-layer AI application:
1. **Frontend:** A structured, high-converting, mobile-friendly Chatbot with a strict 7-step guided flow, heavily branded (black, gold, glassmorphic UI). Built currently in pure HTML/JS as a prototype (`demo/index.html`).
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
  * **Input/Output Filters:** Regex patterns block "ignore previous instructions", redact PII, and check for sycophancy.
* **Endpoints:**
  * `POST /api/v1/chat`: Handles RAG questions. Expects `question` and `language` ("en" or "es").
  * `POST /api/v1/lead`: (Stubbed) Ingests lead data and simulates a TXLife 103 ACORD submission.

### The Frontend (`demo/index.html`)
* **State Machine:** A rigid 7-step flow (Intent, Coverage, Age, Tobacco, State, Price calculation, Lead Form) that completely locks the free-text input until explicitly needed.
* **Fuzzy Logic Validation:** In Step 5, it uses Levenshtein distance filtering (`isCaliforniaInput()`) to accept "CA", "Cali", "Calfornia" (typos) while rejecting "NY", "Texas", etc. Non-CA users are hit with a soft rejection.
* **API Rate Limiting:** Users get exactly 3 free-chat RAG queries. Once exhausted, the chat locks permanently, and an inline popup forces a "📅 Schedule 10-min Call" (Calendly bypass).
* **Bilingual Support (EN/ES):** Full toggling capability. Uses a `confirm()` dialog; if accepted, it *completely wipes all state* to prevent cross-language context bleed.

### The Knowledge Base (`knowledge/`)
9 JSON files containing dictionaries of responses, scripts, FAQs, and objections:
* `agency.json` / `products.json` / `pricing.json` / `faq.json` / `compliance.json`
* **`scripts.json`:** The step-by-step UI script.
* **`hooks.json`:** Psychological trust-builders and conversational filler.
* **`objections.json`:** Deterministic keyword triggers for things like "Too expensive", pre-empting the LLM RAG search entirely.

---

## 3. Critical Fixes Applied in the Final Sessions
A rigorous testing phase uncovered several bugs, which have all been fixed:

1. **RAG JSON Dumping Bug:** The backend was occasionally regurgitating raw `definition_en: "..."` keys instead of prose. 
   - *Fix:* Created a `.env` file and injected actual API keys (`GROQ_API_KEY`, etc.). The root cause was that API keys were missing inside Docker, causing the LLM to fail silently and fall back to dumping raw ChromaDB chunks. Also updated `generator.py` so that if API keys *do* fail, it returns a clean bilingual error message instead of raw JSON.
2. **Missing Spanish Translations:** RAG was outputting English field names while answering in Spanish.
   - *Fix:* Added all missing `_es` translations (e.g., `key_benefit_es`, `disclaimer_es`) into `knowledge.json` and `pricing.json`.
3. **"Chat More" Loophole:** The 3-Chat Limiter originally supplied a "Chat More" button that bypassed the restriction. 
   - *Fix:* Removed the "Chat More" option. Once 3 chats are burned, the *only* option is Calendly. 
4. **Ghost Language State Bug:** Switching the language from EN to ES mid-chat previously caused weird mixed-language responses. 
   - *Fix:* `setLang()` in `demo/index.html` now thoroughly resets all variables (`STEP`, `freeTextCount`, `ANSWERS`) and wipes the `MSGS.innerHTML` so the chat restarts clean.

---

## 4. Current Deployment & Run State
* **API Keys:** API keys are set in the `.env` file (`GROQ_API_KEY=...` and `OPENROUTER_API_KEY=...`).
* **To build & run:** `docker-compose down ; docker-compose up --build -d`
* **Test the Prototype:** Open `http://localhost:8080/demo/index.html` (the Nginx container).

## 5. NEXT STEPS: IMMEDIATE TASK HANDOFF
The user wants to completely redesign the pure HTML/JS prototype (`demo/index.html`) to be a **Full HD (1920x1080) 2-column layout**.
* Right now it's a mobile-style centered chat window. 
* It needs to become a split view:
  * **Left Panel:** Agency branding (Logo), Contact Info, Services offered, and Trust/Compliance details, anchored to the top left.
  * **Right Panel:** The exact same existing chat flow, but styled with deep, premium **Glassmorphism** (frosted glass over solid black backgrounds with glowing gold borders) as specified in `lovable_frontend_prompt.md`.
* **CRITICAL CONSTRAINT FOR NEXT LLM:** You must rewrite the CSS and HTML structure of `demo/index.html` to achieve this 1920x1080 layout, but you MUST preserve the 500+ lines of JavaScript at the bottom of the file absolutely verbatim. Do not change the underlying logic of the 7-step flow, the webhook fetch, or the fuzzy state matcher.
