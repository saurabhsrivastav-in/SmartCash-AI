# 🛡️ Sprint 4 Backlog: Multi-Currency Scaling & Audit Hardening

**Sprint Goal:** Finalize the global scaling engine to handle cross-border FX variances and secure the SOC2 Audit Ledger for production-grade governance.

---

## 🏗️ Story 4.1: Multi-Currency FX Variance Engine
**User Persona:** As a Treasury Manager, I want the system to handle small FX discrepancies so that international payments aren't rejected due to penny-rounding errors.

### 📝 Description
Implement a "Currency Tolerance" logic gate. When matching a EUR payment to a USD invoice, the engine must allow for a +/- 2% variance to account for mid-market rate fluctuations and intermediary bank fees.

### ✅ Acceptance Criteria
- [ ] **FX Gate:** Engine successfully matches payments across different currency codes if the converted amount is within tolerance.
- [ ] **Auto-Adjustment:** System creates a "Penny-Rounding" log for differences < $5.00.
- [ ] **Reporting:** The Executive Dashboard reflects the "FX Impact" on total liquidity.

---

## 🏗️ Story 4.2: Institutional Audit Ledger (Production)
**User Persona:** As an External Auditor, I want to see an immutable record of every AI-driven decision so that the company remains SOC2 compliant.

### 📝 Description
Upgrade the `Audit Ledger` from a simple table to a cryptographically verified log. Every match action must be hashed using SHA-256, linking the user session, the algorithm used, and the final outcome.

### ✅ Acceptance Criteria
- [ ] **Immutability:** Every log entry includes a `Hash_ID` that changes if the row data is tampered with.
- [ ] **Decision Mapping:** Logs must clearly distinguish between `AUTO_STP` (Engine) and `MANUAL_CONFIRM` (Analyst).
- [ ] **Export Functionality:** Add a "Download Audit CSV" button for reporting purposes.



---

## 🏗️ Story 4.3: Smart Matching 2.0 (Collective Payments)
**User Persona:** As an AR Analyst, I want the system to match one bank credit to multiple invoices so that I don't have to manually split bulk payments.

### 📝 Description
Implement "Many-to-One" matching logic. If a single bank credit amount equals the sum of two or more open invoices for the same customer, the engine suggests a "Collective Match."

### ✅ Acceptance Criteria
- [ ] **Heuristic Gate:** Logic scans for combinations of open invoices that sum up to the received `Bank_Amount`.
- [ ] **Verification:** Collective matches must be flagged for Analyst review in the Workbench before posting.
- [ ] **UI Update:** The workbench must show the specific list of invoices being settled by the bulk payment.



---

## 🏗️ Story 4.4: Performance Benchmarking & Scaling
**User Persona:** As a Treasury IT Lead, I want the dashboard to load in < 2 seconds even with 50,000 invoices so that the system remains responsive under high volume.

### 📝 Description
Optimize the Streamlit caching layer (`st.cache_data`) and the `thefuzz` execution speed. Implement batch-processing for fuzzy matching to avoid UI blocking.

### ✅ Acceptance Criteria
- [ ] **Latency Check:** Dashboard metrics and Waterfall charts render in < 1.5s for datasets up to 1,000 rows.
- [ ] **Batch Processing:** Fuzzy matching runs as a background process to prevent the UI from freezing.
- [ ] **Resource Monitoring:** Ensure memory usage remains stable during heavy data ingestion.

---

## 🚀 Technical Sub-tasks for Developers
1. **Security:** Implement the `hashlib` logic in `backend/compliance.py`.
2. **Algorithms:** Develop the subset-sum algorithm for "Many-to-One" matching in `backend/engine.py`.
3. **Optimizations:** Refactor `load_data()` to use Parquet format if CSV performance bottlenecks are found.
4. **Mock Data:** Update `mock_data_maker.py` to include "Bulk Payment" scenarios where one bank row matches two invoice rows.
