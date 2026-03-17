# Agent Skill Blueprint System
## Applied AI Engineer — JD to Skill Kit Transformation

> **JDs = latent skill ontologies.** This document converts every responsibility from the Applied AI Engineer job description into a complete, modular agent skill blueprint.

---

# Skill 1 — AI Solution Development & Deployment

## Skill Name
`ai-solution-dev`

## Responsibility Mapping
> *"Assist in the development and deployment of AI-powered software solutions for client problem statements."*

## Skill Objective
Enable an AI agent to take an ambiguous client problem statement and systematically decompose it into an ML problem type, select the optimal tech stack, scaffold the project, implement the solution, and deploy it — producing architecture docs, code scaffolds, and deployment checklists as artifacts.

## Research Prompt
```
You are a senior Applied AI architect with 10+ years building production ML systems.

I am building an agentic skill for an AI engineer who must assist in developing
and deploying AI-powered solutions for client problem statements.

Produce a deeply practical engineering guide covering:

1. A FRAMEWORK to decompose any client problem statement into:
   - ML problem type (classification, regression, generation, retrieval, ranking, anomaly detection)
   - Data requirements (volume, labeling, format, availability)
   - System architecture (monolith vs microservice, sync vs async inference)
   - Deployment constraints (latency SLA, throughput, cost ceiling, compliance)
   - Success metrics (business KPIs mapped to ML metrics)

2. A STACK DECISION MATRIX comparing:
   | Criterion        | OpenAI API | HuggingFace | LangChain | LlamaIndex | FastAPI | vLLM | TGI |
   Including: cost model, latency, scalability ceiling, vendor lock-in risk, fine-tuning support.

3. A REUSABLE PROJECT SCAFFOLD:
   Produce a complete folder structure for an AI solution project including:
   - src/, tests/, configs/, data/, models/, scripts/, docs/
   - Key files: main.py, config.yaml, Dockerfile, requirements.txt, Makefile, .env.example

4. DEPLOYMENT STRATEGIES with decision criteria:
   - Local inference (when, how, GPU requirements)
   - Cloud API deployment (FastAPI + Docker + cloud run)
   - Serverless (Lambda/Cloud Functions + cold start tradeoffs)
   - Kubernetes (HPA, GPU node pools, model serving with Triton/vLLM)

5. A DEPLOYMENT CHECKLIST usable by a junior AI engineer:
   Pre-deployment, deployment, post-deployment verification steps.
   Include rollback procedures and smoke test commands.

6. The 15 MOST COMMON implementation mistakes in AI product prototypes:
   For each mistake: description, real-world consequence, prevention strategy.

Output must be exhaustive, code-rich, and immediately actionable.
Do NOT produce theory — produce engineering artifacts.
```

## Skill Builder Prompt
```
You are an expert agentic workflow designer.

Convert the following research knowledge into a production-ready SKILL.md file
compatible with the Antigravity/Cursor/Claude Code progressive disclosure standard.

The skill must help an AI agent go from:
  CLIENT PROBLEM STATEMENT → DEPLOYED AI SYSTEM

The SKILL.md must contain:

1. YAML Frontmatter:
   ---
   name: ai-solution-dev
   description: "Use this skill when tasked with developing an AI-powered solution
   from a client problem statement, designing system architecture, scaffolding
   a project, or deploying an ML/LLM application."
   ---

2. OVERVIEW: When to activate this skill (trigger conditions).

3. REQUIRED INPUTS: What the agent needs from the user before starting.

4. STEP-BY-STEP WORKFLOW:
   Phase 1 — Problem Decomposition (output: problem_specification.md)
   Phase 2 — Stack Selection (output: stack_decision.md with decision matrix)
   Phase 3 — Architecture Design (output: architecture.md + system diagram)
   Phase 4 — Project Scaffolding (output: complete folder structure + boilerplate)
   Phase 5 — Implementation (output: working codebase)
   Phase 6 — Testing (output: test suite)
   Phase 7 — Deployment (output: deployment artifacts + checklist)

5. GENERATED ARTIFACTS: List every file/document the skill produces.

6. DECISION TABLES: Embed the stack selection matrix and deployment strategy matrix.

7. ANTI-PATTERNS: List dangerous patterns the agent must avoid.

8. FAILURE RECOVERY: What to do when each phase fails.

Format as clean, well-structured Markdown with proper headings.
The skill must be deterministic — given the same input, it produces the same workflow.
```

## Instruction Builder Prompt
```
You are a technical writer creating agent operating instructions.

Generate an instructions.md file for the "ai-solution-dev" skill that explains:

1. HOW THE SKILL ACTIVATES:
   - Trigger phrases and semantic patterns
   - What the agent reads first (YAML frontmatter)
   - How progressive disclosure loads the full skill

2. STEP-BY-STEP EXECUTION:
   For each of the 7 phases:
   - What the agent does
   - What tools it uses (file creation, terminal commands, web search)
   - What artifacts it produces
   - What validation checks it runs before proceeding

3. INTERACTION PROTOCOL:
   - When to ask the user for clarification
   - When to proceed autonomously
   - How to present choices (e.g., stack selection)

4. OUTPUT FORMAT STANDARDS:
   - Markdown structure for all documents
   - Code style requirements
   - File naming conventions

5. HANDOFF PROTOCOL:
   - How to hand off to other skills (e.g., ai-reliability for testing)
   - How to log completion

Write as imperative instructions addressed to the AI agent.
Use numbered steps. Be explicit. Assume the agent has no prior context.
```

