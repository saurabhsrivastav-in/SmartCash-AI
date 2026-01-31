# 📘 User Guide: AR Analyst Workbench
> **Product:** SmartCash AI  
> **Module:** Treasury Automation & Cash Application  
> **Version:** 1.0.0

---

## 1. Introduction
Welcome to **SmartCash AI**. This platform is designed to act as your "Digital Assistant," handling the repetitive manual matching of bank statements to invoices so you can focus on high-value exception management and financial strategy.

---

## 2. Getting Started
### 2.1 Accessing the Dashboard
1.  Navigate to the [SmartCash AI Live Link](https://smartcash-ai-cgumahyfurnnel8ocgbya5.streamlit.app/).
2.  Ensure your **Dark Mode** is enabled in browser settings for the optimal "Command Center" experience.

### 2.2 Data Ingestion
To start a reconciliation cycle, upload your latest data files via the sidebar:
* **Invoices (A/R Ledger):** Upload your `invoices.csv` containing open balances.
* **Bank Feed (MT942/CAMT):** Upload the daily bank credit statement.

---

## 3. Interpreting the "Risk Radar"
The **Sunburst Chart** on the main dashboard represents your global liquidity risk.



* **Inner Ring (Currency):** Shows concentration of cash (USD, EUR, etc.).
* **Middle Ring (Customer):** Identifies which accounts hold the most open debt.
* **Outer Ring (ESG):** Visualizes the ESG risk score of your payers—critical for institutional compliance.

---

## 4. The Matching Workflow
The engine automatically categorizes every transaction into three buckets:

### ✅ Bucket A: Auto-Matched (STP)
* **Status:** Green
* **Action:** None required. The system found a 95%+ match. These are queued for automatic ERP upload.

### ⚠️ Bucket B: AI Suggestions (Manual Review)
* **Status:** Amber
* **Action:** Review the **Confidence Score**. 
    * If the Payer Name is slightly misspelled (e.g., "Saurabh Srivastav Inc" vs "S. Srivastav"), click **"Confirm Match."**
    * The system uses `thefuzz` logic to highlight exactly where the strings differ.

### ❌ Bucket C: Exceptions (GenAI Required)
* **Status:** Red
* **Action:** Click the **"Generate Remittance Request"** button.
    * The **GenAIAssistant** will read the transaction details and draft an email to the client asking for missing invoice numbers.
    * Review the draft and click **"Send Email."**

---

## 5. Liquidity Stress Testing
As an analyst, you can model "What-If" scenarios for the CFO:
1.  Locate the **Collection Latency Slider**.
2.  Adjust the days (e.g., move from 0 to 30 days).
3.  Observe the **Waterfall Chart** to see how delayed payments impact the company's "Free Cash Flow" in real-time.

---

## 6. Audit & Compliance
Every action you take (including manual overrides) is logged.
* To view the audit trail, go to the **Audit Ledger** tab.
* Each entry has a unique **Hash_ID**, ensuring that no one can alter the record of who matched which invoice and when.

---

## 7. Troubleshooting & FAQ
**Q: Why is my CSV not uploading?** A: Ensure the file is `UTF-8` encoded and contains the mandatory columns: `Invoice_ID`, `Amount`, and `Customer_Name`.

**Q: The AI suggestion is wrong. What do I do?** A: Click **"Reject Match."** This prevents the transaction from being cleared and moves it to the manual investigation queue.

---
**Support:** For technical issues, please open a ticket in the [GitHub Issues](https://github.com/saurabhsrivastav-in/SmartCash-AI/issues) repository.
