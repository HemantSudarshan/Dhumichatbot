# syntax=docker/dockerfile:1
# ─────────────────────────────────────────────────────────────
#  Intermarq Agency — RAG Backend
#  Target image size: < 2 GB (fits Railway free 4 GB limit)
# ─────────────────────────────────────────────────────────────

# ── Stage 1: Builder ──────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build deps (needed by chromadb / sentence-transformers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ && \
    rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .

# Install CPU-only PyTorch FIRST (~300 MB vs ~2.1 GB for full GPU version)
# This is the single biggest image size reduction for a CPU-only cloud deployment
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install \
        torch --index-url https://download.pytorch.org/whl/cpu

# Install remaining requirements (sentence-transformers will use the CPU torch above)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt && \
    # Pre-download the embedding model so runtime doesn't need internet access
    PYTHONPATH=/install/lib/python3.11/site-packages \
    HF_HOME=/install/hf_cache \
    python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"


# ── Stage 2: Runtime ──────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed packages + pre-downloaded model from builder
COPY --from=builder /install /usr/local

# Copy source code and static files only
COPY app/ ./app/
COPY knowledge/ ./knowledge/
COPY demo/ ./demo/

# Create dirs for volumes
RUN mkdir -p /app/mlruns /app/chroma_db

# Non-root user for security
RUN addgroup --system intermarq && adduser --system --ingroup intermarq intermarq
USER intermarq

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MLFLOW_TRACKING_URI=/app/mlruns \
    HF_HOME=/usr/local/hf_cache \
    TRANSFORMERS_OFFLINE=1 \
    PORT=8000

CMD python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
