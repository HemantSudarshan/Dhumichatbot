# Intermarq Agency — California Insurance Chatbot: Complete Knowledge Base

> **Document Purpose**: This is the A-to-Z compiled knowledge base for building the Intermarq Agency California insurance chatbot. It combines all research findings from both source documents and all 14 sections of research answers.

---

# Part 1 — Agency & Business Context

## Intermarq Agency Profile

| Item | Status |
|------|--------|
| Insurance carriers represented | ❌ Not in source documents — need from agency |
| Geographic coverage | California statewide. Chatbot verifies: *"We currently serve residents of California"* |
| CA DOI License / NPN numbers | ❌ Not in source documents — need from agency |
| Value proposition vs competitors | ❌ Not in source documents — need from agency |
| CRM system | ❌ Not specified. Documents state chatbot should push leads to "CRM, email, or text notification" and use "AI lead scoring so your CRM prioritizes the best leads first" |
| Lead-to-close conversion rate | ❌ Not provided. Psychology-based scripts claim **35–45% website visitor → booked appointment** conversion potential |
| Appointment scheduling tool | **Calendly** or **Google Calendar** (both recommended, specific choice TBD) |
| Preferred contact method | ❌ Not specified. Chatbot captures Name, Email, Phone, Zip Code |
| Brand kit (logo, colors, fonts) | ❌ Not in source documents — need from agency |
| Website platform | ❌ Not specified. Documents reference "insurance website visitors" implying a website exists |

## Trust & Licensing Statement
The chatbot should display:
> *"Our agents are licensed and registered through the National Insurance Producer Registry."*

---

# Part 2 — Insurance Products & Coverage

## Chatbot Product Lines (4 Total)

The chatbot MVP covers exactly **4 product categories** presented as initial selection buttons:
1. **Mortgage Protection**
2. **My Family** (Term/Permanent Life)
3. **Final Expenses** (Burial Insurance)
4. **Business Protection**

---

### 2A. Mortgage Protection Insurance

| Detail | Information |
|--------|-------------|
| **Coverage amounts (chatbot buttons)** | $100,000 · $250,000 · $500,000 · $1,000,000+ · Not sure yet |
| **Qualification CTA range** | *"Based on your answers, you may qualify for plans between $150k–$500k"* |
| **Sample pricing** | Healthy 35-year-old non-smoker seeking $250,000 → **$30–$45/month** |
| **Age brackets** | Under 30 · 30-39 · 40-49 · 50-59 · 60+ |
| **Key selling script** | *"Mortgage protection insurance ensures your family can stay in their home by paying off the remaining mortgage balance if something happens to you."* |
| **Differentiation** | Framed as a targeted policy so "family keeps the house" — distinct from general term life |
| **Carriers & specific products** | ❌ Not in source documents |
| **Underwriting type** | ❌ Not specified (simplified issue vs. guaranteed issue vs. fully underwritten) |
| **Disqualifying health conditions** | ❌ Not specified. Chatbot asks tobacco use as pricing factor |
| **Riders available** | ❌ Not specified |
| **Full rate tables** | ❌ Not provided — only the single sample data point above |

### Educational Topics to Cover
- What mortgage protection is and how it works
- How it pays off the house if something happens
- Difference between term life vs. mortgage protection

---

### 2B. Term Life Insurance

| Detail | Information |
|--------|-------------|
| **Coverage limits** | Up to **$1,000,000+** (per chatbot button options) |
| **Term lengths** | 10, 15, 20, or 30 years (standard industry, not specified per carrier) |
| **Description** | Provides a death benefit for a fixed period. Typically the least expensive option with no cash value. Used for income replacement during working years. |
| **Carriers & products** | ❌ Not in source documents |
| **Pricing by age/gender/health** | ❌ Not provided |
| **Conversion options (term → permanent)** | ❌ Not provided |
| **Medical exam requirements** | ❌ Not provided |

### California-Specific Scenario
> **35-year-old software engineer in San Jose** with a spouse and young child buys a 20-year term policy to replace income while the child grows up. Agent must ensure the policy fits the family's needs and provide clear disclosures of premiums, benefits, and any riders.

---

