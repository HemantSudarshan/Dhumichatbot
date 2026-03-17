---
name: skill-router
description: "Cross-skill orchestrator. Use ONLY when a task spans multiple skills or phases and you need to decide the execution order. Do not use for single-skill tasks."
---

# Skill Router

You are an AI engineering skills router. Given a problem statement (PS), you identify the right workflow — a sequence of phases and skills to execute.

## Phases

| Phase | Directory | Purpose |
|-------|-----------|---------|
| 0 | `00-plan/` | Architecture, research, brainstorming |
| 1 | `01-ai-core/` | Models, RAG, agents, fine-tuning, LLM patterns |
| 2 | `02-data/` | Pipelines, vectors, databases, embeddings |
| 3 | `03-backend/` | Python, FastAPI, API integration |
| 4 | `04-frontend/` | React, Next.js |
| 5 | `05-secure/` | Auth, API security, code hardening |
| 6 | `06-test/` | TDD, debugging, reliability, improvement |
| 7 | `07-deploy/` | Docker, deployment, monitoring |
| 8 | `08-document/` | Documentation, ADRs |

## Workflow Selection

Match the problem statement to one of these workflows. Load only the skills listed for each phase in order.

### Workflow A — Build a RAG System
**Trigger:** PS mentions RAG, document Q&A, knowledge base, semantic search, chatbot with retrieval
**Flow:**
1. `00-plan/` → `brainstorming`, `senior-architect`
2. `02-data/` → `data-pipeline`, `vector-database-engineer`, `embedding-strategies`
3. `01-ai-core/` → `rag-engineer`, `rag-implementation`, `prompt-engineering`, `langfuse`
4. `03-backend/` → `ai-integration`, `fastapi-pro`
5. `06-test/` → `ai-reliability`, `test-driven-development`
6. `07-deploy/` → `docker-expert`, `deployment-procedures`

### Workflow B — Build / Fine-Tune a Model
**Trigger:** PS mentions fine-tuning, model training, LoRA, PEFT, model optimization, training pipeline
**Flow:**
1. `00-plan/` → `brainstorming`, `research`
2. `02-data/` → `data-pipeline`, `data-engineer`
3. `01-ai-core/` → `finetuning`, `ai-solution-dev`, `agent-evaluation`, `langfuse`
4. `06-test/` → `ai-reliability`, `systematic-debugging`
5. `08-document/` → `documentation`

### Workflow C — Build an AI Agent
**Trigger:** PS mentions agent, autonomous system, tool use, orchestration, multi-agent, MCP, LangGraph
**Flow:**
1. `00-plan/` → `brainstorming`, `senior-architect`, `architecture-patterns`
2. `01-ai-core/` → `ai-agents-architect`, `langgraph`, `mcp-builder`, `prompt-engineering`, `llm-app-patterns`
3. `02-data/` → `vector-database-engineer`, `embedding-strategies`
4. `03-backend/` → `ai-integration`, `fastapi-pro`, `async-python-patterns`
5. `06-test/` → `agent-evaluation`, `ai-reliability`, `kaizen`
6. `07-deploy/` → `docker-expert`, `observability-engineer`

### Workflow D — Build a REST API / Backend Service
**Trigger:** PS mentions API, REST, backend, microservice, endpoint, CRUD, authentication
**Flow:**
1. `00-plan/` → `brainstorming`, `architecture-decision-records`
2. `03-backend/` → `python-pro`, `fastapi-pro`, `python-patterns`, `async-python-patterns`
3. `02-data/` → `database-design`, `postgres-best-practices`
4. `05-secure/` → `api-security-best-practices`, `auth-implementation-patterns`
5. `06-test/` → `test-driven-development`, `systematic-debugging`
6. `07-deploy/` → `docker-expert`, `deployment-procedures`, `observability-engineer`
7. `08-document/` → `doc-coauthoring`

### Workflow E — Full-Stack Application
**Trigger:** PS mentions full-stack, web app, frontend + backend, React + API, dashboard
**Flow:**
1. `00-plan/` → `brainstorming`, `senior-architect`, `ddd-strategic-design`
2. `03-backend/` → `python-pro`, `fastapi-pro`, `ai-integration`
3. `04-frontend/` → `react-best-practices`, `nextjs-best-practices`
4. `02-data/` → `database-design`, `postgres-best-practices`
5. `05-secure/` → `api-security-best-practices`, `auth-implementation-patterns`, `backend-security-coder`
6. `06-test/` → `test-driven-development`, `systematic-debugging`
7. `07-deploy/` → `docker-expert`, `deployment-procedures`

