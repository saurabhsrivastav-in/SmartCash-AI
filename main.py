import streamlit as st
import pandas as pd
import os
from backend.engine import SmartMatchingEngine
from backend.compliance import ComplianceGuard
from backend.treasury import TreasuryManager
from backend.ai_agent import GenAIAssistant

# --- CONFIGURATION ---
st.set_page_config(page_title="SmartCash AI", page_icon="🏦", layout="wide")

# --- DATA LOADING (DYNAMIC) ---
@st.cache_data
def load_data():
    inv = pd.read_csv('data/invoices.csv')
    bank = pd.read_csv('data/bank_feed.csv')
    return inv, bank

# --- INITIALIZE SESSION STATE ---
if 'audit_engine' not in st.session_state:
    st.session_state.audit_engine = ComplianceGuard()
if 'treasury' not in st.session_state:
    st.session_state.treasury = TreasuryManager()

# --- APP LAYOUT ---
st.sidebar.title("🏦 SmartCash AI")
menu = st.sidebar.radio("Navigation", ["Executive Dashboard", "Analyst Workbench", "Audit & Governance"])

invoices, bank_feed = load_data()

# --- 1. EXECUTIVE DASHBOARD ---
if menu == "Executive Dashboard":
    st.header("📊 Global Cash Performance")
    c1, c2, c3 = st.columns(3)
    c1.metric("STP Rate", "94.2%", "+2.1%")
    c2.metric("Unapplied Cash", f"${invoices['Amount'].sum():,.2f}", "Live Data")
    c3.metric("DSO", "28 Days", "-4 Days")
    st.area_chart(pd.DataFrame([10, 15, 8, 22, 18, 25, 30], columns=["Cash Flow Forecast"]))

# --- 2. ANALYST WORKBENCH (DYNAMIC MATCHING) ---
elif menu == "Analyst Workbench":
    st.header("⚡ Smart Worklist")
    
    # 1. Select a transaction from your bank_feed.csv
    st.subheader("Step 1: Ingest Bank Feed")
    selected_tx = st.selectbox(
        "Select an incoming payment to reconcile:",
        bank_feed.index,
        format_func=lambda x: f"{bank_feed.iloc[x]['Payer_Name']} - ${bank_feed.iloc[x]['Amount_Received']}"
    )
    
    tx_data = bank_feed.iloc[selected_tx]
    
    # 2. Run Engine
    if st.button("Run AI Matching Engine"):
        engine = SmartMatchingEngine()
        matches = engine.run_match(tx_data['Amount_Received'], tx_data['Payer_Name'], invoices)
        
        if matches:
            match = matches[0]
            st.success(f"Match Found! Status: {match['status']}")
            st.write(f"**Customer:** {match['Customer']} | **Invoice:** {match['Invoice_ID']}")
            st.progress(match['confidence'], text=f"Confidence: {match['confidence']*100}%")
            
            # Action Gates
            if match['confidence'] >= 0.95:
                st.balloons()
                st.info("🚀 Zero-Touch Clearing Triggered. Transaction posted to SAP.")
                st.session_state.audit_engine.log_transaction(match['Invoice_ID'], "AUTO_MATCH")
            else:
                st.warning("Manual Review Required.")
                if st.button("Draft AI Response"):
                    st.text_area("Draft:", GenAIAssistant().generate_email(match['Customer'], tx_data['Amount_Received']))
        else:
            st.error("No Match Found. Routing to Exception Management.")

# --- 3. AUDIT & GOVERNANCE ---
elif menu == "Audit & Governance":
    st.header("🛡️ Compliance Vault")
    st.subheader("Immutable Transaction Ledger")
    st.table(st.session_state.audit_engine.get_logs())
