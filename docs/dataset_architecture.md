# Dataset Architecture — California Insurance Chatbot

> Everything about the data: what we have, what we need externally, how it flows, and how it's structured.

---

## Part 1 — Our Own Data (Already Available)

These are the source documents we've already compiled. They form the **primary knowledge base** for the chatbot.

| File | Size | Contains | Used For |
|------|------|----------|----------|
| `complete_knowledge_base.md` | 34KB | Products, regulations, scripts, flows, pricing, compliance — A to Z | Primary chatbot brain (Gold Layer source) |
| `Research Question and Answers/1.txt` | ~8KB | Agency context Q&A | Product config, agency profile |
| `Research Question and Answers/2.txt` | ~10KB | Product & coverage details | Product knowledge base |
| `Research Question and Answers/3.txt` | ~15KB | California regulatory compliance (SB 263, Prop 103, CIC 10509) | Compliance engine |
| `Research Question and Answers/4.txt` | ~20KB | Lead qualification flow — exact scripts, scoring, objections | Conversation state machine |
| `Research Question and Answers/5,6,7.txt` | ~25KB | Multilingual, scripts, CRM/tech integration | Multilingual, lead routing |
| `Research Question and Answers/8,9,10.txt` | ~45KB | Pricing, workflow, analytics | Pricing engine, KPIs |
| `Research Question and Answers/11 12 13.txt` | ~48KB | Security, edge cases, deployment | Compliance disclosures, fallback handling |
| `Research Question and Answers/14.txt` | ~54KB | Future roadmap (annuities, multi-state, Policy-as-Code) | Architecture planning |
| `us calfornia insurance.md` | 26KB | California insurance overview — life, annuities, regulation | RAG semantic search |
| `US-Calfornia_InsuranceOverview.pdf` | 313KB | Full California insurance regulation document | RAG semantic search (compliance) |
| `CHATBOT SUGGESTIONS INTERMARQ AGENCY (1).docx` | 23KB | Exact chatbot flow, 7 qualification steps, psychology scripts | Conversation flow design |

**Total available**: ~590KB of curated insurance knowledge

---

## Part 2 — External Data Sources

### 2A. NLP & Conversational Training Data

These are used to train the chatbot to understand natural language variations of the same intent (e.g., "I want life insurance" = "looking for coverage" = "protect my family").

| Source | Type | What It Provides | License / Cost |
|--------|------|------------------|----------------|
| **Bitext** | Synthetic NLP | Insurance-specific multilingual chatbot training data. 100% semantically equivalent utterances across EN/ES. Purpose-built for LLM and chatbot training. | Commercial |
| **Agents Republic** | Synthetic conversational | Custom multilingual conversational AI training data including voice, privacy-free and highly accurate | Commercial |
| **Stack Exchange** (Insurance Q&A) | Public Q&A | Real questions users ask about insurance — natural language patterns | Free (CC BY-SA) |
| **Reddit /r/personalfinance, /r/insurance** | Public conversational | Real user insurance questions and objections | Free (API) |
| **Common Crawl** | Web corpus | Massive NLP pre-training data for foundational language understanding | Free |

### 2B. Financial & Regulatory Data

Used to validate compliance rules and supplement pricing data.

| Source | Type | What It Provides | License / Cost |
|--------|------|------------------|----------------|
| **Data.gov** | Government open data | US regulatory data, CDI filings, public affairs data | Free |
| **Data.world** | Open datasets | Insurance and financial datasets, state regulatory data | Free / Freemium |
| **Nasdaq Data Link** | Financial | 250+ economic datasets — Federal Reserve, exchange rates, government finance | Freemium |
| **QuantConnect** | Financial | ETF data (2,650 listings), Benzinga News Feed (~1,250 articles/day) | Commercial |

### 2C. Synthetic Data (Privacy-Compliant Testing)

> ⚠️ **Critical for Insurance**: The chatbot will handle PII (name, email, phone, zip). Real customer data **cannot** be used for training or testing. Synthetic data solves this.

