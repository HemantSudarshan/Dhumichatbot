"""
Retriever: semantic search over ChromaDB with keyword fallback.

Implements hybrid retrieval per rag-engineer skill:
  - Vector similarity search (cosine, top-K)
  - Metadata filtering by category/source
  - Relevance threshold (discard low-confidence hits)
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
from typing import Optional

CHROMA_DIR = os.environ.get("CHROMA_PERSIST_DIR",
    os.path.join(os.path.dirname(__file__), "..", "chroma_db"))
MODEL_NAME = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Singleton instances (loaded once at startup)
_model: Optional[SentenceTransformer] = None
_collection = None


def init_retriever():
    """Initialize embedding model and ChromaDB collection. Call once at startup."""
    global _model, _collection
    _model = SentenceTransformer(MODEL_NAME)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    _collection = client.get_collection("intermarq_knowledge")
    count = _collection.count()
    print(f"✅ Retriever ready: {count} chunks in ChromaDB")
    return count


def retrieve(query: str, top_k: int = 5, threshold: float = 0.3,
             category: Optional[str] = None) -> list[dict]:
    """
    Retrieve top-K relevant chunks for a query.

    Args:
        query: User's free-text question
        top_k: Number of results to return
        threshold: Minimum similarity score (0-1, higher = more relevant)
        category: Optional category filter (faq, pricing, compliance, etc.)

    Returns:
        List of dicts with keys: id, text, source, category, score
    """
    if _model is None or _collection is None:
        raise RuntimeError("Retriever not initialized. Call init_retriever() first.")

    # Embed the query
    query_embedding = _model.encode(query).tolist()

    # Build optional filter
    where_filter = None
    if category:
        where_filter = {"category": category}

    # Query ChromaDB
    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where_filter,
        include=["documents", "metadatas", "distances"],
    )

    # Convert cosine distance to similarity score (ChromaDB returns distance)
    chunks = []
    for i, doc_id in enumerate(results["ids"][0]):
        distance = results["distances"][0][i]
        # ChromaDB cosine distance: 0 = identical, 2 = opposite
        # Convert to similarity: 1 - (distance / 2)
        similarity = 1 - (distance / 2)

        if similarity < threshold:
            continue

        chunks.append({
            "id": doc_id,
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i].get("source", "unknown"),
            "category": results["metadatas"][0][i].get("category", ""),
            "score": round(similarity, 3),
        })

    # Sort by score descending
    chunks.sort(key=lambda x: x["score"], reverse=True)
    return chunks


def get_chunk_count() -> int:
    """Return the number of chunks in the collection."""
    if _collection is None:
        return 0
    return _collection.count()
