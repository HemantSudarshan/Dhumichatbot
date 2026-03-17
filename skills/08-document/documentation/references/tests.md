# Technical Documentation — Test Cases

---

## Test 1 — Model Card Generation

**Input**:
```
Generate a model card for my fine-tuned sentiment classifier.
Model: fine-tuned distilbert-base-uncased on IMDB dataset.
Accuracy: 92.3%, F1: 91.8%.
```

**Expected Behavior**:
1. Agent uses the Model Card template.
2. Fills in all sections: model details, training data, evaluation results.
3. Adds limitations and ethical considerations.

**Pass Criteria**:
- [ ] All required sections present
- [ ] Evaluation metrics included with values
- [ ] Intended use and out-of-scope use specified
- [ ] Limitations section is non-empty

---

## Test 2 — Deployment Runbook

**Input**:
```
Create a deployment runbook for our RAG API.
Deployed on Docker, using FastAPI, Pinecone for vector DB.
```

**Expected Behavior**:
1. Agent creates runbook with pre-deployment checklist.
2. Includes exact deployment commands.
3. Includes smoke test commands.
4. Includes rollback procedure.

**Pass Criteria**:
- [ ] Pre-deployment checklist is complete
- [ ] Commands are exact (not pseudocode)
- [ ] Smoke tests are runnable
- [ ] Rollback procedure explicitly documented

---

## Test 3 — API Documentation

**Input**:
```
Document the /predict endpoint of our FastAPI application.
It accepts a JSON body with "text" field and returns "prediction" and "confidence".
```

**Expected Behavior**:
1. Agent documents the endpoint with method, path, request/response schema.
2. Provides examples in cURL, Python, JavaScript.
3. Lists error codes.
4. Includes authentication if present.

**Pass Criteria**:
- [ ] Endpoint fully described
- [ ] Examples in 3+ formats
- [ ] Error codes listed
- [ ] Examples are executable

---

## Test 4 — Architecture Decision Record

**Input**:
```
Write an ADR for choosing Pinecone over Weaviate for our vector database.
We chose Pinecone because: managed service, lower ops overhead, better customer support.
Trade-off: higher cost, vendor lock-in.
```

**Expected Behavior**:
1. Agent uses ADR template.
2. Fills in context, decision, alternatives, consequences.
3. Both positive and negative consequences documented.

**Pass Criteria**:
- [ ] Context explains why the decision was needed
- [ ] Decision clearly stated
- [ ] Weaviate listed as alternative with pros/cons
- [ ] Vendor lock-in listed as negative consequence

---

## Test 5 — Documentation Audit

**Input**:
```
Audit the documentation in our project. What's missing?
```

**Expected Behavior**:
1. Agent scans project files for existing docs.
2. Checks for: README, model cards, experiment logs, API docs, runbooks, ADRs.
3. Reports what exists and what's missing.
4. Prioritizes what to create first.

**Pass Criteria**:
- [ ] Comprehensive audit of existing docs
- [ ] Missing documentation identified
- [ ] Priority recommendations provided
- [ ] Quality assessment for existing docs
