# syntax=docker/dockerfile:1
# ─────────────────────────────────────────────────────────────
#  Intermarq Agency — RAG Backend (Lean Deploy)
#  Target: < 1.5 GB (Railway free tier limit: 4 GB)
#
#  Key optimisations:
#    - CPU-only PyTorch (~300 MB vs 2.1 GB GPU)
#    - No MLflow (telemetry falls back to console)
#    - Model downloaded at first startup, not baked in
# ─────────────────────────────────────────────────────────────

# ── Stage 1: Builder ──────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ && \
    rm -rf /var/lib/apt/lists/*

COPY app/requirements-deploy.txt ./requirements.txt

# CPU-only PyTorch first, then remaining deps
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install \
        torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: Runtime ──────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app/ ./app/
COPY knowledge/ ./knowledge/
COPY demo/ ./demo/

RUN mkdir -p /app/mlruns /app/chroma_db

RUN addgroup --system intermarq && adduser --system --ingroup intermarq intermarq
USER intermarq

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MLFLOW_TRACKING_URI=/app/mlruns \
    PORT=8000

CMD python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
