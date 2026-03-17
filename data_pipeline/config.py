"""
config.py — Shared paths and settings for all data pipeline scripts.
"""
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# PROJECT ROOTS
# ─────────────────────────────────────────────────────────────

# Project root = parent of this data_pipeline/ folder
PROJECT_ROOT = Path(__file__).parent.parent

# This folder
PIPELINE_DIR = Path(__file__).parent

# ─────────────────────────────────────────────────────────────
# SOURCE FILES (Bronze Layer — raw research docs)
# ─────────────────────────────────────────────────────────────

SOURCE_FILES = {
    "complete_knowledge_base":  PROJECT_ROOT / "complete_knowledge_base.md",
    "ca_insurance_overview":    PROJECT_ROOT / "us calfornia insurance.md",
    "research_answer_1":        PROJECT_ROOT / "Research Question and Answers" / "1.txt",
    "research_answer_2":        PROJECT_ROOT / "Research Question and Answers" / "2.txt",
    "research_answer_3":        PROJECT_ROOT / "Research Question and Answers" / "3.txt",
    "research_answer_4":        PROJECT_ROOT / "Research Question and Answers" / "4.txt",
    "research_answer_567":      PROJECT_ROOT / "Research Question and Answers" / "5,6,7.txt",
    "research_answer_8910":     PROJECT_ROOT / "Research Question and Answers" / "8,9,10.txt",
    "research_answer_111213":   PROJECT_ROOT / "Research Question and Answers" / "11 12 13.txt",
    "research_answer_14":       PROJECT_ROOT / "Research Question and Answers" / "14.txt",
}

# Primary knowledge source — used for ETL and RAG
PRIMARY_KB_FILE = SOURCE_FILES["complete_knowledge_base"]

# Files to include in RAG index
RAG_SOURCE_FILES = [
    SOURCE_FILES["complete_knowledge_base"],
    SOURCE_FILES["ca_insurance_overview"],
    SOURCE_FILES["research_answer_3"],   # CA compliance section
    SOURCE_FILES["research_answer_4"],   # Scripts and flow
    SOURCE_FILES["research_answer_8910"], # Pricing
]

# ─────────────────────────────────────────────────────────────
# OUTPUT DIRS (Gold Layer)
# ─────────────────────────────────────────────────────────────

KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
RAG_STORE_DIR = PROJECT_ROOT / "rag_store"

KNOWLEDGE_DIR.mkdir(exist_ok=True)
RAG_STORE_DIR.mkdir(exist_ok=True)

# Gold Layer JSON files
KNOWLEDGE_FILES = {
    "products":    KNOWLEDGE_DIR / "products.json",
    "scripts":     KNOWLEDGE_DIR / "scripts.json",
    "compliance":  KNOWLEDGE_DIR / "compliance.json",
    "pricing":     KNOWLEDGE_DIR / "pricing.json",
    "faq":         KNOWLEDGE_DIR / "faq.json",
}

# Check report output
CHECK_REPORT_FILE = PIPELINE_DIR / "check_report.json"

# ─────────────────────────────────────────────────────────────
# RAG SETTINGS
# ─────────────────────────────────────────────────────────────

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_COLLECTION_NAME = "insurance_knowledge"
CHROMA_PERSIST_DIR = str(RAG_STORE_DIR)

# Parent-child chunk sizes (in characters)
PARENT_CHUNK_SIZE = 2000   # ~500 tokens — full section
CHILD_CHUNK_SIZE  = 400    # ~100 tokens — individual clause
CHUNK_OVERLAP     = 50     # overlap between chunks to avoid context loss

# Number of results to retrieve per query
RAG_TOP_K = 3

# ─────────────────────────────────────────────────────────────
# SERVER SETTINGS
# ─────────────────────────────────────────────────────────────

API_HOST = "0.0.0.0"
API_PORT = 8001
STREAM_CHUNK_SIZE = 512   # bytes per streaming chunk

# ─────────────────────────────────────────────────────────────
# EXTERNAL DATA SOURCES
# ─────────────────────────────────────────────────────────────

EXTERNAL_DATA_DIR = PIPELINE_DIR / "external_data"
EXTERNAL_DATA_DIR.mkdir(exist_ok=True)

# STAG dual-store output
VECTOR_KNOWLEDGE_DIR     = KNOWLEDGE_DIR / "vector"
RELATIONAL_KNOWLEDGE_DIR = KNOWLEDGE_DIR / "relational"
VECTOR_KNOWLEDGE_DIR.mkdir(exist_ok=True)
RELATIONAL_KNOWLEDGE_DIR.mkdir(exist_ok=True)

# External source URLs (all free, no API keys needed for MVP)
EXTERNAL_SOURCES = {
    "ca_insurance": {
        "url": "https://data.ca.gov/api/3/action/package_search?q=insurance&rows=50",
        "description": "California open data — insurance datasets",
        "format": "json",
    },
    "fred_insurance_cpi": {
        "url": "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=CUUR0000SEMD01&scale=left&cosd=2020-01-01&coed=2025-12-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2026-03-16&revision_date=2026-03-16&nd=1997-12-01",
        "description": "FRED — Life insurance premium CPI index (CUUR0000SEMD01)",
        "format": "csv",
    },
    "census_ca_housing": {
        "url": "https://api.census.gov/data/2022/acs/acs5?get=NAME,B25003_001E,B25003_002E,B25003_003E,B19013_001E&for=county:*&in=state:06",
        "description": "US Census ACS 5yr — CA counties: total housing, owners, renters, median income",
        "format": "json",
    },
    "common_crawl": {
        "url": "https://index.commoncrawl.org/CC-MAIN-2024-51-index?url=*.insurance.ca.gov&output=json&limit=50",
        "description": "Common Crawl — CA DOI website page index",
        "format": "jsonl",
    },
    "stack_exchange": {
        "url": "https://api.stackexchange.com/2.3/search?order=desc&sort=votes&tagged=insurance&site=money&pagesize=30&filter=withbody",
        "description": "Stack Exchange Money.SE — top insurance Q&A",
        "format": "json",
    },
}

# Bitext-style synthetic data (generated locally, no API)
BITEXT_OBJECTION_TEMPLATES = {
    "already_have_insurance": [
        "I already have life insurance",
        "I'm covered already", "I have a policy",
        "My employer provides coverage", "I got insurance through work",
    ],
    "just_looking": [
        "I'm just looking", "Just browsing", "Not ready to buy",
        "I'm just exploring options", "Just doing research",
    ],
    "too_expensive": [
        "It's too expensive", "I can't afford it",
        "Insurance costs too much", "That's out of my budget",
    ],
    "not_interested": [
        "I'm not interested", "No thanks", "Maybe later",
        "I don't need this right now", "Not for me",
    ],
    "need_to_think": [
        "I need to think about it", "Let me discuss with my spouse",
        "I'll get back to you", "Need more time to decide",
    ],
}

# OPA / Rego compliance rule IDs
OPA_RULES = {
    "cic_10509": "CIC Section 10509 — Replacement rule disclosure",
    "sb_263":    "SB 263 — Suitability in annuity transactions",
    "clhiga":    "CLHIGA — CA Life & Health Insurance Guarantee Association limits",
    "prop_103":  "Proposition 103 — Rate approval and consumer protection",
}