## Debug Prompt
```
You are an AI engineering QA reviewer specializing in fault analysis.

The "ai-solution-dev" skill guides agents through building and deploying AI solutions.
Stress-test this skill by simulating these failure scenarios:

1. AMBIGUOUS PROBLEM STATEMENT:
   "We want to use AI to improve our business."
   → How should the skill force decomposition? What clarifying questions?

2. MISSING OR UNAVAILABLE DATA:
   Client has no labeled dataset and no budget for annotation.
   → What fallback strategies should the skill recommend?

3. INCOMPATIBLE MODEL CHOICE:
   Agent selects a 70B parameter model for a latency-sensitive mobile app.
   → What guardrails catch this? What's the escalation path?

4. DEPLOYMENT ENVIRONMENT MISMATCH:
   Solution requires GPU but target environment is CPU-only serverless.
   → How does the skill detect and resolve this?

5. SCOPE CREEP:
   Client adds 3 new requirements mid-implementation.
   → How does the skill enforce scope boundaries?

6. SECURITY VIOLATION:
   Agent generates code that hardcodes API keys or skips auth.
   → What security checks run automatically?

7. INTEGRATION FAILURE:
   Deployed API returns 200 but produces garbage outputs.
   → What smoke tests and validation gates catch this?

For each scenario, generate:
- Failure description
- Root cause
- Expected skill behavior
- Recommended fix to the skill instructions
- Test case to prevent recurrence

Output as a structured debug.md file.
```

## Test Prompts
```
Test Case 1 — Basic E2E:
"A client wants to build a chatbot that answers questions about their
internal documentation. Design and deploy the solution."
Expected: Problem decomposition → RAG architecture → scaffold → deploy

Test Case 2 — Ambiguity Handling:
"Use AI to make our customer support better."
Expected: Agent asks 5+ clarifying questions before proceeding.

Test Case 3 — Constraint Satisfaction:
"Build an image classifier. Budget: $0. Latency: <100ms. No GPU."
Expected: Agent selects lightweight model, local CPU inference, quantized.

Test Case 4 — Stack Selection:
"We need a text summarization API for 10K documents/day."
Expected: Agent produces decision matrix, recommends appropriate stack.

Test Case 5 — Deployment Validation:
"Deploy this model to production."
Expected: Agent runs full checklist, smoke tests, rollback verification.
```

## Expected Outputs
- `problem_specification.md` — structured problem decomposition
- `stack_decision.md` — technology selection matrix with rationale
- `architecture.md` — system architecture document with diagrams
- Project scaffold (complete folder structure with boilerplate code)
- `deployment_checklist.md` — pre/during/post deployment steps
- `risk_assessment.md` — identified risks and mitigation strategies
- Working `Dockerfile` and `docker-compose.yml`
- API endpoint code (`main.py` with FastAPI)

## Edge Cases

| Edge Case | Risk | Mitigation |
|-----------|------|------------|
| Problem statement is a single vague sentence | Agent generates incorrect architecture | Force clarification loop — refuse to proceed without 5 minimum datapoints |
| Client changes requirements after Phase 4 | Wasted implementation work | Checkpoint system — each phase requires explicit sign-off |
| No training data exists | Cannot train/fine-tune models | Recommend zero-shot, few-shot, or synthetic data generation |
| Target deployment has no internet access | Cannot use cloud APIs | Default to local models (GGUF quantized, ONNX runtime) |
| Multi-modal requirements (text + image + audio) | Architecture complexity explosion | Decompose into separate pipelines, integrate via orchestrator |
| Compliance requirements (HIPAA, GDPR, SOC2) | Legal exposure | Trigger compliance checklist sub-skill before architecture phase |

---

# Skill 2 — Fine-Tuning & Model Optimization

## Skill Name
`finetuning`

## Responsibility Mapping
> *"Support fine-tuning and optimization of machine learning models and Large Language Models (LLMs)."*

## Skill Objective
Guide an AI agent through the complete fine-tuning lifecycle: dataset preparation → training configuration → execution → evaluation → optimization → export. The skill must support full fine-tuning, LoRA, QLoRA, and PEFT, and produce production-ready training scripts and evaluation reports.

## Research Prompt
```
You are an ML engineer specializing in LLM fine-tuning and model optimization.

Produce an exhaustive, code-first engineering guide covering:

1. FINE-TUNING PIPELINE — end-to-end workflow:
   Data audit → Format conversion → Tokenization → Training → Evaluation → Export
   Include a state machine diagram of the pipeline.

2. METHOD COMPARISON with decision criteria:
   | Method       | VRAM Required | Training Speed | Quality | When to Use |
   | Full FT      |               |                |         |             |
   | LoRA         |               |                |         |             |
   | QLoRA        |               |                |         |             |
   | PEFT/Adapters|               |                |         |             |
   | Prefix Tuning|               |                |         |             |
   Include GPU memory calculations for 7B, 13B, 70B models.

3. DATASET PREPARATION:
   - Format requirements for SFT (instruction-response pairs)
   - Format for DPO (chosen/rejected pairs)
   - Format for RLHF
   - Data quality filters and deduplication strategies
   - Recommended dataset sizes by task type
   - Working code to convert CSV/JSON to training format

4. HYPERPARAMETER TUNING GUIDE:
   - Learning rate schedules (cosine, linear warmup)
   - Batch size vs gradient accumulation tradeoffs
   - LoRA rank and alpha selection heuristics
   - Epoch count by dataset size
   - Provide a hyperparameter cheat sheet table

5. TRAINING SCRIPT TEMPLATES:
   - HuggingFace Transformers + PEFT + BitsAndBytes
   - TRL (SFTTrainer, DPOTrainer)
   - Weights & Biases logging integration
   - Multi-GPU training with Accelerate/DeepSpeed
   - Working, runnable code (not pseudocode)

6. EVALUATION FRAMEWORK:
   - Perplexity measurement
   - Task-specific metrics (BLEU, ROUGE, F1, BERTScore)
   - Human evaluation protocols
   - A/B comparison framework
   - Overfitting detection checklist

7. POST-TRAINING OPTIMIZATION:
   - GGUF quantization pipeline
   - ONNX export
   - vLLM serving optimization
   - Merging LoRA adapters back to base model
   - Benchmarking inference speed

Output format: engineer-ready reference document with all code blocks runnable.
```

