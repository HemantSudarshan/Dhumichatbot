# Test Suite for Mortgage Protection Insurance Chatbot

This test suite is organized from easy sanity checks to complex, end‑to‑end and edge‑case scenarios.

---

## 1. Easy – Basic Greeting, Language, and Channel

### TC-001: Chatbot greeting on first visit
- **Goal:** Ensure chatbot displays initial greeting when a new visitor lands on the site.
- **Preconditions:** New browser session, cookies cleared.
- **Steps:**
  1. Open the website home page.
  2. Wait 5 seconds.
- **Expected result:**
  - Chat widget is visible.
  - A greeting message appears (e.g., “Hi, I can help you explore mortgage protection options.”).

### TC-002: Multilingual language selection (English)
- **Goal:** Ensure user can select English and the bot responds in English.
- **Preconditions:** Chat widget visible.
- **Steps:**
  1. Click the chat widget.
  2. When prompted for language, select **English**.
- **Expected result:**
  - Bot confirms language: “You’re all set, I’ll help you in English.”
  - All subsequent messages are in English.

### TC-003: Multilingual language selection (Spanish)
- **Goal:** Ensure user can select Spanish and the bot responds in Spanish.
- **Preconditions:** Chat widget visible.
- **Steps:**
  1. Click the chat widget.
  2. When prompted for language, select **Spanish**.
- **Expected result:**
  - Bot confirms language in Spanish.
  - All subsequent messages are in Spanish.

### TC-004: Chatbot availability message when agents offline
- **Goal:** Verify that when human agents are offline, the bot still collects leads.
- **Preconditions:** Agents are configured as offline in the system.
- **Steps:**
  1. Start a new chat.
- **Expected result:**
  - Bot shows message similar to: “Our agents may be offline, but I can help you get a quote started.”

---

## 2. Easy – Core Intent Question (“What are you looking to protect?”)

### TC-010: Intent question shown at start
- **Goal:** Ensure the bot asks the main intent question early in the flow.
- **Preconditions:** Chat open, language selected.
- **Steps:**
  1. Start chat until first question from bot.
- **Expected result:**
  - Bot asks: “What would you like to protect today?”
  - Options shown as buttons: **My Mortgage**, **My Family**, **Final Expenses**, **Business Protection**, **Just exploring**.

### TC-011: Select “My Mortgage” intent
- **Goal:** Ensure correct downstream flow for mortgage protection.
- **Preconditions:** Intent question is visible.
- **Steps:**
  1. Click **My Mortgage**.
- **Expected result:**
  - Bot acknowledges mortgage protection intent.
  - Next question is about **coverage amount** or **homeowner status**.

### TC-012: Select “Just exploring” intent
- **Goal:** Ensure low-intent visitors are still engaged.
- **Preconditions:** Intent question is visible.
- **Steps:**
  1. Click **Just exploring**.
- **Expected result:**
  - Bot responds with a friendly, low-pressure message (e.g., “No problem. Would you like a quick estimate while you’re here?”).

---

## 3. Medium – Qualification Questions (Coverage, Age, Tobacco, State, Homeowner)

### TC-020: Coverage amount options
- **Goal:** Verify coverage amount presets and handling of “Not sure yet”.
- **Preconditions:** User chose a protection intent (e.g., My Mortgage).
- **Steps:**
  1. Proceed until bot asks: “How much coverage are you considering?”
- **Expected result:**
  - Buttons: **$100,000**, **$250,000**, **$500,000**, **$1,000,000+**, **Not sure yet**.

### TC-021: Coverage amount – serious buyer
- **Goal:** Ensure selection of a specific coverage amount is accepted.
- **Preconditions:** Coverage question visible.
- **Steps:**
  1. Select **$250,000**.
- **Expected result:**
  - Bot confirms selected coverage.
  - Internal lead score should increase (if visible in logs/CRM).

### TC-022: Coverage amount – “Not sure yet”
- **Goal:** Ensure bot handles uncertain users gracefully.
- **Preconditions:** Coverage question visible.
- **Steps:**
  1. Select **Not sure yet**.
- **Expected result:**
  - Bot provides guidance (e.g., suggests typical coverage ranges or asks follow-up questions).

### TC-023: Age range question and options
- **Goal:** Verify that age ranges are shown correctly.
- **Preconditions:** Reached age question.
- **Steps:**
  1. Proceed until bot asks: “Which age range do you fall into?”
- **Expected result:**
  - Buttons: **Under 30**, **30–39**, **40–49**, **50–59**, **60+**.

### TC-024: Tobacco use question and options
- **Goal:** Ensure tobacco use question appears and options are correct.
- **Preconditions:** Reached tobacco question.
- **Steps:**
  1. Proceed until bot asks: “Do you currently use tobacco products?”