| Provider | What It Generates | Use Case |
|----------|------------------|----------|
| **MOSTLY AI** | Artificial lead profiles mimicking real CA demographics | Test lead scoring engine, routing logic |
| **Gretel.ai** | Privacy-safe synthetic datasets with differential privacy guarantees | Test CCPA data handling, transit pipelines |
| **Syntho** | Statistically accurate synthetic customer records | Integration testing CRM pipeline |
| **K2view** | Enterprise synthetic data for CRM and app testing | Test CRM API integration without real PII |
| **Skanalytix** | Synthetic financial time series (premium rates, risk modeling) | Simulate rate table behavior |
| **TagX** | Synthetic insurance documents (policy forms, applications) | Test document parsing pipeline |

---

## Part 3 — Medallion Lakehouse Pipeline

All data flows through **3 layers** before reaching the chatbot. Each layer has a specific purpose and quality gate.

```
SOURCE DOCUMENTS + EXTERNAL DATA
           │
           ▼
┌──────────────────────────────────┐
│         BRONZE LAYER             │
│  Raw Ingest — As-Is              │
│                                  │
│  • PDFs ingested as binary       │
│  • DOCX text extracted           │
│  • TXT files read with encoding  │
│  • External API responses stored │
│  • No modification               │
└──────────────────┬───────────────┘
                   │
                   ▼
┌──────────────────────────────────┐
│         SILVER LAYER             │
│  Clean + Normalize               │
│                                  │
│  • Deduplicate content           │
│  • Schema validation             │
│  • Type casting                  │
│  • Enforce business rules        │
│  • Remove contradictory records  │
│  • ACORD field mapping           │
│  • Text normalization (NLP)      │
└──────────────────┬───────────────┘
                   │
                   ▼
┌──────────────────────────────────┐
│         GOLD LAYER               │
│  Business-Ready                  │
│                                  │
│  products.json  ─── Chatbot      │
│  scripts.json   ─── State        │
│  compliance.json─── Machine      │
│  pricing.json   ─── +            │
│  faq.json       ─── RAG          │
│  ChromaDB       ─── Engine       │
└──────────────────────────────────┘
```

---

## Part 4 — Gold Layer Dataset Files

These are the final, structured datasets that power the chatbot's responses directly.

### `knowledge/products.json`

**Source**: `complete_knowledge_base.md` Part 2, Research Answer 2.txt

```json
{
  "mortgage_protection": {
    "name": "Mortgage Protection",
    "emoji": "🏠",
    "chatbot_label": "Mortgage Protection",
    "description": "Ensures your family can stay in their home by paying off the remaining mortgage balance if something happens to you.",
    "coverage_amounts": ["$100,000", "$250,000", "$500,000", "$1,000,000+", "Not sure yet"],
    "selling_points": ["Family keeps the house", "Pays off remaining mortgage"],
    "qualification_cta": "Based on your answers, you may qualify for plans between $150k–$500k.",
    "education_script": "Mortgage protection insurance ensures your family can stay in their home by paying off the remaining mortgage balance if something happens to you.",
    "ca_scenario": "35-year-old in San Jose with a new mortgage buys a 20-year term to match their loan payoff timeline."
  },
  "family_life": {
    "name": "My Family",
    "emoji": "👨‍👩‍👧‍👦",
    "chatbot_label": "My Family",
    "description": "Term or permanent life insurance for income replacement and long-term family protection.",
    "types": ["Term Life", "Whole Life", "Universal Life", "Variable Life (FINRA required)"],
    "selling_points": ["Income replacement", "Estate planning", "Long-term protection"]
  },
  "final_expense": {
    "name": "Final Expenses",
    "emoji": "⚰️",
    "chatbot_label": "Final Expenses",
    "description": "Covers funeral costs, medical bills, and end-of-life expenses so your family isn't burdened.",
    "typical_coverage": "$5,000–$50,000",
    "typical_ages": "50–85"
  },
  "business_protection": {
    "name": "Business Protection",
    "emoji": "🏢",
    "chatbot_label": "Business Protection",
    "description": "Key person insurance, buy-sell agreement funding, and business continuity coverage.",
    "ca_scenario": "60-year-old LA business owner uses permanent life to fund a buy-sell agreement with a partner."
  }
}
```

