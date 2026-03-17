---
name: documentation
description: "Use this skill when tasked with creating, updating, or maintaining technical documentation for AI systems. Covers model cards, experiment logs, deployment runbooks, API documentation, architecture decision records, and documentation automation."
---

# Technical Documentation

## Overview

This skill automates the creation and maintenance of comprehensive technical documentation for AI systems, including model cards, experiment logs, deployment runbooks, API docs, and architecture decision records (ADRs).

## Supporting References

Load only the reference file you need:
- `references/instructions.md` for the authoring workflow and completeness checks
- `references/debug.md` for doc-quality failure cases and remediation
- `references/tests.md` for validation prompts and expected deliverables

## Required Inputs

1. **Document type** — model card, experiment log, runbook, API doc, or ADR
2. **Subject** — what system/model/API to document
3. **Audience** — technical team, leadership, external developers
4. **Source material** — code, configs, experiment artifacts

## Step-by-Step Workflow

### Phase 1 — Documentation Audit

**Objective**: Assess what exists and what's missing.

1. Scan the project for existing documentation:
   - `README.md`
   - `docs/` folder
   - Code comments and docstrings
   - API specs (OpenAPI)
   - Inline markdown files

2. Generate `docs_audit_report.md`:
   ```markdown
   ## Documentation Audit
   
   | Document Type | Status | Quality | Notes |
   |--------------|--------|---------|-------|
   | README | ✅ Exists | ⚠ Outdated | Missing setup instructions |
   | Model Card | ❌ Missing | N/A | |
   | API Docs | ✅ Exists | ✅ Current | Auto-generated from OpenAPI |
   | Deployment Runbook | ❌ Missing | N/A | |
   | Experiment Logs | ❌ Missing | N/A | |
   | ADRs | ❌ Missing | N/A | |
   ```

---

### Phase 2 — Template Selection

Select template based on document type:

| Document | Template | Key Sections |
|----------|----------|-------------|
| Model Card | Google Model Cards | Details, Use, Training, Evaluation, Ethics |
| Experiment Log | MLflow-style | ID, Hypothesis, Config, Results, Conclusions |
| Deployment Runbook | SRE-style | Pre-checks, Steps, Smoke Test, Rollback |
| API Docs | OpenAPI-based | Endpoints, Auth, Examples, Errors, Changelog |
| ADR | Nygard ADR | Context, Decision, Alternatives, Consequences |

---

### Phase 3 — Content Generation

#### Model Card Template

```markdown
# Model Card: [Model Name]

## Model Details
- **Model Name**: [name]
- **Version**: [version]
- **Type**: [classification/generation/retrieval]
- **Framework**: [PyTorch/TensorFlow/HuggingFace]
- **Base Model**: [if fine-tuned, what was the base]
- **Date**: [YYYY-MM-DD]
- **Author**: [team/person]

## Intended Use
- **Primary Use**: [what the model is designed for]
- **Out-of-Scope Use**: [what the model should NOT be used for]
- **Users**: [who should use this model]

## Training Data
- **Dataset**: [name, version]
- **Size**: [number of samples]
- **Preprocessing**: [what was done to the data]
- **Known Biases**: [document any known biases]

## Evaluation Results
| Metric | Value | Benchmark |
|--------|-------|-----------|
| [metric] | [value] | [comparison] |

## Limitations
- [Known limitation 1]
- [Known limitation 2]

## Ethical Considerations
- [Any ethical concerns with this model]
- [Bias mitigation steps taken]

## Maintenance
- **Update Schedule**: [how often is the model retrained]
- **Monitoring**: [what metrics are tracked in production]
- **Contact**: [who to reach for issues]
```

#### Experiment Log Template

