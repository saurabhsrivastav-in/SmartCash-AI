# 🚀 Release Notes: SmartCash AI
> **Current Version:** `v1.0.0-gold`  
> **Release Date:** January 31, 2026  
> **Status:** Production Ready / Live Demo

---

## [1.0.0] - 2026-01-31
### "The Institutional Foundation"
This is the first major release of the SmartCash AI Treasury Engine, focusing on the core "Order-to-Cash" automation bridge.

### ✨ Key Features
* **Waterfall Matching Engine:** Implementation of tiered heuristic matching using `thefuzz`.
    * *Exact Match:* Automatic clearing for high-confidence ID/Amount pairings.
    * *Fuzzy Match:* AI-driven suggestions for misspelled or truncated payer names.
* **GenAI Exception Assistant:** Integrated LLM agent to analyze variances and draft professional remittance request emails.
* **Risk Radar Dashboard:** Real-time **Plotly Sunburst** visualization for multi-level risk analysis (Currency > Customer > ESG).
* **SOC2 Compliance Vault:** Every transaction now generates an immutable `Hash_ID` logged for audit traceability.
* **Liquidity Stress Simulator:** A `NumPy`-powered slider allowing Treasury leads to model the impact of collection delays on cash positions.



### 🛠️ Technical Improvements
* **FastAPI Backend:** Migrated core logic to an asynchronous FastAPI structure for better scalability.
* **State Management:** Optimized Streamlit session states and implemented `st.cache_data` for handling large A/R ledger uploads.
* **Input Sanitization:** Added UTF-8 enforcement and regex-based cleaning for "noisy" bank remittance text strings.

### 🐞 Bug Fixes
* Fixed a `ZeroDivisionError` in the Treasury Stress simulation when latency was set to zero.
* Resolved a CSS injection bug where metric cards were unreadable in certain browser "Light Mode" settings.
* Corrected the "double time" typo in the user interface description box.

---

## [0.9.0-beta] - 2025-12-15
### "The Proof of Concept"
* Initial prototype of the Streamlit frontend.
* Basic CSV upload functionality for bank feeds.
* First iteration of the Levenshtein-based matching logic.

---

## 📈 Roadmap (What's Next?)
* **v1.1.0:** Direct API Connectors for SAP S/4HANA.
* **v1.2.0:** Multi-entity "Intercompany" reconciliation logic.
* **v2.0.0:** Predictive Payer Behavior models using `SciPy` and `Prophet`.

---
**Build:** `2026.01.31.release_v1`  
**Lead:** [Saurabh Srivastav](https://github.com/saurabhsrivastav-in)
