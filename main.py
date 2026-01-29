import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from backend.engine import SmartMatchingEngine
from backend.compliance import ComplianceGuard
from backend.treasury import TreasuryManager
from backend.ai_agent import GenAIAssistant

# --- 1. ENTERPRISE CONFIGURATION ---
st.set_page_config(
    page_title="SmartCash AI | Treasury Command", 
    page_icon="🏦", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Banking UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .stMetric { background-color: #1c2128; border: 1px solid #30363d; padding: 20px; border-radius: 12px; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #238636; color: white; border: none; }
    .stDataFrame { border: 1px solid #30363d; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INTELLIGENT DATA INGESTION ---
@st.cache_data
def load_data():
    # Loading multi-year, multi-currency datasets
    inv = pd.read_csv('data/invoices.csv')
    bank = pd.read_csv('data/bank_feed.csv')
    
    # Pre-processing for time-series and currency normalization
    inv['Due_Date'] = pd.to_datetime(inv['Due_Date'])
    inv['Year'] = inv['Due_Date'].dt.year
    inv['Month'] = inv['Due_Date'].dt.strftime('%b')
    return inv, bank

# --- 3. SESSION STATE & ORCHESTRATION ---
if 'audit_engine' not in st.session_state:
    st.session_state.audit_engine = ComplianceGuard()
if 'treasury' not in st.session_state:
    st.session_state.treasury = TreasuryManager()

invoices, bank_feed = load_data()
engine = SmartMatchingEngine()

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.image("https://img.icons8.com/fluency/96/shield-with-dollar.png", width=60)
st.sidebar.title("SmartCash AI")
st.sidebar.markdown("**Institutional Treasury Hub**")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Navigation Center", 
    ["Executive Dashboard", "Analyst Workbench", "Risk & Governance", "Audit Ledger"]
)

st.sidebar.divider()
st.sidebar.info(f"🟢 **System:** Operational\n\n📅 **Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n📂 **Records:** {len(invoices)} Invoices")

# --- 5. EXECUTIVE DASHBOARD ---
if menu == "Executive Dashboard":
    st.title("📊 Global Cash & Liquidity Position")
    
    # Strategic KPIs
    m1, m2, m3, m4 = st.columns(4)
    total_val = invoices['Amount'].sum()
    m1.metric("Total A/R Position", f"${total_val/1e6:.2f}M", "+4.2% MoM")
    m2.metric("STP Efficiency", "94.2%", "Target: 92%")
    m3.metric("Portfolio ESG Rating", "A-", "Trend: Up")
    m4.metric("DSO Index", "26 Days", "-3 Days")

    st.divider()

    # Multi-Year Liquidity Trend
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📈 Multi-Year Inflow Analysis")
        yearly_summary = invoices.groupby(['Year', 'Currency'])['Amount'].sum().reset_index()
        fig = px.bar(yearly_summary, x="Year", y="Amount", color="Currency", 
                     title="Cash Collection Forecast by Region", barmode='group',
                     template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("🌍 Currency Exposure")
        fig_fx = px.pie(bank_feed, names='Currency', values='Amount_Received', 
                        hole=0.5, title="Net Cash by Currency",
                        template="plotly_dark")
        st.plotly_chart(fig_fx, use_container_width=True)

# --- 6. ANALYST WORKBENCH ---
elif menu == "Analyst Workbench":
    st.title("⚡ Smart Reconciliation Workbench")
    
    st.markdown("### 📥 Inbound Bank Feed")
    st.dataframe(bank_feed, use_container_width=True, hide_index=True)

    st.divider()

    col_sel, col_match = st.columns([1, 2])
    
    with col_sel:
        st.subheader("Step 1: Focus Item")
        tx_id = st.selectbox(
            "Select Transaction for Resolution:",
            bank_feed.index,
            format_func=lambda x: f"{bank_feed.iloc[x]['Bank_TX_ID']} | {bank_feed.iloc[x]['Payer_Name']} ({bank_feed.iloc[x]['Currency']})"
        )
        tx_data = bank_feed.iloc[tx_id]
        st.info(f"**Selected Amount:** {tx_data['Currency']} {tx_data['Amount_Received']:,.2f}")

    with col_match:
        st.subheader("Step 2: AI Execution")
        if st.button("Run Multi-Factor Match"):
            matches = engine.run_match(
                tx_data['Amount_Received'], 
                tx_data['Payer_Name'], 
                tx_data['Currency'], 
                invoices
            )
            
            if matches:
                top_match = matches[0]
                conf = top_match['confidence']
                
                if conf >= 0.95:
                    st.success(f"STP MATCH CONFIRMED ({conf*100}%)")
                    st.json(top_match)
                    st.balloons()
                    st.session_state.audit_engine.log_transaction(top_match['Invoice_ID'], "AUTO_STP_POST")
                else:
                    st.warning(f"EXCEPTION ENCOUNTERED: {top_match['status']} ({conf*100}%)")
                    st.write(f"Suggested Invoice: **{top_match['Invoice_ID']}** for **{top_match['Customer']}**")
                    
                    # Logic for generating dispute or clarification
                    st.markdown("---")
                    st.subheader("🤖 AI Agent Assistance")
                    agent = GenAIAssistant()
                    draft = agent.generate_email(top_match['Customer'], tx_data['Amount_Received'])
                    st.text_area("Draft Communication:", draft, height=200)
                    st.button("📧 Send to Counterparty")
            else:
                st.error("NO MATCH FOUND: Routing to Manual Treasury Investigation.")

# --- 7. RISK & GOVERNANCE ---
elif menu == "Risk & Governance":
    st.title("🛡️ Institutional Risk & ESG Controls")
    
    g1, g2 = st.columns(2)
    with g1:
        st.subheader("🛑 ESG Compliance Violations")
        risk_clients = invoices[invoices['ESG_Score'].isin(['D', 'E'])]
        st.error(f"Attention: {len(risk_clients)} High-Risk Counterparties Detected")
        st.dataframe(risk_clients[['Invoice_ID', 'Customer', 'Amount', 'ESG_Score']], hide_index=True)
        
    with g2:
        st.subheader("⚖️ Concentration Risk (Top 5)")
        concentration = invoices.groupby('Customer')['Amount'].sum().nlargest(5).reset_index()
        fig_risk = px.funnel(concentration, x='Amount', y='Customer', title="Exposure by Entity", template="plotly_dark")
        st.plotly_chart(fig_risk, use_container_width=True)

# --- 8. AUDIT LEDGER ---
elif menu == "Audit Ledger":
    st.title("🔐 SOC2 Compliance Vault")
    st.caption("Immutable audit trail of all automated treasury actions.")
    
    logs = st.session_state.audit_engine.get_logs()
    if logs is not None and not logs.empty:
        st.dataframe(logs, use_container_width=True, hide_index=True)
        st.download_button("📥 Export Audit Report (CSV)", logs.to_csv(), "treasury_audit.csv")
    else:
        st.info("System Initialized. Awaiting first transaction logging...")