```markdown
# Experiment Log: [Experiment Name]

## Metadata
- **ID**: EXP-[YYYYMMDD]-[SEQ]
- **Date**: [YYYY-MM-DD]
- **Author**: [name]
- **Status**: RUNNING | COMPLETED | FAILED | ABANDONED

## Hypothesis
[What we expect to happen and why]

## Configuration
- **Model**: [model name/version]
- **Dataset**: [dataset name, version, size]
- **Method**: [training method]
- **Hyperparameters**:
  | Parameter | Value |
  |-----------|-------|
  | learning_rate | |
  | batch_size | |
  | epochs | |

## Results
| Metric | Value | vs Baseline |
|--------|-------|-------------|
| | | |

## Observations
[What happened during the experiment]

## Conclusions
[What we learned]

## Next Steps
[What to try next based on these results]

## Reproducibility
- **Code Commit**: [git hash]
- **Data Version**: [hash or version tag]
- **Environment**: [Python version, key package versions]
- **Hardware**: [GPU model, VRAM]
- **Random Seed**: [seed value]
```

#### Deployment Runbook Template

```markdown
# Deployment Runbook: [Service Name]

## Overview
- **Service**: [name]
- **Environment**: [staging/production]
- **Last Updated**: [date]

## Pre-Deployment Checklist
- [ ] All tests pass in CI
- [ ] Code review approved
- [ ] Model evaluation metrics meet threshold
- [ ] Environment variables configured
- [ ] Database migrations run (if applicable)
- [ ] Monitoring dashboards accessible

## Deployment Steps
1. [Step 1 with exact command]
2. [Step 2 with exact command]
3. [Step 3 with exact command]

## Smoke Tests
After deployment, run:
```bash
# Health check
curl -f https://[endpoint]/health

# Prediction test
curl -X POST https://[endpoint]/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "test input"}'
```

## Rollback Procedure
If any smoke test fails:
1. [Rollback step 1]
2. [Rollback step 2]
3. [Notify team]

## Post-Deployment
- [ ] Verify monitoring shows healthy metrics
- [ ] Check error rate < 0.1%
- [ ] Verify latency p95 < [threshold]
- [ ] Update documentation
```

#### Architecture Decision Record Template

```markdown
# ADR-[NUMBER]: [Title]

## Status
PROPOSED | ACCEPTED | DEPRECATED | SUPERSEDED BY ADR-[N]

## Date
[YYYY-MM-DD]

## Context
[Why are we making this decision? What problem are we solving?]

## Decision
[What did we decide?]

## Alternatives Considered
### Option A: [Name]
- Pros: ...
- Cons: ...

### Option B: [Name]
- Pros: ...
- Cons: ...

## Consequences
### Positive
- [benefit 1]
- [benefit 2]

### Negative
- [tradeoff 1]
- [tradeoff 2]

### Risks
- [risk 1 and mitigation]
```

---

### Phase 4 — Review & Validation

1. **Completeness check**: Verify all required sections are filled.
2. **Accuracy check**: Cross-reference with code and configs.
3. **Readability check**: Appropriate for the target audience.
4. **Freshness check**: All dates and versions current.

---

### Phase 5 — Documentation Maintenance

1. **When to update**: After any code change that affects behavior.
2. **Update protocol**: Modify doc, update date, add changelog entry.
3. **Automation**: Set up pre-commit hooks to lint documentation.

---

## Anti-Patterns — DO NOT

| Anti-Pattern | Consequence | Correct Approach |
|-------------|-------------|------------------|
| Write docs after the project is done | Forgotten details, incomplete docs | Document as you build |
| Copy docs from another project without editing | Inaccurate, misleading | Always customize for the specific system |
| Skip evaluation results in model card | No trust in the model | Always include empirical metrics |
| Write a runbook without testing it | Fails during actual deployment | Execute the runbook once before finalizing |
| Omit rollback procedure | Cannot recover from bad deployments | Always document how to undo |

## Skill Coordination

- Use `ai-solution-dev` when the documentation task depends on unfinished architecture or delivery decisions.
- Use `finetuning` to gather training and evaluation details for model cards and experiment logs.
- Use `ai-integration` for endpoint contracts and serving behavior that must be documented accurately.
- Use `ai-reliability` for monitoring, SLO, and incident response details used in runbooks.
- Use `research` when documentation needs technology assessment context or ADR inputs.
