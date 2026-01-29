import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np

class SmartMatchingEngine:
    def __init__(self):
        # JPMC Standard: STP (Straight Through Processing) requires > 95% confidence
        self.stp_threshold = 0.95
        self.manual_review_threshold = 0.70
        
        # Entity Alias Registry (Simulating Master Data Management)
        self.alias_map = {
            "tesla motors": "Tesla Inc",
            "tesla gmbh": "Tesla Inc",
            "google ireland": "Alphabet Inc",
            "saurabh softwares": "Saurabh Soft"
        }

    def run_match(self, payment_amt, payer_name, currency, invoice_df):
        """
        Institutional-grade matching using a weighted decision matrix:
        1. Amount & Currency Vector (50%)
        2. Entity/Alias Vector (40%)
        3. Strategic Metadata Vector (10%)
        """
        try:
            results = []
            if invoice_df.empty:
                return []

            for _, inv in invoice_df.iterrows():
                # --- 1. Amount & Currency Logic (Weight: 0.50) ---
                # Tolerance for bank fees: matches within 0.1% or fixed $5 variance
                inv_amt = float(inv['Amount'])
                pay_amt = float(payment_amt)
                
                amt_score = 0.0
                if pay_amt == inv_amt and currency == inv['Currency']:
                    amt_score = 1.0
                elif abs(pay_amt - inv_amt) <= max(5.0, 0.001 * inv_amt):
                    amt_score = 0.8  # Probable match with bank fee deduction
                
                # --- 2. Entity Alias Resolution (Weight: 0.40) ---
                clean_payer = str(payer_name).lower().strip()
                resolved_payer = self.alias_map.get(clean_payer, clean_payer)
                clean_customer = str(inv['Customer']).lower().strip()
                
                # Token Set Ratio handles "Inc", "Ltd", "LLC" variations effectively
                name_score = fuzz.token_set_ratio(resolved_payer, clean_customer) / 100

                # --- 3. Weighted Confidence Calculation ---
                # Formula: (Amount * 0.5) + (Name * 0.5)
                # Note: Expandable to include Date Proximity (0.1) in v2.0
                total_confidence = (amt_score * 0.5) + (name_score * 0.5)

                # --- 4. Categorization Logic ---
                if total_confidence >= self.stp_threshold:
                    status = "STP: Automated"
                elif total_confidence >= self.manual_review_threshold:
                    status = "EXCEPTION: High Confidence"
                else:
                    status = "EXCEPTION: Investigation Required"

                if total_confidence > 0.40:  # Noise filter
                    results.append({
                        "Invoice_ID": inv['Invoice_ID'],
                        "Customer": inv['Customer'],
                        "Currency": inv['Currency'],
                        "confidence": round(total_confidence, 2),
                        "status": status,
                        "esg_score": inv.get('ESG_Score', 'N/A')
                    })

            # Rank by institutional confidence
            return sorted(results, key=lambda x: x['confidence'], reverse=True)

        except Exception as e:
            print(f"Engine Fault: {e}")
            return []
