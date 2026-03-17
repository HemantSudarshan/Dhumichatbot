# AI Solution Development — Agent Instructions

## How This Skill Activates

1. The agent reads the YAML frontmatter of this skill during discovery.
2. If the user's request semantically matches "developing an AI solution," "building an ML app," "deploying a model," or "designing AI architecture," this skill is loaded fully into context.
3. Upon activation, read the entire SKILL.md to understand the 7-phase workflow.

## Execution Instructions

### Step 1 — Collect Requirements

When receiving a new AI solution request:

1. Read the user's problem statement carefully.
2. If the statement contains fewer than 3 concrete requirements, **STOP** and ask:
   - "What specific problem are you trying to solve?"
   - "What data do you have available?"
   - "What are your latency and budget constraints?"
   - "Who will use this system?"
   - "How will you measure success?"
3. Do NOT proceed until you have answers to at least 4 of these questions.
4. Document all requirements in `problem_specification.md`.

### Step 2 — Decompose the Problem

1. Classify the ML problem type using the decision table in SKILL.md Phase 1.
2. List all data requirements: type, volume, labeling status, format.
3. Map business KPIs to ML metrics:
   - "More sales" → conversion rate → click prediction accuracy
   - "Faster support" → resolution time → retrieval recall
   - "Better content" → engagement → generation quality (BLEU/human eval)
4. Document constraints: max latency (ms), max cost ($/month), compliance needs.
5. Write the complete `problem_specification.md`.

### Step 3 — Select the Tech Stack

1. Reference the stack decision matrix in SKILL.md Phase 2.
2. Score each candidate stack against the user's constraints.
3. Present the top 2 options to the user with trade-offs.
4. **Wait for user confirmation** before proceeding.
5. Write `stack_decision.md` with the rationale.

### Step 4 — Design Architecture

1. Select the appropriate architecture pattern:
   - Standard API, RAG pipeline, multi-agent, or batch.
2. Draw the data flow (use text-based diagrams with Mermaid syntax).
3. Define API contracts: endpoint paths, request/response schemas.
4. Specify infrastructure requirements.
5. Write `architecture.md`.
6. **Present architecture to user for review** before building.

### Step 5 — Scaffold the Project

1. Create the folder structure defined in SKILL.md Phase 4.
2. Generate all boilerplate files:
   - `main.py` with FastAPI app setup, CORS, health check
   - `config.py` with Pydantic Settings
   - `Dockerfile` with multi-stage build
   - `docker-compose.yml` for local dev
   - `requirements.txt` with pinned versions
   - `.env.example` with all required variables
   - `.gitignore` for Python projects
   - `Makefile` with common commands (run, test, build, deploy)
3. Ensure every file is functional, not placeholder.

### Step 6 — Implement the Solution

1. Implement model loading in `models/predictor.py`:
   - Lazy loading (load model on first request, not at import)
   - Error handling for model load failures
   - GPU/CPU detection
2. Implement business logic in `services/pipeline.py`:
   - Input validation
   - Preprocessing → inference → postprocessing pipeline
3. Implement API routes in `api/routes.py`:
   - Pydantic request/response models
   - Proper HTTP status codes
   - Structured error responses
4. Add structured logging throughout.

### Step 7 — Write Tests

1. Create unit tests for each module.
2. Create integration tests for the API:
   ```python
   # Use TestClient from FastAPI
   from fastapi.testclient import TestClient
   from src.main import app
   
   client = TestClient(app)
   
   def test_health():
       response = client.get("/health")
       assert response.status_code == 200
   
   def test_predict_valid():
       response = client.post("/predict", json={"text": "test input"})
       assert response.status_code == 200
       assert "prediction" in response.json()
   
   def test_predict_empty():
       response = client.post("/predict", json={"text": ""})
       assert response.status_code == 422
   ```
3. Run: `pytest tests/ -v --cov=src --cov-report=term-missing`
4. All tests must pass before proceeding.

### Step 8 — Deploy

1. Build Docker image: `docker build -t solution-name .`
2. Run locally: `docker-compose up`
3. Run smoke tests against the local container
4. Execute the deployment checklist from SKILL.md Phase 7
5. Verify the deployed system responds correctly
6. Generate `deployment_checklist.md` with all items checked

## Interaction Protocol

| Situation | Agent Behavior |
|-----------|---------------|
| Vague problem statement | Ask clarifying questions, do not guess |
| Stack selection | Present top 2 options, let user decide |
| Architecture review | Show design, wait for approval |
| Test failures | Report failures with root cause, suggest fixes |
| Deployment issues | Stop, diagnose, present options |

## Output Files

Every execution of this skill produces:
1. `problem_specification.md`
2. `stack_decision.md`
3. `architecture.md`
4. Complete project scaffold
5. Working implementation code
6. Test suite
7. `deployment_checklist.md`

## Handoff to Other Skills

- If fine-tuning is needed → activate `finetuning` skill
- If RAG pipeline needed → include RAG components in architecture
- If monitoring needed → activate `ai-reliability` skill
- If documentation needed → activate `documentation` skill
