import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np
from datetime import datetime

class SmartMatchingEngine:
    def __init__(self):
        # Institutional Standards: STP (Straight Through Processing) requires > 95% confidence
        self.stp_threshold = 0.95
        self.manual_review_threshold = 0.70
        
        # --- UPDATED: Entity Alias Registry (Institutional Master Data) ---
        # Maps messy bank string variations to the canonical Master Data name
        self.alias_map = {
            # Tesla Variations
            "tsla motors gmbh": "Tesla Inc",
            "tesla giga-factory": "Tesla Inc",
            "tsla-motors-us": "Tesla Inc",
            "tesla inc /bnf/": "Tesla Inc",
            "tsla-us-motors": "Tesla Inc",
            
            # Global Blue Variations
            "global blue (remit)": "Global Blue SE",
            "global-blue-fr": "Global Blue SE",
            "globel blue intl": "Global Blue SE",
            "gbl blue se": "Global Blue SE",
            "global blue group": "Global Blue SE",
            
            # Tech Retail Variations
            "techretail-europe": "Tech Retail Corp",
            "tech retail (uk)": "Tech Retail Corp",
            "tech retail corp.": "Tech Retail Corp",
            "tech ret corp": "Tech Retail Corp",
            "techretail-apac": "Tech Retail Corp",
            
            # Eco Energy Variations
            "eco energy syst": "Eco Energy Systems",
            "eco nrg na": "Eco Energy Systems",
            "eco energy inc": "Eco Energy Systems",
            "eco-nrg": "Eco Energy Systems",
            
            # Saurabh Soft Variations
            "saurabh_software_ltd": "Saurabh Soft",
            "saurabh soft solutions": "Saurabh Soft",
            "saurabh_software_uk": "Saurabh Soft",
            "saurabh softwares": "Saurabh Soft"
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
        Institutional-grade matching using a weighted decision matrix.
        Weights: Amount/Currency (50%), Name Fuzzy Match (40%), Partial Logic (10%)
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
                
                # Check for exact matches
                if pay_amt == inv_amt and currency == inv['Currency']:
                    amt_score = 1.0
                    is_exact_amt = True
                # Check for bank fee tolerance (Fixed $5 or 0.1%)
                elif abs(pay_amt - inv_amt) <= max(5.0, 0.001 * inv_amt):
                    amt_score = 0.8 
                
                # --- 2. Entity Alias Resolution (Weight: 0.40) ---
                clean_payer = str(payer_name).lower().strip()
                # Resolve using alias_map; fallback to the original name if not found
                resolved_payer = self.alias_map.get(clean_payer, clean_payer)
                clean_customer = str(inv['Customer']).lower().strip()
                
                # Use token_set_ratio to handle word reordering (e.g., "Motors Tesla")
                name_score = fuzz.token_set_ratio(resolved_payer, clean_customer) / 100

                # --- 3. Partial Match & Strategic Logic (Weight: 0.10) ---
                partial_match_bonus = 0.0
                status_note = ""
                
                # If amount is perfect but name is messy, force into manual review
                if is_exact_amt and name_score < 0.5:
                    partial_match_bonus = 0.7 
                    status_note = " (Partial Match: Amount Alignment)"

                # --- 4. Weighted Confidence Calculation ---
                total_confidence = (amt_score * 0.5) + (name_score * 0.4)
                
                if partial_match_bonus > total_confidence:
                    total_confidence = partial_match_bonus

                # --- 5. Categorization Logic ---
                if total_confidence >= self.stp_threshold:
                    status = "STP: Automated"
                elif total_confidence >= self.manual_review_threshold:
                    status = f"EXCEPTION: High Confidence{status_note}"
                else:
                    status = "EXCEPTION: Investigation Required"

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
