<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# i need more and more

Got it—you want an even larger, deeper test suite. Here are many additional test cases you can append to your existing markdown, continuing from the previous structure.

***

## 14. Complex – Conversation Quality, Tone, and Compliance

### TC-130: Friendly, non-pushy tone for low-intent users

- **Goal:** Ensure tone stays helpful and non-aggressive when user is just browsing.
- **Steps:**

1. Start chat and choose **Just exploring**.
2. Decline lead capture twice.
- **Expected result:**
    - Bot maintains friendly, educational tone.
    - No guilt-tripping or hard sell; conversation ends politely.


### TC-131: No misleading guarantees about approval

- **Goal:** Verify the bot does not promise guaranteed approval or fixed prices.
- **Steps:**

1. Ask: “Can you guarantee I’ll be approved?” or “So is this the final price?”.
- **Expected result:**
    - Bot clarifies that prices and approval depend on underwriting and carrier rules.
    - Uses safe phrasing like “estimated range” and “may qualify.”[^1]


### TC-132: Disclosure that quote is an estimate, not a binding offer

- **Goal:** Ensure regulatory-sound messaging around quotes.
- **Steps:**

1. Complete a basic quote flow to where bot shows price range (e.g., 30–45/month for 35-year-old non-smoker at 250k coverage).[^1]
- **Expected result:**
    - Bot clearly states that it is an estimate and final pricing may differ after full application.


### TC-133: No collection of sensitive data beyond configured scope

- **Goal:** Confirm bot does not request info like SSN, full medical history, etc., if not in requirements.
- **Steps:**

1. Go through full flow and review all questions asked.
- **Expected result:**
    - Only configured data points (age range, coverage, tobacco, state, contact info) are requested.[^1]

***

## 15. Complex – Security, Privacy, and Data Handling

### TC-140: Masking of sensitive fields (if applicable)

- **Goal:** Ensure sensitive fields (e.g., email, phone) are handled securely in UI.
- **Steps:**

1. Enter email and phone at lead capture step.
- **Expected result:**
    - Inputs are not exposed in URLs or logs visible to end user.
    - No echoing back of full phone/email more than necessary.


### TC-141: PII not logged in analytics debug console

- **Goal:** Ensure analytics/debug logs exclude full PII.
- **Steps:**

1. Enable browser dev tools and inspect network/console logs.
2. Complete a lead capture flow.
- **Expected result:**
    - Analytics events contain anonymized identifiers, not raw phone/email.


### TC-142: Conversation history is not visible to other users

- **Goal:** Protect user data between sessions.
- **Steps:**

1. Complete a conversation as User A in one browser.
2. Start new incognito session or different browser as User B.
- **Expected result:**
    - User B does not see User A’s previous conversation history.

***

## 16. Hard – Multi-Device and Multi-Browser Behavior

### TC-150: Desktop responsiveness

- **Goal:** Ensure chatbot widget works correctly on desktop resolutions.
- **Steps:**

1. Open site on desktop (≥ 1280px width).
2. Open and use chatbot through an end-to-end mortgage flow.
- **Expected result:**
    - Widget is visible, non-overlapping with key UI.
    - All buttons and messages readable and clickable.


### TC-151: Mobile responsiveness

- **Goal:** Verify usability on mobile.
- **Steps:**

1. Use mobile device or responsive mode (≤ 414px width).
2. Start chat and answer multiple questions.
- **Expected result:**
    - Chat UI fits screen, keyboard doesn’t hide input box.
    - Buttons scroll correctly and are tappable.


### TC-152: Cross-browser consistency

- **Goal:** Ensure major browsers behave consistently.
- **Steps:**

1. Run the same core journey (from greeting to lead capture) in Chrome, Firefox, Safari, and Edge.
- **Expected result:**
    - No layout breaks or missing messages.
    - All flows complete successfully in each browser.

***

## 17. Hard – Fallbacks for NLP Misunderstandings

### TC-160: Unrecognized question handling

- **Goal:** Ensure graceful fallback when bot doesn’t understand.
- **Steps:**

1. Type a random or off-topic message (e.g., “Tell me a joke about dragons and pizza”).
- **Expected result:**
    - Bot responds with a clarification or fallback, e.g., “I’m here to help with mortgage protection and life insurance. Do you want to see coverage options?”[^1]


### TC-161: Multiple intents in a single message

- **Goal:** Test how bot handles “multi-intent” inputs.
- **Steps:**

1. Type: “I want to protect my mortgage and maybe final expenses but I’m not sure yet.”
- **Expected result:**
    - Bot either:
        - Asks which to focus on first, or
        - Picks a primary intent (e.g., mortgage) and confirms with user.


### TC-162: Re-asking a misunderstood question

- **Goal:** Confirm bot can re-ask or rephrase for clarity.
- **Steps:**

1. Answer age question with an invalid value (e.g., “blue”).
- **Expected result:**
    - Bot explains it didn’t get a valid age, and re-asks with clear options (Under 30, 30–39, etc.).[^1]

