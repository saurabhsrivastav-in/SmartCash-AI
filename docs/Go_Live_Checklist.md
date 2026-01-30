# 🏁 Go-Live Checklist: SmartCash AI

**Project:** SmartCash AI - Institutional Treasury Command  
**Deployment Target:** Production Environment (Streamlit Cloud / Enterprise VPC)  
**Version:** 1.0.0 (Gold Master)  
**Release Lead:** Saurabh Srivastav  

---

## 1. Data Integrity & Ingestion (Critical)
* [ ] **Data Source Validation:** Ensure `data/invoices.csv` and `data/bank_feed.csv` are mapped to live production feeds rather than mock data.
* [ ] **Schema Check:** Verify all required columns (`ESG_Score`, `Currency`, `Invoice_ID`) exist to prevent Plotly Sunburst rendering failures.
* [ ] **Encoding:** Confirm all CSV files are encoded in `UTF-8` to handle multi-currency symbols (e.g., €, £, ₹).

---

## 2. Engine & Logic Verification
* [ ] **Fuzzy Thresholds:** Validate that the `thefuzz` match threshold is set to a minimum of **90%** to minimize false positives in automated clearing.
* [ ] **Stress Simulation:** Test the "Collection Latency" slider to ensure it doesn't cause `ZeroDivisionError` in the waterfall calculations.
* [ ] **GenAI Prompting:** Confirm the `GenAIAssistant` is utilizing the latest system instructions for professional dunning correspondence.



---

## 3. Security & Governance (Audit-Ready)
* [ ] **SOC2 Vault Logging:** Perform a test match and verify the `Hash_ID` is generated and saved in the `Audit Ledger`.
* [ ] **Secrets Management:** Ensure no API keys or database credentials are hardcoded in `main.py` (Use `st.secrets` or `.env`).
* [ ] **Asset Failover:** Verify that `st.image` calls have the `try-except` failover implemented to prevent "broken image" icons during stakeholder demos.

---

## 4. UI/UX & Visualization
* [ ] **Dark Mode Styling:** Verify the custom CSS injects correctly, ensuring metrics are legible against the `#0b0e14` background.
* [ ] **Responsive Design:** Test the **Risk Radar** Sunburst chart on multiple screen sizes (Tablet vs. Desktop) for readability.
* [ ] **Final Cleanup:** Remove all print statements and developer `st.write()` debuggers from the code.



---

## 5. Infrastructure & Deployment
* [ ] **Requirements.txt:** Confirm all libraries (`thefuzz`, `scipy`, `plotly`) are pinned to stable versions to avoid deployment drift.
* [ ] **Resource Limits:** Ensure the Streamlit Cloud instance has sufficient memory (RAM) to handle the `st.cache_data` load for large invoice datasets.
* [ ] **Pathing:** Verify `sys.path.append` logic is correctly pointing to the `backend/` directory for cloud execution.

---

## 6. Stakeholder Handover
* [ ] **User Guide:** Distribute the `User_Guide_AR_Analyst.md` to the operations team.
* [ ] **UAT Sign-off:** Confirm final approval from the Treasury Lead and Compliance Officer.
* [ ] **Emergency Contact:** Establish a "War Room" contact for the first 48 hours post-deployment.

---

### 🚀 Launch Status: [ ] GO | [ ] NO-GO

**Final Approval:** ____________________ **Date:** __________
