---
name: ai-reliability
description: "Use this skill when tasked with ensuring quality, scalability, or reliability of an AI system. Covers testing strategies (unit, integration, model quality), scaling patterns, monitoring and observability setup, model drift detection, incident response, and production QA checklists."
---

# Quality, Scalability, Reliability

## Overview

This skill provides a comprehensive framework for making AI systems production-ready — covering testing, scaling, monitoring, drift detection, incident response, and quality assurance.

## Supporting References

Load only the reference file you need:
- `references/instructions.md` for audit order, implementation steps, and escalation rules
- `references/debug.md` for latency, drift, and outage recovery guidance
- `references/tests.md` for production-readiness validation scenarios

## Required Inputs

1. **System to assess** — what AI system needs reliability work?
2. **Current state** — what testing/monitoring exists today?
3. **SLAs** — what latency, uptime, accuracy targets?
4. **Scale requirements** — expected traffic, growth projections

## Step-by-Step Workflow

### Phase 1 — Quality Assessment (Current State Audit)

**Objective**: Understand the current reliability posture.

**Assessment Checklist**:
```markdown
## Reliability Audit

### Testing
- [ ] Unit tests exist for core logic
- [ ] Integration tests exist for API
- [ ] Model quality tests exist (accuracy regression)
- [ ] Load tests have been run
- Total test coverage: ____%

### Monitoring
- [ ] Health check endpoint exists
- [ ] Latency tracked (p50, p95, p99)
- [ ] Error rate tracked
- [ ] GPU/CPU utilization tracked
- [ ] Model confidence distribution tracked
- [ ] Alerting configured

### Scaling
- [ ] Horizontal scaling configured
- [ ] Auto-scaling policies defined
- [ ] Resource limits set
- [ ] Load tested at expected peak

### Incident Response
- [ ] Runbook exists
- [ ] Rollback procedure documented
- [ ] On-call schedule defined
- [ ] Post-mortem process established
```

**Output**: `reliability_audit.md`

---

### Phase 2 — Test Suite Design & Implementation

**Testing Hierarchy for AI Systems**:

| Test Type | What It Validates | Example |
|----------|-------------------|---------|
| **Unit Tests** | Individual functions | Data preprocessing logic |
| **Integration Tests** | API + model together | POST /predict returns valid response |
| **Model Quality Tests** | Model accuracy hasn't regressed | F1 > 0.85 on test set |
| **Contract Tests** | API schema compliance | Response matches OpenAPI spec |
| **Load Tests** | Performance under stress | p99 < 2s at 100 RPS |
| **Shadow Tests** | New model vs old model comparison | Run both, compare outputs |

**Example Test Suite**:
```python
# tests/test_unit.py
def test_preprocess_handles_empty_string():
    result = preprocess("")
    assert result == ""

def test_preprocess_removes_html():
    result = preprocess("<b>hello</b>")
    assert result == "hello"

# tests/test_integration.py
def test_predict_valid_input(client):
    response = client.post("/predict", json={"text": "great product"})
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_predict_returns_confidence(client):
    response = client.post("/predict", json={"text": "test"})
    data = response.json()
    assert 0 <= data["confidence"] <= 1

# tests/test_model_quality.py
def test_model_accuracy_above_threshold():
    predictions = [model.predict(x) for x in test_data]
    accuracy = sum(p == l for p, l in zip(predictions, labels)) / len(labels)
    assert accuracy >= 0.85, f"Model accuracy {accuracy} below threshold 0.85"

def test_no_accuracy_regression():
    current_f1 = evaluate_model(model, test_set)
    baseline_f1 = load_baseline_metrics()["f1"]
    assert current_f1 >= baseline_f1 - 0.02, \
        f"F1 regressed: {current_f1} < {baseline_f1} - 0.02"
```

---

### Phase 3 — Scalability Architecture

**Scaling Patterns**:

