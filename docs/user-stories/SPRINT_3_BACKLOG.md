# Sprint 3 Backlog: Scale & ERP Integration

**Sprint Goal:** Complete the O2C loop by integrating Sales Order data, automating SAP GL posting (Write-back), and deploying AI-driven worklist prioritization.

---

## 🏗️ Story 3.1: Full O2C Data Integration (Orders to Cash)
**User Persona:** As a Credit Manager, I want to see the original Sales Order data linked to the outstanding invoice so that I can verify pricing or shipping disputes instantly.

### 📝 Description
Integrate the Sales Order (SO) table data from the ERP. The system must create a "Golden Record" that links: `Sales Order` ⮕ `Delivery Note` ⮕ `Invoice` ⮕ `Payment`.



### ✅ Acceptance Criteria
- [ ] UI displays the linked PO/SO number alongside every open invoice.
- [ ] System automatically resolves "Pricing Mismatches" by checking the approved Sales Order price against the payment received.
- [ ] Users can drill down into "Line Item" details for Bulk Payments.

---

## 🏗️ Story 3.2: Automated SAP GL Clearing (Write-back)
**User Persona:** As an AR Accountant, I want the system to automatically post the matched payments to SAP so that the General Ledger is updated without manual entry.

### 📝 Description
Develop the "Write-back" connector. Once a match is confirmed (Auto or Manual), the system calls the SAP BAPI (e.g., `BAPI_ACC_DOCUMENT_POST`) to clear the invoice.

### ✅ Acceptance Criteria
- [ ] Successful posting of "Full Payments" directly to the SAP GL.
- [ ] Successful posting of "Partial Payments" with the correct **Deduction Reason Code**.
- [ ] System captures the "SAP Document Number" as a reference for successful posting.
- [ ] Fail-safe: Any failed posting must be logged and flagged in the "Sync Error" queue.

---

## 🏗️ Story 3.3: AI-Prioritized "Smart Worklist"
**User Persona:** As an AR Analyst, I want the system to sort my worklist by "Collection Risk" and "Value" so that I tackle the most critical items first.

### 📝 Description
Replace the static list with an AI-prioritized queue. The algorithm should rank tasks based on:
1. Amount ($) 
2. Days Overdue
3. Historical "Payment Reliability" of the customer.



### ✅ Acceptance Criteria
- [ ] The dashboard "Sort" defaults to the **Smart Score**.
- [ ] Display a "Risk Indicator" (High/Medium/Low) based on historical claim frequency.
- [ ] Real-time refresh of the worklist as new MT942 files are ingested.

---

## 🏗️ Story 3.4: Real-time Claim & Deduction Aging Report
**User Persona:** As a Finance Director, I want to see the aging of open claims so that I can identify recurring commercial disputes.

### 📝 Description
Create a reporting module that tracks deductions that were coded in Sprint 2 but remain unresolved.

### ✅ Acceptance Criteria
- [ ] Chart showing "Deductions by Category" (e.g., 40% Damaged, 30% Pricing).
- [ ] Aging buckets for claims (0-30, 31-60, 61+ days).
- [ ] Export functionality to CSV/Excel for commercial team review.

---

## 🚀 Technical Sub-tasks for Developers
1. **ERP Connector:** Develop the SAP RFC or OData service for `POST` operations.
2. **Priority Algorithm:** Build a scoring weightage script (e.g., `Score = (Amount * 0.6) + (Days_Overdue * 0.4)`).
3. **Analytics:** Implement `Plotly` or `Chart.js` in Streamlit for the Aging Report.
4. **Final UI Polish:** Implement Role-Based Access Control (RBAC) so only "Managers" can approve high-value overrides.