## Skill Builder Prompt
```
Create a production-ready SKILL.md for the "finetuning" skill.

YAML Frontmatter:
---
name: finetuning
description: "Use this skill when tasked with fine-tuning, optimizing, or adapting
a machine learning model or LLM. Covers dataset preparation, training configuration,
LoRA/QLoRA/PEFT setup, evaluation, and post-training optimization."
---

The skill workflow must cover:
Phase 1 — Data Audit & Preparation
Phase 2 — Method Selection (decision matrix)
Phase 3 — Training Configuration
Phase 4 — Training Execution & Monitoring
Phase 5 — Evaluation & Validation
Phase 6 — Post-Training Optimization & Export

Each phase must specify:
- Required inputs
- Actions the agent takes
- Artifacts produced
- Validation gates (what must pass before next phase)
- Failure recovery

Include embedded decision tables and anti-patterns.
```

## Instruction Builder Prompt
```
Generate instructions.md for the "finetuning" skill.

Write step-by-step execution instructions for an AI agent:

1. How to assess whether fine-tuning is actually needed vs prompting/RAG
2. How to audit and prepare the training dataset (with code templates)
3. How to select the right fine-tuning method based on constraints
4. How to configure and launch training (exact commands)
5. How to monitor training (Weights & Biases, loss curves, gradient norms)
6. How to evaluate the fine-tuned model (exact metrics and code)
7. How to optimize and export the model for serving
8. How to document the entire experiment (experiment log template)

Each step must include:
- The exact tools/commands the agent runs
- Decision criteria for branching logic
- Checklist items the agent verifies
```

## Debug Prompt
```
Stress-test the finetuning skill against these failure scenarios:

1. CUDA OUT OF MEMORY during training
   → Detection: watch nvidia-smi, catch RuntimeError
   → Fixes: reduce batch size, enable gradient checkpointing, switch to QLoRA,
     reduce sequence length
   → Test: attempt training with batch_size=32 on a 7B model with 8GB VRAM

2. BAD DATASET FORMATTING
   → Missing columns, wrong JSON structure, encoding errors
   → The skill must validate dataset schema BEFORE tokenization

3. TOKENIZATION ERRORS
   → Special tokens not added, chat template mismatch, truncation too aggressive
   → The skill must run a tokenization sanity check on 10 samples

4. OVERFITTING
   → Training loss drops, validation loss increases after epoch 2
   → Detection: mandatory val loss tracking every N steps
   → Fixes: early stopping, dropout, reduce epochs, increase data

5. CATASTROPHIC FORGETTING
   → Model loses general capability after fine-tuning
   → Detection: benchmark on general tasks before and after
   → Fixes: lower learning rate, use LoRA with low rank, replay buffer

6. ADAPTER MERGE CORRUPTION
   → Merged model produces garbage after LoRA merge
   → Detection: inference test suite pre/post merge
   → Fixes: verify base model version match, check dtype consistency

For each: failure description, root cause analysis, diagnostic steps, fix, test case.
```

## Test Prompts
```
Test 1 — Method Selection:
"I have 500 instruction-response pairs and a single A100. Fine-tune Llama-3-8B."
Expected: Agent selects LoRA, configures PEFT, produces training script.

Test 2 — Data Validation:
Provide a CSV with 3 missing columns and bad encoding.
Expected: Agent detects issues, reports them, and refuses to proceed until fixed.

Test 3 — Overfitting Detection:
Simulate training where val_loss increases after epoch 2.
Expected: Agent triggers early stopping and reports the issue.

Test 4 — Resource Constraint:
"Fine-tune a 70B model on a laptop with 16GB RAM."
Expected: Agent recommends QLoRA with 4-bit quantization or cloud training.

Test 5 — Export Pipeline:
"Convert the fine-tuned model to GGUF for llama.cpp."
Expected: Agent produces the exact conversion commands and verifies output.
```

## Expected Outputs
- `dataset_audit_report.md` — data quality assessment
- `training_config.yaml` — all hyperparameters documented
- `train.py` — complete, runnable training script
- `eval_report.md` — evaluation metrics and analysis
- `experiment_log.md` — full experiment metadata
- Optimized model artifacts (GGUF, ONNX, merged weights)
- `hyperparameter_cheatsheet.md`

## Edge Cases

| Edge Case | Risk | Mitigation |
|-----------|------|------------|
| Dataset has only 50 samples | Severe overfitting | Recommend few-shot prompting instead; if FT required, use high dropout and 1 epoch |
| No GPU available | Cannot train | Recommend cloud GPU (Colab, RunPod, Lambda) or API-based fine-tuning (OpenAI, Together) |
| Base model is gated (Llama, Gemma) | Download fails | Check HF token and model access agreement before training setup |
| Mixed-language dataset | Tokenizer coverage gaps | Verify tokenizer vocabulary coverage, consider multilingual base model |
| Training data contains PII | Legal/compliance risk | Run PII detection scan before training, flag for human review |

---

