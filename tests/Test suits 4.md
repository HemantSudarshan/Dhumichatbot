**Simple:**  
**Question 1: The "Too Expensive" Objection**

*"I think this is too expensive for me right now."*

**Expected Answer / Behavior:** The chatbot must trigger the exact "Too expensive" objection handler from your `objections.json` file. It should reframe the cost by anchoring it to **$15/month** (less than a Netflix subscription).

**What it tests:** This validates your NLP trigger mapping for common sales pushback. By recognizing phrases related to cost, the bot successfully applies the agency's predefined psychological reframing rather than hallucinating financial advice.

---

**Question 2: The "Just Exploring" Flow** *Action: The user clicks the "Just exploring" button on Step 1 of the qualification flow.*

**Expected Answer / Behavior:** The bot must trigger the **Loss Aversion hook**. It should respond exactly with: *"No problem. Would you like a quick estimate while you're here?"*.

**What it tests:** This tests the conditional routing of your UI buttons. It ensures that low-intent leads (2-star profiles) are not turned away, but rather kept engaged with a low-pressure offer to receive an instant estimate.

---

**Question 3: Basic Product Education**

*"What is mortgage protection insurance and how does it pay off?"*

**Expected Answer / Behavior:** The bot retrieves the educational definition from `products.json` or `knowledge.json`. It must explain: *"Mortgage protection insurance ensures your family can stay in their home by paying off the remaining mortgage balance if something happens to you."*.

**What it tests:** This verifies your basic RAG retrieval capabilities for standard educational queries. It ensures the bot correctly explains the distinct purpose of mortgage protection versus standard term life insurance.

---

**Question 4: Out-of-State Fallback** *Action: The user types "Nevada" or "NV" when asked "What state do you live in?"*

**Expected Answer / Behavior:** The bot must reject the state and trigger the non-California fallback message: *"Great, we currently serve residents of California."*.

**What it tests:** This validates your geographic routing and fuzzy matching script. Because insurance licensing is strictly state-specific, the system must immediately identify that the agency is only licensed in California and halt the CA-specific compliance flow.

---

**Question 5: The "Already Covered" Objection**

*"I already have a life insurance policy through my employer."*

**Expected Answer / Behavior:** The bot must trigger the "Already have insurance" objection handler. It should respond with the specific mortgage reframe: *"Many homeowners keep a separate policy specifically to protect their mortgage so their family keeps the house."*.

**What it tests:** This tests the NLP engine's ability to handle the most common insurance objection. It proves the bot can strategically pivot the conversation to explain why a separate policy is necessary, keeping the user in the sales funnel.

---

**Question 6: The Trust Verification Hook** *Action: The user reaches Step 7 and is asked to provide their Phone and Email.*

**Expected Answer / Behavior:** Right before or as it asks for contact info, the bot must inject the **Trust Verification hook**: *"Our agents are licensed and registered through the National Insurance Producer Registry."*.

**What it tests:** This verifies that your UI successfully injects psychological trust-building scripts at the exact point of maximum friction (lead capture). This specific line is proven to increase conversion rates by reassuring users before they hand over PII.

---

**Question 7: The 3-Chat Limiter (Context Exhaustion Defense)** *Action: The user types their 3rd free-text question into the RAG input box.*

**Expected Answer / Behavior:** Upon hitting "Enter" for the 3rd time, the **text input box disables itself**. The bot then automatically injects the offline fallback hook: *"Our agents may be offline, but I can help you get a quote started. Would you like to schedule a quick 10-minute call with a licensed agent?"* alongside the inline Calendly widget.

**What it tests:** This tests your frontend JavaScript state machine (`let freeTextCount = 0`). It mathematically guarantees that the user cannot endlessly distract the LLM, forcing the conversation to convert into a booked appointment.

Medium: **Test 1: The Tobacco Pricing Multiplier** *Action / Input:* The user selects "30-39" for their age range, "$250,000" for coverage amount, and answers "Yes" to the tobacco use question. *Expected Answer / Behavior:* The chatbot dynamically calculates the base rate of $30–$45/month and mathematically applies the **1.5x tobacco multiplier** on the fly, updating the UI to display a final estimated range of **$45–$67.50/month**. *What it tests:* This validates your internal JavaScript math and pricing engine, ensuring that risk factors correctly adjust the quotes displayed to the user before they submit their lead.

**Test 2: Geographic Routing & State Validation** *Action / Input:* When asked "What state do you live in?", the user types an out-of-state input like "Texas" or "TX". *Expected Answer / Behavior:* The system must reject the input, halt the standard flow, and trigger the out-of-state fallback response: **"Great, we currently serve residents of California."**. *What it tests:* This tests the routing logic and fuzzy matching engine. Because insurance licensing is strictly state-specific, the bot must seamlessly filter out non-California traffic to ensure all captured leads are serviceable.

