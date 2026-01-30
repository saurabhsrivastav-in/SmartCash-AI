import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class GenAIAssistant:
    """
    The Intelligence Layer for SmartCash AI.
    Handles exception reasoning, dunning email generation, and 
    liquidity advice using LLM logic.
    """
    
    def __init__(self):
        # Initializing the client (Works with OpenAI or Gemini API)
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def reason_exception(self, bank_tx, top_candidates):
        """
        Sprint 3/6: Analyze why a match failed and suggest a fix.
        """
        if not self.client:
            return "AI Analysis unavailable: No API Key found."

        prompt = f"""
        As a Treasury Expert, analyze this reconciliation exception:
        Bank Transaction: {bank_tx}
        Top Potential Invoice Matches: {top_candidates}
        
        Identify the likely discrepancy (e.g., Bank Fee, Short-pay, Name Mismatch) 
        and suggest the next step for the AR Analyst.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a Senior Treasury Controller."},
                          {"role": "user", "content": prompt}],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI Logic Error: {str(e)}"

    def generate_dunning_email(self, customer_name, amount_due, invoice_id, esg_score):
        """
        Sprint 4: Generates a professional dunning email tailored 
        to the customer's ESG/Behavioral profile.
        """
        # Tailor tone based on ESG/Credit Risk
        tone = "collaborative" if esg_score in ['AA', 'A'] else "firm and formal"
        
        prompt = f"""
        Draft a {tone} email to {customer_name} regarding Invoice {invoice_id} 
        for the amount of {amount_due}. 
        The payment is slightly delayed. Maintain a professional treasury tone.
        """
        
        if not self.client:
            # Fallback local logic for offline demos
            return f"Subject: Payment Inquiry - {invoice_id}\n\nDear {customer_name},\n\nOur records indicate a balance of {amount_due} remains open. Please advise on the settlement status."

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except:
            return "Error generating email. Please use the fallback template."
