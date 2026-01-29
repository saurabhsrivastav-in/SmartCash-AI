class GenAIAssistant:
    def generate_email(self, customer_name, amount_received):
        """Sprint 6: LLM-powered response for unmatched payments."""
        prompt = f"""
        Subject: Action Required: Payment Clarification for {customer_name}
        
        Dear Finance Team at {customer_name},
        
        We have received your payment of ${amount_received}. However, our 
        SmartCash AI engine could not find an exact invoice match. 
        
        Please provide the remittance advice to ensure this is applied correctly.
        
        Regards,
        Autonomous Treasury Bot
        """
        return prompt
