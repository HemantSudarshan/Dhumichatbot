# AI Research — Test Cases

---

## Test 1 — Vector Database Comparison

**Input**:
```
Research the best vector database for our RAG pipeline.
Requirements: Python SDK, <100ms query latency, supports metadata filtering,
managed or self-hosted. Budget: $200/month.
```

**Expected Behavior**:
1. Agent identifies candidates: Pinecone, Weaviate, Chroma, Qdrant, Milvus, pgvector.
2. Builds weighted evaluation matrix.
3. Builds PoC with top 2 (e.g., Pinecone vs Qdrant).
4. Produces tech spike report with recommendation.

**Pass Criteria**:
- [ ] 5+ candidates identified
- [ ] Evaluation matrix with weighted scores
- [ ] PoC built for top 2
- [ ] Recommendation includes cost analysis
- [ ] License checked for all candidates

---

## Test 2 — Paper Assessment

**Input**:
```
Read this paper: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
Assess if we should adopt this technique.
```

**Expected Behavior**:
1. Agent follows the speed-read protocol.
2. Produces structured paper summary.
3. Assesses relevance with ADOPT/TRIAL/ASSESS/HOLD rating.
4. Identifies limitations.

**Pass Criteria**:
- [ ] Summary covers key contribution, results, method
- [ ] Relevance assessment is specific (not generic)
- [ ] Limitations documented
- [ ] Citation correct and URL provided

---

## Test 3 — AI Framework Landscape

**Input**:
```
What's the current state of agentic AI frameworks?
We're building a multi-agent system for document processing.
```

**Expected Behavior**:
1. Agent maps the landscape: LangGraph, AutoGen, CrewAI, Swarm, custom.
2. Evaluates each against the specific use case.
3. Identifies top 2-3 candidates.
4. Provides recommendation with justification.

**Pass Criteria**:
- [ ] 5+ frameworks identified
- [ ] Use-case-specific evaluation
- [ ] Maturity ratings for each
- [ ] Clear recommendation

---

## Test 4 — Time-Boxed Research

**Input**:
```
Research everything about AI code generation for the next 4 hours.
```

**Expected Behavior**:
1. Agent enforces its time-box: max 2 hours discovery.
2. After 2 hours, stops discovering and starts synthesizing.
3. Reports what was found within the time limit.
4. Does NOT continue researching indefinitely.

**Pass Criteria**:
- [ ] Time-box enforced
- [ ] Report produced with available information
- [ ] Agent explicitly notes areas not yet covered

---

## Test 5 — Licensing Check

**Input**:
```
Should we use LLama-3 for our commercial SaaS product?
```

**Expected Behavior**:
1. Agent checks Llama 3 license (Meta Community License).
2. Reviews commercial use restrictions.
3. Assesses compliance requirements.
4. Provides clear recommendation.

**Pass Criteria**:
- [ ] License terms accurately described
- [ ] Commercial use implications stated
- [ ] Specific restrictions highlighted
- [ ] Alternative (permissive license) models suggested if relevant
