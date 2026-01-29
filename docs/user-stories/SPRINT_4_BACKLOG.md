# Sprint 4 Backlog: Advanced Analytics & Dunning Automation

**Sprint Goal:** Automate proactive customer communication (Dunning) and deploy high-level executive dashboards for DSO and cash flow forecasting.

---

## 🏗️ Story 4.1: Automated Dunning Engine (ZF259+)
**User Persona:** As a Credit Manager, I want the system to automatically send reminder emails based on invoice due dates so that I can reduce manual follow-up time.

### 📝 Description
Develop a trigger-based email engine that pulls "Confirmation Scenarios" from the DB. If no confirmation is received for an invoice due within 5 days, the system sends a customized Dunning letter.



### ✅ Acceptance Criteria
- [ ] System identifies invoices meeting the "Dunning Trigger" (e.g., 5 days before due date).
- [ ] Emails are populated with a dynamic spreadsheet attachment of all overdue items for that specific customer.
- [ ] System logs the "Last Contact Date" in the SAP customer master record.
- [ ] Analyst can "Snooze" dunning for specific disputed accounts.

---

## 🏗️ Story 4.2: Real-time "Time-Gap" & Performance Tracker
**User Persona:** As an Operations Lead, I want to track the time difference between bank receipt (MT942) and GL clearing so that I can identify operational bottlenecks.

### 📝 Description
Create a performance metric that calculates the "Mean Time to Post." It tracks the payment journey from Bank Ingestion ⮕ AI Match ⮕ Analyst Approval ⮕ SAP Posting.

### ✅ Acceptance Criteria
- [ ] Dashboard displays "Average Posting Latency" (Target: < 4 hours).
- [ ] Visualization of the "Bottleneck Step" (e.g., Is the delay in AI processing or Analyst review?).
- [ ] Ability to filter performance by Analyst or Region.

---

## 🏗️ Story 4.3: Cash Flow & DSO Forecasting Dashboard
**User Persona:** As a CFO, I want to see a forecast of expected cash inflows based on historical payment behavior so that I can manage company liquidity.

### 📝 Description
Leverage historical "Payment Receipt" data to predict when "Open Invoices" will likely be paid, regardless of the official due date.



### ✅ Acceptance Criteria
- [ ] Forecast chart showing "Projected Cash Inflow" for the next 30/60/90 days.
- [ ] Integration of "Scenario C" (Claims) into the forecast (e.g., reducing expected inflow by the average claim %).
- [ ] Display real-time **DSO (Days Sales Outstanding)** trend line.

---

## 🏗️ Story 4.4: Role-Based Access Control (RBAC) & Audit Trail
**User Persona:** As an Internal Auditor, I want a complete log of all manual overrides so that we comply with SOX and internal security policies.

### 📝 Description
Implement secure login and permission tiers. Ensure every manual change to a match is logged with a "Reason for Change."

### ✅ Acceptance Criteria
- [ ] Define roles: `AR_Analyst` (Match/Code), `AR_Manager` (Approve High Value), `Auditor` (Read Only).
- [ ] Every manual override must require a text comment and a Reason Code.
- [ ] Exportable "Audit Log" showing: `Timestamp`, `User`, `Old_Value`, `New_Value`, `Action`.

---

## 🚀 Technical Sub-tasks for Developers
1. **Email Service:** Integrate `SendGrid` or `SMTP` for automated dunning triggers.
2. **Data Science:** Build a simple linear regression or moving average model for the cash forecast.
3. **Security:** Implement `OAuth2` or `JWT` for secure session management.
4. **Logging:** Use `Loguru` or standard Python logging to capture all state changes in a dedicated `audit_log` table.
