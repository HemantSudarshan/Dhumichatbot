# Data Flow Diagram — California Insurance Chatbot

## Full Pipeline: Sources → Normalization → Chatbot

```mermaid
flowchart TD
    %% ─── SOURCE LAYER ───────────────────────────────────────
    subgraph SOURCES["📂 SOURCE LAYER (Raw Inputs)"]
        direction TB
        A1["CHATBOT SUGGESTIONS INTERMARQ.docx\n(Conversation flow, scripts, objections)"]
        A2["US California Insurance Overview.md\n(CA regulations, product types)"]
        A3["Research Answers 1–14 (.txt)\n(14 files — pricing, compliance, scripts,\n CA rules, edge cases, roadmap)"]
        A4["complete_knowledge_base.md\n(Compiled master reference — all parts)"]
        A5["External: Bitext / Common Crawl\n(NLP training data for intent matching)"]
        A6["External: Data.gov / Nasdaq\n(Regulatory & financial reference data)"]
        A7["Synthetic: MOSTLY AI / Gretel\n(Privacy-compliant test lead data)"]
    end

    %% ─── BRONZE LAYER ───────────────────────────────────────
    subgraph BRONZE["🟤 BRONZE LAYER (Raw Ingest)"]
        direction TB
        B1["Read files as-is\n(UTF-8, no transformation)"]
        B2["Store raw bytes + metadata\n(filename, size, timestamp)"]
        B3["No modification — exact copy\nof all source documents"]
    end

    %% ─── SILVER LAYER ───────────────────────────────────────
    subgraph SILVER["⚪ SILVER LAYER (Clean & Normalize)"]
        direction TB
        C1["Deduplicate identical lines"]
        C2["Normalize whitespace\n(strip noise, collapse blank lines)"]
        C3["Schema validation\n(field types, required fields)"]
        C4["Business rule enforcement\n(age ranges valid, prices positive)"]
        C5["ACORD field mapping\n(map chatbot fields → TXLife schema)"]
    end

    %% ─── GOLD LAYER ─────────────────────────────────────────
    subgraph GOLD["🟡 GOLD LAYER (Business-Ready JSON)"]
        direction TB
        D1["products.json\n4 products with selling points,\nscripts, CA scenarios"]
        D2["scripts.json\nAll prompts, responses,\nobjections, button labels"]
        D3["compliance.json\nSB 263, Prop 103, CIC 10509,\nCLHIGA limits, disclosures"]
        D4["pricing.json\nAge-band rate ranges,\ntobacco multiplier, disclaimers"]
        D5["faq.json\n12 Q&A pairs with\ncategories and keywords"]
        D6["ChromaDB / rag_store\nParent-child embedded chunks\n(sentence-transformers)"]
    end

    %% ─── ACORD NORMALIZATION ──────────────────────────────
    subgraph ACORD["📋 ACORD NORMALIZATION"]
        direction TB
        E1["TXLife 103\nNew Business Submission\n(Lead → Carrier JSON payload)"]
        E2["TXLife 228\nProducer Inquiry\n(Agent license verification)"]
    end

    %% ─── STREAMING LAYER ─────────────────────────────────
    subgraph STREAM["🚀 STREAMING API (FastAPI)"]
        direction TB
        F1["GET /stream/source/{name}\n→ raw research docs\n(512-byte chunks)"]
        F2["GET /stream/knowledge/{name}\n→ Gold Layer JSON\n(512-byte chunks)"]
        F3["GET /rag/query?q=...\n→ ChromaDB semantic search\n(top-3 results)"]
        F4["GET /knowledge/{name}\n→ structured JSON\n(full file)"]
    end

    %% ─── CHATBOT ─────────────────────────────────────────
    subgraph CHATBOT["💬 CHATBOT ENGINE"]
        direction TB
        G1["State Machine\n(7-step DOCX flow)"]
        G2["Lead Scoring\n(5-factor weighted model)"]
        G3["RAG Retrieval\n(open Q&A fallback)"]
        G4["ACORD Serializer\n(TXLife 103 lead payload)"]
        G5["CRM / Agent Routing"]
    end

    %% ─── CONNECTIONS ─────────────────────────────────────
    A1 & A2 & A3 & A4 --> B1
    A5 & A6 & A7 --> B1
    B1 --> B2 --> B3

    B3 --> C1 --> C2 --> C3 --> C4 --> C5

    C5 --> D1
    C5 --> D2
    C5 --> D3
    C5 --> D4
    C5 --> D5
    C5 --> D6

    D3 --> E1
    D3 --> E2

    D1 & D2 & D3 & D4 & D5 --> F2
    A1 & A2 & A3 & A4 --> F1
    D6 --> F3
    D1 & D2 & D4 & D5 --> F4

    F2 --> G1
    F4 --> G2
    F3 --> G3
    E1 --> G4
    E2 --> G4
    G1 & G2 & G3 --> G4 --> G5
```