- **Expected result:**
  - Buttons: **Yes**, **No**, **Occasionally**.

### TC-025: State of residence question
- **Goal:** Verify state question and licensing logic.
- **Preconditions:** Reached state question.
- **Steps:**
  1. When asked “What state do you live in?”, enter **California**.
- **Expected result:**
  - Bot replies: e.g., “Great, we currently serve residents of California.”

### TC-026: State not served
- **Goal:** Ensure user is informed when outside licensed states.
- **Preconditions:** Reached state question; system configured with at least one unsupported state.
- **Steps:**
  1. Enter a state not in the licensed list.
- **Expected result:**
  - Bot politely explains service is unavailable and may offer generic education instead of quotes.

### TC-027: Homeowner question
- **Goal:** Verify homeowner question flow.
- **Preconditions:** Reached homeowner question.
- **Steps:**
  1. Bot asks: “Do you currently own a home with a mortgage?”
- **Expected result:**
  - Buttons: **Yes**, **No**, **Planning to buy**.

### TC-028: Homeowner = Yes (high-intent)
- **Goal:** Ensure homeowners are treated as high-value leads.
- **Preconditions:** Homeowner question visible.
- **Steps:**
  1. Select **Yes**.
- **Expected result:**
  - Bot acknowledges mortgage holder is an ideal client.
  - Lead score should be high.

---

## 4. Medium – Education and Objection Handling

### TC-030: Mortgage protection education basics
- **Goal:** Ensure bot can explain mortgage protection clearly.
- **Preconditions:** User intent = My Mortgage or relevant.
- **Steps:**
  1. Ask: “What is mortgage protection insurance?” or choose a help/learn-more option.
- **Expected result:**
  - Bot explains that mortgage protection helps pay off the mortgage balance if the insured passes away.
  - May mention difference between term life vs mortgage protection.

### TC-031: Objection – “I already have life insurance.”
- **Goal:** Verify scripted response for common objection.
- **Preconditions:** In conversation; user has given some basic info.
- **Steps:**
  1. User types: “I already have life insurance.”
- **Expected result:**
  - Bot responds along the lines of: “Many homeowners keep a separate policy specifically to protect their mortgage so their family keeps the house.”

### TC-032: Objection – “I’m just looking.”
- **Goal:** Ensure the bot re-engages low-intent users.
- **Preconditions:** In conversation.
- **Steps:**
  1. User types: “I’m just looking.”
- **Expected result:**
  - Bot says something like: “No problem. Would you like a quick estimate while you’re here?”

---

## 5. Medium – Lead Capture and CRM Handoff

### TC-040: Lead capture prompt before exit
- **Goal:** Ensure bot attempts lead capture before visitor leaves.
- **Preconditions:** Visitor has answered at least 2–3 qualification questions.
- **Steps:**
  1. Stop responding for a configured inactivity period or move towards end of flow.
- **Expected result:**
  - Bot asks: “Would you like a licensed agent to send you a personalized quote?”
  - Fields requested: **Name**, **Email**, **Phone**, **Zip Code**.

### TC-041: Lead capture – all valid fields
- **Goal:** Verify form validation on standard, valid inputs.
- **Preconditions:** Lead capture form visible.
- **Steps:**
  1. Enter a valid name.
  2. Enter a valid email.
  3. Enter a valid phone number.
  4. Enter a valid ZIP code.
  5. Submit.
- **Expected result:**
  - Bot confirms lead submission.
  - Lead is stored in CRM and optionally sent via email/text.

### TC-042: Lead capture – invalid email format
- **Goal:** Ensure invalid emails are rejected.
- **Preconditions:** Lead capture form visible.
- **Steps:**
  1. Enter `abc@` as email.
  2. Submit.
- **Expected result:**
  - Bot shows an error or validation message.
  - Lead is not submitted until a valid email is entered.

### TC-043: Lead capture – missing required phone
- **Goal:** Ensure required fields are enforced.
- **Preconditions:** Lead capture form visible.
- **Steps:**
  1. Leave phone empty.
  2. Fill other fields correctly.
  3. Submit.
- **Expected result:**
  - Bot shows that phone is required.
  - Lead submission is blocked until phone is provided (if phone is required by business rules).

### TC-044: Data sync to CRM
- **Goal:** Verify integration with CRM/email/text systems.
- **Preconditions:** CRM integration configured.
- **Steps:**
  1. Complete a full lead capture flow.
  2. Open CRM or notification channel.
- **Expected result:**
  - Lead record appears with captured fields and conversation metadata.

---