---

### `knowledge/scripts.json`

**Source**: `CHATBOT SUGGESTIONS INTERMARQ AGENCY.docx`, Research Answer 4.txt, `complete_knowledge_base.md` Appendix B

```json
{
  "greeting": "Hi! 👋 I'm here to help you find the right insurance coverage.",
  "conversion_booster": "Most homeowners can qualify for mortgage protection coverage in under 2 minutes.",
  "prompts": {
    "coverage_type": "What type of coverage are you looking for?",
    "coverage_amount": "How much coverage are you looking for?",
    "age_range": "What is your age range?",
    "state": "What state do you live in?",
    "tobacco": "Do you currently use tobacco?",
    "homeowner": "Do you currently own a home with a mortgage?",
    "lead_capture": "Would you like a licensed agent to prepare a personalized quote? Just share your details below.",
    "appointment": "Would you like to schedule a quick 10-minute call to review your options?"
  },
  "responses": {
    "state_confirmed_ca": "Great, we currently serve residents of California.",
    "state_not_served": "We're currently expanding to your area. Leave your details and we'll reach out when we're available.",
    "qualification_result": "Based on your answers, you may qualify for plans between $150k–$500k.",
    "qualification_generic": "Based on your answers, you may qualify for coverage options. Would you like a licensed agent to prepare a personalized quote?",
    "agent_offline": "Our agents may be offline, but I can help you get a quote started.",
    "trust_statement": "Our agents are licensed and registered through the National Insurance Producer Registry.",
    "thank_you": "Thank you, {name}! You've been matched with a licensed agent."
  },
  "objections": {
    "just_looking": "No problem. Would you like a quick estimate while you're here?",
    "already_insured": "Many homeowners keep a separate policy specifically to protect their mortgage so their family keeps the house.",
    "too_expensive": "Plans start as low as $30/month. Would you like to see what fits your budget?",
    "not_interested": "I understand. If you change your mind, I'm here 24/7."
  },
  "buttons": {
    "coverage_type": ["Mortgage Protection", "My Family", "Final Expenses", "Business Protection"],
    "coverage_amount": ["$100,000", "$250,000", "$500,000", "$1,000,000+", "Not sure yet"],
    "age_range": ["Under 30", "30-39", "40-49", "50-59", "60+"],
    "tobacco": ["Yes", "No", "Occasionally"],
    "homeowner": ["Yes", "No", "Planning to buy"],
    "appointment": ["Schedule Now", "I'll wait for a call"]
  }
}
```

---

### `knowledge/compliance.json`

**Source**: Research Answer 3.txt, `us calfornia insurance.md`, `US-Calfornia_InsuranceOverview.pdf`