### 2C. Whole Life Insurance

| Detail | Information |
|--------|-------------|
| **Description** | Permanent policy with fixed premiums and guaranteed cash value growth |
| **Use cases** | Long-term protection and estate planning |
| **Key feature** | Guaranteed cash value accumulation |

---

### 2D. Universal Life Insurance

| Detail | Information |
|--------|-------------|
| **Description** | Flexible premiums and flexible death benefit, with cash value tied to interest or market indexes |
| **IUL (Indexed Universal Life)** | Tax-deferred growth linked to a market index with a guaranteed floor against market loss |
| **Key feature** | Flexibility in premium payments and death benefit |

---

### 2E. Variable Life Insurance

| Detail | Information |
|--------|-------------|
| **Description** | Most complex permanent option where cash value is invested in securities (the market) |
| **Risk profile** | Higher risk and reward |
| **Special requirement** | Agents must be registered with **FINRA** to sell this product |

---

### 2F. Final Expense / Burial Insurance

| Detail | Information |
|--------|-------------|
| **Chatbot role** | Offered as "Final Expenses" primary coverage option |
| **Carriers** | ❌ Not provided |
| **Coverage ranges** | ❌ Not provided (industry typical: $5K–$50K) |
| **Age restrictions** | ❌ Not provided (industry typical: 50–85) |
| **Monthly premiums** | ❌ Not provided |
| **Graded vs. immediate benefit** | ❌ Not provided |
| **Health questions** | ❌ Not provided |

---

### 2G. Business Insurance

| Detail | Information |
|--------|-------------|
| **Chatbot role** | Offered as "Business Protection" option |
| **Specific lines (BOP, GL, WC, etc.)** | ❌ Not provided |
| **Target industries** | ❌ Not provided |
| **Premiums** | ❌ Not provided |
| **Buy-sell agreement funding** | California scenario: 60-year-old LA business owner buys permanent life to fund buy-sell with partner |

### California-Specific Scenario
> **60-year-old small business owner in Los Angeles** buys a permanent life policy to fund a buy-sell agreement with a business partner. Agent must consider the owner's long-term goals and financial situation, and strictly comply with California's replacement rules if switching from an older policy.

---

### 2H. Annuities (Future Product Support — Architecture Already Built)

#### Types of Annuities

| Type | Description |
|------|-------------|
| **Fixed** | Insurer guarantees minimum interest rate and payment formula. Conservative, predictable income. Shielded from market volatility. |
| **Indexed** | Interest credited based on market index (e.g., S&P 500) with caps and floors. Principal guaranteed against market loss. Middle ground between fixed and variable. |
| **Variable** | Assets held in separate accounts tied to underlying investments. Growth depends on market performance. Owner assumes market risk. |
| **Immediate** | Payout begins right away after a lump-sum contribution |
| **Deferred** | Accumulation phase before payout phase begins |

#### Annuity Phases
- **Accumulation Phase**: Buyer pays premiums (lump sum or multiple contributions), funds grow per contract type
- **Payout Phase**: Value converted into stream of payments (annuitized) or systematic withdrawals. Payouts can last for life, cover joint survivor, or last a set period.

#### California Annuity Scenarios
- **55-year-old nurse**: Fixed annuity for guaranteed retirement income
- **70-year-old retiree**: Immediate annuity to convert savings into guaranteed income stream
- **60-year-old investor**: Variable annuity for growth potential with market exposure

---

# Part 3 — California Regulatory Compliance

## Key Regulatory Bodies & Laws

### California Department of Insurance (CDI)
- Led by an **elected Commissioner**
- Regulates **1,600+ companies** and **500,000+ professionals**
- Mission: Consumer protection, fair rates, solvency
- Funded by license fees and assessments (not general taxes)
- All insurers and agents must be CDI-licensed to operate in CA

### Proposition 103
- Requires **"prior approval"** for rates in property and casualty lines (auto, homeowners)
- Ensures rates are not excessive, inadequate, or unfairly discriminatory
- **Does NOT apply** to life insurance or annuity price estimates shown by chatbot

