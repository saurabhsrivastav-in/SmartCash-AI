import datetime

class GenAIAssistant:
    """
    The Cognitive Layer of SmartCash AI.
    Handles autonomous correspondence, reason-code prediction, 
    and executive risk summarization.
    """
    def __init__(self, model_provider="Gemini-3-Flash"):
        self.model_provider = model_provider
        self.bank_name = "SmartCash Institutional Treasury"
        # In a production environment, you would initialize your LLM client here
        # self.client = initialize_llm(model_provider)

    def generate_email(self, customer_name, amount_received, invoice_data=None):
        """
        Orchestrates email generation using 'Finance-Specific' context.
        Incorporates logic for Short-Pays, Over-payments, and FX Variances.
        """
        invoice_data = invoice_data or {}
        expected_amt = invoice_data.get('Amount', amount_received)
        currency = invoice_data.get('Currency', 'USD')
        variance = expected_amt - amount_received
        
        # Determine the "Persona" and "Scenario"
        if abs(variance) < 0.01:
            return self._compose_standard_receipt(customer_name, amount_received, currency)
        
        elif variance > 0:
            # Short-Pay Logic (Sprint 3 & 6)
            return self._compose_exception_email(
                customer_name, amount_received, expected_amt, variance, currency, "SHORT_PAY"
            )
        
        else:
            # Over-payment Logic
            return self._compose_exception_email(
                customer_name, amount_received, expected_amt, abs(variance), currency, "OVER_PAY"
            )

    def _compose_exception_email(self, customer, received, expected, diff, curr, scenario):
        """
        Uses a Reasoning-first approach to draft professional dunning.
        """
        today = datetime.date.today().strftime("%b %d, %Y")
        
        subject_lines = {
            "SHORT_PAY": f"REMITTANCE VARIANCE: Action Required | {customer} | {today}",
            "OVER_PAY": f"OVERPAYMENT NOTICE: Reconciliation Required | {customer} | {today}"
        }
        
        # Logic for 'Cognitive' Context
        reasoning = "unidentified deduction" if scenario == "SHORT_PAY" else "excess liquidity"
        
        body = f"""
Subject: {subject_lines.get(scenario)}

Dear Accounts Payable Team at {customer},

Our automated reconciliation engine has processed your recent remittance of {curr} {received:,.2f}. 

Upon comparison with our ERP records (Invoice Value: {curr} {expected:,.2f}), we have identified a variance of {curr} {diff:,.2f} labeled as an {reasoning}.

**Institutional Governance Requirements:**
To ensure non-repudiation and maintain your current credit standing, please provide one of the following via our secure portal:
1. A valid Reason Code for the deduction (e.g., Bank Fees, Tax Withholding, or Dispute).
2. A remittance advice PDF for manual mapping by our AI agent.

If this variance was intentional (e.g., partial settlement), please confirm so we may update your DSO (Days Sales Outstanding) forecast accordingly.

Regards,

The Treasury Operations Team
{self.bank_name}
[Verified via SmartCash AI Compliance Vault]
"""
        return body

    def _compose_standard_receipt(self, customer, received, curr):
        return f"Subject: Payment Confirmation - {self.bank_name}\n\nDear {customer},\n\nYour payment of {curr} {received:,.2f} has been matched and posted with 100% confidence. No further action is required."

    def generate_risk_briefing(self, customer_name, esg_score, exposure_amt, behavior_profile):
        """
        Sprint 7/8: Generates an AI-driven briefing based on behavioral profiles.
        """
        # Mapping profiles to executive language
        profile_descriptions = {
            "Laggard": "exhibits habitual payment delays beyond 15 days.",
            "Early Bird": "demonstrates high-liquidity reliability.",
            "Strategic": "matches payments to specific discount windows."
        }
        
        desc = profile_descriptions.get(behavior_profile, "shows inconsistent payment patterns.")
        
        briefing = f"""
        EXECUTIVE SUMMARY: Counterparty Risk Assessment
        -----------------------------------------------
        Entity: {customer_name} | ESG Rating: {esg_score}
        Behavioral Profile: {behavior_profile} ({desc})
        Current Exposure: ${exposure_amt:,.2f}
        
        AI ANALYSIS:
        The combination of a '{esg_score}' rating and '{behavior_profile}' behavior suggests a 
        volatility risk in the next 30-day liquidity window. 
        
        RECOMMENDATION:
        1. Increase the 'Stress Haircut' for this entity by 12% in the Waterfall Model.
        2. Hold future order releases if 'Net Exposure' exceeds ${exposure_amt * 0.8:,.0f}.
        """
        return briefing
