import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np
from datetime import datetime

class SmartMatchingEngine:
    def __init__(self):
        """
        Institutional Grade Matching Engine Configuration.
        STP (Straight-Through Processing) requires high confidence (>95%).
        """
        self.stp_threshold = 0.95
        self.manual_review_threshold = 0.70
        
        # --- Entity Alias Registry (Institutional Master Data) ---
        # Maps varied bank strings to canonical ERP Master Data names
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
        """
        Metric Hook: Calculates Days Sales Outstanding (DSO).
        Standard Formula: (Net AR / Total Sales) * 365
        """
        try:
            if invoice_df.empty:
                return 0.0
            
            # Filter for unpaid invoices
            open_inv = invoice_df[invoice_df['Status'] == 'Open']
            ar_balance = open_inv['Amount'].sum()
            total_sales = invoice_df['Amount'].sum()
            
            dso = (ar_balance / total_sales) * 365 if total_sales > 0 else 0
            return round(dso, 1)
        except Exception:
            return 0.0

    def run_match(self, payment_amt, payer_name, currency, invoice_df):
        """
        Waterfall Matching Logic:
        1. Exact Match: Amount + Currency + Resolved Identity.
        2. Fuzzy Match: Uses 'thefuzz' for name similarity.
        3. Exception Logic: Handles Bank Fees & Short-pays.
        """
        try:
            results = []
            if invoice_df.empty:
                return []

            # Standardize Payer Name from Bank Feed
            clean_payer = str(payer_name).lower().strip()
            resolved_payer = self.alias_map.get(clean_payer, clean_payer)

            for _, inv in invoice_df.iterrows():
                # --- SPRINT 1: Exact Amount & Currency Logic (Weight: 0.50) ---
                inv_amt = float(inv['Amount'])
                pay_amt = float(payment_amt)
                
                amt_score = 0.0
                is_exact_amt = (pay_amt == inv_amt and currency == inv['Currency'])
                
                if is_exact_amt:
                    amt_score = 1.0
                # Sprint 3: Bank fee tolerance (Fixed $5 or 0.1% variance)
                elif abs(pay_amt - inv_amt) <= max(5.0, 0.001 * inv_amt):
                    amt_score = 0.8 
                
                # --- SPRINT 2: Name Similarity (Weight: 0.40) ---
                # Handle dynamic column names (Customer vs Customer_Name)
                cust_col = 'Customer_Name' if 'Customer_Name' in inv else 'Customer'
                clean_customer = str(inv[cust_col]).lower().strip()
                
                # token_set_ratio handles noise like "Inc", "Ltd", or reordered words
                name_score = fuzz.token_set_ratio(resolved_payer, clean_customer) / 100

                # --- SPRINT 3: Partial Match/Short-Pay Logic (Weight: 0.10) ---
                partial_match_bonus = 0.0
                status_note = ""
                
                # If amount is perfect but name is ambiguous, apply a safety bonus
                if is_exact_amt and name_score < 0.5:
                    partial_match_bonus = 0.7 
                    status_note = " (Amount Matched, Name Check Required)"

                # --- Weighted Confidence Calculation ---
                total_confidence = (amt_score * 0.5) + (name_score * 0.4)
                
                # Override if partial match logic suggests a likely connection
                if partial_match_bonus > total_confidence:
                    total_confidence = partial_match_bonus

                # --- Categorization & Status Assignment ---
                if total_confidence >= self.stp_threshold:
                    status = "STP: Automated"
                elif total_confidence >= self.manual_review_threshold:
                    status = f"EXCEPTION: High Confidence{status_note}"
                else:
                    status = "EXCEPTION: Investigation Required"

                # Filter out noise; only return candidates with >40% relevance
                if total_confidence > 0.40: 
                    results.append({
                        "Invoice_ID": inv['Invoice_ID'],
                        "Customer": inv[cust_col],
                        "Currency": inv['Currency'],
                        "Amount": inv_amt,
                        "confidence": round(total_confidence, 2),
                        "status": status,
                        "esg_score": inv.get('ESG_Score', 'N/A'),
                        "due_date": str(inv.get('Due_Date', 'N/A'))
                    })

            # Return results sorted by highest confidence first
            return sorted(results, key=lambda x: x['confidence'], reverse=True)

        except Exception as e:
            print(f"Engine Failure: {str(e)}")
            return []
