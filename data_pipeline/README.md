# Data Pipeline — California Insurance Chatbot

This folder contains **all data engineering scripts** for the chatbot.
Run them in order (01 → 02 → 03 → 04) to go from raw research docs to a fully indexed, streamable knowledge base.

---

## Folder Structure

```
data_pipeline/
├── README.md               ← You are here
├── requirements.txt        ← Install these first
│
├── 01_check_sources.py     ← STEP 1: Verify all source files exist and are readable
├── 02_data_pipeline.py     ← STEP 2: Medallion ETL → outputs knowledge/ JSON files
├── 03_build_rag_index.py   ← STEP 3: Chunk + embed knowledge docs → ChromaDB store
├── 04_stream_server.py     ← STEP 4: FastAPI server to test streaming access via API
│
└── config.py               ← Shared paths and settings for all scripts
```

---

## Prerequisites

```bash
pip install -r data_pipeline/requirements.txt
```

---

## Run Order

```bash
# Step 1 — Check all source files are accessible
python data_pipeline/01_check_sources.py

# Step 2 — Run Medallion ETL (Bronze → Silver → Gold)
# Reads: complete_knowledge_base.md, research answers, DOCX text
# Writes: knowledge/products.json, scripts.json, compliance.json, pricing.json, faq.json
python data_pipeline/02_data_pipeline.py

# Step 3 — Build RAG index (parent-child chunking + embeddings)
# Reads: complete_knowledge_base.md, us calfornia insurance.md, knowledge/*.json
# Writes: rag_store/chroma.sqlite3
python data_pipeline/03_build_rag_index.py

# Step 4 — Start streaming API server to test all data access
# Open: http://localhost:8001/docs
python data_pipeline/04_stream_server.py
```

---

## What Each Script Produces

| Script | Output | Location |
|--------|--------|----------|
| `01_check_sources.py` | Console report + `check_report.json` | `data_pipeline/` |
| `02_data_pipeline.py` | 5 Gold Layer JSON files | `knowledge/` |
| `03_build_rag_index.py` | ChromaDB vector store | `rag_store/` |
| `04_stream_server.py` | REST + streaming API (port 8001) | Runtime only |

---

## Medallion Architecture

```
BRONZE (raw)    →    SILVER (clean)    →    GOLD (structured)
  source docs          deduplicated          products.json
  research txt         schema-validated      scripts.json
  DOCX text            ACORD-mapped          compliance.json
  PDF content          business rules        pricing.json
                                             faq.json
                                             ChromaDB (RAG)
```