| Pattern | When to Use | Implementation |
|---------|------------|----------------|
| **Horizontal Scaling** | Stateless APIs | Multiple replicas behind load balancer |
| **Dynamic Batching** | GPU inference | Collect N requests, batch inference |
| **Response Caching** | Repeated queries | Redis/in-memory LRU cache |
| **Async Processing** | Long-running inference | Queue (Redis/RabbitMQ) + workers |
| **Auto-scaling** | Variable traffic | K8s HPA, cloud auto-scale groups |

**Kubernetes HPA Example**:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: model-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: model-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: 100
```

**Caching Implementation**:
```python
from functools import lru_cache
import hashlib

# In-memory cache for predictions
@lru_cache(maxsize=10000)
def cached_predict(input_hash: str):
    return model.predict(input_from_hash(input_hash))

def predict_with_cache(text: str):
    text_hash = hashlib.md5(text.encode()).hexdigest()
    return cached_predict(text_hash)
```

---

### Phase 4 — Monitoring & Observability

**Essential Metrics Dashboard**:

| Metric | Alert Threshold | Severity |
|--------|----------------|----------|
| Health check status | DOWN for > 30s | CRITICAL |
| Request latency p95 | > 2x baseline | WARNING |
| Request latency p99 | > 5x baseline | CRITICAL |
| Error rate (5xx) | > 1% | CRITICAL |
| Error rate (4xx) | > 10% | WARNING |
| GPU utilization | > 90% sustained | WARNING |
| Memory usage | > 85% | WARNING |
| Model confidence avg | Drops > 20% | WARNING |
| Request throughput | Drops > 50% | CRITICAL |

**Prometheus Metrics Implementation**:
```python
from prometheus_client import Counter, Histogram, Gauge
import time

REQUEST_COUNT = Counter('api_requests_total', 'Total requests', ['endpoint', 'status'])
REQUEST_LATENCY = Histogram('api_request_duration_seconds', 'Request latency', ['endpoint'])
MODEL_CONFIDENCE = Histogram('model_confidence', 'Prediction confidence distribution')
GPU_UTILIZATION = Gauge('gpu_utilization_percent', 'GPU utilization')

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    REQUEST_COUNT.labels(endpoint=request.url.path, status=response.status_code).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(duration)
    
    return response
```

---

### Phase 5 — Drift Detection

**Types of Drift**:

| Drift Type | What Changes | Detection |
|-----------|-------------|-----------|
| **Data Drift** | Input distribution shifts | PSI, KL divergence on features |
| **Concept Drift** | Relationship between input→output changes | Accuracy on recent data drops |
| **Prediction Drift** | Output distribution shifts | KL divergence on predictions |

**Drift Detection Script**:
```python
import numpy as np
from scipy.stats import ks_2samp

def detect_drift(reference_data, current_data, threshold=0.05):
    """Detect data drift using Kolmogorov-Smirnov test."""
    results = {}
    for feature in reference_data.columns:
        statistic, p_value = ks_2samp(
            reference_data[feature].dropna(),
            current_data[feature].dropna()
        )
        results[feature] = {
            "statistic": statistic,
            "p_value": p_value,
            "drift_detected": p_value < threshold
        }
    
    drifted_features = [f for f, r in results.items() if r["drift_detected"]]
    return {
        "drift_detected": len(drifted_features) > 0,
        "drifted_features": drifted_features,
        "details": results
    }