# Skill 3 — Data Preprocessing + Evaluation + Testing

## Skill Name
`data-pipeline`

## Responsibility Mapping
> *"Perform data preprocessing, model evaluation, and performance testing."*

## Skill Objective
Provide a complete, reusable pipeline skill that takes raw data (NLP, tabular, image), cleans and transforms it, evaluates ML/LLM models against structured metrics, and runs performance/load tests on AI APIs — producing preprocessing scripts, evaluation reports, and load test configurations.

## Research Prompt
```
You are a senior data engineer and ML evaluation specialist.

Produce a deeply practical engineering guide covering:

1. DATA PREPROCESSING WORKFLOWS by modality:
   NLP: tokenization, normalization, deduplication, language detection,
        encoding handling, stopword removal, chunking for RAG
   Tabular: missing value imputation, outlier detection, feature scaling,
            encoding categoricals, train/val/test splitting
   Image: resizing, augmentation, normalization, format conversion,
          annotation validation

   For each modality: provide complete Python code using pandas, numpy, PIL,
   HuggingFace datasets, and scikit-learn.

2. EVALUATION METRICS by task type:
   | Task           | Metrics                                    | Library         |
   | Classification | accuracy, precision, recall, F1, AUC-ROC   | sklearn         |
   | Regression     | MSE, RMSE, MAE, R²                         | sklearn         |
   | Generation     | BLEU, ROUGE, BERTScore, perplexity         | evaluate, nltk  |
   | Retrieval      | Recall@K, MRR, nDCG, MAP                   | custom          |
   | Ranking        | Spearman correlation, Kendall tau           | scipy           |

   Include code for EVERY metric.

3. AUTOMATED EVALUATION PIPELINE:
   A reusable Python class that:
   - Takes model + test dataset
   - Runs all relevant metrics
   - Produces a structured JSON report
   - Generates visualizations (confusion matrix, ROC, precision-recall curve)

4. PERFORMANCE TESTING for AI APIs:
   - Load testing with locust: complete locustfile.py example
   - Latency profiling: p50, p95, p99 measurement
   - Throughput benchmarking: requests/second under load
   - Memory profiling during inference
   - GPU utilization monitoring

5. DATA QUALITY CHECKLIST:
   20-item checklist covering: completeness, consistency, accuracy,
   timeliness, uniqueness, validity. With automated check code for each.

Output must contain runnable code for every section.
```

## Skill Builder Prompt
```
Create SKILL.md for the "data-pipeline" skill.

YAML:
---
name: data-pipeline
description: "Use this skill when tasked with data preprocessing, cleaning,
transformation, model evaluation, metric computation, or performance/load
testing of AI systems and APIs."
---

Workflow:
Phase 1 — Data Ingestion & Profiling
Phase 2 — Data Cleaning & Transformation
Phase 3 — Data Validation & Quality Checks
Phase 4 — Model Evaluation & Metrics
Phase 5 — Performance & Load Testing
Phase 6 — Report Generation

Each phase produces specific artifacts with validation gates.
Include decision tables for preprocessing strategy selection.
```

## Instruction Builder Prompt
```
Generate instructions.md for the "data-pipeline" skill.

Write execution instructions covering:
1. How the agent identifies data modality and selects preprocessing strategy
2. Step-by-step data cleaning operations with code
3. How to split data correctly (avoiding leakage)
4. How to run evaluation metrics and interpret results
5. How to set up and run load tests
6. How to generate the final quality/evaluation report
7. Format and naming conventions for all output files
```

## Debug Prompt
```
Stress-test the data-pipeline skill:

1. MISSING VALUES: 60% of a critical column is NaN
   → Skill must decide: impute, drop, or flag for human review

2. DATA LEAKAGE: Test data accidentally included in training set
   → Skill must detect via hash comparison or timestamp analysis

3. IMBALANCED DATASET: 99:1 class ratio
   → Skill must recommend: SMOTE, class weights, stratified sampling

4. ENCODING ERRORS: Mixed UTF-8/Latin-1 in CSV
   → Skill must detect encoding, handle gracefully

5. CORRUPT FILES: Truncated images, malformed JSON
   → Skill must validate file integrity before processing

6. METRIC SELECTION ERROR: Using accuracy on imbalanced classification
   → Skill must flag inappropriate metrics and suggest alternatives

For each: diagnostic steps, expected behavior, recommended fix.
```

## Test Prompts
```
Test 1: "Clean this CSV with 10K rows, 15% missing values, 3 datetime columns."
Expected: Agent produces cleaned dataset + data quality report.

Test 2: "Evaluate my text classifier on this test set."
Expected: Agent computes precision, recall, F1, confusion matrix, generates report.

Test 3: "Load test my FastAPI model endpoint at /predict."
Expected: Agent generates locustfile.py, runs test, produces latency report.

Test 4: "Check this dataset for data leakage."
Expected: Agent runs overlap detection between train/test splits.
```

## Expected Outputs
- `data_quality_report.md` — profiling and quality assessment
- `preprocessing_pipeline.py` — reusable cleaning script
- `eval_report.md` — metrics, charts, analysis
- `eval_harness.py` — automated evaluation class
- `locustfile.py` — load testing configuration
- `performance_report.md` — latency percentiles, throughput, resource usage
- Visualizations: confusion matrices, ROC curves, distribution plots

## Edge Cases

| Edge Case | Risk | Mitigation |
|-----------|------|------------|
| Dataset too large for memory | OOM crash | Use chunked processing, Dask, or streaming |
| All values in a column are identical | Feature is useless, may cause division by zero | Detect and auto-drop constant columns |
| Datetime formats vary across rows | Parsing errors | Use `dateutil.parser` with fallback chain |
| Labels have typos ("positive", "Positive", "pos") | Inflated class count | Normalize labels before evaluation |
| Model returns probabilities but test expects classes | Metric computation fails | Auto-detect output format and threshold |

