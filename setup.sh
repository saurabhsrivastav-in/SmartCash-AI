#!/bin/bash

echo "🚀 Initializing SmartCash AI Environment..."

# 1. Create directory structure if missing
mkdir -p backend
mkdir -p data

# 2. Create __init__.py files to ensure Python treats folders as packages
# This is usually why the 'ModuleNotFoundError' occurs on Streamlit Cloud
touch backend/__init__.py

# 3. Create dummy data files if they don't exist (prevents crash on first load)
if [ ! -f data/invoices.csv ]; then
    echo "Invoice_ID,Customer,Amount,Currency,Due_Date,Status,ESG_Score" > data/invoices.csv
    echo "INV-001,Tesla Inc,50000,USD,2026-02-15,Open,AA" >> data/invoices.csv
fi

if [ ! -f data/bank_feed.csv ]; then
    echo "Bank_TX_ID,Payer_Name,Amount_Received,Bank_Reference,Currency" > data/bank_feed.csv
    echo "TXN-613,Tesla Tokyo KK,50000,INV-001,USD" >> data/bank_feed.csv
fi

# 4. Install dependencies
echo "📦 Installing Institutional-Grade dependencies..."
pip install -r requirements.txt

echo "✅ Setup Complete. Run 'streamlit run main.py' to launch."
