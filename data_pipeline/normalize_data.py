"""
normalize_data.py — Preprocess, normalize & validate knowledge
================================================================
Reads streamed data from external_data/, cleans it,
and validates that the knowledge/ JSON files contain everything
the DOCX chatbot flow requires.

Usage:  python data_pipeline/normalize_data.py
"""
import io, sys, json, re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = Path(__file__).parent.parent
EXT = Path(__file__).parent / "external_data"
NORM = Path(__file__).parent / "normalized"
KNOW = BASE / "knowledge"
NORM.mkdir(exist_ok=True)


def load(path):
    if not path.exists(): return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def clean(text):
    if not isinstance(text, str): return str(text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


# ── NORMALIZE EACH STREAMED SOURCE ────────────────────────

def norm_data_gov(raw):
    if not isinstance(raw, list): return []
    seen = set()
    out = []
    for r in raw:
        title = clean(r.get("title", ""))
        if title and title not in seen:
            seen.add(title)
            out.append({"title": title, "notes": clean(r.get("notes", "")),
                        "tags": r.get("tags", [])})
    return out

def norm_census(raw):
    if not isinstance(raw, list): return []
    return [c for c in raw if c.get("total_units", 0) > 0 and c.get("county")]

def norm_stackexchange(raw):
    if not isinstance(raw, list): return []
    return [{"question": clean(q.get("title", "")),
             "answer_preview": clean(q.get("body_preview", ""))[:300],
             "score": q.get("score", 0), "tags": q.get("tags", [])}
            for q in raw if q.get("score", 0) > 0]

def norm_worldbank(raw):
    if not isinstance(raw, dict): return None
    gdp = raw.get("gdp", {}).get("records", [])
    cpi = raw.get("cpi", {}).get("records", [])
    if not gdp and not cpi: return None
    return {"source": "World Bank", "gdp": gdp, "cpi": cpi,
            "count": len(gdp) + len(cpi)}

def norm_reddit(raw):
    if not isinstance(raw, list): return []
    return [{"title": clean(p.get("title", "")),
             "text": clean(p.get("selftext", ""))[:300],
             "score": p.get("score", 0), "comments": p.get("num_comments", 0)}
            for p in raw if p.get("score", 0) > 0]

def norm_synthetic(raw):
    if not isinstance(raw, dict): return None
    return raw


# ── VALIDATE KNOWLEDGE FILES ─────────────────────────────

def validate():
    """Validate that all knowledge files match DOCX requirements."""
    print("\n── Knowledge File Validation ────────────────────")
    checks = {}

    scripts = load(KNOW / "scripts.json") or {}
    hooks = load(KNOW / "hooks.json") or {}
    objections = load(KNOW / "objections.json") or {}
    knowledge = load(KNOW / "knowledge.json") or {}

    stxt = json.dumps(scripts)
    htxt = json.dumps(hooks)
    otxt = json.dumps(objections)
    ktxt = json.dumps(knowledge)

    # 1. scripts.json: 7 steps
    checks["7_step_flow"] = all(f"step_{i}" in scripts for i in range(1, 8))

    # 2. Bilingual: EN + ES questions
    checks["bilingual_en_es"] = "question_en" in stxt and "question_es" in stxt

    # 3. Buttons for steps 1-4, 6
    checks["button_options"] = all(
        "buttons_en" in json.dumps(scripts.get(f"step_{i}", {}))
        for i in [1, 2, 3, 4, 6]
    )

    # 4. Lead capture fields
    step7 = scripts.get("step_7", {})
    checks["lead_capture"] = all(f in step7.get("fields", [])
                                  for f in ["name", "email", "phone", "zip_code"])

    # 5. Lead scoring rules
    checks["lead_scoring"] = "lead_scoring" in scripts and len(
        scripts.get("lead_scoring", {}).get("rules", [])) >= 3

    # 6. Appointment booking
    checks["appointment_booking"] = "appointment_booking" in scripts

    # 7. Greeting hook
    checks["greeting_hook"] = "greeting_hook" in hooks and "homeowners" in htxt.lower()

    # 8. Trust verification
    checks["trust_verification"] = "trust_verification" in hooks and "licensed" in htxt.lower()

    # 9. Offline fallback
    checks["offline_fallback"] = "offline_fallback" in hooks and "offline" in htxt.lower()

    # 10. Objection: already have insurance
    checks["obj_already_have"] = "already_have_insurance" in objections and \
        "mortgage" in otxt.lower()

    # 11. Objection: just looking
    checks["obj_just_looking"] = "just_looking" in objections and \
        "quick estimate" in otxt.lower()

    # 12. Price teasers
    checks["price_teasers"] = "$30" in ktxt and "$45/month" in ktxt

    # 13. Education / definitions
    checks["education_content"] = "mortgage_protection" in knowledge.get("education", {})

    # 14. Pricing reference
    checks["pricing_reference"] = "rates_by_age_non_smoker" in json.dumps(
        knowledge.get("pricing_reference", {}))

    # 15. CA compliance
    checks["ca_compliance"] = "California" in json.dumps(knowledge.get("ca_compliance", {}))

    for name, ok in checks.items():
        print(f"   [{'OK' if ok else 'XX'}] {name}")

    passed = sum(checks.values())
    total = len(checks)
    print(f"\n   {passed}/{total} checks passed")
    return passed == total, checks


# ── MAIN ──────────────────────────────────────────────────

def main():
    print("=" * 58)
    print("  NORMALIZE & VALIDATE — MVP")
    print("=" * 58)

    # Normalize streamed data
    print("\n── Normalizing streamed data ────────────────────")
    sources = {
        "data_gov":       (norm_data_gov,       "data_gov"),
        "census":         (norm_census,          "census"),
        "stack_exchange":  (norm_stackexchange,   "stack_exchange"),
        "worldbank":      (norm_worldbank,       "worldbank"),
        "reddit":         (norm_reddit,          "reddit"),
        "synthetic":      (norm_synthetic,       "synthetic"),
    }

    for key, (fn, save_name) in sources.items():
        raw = load(EXT / f"{key}.json")
        if raw is None or (isinstance(raw, dict) and raw.get("status") == "failed"):
            print(f"   [{key}] skipped (no data)")
            continue
        cleaned = fn(raw)
        if cleaned is None:
            print(f"   [{key}] skipped (empty)")
            continue
        save(NORM / f"{save_name}.json", cleaned)
        count = len(cleaned) if isinstance(cleaned, list) else cleaned.get("count", cleaned.get("total", "ok"))
        print(f"   [{key}] -> {count} records")

    print(f"   Saved to: {NORM}")

    # Validate knowledge files
    ok, checks = validate()

    print(f"\n{'='*58}")
    if ok:
        print("  ALL CHECKS PASSED — knowledge base is DOCX-aligned")
    else:
        failed = [k for k, v in checks.items() if not v]
        print(f"  {len(failed)} CHECK(S) FAILED:")
        for f in failed:
            print(f"    - {f}")
    print(f"{'='*58}")
    return ok


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
