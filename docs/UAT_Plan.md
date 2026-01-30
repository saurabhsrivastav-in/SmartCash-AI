# 🧪 User Acceptance Testing (UAT) Plan: SmartCash AI

**Project:** SmartCash AI - Institutional Treasury Automation  
**Version:** 1.0.0 (Pre-Production Validation)  
**Lead QA/UAT Lead:** Saurabh Srivastav  
**Stakeholders:** Treasury Operations, AR Analysts, Compliance/Audit  

---

## 1. UAT Objective
The goal of this UAT is to ensure that the **SmartCash AI** platform accurately identifies payment matches, handles financial exceptions via AI, and maintains a perfect audit trail before moving to a live production environment with SAP integration.

---

## 2. Test Environment & Prerequisites
* **Platform:** Streamlit Cloud / Local Python 3.11 Environment.
* **Test Data:** Generated via `mock_data_maker.py` (200+ invoices across USD, EUR, GBP, INR, CHF).
* **Browser:** Chrome, Edge, or Safari (Latest versions).
* **Dependencies:** `thefuzz`, `pandas`, `plotly` libraries must be initialized.

---

## 3. UAT Scope & Test Scenarios

### 3.1 Scenario 1: Executive Dashboard & Macro Stress
**Goal:** Validate that the "Liquidity Haircut" logic correctly impacts the waterfall chart.
* **Action:** Adjust the "Collection Latency" slider in the sidebar.
* **Expected Result:** * "Adjusted DSO" metric increases in real-time.
    * "Liquidity Bridge" waterfall chart updates to show a reduction in "Collections (Stressed)."
    * No "Broken Image" icons appear in the hero section.



### 3.2 Scenario 2: Smart Matching (Exact & Fuzzy)
**Goal:** Test the `thefuzz` engine's ability to handle "dirty" bank data.
* **Action:** Select a transaction in the **Analyst Workbench** where the payer name in the bank feed is slightly different from the invoice (e.g., "Tesla Ltd" vs "Tesla Inc").
* **Expected Result:** * System returns a "Fuzzy Match" with a confidence score.
    * If score > 95%, system triggers "STP MATCH CONFIRMED" and balloons.
    * Matching logic correctly identifies the Invoice ID.



### 3.3 Scenario 3: Exception Handling & GenAI
**Goal:** Verify the AI "Co-Pilot" functionality for low-confidence matches.
* **Action:** Identify a transaction with < 90% confidence.
* **Expected Result:** * A warning message appears: "⚠️ EXCEPTION: Match Confidence Low."
    * The "AI Remittance Request Draft" text area populates with a professional, customer-specific email.

### 3.4 Scenario 4: Audit Ledger & Compliance
**Goal:** Ensure 100% traceability of all actions.
* **Action:** Navigate to the **Audit Ledger** after performing 3-5 matches.
* **Expected Result:** * The table displays unique `Hash_ID` for every transaction.
    * The "Action" column correctly logs "AUTO_STP" or "MANUAL_REVIEW."

---

## 4. Acceptance Criteria (Go/No-Go)
| ID | Criteria | Required Result |
| :--- | :--- | :--- |
| **AC-01** | **Matching Accuracy** | > 98% accuracy on Level 1 (Exact) matches. |
| **AC-02** | **System Latency** | UI updates and calculations occur in < 1.5 seconds. |
| **AC-03** | **Data Integrity** | Sum of "Net Position" in Waterfall must match calculated metrics. |
| **AC-04** | **Risk Visibility** | Risk Radar Sunburst must correctly segment by Currency. |



---

## 5. Defect Logging & Severity Levels
* **S1 (Critical):** Application crash or incorrect cash balance calculation.
* **S2 (High):** Fuzzy matching logic failing on obvious matches (>90% similarity).
* **S3 (Medium):** UI misalignment or formatting errors in charts.
* **S4 (Low):** Minor typos or caption changes.

---

## 6. Sign-Off Panel
* **Business Lead:** ____________________ Date: __________
* **Technical Lead:** ____________________ Date: __________
* **Audit/Compliance:** ____________________ Date: __________

---
