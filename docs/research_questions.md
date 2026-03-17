# 🔍 Research Questions — Intermarq Agency California Insurance Chatbot

> **Context**: These questions are derived from two source documents:
> 1. **CHATBOT SUGGESTIONS INTERMARQ AGENCY** — defines chatbot features (lead qualification, 7 converting questions, mortgage protection focus, lead capture, objection handling, multilingual, AI scoring)
> 2. **US California Insurance Overview** — covers CA regulations (CDI, Prop 103, life insurance, annuities, SB 263, suitability rules, agent training)
>
> Feed each section to your research chatbot. Compile the answers and share them back so we can build the chatbot end-to-end.

---

## Section 1 — Intermarq Agency & Business Context

> *We need to understand the agency's identity, carriers, and operations to configure the chatbot correctly.*

1. What insurance carriers does Intermarq Agency represent in California?
2. What geographic areas / zip codes does Intermarq Agency serve?
3. What are Intermarq Agency's **license numbers** (CA DOI license, NPN via NIPR)?
4. What is Intermarq Agency's primary value proposition vs competitors?
5. What **CRM system** does the agency currently use (Applied Epic, HawkSoft, AgencyZoom, etc.)?
6. What is the agency's current lead-to-close conversion rate and average response time?
7. What is the agency's **appointment scheduling tool** (Calendly, Google Calendar, Acuity, etc.)?
8. What is the **preferred contact method** for leads: phone call, text, email, or in-person?
9. What is the agency's **brand kit** (logo, primary/secondary colors, fonts, tone of voice)?
10. Does the agency have an **existing website** and what platform is it on (WordPress, Wix, custom)?

---

## Section 2 — Product & Coverage Deep Dive

> *The chatbot handles 4 product lines per the DOCX: Mortgage Protection, Life, Final Expense, and Business Insurance. We need exact details for each.*

### Mortgage Protection Insurance
11. What specific **mortgage protection** products does Intermarq offer? (Carrier names, product names, policy terms)
12. What are the **coverage amount ranges** for mortgage protection? (Document mentions $150k–$500k — confirm exact range)
13. What are the **typical monthly premiums** by age bracket for mortgage protection? (Doc mentions $30–$45/month for healthy 35-year-old non-smoker at $250k — need full table)
14. What are the **underwriting requirements** — is this simplified issue, guaranteed issue, or fully underwritten?
15. What **health conditions** disqualify or rate-up applicants for mortgage protection?
16. What is the **age eligibility range** for mortgage protection? (Doc mentions Under 30, 30–39, 40–49, 50–59, 60+)
17. How does mortgage protection differ from **standard term life** in policy structure and benefits?
18. What are the **key selling points** of mortgage protection vs. traditional life insurance?
19. What **riders** are available (accelerated death benefit, waiver of premium, disability rider)?

### Term Life Insurance
20. What **term life products** does Intermarq offer? (10, 15, 20, 30 year terms, carrier names)
21. What are the **coverage limits** available? (Doc mentions up to $1M+)
22. What is the **pricing structure** by age/gender/health class for term life?
23. What **conversion options** exist (term to permanent) and are they available with all carriers?
24. What medical exams or lab work are required vs. **no-exam options**?

### Final Expense / Burial Insurance
25. What **final expense products** does Intermarq offer? (Guaranteed issue vs. simplified issue)
26. What are the **coverage ranges** for final expense? (Typically $5k–$50k — confirm)
27. What are the **age eligibility** requirements for final expense? (Typically 50–85)
28. What are the **typical monthly premiums** for final expense by age?
29. What are the **graded benefit** vs. **immediate benefit** policy structures offered?
30. What **health questions** are asked on simplified issue final expense applications?

