# Technical Documentation — Debug Protocol

---

## Failure 1 — Code and Docs Are Out of Sync

**Symptom**: Documentation describes v1 behavior but code is at v2.

**Diagnostic Steps**:
1. Compare doc metadata (version/date) with code version:
   ```bash
   git log -1 --format="%H %ai" src/main.py
   # Compare with version in model_card.md
   ```
2. Diff the documented API against actual OpenAPI spec.
3. Check if recent code changes have corresponding doc updates.

**Fix**:
- Update all outdated sections.
- Add version tag to every document.
- Recommend: add doc-update check to PR template.

---

## Failure 2 — Missing Critical Sections

**Symptom**: Runbook has no rollback procedure, model card has no evaluation results.

**Diagnostic Steps**:
1. Run the completeness checklist from instructions.md Step 4.
2. List all missing/incomplete sections.
3. Priority rank by risk:
   - Critical: rollback, evaluation, limitations
   - Important: examples, troubleshooting
   - Nice-to-have: changelog, version history

**Fix**:
- Generate missing sections from available source material.
- If source material unavailable, mark as "⚠️ REQUIRED — needs input."
- Report to user with specific questions to fill gaps.

---

## Failure 3 — Incorrect API Examples

**Symptom**: Documented code examples return errors when executed.

**Diagnostic Steps**:
1. Copy each example from API docs.
2. Execute against staging/local endpoint.
3. Compare expected vs actual response.

**Fix**:
- Update examples with actual working requests/responses.
- Add automated example validation to CI:
  ```bash
  # Test API examples
  curl -f -X POST localhost:8000/predict \
    -H "Content-Type: application/json" \
    -d '{"text": "test"}' || exit 1
  ```
- Add version check: example should state which API version it targets.

---

## Failure 4 — Stale Experiment Logs

**Symptom**: 20 experiments ran but only 5 are logged.

**Diagnostic Steps**:
1. List all experiment artifacts (checkpoints, configs, results):
   ```bash
   ls -la experiments/ models/ output/
   ```
2. Cross-reference with documented experiments.
3. Identify undocumented experiments.

**Fix**:
- Generate retroactive experiment logs from available artifacts.
- For each: extract config, results, infer hypothesis if possible.
- Mark as "RETROACTIVE LOG — some details may be approximate."
- Prevention: enforce experiment logging as a mandatory step in the `finetuning` skill.

---

## Failure 5 — Documentation Contains Sensitive Information

**Symptom**: API keys, passwords, internal URLs, or PII in documentation.

**Diagnostic Steps**:
1. Scan for common patterns:
   ```python
   import re
   patterns = [
       r'sk-[a-zA-Z0-9]{32,}',          # OpenAI API key
       r'[a-f0-9]{32}',                   # Generic hex key
       r'password\s*[:=]\s*\S+',          # Passwords
       r'Bearer\s+[a-zA-Z0-9._-]{20,}',  # Bearer tokens
       r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', # IP addresses
   ]
   ```
2. Flag any matches.

**Fix**:
- Replace real values with placeholders: `YOUR_API_KEY`, `your-password`
- Add note: "Replace placeholder values with your actual credentials."
- Add PII scan to documentation generation pipeline.
