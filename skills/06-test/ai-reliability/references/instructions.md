# AI Reliability — Agent Instructions

## Execution Instructions

### Step 1 — Assess Current State

1. Run the reliability audit from SKILL.md Phase 1.
2. Check what exists:
   - Tests? → `ls tests/`
   - Monitoring? → Check for Prometheus/Grafana configs
   - Scaling? → Check Kubernetes/docker configs
   - Incident response? → Check for runbooks
3. Produce `reliability_audit.md` with findings.

### Step 2 — Design Test Suite

1. Identify test gaps from the audit.
2. Prioritize:
   - First: health check + basic prediction tests (integration)
   - Second: model quality regression tests
   - Third: load tests
   - Fourth: shadow/canary tests
3. Generate test files using templates from SKILL.md Phase 2.
4. Run tests: `pytest tests/ -v --cov`

### Step 3 — Design Scalability

1. Understand traffic patterns:
   - "How many requests per second at peak?"
   - "What's the expected growth rate?"
   - "Are there traffic spikes (time-of-day, events)?"
2. Select scaling pattern from SKILL.md Phase 3.
3. Generate configuration files (HPA, docker-compose scale, etc.).
4. Document scaling strategy in `scaling_architecture.md`.

### Step 4 — Set Up Monitoring

1. Implement Prometheus metrics in the application (SKILL.md Phase 4).
2. Create Grafana dashboard:
   - Row 1: Request rate, error rate
   - Row 2: Latency percentiles
   - Row 3: GPU/CPU/Memory
   - Row 4: Model confidence distribution
3. Configure alerting rules (thresholds from SKILL.md Phase 4).
4. Test alerts: trigger a fake alert to verify notification works.

### Step 5 — Configure Drift Detection

1. Capture reference data (production data at time of model deployment).
2. Set up drift detection script (SKILL.md Phase 5).
3. Schedule daily runs.
4. Configure alerts for drift detected.

### Step 6 — Create Incident Response Plan

1. Use the playbook template from SKILL.md Phase 6.
2. Define severity levels for this specific system.
3. Document response procedures per severity.
4. Create post-mortem template.

### Step 7 — Run QA Checklist

1. Execute the 30-item checklist from SKILL.md Phase 7.
2. Mark each item PASS/FAIL.
3. For any FAIL: create a task to fix it.
4. Generate `qa_report.md` with results.

## Interaction Protocol

| Situation | Agent Behavior |
|-----------|---------------|
| No tests exist at all | Start with 3 critical tests before anything else |
| No monitoring at all | Deploy health + latency + error rate monitoring first |
| Drift detected | Report with data, recommend evaluation, let user decide on retraining |
| Incident during work | Switch to incident response mode, follow playbook |
| QA checklist has > 5 failures | Flag as "not production-ready," prioritize critical items |

## Handoff

- If model retraining needed → `finetuning` skill
- If API changes needed → `ai-integration` skill
- If documentation missing → `documentation` skill
- If evaluation needed → `data-pipeline` skill
