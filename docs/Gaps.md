# Requirements Checklist — What Intermarq Agency Must Provide

> **Purpose**: Everything below is **missing from the source documents** and must be collected from Intermarq Agency stakeholders before (or during) the chatbot build.
>
> Items are ranked by priority: 🔴 **Blocks MVP** · 🟡 **Can use defaults initially** · 🟢 **Post-launch / nice-to-have**

---

## 🔴 Priority 1 — Blocks MVP Build

### Agency Identity & Licensing
- [ ] **CA DOI license number** and **NPN** (National Producer Number) — required for chatbot trust disclosure
- [ ] **Agency physical address** and **contact phone number** — for widget footer and fallback routing
- [ ] List of **carriers represented** in California — needed to configure product flows

### Brand & Design
- [ ] **Logo** (SVG or high-res PNG, light + dark variants)
- [ ] **Brand colors** (primary, secondary, accent — hex codes)
- [ ] **Typography** (preferred fonts or Google Fonts equivalent)
- [ ] **Tone of voice** guidelines (professional? friendly? empathetic? casual?)

### Product & Rate Data
- [ ] **Mortgage protection** — carrier names, product names, available term lengths, full rate table by age/gender/health/coverage
- [ ] **Term life** — carrier names, products, term lengths (10/15/20/30yr), rates by age/gender/health class, conversion options, exam vs no-exam
- [ ] **Final expense** — carrier names, coverage range (e.g., $5K–$50K), age eligibility, graded vs immediate benefit details, health questions asked, monthly premiums by age
- [ ] **Business insurance** — lines offered (BOP, GL, WC, Professional Liability, Cyber, Key Person), target industries, minimum premiums, quote intake fields
- [ ] **Available riders** for each product (accelerated death benefit, waiver of premium, disability, etc.)
- [ ] **Underwriting types** per product (simplified issue, guaranteed issue, fully underwritten)
- [ ] **Disqualifying health conditions** per product line

### CRM & Scheduling
- [ ] **CRM platform** name (Applied Epic, HawkSoft, AgencyZoom, Salesforce, HubSpot, etc.)
- [ ] **CRM API documentation** or integration method (API, Zapier, webhook, email-to-CRM)
- [ ] **Scheduling tool** — confirm **Calendly** or **Google Calendar** (the docs suggest both but don't confirm which)
- [ ] **Scheduling link** or API key for integration

### Website
- [ ] **Website URL** where chatbot will be deployed
- [ ] **Website platform** (WordPress, Wix, Squarespace, custom HTML, Webflow, etc.)
- [ ] Confirm **deployment method**: JavaScript embed, WordPress plugin, iframe, or other

---

## 🟡 Priority 2 — Can Use Smart Defaults, But Agency Input Preferred

### Lead Routing & Operations
- [ ] **Preferred contact method** for leads — phone call, text, email, or combo
- [ ] **Agent availability hours** for live handoff (e.g., Mon-Fri 9am-5pm PT)
- [ ] **Target response time** SLA — how quickly should an agent contact a 5★ lead? (5 min? 1 hour? same day?)
- [ ] **Lead routing rules** — should leads go to a specific agent by product type, language, or zip code?
- [ ] **Low-score lead nurture** — what happens to 2★ leads? Email drip sequence? Ignore? Monthly re-engagement?

### Pricing Display
- [ ] **Rate ranges by age bracket** for chatbot display (even rough ranges per product are helpful)
- [ ] **Price estimate disclaimer** — approve or customize: *"These are estimated ranges for illustration only. Actual rates determined through underwriting."*
- [ ] Decision: show **generic ranges** only (recommended) or attempt **carrier-specific** quotes?

### Follow-Up Automation
- [ ] **Automated email content** — thank you email copy after lead capture
- [ ] **Follow-up cadence** — e.g., 24h SMS reminder, 48h email, 7-day re-engagement
- [ ] **Email sender** — what email/domain sends automated follow-ups? (agency email, CRM, marketing tool)

### Compliance Specifics
- [ ] **CCPA consent language** — legal team to approve exact wording for data collection notice
- [ ] **Privacy policy URL** — link to existing policy or need to create one
- [ ] **Data retention policy** — how long to store conversation transcripts and PII
- [ ] **Third-party data processors list** — who touches the data (CRM provider, email provider, SMS provider, hosting)

### Multilingual
- [ ] **Spanish translation** of all chatbot scripts and educational content
- [ ] **Insurance glossary** in Spanish (e.g., policy = póliza, premium = prima, coverage = cobertura, deductible = deducible)
- [ ] Decision: support **other languages** besides EN/ES? (Mandarin, Korean, Vietnamese, Tagalog for CA market)

---

## 🟢 Priority 3 — Post-Launch / Enhancement Phase

### Conversion Scripts
- [ ] **The 5 psychology-based scripts** (35–45% conversion) mentioned in the DOCX — request from document author
- [ ] **Urgency/scarcity messages** approval (e.g., *"Rates typically increase with age — lock in today's rate"*)
- [ ] **Additional objection handling scripts** beyond the 2 provided
- [ ] **Customer testimonials / social proof** (with compliance review)

### Content & FAQs
- [ ] **Top 10 FAQs** the agency currently receives per product line
- [ ] **Term life vs mortgage protection comparison** — detailed explanation script
- [ ] **Final expense education script** — value proposition, who needs it, typical costs
- [ ] **Business insurance education script** — types of coverage, who needs what

### Analytics & KPIs
- [ ] **Target conversion rates**: conversations → qualified leads → appointments → policies
- [ ] **Monthly reporting format** — what does leadership want to see? (total conversations, leads, appointments, policies, revenue)
- [ ] **A/B testing priorities** — which elements to test first (greeting, CTA, flow order, pricing display)
- [ ] **User satisfaction mechanism** — thumbs up/down, 5-star, NPS, or none?

### Security & Privacy (Pre-Production Sign-Off)
- [ ] **Encryption standards** — confirm TLS 1.3 in transit, AES-256 at rest (or specify alternatives)
- [ ] **Privacy impact assessment** — does legal/compliance require one before launch?
- [ ] **Data residency** — must data stay in CA/US? Which cloud region?
- [ ] **Penetration testing** — required before go-live?

### Launch Planning
- [ ] **Target launch date**
- [ ] **Beta / soft launch plan** — limited traffic percentage or selected pages first?
- [ ] **Agent training session** — schedule a walkthrough for agents on how chatbot leads arrive in CRM
- [ ] **Feedback channel** — Slack channel, email alias, or ticketing system for agents to report chatbot issues
- [ ] **Rollback plan** — what to do if chatbot performs poorly after launch (disable widget, revert to contact form, etc.)

---

## Quick Summary

| Priority | Items | Status |
|----------|-------|--------|
| 🔴 Blocks MVP | 19 items | Must collect before build |
| 🟡 Defaults OK | 14 items | Can start with smart defaults |
| 🟢 Post-Launch | 18 items | Enhance after MVP is live |
| **Total** | **51 items** | |

---

> **Next Step**: Share this checklist with Intermarq Agency stakeholders. Start with the 🔴 items — once those are in, we can begin building the chatbot immediately.