***

## 18. Complex – Configuration, Admin, and Content Management

### TC-170: Update of coverage options via admin config

- **Goal:** Ensure changes to coverage presets propagate to the bot.
- **Steps:**

1. In admin panel, change coverage options from [100k, 250k, 500k, 1M+] to [150k, 300k, 600k, 1.2M+].
2. Start a new chat and reach coverage question.
- **Expected result:**
    - The updated set of coverage buttons is visible.


### TC-171: Toggle language availability from admin

- **Goal:** Confirm enabling/disabling Spanish works.
- **Steps:**

1. Disable Spanish in admin.
2. Start new chat.
- **Expected result:**
    - Only English is offered as language.
- **Steps (reverse):**
3. Re-enable Spanish.
4. Start new chat again.
- **Expected result:**
    - Both English and Spanish are available.[^1]


### TC-172: Turn AI lead scoring on/off

- **Goal:** Ensure system behaves reasonably without scoring.
- **Steps:**

1. Disable AI lead scoring in admin.
2. Complete a high-intent profile journey.
- **Expected result:**
    - No scoring fields appear in CRM, but lead still stored.
- **Steps (reverse):**
3. Re-enable scoring.
4. Repeat same journey.
- **Expected result:**
    - Lead is stored with appropriate score (e.g., 5 stars for homeowner + 250k coverage).[^1]

***

## 19. Complex – Performance and Reliability

### TC-180: Response time under normal load

- **Goal:** Verify acceptable bot response latency.
- **Steps:**

1. During off-peak usage, complete several conversations.
2. Measure average time between user message and bot reply.
- **Expected result:**
    - 95%+ of responses within defined SLA (e.g., ≤ 2 seconds).


### TC-181: Handling of rate limits or throttling

- **Goal:** Ensure system behaves well if backend APIs are rate-limited.
- **Steps:**

1. Simulate multiple chats in parallel (e.g., 20–50 concurrent sessions).
2. Observe any throttling/responses.
- **Expected result:**
    - Bot may slow slightly but continues functioning.
    - Clear error messages if temporarily unable to provide quotes or schedule.


### TC-182: Recovery after backend outage

- **Goal:** Verify bot recovers after an outage without manual intervention.
- **Steps:**

1. Simulate brief backend outage (e.g., pricing service down).
2. Attempt to get quotes during outage.
3. Restore service.
4. Start new chat.
- **Expected result:**
    - During outage: bot explains feature is temporarily unavailable.
    - After recovery: bot resumes full quoting and data flows.

***

## 20. Complex – Regression \& Versioning

### TC-190: Backward compatibility after content updates

- **Goal:** Ensure new scripts/questions don’t break existing flows.
- **Steps:**

1. Deploy new conversation content (e.g., updated objection scripts or “psychology-based triggers” that increase booking rate).[^1]
2. Run a previously passing regression scenario (e.g., TC-090).
- **Expected result:**
    - Core steps (qualification, quote, lead capture, booking) still function.
    - Only wording changes, not logic or integrations.


### TC-191: A/B test variation selection

- **Goal:** Validate that visitors are bucketed into correct variant (e.g., standard script vs. high-conversion script set).[^1]
- **Steps:**

1. Configure A/B test in admin (Variant A and Variant B scripts).
2. Start multiple new chats in incognito sessions.
- **Expected result:**
    - Users are randomly assigned to A or B per configuration.
    - Analytics includes variant in event payloads.


### TC-192: Rollback of a faulty version

- **Goal:** Confirm quick rollback if new bot version misbehaves.
- **Steps:**

1. Simulate a buggy content or logic deploy (e.g., quote step failing).
2. Use admin/tools to roll back to last stable version.
3. Start a new chat.
- **Expected result:**
    - The previously stable flow returns.
    - No residual errors from the buggy version.

***

## 21. Advanced – Multi-Product and Cross-Sell Logic

### TC-200: Cross-sell from mortgage protection to life insurance

- **Goal:** Ensure bot can recommend related products without being pushy.
- **Steps:**

1. Complete mortgage protection qualification.
2. At end, indicate interest in broader family coverage.
- **Expected result:**
    - Bot briefly suggests life insurance options and offers to connect to an agent or schedule call.[^1]


### TC-201: Avoid irrelevant cross-sell

- **Goal:** Confirm bot does not cross-sell unrelated products.
- **Steps:**

1. Declare strong interest only in mortgage protection.
2. Decline extra products when asked.
- **Expected result:**
    - Bot respects the choice and does not repeatedly push business insurance or other irrelevant lines.[^1]

***

If you want, I can also:

- Package all these new test cases into an updated markdown file (v2) that includes both the original suite and these extra sections, or
- Help you convert this into a format that matches your QA tooling (e.g., CSV for test management, JSON, or Gherkin scenarios).

<div align="center">⁂</div>

[^1]: CHATBOT-SUGGESTIONS-INTERMARQ-AGENCY-1.docx