---

# Skill 4 — AI Integration with Applications

## Skill Name
`ai-integration`

## Responsibility Mapping
> *"Collaborate with development and product teams to integrate AI solutions into applications."*

## Skill Objective
Enable an AI agent to expose ML models as production APIs, containerize them, define API contracts, generate integration documentation, and produce client SDK stubs — bridging the gap between data science outputs and application engineering.

## Research Prompt
```
You are a senior backend/ML platform engineer.

Produce a practical engineering guide for integrating AI models into
production applications:

1. MODEL SERVING PATTERNS:
   - Synchronous API (request-response)
   - Asynchronous API (queue-based, webhook callback)
   - Streaming (SSE, WebSocket for LLM generation)
   - Batch inference (scheduled jobs)
   Decision matrix: when to use each pattern.

2. API DESIGN FOR ML MODELS:
   - RESTful endpoint design for prediction APIs
   - Request/response schema design (Pydantic models)
   - Versioning strategies (URL, header, content-type)
   - Error handling patterns for ML (confidence thresholds, fallbacks)
   - Rate limiting and authentication
   Working FastAPI example with full endpoint implementation.

3. CONTAINERIZATION:
   - Multi-stage Dockerfile for ML applications
   - Docker Compose for local development
   - GPU-enabled containers (NVIDIA Docker)
   - Health checks and readiness probes
   - Environment variable management
   Complete, production-ready Dockerfile template.

4. API CONTRACT SPECIFICATION:
   - OpenAPI 3.0 schema generation from FastAPI
   - Request/response examples
   - Error response catalog
   - SDK generation from OpenAPI spec

5. INTEGRATION DOCUMENTATION TEMPLATE:
   - Getting started guide for frontend developers
   - Authentication guide
   - Endpoint reference
   - Code examples in Python, JavaScript, cURL
   - Troubleshooting guide

6. CROSS-TEAM COLLABORATION PATTERNS:
   - API contract review workflow
   - Staging environment setup
   - Integration testing strategy
   - Feature flag patterns for AI rollout
```

## Skill Builder Prompt
```
Create SKILL.md for the "ai-integration" skill.

YAML:
---
name: ai-integration
description: "Use this skill when tasked with exposing an ML model as an API,
containerizing an AI application, creating API contracts, writing integration
documentation, or helping developers consume AI services."
---

Workflow:
Phase 1 — Serving Pattern Selection
Phase 2 — API Design & Implementation
Phase 3 — Containerization
Phase 4 — Contract Definition & SDK Generation
Phase 5 — Integration Documentation
Phase 6 — Integration Testing

Include: endpoint templates, Dockerfile templates, OpenAPI examples.
```

## Instruction Builder Prompt
```
Generate instructions.md for the "ai-integration" skill.

Cover:
1. How the agent determines the right serving pattern
2. Step-by-step API creation with FastAPI
3. How to build and test Docker containers
4. How to generate and validate OpenAPI specs
5. How to produce integration documentation
6. How to set up integration tests
7. Handoff protocol to frontend/product teams
```

## Debug Prompt
```
Stress-test the ai-integration skill:

1. API LATENCY > 5 seconds per request
   → Profiling steps, model optimization, caching strategies

2. INVALID REQUEST PAYLOADS
   → Pydantic validation, error messages, request schema documentation

3. MODEL RESPONSE FAILURES (null outputs, exceptions)
   → Fallback responses, circuit breaker pattern, error logging

4. CONTAINER BUILD FAILURES
   → Dependency conflicts, missing system libraries, GPU driver mismatch

5. VERSION MISMATCH (model v2 deployed but API expects v1 schema)
   → Schema versioning checks, backwards compatibility validation

6. COLD START LATENCY (serverless/container startup too slow)
   → Model preloading, keep-alive strategies, warm pool config

For each: root cause, detection mechanism, fix, prevention.
```

## Test Prompts
```
Test 1: "Expose my sentiment analysis model as a REST API."
Expected: FastAPI app, Pydantic schemas, Dockerfile, OpenAPI spec.

Test 2: "Create integration docs for our prediction API."
Expected: Getting started guide, auth guide, code examples in 3 languages.

Test 3: "Containerize my LLM application with GPU support."
Expected: Multi-stage Dockerfile with NVIDIA runtime, docker-compose.yml.

Test 4: "Add streaming support for our text generation endpoint."
Expected: SSE endpoint with proper chunked response handling.
```

## Expected Outputs
- `main.py` — FastAPI application with model serving
- `schemas.py` — Pydantic request/response models
- `Dockerfile` + `docker-compose.yml`
- `openapi.json` — API contract specification
- `integration_guide.md` — developer documentation
- `test_integration.py` — integration test suite
- Client SDK stubs (Python, JavaScript)

## Edge Cases

| Edge Case | Risk | Mitigation |
|-----------|------|------------|
| Model too large to fit in container | Build/deploy fails | Use model download at startup, external model storage |
| Concurrent requests cause race conditions | Inconsistent predictions | Implement request isolation, stateless inference |
| Frontend sends unexpected data types | API crashes silently | Strict Pydantic validation with clear error messages |
| API works locally but fails in Kubernetes | Environment mismatch | Environment parity checks, staging validation |
| Model updates break existing integrations | Downstream failures | Semantic versioning, deprecation warnings, canary deploys |

---