### Senate Bill 263 (SB 263) — Effective January 1, 2025
- **Best Interest Standard** for annuity recommendations
- Requires **buyer's guide** for all annuity purchasers
- Mandatory disclosures: surrender periods, surrender charges, M&E fees, investment advisory fees, tax penalties, market risks
- Material conflicts of interest must be disclosed in writing
- Strengthened disclosure rules for life insurance replacements

### CIC Section 10509 — Anti-Churning / Replacement Rules
A replacement is legally triggered if a new policy is purchased while an existing policy is lapsed, surrendered, or subjected to borrowing >25% of loan value.

When replacement is triggered, the chatbot/system must:
1. Collect applicant-signed statement regarding the replacement
2. Issue formal **"Notice Regarding Replacement"**
3. Generate written comparison of premiums, cash values, and death benefits of both policies

### CLHIGA (California Life and Health Insurance Guarantee Association)
Protects policyholders if an insurer fails:

| Coverage Type | Limit |
|--------------|-------|
| Life insurance death benefits | $300,000 |
| Annuity present value | $250,000 |
| Life insurance cash value | $100,000 |

---

## Chatbot Compliance Requirements

### Required Disclosures
Before recommending permanent life insurance or annuities, disclose:
- Surrender periods and charges
- Mortality and expense fees
- Investment advisory fees
- Tax penalties for premature annuitization
- Market risks
- All material conflicts of interest (in writing)

### Suitability Data Fields (Must Collect Before Recommending)
Per SB 263 "best interest" standard:
- Age
- Annual income
- Financial situation and needs
- Existing assets (including life insurance and investments)
- Liquidity needs
- Liquid net worth
- Risk tolerance
- Tax status
- Intent to apply for means-tested government benefits (Medi-Cal)

### AI / Automated System Disclosure
- California CCPA grants consumers right to opt-out of automated decision-making
- Chatbot should state: *"Our agents may be offline, but I can help you get a quote started"*
- Should offer option to connect with a licensed human agent

### Price Estimates — Legal Status
- Chatbot strategy recommends showing rough premium ranges ($30–$45/month example)
- **Legal classification unclear** — sources do not explicitly confirm whether price ranges constitute an "insurance quote" under CA law
- Recommendation: Display with clear disclaimer that rates are estimates subject to underwriting

### Record Retention
- High-risk AI systems must maintain use logs and tamper-proof event logs for continuous monitoring
- Specific California insurance retention timeframes: ❌ Not specified in sources

### CCPA/CPRA
- Consumers must be given right to opt-out of automated decision-making (particularly behavioral profiling)
- Specific privacy disclosure language: ❌ Not detailed in sources

### Advertising Compliance
- Life insurance language must not be "deceptive or inherently unfair"
- SB 263 prohibits misleading sales practices (e.g., selling annuity solely for Medi-Cal eligibility without objective benefit)

### Agent Training Verification
- New 2025 rules: **4-hour training course** required for agents selling non-term life policies with cash value
- **8-hour Best Interest training** required for SB 263 compliance
- Chatbot does NOT count as "selling" — but must verify **human agent** credentials
- System triggers **ACORD TXLife 228** (Producer Inquiry) before routing leads to verify agent training compliance
- If agent is non-compliant → lead auto-reassigned to certified agent

---

# Part 4 — Lead Qualification Flow

## Complete Conversation Flow

### Step 1 — Coverage Type Selection
**Bot asks**: *"What type of coverage are you looking for?"*

Buttons:
- 🏠 Mortgage Protection
- 👨‍👩‍👧‍👦 My Family
- ⚰️ Final Expenses
- 🏢 Business Protection

---

### Step 2 — Coverage Amount
**Bot asks**: *"How much coverage are you looking for?"*

Buttons:
- $100,000
- $250,000
- $500,000
- $1,000,000+
- Not sure yet

---

### Step 3 — Age Range
**Bot asks**: *"What is your age range?"*

Buttons:
- Under 30
- 30-39
- 40-49
- 50-59
- 60+

---

### Step 4 — State of Residence
**Bot asks**: *"What state do you live in?"*

- If California → *"Great, we currently serve residents of California."* → Continue
- If other state → Verify non-resident licensing. If not licensed → redirect/end flow

