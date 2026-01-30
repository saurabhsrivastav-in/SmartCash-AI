import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_mock_data():
    """
    Generates institutional-grade datasets for SmartCash AI.
    Features: ESG Scoring (S5), Credit Limits (S7), and Company Codes (S10).
    """
    # 1. Setup Master Data
    customers = [
        ('Tesla Inc', 'AA', 2500000), 
        ('Global Blue SE', 'A', 1500000), 
        ('Tech Retail Corp', 'B', 800000),
        ('Saurabh Soft', 'AA', 3000000), 
        ('Eco Energy', 'A', 1200000), 
        ('Nordic Logistics', 'B', 950000),
        ('Swiss Finance', 'AA', 5000000), 
        ('Pacific Rim', 'C', 450000), 
        ('Horizon Ventures', 'A', 1100000)
    ]
    currencies = ['USD', 'EUR', 'GBP', 'INR', 'CHF']
    # Sprint 10: Multi-entity hierarchy
    company_codes = ['US01', 'EU10', 'AP20', 'CH05'] 

    # 2. Generate Invoices
    invoice_data = []
    for i in range(1, 201):
        cust, esg, limit = customers[np.random.randint(0, len(customers))]
        curr = currencies[np.random.randint(0, len(currencies))]
        cocode = company_codes[np.random.randint(0, len(company_codes))]
        
        amount = np.random.uniform(15000, 450000)
        # Create a mix of past-due and future-due invoices
        due_date = datetime.now() + timedelta(days=np.random.randint(-45, 60))
        status = 'Paid' if np.random.random() > 0.6 else 'Open'
        
        invoice_data.append([
            f"INV-{2026}{i:03d}",
            cust, 
            round(amount, 2), 
            curr, 
            due_date.strftime('%Y-%m-%d'), 
            status, 
            esg,      # Sprint 5: ESG Score
            limit,    # Sprint 7: Credit Limit
            cocode    # Sprint 10: Company Code
        ])
        
    inv_df = pd.DataFrame(invoice_data, columns=[
        'Invoice_ID', 'Customer_Name', 'Amount', 'Currency', 
        'Due_Date', 'Status', 'ESG_Score', 'Credit_Limit', 'Company_Code'
    ])

    # 3. Generate Bank Feed (Simulating ~50% collections)
    bank_data = []
    open_invoices = inv_df[inv_df['Status'] == 'Open'].sample(frac=0.5)
    
    for idx, row in open_invoices.iterrows():
        # Injecting "Noisy" data for Fuzzy Matching logic
        rand_scenario = np.random.random()
        
        if rand_scenario > 0.8: # Misspelled Name
            payer = row['Customer_Name'].replace('Inc', 'Incorporated').replace('Corp', 'Co.')
            amt_received = row['Amount']
            ref = "Trade Settlement" 
        elif rand_scenario < 0.2: # Short Pay / Fee Deduction
            payer = row['Customer_Name']
            amt_received = row['Amount'] - np.random.choice([25, 50, 100])
            ref = row['Invoice_ID']
        else: # Perfect Match
            payer = row['Customer_Name']
            amt_received = row['Amount']
            ref = row['Invoice_ID']

        bank_data.append([
            f"BNK-{idx:04d}", 
            round(amt_received, 2), 
            row['Currency'], 
            payer, 
            ref,
            datetime.now().strftime('%Y-%m-%d'),
            row['Company_Code'], # Ensure entity alignment
            'Unmatched'
        ])

    bank_df = pd.DataFrame(bank_data, columns=[
        'Bank_Ref', 'Amount_Received', 'Currency', 'Payer_Name', 
        'Remittance_Text', 'Date', 'Company_Code', 'Match_Status'
    ])

    # 4. Save to Repository
    os.makedirs('data', exist_ok=True)
    inv_df.to_csv('data/invoices.csv', index=False)
    bank_df.to_csv('data/bank_feed.csv', index=False)
    
    print("✅ Strategic Data Generated: /data/invoices.csv and /data/bank_feed.csv")

if __name__ == "__main__":
    generate_mock_data()
