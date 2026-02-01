import pandas as pd
import numpy as np
import os

def generate_institutional_data():
    # Fix for GitHub Runners: Ensure the data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Seed for reproducibility in CI/CD tests
    np.random.seed(42)
    rows = 50

    # Match the schema used in backend/engine.py and tests
    invoices = pd.DataFrame({
        'Invoice_ID': [f'INV-{2026000 + i}' for i in range(rows)],
        'Customer': np.random.choice(['Tesla Inc', 'Saurabh Soft', 'Acme Corp'], size=rows),
        'Amount_Remaining': np.round(np.random.uniform(1000, 50000, size=rows), 2),
        'Currency': np.random.choice(['USD', 'EUR', 'GBP'], size=rows),
        'Due_Date': ['2026-02-15'] * rows,
        'Status': np.random.choice(['Open', 'Paid'], size=rows),
        'Company_Code': np.random.choice(['US01', 'EU10', 'AP20'], size=rows),
        'ESG_Score': np.random.choice(['AAA', 'AA', 'A', 'B', 'C', 'D'], size=rows)
    })

    # Bank Feed with the matching keys for the AI Matcher
    bank = pd.DataFrame({
        'Bank_TX_ID': [f'TXN-{i}' for i in range(10)],
        'Payer_Name': np.random.choice(['TSLA MOTORS', 'SAURABH SOFTWARE', 'ACME CORP'], size=10),
        'Amount_Received': np.round(np.random.uniform(1000, 50000, size=10), 2),
        'Currency': np.random.choice(['USD', 'EUR'], size=10),
        'Company_Code': np.random.choice(['US01', 'EU10'], size=10)
    })

    invoices.to_csv('data/invoices.csv', index=False)
    bank.to_csv('data/bank_feed.csv', index=False)
    print("✅ Success: Mock data generated with synchronized column names.")

if __name__ == "__main__":
    generate_institutional_data()