---

### Step 5 — Tobacco Use
**Bot asks**: *"Do you currently use tobacco?"*

Buttons:
- Yes
- No
- Occasionally

> *Rationale: "Insurance companies price heavily based on this"*

---

### Step 6 — Homeowner Status
**Bot asks**: *"Do you currently own a home with a mortgage?"*

Buttons:
- Yes
- No
- Planning to buy

> *Rationale: Mortgage holders are highest-converting clients. Homeowners scored 5★, renters scored 2★.*

---

### Step 7 — Qualification Result + CTA
**Bot responds**: *"Based on your answers, you may qualify for plans between $150k–$500k."*

**Alternate CTA**: *"Based on your answers, you may qualify for coverage options. Would you like a licensed agent to prepare a personalized quote?"*

---

### Step 8 — Lead Capture (MOST IMPORTANT)
Collect:
- **Name**
- **Email**
- **Phone**
- **Zip Code**

---

### Step 9 — Appointment Booking
Immediately after lead capture:
> *"Would you like to schedule a quick consultation?"*

Integrate with **Calendly** or **Google Calendar** for 10-minute call scheduling.

---

## AI Lead Scoring Matrix

| Profile | Score | Routing |
|---------|-------|---------|
| Homeowner + $250K+ coverage | ⭐⭐⭐⭐⭐ (5 stars) | Immediately routed to live agent's CRM queue |
| Age 50+ + mortgage protection | ⭐⭐⭐⭐ (4 stars) | High priority routing |
| Renter + "just exploring" | ⭐⭐ (2 stars) | Bypass human agents → automated email nurture sequence |

---

## Objection Handling Scripts

### "I'm just looking"
> *"No problem. Would you like a quick estimate while you're here?"*

### "I already have insurance"
> *"Many homeowners keep a separate policy specifically to protect their mortgage so their family keeps the house."*

---

## Conversion Boosting Message
Display early in conversation:
> *"Most homeowners can qualify for mortgage protection coverage in under 2 minutes."*

---

## 5 Psychology-Based Scripts
> ⚠️ **NOT INCLUDED** in the source documents. The DOCX teases: *"If you want, I can also show you something extremely powerful: The 5 chatbot scripts that convert insurance website visitors into booked appointments at 35–45%. Most agencies don't know these. They are psychology based conversation triggers."*
>
> **Action Required**: Request these scripts from the document's author.

---

# Part 5 — Multilingual Support

| Item | Detail |
|------|--------|
| **Primary languages** | English + Spanish |
| **Spanish importance** | *"Very important in California"* — estimated to *"double conversions"* |
| **Detection method** | Hybrid: auto-detect via browser locale + user preference selector |
| **Translation glossary** | ❌ Not provided — needs professional insurance terminology translation |
| **CA language access mandates** | ❌ Not specified in sources |
| **WCAG/ADA accessibility** | ❌ Not specified in sources |
| **Other languages** | Not recommended in current scope (EN + ES only) |

---

# Part 6 — Conversation Scripts & Educational Content

## Mortgage Protection Education
> *"Mortgage protection insurance ensures your family can stay in their home by paying off the remaining mortgage balance if something happens to you."*

Additional topics to cover:
- What mortgage protection is and how it works
- How it pays off the house
- Difference between term life vs. mortgage protection *(exact comparison script not provided)*

## Trust-Building Statements
1. *"Our agents are licensed and registered through the National Insurance Producer Registry."*

## Conversion Booster
> *"Most homeowners can qualify for mortgage protection coverage in under 2 minutes."*

## Urgency/Scarcity Messages
❌ No specific urgency messaging provided (e.g., "rates increase with age" not included)

## Testimonials / Social Proof
❌ Not provided in source documents

## Life Insurance Type Explanations (Plain Language)

### Term Life
> A death benefit for a fixed period (10, 20, or 30 years). Typically the least expensive option with no cash value. Best for income replacement during working years.

### Whole Life
> A permanent policy with fixed premiums and guaranteed cash value growth. Used for long-term protection and estate planning.

