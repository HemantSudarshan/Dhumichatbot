 Generation Prompt: Intermarq Insurance Assistant

---

## Project Overview & Visual Identity
I need a modern, high-converting React web application for a California-based insurance agency (Intermarq). The application is an interactive form and chatbot that guides users through a 7-step qualification process for Mortgage Protection, Term Life, and Final Expense insurance. 

**IMPORTANT: I have uploaded the company logo image. You MUST use this image prominently in the header/UI.**

The design must perfectly match this exact brand identity. It should feel premium, regal, and highly professional.

### Color Palette
*   **Background:** Solid Black (`#000000`). This provides a high-contrast canvas that makes the other elements pop.
*   **Primary Text:** Pure White (`#FFFFFF`). Used for the company name, entity type, website, and phone labels ("Business", "Office").
*   **Accent Color:** Gold / Dark Yellow (`#D4AF37` or similar metallic gradient, flat mustard gold for text). Used for the logo and the services/phone numbers. 

### Typography
*   **Font Style:** You MUST use an elegant, classic Serif font for the entire graphic (e.g., `Playfair Display`, `Cinzel`, `Garamond`, or `Merriweather`).
*   **Main Title:** "INTERMARQ" must be in all caps, high contrast between thick and thin strokes. Emulate a distinct, elongated swooping tail on the letter "Q" if the web font supports it or via SVG.
*   **Subtitles & Services:** All caps, smaller point size. (Text: "INSURANCE AGENCY LLC" and "LIFE WHOLE TERM ANNUITY FINAL EXPENSE")
*   **Contact Info:** Top Header should include the logo, then "Business: 888-213-3537 | Office: 323-475-6955".
*   **Website URL:** Lowercase, traditional readable serif (`intermarqinsuranceagency.com`).

### Structure & Layout
*   Center the majestic Lion Crest Logo (from the uploaded image) at the very top.
*   Below the logo, the main title "INTERMARQ"
*   Below that, "INSURANCE AGENCY LLC"
*   Below that, the services list: "LIFE • WHOLE • TERM • ANNUITY • FINAL EXPENSE"
*   Implement modern UI patterns focused on **Heavy Glassmorphism**: deep, frosted glass panels over the solid black background with very subtle, glowing gold borders. The UI should look bespoke and highly customized, NOT like a generic, robotic template.
*   **No Emojis:** Do not include useless emojis like thumbs up/down feedback buttons or smiley faces in the design.
*   Use `shadcn/ui` dark mode variants, but heavily customized to be transparent/glassy with the gold accent color.

## The 7-Step State Machine Flow
The UI is a stepped chat interface. The user interacts via buttons for steps 1-4 and 6. The free-text input box must be disabled and grayed out until explicitly allowed.

*   **Step 1: Intent Selection**
    *   Prompt: "What brings you to Intermarq today?"
    *   Buttons: "My Mortgage", "Term Life", "Final Expenses", "Just exploring"
*   **Step 2: Coverage Amount**
    *   Prompt: "How much coverage are you looking for?"
    *   Buttons: "$100,000", "$250,000", "$500,000", "$1M+"
*   **Step 3: Age Range**
    *   Prompt: "What is your current age?"
    *   Buttons: "18-29", "30-39", "40-49", "50-59", "60+"
*   **Step 4: Tobacco Use**
    *   Prompt: "Have you used tobacco or nicotine products in the last 12 months?"
    *   Buttons: "Yes", "No"
*   **Step 5: State Verification (Text Input Allowed)**
    *   Prompt: "What state do you live in? (we presently serve in California)"
    *   *Constraint:* Enable the chat input box. The user must type their state. If the input fuzzy matches "CA" or "California", proceed to Step 6. If not, show an error message: "We currently only write policies for California residents." and halt the flow.
*   **Step 6: Dynamic Pricing Display**
    *   Prompt: "Great. Based on your profile, your estimated monthly premium is between **[LOW]** and **[HIGH]**. Does this fit your budget?"
    *   *Logic:* Base range is $30-$45. If Step 4 = "Yes" (Tobacco), multiply the base range by 1.5 ($45-$67). If Step 1 = "Just exploring", inject a loss aversion hook text before the pricing: "Locking in coverage today guarantees your rate before age or health changes."
    *   Buttons: "Yes, let's proceed", "This is too expensive"