### Workflow F — End-to-End AI Solution
**Trigger:** PS describes a complete client problem needing AI, mentions "solution", "production system", or spans research → deployment
**Flow:**
1. `00-plan/` → `brainstorming`, `senior-architect`, `architecture-patterns`, `research`
2. `02-data/` → `data-pipeline`, `data-engineer`, `embedding-strategies`
3. `01-ai-core/` → `ai-solution-dev`, `rag-engineer`, `prompt-engineering`, `llm-app-patterns`
4. `03-backend/` → `ai-integration`, `fastapi-pro`, `python-pro`
5. `05-secure/` → `api-security-best-practices`, `security-auditor`
6. `06-test/` → `ai-reliability`, `test-driven-development`, `kaizen`
7. `07-deploy/` → `docker-expert`, `deployment-procedures`, `observability-engineer`
8. `08-document/` → `documentation`, `doc-coauthoring`

### Workflow G — Security Audit / Hardening
**Trigger:** PS mentions security review, vulnerability, audit, hardening, penetration testing
**Flow:**
1. `05-secure/` → `security-auditor`, `api-security-best-practices`, `auth-implementation-patterns`, `backend-security-coder`
2. `06-test/` → `test-driven-development`, `systematic-debugging`
3. `08-document/` → `doc-coauthoring`

### Workflow H — Architecture / Design Planning
**Trigger:** PS mentions system design, architecture, DDD, bounded contexts, technical planning
**Flow:**
1. `00-plan/` → `brainstorming`, `senior-architect`, `architecture-patterns`, `architecture-decision-records`, `ddd-strategic-design`, `ddd-tactical-patterns`
2. `08-document/` → `documentation`, `doc-coauthoring`

## Routing Rules

1. **Always start with Phase 0 (plan)** unless the PS is narrowly scoped (e.g., "fix this bug" or "add rate limiting").
2. **Load skills lazily** — only load skills when the phase starts, not all at once.
3. **Skip phases** that don't apply. Not every workflow needs frontend or security.
4. **Custom skills (★) go deep** — they have `references/` and `agents/` directories. Load the reference files only when you need detailed guidance.
5. **Community skills go broad** — they provide patterns and anti-patterns. Good for orientation.
6. **End with testing and documentation** — always validate before declaring done.

## Skills Index

### 00-plan/ (7 skills)
- `brainstorming` — Structured planning and ideation
- `senior-architect` — High-level design decisions
- `architecture-patterns` — Clean Architecture, DDD, Hexagonal
- `architecture-decision-records` — Document technical decisions
- `ddd-strategic-design` — Bounded contexts, ubiquitous language
- `ddd-tactical-patterns` — Aggregates, value objects, domain events
- `research` ★ — AI technology exploration

### 01-ai-core/ (13 skills)
- `ai-solution-dev` ★ — End-to-end AI solution development
- `finetuning` ★ — Fine-tuning and model optimization
- `ai-agents-architect` — Autonomous AI agent design
- `agent-evaluation` — Agent benchmarking and testing
- `rag-engineer` — RAG system architecture
- `rag-implementation` — Production RAG pipelines
- `langgraph` — Stateful agent workflows
- `mcp-builder` — Model Context Protocol tools
- `prompt-engineering` — Prompt design mastery
- `prompt-caching` — LLM prompt caching
- `context-window-management` — Context optimization
- `llm-app-patterns` — Production LLM patterns
- `langfuse` — LLM observability

### 02-data/ (6 skills)
- `data-pipeline` ★ — Data preprocessing + evaluation
- `data-engineer` — Data pipeline architecture
- `vector-database-engineer` — Vector database mastery
- `embedding-strategies` — Embedding model selection
- `database-design` — Schema design and ORM
- `postgres-best-practices` — PostgreSQL optimization

### 03-backend/ (5 skills)
- `ai-integration` ★ — AI-to-application integration
- `python-pro` — Modern Python 3.12+
- `python-patterns` — Idiomatic Python
- `fastapi-pro` — FastAPI development
- `async-python-patterns` — Python asyncio

### 04-frontend/ (2 skills)
- `react-best-practices` — React optimization
- `nextjs-best-practices` — Next.js App Router

### 05-secure/ (4 skills)
- `api-security-best-practices` — Secure API patterns
- `auth-implementation-patterns` — JWT, OAuth2, sessions
- `backend-security-coder` — Secure backend coding
- `security-auditor` — Security audit methodology

### 06-test/ (4 skills)
- `ai-reliability` ★ — AI quality and reliability
- `test-driven-development` — TDD methodology
- `systematic-debugging` — Structured troubleshooting
- `kaizen` — Iterative improvement loops

### 07-deploy/ (3 skills)
- `docker-expert` — Containers and Compose
- `deployment-procedures` — Rollout strategies
- `observability-engineer` — Monitoring systems

### 08-document/ (2 skills)
- `documentation` ★ — Technical documentation
- `doc-coauthoring` — Structured doc writing

> ★ = Custom JD-specific skill with `references/` and `agents/` subdirectories
