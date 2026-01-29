# BRD: SmartCash AI - Treasury Automation Engine

**Project:** SmartCash AI Automation: Next-Gen Order-to-Cash (O2C)  
**Product Area:** AI-Driven Invoice Management & Treasury Operations  
**Author:** Saurabh Srivastav  
**Date:** January 2026  
**Status:** Final Version for Stakeholder Approval  

---

## 1. Executive Summary
The SmartCash AI initiative is designed to eliminate the manual "last-mile" friction in the Order-to-Cash (O2C) cycle. By leveraging Large Language Models (LLMs) and fuzzy matching logic, we aim to bridge the gap between fragmented remittance data (PDFs, emails, portals) and the SAP General Ledger. Our goal is to transform the treasury from a reactive processing center to a proactive liquidity hub.

---

## 2. Business Context: The Strategic O2C Flow
The automation targets the critical junction where financial intent meets bank reality:



1. **Purchase Order Ingestion**
2. **Inventory Validation**
3. **PO Acceptance**
4. **Sales Invoice Generation**
5. **Service/Goods Fulfillment**
6. **A/R Ledger Update**
7. **Billing Distribution**
8. **Payment Initiation**
9. **Bank Credit Receipt**
10. **Invoice Management (AI Priority)**
11. **Reconciliation & Clearing (AI Priority)**
12. **Financial Reporting**

---

## 3. Current State & Problem Definition

### 3.1 The "Manual Trap" Workflow
Currently, the "Operations Team" acts as a human middleware:
* **Fragmented Remittance:** Analysts manually scrape remittance data from a centralized mailbox.
* **Comment Registration:** Qualitative customer data is manually keyed into "Cash Reports."
* **Claim Gridlock:** Deductions and short-payments are handled via email threads with no central audit trail.

### 3.2 Quantitative Pain Points
* **Reconciliation Latency:** Average 48-hour delay between bank credit and SAP clearing.
* **DSO Bloat:** Days Sales Outstanding (DSO) is currently 3-5 days higher than the industry benchmark due to unapplied cash.
* **Exception Fatigue:** 40% of transactions require manual intervention due to missing Invoice IDs or currency fluctuations.

---

## 4. Technical Architecture
The solution sits at the intersection of three enterprise units:



1. **Treasury Gateway (MT942):** 4x daily ingestion of SWIFT intraday messages.
2. **SmartCash AI Engine:** Python-based matching logic (utilizing `thefuzz` and `LLMs`).
3. **SAP Integration Layer:** Automated Posting (BAPI/OData) for GL settlement.

---

## 5. Functional Requirements (FR)

### 5.1 Data Orchestration
| ID | Requirement | Technical Specification | Priority |
| :--- | :--- | :--- | :--- |
| **FR-01** | **MT942 Real-time Sync** | Automatic parsing of SWIFT MT942 files every 6 hours. | P0 |
| **FR-02** | **Cognitive Extraction** | AI-driven OCR to extract remittance data from PDF, JPG, and Email. | P0 |
| **FR-03** | **Heuristic Matching** | Matching engine must support Exact, Fuzzy, and Multi-Invoice grouping. | P0 |
| **FR-04** | **ESG Integration** | Flag payments from customers with ESG scores below 'C'. | P2 |

### 5.2 The Logic Gates (Confirmation Scenarios)
The engine must classify all incoming credits into one of four logic buckets:
* **Scenario A (Standard):** Full match of Amount + Invoice ID.
* **Scenario B (Dispute):** Payer confirms they will NOT pay specific line items.
* **Scenario C (Partial/Claims):** Payment received with attached deduction codes (e.g., "Damaged Goods").
* **Scenario D (Unidentified):** Receipt with no metadata (Routed to AI Agent for customer outreach).

---

## 6. AI & Intelligent Workflows
* **Autonomous Dunning:** AI generates personalized, polite follow-ups for Scenario D cases.
* **Deduction Mapping:** System auto-suggests GL reason codes based on historical claim patterns.
* **Liquidity Heatmaps:** Real-time visualization of cash inflow vs. forecast.

---

## 7. Non-Functional Requirements (NFR)
* **Straight-Through Processing (STP):** Target >90% for standard invoices.
* **Auditability:** Every AI decision must be logged in the **SOC2 Compliance Vault**.
* **Global Support:** Support for USD, EUR, and GBP with real-time FX conversion logic.

---

## 8. Implementation Roadmap
* **Q1 (Foundation):** MT942 ingestion, Python engine setup, and "Exact Match" logic.
* **Q2 (Intelligence):** Implementation of `thefuzz` and LLM-based remittance scraping.
* **Q3 (Ecosystem):** Full SAP write-back and automated dispute resolution.

---

## 9. Key Performance Indicators (KPIs)
* **DSO Reduction:** -4 days.
* **STP Rate:** 85%+ (Automated Clearing).
* **FTE Efficiency:** 60% reduction in manual data entry time.
