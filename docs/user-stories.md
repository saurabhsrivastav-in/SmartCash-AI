# 🏃 User Stories & Sprint Backlog: SmartCash AI

**Project:** SmartCash AI - Treasury Automation  
**Cycle:** 2-Week Sprints (8 Weeks Total)  
**Alignment:** BRD v1.0 / PRD v1.1

---

## 🟦 Sprint 1: The Heuristic Core (Weeks 1-2)
**Goal:** Implement the "Waterfall" matching logic to achieve basic STP.

### US-101: Tiered Matching Logic
* **As an** AR Analyst,
* **I want** the system to automatically clear invoices where the Amount and ID match exactly,
* **So that** I don't waste time on standard transactions.
* **Acceptance Criteria:**
    * System identifies $1:1$ matches with 100% precision.
    * Logic utilizes `thefuzz` for Level 2 similarity scoring (>90%).
    * Results are categorized into "Green" (Auto) and "Amber" (Review) buckets.

### US-102: Data Ingestion Pipeline
* **As a** System Architect,
* **I want** an asynchronous FastAPI endpoint for CSV uploads,
* **So that** large bank feeds (1,000+ rows) don't freeze the UI.
* **Acceptance Criteria:**
    * Supports UTF-8 encoded CSVs.
    * Validation logic rejects files missing mandatory columns (`Invoice_ID`, `Amount`).

---

## 🟩 Sprint 2: Strategic Visualization (Weeks 3-4)
**Goal:** Transform raw data into executive-level liquidity insights.

### US-201: Multi-Level Risk Radar
* **As a** Treasurer,
* **I want** a Sunburst visualization of my ledger,
* **So that** I can see risk concentration by Currency and Customer ESG score.
* **Acceptance Criteria:**
    * Interactive Plotly chart with at least 3 layers (Currency > Payer > Risk Level).
    * Chart updates dynamically based on the uploaded dataset.



### US-202: Liquidity Stress Simulator
* **As a** CFO,
* **I want** to use a slider to simulate the impact of collection delays,
* **So that** I can forecast "Free Cash Flow" under market stress.
* **Acceptance Criteria:**
    * Uses `NumPy` for real-time recalculation of the waterfall chart.
    * Handles latency inputs from 0 to 90 days.

---

## 🟨 Sprint 3: GenAI & Exception Mgmt (Weeks 5-6)
**Goal:** Automate the "Last-Mile" communication gap.

### US-301: Autonomous Remittance Request
* **As an** AR Analyst,
* **I want** the AI to draft a dunning email for "Red" (Unmatched) scenarios,
* **So that** I don't have to manually investigate every missing reference.
* **Acceptance Criteria:**
    * GenAI extracts "Payer Name" and "Amount" from unstructured bank text.
    * Drafts a professional email template via LLM integration.

### US-302: Deduction Root-Cause Analysis
* **As an** Auditor,
* **I want** the system to flag if a variance is likely a "Bank Fee" or a "Short Payment,"
* **So that** I can categorize losses correctly.
* **Acceptance Criteria:**
    * Categorizes variances within a 2% threshold as "Fees."
    * Flags larger variances as "Disputes."

---

## 🟥 Sprint 4: Governance & Compliance (Weeks 7-8)
**Goal:** Lock down the system for institutional audit.

### US-401: SOC2 Compliance Vault (Logging)
* **As a** Compliance Officer,
* **I want** every automated match to generate a unique cryptographic hash,
* **So that** I have an immutable trail of AI-driven decisions.
* **Acceptance Criteria:**
    * `Hash_ID` is generated using SHA-256 for every reconciliation.
    * Logs are viewable in a non-editable "Audit Ledger" tab.

### US-402: Production Hardening
* **As a** Lead Developer,
* **I want** to move all secrets to an environment vault and pin dependencies,
* **So that** the deployment is secure and stable.
* **Acceptance Criteria:**
    * `requirements.txt` contains pinned versions (e.g., `thefuzz==0.19.0`).
    * No API keys present in `main.py`.

---

## 📈 Sprint Estimation Summary
| Sprint | Duration | Story Points | Status |
| :--- | :--- | :--- | :--- |
| **S1: Core** | 2 Weeks | 21 | ✅ Complete |
| **S2: Visual** | 2 Weeks | 13 | ✅ Complete |
| **S3: GenAI** | 2 Weeks | 21 | ✅ Complete |
| **S4: Vault** | 2 Weeks | 8 | ✅ Complete |
