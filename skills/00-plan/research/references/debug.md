# AI Research — Debug Protocol

---

## Failure 1 — Paper Claims Don't Reproduce

**Symptom**: PoC cannot match the performance reported in the paper.

**Diagnostic Steps**:
1. Verify you're using the exact same:
   - Dataset (version, splits)
   - Preprocessing pipeline
   - Hyperparameters
   - Hardware
2. Check if paper used cherry-picked results or specific evaluation subsets.
3. Check for errata or follow-up papers.

**Expected Behavior**:
- Agent documents the discrepancy with exact numbers.
- Agent assesses: is the gap due to implementation, hardware, or exaggerated claims?
- Agent adjusts recommendation accordingly.

---

## Failure 2 — Too Many Options (Analysis Paralysis)

**Symptom**: 15+ competing tools, cannot make a decision.

**Fix**:
1. Apply rapid elimination criteria:
   - Remove anything with < 100 GitHub stars (unless very new and from a major org)
   - Remove anything with no commits in last 6 months
   - Remove anything with incompatible license
   - Remove anything that doesn't support your language/framework
2. Should reduce to 3-5 candidates.
3. If still too many → prioritize by community adoption and documentation quality.

---

## Failure 3 — Technology Is Too Immature

**Symptom**: No stable release, breaking API changes weekly, poor documentation.

**Diagnostic**: Check these maturity signals:
- Version number (< 1.0 = unstable)
- GitHub issues vs resolved issues ratio
- Frequency of breaking changes in changelog
- Number of production users listed

**Expected Behavior**:
- Agent flags maturity risk explicitly
- Agent recommends: ASSESS (monitor, don't adopt yet)
- Agent suggests mature alternatives
- Agent sets a reminder: "Re-evaluate in 3 months"

---

## Failure 4 — PoC Succeeds but Doesn't Scale

**Symptom**: Works on 100 samples but fails or slows severely on 100K.

**Diagnostic Steps**:
1. Profile memory usage as data grows.
2. Measure latency at 10x, 100x, 1000x scale.
3. Identify algorithmic complexity (O(n²) problems).

**Fix**:
- Include scalability as a mandatory PoC test criterion.
- Test at representative scale, not toy scale.
- Add to report: "Tested at [X] scale. Extrapolated performance at production scale: [Y]."

---

## Failure 5 — Research Is Outdated

**Symptom**: Evaluating a paper/tool from 1+ year ago that has been superseded.

**Diagnostic Steps**:
1. Check "Cited By" on Semantic Scholar / Google Scholar.
2. Search for newer versions or competing approaches.
3. Check if the technology has been deprecated.

**Expected Behavior**:
- Agent verifies publication date.
- If > 6 months old, agent checks for newer work.
- Agent notes in report: "This approach has been superseded by [X] (published [date])."

---

## Failure 6 — Licensing Conflicts

**Symptom**: Selected technology uses GPL or proprietary license incompatible with the project.

**Diagnostic Steps**:
1. Check LICENSE file in the repository.
2. Understand license implications:
   - MIT/Apache-2.0: safe for commercial use
   - GPL: copyleft, requires open-sourcing derivative works
   - AGPL: network copyleft, even SaaS must open-source
   - Proprietary: requires license purchase
3. Check if model weights have separate licensing (common for LLMs).

**Expected Behavior**:
- Agent always includes license in evaluation matrix.
- Agent flags any non-MIT/Apache license as a risk.
- Agent recommends legal review for GPL/AGPL/proprietary.
