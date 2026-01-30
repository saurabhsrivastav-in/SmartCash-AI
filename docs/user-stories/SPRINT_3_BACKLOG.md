# 🤖 Sprint 3 Backlog: Cognitive Automation & GenAI Agents

**Sprint Goal:** Deploy the GenAI "Co-Pilot" to autonomously resolve reconciliation exceptions and automate institutional remittance dunning.

---

## 🏗️ Story 3.1: GenAI Remittance Agent
**User Persona:** As an AR Analyst, I want the system to draft personalized dunning emails for unmatched payments so I can resolve exceptions without manual typing.

### 📝 Description
Integrate a Large Language Model (LLM) via the `GenAIAssistant` class. When the Match Engine fails to find a Level 1 or Level 2 match, the system must analyze the bank narrative and generate a professional inquiry email.

### ✅ Acceptance Criteria
- [ ] **Context Awareness:** The draft must include the Payer Name, Amount, and Currency found in the bank feed.
- [ ] **Tone Control:** Emails must maintain "Institutional Professionalism" (Polite but firm).
- [ ] **UI Integration:** The draft must appear in a `st.text_area` within the Analyst Workbench for one-click copying.



---

## 🏗️ Story 3.2: Short-Payment & Variance Logic
**User Persona:** As a Finance Manager, I want the system to identify partial payments so that we can trigger dispute workflows for underpayments.

### 📝 Description
Develop logic to handle "Scenario C" (Partial Payments). The engine must identify if a payment is within a "Bank Fee" tolerance (e.g., <$25) or if it constitutes a significant "Short-Pay" dispute.

### ✅ Acceptance Criteria
- [ ] **Tolerance Check:** Amounts within 0.5% variance are flagged as "Minor Variance" (Auto-Adjust).
- [ ] **Dispute Flagging:** Variances >0.5% are marked as `STATUS_DISPUTE`.
- [ ] **Reason Coding:** GenAI suggests a reason code (e.g., "Tax Withholding" or "Damaged Goods") based on the bank narrative.

---

## 🏗️ Story 3.3: Advanced Liquidity Bridge (Waterfall 2.0)
**User Persona:** As a CFO, I want to see the specific impact of "Stressed Collections" on our net cash position.

### 📝 Description
Enhance the Plotly Waterfall chart to show three distinct states: Opening Balance, Expected Inflows (Full), and Stressed Inflows (Haircut).

### ✅ Acceptance Criteria
- [ ] **Dynamic Calculation:** The "Collections (Stressed)" bar must reflect the `liquidity_haircut` variable in real-time.
- [ ] **Connector Logic:** Ensure Waterfall connectors properly link "Gross Liquidity" to "Net Position."
- [ ] **Legend & Tooltips:** Add hover-data showing the exact dollar amount lost to "Collection Latency."



---

## 🏗️ Story 3.4: Global ESG Risk Flagging
**User Persona:** As a Compliance Officer, I want the system to highlight payments from low-ESG-rated entities so we can maintain ethical treasury standards.

### 📝 Description
Upgrade the Risk & Governance view to include an **ESG Portfolio Alert** system. Payments from 'C' rated customers must trigger a visual warning in the Audit Ledger.

### ✅ Acceptance Criteria
- [ ] **Visual Cues:** Use `st.warning` or color-coded rows for transactions involving 'C' rated entities.
- [ ] **Drill-Down:** Clicking a segment in the Sunburst chart displays a list of the specific invoices contributing to that risk level.
- [ ] **Compliance Log:** The `Audit Ledger` must record the ESG score at the time of match.

---

## 🚀 Technical Sub-tasks for Developers
1. **GenAI Integration:** Implement `backend/ai_agent.py` using an LLM API (OpenAI/Gemini/Local Llama).
2. **Logic Expansion:** Update `SmartMatchingEngine.run_match` to return "Partial Match" statuses.
3. **UI Polish:** Add `st.balloons()` for STP success and `st.snow()` if the liquidity haircut exceeds 30%.
4. **Mock Data Expansion:** Update `mock_data_maker.py` to create "Short-Payment" rows where `Bank_Amount < Invoice_Amount`.
