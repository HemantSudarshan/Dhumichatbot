---
name: research
description: "Use this skill when tasked with researching emerging AI technologies, evaluating new tools or frameworks, reading and summarizing research papers, building proof-of-concept implementations, or conducting technology assessments and tech spike reports."
---

# AI Research and Technology Exploration

## Overview

This skill provides a systematic framework for discovering, evaluating, and prototyping emerging AI technologies — turning research into actionable engineering decisions through structured evaluation and PoC development.

## Supporting References

Load only the reference file you need:
- `references/instructions.md` for the research workflow and reporting protocol
- `references/debug.md` for failure patterns in evaluation and PoC work
- `references/tests.md` for validation prompts that check decision quality

## Required Inputs

1. **Research question** — what technology/capability are we evaluating?
2. **Use case context** — why? what problem does it solve?
3. **Constraints** — budget, timeline, tech stack compatibility
4. **Decision scope** — build vs buy? adopt vs wait?

## Step-by-Step Workflow

### Phase 1 — Research Discovery & Scoping

**Objective**: Define what to research and gather sources.

1. **Clarify the research question**:
   - What specific problem needs a solution?
   - What's the decision to be made?
   - Who is the audience for the findings?

2. **Source inventory**:
   | Source Type | Platform | Best For |
   |-----------|----------|----------|
   | Papers | arXiv, Semantic Scholar | Cutting-edge techniques |
   | Benchmarks | Papers With Code | Performance comparisons |
   | Tools | GitHub, HuggingFace | Implementation readiness |
   | Community | Reddit, Twitter/X, Discord | Real-world feedback |
   | Docs | Official documentation | Stability assessment |
   | Tutorials | Medium, YouTube, blogs | Ease of adoption |

3. **Research scope**:
   - Time-box: maximum 2 hours for discovery phase
   - Focus: top 5-7 candidates maximum
   - Output: `research_notes.md` with links and key findings

---

### Phase 2 — Technology Evaluation

**Objective**: Systematically compare candidates.

**Evaluation Matrix Template**:

| Criterion (Weight) | Tech A | Tech B | Tech C |
|-------------------|--------|--------|--------|
| **Maturity** (0.2) | Score 1-5 | Score 1-5 | Score 1-5 |
| **Performance** (0.25) | | | |
| **Community/Support** (0.15) | | | |
| **Documentation** (0.1) | | | |
| **Integration Cost** (0.15) | | | |
| **Maintenance Risk** (0.1) | | | |
| **License** (0.05) | | | |
| **Weighted Total** | | | |

**Maturity Assessment Rubric**:
| Score | Meaning | Signals |
|-------|---------|---------|
| 1 | Experimental | No stable release, frequent breaking changes |
| 2 | Early | <1 year old, small community, limited docs |
| 3 | Growing | Stable releases, growing community, decent docs |
| 4 | Mature | Production-used, large community, comprehensive docs |
| 5 | Industry Standard | Widely adopted, backed by major org, battle-tested |

**Output**: `tech_comparison_matrix.md`

---

### Phase 3 — Proof-of-Concept (PoC)

**Objective**: Build a time-boxed PoC for the top 1-2 candidates.

**PoC Rules**:
- Maximum 2 days per PoC
- Define success criteria BEFORE building
- Use real (or representative) data
- Document everything as you go

**PoC Folder Structure**:
```
poc/
├── {tech-name}/
│   ├── README.md       # Setup instructions + results
│   ├── main.py         # Core PoC code
│   ├── requirements.txt
│   ├── results/        # Benchmarks, outputs, screenshots
│   └── notes.md        # Observations during implementation
```

**PoC Success Criteria Template**:
```markdown
## PoC: [Technology Name]

### Success Criteria (defined before implementation)
- [ ] Can process our data format (____ format)
- [ ] Meets latency requirement (< ____ms)
- [ ] Integrates with our stack (Python ____, FastAPI)
- [ ] Documentation sufficient for team adoption
- [ ] Total setup time < ____ hours

### Results
- Criteria met: X/Y
- Overall assessment: ADOPT / TRIAL / ASSESS / HOLD
```

---

### Phase 4 — Tech Spike Report

**Objective**: Compile findings into a decision document.

**Report Template**:
```markdown
# Tech Spike Report: [Topic]
Date: YYYY-MM-DD
Author: [Agent/User]
Status: DRAFT | FINAL

## Problem Statement
What problem are we trying to solve?

## Technologies Evaluated
- Tech A: [one-sentence description]
- Tech B: [one-sentence description]
- Tech C: [one-sentence description]

## Comparison Matrix
[Embed weighted evaluation matrix]

## PoC Results
### Tech A
- Setup time: X hours
- Performance: [metrics]
- Pros: ...
- Cons: ...

### Tech B
- [Same structure]

## Recommendation
**Recommended**: [Technology Name]
**Rationale**: [3-5 sentences]
**Risk Level**: LOW / MEDIUM / HIGH
**Migration Effort**: [estimate]

## Next Steps
1. [Specific action item]
2. [Specific action item]
3. [Specific action item]

## Appendix
- Links to PoC code
- Raw benchmark data
- Reference papers/docs
```

---

### Phase 5 — Paper Reading Protocol

When evaluating a specific research paper:

**Speed-Read Protocol (15 minutes)**:
1. Read abstract (2 min) — understand the claim
2. Look at figures and tables (3 min) — understand the results
3. Read results/experiments section (5 min) — verify the claim
4. Read methodology (5 min) — understand how it works

**Paper Summary Template**:
```markdown
## Paper: [Title]
Authors: [Names]
Published: [Date, Venue]
Link: [URL]

### Key Contribution
[1-2 sentences: what's new]

### Results
[Key metrics/benchmarks]

### Relevance to Us
- Applicable: YES / NO / PARTIALLY
- Effort to implement: LOW / MEDIUM / HIGH
- Expected benefit: [description]

### Limitations
[What the paper doesn't address]

### Our Assessment
ADOPT: Start using this technique
TRIAL: Build a PoC to validate
ASSESS: Monitor for maturity
HOLD: Not relevant now, revisit later
```

---

## Anti-Patterns — DO NOT

| Anti-Pattern | Consequence | Correct Approach |
|-------------|-------------|------------------|
| Research without time-box | Week-long rabbit holes | Max 2 hours discovery, 2 days PoC |
| Compare > 7 technologies | Analysis paralysis | Narrow to top 3-5 early |
| Skip PoC and adopt based on docs | Production surprises | Always build before adopting |
| Ignore licensing | Legal liability | Check license for every tool |
| Trust benchmarks without reproduction | Misleading comparisons | Run your own benchmarks |
| Recommend without stating risks | Uninformed decisions | Always include risk assessment |

## Skill Coordination

- Use `ai-solution-dev` when research has narrowed to an implementation-ready solution path.
- Use `finetuning` when the recommendation depends on adapting a base model.
- Use `data-pipeline` when independent benchmarking or evaluation harnesses are required.
- Use `ai-integration` when a promising PoC must become an application-facing service.
- Use `documentation` to capture the tech spike, ADR, or recommendation package.