```json
{
  "regulations": {
    "sb_263": {
      "name": "Senate Bill 263",
      "effective_date": "2025-01-01",
      "applies_to": ["annuities", "non_term_life_with_cash_value"],
      "requires": ["buyers_guide", "fee_disclosure", "suitability_assessment", "conflict_of_interest_disclosure"],
      "training_hours_required": 8,
      "suitability_fields": [
        "age", "annual_income", "financial_situation", "existing_assets",
        "liquidity_needs", "liquid_net_worth", "risk_tolerance",
        "tax_status", "government_benefits_intent"
      ]
    },
    "prop_103": {
      "name": "Proposition 103",
      "applies_to": ["property_casualty"],
      "not_applicable_to": ["life_insurance", "annuities"],
      "description": "Prior approval for P&C rates. Does NOT affect life insurance chatbot pricing display."
    },
    "cic_10509": {
      "name": "CIC Section 10509",
      "type": "anti_churning_replacement_rules",
      "trigger": "existing_policy_lapsed_surrendered_or_borrowing_over_25pct",
      "required_actions": [
        "Collect applicant-signed replacement statement",
        "Issue formal Notice Regarding Replacement",
        "Written comparison: premiums, cash values, death benefits (old vs new)"
      ]
    },
    "clhiga": {
      "name": "California Life and Health Insurance Guarantee Association",
      "life_death_benefit_limit": 300000,
      "annuity_present_value_limit": 250000,
      "life_cash_value_limit": 100000
    }
  },
  "disclosures": {
    "ai_disclosure": "This is an automated assistant. A licensed agent will review your information. For personalized advice, please speak with a licensed professional.",
    "price_disclaimer": "These are estimated ranges for illustration purposes only. Actual rates are determined through underwriting and may vary based on your health, lifestyle, and other factors.",
    "sb_263_annuity_disclaimer": "Before recommending this product, a licensed agent must review your financial suitability, including income, assets, risk tolerance, and tax status.",
    "data_collection_notice": "By continuing, you agree that the information you share may be used to prepare insurance quotes. See our Privacy Policy.",
    "nipr_statement": "Our agents are licensed and registered through the National Insurance Producer Registry."
  },
  "agent_training": {
    "non_term_life_cash_value_hours": 4,
    "sb_263_best_interest_hours": 8,
    "verification_standard": "ACORD TXLife 228 (Producer Inquiry)"
  }
}
```

---

### `knowledge/pricing.json`

**Source**: Research Answer 8.txt, `complete_knowledge_base.md` Part 8
> ⚠️ **These are industry averages only, NOT carrier-specific rates. Always display with the price disclaimer.**

```json
{
  "display_strategy": "generic_ranges_only",
  "disclaimer": "Estimated ranges. Actual rates subject to underwriting.",
  "mortgage_protection": {
    "data_point_source": "CHATBOT SUGGESTIONS INTERMARQ AGENCY.docx",
    "verified_example": {
      "profile": "Healthy 35-year-old non-smoker, $250,000 coverage",
      "range": "$30–$45/month"
    },
    "rates_by_age_industry_average": {
      "under_30": {
        "250k_non_smoker": "$22–$35/month",
        "500k_non_smoker": "$40–$60/month"
      },
      "30_39": {
        "250k_non_smoker": "$30–$45/month",
        "500k_non_smoker": "$55–$80/month"
      },
      "40_49": {
        "250k_non_smoker": "$45–$70/month",
        "500k_non_smoker": "$80–$120/month"
      },
      "50_59": {
        "250k_non_smoker": "$70–$110/month",
        "500k_non_smoker": "$120–$180/month"
      },
      "60_plus": {
        "250k_non_smoker": "$110–$170/month",
        "500k_non_smoker": "$180–$280/month"
      }
    },
    "tobacco_multiplier": 1.5,
    "note": "Multiply non-smoker rate × 1.5 for tobacco users (occasional treated same as Yes for pricing)"
  },
  "family_life": {
    "note": "No carrier-specific rates available. Generic ranges only.",
    "industry_note": "Term life is typically the least expensive per dollar of coverage."
  },
  "final_expense": {
    "typical_range": "$15–$100/month",
    "typical_coverage": "$5,000–$50,000",
    "note": "Industry typical. No agency-specific rates available."
  },
  "business_protection": {
    "note": "Highly variable by business size, industry, and coverage type. No generic range appropriate."
  }
}
```

---

### `knowledge/faq.json`

**Source**: Extracted from all 8 Research Answer files + `complete_knowledge_base.md`

