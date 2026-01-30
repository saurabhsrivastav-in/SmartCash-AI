import os
import sys
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SmartCash AI | Treasury Command", page_icon="🏦", layout="wide")

# Institutional Dark Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #0b1117; color: #e6edf3; }
    [data-testid="stMetricValue"] { font-size: 32px; font-weight: 700; color: #58a6ff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA INITIALIZATION ---
@st.cache_data
def load_data():
    # Corrected: Using full integers to avoid SyntaxError with 'M'
    inv = pd.DataFrame({
        'Company_Code': ['1000', '1000', '2000', '3000'],
        'Customer': ['Tesla', 'EcoEnergy', 'GlobalBlue', 'TechRetail'],
        'Amount': [5200000, 15000000, 800000, 2100000], 
        'Currency': ['USD', 'USD', 'EUR', 'GBP'],
        'ESG_Score': ['AAA', 'B', 'D', 'A'],
        'Weighted_Risk': [260000, 600000, 640000, 520000]
    })
    # Ensure date logic is fresh for 2026
    bank = pd.DataFrame({
        'Date': [pd.Timestamp('2026-01-25')], 
        'Company_Code': ['1000'], 
        'Amount': [1000000]
    })
    return inv, bank

invoices, bank_feed = load_data()

# Initialize Session States
if 'audit_log' not in st.session_state: 
    st.session_state.audit_log = []

# --- SIDEBAR & GLOBAL CONTROLS ---
with st.sidebar:
    st.title("🏦 SmartCash AI")
    menu = st.radio("Workspace", ["📈 Executive Dashboard", "🛡️ Risk Radar", "📜 Audit Ledger"])
    st.divider()
    st.subheader("⚙️ Global Parameters")
    latency_days = st.slider("Collection Latency (Days)", 0, 90, 15)
    entity = st.selectbox("Company Entity", ["All Entities", "1000", "2000", "3000"])
    st.divider()
    st.subheader("📝 Scenario Governance")
    scenario_name = st.text_input("Scenario Label", "Q1 Assessment")
    scenario_note = st.text_area("Notes", "Simulating high volatility.")

# --- TOP LEVEL METRICS ---
def display_header_metrics():
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Adjusted DSO", f"{34 + latency_days} Days", f"+{latency_days}d Latency")
    m2.metric("Liquidity Buffer", "$292.5M", "+1.4% YoY")
    m3.metric("Avg ESG Score", "Tier B", "Stable")
    m4.metric("Matching Rate", "94.2%", "STP Verified")

# --- DASHBOARD LOGIC ---
if menu == "📈 Executive Dashboard":
    display_header_metrics()
    st.divider()
    
    # 1. DATA CONFIDENCE & FLOW
    c1, c2 = st.columns([1, 2])
    with c1:
        # Confidence Gauge
        fig_conf = go.Figure(go.Indicator(
            mode="gauge+number", value=92, title={'text': "Data Confidence (%)"},
            gauge={'bar':{'color':"#58a6ff"}, 'steps':[{'range':[0,50], 'color':"#f85149"}]}))
        fig_conf.update_layout(height=250, template="plotly_dark", margin=dict(t=50, b=0))
        st.plotly_chart(fig_conf, use_container_width=True)
        
    with c2:
        st.subheader("💹 Cash Flow Forecast (Actual vs. Proj)")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        fig_flow = go.Figure()
        fig_flow.add_trace(go.Scatter(x=months, y=[42, 48, 45, 52, 58, 62], name="2026 Forecast", line=dict(color='#58a6ff', width=4)))
        fig_flow.add_trace(go.Scatter(x=months, y=[38, 41, 40, 46, 50, 52], name="2025 Actual", line=dict(color='#30363d', dash='dot')))
        fig_flow.update_layout(template="plotly_dark", height=280, margin=dict(t=20, b=20))
        st.plotly_chart(fig_flow, use_container_width=True)

    st.divider()

    # 2. STRESS TEST & WATERFALL
    col_ctrl, col_chart = st.columns([1, 2])
    with col_ctrl:
        st.subheader("🚨 Stress Test")
        stress_active = st.toggle("Simulate 'D' Defaults")
        fx_swing = st.toggle("5% USD Strengthening")
        hedge_ratio = st.slider("Hedge Ratio %", 0, 100, 50) / 100 if fx_swing else 0
        
        if st.button("💾 Log Scenario to Ledger"):
            entry = {
                "Timestamp": datetime.now().strftime("%H:%M"), 
                "Label": scenario_name, 
                "Hedge %": f"{hedge_ratio:.0%}",
                "Note": scenario_note
            }
            st.session_state.audit_log.insert(0, entry)
            st.success("Scenario Archived.")

    with col_chart:
        st.subheader("📉 Interactive Hedge Effectiveness")
        base, fx_loss, hedge_gain = 292.5, -14.6, 14.6 * hedge_ratio
        fig_water = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["absolute", "relative", "relative", "total"],
            x = ["Base Assets", "Unhedged FX", "Hedge Recovery", "Net Position"],
            y = [base, fx_loss if fx_swing else 0, hedge_gain if fx_swing else 0, 0],
            connector = {"line":{"color":"#30363d"}},
            decreasing = {"marker":{"color":"#f85149"}},
            increasing = {"marker":{"color":"#3fb950"}},
            totals = {"marker":{"color":"#1f6feb"}}
        ))
        fig_water.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_water, use_container_width=True)

    st.divider()

    # 3. SENSITIVITY HEATMAP
    st.subheader("🔥 Risk Sensitivity Heatmap (Net Liquidity Impact)")
    st.info("Visualizes how FX Volatility vs. Hedge Ratios affect millions of USD in liquidity.")
    
    fx_range = np.linspace(-0.10, 0.02, 5) # -10% to +2%
    hedge_range = np.linspace(0, 1, 5)     # 0% to 100%
    z_data = [[round(117 * f * (1 - h), 2) for h in hedge_range] for f in fx_range]

    fig_heat = px.imshow(
        z_data,
        labels=dict(x="Hedge Ratio", y="FX Swing %", color="Impact ($M)"),
        x=['0%', '25%', '50%', '75%', '100%'],
        y=['-10%', '-7%', '-4%', '-1%', '+2%'],
        color_continuous_scale='RdYlGn',
        aspect="auto",
        text_auto=True
    )
    fig_heat.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_heat, use_container_width=True)

# --- TAB: AUDIT LEDGER ---
elif menu == "📜 Audit Ledger":
    st.subheader("🔐 Treasury Audit Trail")
    if st.session_state.audit_log:
        audit_df = pd.DataFrame(st.session_state.audit_log)
        st.dataframe(audit_df, use_container_width=True, hide_index=True)
    else:
        st.info("No scenarios logged yet. Use the sidebar to archive a scenario.")

# --- TAB: RISK RADAR ---
elif menu == "🛡️ Risk Radar":
    st.subheader("🛡️ Portfolio Risk Radar")
    fig_radar = px.sunburst(invoices, path=['Currency', 'ESG_Score', 'Customer'], values='Amount',
                            color='ESG_Score', color_discrete_map={'AAA':'#238636', 'D':'#f85149'})
    fig_radar.update_layout(template="plotly_dark", height=600)
    st.plotly_chart(fig_radar, use_container_width=True)
