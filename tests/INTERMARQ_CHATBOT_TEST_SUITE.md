# 🧪 Intermarq Agency — Insurance Chatbot Test Suite

> **Version:** 1.0  
> **Coverage:** Lead Qualification · Quote Engine · Appointment Booking · Lead Capture · Objection Handling · Multilingual · AI Scoring · Integrations  
> **Levels:** Easy → Medium → Hard → Complex

---

## 📋 Table of Contents

1. [Test Conventions](#test-conventions)
2. [🟢 Easy — Core UI & Basic Flow](#-easy--core-ui--basic-flow)
3. [🟡 Medium — Logic, Validation & Routing](#-medium--logic-validation--routing)
4. [🔴 Hard — End-to-End Flows & Integrations](#-hard--end-to-end-flows--integrations)
5. [⚫ Complex — Edge Cases, AI Scoring & Stress](#-complex--edge-cases-ai-scoring--stress)
6. [📊 Test Summary Matrix](#-test-summary-matrix)

---

## Test Conventions

| Field | Description |
|---|---|
| **ID** | Unique test identifier (e.g., `E-001`) |
| **Given** | Precondition / initial state |
| **When** | Action performed |
| **Then** | Expected result |
| **Pass Criteria** | Specific, measurable outcome |
| **Fail Criteria** | What constitutes a failure |

**Test ID Prefixes:**

- `E-` Easy
- `M-` Medium
- `H-` Hard
- `C-` Complex

---

## 🟢 Easy — Core UI & Basic Flow

> These tests verify that the chatbot renders correctly, buttons are clickable, and the opening flow functions as documented.

---

### E-001 — Chatbot Widget Loads on Page

| | |
|---|---|
| **Given** | A visitor opens the Intermarq agency website |
| **When** | The page fully loads |
| **Then** | The chatbot widget is visible on the page |
| **Pass Criteria** | Chat bubble/widget appears within 3 seconds of page load |
| **Fail Criteria** | Widget is missing, hidden, or takes >5 seconds to appear |

---

### E-002 — Opening Greeting Message Displays

| | |
|---|---|
| **Given** | The chatbot widget is loaded |
| **When** | User clicks to open the chat |
| **Then** | Bot shows the conversion-boosting opener |
| **Pass Criteria** | Message reads: *"Most homeowners can qualify for mortgage protection coverage in under 2 minutes."* |
| **Fail Criteria** | No message appears, or message is blank/incorrect |

---

### E-003 — Coverage Type Question Appears

| | |
|---|---|
| **Given** | User opens the chat |
| **When** | The greeting message is displayed |
| **Then** | Bot asks: *"What would you like to protect today?"* with 5 option buttons |
| **Pass Criteria** | All 5 buttons render: `My Mortgage`, `My Family`, `Final Expenses`, `Business Protection`, `Just exploring` |
| **Fail Criteria** | Fewer than 5 buttons appear, or button labels are wrong |

---

### E-004 — Each Coverage Button Is Clickable

| | |
|---|---|
| **Given** | The coverage type question is displayed |
| **When** | User clicks each button one at a time (in separate sessions) |
| **Then** | Each click registers and the bot advances to the next question |
| **Pass Criteria** | All 5 buttons respond; no button is disabled or unresponsive |
| **Fail Criteria** | Any button does not trigger a bot response |

---

### E-005 — Age Range Question Displays Correct Buttons

| | |
|---|---|
| **Given** | User selects any coverage type |
| **When** | Bot reaches the age range question |
| **Then** | Bot asks: *"Which age range do you fall into?"* with 5 buttons |
| **Pass Criteria** | Buttons: `Under 30`, `30-39`, `40-49`, `50-59`, `60+` — all present |
| **Fail Criteria** | Missing buttons or incorrect age ranges displayed |

---

### E-006 — Tobacco Use Question Displays Correct Buttons

| | |
|---|---|
| **Given** | User has answered age range |
| **When** | Bot reaches tobacco question |
| **Then** | Bot asks: *"Do you currently use tobacco products?"* |
| **Pass Criteria** | Buttons: `Yes`, `No`, `Occasionally` — all present and clickable |
| **Fail Criteria** | Missing any button or wrong label |

---

### E-007 — Coverage Amount Question Displays

| | |
|---|---|
| **Given** | User progresses through coverage type and age |
| **When** | Bot asks coverage amount |
| **Then** | Question and 5 buttons appear |
| **Pass Criteria** | Buttons: `$100,000`, `$250,000`, `$500,000`, `$1,000,000+`, `Not sure yet` |
| **Fail Criteria** | Wrong amounts or missing the "Not sure yet" fallback |

---

### E-008 — State of Residence Question Appears

| | |
|---|---|
| **Given** | User has answered coverage, age, and tobacco questions |
| **When** | Bot asks state of residence |
| **Then** | A state selection input (dropdown or text field) is displayed |
| **Pass Criteria** | User can enter or select a U.S. state; field accepts valid input |
| **Fail Criteria** | No input field appears, or field is disabled |

---

### E-009 — Homeowner Question Appears

| | |
|---|---|
| **Given** | User has answered all prior qualification questions |
| **When** | Bot reaches homeowner question |
| **Then** | Bot asks: *"Do you currently own a home with a mortgage?"* |
| **Pass Criteria** | Buttons: `Yes`, `No`, `Planning to buy` — all present |
| **Fail Criteria** | Question skipped or buttons missing |

---

### E-010 — Lead Capture Fields Render

| | |
|---|---|
| **Given** | User completes all qualification questions |
| **When** | Bot reaches lead capture step |
| **Then** | Bot displays message and shows input fields |
| **Pass Criteria** | Fields for `Name`, `Email`, `Phone`, `Zip Code` all present and editable |
| **Fail Criteria** | Any field is missing or non-editable |

---

## 🟡 Medium — Logic, Validation & Routing

> These tests verify business logic: quote accuracy, objection responses, routing by state, and input validation.

---

### M-001 — Qualified Licensed State Triggers Positive Response

| | |
|---|---|
| **Given** | User is filling out the state question |
| **When** | User selects or enters `California` |
| **Then** | Bot responds positively confirming service availability |
| **Pass Criteria** | Bot responds: *"Great, we currently serve residents of California."* or equivalent confirmation |
| **Fail Criteria** | Bot gives a rejection message or no response for a licensed state |

---

### M-002 — Unlicensed State Triggers Graceful Fallback

| | |
|---|---|
| **Given** | User enters a state where the agency is NOT licensed |
| **When** | Bot checks state against licensed-state list |
| **Then** | Bot informs user they cannot currently be served in that state |
| **Pass Criteria** | Polite message with no lead capture attempted for unlicensed states; no error thrown |
| **Fail Criteria** | Bot still collects lead data for an unlicensed state, or crashes |

---

### M-003 — Non-Smoker Quote Range (35-Year-Old, $250k)

| | |
|---|---|
| **Given** | User selects: Age `30-39`, Tobacco `No`, Coverage `$250,000` |
| **When** | Bot generates an estimated price range |
| **Then** | Bot returns the expected quote range |
| **Pass Criteria** | Bot message includes: *"A healthy 35-year-old non-smoker seeking $250,000 in mortgage protection coverage may pay between $30–$45/month."* or a figure within this documented range |
| **Fail Criteria** | Quote is wildly outside the documented range, or no quote is generated |

---

### M-004 — Smoker Quote is Higher Than Non-Smoker Quote

| | |
|---|---|
| **Given** | Two sessions, identical inputs (Age `30-39`, Coverage `$250,000`), differing only in tobacco use |
| **When** | Session A selects `No` and Session B selects `Yes` for tobacco |
| **Then** | Session B (smoker) receives a higher estimated premium |
| **Pass Criteria** | Smoker quote minimum ≥ non-smoker quote maximum |
| **Fail Criteria** | Smoker and non-smoker quotes are identical, or smoker quote is lower |

---

### M-005 — "I Already Have Life Insurance" Objection Response

| | |
|---|---|
| **Given** | The bot is in conversation and user types the objection |
| **When** | User sends: *"I already have life insurance."* |
| **Then** | Bot responds with the documented reframe |
| **Pass Criteria** | Bot replies with message about keeping a separate mortgage-specific policy so the family keeps the house |
| **Fail Criteria** | Bot gives a generic fallback, error message, or no response |

---

### M-006 — "I'm Just Looking" Objection Response

| | |
|---|---|
| **Given** | User expresses low buying intent |
| **When** | User sends: *"I'm just looking."* |
| **Then** | Bot softly re-engages with the quick estimate offer |
| **Pass Criteria** | Bot responds: *"No problem. Would you like a quick estimate while you're here?"* or equivalent |
| **Fail Criteria** | Bot ends conversation, gives an unrelated response, or ignores the input |

---

### M-007 — Off-Hours Offline Message Appears

| | |
|---|---|
| **Given** | All agents are offline (outside business hours) |
| **When** | A new visitor opens the chatbot |
| **Then** | Bot informs the user agents are offline but still offers to help |
| **Pass Criteria** | Bot says: *"Our agents may be offline, but I can help you get a quote started."* |
| **Fail Criteria** | Bot shows an error, is disabled, or gives no message |

---

### M-008 — Email Field Rejects Invalid Format

| | |
|---|---|
| **Given** | User is on the lead capture step |
| **When** | User enters an invalid email (e.g., `notanemail`, `test@`, `@domain.com`) |
| **Then** | Bot or form validation flags the error |
| **Pass Criteria** | Inline validation message shown; form does not submit; user is prompted to correct email |
| **Fail Criteria** | Invalid email is accepted and lead is submitted |

---

### M-009 — Phone Field Rejects Non-Numeric / Short Input

| | |
|---|---|
| **Given** | User is on the lead capture step |
| **When** | User enters `123` or `abcdefghij` in phone field |
| **Then** | Validation rejects the input |
| **Pass Criteria** | User sees an error and cannot submit until a valid 10-digit US phone number is entered |
| **Fail Criteria** | Invalid phone number is accepted and submitted to CRM |

---

### M-010 — Zip Code Field Validation

| | |
|---|---|
| **Given** | User is filling the lead capture form |
| **When** | User enters a non-5-digit value (e.g., `9999`, `HELLO`, `123456`) |
| **Then** | Form rejects the input |
| **Pass Criteria** | Validation error shown; submit blocked until valid 5-digit zip is entered |
| **Fail Criteria** | Invalid zip is accepted |

---

### M-011 — "Not Sure Yet" Coverage Amount Routes Correctly

| | |
|---|---|
| **Given** | User reaches the coverage amount question |
| **When** | User selects `Not sure yet` |
| **Then** | Bot does not drop the user; it continues the flow with educational messaging |
| **Pass Criteria** | Bot acknowledges uncertainty, provides helpful guidance, and continues to lead capture |
| **Fail Criteria** | Bot loops, crashes, or ends the conversation |

---

### M-012 — "Just Exploring" Intent Routes Correctly

| | |
|---|---|
| **Given** | User selects `Just exploring` on the first question |
| **When** | Bot receives this low-intent signal |
| **Then** | Bot continues engagement rather than ending the flow |
| **Pass Criteria** | Bot provides educational content (e.g., mortgage protection explainer) and re-offers quote |
| **Fail Criteria** | Bot ends conversation or skips to lead capture without engaging |

---

### M-013 — Mortgage Protection Education Content Accuracy

| | |
|---|---|
| **Given** | User indicates interest in learning about mortgage protection |
| **When** | Bot delivers the education block |
| **Then** | Bot explains what mortgage protection is, how it pays off the house, and difference from term life |
| **Pass Criteria** | All 3 educational points are covered in the response |
| **Fail Criteria** | Any of the 3 key points is missing |

---

### M-014 — Language Toggle: Spanish Mode Activates

| | |
|---|---|
| **Given** | Bot supports multilingual mode (English + Spanish) |
| **When** | User selects Spanish or sends a Spanish-language message |
| **Then** | Bot switches all responses to Spanish |
| **Pass Criteria** | All subsequent bot messages are in correct Spanish; no English fallback shown |
| **Fail Criteria** | Bot remains in English, partially translates, or returns an error |

---

### M-015 — Language Toggle: English Mode Restores

| | |
|---|---|
| **Given** | User is in Spanish mode |
| **When** | User switches back to English |
| **Then** | Bot immediately resumes English responses |
| **Pass Criteria** | All messages from that point are in English |
| **Fail Criteria** | Bot continues in Spanish after English selection |

---

## 🔴 Hard — End-to-End Flows & Integrations

> These tests verify complete user journeys, CRM delivery, and calendar booking integrations.

---

### H-001 — Full Qualification → Quote → Lead Capture Flow

| | |
|---|---|
| **Given** | A new visitor opens the chatbot |
| **When** | User completes all 7 qualification questions + submits lead capture form |
| **Then** | All data is captured and a confirmation is shown |
| **Pass Criteria** | (1) All questions are answered in order; (2) Quote range is shown; (3) Lead form submitted successfully; (4) Confirmation message appears |
| **Fail Criteria** | Flow breaks at any step, data is not submitted, or confirmation is missing |

**Test Data:**

```
Coverage Type:    My Mortgage
Coverage Amount:  $250,000
Age Range:        30-39
Tobacco:          No
State:            California
Homeowner:        Yes
Name:             Test User
Email:            testuser@example.com
Phone:            5559876543
Zip Code:         90210
```

---

### H-002 — Lead Data Delivered to CRM

| | |
|---|---|
| **Given** | User completes the lead capture form |
| **When** | Form is submitted successfully |
| **Then** | Lead record appears in the connected CRM within 60 seconds |
| **Pass Criteria** | CRM record contains correct: Name, Email, Phone, Zip Code, coverage selections, and timestamp |
| **Fail Criteria** | CRM record is missing, incomplete, or delayed beyond 60 seconds |

---

### H-003 — Lead Triggers Email Notification to Agent

| | |
|---|---|
| **Given** | User submits lead capture form |
| **When** | Lead is processed |
| **Then** | Agent receives an email notification |
| **Pass Criteria** | Email is received within 2 minutes; includes lead name, phone, and coverage interest |
| **Fail Criteria** | Email not received, arrives after 5+ minutes, or contains wrong data |

---

### H-004 — Lead Triggers SMS/Text Notification to Agent

| | |
|---|---|
| **Given** | User submits lead capture form |
| **When** | Lead is processed |
| **Then** | Agent receives a text notification |
| **Pass Criteria** | SMS received within 2 minutes; includes at minimum lead name and phone number |
| **Fail Criteria** | SMS not received, or text contains incorrect lead details |

---

### H-005 — Appointment Booking via Calendly Integration

| | |
|---|---|
| **Given** | User completes lead capture and is prompted to book a consultation |
| **When** | User clicks *"Yes"* to schedule a call |
| **Then** | Calendly widget or redirect opens with available time slots |
| **Pass Criteria** | Calendly loads without error; user can select a time slot and confirm; booking appears in Calendly calendar |
| **Fail Criteria** | Calendly fails to load, shows no slots, or booking is not confirmed |

---

### H-006 — Appointment Booking via Google Calendar Integration

| | |
|---|---|
| **Given** | Google Calendar is configured as the booking integration |
| **When** | User books a consultation through the chatbot |
| **Then** | Event is created on the agent's Google Calendar |
| **Pass Criteria** | Calendar event created with: correct time, user name, phone number; confirmation sent to user's email |
| **Fail Criteria** | Event not created, wrong time saved, or user receives no confirmation |

---

### H-007 — High-Score Lead ($250k, Homeowner) Receives Priority Routing

| | |
|---|---|
| **Given** | AI lead scoring is active |
| **When** | User selects `My Mortgage`, `$250,000`, homeowner `Yes` |
| **Then** | Lead is scored 5-stars and routed to priority queue in CRM |
| **Pass Criteria** | CRM record shows 5-star score; lead appears at top of agent's priority queue |
| **Fail Criteria** | Correct lead type receives low score, or scoring is not applied |

---

### H-008 — Low-Score Lead (Renter, Just Exploring) Is Scored Correctly

| | |
|---|---|
| **Given** | AI lead scoring is active |
| **When** | User selects `Just exploring`, homeowner `No`, `Not sure yet` on coverage |
| **Then** | Lead is assigned a low score (2-star) |
| **Pass Criteria** | CRM record shows ≤2 stars; lead is placed below high-score leads in queue |
| **Fail Criteria** | Renter/exploring lead incorrectly assigned 4-5 stars |

---

### H-009 — Agent License Verification Message Displays

| | |
|---|---|
| **Given** | User expresses hesitation about the agency's credentials |
| **When** | Bot is triggered to show trust-building content |
| **Then** | Bot responds with the NIPR license verification message |
| **Pass Criteria** | Bot says: *"Our agents are licensed and registered through the National Insurance Producer Registry."* |
| **Fail Criteria** | Message is absent, inaccurate, or not triggered appropriately |

---

### H-010 — Complete Spanish-Language Lead Capture Flow

| | |
|---|---|
| **Given** | User switches to Spanish at the start of the chat |
| **When** | User completes the entire qualification and lead capture flow in Spanish |
| **Then** | Lead is submitted and all CRM data is correctly stored |
| **Pass Criteria** | (1) All bot messages are in Spanish throughout; (2) Lead data is stored in English in CRM (translated correctly); (3) Confirmation message is in Spanish |
| **Fail Criteria** | Any English fallback shown mid-flow; CRM data is garbled; lead is not submitted |

---

### H-011 — Chatbot Collects Leads While Agents Are Offline

| | |
|---|---|
| **Given** | All agents are offline (after-hours simulation) |
| **When** | A visitor completes the full qualification + lead capture flow |
| **Then** | Lead is successfully stored and agent is notified at next login or via notification |
| **Pass Criteria** | Lead appears in CRM with `offline` flag; agent receives delayed email/SMS notification |
| **Fail Criteria** | Lead is lost, chat is disabled after hours, or no notification is sent |

---

### H-012 — Returning User Context Retention

| | |
|---|---|
| **Given** | A user has previously interacted with the chatbot and submitted a lead |
| **When** | The same user reopens the chatbot on a return visit |
| **Then** | Bot either (a) recognizes returning user and skips re-qualification, or (b) clearly starts fresh without duplication |
| **Pass Criteria** | No duplicate lead records created; UX is smooth for returning visitor |
| **Fail Criteria** | Duplicate CRM records created; or user forced through entire flow again creating data conflicts |

---

## ⚫ Complex — Edge Cases, AI Scoring & Stress

> These tests probe system limits, data integrity under load, adversarial inputs, and scoring model accuracy.

---

### C-001 — XSS Injection in Name Field

| | |
|---|---|
| **Given** | User is on the lead capture form |
| **When** | User enters `<script>alert('XSS')</script>` in the Name field and submits |
| **Then** | Input is sanitized; no script executes |
| **Pass Criteria** | (1) No alert box fires; (2) CRM stores the sanitized/escaped text; (3) Bot continues normally |
| **Fail Criteria** | Script executes in browser, or raw HTML is stored in CRM |

---

### C-002 — SQL Injection in Email Field

| | |
|---|---|
| **Given** | User reaches the lead capture form |
| **When** | User submits `'; DROP TABLE leads;--` as the email address |
| **Then** | Input is rejected by validation before reaching the database |
| **Pass Criteria** | (1) Field validation rejects the input with format error; (2) No database operation is performed; (3) Error logged server-side |
| **Fail Criteria** | Input passes validation or reaches the backend unescaped |

---

### C-003 — Extremely Long Input in Name Field

| | |
|---|---|
| **Given** | User is on the lead capture form |
| **When** | User enters a string of 10,000 characters in the Name field |
| **Then** | System gracefully handles the overflow |
| **Pass Criteria** | Field either truncates to max character limit (e.g., 255) or displays an inline error; UI does not crash or freeze |
| **Fail Criteria** | Page hangs, throws a 500 error, or stores 10,000 characters unchecked |

---

### C-004 — Rapid Button Clicking (Double-Submit Prevention)

| | |
|---|---|
| **Given** | User is on any step with a button |
| **When** | User rapidly clicks the same button 5+ times in under 1 second |
| **Then** | Bot processes only one click; flow advances once |
| **Pass Criteria** | (1) No duplicate question steps; (2) No duplicate lead records; (3) Bot does not skip steps |
| **Fail Criteria** | Bot skips multiple steps, submits the lead form multiple times, or creates duplicate CRM entries |

---

### C-005 — Concurrent Session Isolation (Two Simultaneous Users)

| | |
|---|---|
| **Given** | Two different users open the chatbot at the exact same time on separate browsers |
| **When** | Each user makes different selections (User A = homeowner, User B = renter) |
| **Then** | Each session is completely isolated |
| **Pass Criteria** | (1) User A's and User B's data never mix; (2) Two separate CRM records are created with correct data; (3) No data bleed between sessions |
| **Fail Criteria** | Data from one session appears in the other; only one CRM record created; or sessions interfere |

---

### C-006 — AI Lead Scoring: Age 50+ Mortgage Protection = 4 Stars

| | |
|---|---|
| **Given** | AI scoring engine is active |
| **When** | User inputs: Age `50-59`, Coverage `My Mortgage`, `$250,000`, Homeowner `Yes` |
| **Then** | Lead is assigned a 4-star score |
| **Pass Criteria** | CRM score = ⭐⭐⭐⭐ for this profile; score persists after page refresh |
| **Fail Criteria** | Score is 3 or below, or 5 stars (over-scored); score not stored in CRM |

---

### C-007 — AI Lead Scoring: All 3 Documented Profiles Score Correctly

| | |
|---|---|
| **Given** | AI scoring is active |
| **When** | Three leads are submitted matching each documented profile |
| **Then** | Each lead matches its expected score |

| Profile | Expected Score |
|---|---|
| Homeowner + $250k coverage | ⭐⭐⭐⭐⭐ |
| Renter + exploring | ⭐⭐ |
| Age 50+ mortgage protection | ⭐⭐⭐⭐ |

| **Pass Criteria** | All 3 CRM records show the exact expected scores |
| **Fail Criteria** | Any profile receives a score that differs from documented expected value |

---

### C-008 — Bot Handles Unsupported Free-Text Input Gracefully

| | |
|---|---|
| **Given** | Bot is in a button-only step |
| **When** | User types completely random text (e.g., *"purple elephant"*, *"asdfghjkl"*) |
| **Then** | Bot acknowledges the unexpected input and guides user back to the flow |
| **Pass Criteria** | Bot returns a fallback/clarification message and re-presents the current step's options |
| **Fail Criteria** | Bot crashes, freezes, shows a blank message, or skips to next step |

---

### C-009 — Calendly Webhook Failure → Graceful Degradation

| | |
|---|---|
| **Given** | Calendly API/webhook is temporarily unavailable (simulated timeout) |
| **When** | User attempts to book an appointment |
| **Then** | Bot handles the failure gracefully |
| **Pass Criteria** | Bot informs user of the booking issue and offers an alternative (e.g., *"Our agent will reach out to schedule"*); lead is still saved to CRM |
| **Fail Criteria** | Bot shows a raw API error, white-screens, or loses the lead |

---

### C-010 — CRM Webhook Failure → Lead Not Lost

| | |
|---|---|
| **Given** | CRM API is temporarily unavailable |
| **When** | User submits the lead capture form |
| **Then** | Lead data is not lost |
| **Pass Criteria** | (1) Lead is queued locally or in a retry buffer; (2) Retry succeeds when CRM recovers; (3) User sees a success confirmation (not an error) |
| **Fail Criteria** | Lead is silently dropped; user sees an error; no retry mechanism exists |

---

### C-011 — 100 Simultaneous Sessions (Load Test)

| | |
|---|---|
| **Given** | The chatbot is deployed in production |
| **When** | 100 concurrent users simultaneously go through the full qualification flow |
| **Then** | All sessions complete without degradation |
| **Pass Criteria** | (1) Response time per bot message ≤ 2 seconds under load; (2) All 100 leads are created in CRM; (3) No sessions crash or time out |
| **Fail Criteria** | Response times exceed 5 seconds; fewer than 95 leads are recorded; any session crashes |

---

### C-012 — Spanish + Objection Handling Combo

| | |
|---|---|
| **Given** | User switches to Spanish mode early in the conversation |
| **When** | User sends the objection *"Ya tengo seguro de vida"* ("I already have life insurance") |
| **Then** | Bot responds in Spanish with the correct objection-handling message |
| **Pass Criteria** | Bot responds in Spanish with the mortgage-specific policy reframe (translated correctly, not garbled) |
| **Fail Criteria** | Bot responds in English, gives a generic reply, or fails to handle the Spanish objection |

---

### C-013 — Lead Score Updates on Re-Submission (Same Contact)

| | |
|---|---|
| **Given** | A contact previously submitted as a low-score renter (⭐⭐) |
| **When** | The same email returns and now selects homeowner + $250k coverage |
| **Then** | CRM updates the contact's score to ⭐⭐⭐⭐⭐ without creating a duplicate |
| **Pass Criteria** | (1) No duplicate CRM record; (2) Score updated to 5 stars; (3) Previous session data preserved in history |
| **Fail Criteria** | Duplicate record created; score not updated; original data overwritten without history |

---

### C-014 — Bot Handles Emoji-Only Input

| | |
|---|---|
| **Given** | User is in a free-text input step |
| **When** | User sends only emojis: `🏠💰✅` |
| **Then** | Bot handles gracefully |
| **Pass Criteria** | Bot does not crash; returns a friendly fallback guiding user back to the flow |
| **Fail Criteria** | Crash, blank response, or encoding error in CRM |

---

### C-015 — Full Flow Regression: All 7 Questions in Correct Order

| | |
|---|---|
| **Given** | A new session is started |
| **When** | Bot runs through the complete qualification flow |
| **Then** | Questions appear in the documented order |

**Expected Question Order:**

```
1. What would you like to protect today?          (Coverage Type)
2. How much coverage are you considering?         (Coverage Amount)
3. Which age range do you fall into?              (Age Range)
4. Do you currently use tobacco products?         (Tobacco Use)
5. What state do you live in?                     (State)
6. Do you currently own a home with a mortgage?   (Homeowner)
7. Lead Capture: Name / Email / Phone / Zip       (Lead Close)
```

| **Pass Criteria** | All 7 questions appear in this exact order; no question is skipped or duplicated |
| **Fail Criteria** | Any question is out of order, missing, or repeated |

---

## 📊 Test Summary Matrix

| ID | Description | Level | Category | Priority |
|---|---|---|---|---|
| E-001 | Widget loads on page | 🟢 Easy | UI | P1 |
| E-002 | Opening greeting displays | 🟢 Easy | UI | P1 |
| E-003 | Coverage type question & buttons | 🟢 Easy | UI | P1 |
| E-004 | Each coverage button is clickable | 🟢 Easy | UI | P1 |
| E-005 | Age range buttons correct | 🟢 Easy | UI | P1 |
| E-006 | Tobacco use buttons correct | 🟢 Easy | UI | P1 |
| E-007 | Coverage amount buttons correct | 🟢 Easy | UI | P1 |
| E-008 | State of residence input works | 🟢 Easy | UI | P1 |
| E-009 | Homeowner question buttons correct | 🟢 Easy | UI | P1 |
| E-010 | Lead capture fields render | 🟢 Easy | UI | P1 |
| M-001 | Licensed state positive response | 🟡 Medium | Logic | P1 |
| M-002 | Unlicensed state graceful fallback | 🟡 Medium | Logic | P1 |
| M-003 | Non-smoker quote range accuracy | 🟡 Medium | Quote Engine | P1 |
| M-004 | Smoker quote higher than non-smoker | 🟡 Medium | Quote Engine | P1 |
| M-005 | Objection: already have insurance | 🟡 Medium | Objections | P2 |
| M-006 | Objection: just looking | 🟡 Medium | Objections | P2 |
| M-007 | Off-hours offline message | 🟡 Medium | Logic | P2 |
| M-008 | Email validation rejects invalid format | 🟡 Medium | Validation | P1 |
| M-009 | Phone validation rejects short/alpha | 🟡 Medium | Validation | P1 |
| M-010 | Zip code validation | 🟡 Medium | Validation | P1 |
| M-011 | "Not sure yet" routes correctly | 🟡 Medium | Routing | P2 |
| M-012 | "Just exploring" routes correctly | 🟡 Medium | Routing | P2 |
| M-013 | Mortgage protection education content | 🟡 Medium | Content | P2 |
| M-014 | Spanish mode activates | 🟡 Medium | Multilingual | P1 |
| M-015 | English mode restores | 🟡 Medium | Multilingual | P1 |
| H-001 | Full qualification → quote → capture | 🔴 Hard | E2E Flow | P1 |
| H-002 | Lead data delivered to CRM | 🔴 Hard | Integration | P1 |
| H-003 | Email notification to agent | 🔴 Hard | Integration | P1 |
| H-004 | SMS notification to agent | 🔴 Hard | Integration | P1 |
| H-005 | Calendly booking integration | 🔴 Hard | Integration | P1 |
| H-006 | Google Calendar booking integration | 🔴 Hard | Integration | P1 |
| H-007 | High-score lead priority routing | 🔴 Hard | AI Scoring | P2 |
| H-008 | Low-score lead scored correctly | 🔴 Hard | AI Scoring | P2 |
| H-009 | License verification message | 🔴 Hard | Trust/Content | P3 |
| H-010 | Spanish full lead capture flow | 🔴 Hard | Multilingual E2E | P2 |
| H-011 | Lead capture while offline | 🔴 Hard | E2E Flow | P1 |
| H-012 | Returning user context retention | 🔴 Hard | Data Integrity | P2 |
| C-001 | XSS injection in name field | ⚫ Complex | Security | P1 |
| C-002 | SQL injection in email field | ⚫ Complex | Security | P1 |
| C-003 | Extremely long input (10k chars) | ⚫ Complex | Edge Case | P2 |
| C-004 | Rapid clicking / double-submit | ⚫ Complex | Edge Case | P1 |
| C-005 | Concurrent session isolation | ⚫ Complex | Data Integrity | P1 |
| C-006 | AI scoring: Age 50+ = 4 stars | ⚫ Complex | AI Scoring | P2 |
| C-007 | All 3 scoring profiles correct | ⚫ Complex | AI Scoring | P1 |
| C-008 | Unsupported free-text graceful handling | ⚫ Complex | Edge Case | P2 |
| C-009 | Calendly webhook failure degradation | ⚫ Complex | Resilience | P2 |
| C-010 | CRM webhook failure → lead not lost | ⚫ Complex | Resilience | P1 |
| C-011 | 100 concurrent sessions load test | ⚫ Complex | Performance | P2 |
| C-012 | Spanish + objection handling combo | ⚫ Complex | Multilingual | P2 |
| C-013 | Lead score updates on re-submission | ⚫ Complex | Data Integrity | P2 |
| C-014 | Emoji-only input handled gracefully | ⚫ Complex | Edge Case | P3 |
| C-015 | Full flow regression: correct order | ⚫ Complex | Regression | P1 |

---

**Total Tests: 50**

| Level | Count |
|---|---|
| 🟢 Easy | 10 |
| 🟡 Medium | 15 |
| 🔴 Hard | 12 |
| ⚫ Complex | 13 |

| Priority | Count |
|---|---|
| P1 (Critical) | 30 |
| P2 (Important) | 17 |
| P3 (Nice to Have) | 3 |

---

*Generated for Intermarq Agency Chatbot Solution — Test Suite v1.0*