```json
[
  {
    "id": "faq_001",
    "question": "What is mortgage protection insurance?",
    "answer": "Mortgage protection insurance ensures your family can stay in their home by paying off the remaining mortgage balance if something happens to you.",
    "category": "mortgage_protection",
    "keywords": ["mortgage", "house", "home", "loan", "protection"]
  },
  {
    "id": "faq_002",
    "question": "What is the difference between term life and mortgage protection?",
    "answer": "Mortgage protection is a targeted policy so your family keeps the house — it pays off the mortgage specifically. Term life is broader income replacement for a fixed period and the benefit can be used for anything.",
    "category": "education",
    "keywords": ["term life", "mortgage protection", "difference", "compare"]
  },
  {
    "id": "faq_003",
    "question": "What does SB 263 require?",
    "answer": "Senate Bill 263 (effective Jan 1, 2025) requires agents selling annuities and non-term life insurance to act in the client's best interest, provide a buyer's guide, disclose all fees and conflicts of interest, and complete an 8-hour training course.",
    "category": "compliance",
    "keywords": ["SB 263", "best interest", "annuity", "disclosure", "regulation"]
  },
  {
    "id": "faq_004",
    "question": "What is the CLHIGA protection limit?",
    "answer": "The California Life and Health Insurance Guarantee Association protects policyholders if an insurer fails: up to $300,000 for life insurance death benefits, $250,000 for annuity present value, and $100,000 for life insurance cash value.",
    "category": "compliance",
    "keywords": ["CLHIGA", "guarantee", "insurer fails", "protection", "limit"]
  },
  {
    "id": "faq_005",
    "question": "What is final expense insurance?",
    "answer": "Final expense insurance covers funeral costs, medical bills, and end-of-life expenses so your family isn't financially burdened. Coverage typically ranges from $5,000 to $50,000 with simplified underwriting for ages 50–85.",
    "category": "final_expense",
    "keywords": ["final expense", "burial", "funeral", "end of life", "death benefit"]
  },
  {
    "id": "faq_006",
    "question": "What is indexed universal life (IUL)?",
    "answer": "Indexed Universal Life is a flexible permanent life policy where the cash value grows based on a market index (like the S&P 500) with a guaranteed floor against loss. It offers tax-deferred growth and flexible premium payments.",
    "category": "education",
    "keywords": ["IUL", "indexed universal life", "cash value", "S&P 500", "floor"]
  },
  {
    "id": "faq_007",
    "question": "What is an annuity?",
    "answer": "An annuity is a contract with an insurance company where you make payments (lump sum or installments) and the insurer provides guaranteed income in retirement. Types include fixed (guaranteed rate), indexed (tied to a market index), and variable (invested in the market).",
    "category": "annuities",
    "keywords": ["annuity", "retirement", "income", "fixed", "indexed", "variable"]
  },
  {
    "id": "faq_008",
    "question": "Does Proposition 103 affect life insurance rates?",
    "answer": "No. Proposition 103 requires prior approval only for property and casualty insurance rates (like auto and homeowners). It does NOT apply to life insurance or annuity pricing.",
    "category": "compliance",
    "keywords": ["Prop 103", "proposition 103", "life insurance", "rates", "regulation"]
  }
]
```

---

## Part 5 — ACORD Data Normalization

All lead data is serialized to ACORD standards for carrier compatibility.

### TXLife 103 — New Business Submission

Maps chatbot lead fields → insurance industry standard JSON:

```json
{
  "txlife_103": {
    "version": "2.44",
    "transaction_type": "New Business Submission",
    "party": {
      "person": {
        "age_range": "30-39",
        "tobacco_use": "non_smoker"
      },
      "address": {
        "state": "CA",
        "zip": "90210"
      },
      "contact": {
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "555-123-4567"
      }
    },
    "coverage_request": {
      "product_type": "mortgage_protection",
      "face_amount": 250000,
      "homeowner_status": "yes_with_mortgage"
    },
    "metadata": {
      "ai_lead_score": 5,
      "session_id": "sess_abc123",
      "capture_timestamp": "2025-03-15T22:30:00Z",
      "channel": "chatbot_mvp",
      "chatbot_version": "1.0.0"
    }
  }
}
```

### TXLife 228 — Producer Inquiry (Agent Verification)

Used before routing lead to an agent:

```json
{
  "txlife_228": {
    "inquiry_type": "Agent License & Training Verification",
    "state": "CA",
    "checks": ["state_appointments", "license_status", "sb_263_training_complete"],
    "required_training_hours": 8,
    "action_if_non_compliant": "auto_reassign_to_certified_agent"
  }
}
```

---

## Part 6 — RAG Chunking Strategy

### Document Chunking for ChromaDB

