"""
Embed all knowledge JSON files into ChromaDB.

Chunking strategy: each JSON object is a natural semantic chunk.
Metadata includes source file, chunk ID, category, and keywords.

Usage:
    python -m app.rag.embed_knowledge
"""

import json
import os
import chromadb
from sentence_transformers import SentenceTransformer

# ── Config ──────────────────────────────────────────────
KNOWLEDGE_DIR = os.environ.get("KNOWLEDGE_DIR",
    os.path.join(os.path.dirname(__file__), "..", "..", "knowledge"))
CHROMA_DIR = os.environ.get("CHROMA_PERSIST_DIR",
    os.path.join(os.path.dirname(__file__), "..", "chroma_db"))
MODEL_NAME = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


# Only allow known knowledge files (prevent path traversal via env var)
ALLOWED_FILES = {
    "scripts.json", "hooks.json", "objections.json", "pricing.json",
    "compliance.json", "faq.json", "products.json", "knowledge.json", "agency.json",
}


def load_json(filename: str) -> dict | list:
    """Load a JSON file with UTF-8 encoding. Restricted to ALLOWED_FILES."""
    if filename not in ALLOWED_FILES:
        raise ValueError(f"File not in allowlist: {filename}")
    knowledge_dir = os.path.realpath(KNOWLEDGE_DIR)
    path = os.path.realpath(os.path.join(knowledge_dir, filename))
    # Ensure resolved path is still within the knowledge directory
    if not path.startswith(knowledge_dir):
        raise ValueError(f"Path escapes knowledge directory: {filename}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_chunks() -> list[dict]:
    """Build semantic chunks from all knowledge files."""
    chunks = []

    # ── FAQ (each entry is a chunk) ──
    faq = load_json("faq.json")
    for item in faq:
        chunks.append({
            "id": item["id"],
            "text": f"Q: {item['question']}\nA: {item['answer']}",
            "metadata": {
                "source": "faq.json",
                "category": item.get("category", "general"),
                "keywords": ", ".join(item.get("keywords", [])),
            }
        })

    # ── Products (each product is a chunk) ──
    products = load_json("products.json")
    for key, prod in products.items():
        if not isinstance(prod, dict) or "name" not in prod:
            continue
        text_parts = [
            f"Product: {prod['name']}",
            f"Description: {prod.get('description', '')}",
        ]
        if "selling_points" in prod:
            text_parts.append("Key benefits: " + "; ".join(prod["selling_points"]))
        if "education_script" in prod:
            text_parts.append(f"Education: {prod['education_script']}")
        if "ca_scenario" in prod:
            text_parts.append(f"California example: {prod['ca_scenario']}")

        chunks.append({
            "id": f"product_{key}",
            "text": "\n".join(text_parts),
            "metadata": {"source": "products.json", "category": key, "keywords": key},
        })

    # ── Compliance (each regulation/disclosure is a chunk) ──
    compliance = load_json("compliance.json")
    for key, reg in compliance.get("regulations", {}).items():
        text = f"Regulation: {reg.get('name', key)}\n"
        if "requires" in reg:
            text += "Requires: " + ", ".join(reg["requires"]) + "\n"
        if "description" in reg:
            text += reg["description"] + "\n"
        chunks.append({
            "id": f"regulation_{key}",
            "text": text,
            "metadata": {"source": "compliance.json", "category": "regulation", "keywords": key},
        })
    for key, disc in compliance.get("disclosures", {}).items():
        chunks.append({
            "id": f"disclosure_{key}",
            "text": f"{key.replace('_', ' ').title()}: {disc}",
            "metadata": {"source": "compliance.json", "category": "disclosure", "keywords": key},
        })

    # ── Knowledge (education + pricing references) ──
    knowledge = load_json("knowledge.json")
    if "education" in knowledge:
        for key, edu in knowledge["education"].items():
            if isinstance(edu, dict):
                text = f"{key.replace('_', ' ').title()}\n"
                for k, v in edu.items():
                    if isinstance(v, str):
                        text += f"{k}: {v}\n"
                chunks.append({
                    "id": f"education_{key}",
                    "text": text,
                    "metadata": {"source": "knowledge.json", "category": "education", "keywords": key},
                })

    # ── Pricing (one chunk for the table) ──
    pricing = load_json("pricing.json")
    pricing_text = f"Pricing disclaimer: {pricing['_meta']['disclaimer']}\n"
    mp = pricing.get("mortgage_protection", {})
    if "docx_verified_example" in mp:
        ex = mp["docx_verified_example"]
        pricing_text += f"Example: {ex['profile']} — {ex['coverage']} coverage — {ex['range']}\n"
    if "rates_by_age_non_smoker" in mp:
        for age, rates in mp["rates_by_age_non_smoker"].items():
            for cov, price in rates.items():
                pricing_text += f"Age {age}, {cov}: {price}\n"
    pricing_text += f"Tobacco multiplier: {mp.get('tobacco_multiplier', 1.5)}\n"
    chunks.append({
        "id": "pricing_table",
        "text": pricing_text,
        "metadata": {"source": "pricing.json", "category": "pricing", "keywords": "cost,price,rate,premium"},
    })

    # ── Objections (each is a chunk) ──
    objections = load_json("objections.json")
    for key, obj in objections.items():
        chunks.append({
            "id": f"objection_{key}",
            "text": (
                f"Objection: {key.replace('_', ' ').title()}\n"
                f"Triggers: {', '.join(obj.get('triggers', []))}\n"
                f"Response: {obj.get('response_en', '')}\n"
                f"Follow-up: {obj.get('follow_up_en', 'None')}\n"
                f"Psychology: {obj.get('psychology', '')}"
            ),
            "metadata": {"source": "objections.json", "category": "objection", "keywords": key},
        })

    # ── Hooks (each is a chunk) ──
    hooks = load_json("hooks.json")
    for key, hook in hooks.items():
        chunks.append({
            "id": f"hook_{key}",
            "text": f"{key.replace('_', ' ').title()}: {hook.get('text_en', '')}",
            "metadata": {"source": "hooks.json", "category": "hook",
                         "keywords": hook.get("position", key)},
        })

    return chunks


def embed_and_store(chunks: list[dict]):
    """Embed all chunks and store in ChromaDB."""
    print(f"Loading embedding model: {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)

    print(f"Creating ChromaDB at: {CHROMA_DIR}")
    os.makedirs(CHROMA_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Delete existing collection if exists
    try:
        client.delete_collection("intermarq_knowledge")
    except Exception:
        pass

    collection = client.create_collection(
        name="intermarq_knowledge",
        metadata={"hnsw:space": "cosine"}
    )

    # Prepare batch
    ids = [c["id"] for c in chunks]
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    print(f"Embedding {len(chunks)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"\n✅ Embedded {len(chunks)} chunks into ChromaDB")
    print(f"   Collection: intermarq_knowledge")
    print(f"   Location: {CHROMA_DIR}")
    return collection


if __name__ == "__main__":
    chunks = build_chunks()
    print(f"Built {len(chunks)} chunks from knowledge files:")
    for c in chunks:
        print(f"  [{c['metadata']['source']}] {c['id']}: {c['text'][:60]}...")
    embed_and_store(chunks)
