# AI Integration — Debug Protocol

## Purpose

Troubleshooting for API serving, containerization, and integration failures.

---

## Failure 1 — API Latency > 5 Seconds

**Symptom**: Prediction endpoint takes too long, consumers experience timeouts.

**Diagnostic Steps**:
1. Profile where time is spent:
   ```python
   import time
   
   t0 = time.time()
   preprocessed = preprocess(input)
   t1 = time.time()
   prediction = model.predict(preprocessed)
   t2 = time.time()
   response = format_response(prediction)
   t3 = time.time()
   
   print(f"Preprocess: {t1-t0:.3f}s")
   print(f"Inference: {t2-t1:.3f}s")
   print(f"Postprocess: {t3-t2:.3f}s")
   ```
2. Identify bottleneck (usually model inference).

**Fix Ladder**:
1. Add response caching for identical inputs (Redis/in-memory LRU)
2. Use model quantization (INT8/INT4)
3. Enable dynamic batching
4. Switch to a smaller model
5. Use GPU if on CPU (or faster GPU)
6. Implement async processing for > 10s tasks

---

## Failure 2 — Invalid Request Payloads

**Symptom**: 422 errors from Pydantic validation, or worse — 500 errors from unhandled inputs.

**Diagnostic Steps**:
1. Check the exact validation error message.
2. Verify Pydantic model constraints match API docs.
3. Test with example payloads from documentation.

**Fix**:
- Add comprehensive Pydantic validation with clear error messages
- Add `examples` to Pydantic models for OpenAPI docs
- Return structured error response:
  ```json
  {"detail": "Field 'text' must be at least 1 character", "field": "text"}
  ```
- Add input sanitization layer

---

## Failure 3 — Model Response Failures

**Symptom**: Model returns None, crashes during inference, or produces garbage output.

**Diagnostic Steps**:
1. Test model inference outside the API:
   ```python
   result = model.predict("test input")
   print(type(result), result)
   ```
2. If None → model not loaded correctly
3. If crash → check model compatibility (CPU/GPU, dtype)
4. If garbage → model version mismatch or preprocessing issue

**Fix**:
- Add fallback response for model errors
- Implement circuit breaker pattern:
  - After 5 consecutive failures → return "service degraded" status
  - Stop sending requests to model until it recovers
- Add model version check at startup

---

## Failure 4 — Container Build Failures

**Symptom**: `docker build` fails with dependency errors.

**Diagnostic Steps**:
1. Check error in build log (which layer failed?)
2. Common causes:
   - Missing system packages (libgomp, libgl1)
   - Pip dependency conflicts
   - Python version mismatch
   - Binary packages need different architecture

**Fix**:
```dockerfile
# Add system dependencies BEFORE pip install
RUN apt-get update && apt-get install -y \
    libgomp1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*
```
- Pin all dependencies: `pip freeze > requirements.txt`
- Use `--no-cache-dir` to avoid stale packages
- Fix platform: `FROM --platform=linux/amd64 python:3.11-slim`

---

## Failure 5 — Version Mismatch

**Symptom**: API serves model v2 but clients expect v1 response schema.

**Diagnostic Steps**:
1. Compare current response schema with documented schema.
2. Check if any fields were added/removed/renamed.
3. Verify API version in URL matches the deployed model.

**Fix**:
- Always version APIs: `/v1/predict`, `/v2/predict`
- Maintain backward compatibility in minor versions
- For breaking changes:
  1. Deploy new version at `/v2/predict`
  2. Keep `/v1/predict` running
  3. Notify consumers with deprecation timeline
  4. Remove old version after migration

---

## Failure 6 — Cold Start Latency

**Symptom**: First request after deployment takes 30+ seconds (model loading).

**Diagnostic Steps**:
1. Measure model loading time during container startup.
2. Check if readiness probe passes before routing traffic.

**Fix**:
- Preload model in lifespan handler (before accepting requests)
- Set Kubernetes readiness probe to only pass after model is loaded:
  ```yaml
  readinessProbe:
    httpGet:
      path: /health
      port: 8000
    initialDelaySeconds: 60
    periodSeconds: 10
  ```
- Use model warmup (run one inference during startup)
- Cache model in container layer if small enough