### Universal Life (Including IUL)
> Flexible premiums and flexible death benefit. Cash value tied to interest or market indexes. IUL offers tax-deferred growth linked to a market index with a guaranteed floor against loss.

### Variable Life
> The most complex permanent option. Cash value invested in the market — higher risk and higher reward potential. *Agents must be FINRA-registered to sell.*

## Annuity Explanations (If Asked)

### Fixed Annuity
> The insurer guarantees a minimum interest rate. Conservative, predictable income shielded from market volatility.

### Indexed Annuity
> Interest credited based on a market index (like S&P 500) with caps and floors. Principal guaranteed against market loss.

### Variable Annuity
> Assets tied to underlying investments. Growth depends on market performance — owner assumes market risk.

## California-Specific Scenarios

### Scenario 1 — Young Family in San Jose
> 35-year-old software engineer with spouse and young child buys a 20-year term policy to replace income. Agent provides clear disclosures of premiums, benefits, and riders.

### Scenario 2 — Business Owner in LA
> 60-year-old small business owner buys permanent life policy to fund a buy-sell agreement. Agent complies with CA replacement rules if switching from older policy.

---

# Part 7 — Technical Integration & CRM

## Data Capture Fields
The chatbot captures and sends to CRM:

| Field | Source |
|-------|--------|
| Name | Lead capture form |
| Email | Lead capture form |
| Phone | Lead capture form |
| Zip Code | Lead capture form |
| Coverage type | Qualification flow (Mortgage/Family/Final Expenses/Business) |
| Coverage amount | Qualification flow ($100K/$250K/$500K/$1M+/Not sure) |
| Age range | Qualification flow |
| Tobacco use | Qualification flow (Yes/No/Occasionally) |
| State of residence | Qualification flow |
| Homeowner status | Qualification flow (Yes/No/Planning to buy) |
| AI Lead Score | System-generated (1-5 stars) |

## Data Normalization
- All conversational data serialized into **ACORD TXLife 103** (New Business Submission) JSON format
- Enables instant ingestion by major carriers' automated underwriting engines
- Eliminates manual data entry → enables **straight-through processing**

## Appointment Scheduling
- Integrate with **Calendly API** or **Google Calendar API**
- Chatbot prompts: *"Would you like to schedule a 10-minute call to review your options?"*

## Agent Notification System
Upon lead capture, trigger simultaneously:
1. **CRM entry** (with all captured fields + lead score)
2. **Email notification** to assigned agent
3. **Text/SMS notification** to assigned agent

## Lead Routing Logic

### Priority-Based Routing
| Lead Score | Action |
|-----------|--------|
| ⭐⭐⭐⭐⭐ (5 stars) | Immediately routed via API to live agent's CRM queue |
| ⭐⭐⭐⭐ (4 stars) | High-priority routing to agent queue |
| ⭐⭐ (2 stars) | Bypass human agents → automated email nurture sequence |

### Compliance-Based Routing
Before assigning a California lead to an agent:
1. System triggers **ACORD TXLife 228** (Producer Inquiry)
2. Verifies agent has completed 8-hour Best Interest training
3. If non-compliant → **auto-reassign to certified agent**

## Quoting Engine Integration
- No specific quoting engine named (Quotit, iBridge not mentioned)
- ACORD TXLife 103 format ensures compatibility with any major carrier's system

## Pricing Data Architecture (STAG Pipeline)
- Chatbot uses **Structure Augmented Generation (STAG)** instead of relying on AI model memory
- When calculating premium estimates → queries a **Relational Database** containing "Gold Layer" ACORD JSON data
- Delivers real-time, mathematically accurate pricing at moment of query
- Avoids knowledge cutoff issues of fine-tuned models

## Analytics & Monitoring
- **Azure AI Foundry Observability**
- **Application Insights + OpenTelemetry**
- Captures: latency per tool call, token consumption, reasoning traces, policy evaluations
- **Azure AI Foundry Evaluation Dashboard** for testing and edge-case simulation

## 24/7 Operation
- Chatbot runs **24/7**
- When agents offline: *"Our agents may be offline, but I can help you get a quote started."*
- Collects leads while agents sleep

---

# Part 8 — Pricing, Quoting & Rate Display

