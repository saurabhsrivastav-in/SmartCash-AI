import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_mock_data():
    """
    Generates institutional-grade datasets for SmartCash AI.
    Ensures column names match the Matching Engine and Risk Radar expectations.
    """
    # Create directory if not exists
    if not os.path.exists('data'):
        os.makedirs('data')

    np.random.seed(42)  # For reproducible results
    rows = 50

    # --- 1. GENERATE INVOICES (The ERP Ledger) ---
    invoices = pd.DataFrame({
        'Invoice_ID': [f'INV-{2026000 + i}' for i in range(rows)],
        'Customer_Name': np.random.choice([
            'Tesla Inc', 'Global Blue SE', 'Tech Retail Corp', 
            'Eco Energy Systems', 'Saurabh Soft', 'Acme Corp', 'Global Logistics'
        ], size=rows),
        'Amount': np.round(np.random.uniform(5000, 100000, size=rows), 2),
        'Currency': np.random.choice(['USD', 'EUR', 'GBP'], size=rows),
        'Due_Date': [(datetime.now() + timedelta(days=np.random.randint(-30, 60))).strftime('%Y-%m-%d') for i in range(rows)],
        'Status': np.random.choice(['Open', 'Paid'], size=rows, p=[0.7, 0.3]),
        'Company_Code': np.random.choice(['US01', 'EU10', 'AP20'], size=rows),
        'ESG_Score': np.random.choice(['AA', 'A', 'B', 'C'], size=rows, p=[0.2, 0.4, 0.3, 0.1])
    })

    # --- 2. GENERATE BANK FEED (The Cash Transactions) ---
    # We want some bank transactions to match perfectly and some to be "noisy"
    bank_rows = 15
    bank_data = []

    for i in range(bank_rows):
        # Pick a random invoice to "pay"
        idx = np.random.randint(0, rows)
        inv_ref = invoices.iloc[idx]
        
        # Add "noise" to payer name (e.g., Tesla Inc -> TSLA MOTORS GMBH)
        noise_map = {
            'Tesla Inc': 'TSLA MOTORS GMBH',
            'Global Blue SE': 'GLOBEL BLUE INTL',
            'Saurabh Soft': 'SAURABH_SOFTWARE_LTD'
        }
        payer_name = noise_map.get(inv_ref['Customer_Name'], inv_ref['Customer_Name'].upper())
        
        # Decide if this is an exact match or a short-pay (Sprint 3 logic)
        amount_received = inv_ref['Amount']
        if np.random.random() > 0.8:
            amount_received -= 15.00  # Simulate a bank fee discrepancy
            
        bank_data.append({
            'Bank_TX_ID': f'TXN-{999000 + i}',
            'Payer_Name': payer_name,
            'Amount_Received': amount_received, # Matches main.py selectbox
            'Currency': inv_ref['Currency'],
            'Bank_Ref': f'REMIT-{np.random.randint(10000, 99999)}',
            'Company_Code': inv_ref['Company_Code'],
            'Value_Date': datetime.now().strftime('%Y-%m-%d')
        })

    bank_feed = pd.DataFrame(bank_data)

    # --- 3. EXPORT TO CSV ---
    invoices.to_csv('data/invoices.csv', index=False)
    bank_feed.to_csv('data/bank_feed.csv', index=False)
    
    print("✅ Success: Data generated with Institutional Schema.")
    print(f"📍 Invoices: data/invoices.csv ({len(invoices)} rows)")
    print(f"📍 Bank Feed: data/bank_feed.csv ({len(bank_feed)} rows)")

if __name__ == "__main__":
    generate_mock_data()
