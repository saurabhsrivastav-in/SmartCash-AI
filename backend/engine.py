import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np
from datetime import datetime

class SmartMatchingEngine:
    def __init__(self):
        # Institutional Standards: STP (Straight Through Processing) requires > 95% confidence
        self.stp_threshold = 0.95
        self.manual_review_threshold = 0.70
        
        # Entity Alias Registry (Master Data Management simulation)
        self.alias_map = {
            "tesla motors": "Tesla Inc",
            "tesla gmbh": "Tesla Inc",
            "google ireland": "Alphabet Inc",
            "saurabh softwares": "Saurabh Soft"
        }

    def calculate_dso(self, invoice_df):
        """
        Metric Hook: Calculates Days Sales Outstanding (DSO).
        Formula: (Accounts Receivable / Total Credit Sales) * Number of Days
        """
        try:
            total_ar = invoice_df['Amount'].sum()
            # For demo purposes, we assume 'Amount' represents current AR
            # and simulate a 365-day period with a 20% higher sales volume
            annual_sales = total_ar * 1.2 
            dso = (total_ar / annual_sales) * 365
            return round(dso, 1)
        except Exception:
            return 0.0

    def run_match(self, payment_amt, payer_name, currency, invoice_df):
        """
        Institutional-grade matching using a weighted decision matrix.
        Includes a 'Partial Match' flag for amounts that align without clear IDs.
        """
        try:
            results = []
            if invoice_df.empty:
                return []

            for _, inv in invoice_df.iterrows():
                # --- 1. Amount & Currency Logic (Weight: 0.50) ---
                inv_amt = float(inv['Amount'])
                pay_amt = float(payment_amt)
                
                amt_score = 0.0
                is_exact_amt = False
                
                if pay_amt == inv_amt and currency == inv['Currency']:
                    amt_score = 1.0
                    is_exact_amt = True
                elif abs(pay_amt - inv_amt) <= max(5.0, 0.001 * inv_amt):
                    amt_score = 0.8  # Probable match considering bank fees
                
                # --- 2. Entity Alias Resolution (Weight: 0.40) ---
                clean_payer = str(payer_name).lower().strip()
                resolved_payer = self.alias_map.get(clean_payer, clean_payer)
                clean_customer = str(inv['Customer']).lower().strip()
                
                name_score = fuzz.token_set_ratio(resolved_payer, clean_customer) / 100

                # --- 3. Partial Match & Strategic Logic (Weight: 0.10) ---
                # NEW: If amount matches but name confidence is low, flag as Partial
                partial_match_bonus = 0.0
                status_note = ""
                
                if is_exact_amt and name_score < 0.5:
                    partial_match_bonus = 0.7 # Force a 0.7 confidence for investigation
                    status_note = " (Partial Match: Amount Alignment)"

                # --- 4. Weighted Confidence Calculation ---
                total_confidence = (amt_score * 0.5) + (name_score * 0.4)
                
                # Override if Partial Match logic triggers
                if partial_match_bonus > total_confidence:
                    total_confidence = partial_match_bonus

                # --- 5. Categorization Logic ---
                if total_confidence >= self.stp_threshold:
                    status = "STP: Automated"
                elif total_confidence >= self.manual_review_threshold:
                    status = f"EXCEPTION: High Confidence{status_note}"
                else:
                    status = "EXCEPTION: Investigation Required"

                if total_confidence > 0.40:  # Noise filter
                    results.append({
                        "Invoice_ID": inv['Invoice_ID'],
                        "Customer": inv['Customer'],
                        "Currency": inv['Currency'],
                        "confidence": round(total_confidence, 2),
                        "status": status,
                        "esg_score": inv.get('ESG_Score', 'N/A'),
                        "due_date": inv.get('Due_Date', 'N/A')
                    })

            # Rank by institutional confidence
            return sorted(results, key=lambda x: x['confidence'], reverse=True)

        except Exception as e:
            print(f"Engine Fault: {e}")
            return []
