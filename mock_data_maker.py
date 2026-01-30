import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_mock_data():
    """
    Generates the Institutional Schema for SmartCash AI.
    Ensures all columns required by the Risk Radar and Matching Engine exist.
    """
    # 1. Setup Environment
    if not os.path.exists('data'):
        os.makedirs('data')

    np.random.seed(42)
    rows = 60

    # 2. Generate Invoices (ERP Ledger)
    # Columns MUST match main.py requirements for the Sunburst path
    invoices = pd.DataFrame({
        'Invoice_ID': [f'INV-{2026000 + i}' for i in range(rows)],
        'Customer_Name': np.random.choice([
            'Tesla Inc', 'Global Blue SE', 'Tech Retail Corp', 
            'Eco Energy Systems', 'Saurabh Soft', 'Acme Corp'
        ], size=rows),
        'Amount': np.round(np.random.uniform(5000, 120000, size=rows), 2),
        'Currency': np.random.choice(['USD', 'EUR', 'GBP'], size=rows),
        'Due_Date': [(datetime.now() + timedelta(days=np.random.randint(-15, 45))).strftime('%Y-%m-%d') for i in range(rows)],
        'Status': np.random.choice(['Open', 'Paid'], size=rows, p=[0.7, 0.3]),
        'Company_Code': np.random.choice(['US01', 'EU10', 'AP20'], size=rows), # CRITICAL: Fixed the missing column
        'ESG_Score': np.random.choice(['AA', 'A', 'B', 'C'], size=rows, p=[0.2, 0.4, 0.3, 0.1])
    })

    # 3. Generate Bank Feed (Cash Inflow)
    bank_rows = 12
    bank_data = []
    
    # Map for Alias Matching Engine testing
    aliases = {
        'Tesla Inc': 'TSLA MOTORS GMBH',
        'Global Blue SE': 'GLOBEL BLUE INTL',
        'Saurabh Soft': 'SAURABH_SOFTWARE_LTD'
    }

    for i in range(bank_rows):
        # Pick a random invoice to simulate a payment against it
        target_inv = invoices.iloc[np.random.randint(0, rows)]
        
        # Determine Payer Name (sometimes exact, sometimes aliased)
        raw_name = target_inv['Customer_Name']
        payer_name = aliases.get(raw_name, raw_name.upper())
        
        # Amount Received (simulate occasional bank fee deductions)
        amt = target_inv['Amount']
        if np.random.rand() > 0.8:
            amt -= 15.00 # $15 bank fee discrepancy
            
        bank_data.append({
            'Bank_TX_ID': f'TXN-{888000 + i}',
            'Payer_Name': payer_name,
            'Amount_Received': amt, # Corrected key for main.py
            'Currency': target_inv['Currency'],
            'Company_Code': target_inv['Company_Code'],
            'Bank_Ref': f'REMIT-{np.random.randint(1000, 9999)}',
            'Value_Date': datetime.now().strftime('%Y-%m-%d')
        })

    bank_feed = pd.DataFrame(bank_data)

    # 4. Save to CSV
    invoices.to_csv('data/invoices.csv', index=False)
    bank_feed.to_csv('data/bank_feed.csv', index=False)
    
    print("--- 🏦 SmartCash AI Data Generation Complete ---")
    print(f"Verified Columns in Invoices: {list(invoices.columns)}")
    print(f"Verified Columns in Bank Feed: {list(bank_feed.columns)}")
    print("-------------------------------------------------")

if __name__ == "__main__":
    generate_mock_data()
