# Product Requirements Document (PRD): SmartCash AI 

## 1. Document Overview
* **Product Name:** SmartCash AI
* **Project Lead:** Saurabh Srivastav
* * **Version:** 1.0.0
* **Objective:** To automate the cash application process by matching bank payments to open receivables using explainable AI.

---

## 2. The Problem Space
Enterprise AR (Accounts Receivable) teams struggle with "The Remittance Gap." HighRadius and other legacy players often:
1.  **Lack Transparency:** Users don't know *why* a payment didn't match.
2.  **High Implementation Cost:** Require months of setup.
3.  **Rigid Logic:** Fail when customer names have slight variations (e.g., "Walmart Inc" vs "Walmart #402").

**SmartCash AI** solves this by using fuzzy-logic matching and an "Analyst-First" UI.

---

## 3. System Architecture & Workflow
The application follows a three-tier processing logic to ensure the highest possible Straight-Through Processing (STP) rate.



1.  **Ingestion:** Payment files (Lockbox/EFT) are ingested via API.
2.  **Matching Engine:** The backend runs a multi-pass matching algorithm (Exact -> Fuzzy -> Historical).
3.  **Exception Handling:** Any match below the 90% confidence threshold is routed to the Streamlit Workbench.

---

## 4. Functional Requirements

### 4.1 Automated Matching Engine (Core)
* **REQ-01: Exact Match.** System must automatically clear invoices where Reference ID and Amount are identical.
* **REQ-02: Fuzzy Customer Logic.** System must utilize Levenshtein Distance to identify payers with typos or legal suffix variations (e.g., "Ltd" vs "Limited").
* **REQ-03: Partial Payment Detection.** If a payment is < Invoice Amount, system must flag it as a "Short Payment" and prompt for a Reason Code (e.g., "Damaged Goods").

### 4.2 Analyst Workbench (UI)
* **REQ-04: Confidence Scoring.** Every suggested match must display a 0-100% confidence score.
* **REQ-05: One-Click Posting.** Analysts must be able to approve a "Suggested Match" with a single click.
* **REQ-06: Real-time Metrics.** Dashboard must show "Unapplied Cash" totals in real-time.

---

## 5. Technical Constraints & Stack
* **Backend:** Python 3.10+, FastAPI (chosen for high-speed asynchronous processing).
* **Logic:** FuzzyWuzzy for string similarity; Custom scoring algorithms for financial validation.
* **Frontend:** Streamlit (for rapid prototyping of internal finance tools).

---

## 6. Success Metrics (KPIs)
| KPI | Target | Why it matters |
| :--- | :--- | :--- |
| **STP Rate** | > 90% | Reduces manual labor costs. |
| **Match Accuracy** | 99.9% | Prevents misapplication of cash and customer disputes. |
| **DSO Reduction** | -2 Days | Improves company liquidity and cash flow. |

---

## 7. Future Roadmap (Phase 2)
* **Generative AI Remittance:** Use LLMs to read unstructured email bodies to find payment advice.
* **Deduction Management:** Auto-dispute invalid short-payments by checking shipping logs.
* **ERP Connectors:** Native plugins for SAP S/4HANA and Oracle NetSuite.