| Document | Chunking Method | Chunk Size | Why |
|----------|----------------|------------|-----|
| `complete_knowledge_base.md` | Parent-child | Parent: section (~1000 tokens), Child: clause (~150 tokens) | Preserves context of individual rules |
| `us calfornia insurance.md` | Parent-child | Parent: topic (~800 tokens), Child: detail (~100 tokens) | Detailed regulation clauses |
| `compliance.json` | Structured decomposition → plain text | ~50 tokens per rule | Precision retrieval for compliance Q&A |
| `faq.json` | One chunk per Q&A pair | ~100 tokens | Direct semantic matching |

### Structured Decomposition for Compliance

Legal statutes are decomposed into normalized JSON tags before embedding:

```json
{"regulation": "SB263", "requirement": "disclosure", "field": "surrender_charges", "applies_to": "annuities", "mandatory": true}
{"regulation": "SB263", "requirement": "training", "hours": 8, "product": "non_term_life_annuity"}
{"regulation": "CIC_10509", "trigger": "existing_policy_replacement", "action": "Notice_Regarding_Replacement"}
{"regulation": "Prop103", "applies_to": "property_casualty", "not_applies_to": "life_insurance"}
{"regulation": "CLHIGA", "limit_type": "life_death_benefit", "amount": 300000, "currency": "USD"}
```

### Embedding Model

| Setting | Value |
|---------|-------|
| Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Dimensions | 384 |
| Speed | ~14,000 sentences/second on CPU |
| License | Apache 2.0 (free) |
| Storage | ChromaDB (local SQLite for MVP) |
| Query strategy | Top-3 relevant chunks + parent context |

---

## Part 7 — Lead Scoring Dataset

The AI lead scoring engine uses a weighted multi-factor model based on qualification answers.

| Factor | Weight | Values | Score Contribution |
|--------|--------|--------|--------------------|
| **Homeowner status** | HIGH | Yes with mortgage = +3, Planning to buy = +1, No = 0 | Core signal |
| **Coverage amount** | HIGH | $250K+ = +2, $100K = +1, Not sure = 0 | Intent signal |
| **Product type** | MEDIUM | Mortgage Protection = +2, Family = +1, Final Expense = +1, Business = +1 | Product fit |
| **Age range** | MEDIUM | 40-59 = +2, 30-39/60+ = +1, Under 30 = 0 | Life stage signal |
| **Tobacco use** | LOW | No = +1, Occasionally = 0, Yes = -1 | Risk signal |

### Scoring Output

| Total Score | Stars | CRM Routing Action |
|------------|-------|--------------------|
| 8–10 | ⭐⭐⭐⭐⭐ (5★) | Immediate API push to live agent CRM queue |
| 5–7 | ⭐⭐⭐⭐ (4★) | High-priority agent notification |
| 2–4 | ⭐⭐ (2★) | Automated email nurture sequence, no human agent |

---

## Part 8 — Missing Data (Needs Agency Input)

The following datasets **cannot be built from our research** — they require Intermarq Agency to provide:

| Dataset | What's Needed | Priority |
|---------|--------------|----------|
| **Rate tables** | Actual carrier-specific premiums by age/gender/health/coverage for all 4 products | 🔴 Blocks accurate pricing |
| **Carrier list** | Which carriers Intermarq represents in CA for each product line | 🔴 Blocks product config |
| **Objection scripts** | The 5 psychology-based conversion scripts (35–45% claimed conversion rate) | 🟡 Can use defaults initially |
| **Disqualifying conditions** | Which health conditions disqualify applicants per product | 🟡 Can use "agent will review" |
| **CA DOI license/NPN** | Required for trust disclosure statement | 🟡 Placeholder used in MVP |
| **Brand kit** | Logo, colors, fonts for chatbot UI | 🟡 Placeholder styling in MVP |
| **CRM API details** | Endpoint, auth, field mapping for real CRM integration | 🟡 SQLite used in MVP |
| **Scheduling link** | Calendly or Google Calendar API key / link | 🟡 Mock booking in MVP |
