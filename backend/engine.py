import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np
from datetime import datetime

class SmartMatchingEngine:
    def __init__(self):
        # Institutional Standards: STP requires > 95% confidence
        self.stp_threshold = 0.95
        self.manual_review_threshold = 0.70
        
        # --- Entity Alias Registry (Institutional Master Data) ---
        # Maps messy bank string variations to the canonical Master Data name
        self.alias_map = {
            "tsla motors gmbh": "Tesla Inc",
            "tesla giga-factory": "Tesla Inc",
            "tsla-motors-us": "Tesla Inc",
            "global blue (remit)": "Global Blue SE",
            "globel blue intl": "Global Blue SE",
            "techretail-europe": "Tech Retail Corp",
            "tech ret corp": "Tech Retail Corp",
            "eco energy syst": "Eco Energy Systems",
            "saurabh_software_ltd": "Saurabh Soft",
            "saurabh soft solutions": "Saurabh Soft"
        }

    def calculate_dso(self, invoice_df):
        """Metric Hook: Calculates Days Sales Outstanding (DSO)"""
        try:
            total_ar = invoice_df[invoice_df['Status'] == 'Open']['Amount'].sum()
            annual_sales = invoice_df['Amount'].sum()
            dso = (total_ar / annual_sales) * 365 if annual_sales > 0 else 0
            return round(dso, 1)
        except Exception:
            return 0.0

    def run_match(self, payment_amt, payer_name, currency, invoice_df):
        """
        Waterfall Matching Engine:
        1. Exact (Amount + Currency + Resolved Name)
        2. Fuzzy (Alias Mapping + Token Set Ratio)
        3. Exception (Partial/Short-pay logic)
        """
        try:
            results = []
            if invoice_df.empty:
                return []

            for _, inv in invoice_df.iterrows():
                # --- SPRINT 1: Exact Amount & Currency Logic (Weight: 0.50) ---
                inv_amt = float(inv['Amount'])
                pay_amt = float(payment_amt)
                
                amt_score = 0.0
                is_exact_amt = (pay_amt == inv_amt and currency == inv['Currency'])
                
                if is_exact_amt:
                    amt_score = 1.0
                # Bank fee tolerance (Fixed $5 or 0.1%)
                elif abs(pay_amt - inv_amt) <= max(5.0, 0.001 * inv_amt):
                    amt_score = 0.8 
                
                # --- SPRINT 2: Name Similarity & Alias Resolution (Weight: 0.40) ---
                clean_payer = str(payer_name).lower().strip()
                resolved_payer = self.alias_map.get(clean_payer, clean_payer)
                clean_customer = str(inv['Customer']).lower().strip()
                
                # Using token_set_ratio to handle reordered words (e.g. "Tesla Motors" vs "Motors Tesla")
                name_score = fuzz.token_set_ratio(resolved_payer, clean_customer) / 100

                # --- SPRINT 3: Partial Match/Short-Pay Logic (Weight: 0.10) ---
                # Bonus if the ID is mentioned or amount matches but name is "noisy"
                partial_match_bonus = 0.0
                status_note = ""
                
                if is_exact_amt and name_score < 0.5:
                    partial_match_bonus = 0.7 
                    status_note = " (Amount Matched, Name Discrepancy)"

                # --- Weighted Confidence Calculation ---
                total_confidence = (amt_score * 0.5) + (name_score * 0.4)
                
                if partial_match_bonus > total_confidence:
                    total_confidence = partial_match_bonus

                # --- Categorization Logic ---
                if total_confidence >= self.stp_threshold:
                    status = "STP: Automated"
                elif total_confidence >= self.manual_review_threshold:
                    status = f"EXCEPTION: High Confidence{status_note}"
                else:
                    status = "EXCEPTION: Investigation Required"

                # Filter out low-relevance results
                if total_confidence > 0.40: 
                    results.append({
                        "Invoice_ID": inv['Invoice_ID'],
                        "Customer": inv['Customer'],
                        "Currency": inv['Currency'],
                        "confidence": round(total_confidence, 2),
                        "status": status,
                        "esg_score": inv.get('ESG_Score', 'N/A'),
                        "due_date": str(inv.get('Due_Date', 'N/A'))
                    })

            return sorted(results, key=lambda x: x['confidence'], reverse=True)

        except Exception as e:
            print(f"Engine Fault: {e}")
            return []