### Business Insurance
31. What **business insurance products** does Intermarq offer? (BOP, GL, WC, Professional Liability, Cyber, Key Person)
32. What **industries/business types** does the agency commonly write in California?
33. What are the **minimum premium** ranges for each business line?
34. What **information** is needed to quote business insurance? (Revenue, payroll, employee count, NAICS code, years in business)
35. Does the agency write **Workers' Compensation** in California? What carriers?
36. What **buy-sell agreement funding** solutions does the agency offer?

---

## Section 3 — California Regulatory Compliance for the Chatbot

> *Per the PDF, California is highly regulated (CDI, Prop 103, SB 263). The chatbot must comply.*

37. What **disclosures** must the chatbot display under California Insurance Code? (License info, privacy policy, non-binding nature of quotes)
38. Under **Proposition 103**, are there any rate disclosure requirements the chatbot must follow when showing price estimates?
39. Per **SB 263**, what specific buyer's guide or disclosure documents must be presented before or during a life insurance/annuity conversation?
40. What are the **suitability requirements** the chatbot must gather before recommending any product? (Age, income, existing coverage, financial objectives, risk tolerance — per PDF Page 10)
41. Must the chatbot disclose that it is **not a licensed agent** and is an AI/automated system?
42. Can the chatbot legally provide **price range estimates** (as suggested in the DOCX) without it being considered an insurance quote under CA law?
43. What are the **anti-churning/replacement** rules the chatbot must respect if a user says "I already have insurance"? (Per PDF Page 8)
44. What **record retention** requirements exist for chatbot conversations under CA insurance regulations?
45. What **CCPA/CPRA** disclosures must the chatbot present when collecting personal data (name, email, phone, zip, health info)?
46. Are there California-specific **telemarketing/TCPA** rules if the chatbot sends SMS follow-ups or collects phone numbers?
47. What are the **advertising compliance** rules for insurance chatbots in California? (Truth in advertising, no misleading claims)
48. Does the chatbot need to reference specific California insurance **code sections** in its disclosures?
49. What **CLHIGA (California Life and Health Insurance Guarantee Association)** disclosures, if any, should be mentioned?
50. Per the PDF, agents need a **4-hour training course** for non-term life/annuity sales — does the chatbot's lead qualification count as "selling" and trigger any compliance requirements?

---

## Section 4 — Lead Qualification Flow Details

> *The DOCX defines a specific lead qualification flow. We need granular details to build it.*

