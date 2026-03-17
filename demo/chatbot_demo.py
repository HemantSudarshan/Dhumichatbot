#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intermarq Agency — Interactive Terminal Chatbot Demo
=====================================================
Pure Python, zero dependencies. Reads existing JSON knowledge files.
100% deterministic: numbered choices lock user into DOCX-defined paths.

Usage:
  python demo/chatbot_demo.py
  (Run from project root)
"""

import json
import os
import sys
import time

# ── PATHS ────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")

# ── COLORS (ANSI) ────────────────────────────────────────
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
PURPLE = "\033[95m"

# ── STATE ────────────────────────────────────────────────
CA_ALIASES = {"california", "ca", "calif", "calif.", "cali"}
LANG = "en"
ANSWERS = {}
SESSION = {"start": time.time(), "thumbs_up": 0, "thumbs_down": 0, "drop_off": None,
           "lead_score": None, "completed": False}


def load_json(filename):
    """Load a JSON file from the knowledge directory with UTF-8 encoding."""
    path = os.path.join(KNOWLEDGE_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def bot_say(text, pause=0.5):
    """Print a bot message with a typing effect."""
    print(f"\n  {CYAN}🛡️ {text}{RESET}")
    time.sleep(pause)


def bot_hook(text, emoji="💡"):
    """Print a psychology hook or system message."""
    print(f"  {YELLOW}{emoji} {text}{RESET}")
    time.sleep(0.3)


def user_input(prompt="You"):
    """Get user input."""
    return input(f"\n  {GREEN}{prompt}: {RESET}").strip()


def show_buttons(options):
    """Display numbered button options and return the selected value."""
    print()
    for i, opt in enumerate(options, 1):
        print(f"    {PURPLE}[{i}]{RESET} {opt}")
    while True:
        choice = user_input("Choose (number)")
        try:
            idx = int(choice)
            if 1 <= idx <= len(options):
                selected = options[idx - 1]
                print(f"  {DIM}→ {selected}{RESET}")
                return selected
        except ValueError:
            pass
        print(f"  {RED}Please enter a number 1-{len(options)}{RESET}")


def show_text_input(placeholder):
    """Get free text input."""
    return user_input(placeholder)


def mask_pii(val):
    """Mask personally identifiable information."""
    if not val:
        return "***"
    if "@" in val:
        parts = val.split("@")
        return parts[0][0] + "***@" + parts[1]
    return val[0] + "***"


def print_header():
    """Print the chatbot header."""
    print(f"\n{BOLD}{'═' * 56}{RESET}")
    print(f"{BOLD}  🛡️  Intermarq Agency — Insurance Assistant{RESET}")
    print(f"{DIM}  California Mortgage Protection & Life Insurance{RESET}")
    print(f"{BOLD}{'═' * 56}{RESET}")
    print(f"\n  {DIM}🤖 You're chatting with an AI assistant.{RESET}")
    print(f"  {DIM}A licensed agent is available for personalized advice.{RESET}")
    print(f"  {DIM}Type 'human' anytime to talk to a licensed agent.{RESET}")
    print(f"  {DIM}Type 'es' to switch to Spanish, 'en' for English.{RESET}")


def calc_lead_score():
    """Calculate lead score from answers."""
    is_homeowner = ANSWERS.get("homeowner_status", "").lower() in ("yes", "sí")
    is_mortgage = "mortgage" in ANSWERS.get("coverage_type", "").lower() or \
                  "hipoteca" in ANSWERS.get("coverage_type", "").lower()
    high_coverage = any(x in ANSWERS.get("coverage_amount", "") for x in ["250", "500", "1,000"])
    age_50plus = any(x in ANSWERS.get("age_range", "") for x in ["50", "60"])
    is_ca = ANSWERS.get("state", "") == "California"
    just_exploring = "exploring" in ANSWERS.get("coverage_type", "").lower() or \
                     "explorando" in ANSWERS.get("coverage_type", "").lower()
    is_renter = ANSWERS.get("homeowner_status", "").lower() in ("no",)

    if not is_ca:
        return 1, "⭐"
    if just_exploring and is_renter:
        return 2, "⭐⭐"
    if is_mortgage and age_50plus:
        return 4, "⭐⭐⭐⭐"
    if is_homeowner and high_coverage:
        return 5, "⭐⭐⭐⭐⭐"
    if is_homeowner or high_coverage:
        return 4, "⭐⭐⭐⭐"
    return 3, "⭐⭐⭐"


def show_pricing(pricing):
    """Show estimated pricing based on user answers."""
    age_map = {"Under 30": "under_30", "Menor de 30": "under_30",
               "30-39": "30_39", "40-49": "40_49",
               "50-59": "50_59", "60+": "60_plus"}
    cov_map = {"$100,000": "250k", "$250,000": "250k", "$500,000": "500k",
               "$1,000,000+": "1m", "Not sure yet": "250k", "Aún no estoy seguro": "250k"}

    age_key = age_map.get(ANSWERS.get("age_range", ""), "30_39")
    cov_key = cov_map.get(ANSWERS.get("coverage_amount", ""), "250k")

    rates = pricing["mortgage_protection"]["rates_by_age_non_smoker"].get(age_key, {})
    price_range = rates.get(cov_key, rates.get("250k", "$30-$45/month"))

    is_tobacco = ANSWERS.get("tobacco_use", "").lower() in ("yes", "sí", "occasionally", "ocasionalmente")

    print(f"\n  {BOLD}{'─' * 44}{RESET}")
    print(f"  {BOLD}{CYAN}💰 Your Estimated Range{RESET}")
    print(f"  {BOLD}{GREEN}{price_range}{RESET}")
    print(f"  Mortgage Protection • {ANSWERS.get('coverage_amount', '$250,000')}")
    if is_tobacco:
        print(f"  {RED}⚠️  {pricing['mortgage_protection']['tobacco_note']}{RESET}")
    print(f"\n  {YELLOW}📈 Rates typically increase with age — lock in today's rate.{RESET}")
    print(f"\n  {DIM}{pricing['_meta']['disclaimer']}{RESET}")
    print(f"  {DIM}{YELLOW}Per CA SB 263: A licensed agent will ensure the final")
    print(f"  product meets your best interest.{RESET}")
    print(f"  {BOLD}{'─' * 44}{RESET}")


def ask_feedback():
    """Ask for quick feedback on the experience."""
    feedback = user_input("Rate this experience (👍 or 👎)")
    if "👍" in feedback or "up" in feedback.lower() or "good" in feedback.lower() or "1" in feedback:
        SESSION["thumbs_up"] += 1
        print(f"  {GREEN}Thanks for the positive feedback!{RESET}")
    else:
        SESSION["thumbs_down"] += 1
        print(f"  {CYAN}Thanks — we'll use this to improve.{RESET}")


def print_telemetry():
    """Print session telemetry summary (no PII)."""
    duration = int(time.time() - SESSION["start"])
    print(f"\n{DIM}{'═' * 48}")
    print(f"  SESSION TELEMETRY (no PII)")
    print(f"  Duration: {duration}s")
    print(f"  Completed: {SESSION['completed']}")
    print(f"  Drop-off: {SESSION['drop_off'] or 'None (completed)'}")
    print(f"  Lead Score: {SESSION['lead_score'] or 'N/A'}")
    print(f"  Feedback: 👍 {SESSION['thumbs_up']} / 👎 {SESSION['thumbs_down']}")
    print(f"  Language: {LANG.upper()}")
    print(f"{'═' * 48}{RESET}")


def main():
    global LANG

    # Load knowledge
    scripts = load_json("scripts.json")
    hooks = load_json("hooks.json")
    objections = load_json("objections.json")
    pricing = load_json("pricing.json")
    compliance = load_json("compliance.json")

    print_header()

    # Greeting hook
    bot_say(hooks["greeting_hook"][f"text_{LANG}"])

    # AI disclosure
    bot_say(compliance["disclosures"]["ai_disclosure"], pause=0.3)

    # ── STEP 1 ──────────────────────────────────────────
    SESSION["drop_off"] = "Step 1: Coverage Type"
    step = scripts["step_1"]
    bot_say(step[f"question_{LANG}"])
    ANSWERS["coverage_type"] = show_buttons(step[f"buttons_{LANG}"])

    # Loss aversion hook
    if LANG == "en":
        bot_hook("What would happen to your family's home if something unexpected happened?")
    else:
        bot_hook("¿Qué pasaría con la casa de su familia si algo inesperado sucediera?")

    # ── STEP 2 ──────────────────────────────────────────
    SESSION["drop_off"] = "Step 2: Coverage Amount"
    step = scripts["step_2"]
    bot_say(step[f"question_{LANG}"])
    ANSWERS["coverage_amount"] = show_buttons(step[f"buttons_{LANG}"])

    # ── STEP 3 ──────────────────────────────────────────
    SESSION["drop_off"] = "Step 3: Age Range"
    step = scripts["step_3"]
    bot_say(step[f"question_{LANG}"])
    ANSWERS["age_range"] = show_buttons(step[f"buttons_{LANG}"])

    # ── STEP 4 ──────────────────────────────────────────
    SESSION["drop_off"] = "Step 4: Tobacco Use"
    step = scripts["step_4"]
    bot_say(step[f"question_{LANG}"])
    ANSWERS["tobacco_use"] = show_buttons(step[f"buttons_{LANG}"])

    # Trust hook
    bot_hook(hooks["trust_verification"][f"text_{LANG}"], emoji="🔒")

    # ── STEP 5 ──────────────────────────────────────────
    SESSION["drop_off"] = "Step 5: State"
    step = scripts["step_5"]
    bot_say(step[f"question_{LANG}"])
    state_input = show_text_input("Your state")

    normalized = state_input.lower().strip().replace(".", "")
    if normalized in CA_ALIASES:
        ANSWERS["state"] = "California"
        bot_say(step.get(f"response_ca_{LANG}", "Great, we serve California residents."))
    else:
        ANSWERS["state"] = state_input
        bot_say(step.get(f"response_non_ca_{LANG}",
                         "We currently only serve California residents."))

    # ── STEP 6 ──────────────────────────────────────────
    SESSION["drop_off"] = "Step 6: Homeowner Status"
    step = scripts["step_6"]
    bot_say(step[f"question_{LANG}"])
    ANSWERS["homeowner_status"] = show_buttons(step[f"buttons_{LANG}"])

    # ── STEP 7: LEAD CAPTURE ────────────────────────────
    SESSION["drop_off"] = "Step 7: Lead Capture"

    # Closing reassurance
    bot_say(hooks["closing_reassurance"][f"text_{LANG}"])

    step = scripts["step_7"]
    bot_say(step[f"question_{LANG}"])

    labels = step[f"field_labels_{LANG}"]
    lead = {}
    for field in step["fields"]:
        val = show_text_input(labels[field])
        lead[field] = val

    ANSWERS["lead"] = lead
    print(f"\n  {GREEN}✅ Lead submitted (data masked){RESET}")
    print(f"  {DIM}Name: {mask_pii(lead.get('name', ''))} | Email: {mask_pii(lead.get('email', ''))}{RESET}")

    # Lead score
    score, label = calc_lead_score()
    SESSION["lead_score"] = label
    SESSION["completed"] = True
    SESSION["drop_off"] = None

    # Pricing
    show_pricing(pricing)

    # Lead score display
    print(f"\n  {BOLD}Your Qualification: {label} Priority Lead{RESET}")

    # Reciprocity hook
    if LANG == "en":
        bot_hook("Let me get you a free personalized quote — no commitment required.", emoji="🎁")
    else:
        bot_hook("Permítame obtener una cotización personalizada gratuita — sin compromiso.", emoji="🎁")

    # Social proof
    if LANG == "en":
        bot_hook("Over 500 California families have protected their mortgages through our agency.", emoji="✨")
    else:
        bot_hook("Más de 500 familias de California han protegido sus hipotecas.", emoji="✨")

    # CRM mock
    print(f"\n  {GREEN}✅ Lead sent to Intermarq CRM{RESET}")
    # No PII logged — only confirmation
    print(f"  {DIM}[TELEMETRY] lead_submitted: true, score: {score}{RESET}")

    # Appointment CTA
    cta = scripts["appointment_booking"]
    bot_say(cta[f"cta_{LANG}"])

    if LANG == "en":
        choice = show_buttons(["📅 Schedule 10-min Call", "Maybe Later"])
    else:
        choice = show_buttons(["📅 Programar Llamada", "Quizás Después"])

    if "Schedule" in choice or "Programar" in choice:
        bot_hook("Limited appointment slots available this week.", emoji="⏰")
        print(f"\n  {GREEN}📅 Calendly link: https://calendly.com/intermarq-agency/10min{RESET}")
        bot_say("A licensed California agent will call you at your scheduled time." if LANG == "en"
                else "Un agente licenciado de California le llamará a la hora programada.")
    else:
        bot_say("No problem! You'll receive an email summary shortly. We're here whenever you're ready."
                if LANG == "en" else
                "¡No hay problema! Recibirá un resumen. Estamos aquí cuando esté listo.")
        print(f"  {GREEN}📧 Summary email queued{RESET}")

    # Feedback
    ask_feedback()

    # Session telemetry
    print_telemetry()

    print(f"\n  {BOLD}{CYAN}Thank you for using the Intermarq Agency Insurance Assistant!{RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {DIM}Session ended by user.{RESET}")
        print_telemetry()
    except Exception as e:
        print(f"\n  {RED}Error: {e}{RESET}")
        sys.exit(1)