## Strategy: Generic Ranges, Not Carrier-Specific
- Show **rough price ranges** to increase engagement
- *"People love instant numbers"* — increases user engagement
- Do NOT show carrier-specific rates in chatbot

## Available Pricing Data

| Product | Sample | Details |
|---------|--------|---------|
| Mortgage Protection | $30–$45/month | Healthy 35-year-old non-smoker, $250K coverage |
| Term Life | ❌ Not provided | — |
| Final Expense | ❌ Not provided | — |
| Business Insurance | ❌ Not provided | — |

## Required Disclaimers
Under SB 263, if conversation shifts to actual policy recommendation, system must deliver:
- Surrender period and charge disclosures
- Mortality and expense fee disclosures
- Investment advisory fee disclosures
- Tax penalty disclosures
- Market risk disclosures

> **Recommended chatbot disclaimer**: *"These are estimated ranges for illustration purposes only. Actual rates are determined through underwriting and may vary based on your health, lifestyle, and other factors."*

## Rate Update Mechanism
- STAG pipeline queries relational database for real-time data
- When carrier rates change → update database → instantly reflected in chatbot
- No model retraining required

---

# Part 9 — Appointment & Follow-Up Workflow

## Automated Post-Lead-Capture Flow

```
Lead Captured
    ↓
AI Lead Scoring (1-5 stars)
    ↓
Compliance Verification (ACORD TXLife 228)
    → Agent certified? → Route to agent CRM queue
    → Agent NOT certified? → Auto-reassign to certified agent
    ↓
Simultaneous Notifications
    → CRM entry created
    → Email sent to agent
    → SMS sent to agent
    ↓
Appointment Booking
    → Calendly/Google Calendar prompt to user
    ↓
Data Normalization
    → ACORD TXLife 103 JSON payload created
    → Ready for carrier automated underwriting
```

## Lead Routing by Score

| Score | Action |
|-------|--------|
| 5★ | Immediate API routing to live agent |
| 4★ | High-priority agent queue |
| 2★ | Automated email nurture sequence (no human agent) |

## What Gets Pre-Populated in CRM
- All contact info (Name, Email, Phone, Zip)
- All qualification data (coverage type, amount, age, tobacco, state, homeowner status)
- AI lead score (1-5 stars)
- Normalized via ACORD TXLife 103 standards

## Target Response Time
❌ Not specified. Architecture designed for **immediate** automated engagement. High-priority leads "immediately routed" to CRM.

## Automated Follow-Up Sequences
- Low-score leads → "automated email nurture sequences"
- High-score leads → agent notification + booking prompt
- Specific cadences (24h, 48h follow-ups) → ❌ Not defined in sources

## Agent Pre-Call Preparation
Per California regulations, agent must prepare:
- **For replacements (CIC 10509)**: Notice Regarding Replacement + written comparison of existing vs. proposed policies
- **For annuities (SB 263)**: State-mandated buyer's guide + written disclosures of conflicts, surrender charges, fees

## Pre-Appointment Questionnaire
Not explicitly specified, but per SB 263, agent must collect comprehensive suitability info before recommending:
- Annual income, liquid net worth, existing assets, liquidity needs, risk tolerance, tax status
- Can be collected during chat, via questionnaire, or during consultation

---

# Part 10 — Analytics, KPIs & Optimization

## Available Metrics

| Metric | Source |
|--------|--------|
| Website visitor → booked appointment | **35–45%** (claimed potential of psychology-based scripts) |
| All other conversion targets | ❌ Not defined — need from agency |

## Technical Monitoring Stack
- Azure AI Foundry Observability
- Application Insights + OpenTelemetry
- Tracks: latency, token consumption, reasoning traces, tool-call frequencies
- Azure Monitor alerts for anomaly detection
- Azure AI Foundry Evaluation Dashboard for testing

## Items Needing Agency Input
- ❌ Target conversion rates (conversations → leads → appointments → policies)
- ❌ Drop-off tracking specifics for each qualification step
- ❌ A/B test priorities (greeting variants, CTA copy, flow order)
- ❌ Monthly reporting format requirements
- ❌ User satisfaction mechanism (thumbs up/down, NPS)

