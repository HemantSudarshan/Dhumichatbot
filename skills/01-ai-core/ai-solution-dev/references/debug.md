# AI Solution Development — Debug Protocol

## Purpose

This file guides the agent through deterministic troubleshooting when the AI solution development workflow encounters failures. **When an error occurs, STOP generating code and follow this diagnostic protocol.**

---

## Failure Scenario 1 — Ambiguous Problem Statement

**Symptom**: User provides vague input like "We want to use AI to improve our business."

**Root Cause**: Insufficient requirements to decompose into an ML problem.

**Diagnostic Steps**:
1. Count the number of concrete requirements in the statement.
2. If fewer than 3 specific requirements, trigger clarification loop.

**Expected Behavior**:
- Agent MUST NOT proceed with architecture.
- Agent asks these questions:
  1. "What specific process do you want to improve?"
  2. "What data do you currently collect related to this process?"
  3. "What does success look like? Give me a measurable outcome."
  4. "Who will use this system — internal team or end customers?"
  5. "What's your budget and timeline?"

**Resolution**: Only proceed when at least 4 clarifying answers are received.

---

## Failure Scenario 2 — Missing or Unavailable Data

**Symptom**: The selected ML approach requires labeled data but none exists.

**Root Cause**: Problem decomposition assumed data availability.

**Diagnostic Steps**:
1. Verify what data actually exists (format, volume, labels).
2. If no labeled data: escalate.

**Expected Behavior**:
- Agent presents fallback strategies:
  | Strategy | When to Use | Cost |
  |----------|------------|------|
  | Zero-shot with LLM | Labels unnecessary for the task | API costs only |
  | Few-shot prompting | < 20 examples available | Minimal |
  | Synthetic data generation | Need structured training data | Compute + time |
  | Human labeling (Label Studio) | Need high-quality labels | Person-hours |
  | Pre-trained model (no fine-tuning) | General task, no custom data | Free |

**Resolution**: User selects a fallback strategy before proceeding.

---

## Failure Scenario 3 — Incompatible Model Choice

**Symptom**: Agent selects a model too large for the deployment constraints.

**Example**: 70B parameter model targeted for <100ms latency on a 16GB GPU.

**Root Cause**: No guardrail checking model size against infrastructure.

**Diagnostic Steps**:
1. Calculate model VRAM requirement: `params * 2 bytes (FP16)` or `params * 0.5 bytes (INT4)`
2. Compare against available GPU memory.
3. Calculate expected latency based on model size and hardware.

**Guardrail Table**:
| Model Size | FP16 VRAM | INT4 VRAM | Min GPU | Expected Latency |
|-----------|-----------|-----------|---------|------------------|
| 1B-3B | 2-6 GB | 0.5-1.5 GB | T4 | <50ms |
| 7B-8B | 14-16 GB | 3.5-4 GB | A10G | 50-200ms |
| 13B | 26 GB | 6.5 GB | A100-40 | 100-500ms |
| 70B | 140 GB | 35 GB | 2xA100-80 | 500ms-2s |

**Resolution**: If model exceeds constraints, recommend:
1. Smaller model from same family
2. Quantized version (INT4/INT8)
3. Distilled model
4. API-based alternative (offload to cloud)

---

## Failure Scenario 4 — Deployment Environment Mismatch

**Symptom**: Solution requires GPU but target environment is CPU-only.

**Root Cause**: Architecture phase did not verify deployment infrastructure.

**Diagnostic Steps**:
1. Query the deployment target's hardware specs.
2. Check if GPU is available in the deployment environment.
3. Measure inference latency on CPU.

**Expected Behavior**:
- If CPU inference is acceptable (< SLA):
  - Use ONNX Runtime CPU optimization
  - Use quantized models (GGUF with llama.cpp)
  - Reduce model size
- If CPU inference is unacceptable:
  - Recommend cloud GPU instances
  - Recommend API-based inference (OpenAI, Together, Groq)

---

## Failure Scenario 5 — Scope Creep

**Symptom**: Client adds new requirements after Phase 4 (implementation started).

**Root Cause**: No scope boundary enforcement.

**Diagnostic Steps**:
1. Compare new requirements against `problem_specification.md`.
2. Classify each new requirement: essential vs nice-to-have.

**Expected Behavior**:
- Agent documents new requirements separately.
- Agent estimates impact on timeline and architecture.
- Agent presents: "Adding X requires Y hours and changes to Z component."
- Agent recommends: build current scope first, then iterate.
- Agent DOES NOT silently incorporate changes.

---

## Failure Scenario 6 — Security Violation

**Symptom**: Generated code contains hardcoded API keys, missing auth, or insecure endpoints.

**Diagnostic Steps**:
1. Scan all generated code for:
   - Hardcoded strings matching API key patterns (`sk-`, `pk_`, bearer tokens)
   - Missing authentication middleware
   - Unvalidated user inputs
   - SQL/prompt injection vulnerabilities
2. Check `.env.example` includes all required secrets.
3. Verify `.gitignore` excludes `.env` files.

**Expected Behavior**:
- Agent MUST use environment variables for all secrets.
- Agent MUST add authentication to all endpoints (except `/health`).
- Agent MUST validate all inputs with Pydantic.
- Agent MUST add rate limiting to API endpoints.

**Resolution**: If violation detected, fix immediately before proceeding.

---

## Failure Scenario 7 — Integration Failure (200 OK but Garbage Output)

**Symptom**: API returns HTTP 200 but the response content is wrong or nonsensical.

**Root Cause**: Model loaded incorrectly, preprocessing mismatch, or wrong model version.

**Diagnostic Steps**:
1. Send a known-good test input and inspect the raw response.
2. Verify model loads the correct weights (check model path, version).
3. Verify preprocessing matches training preprocessing.
4. Check tokenizer configuration (special tokens, chat template).
5. Test model inference directly (outside the API) with the same input.

**Smoke Test Checklist**:
- [ ] Send test input → verify response is semantically correct
- [ ] Send empty input → verify appropriate error response
- [ ] Send oversized input → verify truncation or rejection
- [ ] Send adversarial input → verify no crash or hallucination
- [ ] Compare output against known baseline

**Resolution**: If model output is wrong, the issue is in model loading or preprocessing, not the API layer. Debug the model pipeline directly.
