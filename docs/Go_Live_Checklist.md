# 🚀 Go-Live Checklist: SmartCash AI

**Project:** SmartCash AI Automation Deployment  
**Release Version:** v1.0.0 (Global Enterprise Edition)  
**Deployment Date:** January 2026  
**Owner:** Saurabh Srivastav, Product Manager  

---

## 1. Pre-Deployment (T-minus 72 Hours)
Ensure the foundation is stable before the final cutover.

- [ ] **Data Sanitization:** Verify all "Test/Dummy" data is purged from the production database.
- [ ] **Infrastructure Freeze:** No further code changes to the Main branch.
- [ ] **Environment Sync:** Confirm Production environment variables match Staging (API Keys, Endpoints).
- [ ] **Backup Verification:** Perform a full backup of the existing SAP AR tables and the SmartCash DB.

---

## 2. Technical Cutover (T-minus 24 Hours)
The "Heavy Lifting" of system integration.

- [ ] **SFTP Connectivity:** Final handshake test between the Bank’s SFTP and Treasury IT.
- [ ] **API Key Rotation:** Rotate all temporary UAT keys to Production-grade Secret Keys.
- [ ] **SSL/TLS & Security:** Verify that the `https://` certificate for the Vendor Portal is active and PQC encryption is enabled.
- [ ] **Load Balancing:** Confirm the cloud environment is configured to auto-scale for the first 48 hours of high-volume ingestion.



---

## 3. Production Launch (Day 0: Go-Live)
The sequence of events for the launch window.

### Phase A: Data Ingestion (09:00 AM)
- [ ] **MT942 Trigger:** Activate the first intraday bank file ingestion.
- [ ] **OCR Engine:** Start the email listener for the Centralized Remittance Mailbox.
- [ ] **SAP Sync:** Initialize the full pull of Open Items (Receivables) into the SmartCash matching pool.

### Phase B: Processing & Matching (11:00 AM)
- [ ] **The "First Run":** Monitor the first 100 transactions for STP (Straight-Through Processing) accuracy.
- [ ] **Fuzzy Logic Check:** Verify that "Scenario B" (Bulk) and "Scenario C" (Part-pay) logic gates are firing correctly.
- [ ] **Write-back Activation:** Enable the BAPI connector to post the first batch of "Auto-Matches" to the GL.



---

## 4. Organizational Readiness
The human element of the transition.

- [ ] **User Training:** Confirm all AR Analysts have completed the "Analyst Workbench" certification.
- [ ] **Support Desk:** Ensure the IT Support team has the "SmartCash Troubleshooting Guide" and escalation contacts.
- [ ] **Vendor Portal Launch:** Send the "Welcome & Registration" emails to the Top 50 high-volume customers.

---

## 5. Post-Launch Monitoring (T-plus 48 Hours)
Hyper-care period for the first two business days.

- [ ] **Hourly Status Reports:** Send an automated summary of "Processed vs. Exceptions" to the Project Steering Committee.
- [ ] **Latency Audit:** Verify the Dashboard response time remains <2.0s under full load.
- [ ] **Audit Trail Integrity:** Confirm the Hashed Audit Log (Sprint 9) is recording every transaction without gaps.

---

## 6. Contingency / Rollback Plan
In the event of a "Critical" failure during cutover.

| Trigger Event | Action | Responsibility |
| :--- | :--- | :--- |
| **SAP Posting Failure** | Disable SAP Write-back; revert to manual GL entry via legacy CSV export. | SAP IT Lead |
| **MT942 Data Corruption** | Roll back to the previous day’s bank file and re-run ingestion. | Treasury IT |
| **System Downtime > 1hr** | Redirect all users to the "Read-Only" legacy AR report. | DevOps |

---

### Final Go/No-Go Approval

| Authority | Decision | Signature | Time |
| :--- | :--- | :--- | :--- |
| **Saurabh Srivastav** | [ ] GO [ ] NO-GO | ________________ | ________ |
| **Technical Lead** | [ ] GO [ ] NO-GO | ________________ | ________ |
| **Operations VP** | [ ] GO [ ] NO-GO | ________________ | ________ |