*   **Step 7: Lead Capture (Form)**
    *   Prompt: "Please provide your details so a licensed agent can prepare your official quote."
    *   UI: Show a small embedded form in the chat with fields: Full Name, Email, Phone, Zip Code. Include a "Submit for Quote" button.
    *   *Pre-requisite:* Above the form, display a Trust Hook: "Our agents are licensed and registered through the National Insurance Producer Registry."

## Chatbot Mode (Post-Step 6)
If the user types a free-text question at any point during Steps 5, 6, or 7, send the question to the backend API (`/api/v1/chat`).
*   **3-Chat Limiter:** The user can freely send maximum 3 free-text messages to the LLM. Track this in state.
*   **Enforcement:** After the 3rd API response, render an inline Calendly widget with the message: "You've used your free questions. Schedule a 10-minute call with a licensed agent to get all your questions answered — no commitment required!". The ONLY button should be "📅 Schedule 10-min Call". Do NOT offer a "Chat More" bypass here. The input box must remain permanently locked.

## Integration Requirements

### 1. Calendly Integration
Whenever an offline fallback is triggered (e.g., after 3 chats, or if the API returns `fallback: true`), render an inline Calendly popup. If triggering due to 3 chats, show message: "You've used your free questions. Schedule a 10-minute call with a licensed agent to get all your questions answered — no commitment required!". If triggered manually via "Talk to Human", allow them an option to "Chat More".
*   Use the standard Calendly embed script/component.
*   Target URL: `https://calendly.com/your-intermarq-link` (use a placeholder for now).

### 1a. Language Toggle (EN/ES)
Implement an EN/ES toggle switch in the UI header.
*   When clicked, show a `confirm()` dialog: "Switching language will restart the conversation. Do you want to continue?" (Show in the target language).
*   If confirmed, completely reset the app state: `step=0`, `chat_count=0`, clear message history, and reset the form. Zero state from the old language should bleed over. Ensure disclosures read from the translated source.

### 2. Backend API Connectivity
The frontend must connect to a FastAPI backend running on `http://localhost:8000`. Set this default but allow it to be overwritten by a `.env` variable (e.g., `VITE_API_BASE_URL`).

**Endpoints to implement:**

*   **POST `/api/v1/chat`**
    *   Request: `{ "question": "user text", "language": "en" }`
    *   Response: `{ "answer": "Markdown string", "sources": [], "fallback": boolean }`
    *   Display the `answer` in the chat window. Render markdown properly (lists, bolding). If `fallback` is true, trigger the Calendly popup.

*   **POST `/api/v1/lead`**
    *   Triggered when the Step 7 form is submitted.
    *   Payload mapping:
        *   `full_name`, `email`, `phone`, `zip_code` (from Step 7 form)
        *   `coverage_amount` (from Step 2)
        *   `age_range` (from Step 3)
        *   `tobacco_use` (from Step 4)
        *   `state` (from Step 5)
        *   `pricing_range` (calculated in Step 6)
    *   Response handling: If success, show a final celebration message: "Your official quote request has been secured. Transaction ID: [transaction_id]. An agent will contact you shortly."

### 3. Cloudflare Turnstile CAPTCHA (Placeholder)
Add a visual placeholder component for Cloudflare Turnstile right before the "Submit for Quote" button in Step 7. It should look like a standard "Verify you are human" checkbox.

## Component Architecture Preferences
*   `App.jsx`: Main routing/layout.
*   `ChatWindow.jsx`: The main container for the chat interface. Handles scrolling and message history.
*   `MessageBubble.jsx`: Component for individual messages (bot vs. user styling).
*   `ActionButtons.jsx`: Reusable component for the choice buttons in Steps 1-4.
*   `LeadForm.jsx`: The final form component.
*   Use React Context or Zustand for the state machine (current step, collected data, chat count).

Build the entire interface to be mobile-first and highly polished. Do not use dummy text (lorem ipsum); use the exact copywriting provided above.
