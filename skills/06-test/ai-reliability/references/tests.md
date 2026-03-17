# AI Reliability — Test Cases

---

## Test 1 — Monitoring Setup

**Input**:
```
Set up monitoring for our model serving API.
We use FastAPI, deployed on Kubernetes.
Need to track latency, errors, and model confidence.
```

**Expected Behavior**:
1. Agent adds Prometheus metrics to the FastAPI app.
2. Creates Grafana dashboard configuration.
3. Configures alerting rules for latency and error rate.
4. Includes model confidence histogram tracking.

**Pass Criteria**:
- [ ] Prometheus metrics endpoint works (/metrics)
- [ ] Latency tracked with p50/p95/p99
- [ ] Error rate computed and alerted
- [ ] Model confidence distribution recorded
- [ ] Alert rules are reasonable (not too noisy)

---

## Test 2 — Latency Debugging

**Input**:
```
Our API latency increased 3x after the last deployment.
Before: p95 = 200ms. After: p95 = 600ms.
No code changes to the model, only updated dependencies.
```

**Expected Behavior**:
1. Agent profiles each pipeline stage.
2. Checks for dependency version impacts.
3. Compares inference time with previous version.
4. Identifies root cause.

**Pass Criteria**:
- [ ] Profiling results for each stage
- [ ] Dependency diff analyzed
- [ ] Root cause identified (or top 3 hypotheses)
- [ ] Optimization recommendation provided

---

## Test 3 — QA Checklist

**Input**:
```
We're deploying a new sentiment analysis API to production tomorrow.
Run the QA checklist.
```

**Expected Behavior**:
1. Agent runs the 30-item checklist.
2. Tests each item systematically.
3. Marks PASS/FAIL.
4. Reports any blocking issues.

**Pass Criteria**:
- [ ] All 30 items evaluated
- [ ] Blocking items clearly identified
- [ ] Recommendations for each FAIL
- [ ] Overall readiness assessment (GO/NO-GO)

---

## Test 4 — Auto-Scaling Design

**Input**:
```
Design auto-scaling for our model API.
Expected: 50 RPS average, 500 RPS peak (Black Friday).
Single request takes ~200ms on A10G GPU.
```

**Expected Behavior**:
1. Agent calculates: 50 RPS × 0.2s = 10 concurrent requests baseline.
2. Agent calculates: 500 RPS × 0.2s = 100 concurrent requests peak.
3. Agent designs HPA with min 2, max 15 replicas.
4. Agent recommends dynamic batching for efficiency.

**Pass Criteria**:
- [ ] Capacity math is explicit
- [ ] HPA configuration generated
- [ ] Min/max replicas justified
- [ ] Batching strategy included
- [ ] Cost estimate provided

---

## Test 5 — Drift Detection Setup

**Input**:
```
Set up drift detection for our customer churn classifier.
The model was trained on data from January.
We're now in June and want to know if the data has shifted.
```

**Expected Behavior**:
1. Agent captures reference data statistics from January.
2. Implements KS-test or PSI for each feature.
3. Runs detection on current data.
4. Reports drifted features with severity.
5. Recommends retraining if significant drift.

**Pass Criteria**:
- [ ] Reference data captured
- [ ] Statistical test implemented correctly
- [ ] Results reported per feature
- [ ] Severity assessment included
- [ ] Retraining recommendation if warranted

---

## Test 6 — Incident Response

**Input**:
```
Our model API is returning 500 errors for 30% of requests.
This started 15 minutes ago. Help!
```

**Expected Behavior**:
1. Agent identifies this as SEV2 (major degradation).
2. Follows incident response steps:
   - Check recent deployments
   - Check error logs for stack trace
   - Check model health
   - Check infrastructure (memory, GPU, disk)
3. Recommends immediate mitigation (rollback if recent deploy).
4. Creates post-mortem template.

**Pass Criteria**:
- [ ] Severity correctly classified
- [ ] Systematic investigation followed
- [ ] Immediate mitigation recommended
- [ ] Root cause analysis attempted
- [ ] Post-mortem template generated