---

# Part 11 — Security, Privacy & Data Handling

## PII Being Collected
Name, Email, Phone, Zip Code, Age Range, Tobacco Use, Homeowner Status, State of Residence

## Known Requirements
- CCPA: Consumers can opt-out of automated decision-making and behavioral profiling
- High-risk AI systems must maintain tamper-proof event logs
- California data residency considerations

## Items Needing Specification
- ❌ Encryption standards (at rest, in transit)
- ❌ Conversation transcript retention period
- ❌ Exact CCPA consent language for chatbot
- ❌ Data deletion request process
- ❌ List of third-party data processors
- ❌ Privacy impact assessment requirements

---

# Part 12 — Edge Cases & Error Handling

## Off-Topic Questions (Auto, Homeowners, Health Insurance)
- Chatbot MVP is scoped to 4 products only
- Orchestrator Agent limits selection to Mortgage/Family/Final Expenses/Business
- ❌ No specific redirect script provided for out-of-scope products
- **Recommendation**: *"We currently specialize in life insurance and mortgage protection. For auto/home/health insurance, please contact our office at [phone]."*

## Claims-Related Questions
- Not in chatbot scope (MVP = lead generation only)
- ❌ No claims redirect script provided
- **Recommendation**: Redirect to agency phone number

## Minors (Under 18)
- No specific logic defined
- Age qualification groups all young users into "Under 30" bracket
- **Recommendation**: Add "Under 18" check → redirect message

## Cannot Determine Eligibility
- **Self-Healing Agent** activates for edge cases
- If Compliance Agent flags violation (e.g., Medi-Cal limits) → Self-Healing Agent formulates corrective path
- Example: Asks user to adjust coverage amount to satisfy Medi-Cal limits

## Abusive / Inappropriate Messages
- System uses **Zero-Trust and Defensive Engineering**
- Pre-deployment: exhaustive **AI Red Teaming** (adversarial attacks, jailbreak attempts)
- Responses scored on: Groundedness, Relevance, Fluency, Task Adherence
- Professional boundaries maintained regardless of input

## Fallback Messages
- **Generic fallback**: Cached, pre-approved responses if primary models experience issues
- **Agent offline fallback**: *"Our agents may be offline, but I can help you get a quote started."*
- Technical: Self-Healing Agent executes exponential backoff + simplified reasoning mode

## "Talk to a Human" Button
- Not explicitly specified as persistent UI element
- But conversational flow actively pushes for human handoff:
  > *"Would you like a licensed agent to prepare a personalized quote?"*
- 5★ leads are automatically routed to live agent
- **Recommendation**: Include persistent "Talk to Agent" button in chat widget

---

# Part 13 — Deployment & Launch Plan

## Deployment Strategy
- **MVP-first approach** (confirmed in architecture)
- Tightly scoped: high-conversion lead generation + intelligent routing
- Validate architecture before scaling to multi-agent complexity

## Pre-Launch Testing
- **AI Red Teaming**: Adversarial attacks, jailbreak attempts, edge-case queries
- **Azure AI Foundry Evaluation Dashboard**: Automated scoring
- Metrics: Groundedness, Relevance, Fluency, Task Adherence

## SB 263 Compliance Timeline
- SB 263 regulations went into effect **January 1, 2025**
- Chatbot must be compliant from day one

## Items Needing Agency Input
- ❌ Target launch date
- ❌ Agent training plan for handling chatbot leads
- ❌ Feedback channel for agent-reported chatbot issues (Slack, ticketing system, etc.)

---

# Part 14 — Future Roadmap

## Already Architected (Ready for Expansion)

| Feature | Status |
|---------|--------|
| **Annuity support** | Backend already enforces SB 263. Flow extracts suitability data (liquid assets, risk tolerance, etc.). Compliance agent evaluates premiums against Medi-Cal limits. |
| **Multi-state expansion** | System checks non-resident licensing for non-CA states. Loads CA-specific compliance modules when California selected. |
| **Carrier straight-through processing** | ACORD TXLife 103 JSON enables instant carrier underwriting ingestion |
| **Regulatory change management** | Policy-as-Code via Open Policy Agent (OPA) + Rego language. Update one variable → propagates across entire system. No model retraining needed. |