# Skill 5 — AI Research and Technology Exploration

## Skill Name
`research`

## Responsibility Mapping
> *"Contribute to research and implementation of emerging AI technologies."*

## Skill Objective
Enable an AI agent to systematically discover, evaluate, and prototype emerging AI technologies — producing research summaries, technology comparison matrices, Proof-of-Concept implementations, and tech spike reports that inform engineering decisions.

## Research Prompt
```
You are a senior AI researcher bridging academia and industry.

Produce a practical guide covering:

1. RESEARCH DISCOVERY FRAMEWORK:
   - Top sources: arXiv, Papers With Code, Semantic Scholar, HuggingFace
   - How to set up automated paper tracking (RSS, API alerts)
   - How to evaluate paper relevance: checklist of 10 criteria
   - Speed-reading protocol: abstract → figures → results → method (15 min)

2. TECHNOLOGY EVALUATION MATRIX:
   Template for comparing emerging technologies:
   | Criterion        | Weight | Tech A | Tech B | Tech C |
   | Maturity         |        |        |        |        |
   | Community Size   |        |        |        |        |
   | Documentation    |        |        |        |        |
   | Performance      |        |        |        |        |
   | Integration Cost |        |        |        |        |
   | Maintenance Risk |        |        |        |        |

3. PROOF-OF-CONCEPT (PoC) WORKFLOW:
   - Time-boxed sprint: 2-day maximum
   - PoC folder structure and boilerplate
   - Success/failure criteria defined BEFORE implementation
   - PoC report template

4. TECH SPIKE REPORT TEMPLATE:
   - Problem statement
   - Technologies evaluated
   - Comparison matrix
   - PoC results
   - Recommendation with risk assessment
   - Next steps

5. AI TOOLING LANDSCAPE (current):
   Categorized overview of tools in:
   - LLM inference, fine-tuning, evaluation
   - Vector databases, embedding models
   - Agent frameworks, orchestration
   - Deployment, monitoring, observability
```

## Skill Builder Prompt
```
Create SKILL.md for the "research" skill.

YAML:
---
name: research
description: "Use this skill when tasked with researching emerging AI technologies,
evaluating new tools or frameworks, reading and summarizing papers, or building
proof-of-concept implementations for technology assessment."
---

Workflow:
Phase 1 — Research Discovery & Paper Selection
Phase 2 — Technology Evaluation & Comparison
Phase 3 — Proof-of-Concept Implementation
Phase 4 — Tech Spike Report Generation
Phase 5 — Recommendation & Next Steps
```

## Instruction Builder Prompt
```
Generate instructions.md for the "research" skill:

1. How the agent searches for relevant papers and tools
2. How to evaluate technology maturity and fit
3. How to set up and execute a time-boxed PoC
4. How to write the tech spike report
5. How to present recommendations for different audiences
   (technical team vs product team vs leadership)
```

## Debug Prompt
```
Stress-test the research skill:

1. PAPER CLAIMS DON'T REPRODUCE
   → PoC fails to match reported metrics
   → Agent must document discrepancy and assess root cause

2. TOO MANY OPTIONS
   → 15 competing tools for the same problem
   → Agent must apply systematic elimination criteria

3. TECHNOLOGY IS TOO IMMATURE
   → No documentation, breaking API changes weekly
   → Agent must assess maturity risk and recommend alternatives

4. POC SUCCEEDS BUT DOESN'T SCALE
   → Works on toy data, fails at production volume
   → Agent must include scalability criteria in evaluation

5. RESEARCH IS OUTDATED
   → Paper from 6 months ago superseded by newer approach
   → Agent must check recency and citations
```

## Test Prompts
```
Test 1: "Research the best vector database for our RAG pipeline."
Expected: Comparison matrix (Pinecone vs Weaviate vs Chroma vs Qdrant),
PoC with top 2, recommendation report.

Test 2: "Summarize this arXiv paper and assess if we should adopt the technique."
Expected: Structured summary, relevance assessment, feasibility analysis.

Test 3: "What's the current state of agentic AI frameworks?"
Expected: Categorized landscape overview with maturity ratings.
```

## Expected Outputs
- `research_summary.md` — paper/technology summary
- `tech_comparison_matrix.md` — weighted evaluation table
- `poc/` — proof-of-concept code and results
- `tech_spike_report.md` — full evaluation report
- `recommendation.md` — actionable next steps

## Edge Cases

| Edge Case | Risk | Mitigation |
|-----------|------|------------|
| No relevant papers exist for the topic | Agent fabricates citations | Verify every reference URL, admit knowledge gaps |
| Technology has no Python SDK | Cannot prototype quickly | Assess API-based integration or community wrappers |
| Conflicting benchmarks from different sources | Unclear which to trust | Run independent benchmarks when possible |
| Research rabbit hole — agent spends too long | Time waste | Enforce time-box: max 2 hours research, then report what's found |
| Emerging tech has licensing issues (GPL, proprietary) | Legal risk | Always check and document license in evaluation |

---

# Skill 6 — Technical Documentation

## Skill Name
`documentation`

## Responsibility Mapping
> *"Maintain proper technical documentation for AI workflows and deployments."*

## Skill Objective
Enable an AI agent to automatically generate, update, and maintain comprehensive technical documentation for AI systems — including model cards, experiment logs, deployment runbooks, API documentation, and architecture decision records.

