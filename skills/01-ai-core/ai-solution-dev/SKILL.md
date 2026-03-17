---
name: ai-solution-dev
description: "Use this skill when tasked with developing an AI-powered solution from a client problem statement, designing system architecture, scaffolding a project, selecting an AI/ML tech stack, or deploying an ML/LLM application to production."
---

# AI Solution Development & Deployment

## Overview

This skill guides you through the complete lifecycle of building and deploying AI-powered software solutions — from an ambiguous client problem statement to a production-ready deployed system.

## Supporting References

Load only the reference file you need:
- `references/instructions.md` for the execution protocol and interaction rules
- `references/debug.md` for failure diagnosis and recovery
- `references/tests.md` for acceptance tests and regression prompts

## Required Inputs

Before executing, collect these from the user:
1. **Problem statement** — what business problem needs solving?
2. **Data availability** — what data exists? Format? Volume? Quality?
3. **Deployment constraints** — latency requirements? Budget? Infrastructure?
4. **Users** — who will use this? Technical or non-technical?
5. **Success criteria** — how do we know this works?

> **CRITICAL**: If the problem statement is vague (fewer than 3 concrete requirements), you MUST ask clarifying questions before proceeding. Never guess.

## Step-by-Step Workflow

### Phase 1 — Problem Decomposition

**Objective**: Break down the problem into engineering fundamentals.

1. Identify the ML problem type:
   | Problem Pattern | ML Type | Example |
   |----------------|---------|---------|
   | "Categorize X" | Classification | Spam detection, sentiment |
   | "Predict a number" | Regression | Pricing, demand forecasting |
   | "Generate text" | Text Generation | Chatbots, summarization |
   | "Find similar items" | Retrieval/Ranking | Search, recommendations |
   | "Extract information" | NER/Extraction | Resume parsing, invoice reading |
   | "Answer questions about documents" | RAG | Knowledge bases, support bots |

2. Document data requirements (volume, labeling status, format)
3. Define success metrics: map business KPIs → ML metrics
4. Identify constraints: latency SLA, throughput, cost ceiling, compliance

**Output**: `problem_specification.md`

---

### Phase 2 — Stack Selection

**Objective**: Choose the optimal technology stack based on constraints.

**Decision Matrix**:

| Factor | OpenAI API | HuggingFace | LangChain | FastAPI + vLLM | LlamaIndex |
|--------|-----------|-------------|-----------|----------------|------------|
| **Setup Speed** | ★★★★★ | ★★★ | ★★★★ | ★★ | ★★★★ |
| **Cost at Scale** | ★★ | ★★★★★ | ★★★ | ★★★★★ | ★★★ |
| **Customization** | ★★ | ★★★★★ | ★★★★ | ★★★★★ | ★★★★ |
| **Latency** | ★★★ | ★★★★ | ★★★ | ★★★★★ | ★★★ |
| **Data Privacy** | ★★ | ★★★★★ | ★★★ | ★★★★★ | ★★★ |

**Rules**:
- Budget < $50/month → Open-source models (HuggingFace + vLLM)
- Need fastest prototype → OpenAI API
- Data privacy critical → Self-hosted models only
- RAG application → LlamaIndex or LangChain + vector DB
- High throughput → FastAPI + vLLM/TGI

**Output**: `stack_decision.md`

---

### Phase 3 — Architecture Design

**Objective**: Design the system architecture.

1. Select architecture pattern:
   - **Simple API**: Single model behind FastAPI (most cases)
   - **RAG Pipeline**: Embedding + Vector DB + LLM chain
   - **Multi-Agent**: Orchestrator + specialized worker agents
   - **Batch Pipeline**: Scheduled processing (ETL + inference)

2. Design data flow diagram
3. Define API contracts (input/output schemas)
4. Plan infrastructure (compute, storage, networking)

**Output**: `architecture.md`

---

### Phase 4 — Project Scaffolding

**Objective**: Create the project structure.

