---
name: ai-integration
description: "Use this skill when tasked with exposing an ML model as an API, containerizing an AI application, creating API contracts and OpenAPI specs, writing integration documentation for frontend/product teams, or helping developers consume AI services via REST, streaming, or batch endpoints."
---

# AI Integration with Applications

## Overview

This skill bridges the gap between data science and application engineering — taking a trained ML model and making it available as a production API with documentation, containers, and integration guides.

## Supporting References

Load only the reference file you need:
- `references/instructions.md` for the execution sequence and handoff protocol
- `references/debug.md` for API, payload, and serving diagnostics
- `references/tests.md` for endpoint validation and integration scenarios

## Required Inputs

1. **Model** — trained model path or API endpoint
2. **Serving pattern** — sync API, async, streaming, or batch
3. **Consumers** — who will call this API? (frontend, mobile, internal service)
4. **Non-functional requirements** — latency SLA, throughput, auth method

## Step-by-Step Workflow

### Phase 1 — Serving Pattern Selection

**Decision Matrix**:

| Pattern | Use When | Latency | Complexity |
|---------|----------|---------|------------|
| **Sync REST** | Request-response, <5s inference | Low | Low |
| **Async (Queue)** | Heavy processing, >10s inference | High | Medium |
| **Streaming (SSE)** | LLM text generation, token-by-token | Progressive | Medium |
| **WebSocket** | Bidirectional, real-time conversation | Low | High |
| **Batch** | Bulk processing, overnight jobs | N/A | Low |

**Rules**:
- Default to Sync REST unless there's a specific reason not to
- Use SSE for any LLM text generation endpoint
- Use async for inference > 10 seconds
- Use batch for > 1000 items to process

---

### Phase 2 — API Design & Implementation

**FastAPI Template** (Sync REST):
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

# --- Schemas ---
class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000,
                      description="Input text for prediction")

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float = Field(ge=0.0, le=1.0)
    model_version: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str

# --- Application ---
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = load_model("path/to/model")
    yield
    del model

app = FastAPI(
    title="AI Prediction API",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        version="1.0.0"
    )

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        result = model.predict(request.text)
        return PredictionResponse(
            prediction=result["label"],
            confidence=result["score"],
            model_version="1.0.0"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Streaming Template** (SSE for LLM):
```python
from fastapi.responses import StreamingResponse
import asyncio

@app.post("/generate")
async def generate(request: GenerationRequest):
    async def stream_tokens():
        for token in model.generate_stream(request.prompt):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        stream_tokens(),
        media_type="text/event-stream"
    )
```

**Rules**:
- Every endpoint has Pydantic request AND response models
- Every endpoint returns structured error responses
- Health check endpoint is mandatory (`/health`)
- API versioning via URL prefix (`/v1/predict`)

---

### Phase 3 — Containerization

**Multi-Stage Dockerfile**:
```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY src/ ./src/
COPY configs/ ./configs/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Docker Compose** (local dev):
```yaml
version: "3.8"
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/models/model.pt
      - LOG_LEVEL=info
    volumes:
      - ./models:/models
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]  # For GPU support
```

---

### Phase 4 — API Contract Specification

1. Auto-generate OpenAPI spec from FastAPI:
   - Available at `/docs` (Swagger UI) and `/openapi.json`
2. Export and version the spec:
   ```bash
   curl http://localhost:8000/openapi.json > openapi-v1.0.0.json
   ```
3. Generate client SDKs (optional):
   ```bash
   npx @openapitools/openapi-generator-cli generate \
       -i openapi.json -g python -o sdk/python
   ```

---

### Phase 5 — Integration Documentation

**Template** (`integration_guide.md`):

```markdown
# [Service Name] Integration Guide

## Quick Start
1. Get an API key from [admin]
2. Base URL: `https://api.example.com/v1`
3. Make your first request:

### cURL
curl -X POST https://api.example.com/v1/predict \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'

### Python
import requests
response = requests.post(
    "https://api.example.com/v1/predict",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={"text": "Hello world"}
)
print(response.json())

### JavaScript
const response = await fetch('https://api.example.com/v1/predict', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ text: 'Hello world' })
});

## Endpoints
## Error Codes
## Rate Limits
## Changelog
```

---

### Phase 6 — Integration Testing

```python
import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_predict_valid_input():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/predict", json={"text": "test"})
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "confidence" in data
    assert 0 <= data["confidence"] <= 1

@pytest.mark.asyncio
async def test_predict_empty_input():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/predict", json={"text": ""})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

---

## Anti-Patterns — DO NOT

| Anti-Pattern | Consequence | Correct Approach |
|-------------|-------------|------------------|
| Load model on every request | Extreme latency | Load once at startup (lifespan) |
| Return raw exception traces to API consumers | Security risk | Return structured error responses |
| Skip API versioning | Breaking changes affect all consumers | Version from day 1 (/v1/) |
| Hardcode model path | Cannot deploy to different environments | Use environment variables |
| No rate limiting | DDoS / cost explosion | Add rate limiting middleware |
| Skip health check endpoint | Cannot monitor service | Always implement /health |

## Skill Coordination

- Use `ai-solution-dev` when API integration is only one part of a larger solution build.
- Use `finetuning` if the model itself must be adapted before serving.
- Use `data-pipeline` when request preprocessing or evaluation pipelines need deeper treatment.
- Use `ai-reliability` for observability, scaling, and production readiness work after integration.
- Use `documentation` to generate integration guides, API docs, and runbooks.
