# 🏁 Go-Live Checklist: SmartCash AI
> **Project:** SmartCash AI - Institutional Treasury Command  
> **Deployment Target:** Production (Streamlit Cloud / Enterprise VPC)  
> **Version:** `1.0.0` (Gold Master)  
> **Release Lead:** Saurabh Srivastav

---

## 📊 Deployment Progress: 0/6 Sections Complete

### 1. Data Integrity & Ingestion (Critical) 🛡️
- [ ] **Data Source Validation:** Map `data/invoices.csv` and `data/bank_feed.csv` to production feeds (Disconnect Mock Data).
- [ ] **Schema Integrity:** Verify `ESG_Score`, `Currency`, and `Invoice_ID` columns exist to prevent **Plotly Sunburst** crashes.
- [ ] **Encoding Check:** Confirm `UTF-8` encoding for all datasets to support multi-currency symbols (€, £, ₹).
- [ ] **Volume Testing:** Ensure ingestion logic handles >5,000 rows without session timeout.

### 2. Engine & Logic Verification ⚙️
- [ ] **Fuzzy Thresholds:** Set `thefuzz` match threshold to **90%** minimum to prevent false-positive clearing.
- [ ] **Stress Simulation:** Verify "Collection Latency" slider handles boundary values (0 and 100) without `ZeroDivisionError`.
- [ ] **GenAI Prompting:** Validate `GenAIAssistant` system instructions for professional dunning tone and legal compliance.
- [ ] **Model Fallback:** Ensure a secondary matching logic is active if the primary LLM API is unreachable.

### 3. Security & Governance (Audit-Ready) 🔒
- [ ] **SOC2 Vault Logging:** Verify `Hash_ID` generation and storage in the **Audit Ledger** for every match.
- [ ] **Secrets Management:** Confirm **ZERO** hardcoded keys in `main.py`. Use `st.secrets` or `.env`.
- [ ] **Asset Failover:** Implement `try-except` for all `st.image` calls to avoid broken UI components during demos.
- [ ] **PII Masking:** Ensure sensitive customer data is hashed or masked in the frontend view.

### 4. UI/UX & Visualization 🎨
- [ ] **Dark Mode Styling:** Verify CSS injection for `#0b0e14` background compatibility.
- [ ] **Responsive Risk Radar:** Test Sunburst charts on both Desktop (1920x1080) and Tablet resolutions.
- [ ] **Final Cleanup:** Purge all `print()` statements and `st.write()` debuggers.
- [ ] **Instructional Tooltips:** Verify all "Help" icons provide clear context for AR Analysts.

### 5. Infrastructure & Deployment 🚀
- [ ] **Requirements.txt:** Pin `thefuzz`, `scipy`, and `plotly` to specific stable versions.
- [ ] **Memory Management:** Monitor `st.cache_data` usage to stay within Streamlit Cloud RAM limits.
- [ ] **Pathing Logic:** Confirm `sys.path.append` correctly identifies the `/backend/` directory in the cloud environment.
- [ ] **SSL/HTTPS:** Confirm secure connection is active for the production URL.

### 6. Stakeholder Handover 🤝
- [ ] **Documentation:** Distribute `User_Guide_AR_Analyst.md` to the Treasury team.
- [ ] **UAT Sign-off:** Secure final approval from the **Treasury Lead** and **Compliance Officer**.
- [ ] **Support Buffer:** Establish a 48-hour "War Room" support channel for immediate post-launch issues.

---



## 🚀 Launch Status
- [ ] **GO** - *Ready for Production*
- [ ] **NO-GO** - *Remediation Required*

**Final Approval:** `____________________`  
**Timestamp:** `2026-01-31`