## Not Yet Planned

| Feature | Status |
|---------|--------|
| Auto / homeowners insurance | ❌ Not in current scope or roadmap |
| AI voice (IVR, voice assistant) | ❌ No information in sources |
| Policy servicing (payments, changes, docs) | ❌ Not in scope — MVP is lead gen only |

---

# Appendix A — Key Data Standards

## ACORD TXLife Standards Used

| Standard | Purpose |
|----------|---------|
| **TXLife 103** | New Business Submission — serializes chatbot lead data for carrier ingestion |
| **TXLife 228** | Producer Inquiry — verifies agent licensing and training compliance |

## Technology Stack (From Architecture Blueprint)

| Component | Technology |
|-----------|-----------|
| Orchestration | Multi-agent architecture with Orchestrator Agent |
| Compliance | Open Policy Agent (OPA) with Rego language |
| Pricing | Structure Augmented Generation (STAG) + Relational Database |
| Data Layer | Medallion Lakehouse (Bronze → Silver → Gold) |
| Monitoring | Azure AI Foundry + Application Insights + OpenTelemetry |
| Error Recovery | Self-Healing Agent with exponential backoff |
| Security | Zero-Trust + AI Red Teaming |
| Scheduling | Calendly API or Google Calendar API |
| Notifications | CRM + Email + SMS |

---

# Appendix B — All Chatbot Scripts (Quick Reference)

## Greeting / Opening
> *(Script not provided — needs design)*

## Coverage Type Prompt
> *"What type of coverage are you looking for?"*

## Coverage Amount Prompt
> *"How much coverage are you looking for?"*

## Age Range Prompt
> *(Exact prompt text not provided)*

## State Verification
> *"What state do you live in?"*
> **If CA**: *"Great, we currently serve residents of California."*

## Tobacco Question
> *"Do you currently use tobacco?"*

## Homeowner Question
> *"Do you currently own a home with a mortgage?"*

## Qualification CTA
> *"Based on your answers, you may qualify for plans between $150k–$500k."*
>
> *"Based on your answers, you may qualify for coverage options. Would you like a licensed agent to prepare a personalized quote?"*

## Mortgage Protection Education
> *"Mortgage protection insurance ensures your family can stay in their home by paying off the remaining mortgage balance if something happens to you."*

## Conversion Booster
> *"Most homeowners can qualify for mortgage protection coverage in under 2 minutes."*

## Trust Statement
> *"Our agents are licensed and registered through the National Insurance Producer Registry."*

## Objection: "I'm just looking"
> *"No problem. Would you like a quick estimate while you're here?"*

## Objection: "I already have insurance"
> *"Many homeowners keep a separate policy specifically to protect their mortgage so their family keeps the house."*

## Appointment Booking
> *"Would you like to schedule a quick consultation?"*
> *"Would you like to schedule a 10-minute call to review your options?"*

## Agent Offline
> *"Our agents may be offline, but I can help you get a quote started."*

## Sample Price Quote
> *"A healthy 35-year-old non-smoker seeking $250,000 in mortgage protection coverage may pay between $30–$45/month."*

---

# Appendix C — Items Requiring Agency Input

> These items are **NOT available** in the source documents and must be collected directly from Intermarq Agency stakeholders.

### Critical (Blocks Build)
1. Insurance carriers and specific products for each line
2. CA DOI license number and NPN
3. CRM platform and API details
4. Brand kit (logo, colors, fonts, tone)
5. Website platform for chatbot widget embedding
6. Full rate tables for all product lines

### Important (Can Use Defaults Initially)
7. Preferred contact method for leads
8. Exact appointment scheduling tool choice (Calendly vs Google Calendar)
9. Lead-to-close conversion benchmarks
10. The 5 psychology-based conversion scripts
11. Target launch date
12. Agent training plan for chatbot leads
13. Monthly reporting format

### Nice to Have
14. Top 10 FAQs per product line
15. Customer testimonials / social proof
16. Urgency messaging preferences
17. Spanish translation glossary
18. A/B test priorities
19. User satisfaction survey format