---

## ACORD Normalization Detail

```mermaid
flowchart LR
    subgraph CHATBOT_INPUT["Chatbot Collected Fields"]
        I1["coverage_type\ne.g. mortgage_protection"]
        I2["coverage_amount\ne.g. $250,000"]
        I3["age_range\ne.g. 30-39"]
        I4["tobacco_use\ne.g. No"]
        I5["homeowner\ne.g. Yes with mortgage"]
        I6["name / email / phone\n(lead capture step)"]
        I7["state = CA"]
    end

    subgraph ACORD103["TXLife 103 — New Business Submission"]
        O1["party.person\n→ age_range, tobacco_use"]
        O2["party.address\n→ state=CA, zip"]
        O3["party.contact\n→ full_name, email, phone"]
        O4["coverage_request\n→ product_type, face_amount,\nhomeowner_status"]
        O5["metadata\n→ lead_score, session_id,\ntimestamp, channel"]
    end

    subgraph ACORD228["TXLife 228 — Producer Inquiry"]
        P1["inquiry_type\n= Agent License Verification"]
        P2["checks\n= state_appointments,\nlicense_status, SB263_training"]
        P3["action_if_non_compliant\n= auto_reassign"]
    end

    I1 --> O4
    I2 --> O4
    I3 --> O1
    I4 --> O1
    I5 --> O4
    I6 --> O3
    I7 --> O2

    O1 & O2 & O3 & O4 & O5 --> CARRIER["Carrier System\n(straight-through processing)"]

    AGENT["Agent Assignment"] --> P1 --> P2 --> P3 --> CARRIER
```

---

## RAG Chunking Flow

```mermaid
flowchart TD
    RAW["Source Documents\n(.md, .txt)"]

    RAW --> SPLIT["Split by Markdown Headers\n(H1 / H2 / H3)"]
    SPLIT --> PARENT["Parent Chunks\n(~2000 chars = full section)"]
    PARENT --> CHILD["Child Chunks\n(~400 chars = individual clause)"]

    RAW2["compliance.json\nfaq.json"]
    RAW2 --> DECOMP["Structured Decomposition\n(each rule / Q&A → plain text)"]
    DECOMP --> MICRO["Micro Chunks\n(~50–100 chars per rule)"]

    CHILD & MICRO --> EMBED["sentence-transformers\nall-MiniLM-L6-v2\n(384-dim vectors)"]
    EMBED --> CHROMA["ChromaDB\nrag_store/chroma.sqlite3\nParent–Child linked"]

    QUERY["User Question"] --> EMBED2["Query Embedding"]
    EMBED2 --> CHROMA
    CHROMA --> TOPK["Top-3 Relevant Chunks\n+ Parent Context"]
    TOPK --> LLM["Chatbot Response\n(grounded in your data)"]
```

---

## Summary Table

| Layer | Script | Input | Output |
|-------|--------|-------|--------|
| **Bronze** | *(implicit in 02)* | Raw files as-is | In-memory text |
| **Silver** | `02_data_pipeline.py` | Raw text | Cleaned, deduplicated text |
| **Gold** | `02_data_pipeline.py` | Silver text | `knowledge/*.json` (5 files) |
| **RAG** | `03_build_rag_index.py` | Gold JSON + source .md | `rag_store/chroma.sqlite3` |
| **ACORD** | `acord_normalizer.py` *(next)* | Chatbot lead fields | TXLife 103/228 JSON payload |
| **Stream** | `04_stream_server.py` | All Gold + Source | HTTP streaming API (port 8001) |
