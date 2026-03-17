# Technical Documentation — Agent Instructions

## Execution Instructions

### Step 1 — Determine Documentation Type

1. When asked to create documentation, identify which type:
   - "Model card" → Model Card template
   - "Document this experiment" → Experiment Log template
   - "Deployment docs" / "runbook" → Deployment Runbook template
   - "API docs" → API Documentation template
   - "Why did we choose X?" → ADR template
   - "Audit our docs" → Documentation Audit

2. If unclear, ask: "What type of documentation do you need? Model card, experiment log, deployment runbook, API docs, or architecture decision record?"

### Step 2 — Gather Source Information

1. **For model cards**: Read model configuration, training logs, evaluation results.
2. **For experiment logs**: Read training configs, results files, code commits.
3. **For runbooks**: Read deployment scripts, Dockerfiles, CI/CD configs.
4. **For API docs**: Read FastAPI routes, Pydantic models, OpenAPI spec.
5. **For ADRs**: Interview user about the decision context and alternatives.

Sources to examine:
```
# Model information
ls models/ configs/ *.yaml *.yml
cat training_config.yaml

# Code information
cat src/main.py src/api/routes.py

# Deployment information  
cat Dockerfile docker-compose.yml .env.example
cat scripts/deploy.sh
```

### Step 3 — Generate Documentation

1. Select the appropriate template from SKILL.md Phase 3.
2. Fill every section with extracted information. **No placeholders.**
   - If information is unavailable, write: "⚠️ NOT DOCUMENTED — needs input from [role]"
3. Verify accuracy: cross-reference code, configs, and actual behavior.

### Step 4 — Validate Completeness

Run this checklist for each document type:

**Model Card Checklist**:
- [ ] Model name and version specified
- [ ] Intended use clearly described
- [ ] Training data summarized
- [ ] At least 3 evaluation metrics with values
- [ ] Limitations documented
- [ ] Maintenance plan included

**Experiment Log Checklist**:
- [ ] Hypothesis stated
- [ ] All hyperparameters listed
- [ ] Results table complete
- [ ] Conclusions actionable
- [ ] Reproducibility section filled

**Runbook Checklist**:
- [ ] Pre-deployment checklist complete
- [ ] Every step has an exact command
- [ ] Smoke tests are runnable
- [ ] Rollback procedure is explicit
- [ ] Contact information included

**API Docs Checklist**:
- [ ] All endpoints documented
- [ ] Request/response examples provided
- [ ] Error codes listed
- [ ] Auth instructions included
- [ ] Code examples in 2+ languages

**ADR Checklist**:
- [ ] Context explains the problem
- [ ] Decision is clearly stated
- [ ] At least 2 alternatives considered
- [ ] Consequences (positive + negative) listed

### Step 5 — Present for Review

1. Generate the document.
2. Highlight any sections marked as "NOT DOCUMENTED."
3. Ask user to review and provide missing information.

## Interaction Protocol

| Situation | Agent Behavior |
|-----------|---------------|
| No code comments exist | Fall back to reading code directly, ask user for context |
| Multiple configs conflict | Ask user which is the active/production config |
| Evaluation results don't exist | Flag as gap, recommend running evaluation first |
| Audience is non-technical | Write executive-friendly version alongside technical docs |

## Handoff

- If evaluation needed for model card → `data-pipeline` skill
- If deployment steps needed → `ai-integration` skill
- If monitoring not set up → `ai-reliability` skill
