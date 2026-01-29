import streamlit as st
import pandas as pd
import time
import hashlib
import random
from datetime import datetime

# --- CONFIGURATION & THEME (Sprint 1) ---
st.set_page_config(page_title="SmartCash AI | Autonomous O2C", layout="wide")

# --- MOCK DATA GENERATION (Sprints 1-3) ---
def load_mock_data():
    invoices = pd.DataFrame({
        'Invoice_ID': ['INV-1001', 'INV-1002', 'INV-1003', 'INV-1004', 'INV-1005'],
        'Customer': ['Global Corp', 'Tech Solutions', 'Retail Giant', 'Eco Energy', 'Alpha Ltd'],
        'Amount': [5000.00, 1200.50, 3000.00, 450.00, 8900.00],
        'Due_Date': ['2026-01-15', '2026-01-20', '2026-01-10', '2026-01-25', '2026-01-05'],
        'ESG_Score': [85, 40, 92, 98, 55]  # Sprint 9: ESG Integration
    })
    return invoices

# --- BLOCKCHAIN AUDIT LOG LOGIC (Sprint 9 & 11) ---
def generate_audit_hash(action, details):
    timestamp = str(datetime.now())
    block_content = f"{timestamp}-{action}-{details}"
    return hashlib.sha256(block_content.encode()).hexdigest()

# --- AI MATCHING ENGINE (Sprints 2, 5, 10) ---
def matching_engine(payment_amount, payer_name, invoices):
    st.toast("AI Engine running: Analyzing patterns...", icon="🧠")
    
    # Simulate Fuzzy Logic & Trust Scores (Sprint 5/10)
    for index, row in invoices.iterrows():
        # Exact Match
        if payment_amount == row['Amount'] and payer_name.lower() in row['Customer'].lower():
            return row, 1.0, "Auto-Matched"
        # Fuzzy Match / Partial (Scenario C)
        elif abs(payment_amount - row['Amount']) < 100:
            return row, 0.85, "Suggested"
            
    return None, 0.0, "Exception"

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏦 SmartCash AI")
st.sidebar.caption("v1.0.0 | Autonomous Mode Active")
menu = st.sidebar.radio("Navigation", [
    "Dashboard", "Analyst Workbench", "Autonomous Treasury", "Audit & Compliance", "Settings"
])

# --- DASHBOARD (Sprint 4 & 8) ---
if menu == "Dashboard":
    st.header("Executive Insights Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Unapplied Cash", "$12,450", "-15%")
    col2.metric("STP Rate", "88%", "+5%")
    col3.metric("DSO", "32 Days", "-2 Days")
    col4.metric("AI Confidence", "94%", "Stable")

    st.subheader("Cash Flow Forecast (Sprint 8 Predictive AI)")
    chart_data = pd.DataFrame(
        [10, 15, 8, 12, 20, 25, 18],
        columns=['Projected Liquidity ($M)']
    )
    st.area_chart(chart_data)

# --- ANALYST WORKBENCH (Sprints 3, 6, 7) ---
elif menu == "Analyst Workbench":
    st.header("Human-in-the-Loop Workbench")
    invoices = load_mock_data()
    
    with st.expander("📥 Simulate New Bank Feed (MT942)", expanded=True):
        col_a, col_b = st.columns(2)
        pay_amt = col_a.number_input("Payment Amount", value=1200.50)
        pay_name = col_b.text_input("Payer Name", "Tech Solut")
        
        if st.button("Run Matching Engine"):
            match, score, status = matching_engine(pay_amt, pay_name, invoices)
            
            if status == "Auto-Matched":
                st.success(f"Perfect Match! Posted to SAP: {match['Invoice_ID']}")
                st.info(f"Audit Hash: {generate_audit_hash('AUTO_POST', match['Invoice_ID'])}")
            elif status == "Suggested":
                st.warning(f"Suggested Match Found (Confidence: {score*100}%)")
                st.write(f"Match with {match['Invoice_ID']} for {match['Customer']}")
                
                # Sprint 6: GenAI Assistant
                if st.button("Draft AI Dispute Email"):
                    st.code(f"Subject: Payment Discrepancy - {match['Invoice_ID']}\n\nDear {match['Customer']},\nWe received your payment of ${pay_amt}...")
                
                if st.button("Confirm & Clear SAP"):
                    st.balloons()
                    st.success("Transaction Cleared Successfully.")
            else:
                st.error("No Match Found. Manual Investigation Required.")

# --- AUTONOMOUS TREASURY (Sprints 10 & 12) ---
elif menu == "Autonomous Treasury":
    st.header("Autonomous Liquidity & CBDC Settlement")
    
    st.info("System is monitoring real-time news for Black-Swan events (Sprint 10).")
    
    col_x, col_y = st.columns(2)
    with col_x:
        st.subheader("Liquidity Sweep")
        st.write("Current Surplus: **$2.4M**")
        if st.button("Execute Autonomous Sweep"):
            with st.status("Moving funds to Money Market via API..."):
                time.sleep(2)
            st.success("Sweep Complete. Estimated Yield: +$140/day")

    with col_y:
        st.subheader("Instant Settlement (CBDC)")
        st.write("Programmable money rail: **Active**")
        st.toggle("Enable T+0 Atomic Settlement")

# --- AUDIT & COMPLIANCE (Sprints 9 & 11) ---
elif menu == "Audit & Compliance":
    st.header("Governance & Ethical AI Monitor")
    
    tab1, tab2 = st.tabs(["Immutable Audit Log", "Bias Detection"])
    
    with tab1:
        st.dataframe(pd.DataFrame({
            'Timestamp': [datetime.now()],
            'Action': ['MANUAL_OVERRIDE'],
            'Entity': ['INV-1002'],
            'User': ['S. Srivastav'],
            'SHA-256_Hash': [generate_audit_hash('MANUAL', 'INV-1002')]
        }))
        st.button("Download Certified Audit Package (Sprint 9)")

    with tab2:
        st.subheader("Algorithmic Fairness Monitor")
        st.progress(98, text="Bias Firewall Integrity: 98%")
        st.caption("No regional or demographic bias detected in prioritisation logic.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("🔒 Quantum-Secure Connection (Sprint 11)")
