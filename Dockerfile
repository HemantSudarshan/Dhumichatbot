# syntax=docker/dockerfile:1
# ─────────────────────────────────────────────────────────────
#  Intermarq Agency — RAG Backend
#  Multi-stage build: keeps the final image lean (~500 MB)
# ─────────────────────────────────────────────────────────────

# ── Stage 1: Builder ──────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build deps (needed by chromadb / sentence-transformers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ && \
    rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: Runtime ──────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy source code
COPY app/ ./app/
COPY knowledge/ ./knowledge/
COPY demo/ ./demo/

# Create mlruns dir (mounted as volume in compose)
RUN mkdir -p /app/mlruns

# Non-root user for security
RUN addgroup --system intermarq && adduser --system --ingroup intermarq intermarq
USER intermarq

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MLFLOW_TRACKING_URI=/app/mlruns \
    PORT=8000

CMD python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
