# 📡 Sprint 5 Backlog: Strategic Ecosystem & ESG Intelligence

**Sprint Goal:** Integrate external ESG risk scoring and CRM metadata to transform the matching engine into a holistic risk-governance platform.

---

## 🏗️ Story 5.1: Real-Time ESG Risk Orchestration
**User Persona:** As a Compliance Officer, I want the system to flag payments from entities with declining ESG scores so we can proactively manage reputational risk.

### 📝 Description
Develop an integration layer that maps customer IDs to external Sustainability Ratings (AA to C). This data must be injected into the `SmartMatchingEngine` to influence the risk-weighting of unsettled invoices.

### ✅ Acceptance Criteria
- [ ] **Data Mapping:** Successfully joins the `invoices` dataset with a new `esg_ratings` reference table.
- [ ] **Dynamic Flagging:** Any transaction with an ESG score below 'B' must trigger a high-visibility badge in the Analyst Workbench.
- [ ] **Risk Weighting:** The "Executive Risk Radar" must allow filtering specifically by ESG tier.



---

## 🏗️ Story 5.2: CRM Metadata Ingestion (Salesforce/Dynamics)
**User Persona:** As an AR Analyst, I want to see recent "Collection Notes" from our CRM within the workbench so I understand why a customer might be delaying payment.

### 📝 Description
Establish a data connector that pulls qualitative notes (e.g., "Customer disputing shipment #102") and displays them alongside the unmatched bank transaction.

### ✅ Acceptance Criteria
- [ ] **Contextual Display:** A "CRM Insights" panel appears in the Analyst Workbench when a transaction is selected.
- [ ] **GenAI Enhancement:** The `GenAIAssistant` utilizes these CRM notes to customize the tone of the dunning email (e.g., mentioning the specific shipment dispute).

---

## 🏗️ Story 5.3: The "Risk Radar" Sunburst 2.0
**User Persona:** As a Treasurer, I want to see a multi-dimensional view of exposure so I can see which currency-region is most impacted by low-ESG customers.

### 📝 Description
Enhance the Plotly Sunburst visualization to support three levels of drill-down: **Currency → ESG Category → Customer**. 

### ✅ Acceptance Criteria
- [ ] **Visual Depth:** Implement `px.sunburst` with the path `['Currency', 'ESG_Score', 'Customer']`.
- [ ] **Color Logic:** Map colors to the `ESG_Score` column (Green for AA/A, Yellow for B, Red for C).
- [ ] **Interactivity:** Clicking a segment must update the "Unapplied Cash" metric for that specific filtered view.

---

## 🏗️ Story 5.4: Automated Credit Limit Alerts
**User Persona:** As a Credit Manager, I want to receive an alert if a customer’s "Unapplied Cash" + "Open Invoices" exceeds their credit limit.

### 📝 Description
Implement a threshold monitoring system. When a bank credit remains unmatched, the system calculates the total outstanding exposure for that entity and compares it against a pre-set credit limit.

### ✅ Acceptance Criteria
- [ ] **Exposure Calculation:** `Total_Exposure = Sum(Open_Invoices) - Unapplied_Bank_Credits`.
- [ ] **Alert Trigger:** Display a high-priority alert if `Total_Exposure > Credit_Limit`.
- [ ] **Audit Trail:** Log the credit breach alert in the SOC2 Compliance Vault.

---

## 🚀 Technical Sub-tasks for Developers
1. **API Integration:** Create a mock API handler for `services/esg_provider.py`.
2. **Schema Update:** Update `mock_data_maker.py` to generate credit limits and ESG categories.
3. **UI Logic:** Enhance the sidebar with an "ESG Sensitivity" toggle to highlight risky transactions.
4. **Data Science:** Refine the matching engine to prioritize clearing "High ESG Risk" invoices first to reduce exposure.
