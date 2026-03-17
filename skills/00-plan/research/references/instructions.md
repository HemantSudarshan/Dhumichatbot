# AI Research — Agent Instructions

## Execution Instructions

### Step 1 — Scope the Research

1. Clarify the research question with the user:
   - "What specific technology or capability are you evaluating?"
   - "What problem are you trying to solve?"
   - "What's your timeline for making a decision?"
2. Define the scope:
   - Maximum 5-7 candidates to evaluate
   - Time-box: 2 hours for discovery, 2 days for PoC
3. Identify the target audience (engineers? management? both?).

### Step 2 — Discover and Gather Sources

1. Search for relevant technologies:
   - Check GitHub (stars, activity, recent commits)
   - Check HuggingFace (model/dataset availability)
   - Check Papers With Code (benchmarks)
   - Check Reddit/community discussions (real-world usage)
2. For each candidate, collect:
   - Official repository URL
   - Star count and recent commit activity
   - Documentation quality (1-5 rating)
   - License type
   - Known production users
3. Save findings in `research_notes.md`.

### Step 3 — Build the Evaluation Matrix

1. Use the weighted matrix template from SKILL.md Phase 2.
2. Score each technology 1-5 on each criterion.
3. Calculate weighted totals.
4. Identify the top 2 candidates for PoC.
5. Present results to user with rationale.

### Step 4 — Build Proof-of-Concept

1. Create PoC folder structure per SKILL.md Phase 3.
2. Define success criteria BEFORE writing code.
3. Build the PoC using representative data:
   - Keep it minimal — only test what matters
   - Measure: setup time, performance, integration difficulty
4. Document observations as you go.
5. Run benchmarks and record results.

### Step 5 — Write the Tech Spike Report

1. Use the report template from SKILL.md Phase 4.
2. Include:
   - Problem statement
   - Technologies evaluated
   - Comparison matrix
   - PoC results
   - Recommendation with risk assessment
   - Next steps
3. Present to user for review.

### Step 6 — Research Paper Reading (If Applicable)

1. Use the speed-read protocol (15 min max per paper).
2. Fill out the paper summary template.
3. Assess: ADOPT / TRIAL / ASSESS / HOLD.
4. Link to the original paper.

## Interaction Protocol

| Situation | Agent Behavior |
|-----------|---------------|
| Too many candidate technologies | Narrow with elimination criteria |
| Paper claims seem too good | Verify with independent benchmarks |
| Technology is immature (<1 year old) | Flag maturity risk, recommend TRIAL not ADOPT |
| User wants to adopt without PoC | Warn about production risk, strongly recommend PoC |
| Research scope keeps expanding | Enforce time-box, report what's found so far |

## Handoff

- If adopting a new model → `finetuning` skill
- If integrating new tool → `ai-integration` skill
- If documenting findings → `documentation` skill
