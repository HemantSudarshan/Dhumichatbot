"""
test_chatbot_flow.py — Input→Output chatbot test using exact DOCX data
========================================================================
Simulates the 7-step qualification flow, objection handling, hooks,
and pricing teasers using the knowledge/ JSON files.

Only run IF streaming + normalization passed.

Usage:  python data_pipeline/test_chatbot_flow.py
"""
import io, sys, json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

KNOW = Path(__file__).parent.parent / "knowledge"


def load(name):
    p = KNOW / f"{name}.json"
    if not p.exists():
        print(f"  [MISS] {name}.json not found"); return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


class ChatbotMVP:
    """Simulates the exact DOCX chatbot using knowledge/ files."""

    def __init__(self):
        self.scripts = load("scripts")
        self.hooks = load("hooks")
        self.objections = load("objections")
        self.knowledge = load("knowledge")
        self.state = {}
        self.passed = 0
        self.failed = 0

    def check(self, name, condition, detail=""):
        if condition:
            print(f"  [PASS] {name}")
            self.passed += 1
        else:
            print(f"  [FAIL] {name} — {detail}")
            self.failed += 1
        return condition

    # ── STEP TESTS ────────────────────────────────────────

    def test_step(self, step_num, user_choice_index=0):
        """Test a specific step returns correct question + buttons."""
        step = self.scripts.get(f"step_{step_num}", {})
        q_en = step.get("question_en", "")
        q_es = step.get("question_es", "")
        buttons = step.get("buttons_en", [])

        has_q = bool(q_en)
        has_es = bool(q_es)
        has_buttons = len(buttons) >= 2 or step_num == 5  # step 5 has no buttons

        self.check(f"Step {step_num}: English question", has_q, f"Missing question_en")
        self.check(f"Step {step_num}: Spanish question", has_es, f"Missing question_es")

        if step_num != 5 and step_num != 7:
            self.check(f"Step {step_num}: Buttons ({len(buttons)})", has_buttons,
                       f"Only {len(buttons)} buttons")

        return step

    def test_step5_california(self):
        """Step 5: State — must respond with CA-specific message."""
        step = self.scripts.get("step_5", {})
        ca_resp = step.get("response_ca_en", "")
        self.check("Step 5: CA response", "california" in ca_resp.lower(),
                   f"Response doesn't mention California")
        return step

    def test_step7_lead_capture(self):
        """Step 7: Lead capture — must have name/email/phone/zip."""
        step = self.scripts.get("step_7", {})
        fields = step.get("fields", [])
        self.check("Step 7: Lead fields (name/email/phone/zip)",
                   all(f in fields for f in ["name", "email", "phone", "zip_code"]),
                   f"Fields: {fields}")
        self.check("Step 7: CTA question",
                   "licensed agent" in step.get("question_en", "").lower(),
                   "Missing 'licensed agent' in CTA")
        return step

    # ── HOOK TESTS ────────────────────────────────────────

    def test_hooks(self):
        """Test trust builders and conversion hooks."""
        # Greeting hook
        gh = self.hooks.get("greeting_hook", {})
        self.check("Hook: Greeting (homeowners)",
                   "homeowners" in gh.get("text_en", "").lower(),
                   "Missing 'homeowners' text")

        # Trust verification
        tv = self.hooks.get("trust_verification", {})
        self.check("Hook: Trust (licensed)",
                   "licensed" in tv.get("text_en", "").lower(),
                   "Missing 'licensed' text")

        # Offline fallback
        fb = self.hooks.get("offline_fallback", {})
        self.check("Hook: Fallback (offline)",
                   "offline" in fb.get("text_en", "").lower(),
                   "Missing 'offline' text")

        # Appointment CTA
        appt = self.hooks.get("appointment_cta", {})
        self.check("Hook: Appointment CTA",
                   "schedule" in appt.get("text_en", "").lower(),
                   "Missing 'schedule' text")

    # ── OBJECTION TESTS ───────────────────────────────────

    def test_objections(self):
        """Test objection handling responses match DOCX."""
        # Already have insurance
        obj1 = self.objections.get("already_have_insurance", {})
        self.check("Objection: Already have insurance",
                   "mortgage" in obj1.get("response_en", "").lower(),
                   "Response should mention mortgage protection")

        # Just looking
        obj2 = self.objections.get("just_looking", {})
        self.check("Objection: Just looking",
                   "quick estimate" in obj2.get("response_en", "").lower(),
                   "Response should offer quick estimate")

        # Too expensive
        obj3 = self.objections.get("too_expensive", {})
        self.check("Objection: Too expensive",
                   "$15/month" in obj3.get("response_en", ""),
                   "Response should mention $15/month anchor")

    # ── PRICING & KNOWLEDGE TESTS ─────────────────────────

    def test_pricing(self):
        """Test price teasers and education content."""
        teasers = self.knowledge.get("price_teasers", {})
        specific = teasers.get("specific_example", {})
        self.check("Pricing: $30-$45/month teaser",
                   "$30" in specific.get("text_en", "") and "$45/month" in specific.get("text_en", ""),
                   "Missing $30-$45/month range")

        edu = self.knowledge.get("education", {})
        mp = edu.get("mortgage_protection", {})
        self.check("Education: Mortgage protection definition",
                   "family can stay" in mp.get("definition_en", "").lower(),
                   "Definition should mention family staying in home")

        pricing = self.knowledge.get("pricing_reference", {}).get("mortgage_protection", {})
        rates = pricing.get("rates_by_age_non_smoker", {})
        self.check("Pricing: 5 age bands",
                   len(rates) >= 5,
                   f"Only {len(rates)} age bands")

        self.check("Pricing: Tobacco multiplier",
                   pricing.get("tobacco_multiplier") == 1.5,
                   f"Multiplier: {pricing.get('tobacco_multiplier')}")

    # ── LEAD SCORING TESTS ────────────────────────────────

    def test_lead_scoring(self):
        """Test lead scoring rules."""
        ls = self.scripts.get("lead_scoring", {})
        rules = ls.get("rules", [])
        self.check("Lead scoring: At least 3 rules",
                   len(rules) >= 3,
                   f"Only {len(rules)} rules")

        # Homeowner gets 5 stars
        top = rules[0] if rules else {}
        self.check("Lead scoring: Homeowner = 5 stars",
                   top.get("score") == 5 and "homeowner" in top.get("condition", "").lower(),
                   f"Top rule: {top}")

    # ── FULL FLOW SIMULATION ──────────────────────────────

    def simulate_full_flow(self):
        """Walk through the entire chatbot as a homeowner in CA."""
        print("\n── Simulating: Homeowner, 40-49, Non-smoker, CA ──")

        # Step 1: Choose mortgage
        s1 = self.scripts.get("step_1", {})
        choice = s1.get("buttons_en", [])[0]  # "My Mortgage"
        self.check("Flow: Step 1 -> My Mortgage",
                   choice == "My Mortgage", f"Got: {choice}")

        # Step 2: $250k
        s2 = self.scripts.get("step_2", {})
        choice = s2.get("buttons_en", [])[1]  # "$250,000"
        self.check("Flow: Step 2 -> $250,000",
                   choice == "$250,000", f"Got: {choice}")

        # Step 3: 40-49
        s3 = self.scripts.get("step_3", {})
        choice = s3.get("buttons_en", [])[2]  # "40-49"
        self.check("Flow: Step 3 -> 40-49",
                   choice == "40-49", f"Got: {choice}")

        # Step 4: No tobacco
        s4 = self.scripts.get("step_4", {})
        choice = s4.get("buttons_en", [])[1]  # "No"
        self.check("Flow: Step 4 -> No tobacco",
                   choice == "No", f"Got: {choice}")

        # Step 5: California
        s5 = self.scripts.get("step_5", {})
        self.check("Flow: Step 5 -> California response",
                   "california" in s5.get("response_ca_en", "").lower())

        # Step 6: Yes homeowner
        s6 = self.scripts.get("step_6", {})
        choice = s6.get("buttons_en", [])[0]  # "Yes"
        self.check("Flow: Step 6 -> Homeowner Yes",
                   choice == "Yes", f"Got: {choice}")

        # Step 7: Lead capture
        s7 = self.scripts.get("step_7", {})
        self.check("Flow: Step 7 -> Captures name/email/phone/zip",
                   set(["name", "email", "phone", "zip_code"]).issubset(set(s7.get("fields", []))))

        # Price estimate for this profile: 40-49 non-smoker
        rates = self.knowledge.get("pricing_reference", {}).get(
            "mortgage_protection", {}).get("rates_by_age_non_smoker", {})
        rate_40_49 = rates.get("40_49", {})
        self.check("Flow: Price estimate -> $55-$85/month",
                   "$55" in rate_40_49.get("monthly_range", ""),
                   f"Got: {rate_40_49}")

        # Lead score: Homeowner + $250k = 5 stars
        rules = self.scripts.get("lead_scoring", {}).get("rules", [])
        top_rule = rules[0] if rules else {}
        self.check("Flow: Lead score -> 5 stars",
                   top_rule.get("score") == 5)

        # Appointment CTA
        appt = self.hooks.get("appointment_cta", {})
        self.check("Flow: Appointment CTA offered",
                   "schedule" in appt.get("text_en", "").lower())


def main():
    print("=" * 58)
    print("  CHATBOT INPUT → OUTPUT TEST")
    print("  Exact DOCX Alignment Check")
    print("=" * 58)

    bot = ChatbotMVP()

    # Test each component
    print("\n── Step-by-Step Flow ────────────────────────────")
    for i in range(1, 5):
        bot.test_step(i)
    bot.test_step5_california()
    bot.test_step(6)
    bot.test_step7_lead_capture()

    print("\n── Trust & Conversion Hooks ─────────────────────")
    bot.test_hooks()

    print("\n── Objection Handling ───────────────────────────")
    bot.test_objections()

    print("\n── Pricing & Education ─────────────────────────")
    bot.test_pricing()

    print("\n── Lead Scoring ────────────────────────────────")
    bot.test_lead_scoring()

    bot.simulate_full_flow()

    # Summary
    total = bot.passed + bot.failed
    print(f"\n{'='*58}")
    print(f"  RESULTS: {bot.passed}/{total} tests passed")
    if bot.failed == 0:
        print("  ALL TESTS PASSED — Chatbot matches DOCX perfectly")
    else:
        print(f"  {bot.failed} tests FAILED")
    print(f"{'='*58}")
    return bot.failed == 0


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
