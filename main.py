import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="SmartCash AI | Treasury Command", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b1117; color: #e6edf3; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #58a6ff; }
    .stDataFrame { border: 1px solid #30363d; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
@st.cache_data
def load_data():
    inv = pd.DataFrame({
        'Company_Code': ['1000', '1000', '2000', '3000', '1000', '2000', '3000', '1000'],
        'Customer': ['Tesla', 'EcoEnergy', 'GlobalBlue', 'TechRetail', 'Quantum Dyn', 'Alpha Log', 'Nordic Oil', 'Sino Tech'],
        'Amount': [5200000, 15000000, 1250000, 3200000, 12450000, 450000, 8900000, 4100000],
        'Currency': ['USD', 'USD', 'EUR', 'GBP', 'USD', 'EUR', 'NOK', 'USD'],
        'ESG_Score': ['AAA', 'B', 'D', 'A', 'C', 'D', 'B', 'AAA'],
        'Due_Date': ['2026-01-10', '2026-02-15', '2025-12-01', '2026-03-01', '2025-11-20', '2026-01-05', '2026-02-28', '2026-01-20']
    })
    bank = pd.DataFrame({
        'Bank_ID': ['TXN_001', 'TXN_002', 'TXN_003'],
        'Payer': ['Tesla', 'GlobalBlue', 'Unknown'],
        'Amount_Received': [5200000, 1200000, 3150000],
        'Currency': ['USD', 'EUR', 'GBP']
    })
    return inv, bank

raw_invoices, raw_bank = load_data()

# --- 3. GLOBAL STATE & SIDEBAR ---
if 'audit_log' not in st.session_state: st.session_state.audit_log = []

with st.sidebar:
    st.title("🏦 SmartCash AI")
    menu = st.radio("Workspace", ["📈 Executive Dashboard", "🛡️ Risk Radar", "⚡ Analyst Workbench", "📜 Audit Ledger"])
    st.divider()
    
    # GLOBAL FILTERS
    latency_days = st.slider("Collection Latency (Days)", 0, 90, 15)
    entity_choice = st.selectbox("Company Entity", ["All Entities"] + list(raw_invoices['Company_Code'].unique()))
    
    st.divider()
    st.subheader("📝 Scenario Governance")
    scen_label = st.text_input("Scenario Label", "Standard Ops")
    scen_note = st.text_area("Analyst Notes")

# Filter Data based on Sidebar
invoices = raw_invoices.copy()
if entity_choice != "All Entities":
    invoices = invoices[invoices['Company_Code'] == entity_choice]

# --- 4. DYNAMIC CALCULATIONS ---
esg_map = {'AAA': 100, 'AA': 80, 'A': 70, 'B': 50, 'C': 30, 'D': 10}
avg_esg = invoices['ESG_Score'].map(esg_map).mean()
stp_rate = 94.2 - (latency_days * 0.1) # STP drops as latency increases
liquidity_pool = (invoices['Amount'].sum() / 1000000) - (latency_days * 0.2)

# --- WORKSPACE ROUTING ---

if menu == "📈 Executive Dashboard":
    # METRIC ROW
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Adjusted DSO", f"{34 + latency_days} Days", f"+{latency_days}d")
    m2.metric("Liquidity Pool", f"${liquidity_pool:.1f}M", f"{-latency_days*0.2:.1f}M Latency")
    m3.metric("ESG Health Index", f"{avg_esg:.1f}/100", "Live Weighted")
    m4.metric("STP Reliability", f"{stp_rate:.1f}%", "-0.2% Drift")

    st.divider()

    # FORECAST & GAUGE
    c1, c2 = st.columns([1, 2])
    with c1:
        fig_g = go.Figure(go.Indicator(mode="gauge+number", value=92, title={'text': "Data Integrity"},
                                      gauge={'bar':{'color':"#58a6ff"}, 'steps':[{'range':[0,50], 'color':"#f85149"}]}))
        fig_g.update_layout(height=250, template="plotly_dark", margin=dict(t=50, b=0))
        st.plotly_chart(fig_g, use_container_width=True)
    with c2:
        st.subheader("💹 Cash Flow Forecast")
        fig_f = px.line(x=['Jan', 'Feb', 'Mar', 'Apr'], y=[40, 45, 42, 50], labels={'x':'Month', 'y':'$M'})
        fig_f.update_layout(template="plotly_dark", height=250)
        st.plotly_chart(fig_f, use_container_width=True)

    st.divider()

    # STRESS TEST & RE-SCALED HEATMAP
    st.subheader("🔥 Strategic Risk Sensitivity")
    fx_swing = st.toggle("Simulate 5% USD Strengthening")
    hedge_ratio = st.slider("Hedge Coverage %", 0, 100, 50) if fx_swing else 0
    
    # Heatmap calculation (Fully Scaled)
    fx_range = [-0.10, -0.05, -0.02, 0, 0.02]
    h_range = [0, 0.25, 0.5, 0.75, 1.0]
    z = [[round(liquidity_pool * f * (1 - (h)), 2) for h in h_range] for f in fx_range]
    
    fig_h = px.imshow(z, text_auto=True, color_continuous_scale='RdYlGn', aspect="auto",
                      labels=dict(x="Hedge Ratio", y="FX Swing", color="Impact $M"),
                      x=['0%', '25%', '50%', '75%', '100%'], y=['-10%', '-5%', '-2%', '0%', '+2%'])
    fig_h.update_layout(template="plotly_dark", height=450) # Larger height for readability
    st.plotly_chart(fig_h, use_container_width=True)

    if st.button("💾 Archive Scenario to Audit Ledger"):
        st.session_state.audit_log.insert(0, {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Entity": entity_choice,
            "Liquidity": f"${liquidity_pool:.1f}M",
            "ESG": f"{avg_esg:.1f}",
            "Hedge": f"{hedge_ratio}%",
            "Notes": scen_note
        })

elif menu == "🛡️ Risk Radar":
    st.subheader("🛡️ Multi-Level Risk Exposure")
    
    # Restore Weights
    weights = {'AAA': 0.05, 'AA': 0.1, 'A': 0.2, 'B': 0.4, 'C': 0.6, 'D': 0.9}
    invoices['Risk_Value'] = invoices['Amount'] * invoices['ESG_Score'].map(weights)
    
    # Complete Sunburst
    fig_s = px.sunburst(invoices, path=['Company_Code', 'Currency', 'ESG_Score', 'Customer'], 
                        values='Risk_Value', color='ESG_Score',
                        color_discrete_map={'AAA':'#238636', 'B':'#d29922', 'D':'#f85149'})
    st.plotly_chart(fig_s, use_container_width=True)

    # Filterable Ledger Table
    st.subheader("🔍 Searchable Exposure Ledger")
    search = st.text_input("Filter by Customer or Rating", "")
    df_f = invoices[invoices['Customer'].str.contains(search, case=False) | invoices['ESG_Score'].str.contains(search)]
    st.dataframe(df_f, use_container_width=True)

elif menu == "⚡ Analyst Workbench":
    st.subheader("⚡ Transaction Matching & Dunning")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Open Bank Transactions**")
        selected_txn = st.selectbox("Select TXN to Match", raw_bank['Bank_ID'])
        txn = raw_bank[raw_bank['Bank_ID'] == selected_txn].iloc[0]
        st.info(f"Payer: {txn['Payer']} | Amount: {txn['Amount_Received']} {txn['Currency']}")
        
        if st.button("Run AI Matcher"):
            potential = invoices[invoices['Customer'] == txn['Payer']]
            if not potential.empty:
                st.success(f"Match Found! Invoice ID: {potential.index[0]} (99% Confidence)")
            else:
                st.warning("No Direct Match. Partial match search active...")

    with col_b:
        st.write("**Dunning Action Center**")
        overdue = invoices[invoices['ESG_Score'] == 'D']
        target = st.selectbox("Select Delinquent Customer", overdue['Customer'].unique())
        if st.button("Generate Dunning Letter"):
            st.code(f"Subject: URGENT - Payment Overdue\nDear {target},\nOur records show your balance is outstanding...")
            st.success(f"Dunning Letter ready for {target}")

elif menu == "📜 Audit Ledger":
    st.subheader("📜 SOC2 Compliance Ledger")
    if st.session_state.audit_log:
        st.dataframe(pd.DataFrame(st.session_state.audit_log), use_container_width=True)
        csv = pd.DataFrame(st.session_state.audit_log).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV", csv, "audit_log.csv")
    else:
        st.warning("No scenarios recorded. Go to Executive Dashboard to save a simulation.")
