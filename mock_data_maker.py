import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_mock_data():
    """
    Generates an institutional-grade dataset including ESG scores, 
    behavioral profiles, and credit limits.
    """
    # 1. Setup metadata (Sprint 5 & 7)
    customers = [
        ('Tesla Inc', 'AA', 'Early Bird', 1000000), 
        ('Global Blue SE', 'A', 'Strategic', 750000), 
        ('Tech Retail Corp', 'B', 'Laggard', 500000),
        ('Saurabh Soft', 'AA', 'Early Bird', 1200000), 
        ('Eco Energy', 'A', 'Strategic', 600000), 
        ('Nordic Logistics', 'B', 'Laggard', 400000),
        ('Swiss Finance', 'AA', 'Early Bird', 2000000), 
        ('Pacific Rim', 'C', 'Laggard', 250000), 
        ('Horizon Ventures', 'A', 'Strategic', 800000)
    ]
    currencies = ['USD', 'EUR', 'GBP', 'INR', 'CHF']
    entities = ['NORTH_AMERICA', 'EMEA', 'APAC'] # Sprint 10 Multi-entity

    # 2. Generate Invoices (200 rows)
    invoice_data = []
    for i in range(1, 201):
        cust, esg, profile, limit = customers[np.random.randint(0, len(customers))]
        curr = currencies[np.random.randint(0, len(currencies))]
        entity = entities[np.random.randint(0, len(entities))]
        
        amount = np.random.uniform(10000, 250000)
        # Create a mix of past-due and future-due invoices
        due_date = datetime.now() + timedelta(days=np.random.randint(-45, 60))
        status = 'Paid' if np.random.random() > 0.6 else 'Open'
        
        invoice_data.append([
            f"INV-{2026}{i:03d}", # 2026 Serialized IDs
            cust, 
            round(amount, 2), 
            curr, 
            due_date.strftime('%Y-%m-%d'), 
            status, 
            esg, 
            profile, 
            limit,
            entity
        ])
        
    inv_df = pd.DataFrame(invoice_data, columns=[
        'Invoice_ID', 'Customer_Name', 'Amount', 'Currency', 
        'Due_Date', 'Status', 'ESG_Score', 'Behavior_Profile', 
        'Credit_Limit', 'Entity_ID'
    ])

    # 3. Generate Bank Feed with "Noise" for AI Matching (Sprint 2 & 3)
    bank_data = []
    # Take a sample of open invoices to simulate real bank credits
    open_invoices = inv_df[inv_df['Status'] == 'Open'].sample(frac=0.5)
    
    for idx, row in open_invoices.iterrows():
        # SCENARIO A: Exact Match
        # SCENARIO B: Fuzzy Match (Typo in name)
        # SCENARIO C: Short-Pay (Amount is slightly less)
        
        rand_val = np.random.random()
        
        if rand_val > 0.7: # Scenario B: Misspelled Name
            payer = row['Customer_Name'].replace('Inc', 'Incorporated').replace('Corp', 'Co.')
            amt_received = row['Amount']
            ref = "Monthly Settlement" 
        elif rand_val < 0.2: # Scenario C: Short Pay
            payer = row['Customer_Name']
            amt_received = row['Amount'] - np.random.choice([50, 100, 500])
            ref = row['Invoice_ID']
        else: # Scenario A: Perfect Match
            payer = row['Customer_Name']
            amt_received = row['Amount']
            ref = row['Invoice_ID']

        bank_data.append([
            f"BANK-TXN-{idx:04d}", 
            round(amt_received, 2), 
            row['Currency'], 
            payer, 
            ref,
            datetime.now().strftime('%Y-%m-%d'),
            'Unmatched'
        ])

    bank_df = pd.DataFrame(bank_data, columns=[
        'Bank_Ref', 'Amount', 'Currency', 'Payer_Name', 'Reference_Text', 'Date', 'Status'
    ])

    # 4. Save to 'data' folder
    if not os.path.exists('data'):
        os.makedirs('data')
        
    inv_df.to_csv('data/invoices.csv', index=False)
    bank_df.to_csv('data/bank_feed.csv', index=False)
    
    print(f"✅ 2026 Strategic Data Generated:")
    print(f"- Invoices: {len(inv_df)} rows")
    print(f"- Bank Feed: {len(bank_df)} rows")

if __name__ == "__main__":
    generate_mock_data()
