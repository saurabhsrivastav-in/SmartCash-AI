# PRD: SmartCash AI Matching Engine

**Product Manager:** Saurabh Srivastav

**Status:** In-Development

**Target Release:** Q1 2026 (Phase 1)

**Tracking Link:** [Live Demo](https://smartcash-ai-ezywbepvihp9bnvqgndwrb.streamlit.app/)

---

## 1. Goal & Vision

To transform the manual "centralized mailbox" reconciliation into an **Autonomous Cash Application** system. We will move from manual data entry to "Exception-Only" management, targeting a **95% Straight-Through Processing (STP)** rate for all inbound cash.

---

## 2. User Personas

* **AR Analyst (Primary):** Needs a prioritized worklist to resolve "Suggested Matches" and code deductions.
* **Treasury IT Manager:** Needs reliable MT942 data ingestion pipelines.
* **CFO:** Needs real-time visibility into "Unapplied Cash" and DSO metrics.

---

## 3. Functional Specifications

### 3.1 Data Pipeline & Ingestion (The "Input")

The system must act as a data aggregator for the following sources:

| Feature ID | Feature Name | Specification |
| --- | --- | --- |
| **P-1.1** | MT942 Parser | System must pull bank files 4x daily (09:00, 12:00, 15:00, 18:00). It must parse SWIFT Tag 61 (Amounts) and Tag 86 (Unstructured Remittance Info). |
| **P-1.2** | Multi-Channel OCR | Utilize Layout-aware AI to extract Invoice numbers, Net amounts, and Tax amounts from PDF attachments and email bodies. |
| **P-1.3** | SAP Linkage | Query SAP API for Open Receivables (Table BSID/BSAD) to create a real-time "Matching Pool." |

### 3.2 The Matching Logic (The "Brain")

Matches are processed through a "Waterfall" logic:

1. **Level 1: Exact Match:** `Bank_Amount == Invoice_Amount` AND `Bank_Ref == Invoice_ID`. (Status: **Auto-Post**)
2. **Level 2: Fuzzy Match:** Customer name similarity >90% AND `Amount` matches. (Status: **Suggested**)
3. **Level 3: Many-to-One:** One bank credit matches the sum of 2+ open invoices for the same customer. (Status: **Suggested**)
4. **Level 4: Short-Pay Logic:** Match found but `Bank_Amount < Invoice_Amount`. (Status: **Exception - Action Required**)

### 3.3 Analyst Workbench (The "UI")

* **Prioritized View:** Instead of a first-in-first-out list, tasks are sorted by `Invoice Value` and `Customer Risk Score`.
* **Action Buttons:** One-click "Approve Match," "Request Info," and "Post to Account."
* **Deduction Coder:** If a short-pay is identified, the UI must provide a dropdown for **Reason Codes** (e.g., ZF01: Damaged Goods, ZF02: Cash Discount).

---

## 4. User Experience (UX) & Design

* **Dashboard Logic:**
* **Green (STP):** Successfully matched and queued for SAP GL update.
* **Yellow (Action):** High confidence match found, requires one-click analyst approval.
* **Red (Exception):** No match found; requires manual investigation or dunning trigger.


* **Latency:** All dashboard interactions (filtering/sorting) must respond in **<1.5 seconds**.

---

## 5. Non-Functional Requirements (NFRs)

* **Scalability:** The engine must handle up to **50,000 line items per hour** during month-end peaks.
* **Auditability:** Every match (Auto or Manual) must have an audit log: `User_ID`, `Timestamp`, `Algorithm_Confidence`, and `Reason_Code`.
* **Security:** SOC2 Type II compliance. Payment data must be masked where PCI-DSS applies.

---

## 6. Success Metrics (KPIs)

* **Match Rate:** % of payments auto-posted without human touch (Target: 85%).
* **DSO (Days Sales Outstanding):** Goal to reduce from current average to -5 days by Q4.
* **Analyst Throughput:** Increase number of payments processed per hour per head by 400%.

---

## 7. Implementation Roadmap (Technical View)

* **Sprint 1-4 (Foundation):** MT942 Parsing, SAP Read-only API, Exact Match Logic.
* **Sprint 5-8 (Intelligence):** OCR Engine for PDF Remittance, Fuzzy Logic, Deduction Coder UI.
* **Sprint 9-12 (Scale):** AI-Prioritization, Automated SAP Write-back (GL Clearing), Dunning integration.

---

## 8. Exception Handling & Edge Cases

* **Duplicate Remittance:** System must flag if the same bank reference ID is ingested twice.
* **Currency Mismatch:** If a payment is in EUR but the invoice is in USD, the system must pull the midday exchange rate for variance calculation.
* **Overpayments:** Any payment exceeding invoice amount must be flagged for "Customer Credit Memo" creation.

---
