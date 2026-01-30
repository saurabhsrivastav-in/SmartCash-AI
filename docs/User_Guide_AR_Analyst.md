# 📘 AR Analyst User Guide: SmartCash AI

**System Role:** Accounts Receivable / Treasury Operations  
**Platform:** SmartCash AI - Institutional Treasury Command  
**Version:** 1.0.0  

---

## 1. Introduction
Welcome to **SmartCash AI**. This platform is designed to act as your "AI Co-Pilot," automating the repetitive data-entry tasks of bank reconciliation and allowing you to focus on high-value exception management and customer relations.

---

## 2. Navigating the Analyst Workbench
The **Analyst Workbench** is where you will spend most of your time. It is designed to handle transactions that require a "human-in-the-loop" review.

### 2.1 Step 1: Selecting a Transaction
The system automatically pulls the latest intraday bank feed. 
1. Navigate to **Analyst Workbench** via the sidebar.
2. View the **Bank Feed Table** to see incoming credits.
3. Use the **Focus Item** dropdown to select a specific transaction for review.

### 2.2 Step 2: Running the Match Engine
Once a transaction is selected, click **"Run Multi-Factor Match Engine"**. The system will compare the bank data against open invoices using three logic gates:

| Match Type | Confidence | System Action |
| :--- | :--- | :--- |
| **Exact Match** | 100% | Auto-posts and triggers success balloons. |
| **Fuzzy Match** | 90% - 99% | Asks for analyst confirmation. |
| **Exception** | < 90% | Triggers the GenAI Dispute Agent. |



---

## 3. Managing Exceptions & Disputes
When the system cannot find a high-confidence match (due to missing Invoice IDs or "short-pays"), it enters **Exception Mode**.

### 3.1 AI Remittance Request
If a match is below 90% confidence:
1. The system will display a **Warning** message.
2. The **GenAI Assistant** will automatically draft an email tailored to that specific customer.
3. **Action:** Review the draft, copy it, and send it to the customer's AP department to request a remittance advice.

### 3.2 Handling Short-Payments
If the `Amount_Received` is less than the `Invoice_Amount`, the system will flag the variance. You can then use the dashboard metrics to determine if the difference is a bank fee or a formal dispute.

---

## 4. Monitoring Risk & DSO
Analysts are responsible for maintaining the health of the A/R aging. 

* **Check the Executive Dashboard:** Monitor the **Adjusted DSO**. If it increases, it means collections are slowing down.
* **Review the Risk Radar:** Use the Sunburst chart to identify which currencies or customers (with low ESG scores) are causing the highest liquidity concentration.



---

## 5. Compliance & The Audit Ledger
Every action you take—whether confirming an AI suggestion or clearing a transaction—is logged in the **Audit Ledger**.

1. Navigate to **Audit Ledger**.
2. Verify your recent postings.
3. Note the **Hash_ID**: This is a unique digital fingerprint used for SOC2 compliance audits; you do not need to edit this.

---

## 6. Pro-Tips for Peak Efficiency
* **Sidebar Controls:** Use the **Collection Latency** slider during team meetings to show the "What-If" impact of payment delays.
* **Ballon Confirmation:** When you see balloons, the transaction has been successfully logged to the vault and is ready for ERP upload.
* **Refresh Regularly:** Use the browser refresh to pull the latest data if the `invoices.csv` file has been updated by the IT team.

---

## 7. Troubleshooting
* **Missing Invoices:** If an invoice isn't appearing, ensure the `Status` in the source data is set to 'Open'.
* **Broken Images:** If you see a broken icon, check your internet connection; the system includes a failover, but high-latency networks may occasionally block the visual assets.

---
**Need Support?** Contact the Treasury IT Helpdesk or refer to the [Technical Documentation](../docs/PRD.md).