```
project_name/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py             # Configuration management
│   ├── models/               # ML model loading and inference
│   │   ├── __init__.py
│   │   └── predictor.py
│   ├── services/             # Business logic
│   │   ├── __init__.py
│   │   └── pipeline.py
│   ├── api/                  # API routes
│   │   ├── __init__.py
│   │   └── routes.py
│   └── utils/                # Shared utilities
│       ├── __init__.py
│       └── logging.py
├── tests/
│   ├── test_api.py
│   ├── test_models.py
│   └── test_services.py
├── configs/
│   └── config.yaml
├── data/
│   └── .gitkeep
├── scripts/
│   ├── setup.sh
│   └── deploy.sh
├── docs/
│   ├── architecture.md
│   └── api_reference.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Makefile
├── .env.example
├── .gitignore
└── README.md
```

**Output**: Complete folder structure with boilerplate files.

---

### Phase 5 — Implementation

**Objective**: Write the working code.

1. Implement model loading and inference (`models/predictor.py`)
2. Implement business logic (`services/pipeline.py`)
3. Implement API endpoints (`api/routes.py`)
4. Implement configuration (`config.py` + `config.yaml`)
5. Write comprehensive error handling
6. Add structured logging

**Rules**:
- Every function has a docstring
- Every API endpoint has Pydantic request/response models
- All secrets come from environment variables (never hardcoded)
- Use async where appropriate for I/O-bound operations

---

### Phase 6 — Testing

**Objective**: Validate the solution works correctly.

1. Write unit tests for model inference
2. Write integration tests for API endpoints
3. Run all tests: `pytest tests/ -v --cov=src`
4. Achieve minimum 80% code coverage
5. Test edge cases: empty input, oversized input, malformed input

---

### Phase 7 — Deployment

**Objective**: Deploy to the target environment.

**Deployment Checklist**:
- [ ] All tests pass
- [ ] Environment variables configured
- [ ] Docker builds successfully
- [ ] Health check endpoint works (`/health`)
- [ ] Smoke test passes (send real request, verify response)
- [ ] Monitoring configured (latency, error rate, throughput)
- [ ] Rollback procedure documented
- [ ] README updated with deployment instructions

**Output**: Deployed system + `deployment_checklist.md`

---

## Anti-Patterns — DO NOT

| Anti-Pattern | Why It's Dangerous | Do This Instead |
|-------------|-------------------|-----------------|
| Hardcode API keys in source code | Security breach | Use .env files and environment variables |
| Skip evaluation, assume model works | Silent failures in production | Always run metrics before deploying |
| Use the largest model available | Cost explosion, latency issues | Start small, scale up only if metrics justify |
| Build everything before testing anything | Wasted effort on wrong solution | Validate at each phase before proceeding |
| Copy-paste boilerplate without understanding | Brittle, unmaintainable code | Understand every line you generate |
| Deploy without a rollback plan | Cannot recover from failures | Always document rollback procedure |

## Failure Recovery

| Phase | Failure | Recovery |
|-------|---------|----------|
| Phase 1 | Cannot determine ML problem type | Ask user for 3 concrete examples of inputs and expected outputs |
| Phase 2 | All stacks exceed budget | Recommend API-based solution with usage caps |
| Phase 3 | Architecture too complex for team size | Simplify to monolith, plan migration path |
| Phase 5 | Model performance inadequate | Escalate to finetuning skill |
| Phase 7 | Deployment fails | Check Docker build logs, verify env vars, test locally first |

## Skill Coordination

- Use `finetuning` when adapting or tuning a model is the main task.
- Use `data-pipeline` when data cleaning, evaluation, or load testing needs deeper treatment.
- Use `ai-integration` when API design and application-facing contracts are the main concern.
- Use `ai-reliability` when the system must be hardened for production.
- Use `documentation` to produce model cards, runbooks, ADRs, and release-facing docs.
- Use `research` when the stack choice depends on comparing unfamiliar tools or papers.