**Test 3: The High-Value Homeowner Lead Score** *Action / Input:* The user clicks "My Mortgage" for intent, "$250,000" for coverage, and "Yes" to the specific question: "Do you currently own a home with a mortgage?". *Expected Answer / Behavior:* The backend logic silently tags this specific user profile with a **⭐⭐⭐⭐⭐ (5-star) lead score** before routing the payload. *What it tests:* This validates your internal AI Lead Scoring engine. It ensures the mathematical logic accurately prioritizes homeowners seeking high coverage so your CRM can route them immediately to a live agent.

**Test 4: Intent & Cross-Selling Categorization** *Action / Input:* At the very first question ("What would you like to protect today?"), the user selects **"Final Expenses"** or **"My Family"** instead of "My Mortgage". *Expected Answer / Behavior:* The state machine must record the specific product intent without breaking the 7-step flow, ensuring the final output maps to the correct product definition from your `products.json` file. *What it tests:* This validates that your system can successfully handle multiple product types for cross-selling, ensuring the CRM knows exactly what type of policy the user wants to buy.

---

Hard: Here are 5 **Hard** test cases designed to evaluate your chatbot's ability to navigate California's most complex and nuanced insurance regulations, complete with the exact questions and the expected compliance behavior.

### **Test 1: The CIC 10509 Replacement & Loan Threshold Trap**

**Question:**

*"I have a whole life policy and I recently took out a loan against 30% of its value. I want to buy a new Indexed Universal Life (IUL) policy from you instead to replace it. How do we proceed?"*

**Expected Answer / Behavior:** The chatbot must recognize this scenario as a heavily regulated policy replacement. Under **California Insurance Code (CIC) Section 10509**, a replacement is legally triggered if a new policy is purchased while an existing policy is subjected to borrowing that exceeds **25% of its total loan value**. The bot must state that to proceed, the agent will need to submit a signed statement, provide a formal **"Notice Regarding Replacement,"** and generate a written comparison of the existing and proposed policies detailing premiums and cash values. It must then trigger the Calendly CTA to route this complex transaction to a human agent.

---

### **Test 2: The Senior "Free Look" & Variable Market Risk Trap**

**Question:**

*"I am 62 years old and bought a variable annuity 10 days ago. The market just crashed and my account lost 20% of its value. Because I am under the 30-day free look period, I demand a 100% full refund of my original premium."*

**Expected Answer / Behavior:** The chatbot must **refuse the 100% original premium refund**. While California grants seniors (aged 60 and older) a mandatory 30-day "free look" period for life insurance and annuities, there is a strict exception for **variable products**. If the funds were invested in the market during those 30 days, the senior assumes the short-term market risk, and the refund is limited to the **account value on the day the policy is returned**. The bot must accurately reflect this regulatory exception and defer to a licensed agent to process the adjusted refund.

---

### **Test 3: The Standard Nonforfeiture Law Test**

**Question:**

*"I've had my whole life insurance policy for 5 years but I just lost my job and can't pay my premiums anymore. Will I lose absolutely all the money I put into it?"*

**Expected Answer / Behavior:** The chatbot must reassure the user that they will not lose their entire investment, accurately citing the **Standard Nonforfeiture Law (CIC Section 10160\)**. It should explain that because the policy has been in force for over three years, they are legally entitled to a nonforfeiture benefit. The bot should list their three options: taking a lump-sum **Cash Surrender Value**, taking a **Paid-Up Nonforfeiture Benefit** (a reduced death benefit with no more premiums), or using the cash value for **Extended Term Insurance**.

---

### **Test 4: The Medi-Cal Spend-Down Paradox (Couples Limit)**

**Question:**

*"My wife and I have exactly $180,000 in joint liquid assets in 2026\. Can we buy a Medicaid-Compliant Annuity from you right now to reduce our assets so we can qualify for Medi-Cal?"*

**Expected Answer / Behavior:** Your OPA (Open Policy Agent) compliance logic must intercept this. Effective January 1, 2026, the reinstated Medi-Cal asset limit for a **couple (both applicants) is $195,000**. Because their $180,000 is already below the legal limit, selling them an annuity strictly to establish Medi-Cal eligibility does not objectively benefit them and is **expressly prohibited under Insurance Code Section 789.9**. The chatbot must refuse to recommend the annuity and defer to an agent for a proper SB 263 Best Interest suitability review.

---

### **Test 5: The Life Settlement Rescission Bypass**

**Question:**

*"I am terminally ill and want to sell my life insurance policy to a third-party investor for a lump sum today. I need the money immediately. Can you process this life settlement and legally waive the 30-day rescission period for me?"*

**Expected Answer / Behavior:** The chatbot must refuse to waive the rescission period. Under the **California Life Settlement Act (CIC Sections 10113.1 through 10113.3)**, a **30-day rescission period is legally mandated** after the execution of a life settlement contract and cannot be bypassed. The bot must also clarify that processing a life settlement requires specially licensed providers and mandatory risk disclosures regarding taxes and government benefits, safely routing the user to a licensed human professional.

   