```

**Automated Alerting**:
- Run drift detection daily on production data.
- Alert if drift detected in > 30% of features.
- Trigger retraining evaluation if prediction drift > 10%.

---

### Phase 6 — Incident Response Playbook

**Incident Severity Levels**:

| Level | Definition | Response Time | Examples |
|-------|-----------|---------------|---------|
| SEV1 | Complete outage | 15 min | API down, all requests failing |
| SEV2 | Major degradation | 1 hour | Latency 10x normal, 50% errors |
| SEV3 | Minor degradation | 4 hours | Accuracy dropped 5%, increased latency |
| SEV4 | Non-urgent | Next business day | Monitoring gaps, doc updates needed |

**Incident Response Steps**:
1. **DETECT**: Alert fires or user reports issue.
2. **TRIAGE**: Determine severity level.
3. **COMMUNICATE**: Notify stakeholders.
4. **INVESTIGATE**: Check metrics, logs, recent changes.
5. **MITIGATE**: Rollback, restart, or scale up.
6. **RESOLVE**: Fix root cause.
7. **POST-MORTEM**: Document what happened and prevent recurrence.

**Post-Mortem Template**:
```markdown
# Incident Post-Mortem: [Title]
Date: [YYYY-MM-DD]
Severity: [SEV1-4]
Duration: [start → end]

## Summary
[1-2 sentence description]

## Timeline
- HH:MM — [Event]
- HH:MM — [Event]

## Root Cause
[What caused the incident]

## Impact
- Users affected: [count]
- Requests failed: [count]
- Revenue impact: [estimate]

## Resolution
[How the incident was resolved]

## Prevention
- [ ] [Action item 1]
- [ ] [Action item 2]
```

---

### Phase 7 — QA Checklist

**Production Readiness Checklist** (30 items):

**Code Quality (1-8)**:
- [ ] 1. All functions have docstrings
- [ ] 2. No hardcoded credentials
- [ ] 3. Input validation on all endpoints
- [ ] 4. Error handling with structured responses
- [ ] 5. Logging configured (structured, leveled)
- [ ] 6. Code review completed
- [ ] 7. Dependencies pinned with versions
- [ ] 8. Security scan passed (no known vulns)

**Model Quality (9-15)**:
- [ ] 9. Evaluation metrics meet threshold
- [ ] 10. No accuracy regression vs baseline
- [ ] 11. Tested on edge cases
- [ ] 12. Model card documented
- [ ] 13. Training data versioned
- [ ] 14. Reproducibility verified
- [ ] 15. Bias assessment completed

**Performance (16-22)**:
- [ ] 16. Latency p95 within SLA
- [ ] 17. Load tested at expected peak
- [ ] 18. Memory usage stable under load
- [ ] 19. Cold start time acceptable
- [ ] 20. Concurrent request handling verified
- [ ] 21. Resource limits configured
- [ ] 22. Caching strategy implemented (if applicable)

**Operations (23-30)**:
- [ ] 23. Health check endpoint
- [ ] 24. Monitoring and dashboards configured
- [ ] 25. Alerting rules in place
- [ ] 26. Deployment runbook exists
- [ ] 27. Rollback procedure tested
- [ ] 28. Incident response plan exists
- [ ] 29. On-call rotation scheduled
- [ ] 30. Documentation up to date

---

## Anti-Patterns — DO NOT

| Anti-Pattern | Consequence | Correct Approach |
|-------------|-------------|------------------|
| Deploy without tests | Silent failures | Minimum: health + predict + quality tests |
| Monitor only CPU/memory | Miss model degradation | Also track model confidence and accuracy |
| Scale without load testing first | Unknown failure modes | Load test before setting auto-scale policies |
| Skip rollback testing | Cannot recover | Practice rollback at least once per quarter |
| Ignore data drift | Model accuracy decays silently | Run drift detection daily |
| No post-mortem after incidents | Same incidents repeat | Always do a post-mortem |

## Skill Coordination

- Use `ai-solution-dev` when reliability work feeds back into architecture and delivery decisions.
- Use `finetuning` when quality or drift issues require re-training or model adaptation.
- Use `data-pipeline` when data validation and offline evaluation pipelines need reinforcement.
- Use `ai-integration` when serving architecture must change to meet latency or scale goals.
- Use `documentation` to capture runbooks, QA evidence, and post-mortem artifacts.