## Research Prompt
```
You are a technical documentation specialist for AI/ML systems.

Produce a comprehensive guide covering:

1. MODEL CARD STANDARD:
   Based on the Google Model Cards framework, produce a complete template:
   - Model details (name, version, type, framework)
   - Intended use and out-of-scope use cases
   - Training data summary
   - Evaluation metrics and results
   - Ethical considerations and limitations
   - Maintenance and update schedule

2. EXPERIMENT LOG TEMPLATE:
   - Experiment ID, date, objective
   - Hypothesis
   - Dataset used (version, size, splits)
   - Model configuration (architecture, hyperparameters)
   - Results (metrics, artifacts, observations)
   - Conclusions and next steps
   - Reproducibility checklist

3. DEPLOYMENT RUNBOOK TEMPLATE:
   - Pre-deployment checklist
   - Step-by-step deployment procedure
   - Environment configuration
   - Smoke test commands
   - Rollback procedure
   - Monitoring setup verification
   - Incident response contacts

4. API DOCUMENTATION TEMPLATE:
   - Overview and authentication
   - Endpoints with request/response examples
   - Error codes and troubleshooting
   - Rate limits and quotas
   - SDKs and client libraries
   - Changelog

5. ARCHITECTURE DECISION RECORDS (ADR):
   - Title, status, date
   - Context (why this decision matters)
   - Decision (what we chose)
   - Alternatives considered
   - Consequences (tradeoffs accepted)

6. DOCUMENTATION AUTOMATION:
   - Auto-generating docs from code (docstrings → Markdown)
   - Auto-generating API docs from OpenAPI spec
   - CI/CD pipeline for documentation (docs as code)
   - Documentation linting and quality checks
```

## Skill Builder Prompt
```
Create SKILL.md for the "documentation" skill.

YAML:
---
name: documentation
description: "Use this skill when tasked with creating, updating, or maintaining
technical documentation for AI systems, including model cards, experiment logs,
deployment runbooks, API docs, and architecture decision records."
---

Workflow:
Phase 1 — Documentation Audit (what exists, what's missing)
Phase 2 — Template Selection
Phase 3 — Content Generation
Phase 4 — Review & Validation
Phase 5 — Integration into CI/CD
```

## Instruction Builder Prompt
```
Generate instructions.md for the "documentation" skill:

1. How the agent determines which documentation type is needed
2. How to select and customize the appropriate template
3. How to extract information from code, configs, and experiment artifacts
4. How to write clear, consistent documentation
5. Formatting standards (Markdown, heading hierarchy, code blocks)
6. How to validate documentation completeness
7. How to set up auto-generation pipelines
```

## Debug Prompt
```
Stress-test the documentation skill:

1. CODE AND DOCS ARE OUT OF SYNC
   → Model v2 deployed but docs still describe v1
   → Detection: compare code version tags with doc metadata

2. MISSING CRITICAL SECTIONS
   → Runbook has no rollback procedure
   → Validation: checklist of required sections per doc type

3. INCORRECT API EXAMPLES
   → Example requests return errors when executed
   → Test: run all examples against staging endpoint

4. STALE EXPERIMENT LOGS
   → 20 experiments not logged
   → Prevention: enforce documentation as part of workflow

5. PLAGIARIZED CONTENT
   → Agent copies documentation from unrelated project
   → Guardrail: all docs must reference actual project artifacts
```

## Test Prompts
```
Test 1: "Generate a model card for my fine-tuned sentiment classifier."
Expected: Complete model card with all standard sections filled.

Test 2: "Create a deployment runbook for our RAG API."
Expected: Step-by-step runbook with checklist, smoke tests, rollback procedure.

Test 3: "Document this API endpoint."
Expected: Endpoint docs with request/response examples, error codes.

Test 4: "Write an ADR for choosing Pinecone over Weaviate."
Expected: Structured ADR with context, decision, alternatives, consequences.
```

## Expected Outputs
- `model_card.md` — complete model documentation
- `experiment_log.md` — structured experiment record
- `deployment_runbook.md` — step-by-step operations guide
- `api_docs.md` — comprehensive API reference
- `adr/` — architecture decision records folder
- `docs_audit_report.md` — gap analysis of existing documentation

## Edge Cases

| Edge Case | Risk | Mitigation |
|-----------|------|------------|
| No code comments or docstrings exist | Agent cannot extract info automatically | Fall back to manual interview mode — ask user targeted questions |
| Multiple conflicting config files | Docs may reference wrong config | Agent must identify the active/production config |
| Model has no evaluation results | Model card is incomplete | Flag as incomplete, recommend running evaluation first |
| Private/sensitive data in docs | Information leak | PII scan on all generated documentation |
| Documentation audience is non-technical | Too much jargon | Provide two versions: technical + executive summary |

---

# Skill 7 — Quality, Scalability, Reliability

## Skill Name
`ai-reliability`

## Responsibility Mapping
> *"Ensure quality, scalability, and reliability of AI-based systems."*

## Skill Objective
Enable an AI agent to implement comprehensive quality assurance, scalability design patterns, observability/monitoring, and reliability engineering for AI systems — producing QA checklists, monitoring configurations, scaling strategies, and incident response playbooks.

