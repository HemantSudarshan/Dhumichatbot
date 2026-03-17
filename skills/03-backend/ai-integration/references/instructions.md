# AI Integration — Agent Instructions

## Execution Instructions

### Step 1 — Determine Serving Pattern

1. Ask the user:
   - "What does the model do? (classify, generate, retrieve)"
   - "What's the expected latency requirement?"
   - "Who consumes this API? (frontend, mobile, backend service)"
2. Apply the serving pattern decision matrix from SKILL.md Phase 1.
3. Present recommendation. Wait for confirmation.

### Step 2 — Design the API

1. Define endpoints:
   - `GET /health` — always required
   - `POST /v1/predict` — main inference endpoint
   - Additional endpoints as needed
2. Create Pydantic request/response models.
3. Implement proper error handling with HTTP status codes:
   - 200: Success
   - 400: Bad request (invalid input)
   - 422: Validation error
   - 429: Rate limited
   - 500: Internal error
   - 503: Model not ready

### Step 3 — Implement the API

1. Use the FastAPI template from SKILL.md Phase 2.
2. Implement model loading in the lifespan handler.
3. Add structured logging.
4. Add CORS middleware if frontend consumers.
5. Add rate limiting if needed.

### Step 4 — Containerize

1. Write multi-stage Dockerfile (SKILL.md Phase 3).
2. Write docker-compose.yml for local development.
3. Test the container:
   ```bash
   docker build -t service-name .
   docker run -p 8000:8000 service-name
   curl http://localhost:8000/health
   ```
4. Verify health check passes.

### Step 5 — Generate API Contract

1. Start the FastAPI app to auto-generate OpenAPI spec.
2. Export: `curl http://localhost:8000/openapi.json > openapi.json`
3. Review the spec for completeness.
4. Version the spec file.

### Step 6 — Write Integration Documentation

1. Use the template from SKILL.md Phase 5.
2. Write code examples in 3 languages: cURL, Python, JavaScript.
3. Document every endpoint, error code, and rate limit.
4. Add a changelog section.

### Step 7 — Write Integration Tests

1. Use the test template from SKILL.md Phase 6.
2. Cover:
   - Valid inputs → correct predictions
   - Empty/invalid inputs → proper error responses
   - Health endpoint → 200 OK
   - Rate limiting → 429 when exceeded
3. Run: `pytest tests/test_integration.py -v`

## Interaction Protocol

| Situation | Agent Behavior |
|-----------|---------------|
| Serving pattern unclear | Ask about latency needs and consumer type |
| Model too large for container | Recommend external model storage + download at startup |
| Frontend needs SDK | Generate from OpenAPI spec |
| API latency too high | Profile and recommend optimization (caching, batching) |

## Handoff to Other Skills

- If model needs optimization → `finetuning` skill
- If performance under load is a concern → `ai-reliability` skill
- If API docs need enhancement → `documentation` skill
