# AI Integration — Test Cases

---

## Test 1 — Basic API Creation

**Input**:
```
Expose my sentiment analysis model as a REST API.
Model accepts text, returns: label (positive/negative/neutral) and confidence score.
```

**Expected Behavior**:
1. Agent creates FastAPI app with `/predict` endpoint.
2. Pydantic models for request (text) and response (label, confidence).
3. Health check at `/health`.
4. Dockerfile + docker-compose.yml.
5. OpenAPI spec auto-generated.

**Pass Criteria**:
- [ ] API returns valid predictions with confidence scores
- [ ] Invalid inputs return 422 with clear message
- [ ] Health endpoint works
- [ ] Docker container builds and runs
- [ ] OpenAPI spec is complete

---

## Test 2 — Integration Documentation

**Input**:
```
Create integration documentation for our prediction API.
Consumers: React frontend team and mobile team.
```

**Expected Behavior**:
1. Agent produces `integration_guide.md`.
2. Includes code examples in cURL, Python, JavaScript.
3. Documents all endpoints with request/response examples.
4. Includes error codes and troubleshooting.

**Pass Criteria**:
- [ ] Code examples are runnable
- [ ] All endpoints documented
- [ ] Error codes listed
- [ ] Guide is understandable by frontend developers

---

## Test 3 — GPU Container

**Input**:
```
Containerize my LLM application. It requires a GPU with 16GB VRAM.
Using vLLM for serving.
```

**Expected Behavior**:
1. Agent creates Dockerfile with NVIDIA CUDA base image.
2. docker-compose.yml with GPU resource reservation.
3. vLLM serving configuration.
4. Model download/loading strategy.

**Pass Criteria**:
- [ ] Dockerfile uses CUDA base image
- [ ] GPU access configured in docker-compose
- [ ] Health check includes GPU availability
- [ ] Model loading strategy documented

---

## Test 4 — Streaming Endpoint

**Input**:
```
Add a streaming endpoint for our text generation model.
Frontend needs Server-Sent Events (SSE).
```

**Expected Behavior**:
1. Agent creates `/generate` endpoint with StreamingResponse.
2. SSE format with proper `data:` prefixes.
3. `[DONE]` sentinel at end of stream.
4. Frontend consumption example (JavaScript EventSource).

**Pass Criteria**:
- [ ] SSE format is correct
- [ ] Stream terminates properly
- [ ] Frontend example works
- [ ] Error handling during streaming

---

## Test 5 — API Versioning

**Input**:
```
We need to add a v2 endpoint that returns embeddings in addition to predictions.
v1 must continue working.
```

**Expected Behavior**:
1. Agent creates `/v2/predict` with extended response schema.
2. `/v1/predict` remains unchanged.
3. OpenAPI spec includes both versions.
4. Migration guide for consumers.

**Pass Criteria**:
- [ ] v1 endpoint unchanged
- [ ] v2 endpoint includes embeddings
- [ ] Both versions documented
- [ ] Migration guide provided