## 6. Medium – Appointment Scheduling Integration

### TC-050: Offer appointment after lead capture
- **Goal:** Ensure bot offers to schedule a consultation after collecting lead info.
- **Preconditions:** Lead capture submitted successfully.
- **Steps:**
  1. After lead submission, continue the flow.
- **Expected result:**
  - Bot asks: “Would you like to schedule a quick consultation?”
  - Options/buttons to open Calendly or Google Calendar.

### TC-051: Calendly integration – open link
- **Goal:** Verify that Calendly link opens.
- **Preconditions:** Calendly URL configured.
- **Steps:**
  1. Click the Calendly booking option.
- **Expected result:**
  - New tab or modal opens with Calendly scheduling page.

### TC-052: Google Calendar integration – open link
- **Goal:** Verify that Google Calendar link opens.
- **Preconditions:** Google Calendar URL/configuration present.
- **Steps:**
  1. Click the Google Calendar booking option.
- **Expected result:**
  - New tab or modal opens with Google Calendar or scheduling page.

---

## 7. Hard – Pricing Estimation Logic

### TC-060: Quote range for healthy 35-year-old non-smoker, $250k mortgage protection
- **Goal:** Ensure pricing example aligns with business rules.
- **Preconditions:** Pricing logic configured.
- **Steps:**
  1. Select intent: **My Mortgage**.
  2. Coverage amount: **$250,000**.
  3. Age range: **30–39**.
  4. Tobacco use: **No**.
- **Expected result:**
  - Bot returns a range close to the business rule (e.g., “You may pay between $30–$45/month.”).

### TC-061: Price range sensitivity – older age with tobacco use
- **Goal:** Verify higher risk factors increase estimated premium.
- **Preconditions:** Pricing logic configured.
- **Steps:**
  1. Select similar coverage but age **50–59** and tobacco **Yes**.
- **Expected result:**
  - Estimated monthly premium range is significantly higher than in TC-060.

### TC-062: “Not sure yet” coverage – generic price guidance
- **Goal:** Ensure bot handles unknown coverage amount.
- **Preconditions:** Coverage amount = Not sure yet.
- **Steps:**
  1. Provide age and tobacco info.
- **Expected result:**
  - Bot gives a broad example or asks clarifying questions rather than a precise quote.

---

## 8. Hard – AI Lead Scoring

### TC-070: Lead scoring – high score profile
- **Goal:** Validate scoring for a high-intent profile.
- **Profile:** Homeowner, coverage ≥ $250k, age 30–50, non-smoker.
- **Preconditions:** AI lead scoring enabled; lead scoring visible via logs/CRM.
- **Steps:**
  1. Complete flow with: My Mortgage, $250,000 or higher, Age 30–39, Tobacco = No, Homeowner = Yes.
- **Expected result:**
  - Lead score is at or near the maximum (e.g., 5 stars or top tier).

### TC-071: Lead scoring – medium score profile
- **Goal:** Validate scoring for a medium-intent profile.
- **Profile:** Renter, exploring, moderate coverage.
- **Steps:**
  1. Choose **Just exploring** or **Final Expenses**.
  2. Coverage: $100,000.
  3. Age: 40–49.
  4. Tobacco: Occasionally.
- **Expected result:**
  - Lead score in mid-range (e.g., 2–3 stars).

### TC-072: Lead scoring – low score profile
- **Goal:** Validate scoring for low-intent profile.
- **Profile:** Renter, exploring, no clear coverage amount.
- **Steps:**
  1. Intent: Just exploring.
  2. Coverage: Not sure yet.
  3. Age: Under 30.
  4. Tobacco: No.
  5. Homeowner: No.
- **Expected result:**
  - Lead score is low (e.g., 1–2 stars), but lead can still be stored.

---

## 9. Hard – License Verification and Trust Messaging

### TC-080: License verification message
- **Goal:** Ensure trust-building message is available.
- **Preconditions:** License verification feature enabled.
- **Steps:**
  1. Ask: “Are your agents licensed?”
- **Expected result:**
  - Bot responds with a statement like: “Our agents are licensed and registered through the National Insurance Producer Registry.”

### TC-081: License verification on state mismatch
- **Goal:** Check behavior when user in an unsupported state asks about licensing.
- **Preconditions:** State outside licensed area + license feature enabled.
- **Steps:**
  1. Enter unsupported state.
  2. Ask if agents are licensed.
- **Expected result:**
  - Bot still confirms agents are licensed, but clearly states that service is not available in that user’s state.

---

## 10. Complex – End-to-End High-Intent Scenario

