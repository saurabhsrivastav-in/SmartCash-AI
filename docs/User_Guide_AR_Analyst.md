# 📘 User Guide: SmartCash AI Analyst Workbench
**Version:** 1.0 (Production)  
**Target Audience:** Accounts Receivable Analysts & Credit Managers

---

## 1. Getting Started
The SmartCash AI Dashboard is your mission control for daily cash application. The system handles **85% of matches automatically**, leaving you to focus only on high-value exceptions and complex customer disputes.

### Accessing the Dashboard
1. Log in via Single Sign-On (SSO).
2. Ensure your **Company Code** and **Region** are selected in the top-right filter.
3. The dashboard refreshes **4x daily** following the MT942 bank feed cycles.

---

## 2. Navigating the "Smart Worklist"
The worklist is not a "first-in-first-out" list. It is an **AI-Prioritized Queue**.



* **Priority Score:** High-value invoices and "At-Risk" customers are pushed to the top.
* **Status Badges:**
    * 🟢 **Auto-Matched:** Already posted to SAP (View only).
    * 🟡 **Suggested:** AI found a match with >85% confidence. Needs your 1-click approval.
    * 🔴 **Exception:** No match found. Requires manual investigation.

---

## 3. Resolving a "Suggested Match"
When the AI finds a potential match (Scenario B), follow these steps:

1. Click on the **Yellow Badge** to open the "Comparison View."
2. **Review Side-by-Side:** The left panel shows the Bank Remittance; the right panel shows the Open SAP Invoices.
3. **Verify:** Check if the Invoice Number and Payer Name align.
4. **Action:** Click **[Confirm & Post]**. The system will immediately trigger the SAP BAPI to clear the record.

---

## 4. Handling Short-Payments & Deductions
If a customer pays less than the invoice amount (Scenario C):

1. Select the transaction and click **[Action: Code Deduction]**.
2. **Variance Analysis:** The system calculates the difference automatically.
3. **Reason Coding:** Select the appropriate **ZF Code** from the dropdown (e.g., *ZF01 - Damaged Goods*, *ZF05 - Pricing Dispute*).
4. **Attach Evidence:** Drag and drop the customer's debit memo or email directly into the portal.
5. Click **[Post with Deduction]**.



---

## 5. Using the AI Email Assistant
For unresolved exceptions (Scenario D), use the built-in **GenAI Drafter**:

1. Click the **[Draft Email]** button on any Unmatched record.
2. The AI will generate a polite inquiry including the specific Invoice ID and the missing amount.
3. Review the text, click **[Send]**, and the system will automatically set a "Follow-up" reminder for 48 hours.

---

## 6. Pro-Tips for Power Users
* **Bulk Approval:** You can select multiple "Suggested" matches and approve them in one click if the confidence score is >95%.
* **Search Filter:** Use the `Ref:` prefix to search by Bank Reference ID or `Inv:` for SAP Invoice numbers.
* **Export:** Use the **[Export to Excel]** button for your weekly team huddle to show your "Resolution Rate."

---

## 7. Troubleshooting & Support
* **Missing Payment?** Ensure the Bank has sent the MT942 for the current cycle.
* **SAP Error?** Check the "Sync Status" tab; it usually means the invoice is currently "Locked" by another user in SAP.
* **Support:** Raise a ticket via the **Help** button or contact the SmartCash IT team at `support.smartcash@company.com`.

---