51. What are the **exact qualification criteria** to determine a "qualified lead" vs. "unqualified"? (Age range cutoffs, states served, coverage minimums)
52. What **disqualifying conditions** should immediately end the flow or redirect? (e.g., wrong state, too young/old, existing coverage)
53. For the **tobacco/smoking question**: what categories should be used? (Never, former, current, vape/e-cigarette, marijuana)
54. What **coverage amount brackets** should the chatbot present? (Doc suggests $100k–$250k, $250k–$500k, $500k–$1M, $1M+ — confirm exact brackets)
55. What **age range brackets** should be used? (Doc suggests Under 30, 30–39, 40–49, 50–59, 60+ — confirm and check against product eligibility)
56. For the **homeowner question** (Q6 in the DOCX): how should the chatbot handle renters vs. owners differently in the conversation flow?
57. What is the **ideal lead score formula**? (Doc mentions: Homeowner + $250k coverage = 5 stars — what's the full scoring matrix?)
58. What is the **exact CTA message** after qualification? (Doc suggests "Based on your answers, you may qualify for plans between $X–$Y" — need all variants by product)
59. How should the chatbot handle **"I'm just looking"** objection? (Doc mentions smart objection handling — need exact scripts)
60. How should the chatbot handle **"I already have insurance"** objection? (Need recommended response and flow)
61. What are the **5 psychology-based chatbot scripts** mentioned in the DOCX that convert at 35–45%? (Need the exact scripts or their structure)
62. What **follow-up actions** should trigger after lead capture? (CRM entry, email notification, SMS to agent, auto-email to lead, appointment booking)

---

## Section 5 — Multilingual & Accessibility

> *The DOCX recommends English + Spanish for California to double conversions.*

63. What **percentage of Intermarq's target market** speaks Spanish as a primary language?
64. Should the chatbot **detect language preference** automatically or present a language selector?
65. What **insurance terminology translations** are needed? (Policy = póliza, premium = prima, coverage = cobertura — need full glossary)
66. Are there any **California-mandated language access** requirements for insurance communications?
67. What **ADA/WCAG accessibility** standards must the chatbot meet? (Screen reader compatibility, keyboard navigation, color contrast)
68. Should the chatbot support any **other languages** beyond English and Spanish for the California market? (Mandarin, Korean, Vietnamese, Tagalog?)

---

## Section 6 — Conversation Scripts & Content

> *Need exact scripts for the chatbot's educational and objection-handling features.*

69. What is the exact **mortgage protection education script**? (Doc mentions "explains how term life pays off mortgage balance if something happens to you" — need full explanation)
70. What is the **term life vs. mortgage protection comparison** script? (Doc mentions this as a key education topic)
71. What are the **top 10 FAQs** the agency currently gets about each product line?
72. What **trust-building statements** should the chatbot use? (Doc mentions "licensed and registered through the National Insurance Producer Registry" — need all trust signals)
73. What **urgency/scarcity messages** are appropriate and compliant? (e.g., "rates increase with age")
74. What **testimonials or social proof** can the chatbot reference? (With compliance review)
75. What **educational content** should the chatbot offer about life insurance types? (Per PDF: term vs. whole vs. universal vs. variable — need plain-language explanations)
76. What **annuity education** should the chatbot provide if asked? (Per PDF: fixed vs. variable vs. indexed, accumulation vs. payout phases)
77. What **California-specific scenarios** should the chatbot handle? (Per PDF Page 9: 35-year-old in San Jose needing term life, 60-year-old in LA needing permanent for business)

---

## Section 7 — Technical Integration & CRM

> *Need to map infrastructure for the chatbot to integrate with existing agency systems.*

78. What **CRM** does the agency use and does it have an API for lead ingestion?
79. What **fields** should be captured and sent to the CRM? (Name, email, phone, zip, product interest, coverage amount, age, tobacco, homeowner status, lead score, conversation transcript)
80. What **appointment scheduling API** will be used? (Calendly API, Google Calendar API, etc.)
81. What **notification system** should alert agents of new leads? (Email, SMS, push notification, CRM alert, Slack)
82. Should the chatbot integrate with any **quoting engines** (Quotit, iBridge, carrier portals)?
83. What **website platform** will host the chatbot widget? (WordPress plugin, JavaScript embed, iframe)
84. Does the agency need a **dashboard** to view chatbot analytics? (Conversations, leads, conversion rates, drop-off points)
85. What **hours of operation** apply to live agent handoff vs. 24/7 chatbot-only mode?
86. Should leads be **routed to specific agents** based on product type, language, or location?

---

## Section 8 — Pricing, Quoting & Rate Display

> *The DOCX recommends showing price range estimates to increase engagement. Need exact data.*

87. Can you provide a **complete rate table** for mortgage protection by age, gender, health class, coverage amount, and term?
88. Can you provide a **complete rate table** for term life by the same variables?
89. Can you provide a **complete rate table** for final expense by age, gender, and coverage amount?
90. What **disclaimers** must accompany any price estimate shown by the chatbot? (e.g., "Rates are estimates only and subject to underwriting")
91. Should the chatbot show **carrier-specific rates** or **generic ranges**?
92. How frequently do rates change and how will the chatbot's rate data be **updated**?

---

## Section 9 — Appointment & Follow-Up Workflow

> *From lead capture to policy binding — what's the complete post-chatbot workflow?*

93. What is the **step-by-step workflow** after a lead is captured? (Agent receives notification → reviews lead score → contacts lead → needs analysis → application → underwriting → policy delivery)
94. What is the **target time** from lead capture to first agent contact? (Minutes, hours?)
95. What **automated follow-up sequences** should trigger after lead capture? (Thank you email, reminder SMS at 24h, follow-up at 48h, etc.)
96. What **documents** does the agent need to prepare before contacting a qualified lead?
97. What **information** should the chatbot pre-populate into the CRM before the agent call?
98. Should the chatbot send the lead a **pre-appointment form** or **needs assessment questionnaire**?

---

## Section 10 — Analytics, KPIs & Optimization

> *Measure chatbot performance and continuously improve.*

99. What is the **target conversion rate** for chatbot conversations to qualified leads?
100. What is the **target conversion rate** from qualified lead to booked appointment?
101. What is the **target conversion rate** from appointment to policy binding?
102. What **drop-off metrics** should be tracked at each step of the qualification flow?
103. Should the chatbot include a **user satisfaction survey** (thumbs up/down, NPS)?
104. What **A/B tests** should be run initially? (Greeting message variants, CTA copy, flow order)
105. What **monthly reporting** does the agency need? (Total conversations, qualified leads, appointments booked, policies bound, revenue attributed)

---

## Section 11 — Security, Privacy & Data Handling

> *PII is being collected (name, phone, email, health info). Must be handled carefully.*

106. What **encryption standards** are required for storing PII collected by the chatbot?
107. How long should **conversation transcripts** be retained?
108. What **consent language** must be shown before collecting personal information?
109. Should users be able to **request data deletion** (CCPA right to delete)?
110. What **third-party data processors** will have access to chatbot data? (CRM, email provider, SMS provider)
111. Is a **privacy impact assessment** required before deploying the chatbot?

---

## Section 12 — Edge Cases & Error Handling

> *Handle unexpected scenarios gracefully.*

112. How should the chatbot respond to **off-topic questions** (e.g., auto insurance, homeowners, health insurance — products not in the DOCX scope)?
113. Should the chatbot handle **claims-related questions** or redirect to a phone number?
114. How should the chatbot handle **minors** who interact with it? (Under 18)
115. What happens if the chatbot **cannot determine eligibility**? (Edge case health conditions, unusual coverage amounts)
116. How should the chatbot handle **abusive or inappropriate messages**?
117. What is the **fallback message** when the chatbot doesn't understand a query?
118. Should there be a **"talk to a human"** button always visible?

---

## Section 13 — Deployment & Launch Plan

119. What is the **target launch date** for the chatbot?
120. Should there be a **beta/soft launch** phase with limited traffic before full deployment?
121. What **training** do agents need on how leads will arrive from the chatbot?
122. What is the **chatbot testing plan** before go-live? (QA scripts, user testing, compliance review)
123. What **feedback loop** exists for agents to report chatbot issues or suggest improvements?

---

## Section 14 — Future Roadmap

124. Should the chatbot eventually handle **auto insurance and homeowners** quotes (beyond the current 4 product lines)?
125. Is there a plan to add **annuity education and qualification** to the chatbot? (The PDF covers annuities extensively)
126. Should the chatbot eventually support **multi-state** operations beyond California?
127. Is there interest in **AI voice** capabilities (phone-based IVR or voice assistant)?
128. Should the chatbot evolve to handle **policy servicing** (payments, changes, document requests)?
129. Is there a plan to integrate **real-time underwriting** or **instant decisioning** from carriers?
130. Should the chatbot track and respond to **California regulatory changes** automatically?

---

## How to Use This Document

1. **Feed one section at a time** to your research chatbot
2. **Compile the answers** into a structured knowledge base
3. **Share the compiled responses** back with me
4. I'll use those answers to build the complete chatbot — from conversation flows and UI to backend integrations and compliance

> ⚠️ **Priority Sections**: Start with **Section 1** (agency context) and **Section 2** (product details) — these are the foundation everything else builds on.
