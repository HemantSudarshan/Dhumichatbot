# AI Solution Development — Test Cases

## Purpose

Use these test cases to validate that the `ai-solution-dev` skill behaves correctly across different scenarios. Each test defines an input, the expected agent behavior, and pass/fail criteria.

---

## Test 1 — Full End-to-End Pipeline

**Input Prompt**:
```
A client wants to build a chatbot that answers questions about their
internal documentation (500 PDF documents). The chatbot should be accessible
via a web interface. Budget is $200/month. Latency must be under 3 seconds.
```

**Expected Behavior**:
1. Agent identifies this as a RAG problem (retrieval + generation).
2. Agent decomposes: PDF ingestion → chunking → embedding → vector DB → retrieval → LLM generation.
3. Stack selection: LlamaIndex or LangChain + vector DB + open-source LLM (budget constraint).
4. Architecture: RAG pipeline with FastAPI backend.
5. Scaffold: Complete project with `data/`, `src/`, vectorization scripts.
6. Implementation: Working RAG chain.
7. Deployment: Dockerized FastAPI app.

**Pass Criteria**:
- [ ] `problem_specification.md` correctly identifies RAG
- [ ] `stack_decision.md` recommends budget-appropriate stack
- [ ] `architecture.md` includes PDF processing pipeline
- [ ] Working code scaffold with all files
- [ ] Deployment checklist produced

---

## Test 2 — Ambiguity Handling

**Input Prompt**:
```
Use AI to make our customer support better.
```

**Expected Behavior**:
1. Agent recognizes this as vague (only 1 implicit requirement).
2. Agent asks at least 5 clarifying questions.
3. Agent does NOT produce architecture or code.

**Pass Criteria**:
- [ ] Agent asks clarifying questions before any implementation
- [ ] No code or architecture generated before answers received
- [ ] Questions cover: problem specifics, data, constraints, users, success metrics

---

## Test 3 — Constraint Satisfaction

**Input Prompt**:
```
Build an image classifier that detects defective products on a
manufacturing line. Budget: $0 (no cloud APIs). Latency: <100ms.
No GPU available. Must run on a Raspberry Pi 4.
```

**Expected Behavior**:
1. Agent identifies: image classification + extreme resource constraints.
2. Stack selection: TensorFlow Lite or ONNX Runtime on CPU.
3. Model: lightweight MobileNet or EfficientNet-Lite quantized to INT8.
4. Architecture: local inference with camera feed → model → alert.

**Pass Criteria**:
- [ ] Agent does NOT recommend cloud APIs or large models
- [ ] Selected model fits within Raspberry Pi constraints
- [ ] Quantization strategy included
- [ ] Architecture is edge-first (no network dependency)

---

## Test 4 — Stack Selection Decision

**Input Prompt**:
```
We need a text summarization API that processes 10,000 documents per day.
Documents are 2-5 pages each. We have $500/month budget and a single
A10G GPU available.
```

**Expected Behavior**:
1. Agent calculates throughput: ~7 docs/minute sustained.
2. Agent evaluates: OpenAI API cost at this volume vs self-hosted.
3. Agent recommends: self-hosted model (e.g., BART-large or Llama-3-8B) on vLLM.
4. Agent produces cost comparison table.

**Pass Criteria**:
- [ ] `stack_decision.md` includes cost analysis
- [ ] Throughput calculation is explicit
- [ ] Self-hosted model fits within GPU memory
- [ ] Deployment uses batching for efficiency

---

## Test 5 — Deployment Validation

**Input Prompt**:
```
Deploy this sentiment analysis model to production.
(Model already trained and saved as model.pt)
```

**Expected Behavior**:
1. Agent creates FastAPI wrapper around the model.
2. Agent writes Dockerfile.
3. Agent runs the full deployment checklist.
4. Agent verifies smoke tests.
5. Agent documents rollback procedure.

**Pass Criteria**:
- [ ] API serves predictions correctly
- [ ] Docker container builds and runs
- [ ] Health check endpoint responds
- [ ] Smoke test sends real request and validates response
- [ ] Rollback procedure documented
- [ ] `deployment_checklist.md` is complete

---

## Test 6 — Security Compliance

**Input Prompt**:
```
Build an AI system that processes medical records for diagnosis assistance.
Must be HIPAA compliant.
```

**Expected Behavior**:
1. Agent flags HIPAA compliance requirement immediately.
2. Agent does NOT proceed without confirming compliance measures.
3. Agent recommends: encryption at rest, audit logging, access controls, no external APIs for PHI.

**Pass Criteria**:
- [ ] Compliance flagged before architecture
- [ ] No external API calls for sensitive data
- [ ] Encryption and access controls included
- [ ] Audit logging configured
- [ ] `risk_assessment.md` covers HIPAA requirements

---

## Test 7 — Failure Recovery

**Input Prompt**:
```
Build a real-time fraud detection system.
(User provides no data, no infrastructure details, no latency requirements.)
```

**Expected Behavior**:
1. Agent detects massive information gap.
2. Agent asks structured questions:
   - Transaction volume per second?
   - Historical fraud data available?
   - Current detection system (if any)?
   - Acceptable false positive rate?
   - Infrastructure available?
3. Agent does not proceed until minimum viable requirements are gathered.

**Pass Criteria**:
- [ ] No code generated without sufficient requirements
- [ ] Questions are specific and actionable
- [ ] Agent explicitly states what information is missing