### TC-090: Full journey – qualified homeowner to booked appointment
- **Goal:** Validate full conversion funnel for ideal customer.
- **Preconditions:** All integrations active (CRM, Calendly/Google Calendar, email/SMS).
- **Steps:**
  1. Start chat, choose English.
  2. Intent: My Mortgage.
  3. Coverage: $250,000 or $500,000.
  4. Age: 30–39.
  5. Tobacco: No.
  6. State: Supported state (e.g., California).
  7. Homeowner: Yes.
  8. Complete education and objection steps if presented.
  9. Provide lead info (Name, Email, Phone, ZIP).
  10. Accept appointment offer and book via Calendly/Google Calendar.
- **Expected result:**
  - User receives an estimated quote range.
  - Lead is stored in CRM with high score.
  - Appointment is successfully booked and visible on agent’s calendar.

---

## 11. Complex – End-to-End Low-Intent / Education-Only Scenario

### TC-100: Informational journey – user just exploring
- **Goal:** Ensure non-buyers still get value and soft lead capture attempts.
- **Preconditions:** Chat online.
- **Steps:**
  1. Start chat, choose language.
  2. Intent: Just exploring.
  3. Provide partial answers to questions; decline lead capture.
- **Expected result:**
  - Bot provides educational content (mortgage protection basics, pros/cons).
  - Bot attempts lead capture at least once.
  - If user declines, conversation ends politely without forcing submission.

---

## 12. Complex – Edge Cases, Validation, and Resilience

### TC-110: User changes intent mid-conversation
- **Goal:** Ensure bot can gracefully handle a user changing their mind.
- **Steps:**
  1. Start with intent = My Family.
  2. After a few questions, type: “Actually I want to protect my mortgage.”
- **Expected result:**
  - Bot recognizes intent change and either restarts or branches into the mortgage protection flow.

### TC-111: User provides free-text answers instead of clicking buttons
- **Goal:** Validate NLU mapping of free-text to expected options.
- **Steps:**
  1. When asked “Which age range do you fall into?”, type “35”.
  2. When asked “Do you use tobacco?”, type “Nope”.
- **Expected result:**
  - Bot maps age 35 to 30–39 range.
  - Bot understands “Nope” as “No”.

### TC-112: Incomplete qualification then direct lead capture
- **Goal:** Ensure bot can still capture a lead even with missing qualifiers.
- **Steps:**
  1. Answer only 1–2 questions.
  2. Stop responding.
- **Expected result:**
  - After inactivity or exit intent, bot still prompts for email/phone to “send more info later”.

### TC-113: Network/API failure during CRM submission
- **Goal:** Verify fallback behavior when CRM integration fails.
- **Preconditions:** Simulate CRM API failure.
- **Steps:**
  1. Complete lead capture.
  2. Observe failure in backend.
- **Expected result:**
  - Bot apologizes and indicates there was an issue.
  - Bot offers alternative, e.g., “Please email us at X” or retries submission.

### TC-114: Network/API failure for Calendly/Google Calendar
- **Goal:** Verify graceful handling when scheduling link cannot be loaded.
- **Preconditions:** Calendly/Calendar is temporarily unavailable.
- **Steps:**
  1. Attempt to book an appointment.
- **Expected result:**
  - Bot informs user of the issue and suggests a fallback (e.g., agent will follow up by email/phone).

### TC-115: Session timeout or browser refresh mid-flow
- **Goal:** Ensure experience is not completely lost.
- **Steps:**
  1. Start chat and answer several questions.
  2. Refresh page or close and reopen browser.
- **Expected result:**
  - Depending on design, either:
    - Conversation resumes from last saved state, or
    - Conversation restarts with a brief recap offer.

---

## 13. Complex – Analytics and Conversion Tracking (If Implemented)

### TC-120: Track key funnel events
- **Goal:** Ensure analytics events fire at critical steps.
- **Preconditions:** Analytics tools (e.g., GA, Segment) integrated.
- **Steps:**
  1. Start chat.
  2. Answer qualification questions.
  3. Submit lead form.
  4. Book appointment.
- **Expected result:**
  - Events logged for: Chat Started, Qualification Completed, Lead Submitted, Appointment Booked.

### TC-121: Attribution of leads to chatbot channel
- **Goal:** Verify leads from the chatbot are tagged distinctly.
- **Preconditions:** CRM and analytics integrated.
- **Steps:**
  1. Complete lead capture via chatbot.
  2. Inspect lead record in CRM.
- **Expected result:**
  - Lead source/channel is marked as “Chatbot” or equivalent for reporting.

---

This suite can be extended with implementation-specific IDs, success metrics (e.g., SLAs for response time), and negative security tests (e.g., injection attempts in free-text fields) once the exact stack and platform are defined.