## Research Prompt
```
You are a senior ML platform reliability engineer.

Produce an exhaustive engineering guide covering:

1. AI SYSTEM TESTING STRATEGIES:
   - Unit tests for ML code (data processing, feature engineering)
   - Integration tests for model serving APIs
   - Model quality tests (accuracy regression, distribution shift detection)
   - Shadow mode testing (parallel routing: old model + new model)
   - A/B testing framework for model comparison
   - Chaos engineering for AI (what happens when model service dies?)
   Include pytest examples for each test type.

2. SCALABILITY DESIGN PATTERNS:
   - Horizontal scaling for inference (load balancer + replicas)
   - Batching strategies (dynamic batching, continuous batching)
   - Caching strategies (prompt cache, embedding cache, response cache)
   - Async processing (message queues: Redis, RabbitMQ, SQS)
   - Auto-scaling policies (CPU, GPU, request-based triggers)
   - Database scaling (read replicas, sharding for vector stores)

3. MODEL SERVING OPTIMIZATION:
   - Quantization (INT8, INT4, GPTQ, AWQ)
   - Model distillation
   - Hardware optimization (TensorRT, ONNX Runtime, vLLM)
   - Concurrent request handling
   - Memory optimization (KV cache management)

4. OBSERVABILITY & MONITORING:
   - Metrics to track: latency (p50/p95/p99), throughput, error rate,
     GPU utilization, memory usage, model confidence distribution
   - Prometheus + Grafana setup for ML services
   - Log aggregation (structured logging for ML pipelines)
   - Alerting rules and thresholds
   - Distributed tracing for multi-service AI systems

5. MODEL DRIFT DETECTION:
   - Data drift (input distribution shift)
   - Concept drift (relationship between input and output changes)
   - Prediction drift (output distribution shift)
   - Detection methods: PSI, KL divergence, statistical tests
   - Automated retraining triggers

6. INCIDENT RESPONSE for AI systems:
   - Incident classification (model degradation vs outage vs data corruption)
   - Response playbook template
   - Rollback procedures (model version rollback, canary analysis)
   - Post-mortem template for AI incidents
   - SLA definitions for AI services

7. QA CHECKLIST for AI deployments:
   30-item checklist covering: code quality, model quality, data quality,
   security, performance, monitoring, documentation, compliance.
```

## Skill Builder Prompt
```
Create SKILL.md for the "ai-reliability" skill.

YAML:
---
name: ai-reliability
description: "Use this skill when tasked with ensuring quality, scalability,
or reliability of an AI system. Covers testing strategies, scaling patterns,
monitoring setup, drift detection, incident response, and production QA."
---

Workflow:
Phase 1 — Quality Assessment (current state audit)
Phase 2 — Test Suite Design & Implementation
Phase 3 — Scalability Architecture
Phase 4 — Monitoring & Observability Setup
Phase 5 — Drift Detection Configuration
Phase 6 — Incident Response Playbook
Phase 7 — QA Checklist Validation
```

## Instruction Builder Prompt
```
Generate instructions.md for the "ai-reliability" skill:

1. How the agent audits the current quality/reliability posture
2. How to design and implement the test suite
3. How to assess scalability requirements and implement patterns
4. How to set up monitoring (Prometheus, Grafana, alerting)
5. How to configure drift detection pipelines
6. How to create an incident response playbook
7. How to run the QA checklist and produce the report
8. When to flag issues for human review
```

## Debug Prompt
```
Stress-test the ai-reliability skill:

1. MODEL DRIFT DETECTED but no retraining pipeline exists
   → Agent must scaffold an automated retraining workflow

2. LATENCY SPIKES under load (p99 > 10s)
   → Profiling steps: is it model inference, data loading, or network?
   → Fixes: batching, caching, model optimization, horizontal scaling

3. SCALING FAILURE: auto-scaler creates pods but model fails to load
   → Detection: health check failures, OOM kills
   → Fixes: resource limits, model preloading, readiness probes

4. MONITORING BLIND SPOTS: system crashes but no alert fires
   → Agent must audit alerting coverage against failure modes
   → Must recommend alerts for every critical path

5. SILENT MODEL DEGRADATION: accuracy drops 15% but no one notices
   → Agent must implement automated quality gates with thresholds

6. DATA PIPELINE CORRUPTION: training data silently changes
   → Data validation gates, schema enforcement, checksums

For each: detection, root cause analysis, fix, prevention.
```

## Test Prompts
```
Test 1: "Set up monitoring for our model serving API."
Expected: Prometheus metrics, Grafana dashboard config, alerting rules.

Test 2: "Our API latency increased 3x after last deployment. Debug it."
Expected: Profiling steps, root cause analysis, optimization recommendation.

Test 3: "Create a QA checklist for our upcoming model deployment."
Expected: 30-item checklist with pass/fail status for each item.

Test 4: "Design auto-scaling for our model that handles 10K RPM."
Expected: Architecture with load balancer, HPA config, batching strategy.

Test 5: "Set up drift detection for our classifier."
Expected: Data drift + prediction drift pipeline with alerting.
```

## Expected Outputs
- `qa_checklist.md` — comprehensive quality assurance checklist
- `test_suite/` — pytest test files for the AI system
- `scaling_architecture.md` — scalability design document
- `monitoring_config/` — Prometheus rules, Grafana dashboards, alert configs
- `drift_detection.py` — automated drift monitoring script
- `incident_response_playbook.md` — step-by-step incident handling
- `post_mortem_template.md` — incident post-mortem format
- `reliability_report.md` — overall system reliability assessment

## Edge Cases

| Edge Case | Risk | Mitigation |
|-----------|------|------------|
| No existing tests in the codebase | Cannot run quality assessment | Start with smoke tests, build incrementally |
| System has no monitoring at all | Complete observability gap | Deploy minimum viable monitoring first (health + latency + errors) |
| Drift detected but model cannot be retrained (data deleted) | Cannot recover | Implement data retention policies and training data versioning |
| Multi-model system — drift in one model cascades | Complex failure mode | Monitor each model independently + end-to-end system metrics |
| Cost of scaling exceeds budget | Cannot meet SLAs | Right-size models, optimize inference, implement request prioritization |
| Team has no incident response experience | Slow recovery from outages | Run tabletop exercises, document everything, automate rollback |
