import pandas as pd
from fuzzywuzzy import fuzz

class SmartMatchingEngine:
    def __init__(self):
        self.trust_threshold = 0.95  # Sprint 10: Auto-post if >95% match

    def run_match(self, payment_amt, payer_name, invoice_df):
        """Processes incoming bank data against the open invoice ledger."""
        results = []
        
        for _, inv in invoice_df.iterrows():
            # 1. Exact Match Check (Sprint 1)
            amt_match = (payment_amt == inv['Amount'])
            
            # 2. Fuzzy Name Matching (Sprint 2)
            name_score = fuzz.token_sort_ratio(payer_name.lower(), inv['Customer'].lower()) / 100
            
            # 3. Decision Logic (Sprint 5: Strategic Optimization)
            if amt_match and name_score > 0.90:
                confidence = 1.0
                status = "Auto-Match"
            elif name_score > 0.70:
                confidence = name_score
                status = "Suggested"
            else:
                continue

            results.append({
                "Invoice_ID": inv['Invoice_ID'],
                "Customer": inv['Customer'],
                "confidence": confidence,
                "status": status
            })

        # Return matches sorted by highest confidence
        return sorted(results, key=lambda x: x['confidence'], reverse=True)
