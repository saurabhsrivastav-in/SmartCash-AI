import os
import sys
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# --- PATH & BACKEND INTEGRATION ---
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.engine import SmartMatchingEngine
from backend.compliance import ComplianceVault
from backend.analytics import TreasuryAnalytics

# --- 1. ENTERPRISE CONFIGURATION ---
st.set_page_config(
    page_title="SmartCash AI | Treasury Command", 
    page_icon="🏦", 
    layout="wide"
)

# Professional Institutional Styling
st.markdown("""
    <style>
    .stApp { background-color: #0b1117; color: #e6edf3; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #58a6ff; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #161b22; border-radius: 4px 4px 0 0; }
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. RESOURCE INITIALIZATION ---
@st.cache_data
def load_data():
    try:
        inv = pd.read_csv('data/invoices.csv')
        bank = pd.read_csv('data/bank_feed.csv')
        return inv, bank
    except Exception as e:
        st.error(f"⚠️ Data Source Missing: {e}")
        return pd.DataFrame(), pd.DataFrame()   

# Persistent Session Objects
if 'engine' not in st.session_state:
    st.session_state.engine = SmartMatchingEngine()
if 'vault' not in st.session_state:
    st.session_state.vault = ComplianceVault()
if 'analytics' not in st.session_state:
    st.session_state.analytics = TreasuryAnalytics()

invoices, bank_feed = load_data()

# --- 3. SIDEBAR: NAVIGATION & CONTROLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=80)
    st.title("SmartCash AI")
    st.caption("Institutional Liquidity Management v1.0")
    st.divider()
    
    # NEW NAVIGATION MENU
    st.subheader("🧭 Navigation")
    menu = st.radio(
        "Select Workspace",
        ["📈 Executive Dashboard", "⚡ Analyst Workbench", "🛡️ Risk Radar", "📜 Audit Ledger"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.subheader("🛠️ Stress Parameters")
    latency_days = st.slider("Collection Latency (Days)", 0, 90, 15)
    
    entity_list = ["All Entities"] + (invoices['Company_Code'].unique().tolist() if not invoices.empty else [])
    entity = st.selectbox("Company Entity", entity_list)
    
    if entity != "All Entities":
        invoices = invoices[invoices['Company_Code'] == entity]
        bank_feed = bank_feed[bank_feed['Company_Code'] == entity]
    
    st.divider()
    st.info(f"🟢 **System Status: Secure**\n\n**Vault Ref:** {datetime.now().strftime('%H%M%S')}-TXN")

# --- 4. TOP-LEVEL METRICS ---
m1, m2, m3, m4 = st.columns(4)
base_dso = st.session_state.engine.calculate_dso(invoices) if not invoices.empty else 0
m1.metric("Adjusted DSO", f"{base_dso + latency_days:.1f} Days", f"+{latency_days}d Latency")
m2.metric("Matching STP Rate", "94.2%", "+1.4% WoW")
m3.metric("ESG Risk Weight", "Medium", "Tier B Avg")
m4.metric("Vault Health", "Verified", "SHA-256 Active")

st.divider()

# --- 5. PAGE ROUTING LOGIC ---

# --- TAB 1: EXECUTIVE DASHBOARD (FX Hedging & Risk Mitigation) ---
if menu == "📈 Executive Dashboard":
    st.subheader("🗓️ Multi-Currency Liquidity & Risk Mitigation")
    
    # 1. Main Controls
    year_col1, year_col2, year_col3 = st.columns([1, 1, 1])
    with year_col1:
        primary_year = st.selectbox("Primary Year", [2026, 2025, 2024], index=0)
    with year_col2:
        compare_year = st.selectbox("Comparison Year", [2025, 2024, "None"], index=1)
    with year_col3:
        stress_active = st.toggle("🚨 Activate Stress Test")
        fx_swing = st.toggle("💱 Simulate 5% USD Strengthening")
        
    # --- HEDGING & MITIGATION PARAMETERS ---
    insurance_cost = 0
    recovery_rate = 0
    hedge_ratio = 0.0
    
    # Display Hedging Slider if FX Swing is active
    if fx_swing:
        hedge_ratio = st.slider("FX Hedge Ratio (%)", 0, 100, 50, help="Portion of foreign exposure locked via Forward Contracts") / 100
    
    if stress_active:
        m1, m2 = st.columns(2)
        with m1:
            recovery_rate = st.slider("Agency Recovery Rate (%)", 0, 100, 30)
        with m2:
            insurance_cost = st.number_input("Insurance Premium (USD M)", 0.0, 50.0, 5.0, step=0.5)

    # --- SIMULATION ENGINE ---
    curr_total = 292.5 
    # Assume 40% of Liquidity is FX-exposed (EUR/GBP)
    fx_exposed_amount = curr_total * 0.40
    usd_static_amount = curr_total * 0.60
    
    # FX Impact Calculation
    # Impact = Exposed Amount * 5% drop * (1 - Hedge Ratio)
    fx_impact_raw = fx_exposed_amount * -0.05
    fx_mitigated_loss = fx_impact_raw * (1 - hedge_ratio)
    
    # Adjusted Liquidity before defaults
    liquidity_post_fx = usd_static_amount + fx_exposed_amount + fx_mitigated_loss
    
    # Calculate D-Rating Exposure (Impacted by FX and Hedge)
    d_exposure_raw = (invoices[invoices['ESG_Score'] == 'D']['Amount'].sum() / 1_000_000)
    # We assume D-exposure follows the same 40% FX distribution
    d_exposure_fx_impact = (d_exposure_raw * 0.40 * -0.05 * (1 - hedge_ratio))
    d_exposure_adjusted = d_exposure_raw + d_exposure_fx_impact
    
    # Strategy Outcomes
    net_loss_collections = d_exposure_adjusted * (1 - (recovery_rate / 100))
    liquidity_collections = liquidity_post_fx - net_loss_collections
    
    net_loss_insurance = (d_exposure_adjusted * 0.10) + insurance_cost
    liquidity_insurance = liquidity_post_fx - net_loss_insurance

    # --- DECISION METRICS ---
    st.divider()
    met1, met2, met3 = st.columns(3)
    met1.metric("Hedged FX Loss", f"${fx_mitigated_loss:.2f}M", f"{hedge_ratio*100:.0f}% Coverage")
    met2.metric("Portfolio Value", f"${liquidity_post_fx:.1f}M", f"{fx_impact_raw - fx_mitigated_loss:+.2f}M Mitigated")
    
    # Verdict Logic
    if stress_active:
        if liquidity_insurance > liquidity_collections:
            met3.metric("Strategic Verdict", "🛡️ Insure", f"Save ${liquidity_insurance - liquidity_collections:.1f}M")
        else:
            met3.metric("Strategic Verdict", "📞 Collect", f"Save ${liquidity_collections - liquidity_insurance:.1f}M")

    # --- VISUALS ---
    st.divider()
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📉 Hedge Effectiveness Waterfall")
        fig_water = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["absolute", "relative", "relative", "total"],
            x = ["Base Assets", "Unhedged FX Drop", "Forward Hedge Credit", "Net Position"],
            y = [curr_total, fx_impact_raw, (fx_impact_raw * -hedge_ratio), liquidity_post_fx],
            decreasing = {"marker":{"color":"#f85149"}},
            increasing = {"marker":{"color":"#3fb950"}},
            totals = {"marker":{"color":"#1f6feb"}}
        ))
        fig_water.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_water, use_container_width=True)

    with c2:
        st.subheader("🛡️ Residual Risk Exposure")
        # Display how much of the original $292M is now "at risk"
        labels = ['Hedged/Safe', 'FX Risk', 'Credit Risk']
        values = [liquidity_post_fx - net_loss_collections, abs(fx_mitigated_loss), net_loss_collections]
        fig_donut = px.pie(names=labels, values=values, hole=0.5, template="plotly_dark",
                          color_discrete_sequence=['#3fb950', '#d29922', '#f85149'])
        fig_donut.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_donut, use_container_width=True)
        

# --- TAB 2: ANALYST WORKBENCH ---
elif menu == "⚡ Analyst Workbench":
    st.subheader("📥 Active Bank Feed")
    st.dataframe(bank_feed, use_container_width=True, hide_index=True)
    
    if not bank_feed.empty:
        w1, w2 = st.columns([1, 2])
        with w1:
            st.subheader("Step 1: Focus Item")
            tx_selection = st.selectbox("Select Bank Transaction", bank_feed.index, 
                                       format_func=lambda x: f"{bank_feed.iloc[x]['Payer_Name']} | {bank_feed.iloc[x]['Amount_Received']}")
            tx = bank_feed.iloc[tx_selection]
            st.info(f"**Target:** {tx['Payer_Name']} | **Sum:** {tx['Currency']} {tx['Amount_Received']:,.2f}")

        with w2:
            st.subheader("Step 2: AI Match Execution")
            if st.button("🔥 Execute Multi-Factor Matching"):
                results = st.session_state.engine.run_match(tx['Amount_Received'], tx['Payer_Name'], tx['Currency'], invoices)
                if results:
                    match = results[0]
                    st.success(f"✅ **STP MATCH FOUND: {match['confidence']*100:.1f}% Confidence**")
                    st.session_state.vault.log_action(match['Invoice_ID'], "AUTO_MATCH_STP", tx['Amount_Received'])
                else:
                    st.error("❌ No suitable candidates found.")

# --- TAB 3: RISK RADAR (Restored & Enhanced) ---
elif menu == "🛡️ Risk Radar":
    st.subheader("🌎 Institutional Risk Exposure (ESG Weighted)")
    
    if 'ESG_Score' in invoices.columns and 'Company_Code' in invoices.columns:
        # 1. Define Weighting Logic
        rating_weights = {'AAA': 0.05, 'AA': 0.15, 'A': 0.25, 'B': 0.40, 'C': 0.60, 'D': 0.80}
        invoices['Risk_Factor'] = invoices['ESG_Score'].map(rating_weights)
        invoices['Weighted_Risk'] = invoices['Amount'] * invoices['Risk_Factor']
        
        name_col = 'Customer' if 'Customer' in invoices.columns else 'Customer_Name'
        
        # 2. Enhanced Sunburst with Full Hover Context
        fig_sun = px.sunburst(
            invoices, 
            path=['Company_Code', 'Currency', name_col, 'ESG_Score'], 
            values='Weighted_Risk',
            color='ESG_Score',
            color_discrete_map={'AAA':'#238636', 'AA':'#2ea043', 'A':'#3fb950', 'B':'#d29922', 'C':'#db6d28', 'D':'#f85149'},
            hover_data={
                'Amount': ':,.2f',        # Show raw amount
                'Weighted_Risk': ':,.2f', # Show risk amount
                'Risk_Factor': ':.0%',    # Show multiplier
                'Company_Code': True,
                'Currency': True
            },
            template="plotly_dark",
            title="Institutional Risk Hierarchy (By Weighted Exposure)"
        )

        # This ensures the tooltip shows the parent path (Hierarchy) + our custom metrics
        fig_sun.update_traces(
            hovertemplate="<b>%{label}</b><br>" + 
                          "Weighted Risk: %{value:,.2f}<br>" + 
                          "Raw Amount: %{customdata[0]:,.2f}<br>" + 
                          "Risk Multiplier: %{customdata[2]:.0%}<br>" +
                          "Total Path: %{id}"
        )
        
        st.plotly_chart(fig_sun, use_container_width=True)

      # 3. ENHANCED: Detailed Exposure Ledger with Multi-Filter
        st.divider()
        st.subheader("📜 Detailed Exposure Ledger")
        
        # UI for Filtering
        expander = st.expander("🔍 Filter & Search Options", expanded=False)
        with expander:
            f1, f2, f3 = st.columns(3)
            with f1:
                search_query = st.text_input("Search Customer Name", "")
            with f2:
                selected_ratings = st.multiselect("Filter by ESG Rating", options=sorted(invoices['ESG_Score'].unique()), default=sorted(invoices['ESG_Score'].unique()))
            with f3:
                risk_min, risk_max = st.slider("Weighted Risk Range", 0.0, float(invoices['Weighted_Risk'].max()), (0.0, float(invoices['Weighted_Risk'].max())))

        # Apply Filters to the Dataframe
        df_filtered = invoices.copy()
        
        if search_query:
            df_filtered = df_filtered[df_filtered[name_col].str.contains(search_query, case=False)]
        
        df_filtered = df_filtered[df_filtered['ESG_Score'].isin(selected_ratings)]
        df_filtered = df_filtered[(df_filtered['Weighted_Risk'] >= risk_min) & (df_filtered['Weighted_Risk'] <= risk_max)]

        # Prepare for Display
        df_display = df_filtered[[
            'Company_Code', 'Currency', name_col, 'Amount', 'ESG_Score', 'Risk_Factor', 'Weighted_Risk'
        ]].copy()
        
        # Display with Column Config for better visuals
        st.dataframe(
            df_display.sort_values(by='Weighted_Risk', ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Amount": st.column_config.NumberColumn(format="$%.2f"),
                "Weighted_Risk": st.column_config.NumberColumn(format="$%.2f"),
                "Risk_Factor": st.column_config.ProgressColumn(
                    "Risk Intensity",
                    help="The risk multiplier applied based on ESG Score",
                    format="%.2f",
                    min_value=0,
                    max_value=1
                ),
                "ESG_Score": st.column_config.TextColumn("Rating")
            }
        )
        st.caption(f"Showing {len(df_filtered)} of {len(invoices)} exposure records.")
        
    else:
        st.error("Schema Mismatch: Please ensure invoices.csv contains 'Company_Code' and 'ESG_Score'.")
    
        
# --- TAB 4: AUDIT LEDGER ---
elif menu == "📜 Audit Ledger":
    st.subheader("🔐 SOC2 Compliance Vault (Immutable)")
    st.info("Real-time feed from the SHA-256 Hashed Audit Ledger.")
    logs = st.session_state.vault.get_logs()
    st.dataframe(logs, use_container_width=True, hide_index=True)
