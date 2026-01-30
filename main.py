import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. BOILERPLATE & STABILITY INITIALIZATION ---
if 'audit' not in st.session_state:
    st.session_state.audit = []
if 'search_key' not in st.session_state:
    st.session_state.search_key = ""
if 'chat_key' not in st.session_state:
    st.session_state.chat_key = ""

# --- 2. DATA ENGINE ---
@st.cache_data
def load_institutional_data():
    customers = ['Tesla', 'EcoEnergy', 'GlobalBlue', 'TechRetail', 'Quantum Dyn', 'Alpha Log', 'Nordic Oil', 'Sino Tech', 'Indo Power', 'Euro Mart']
    entities = ['1000 (US)', '2000 (EU)', '3000 (UK)']
    currencies = {'1000 (US)': 'USD', '2000 (EU)': 'EUR', '3000 (UK)': 'GBP'}
    ratings = ['AAA', 'AA', 'A', 'B', 'C', 'D']
    
    inv_data = []
    for i in range(300):
        ent = np.random.choice(entities)
        amt = np.random.uniform(50000, 2500000)
        due = datetime(2026, 1, 30) - timedelta(days=np.random.randint(-30, 600))
        inv_data.append({
            'Invoice_ID': f"INV-{1000+i}",
            'Company_Code': ent,
            'Customer': np.random.choice(customers),
            'Amount_Remaining': round(amt, 2),
            'Currency': currencies[ent],
            'ESG_Score': np.random.choice(ratings),
            'Due_Date': due.strftime('%Y-%m-%d'),
            'Status': 'Overdue' if due < datetime(2026, 1, 30) else 'Open',
            'Is_Disputed': False
        })
    
    bank_data = []
    for i in range(20):
        bank_data.append({
            'Bank_ID': f"TXN-{8000+i}",
            'Customer': np.random.choice(customers),
            'Amount_Received': round(np.random.uniform(20000, 1500000), 2),
            'Date': (datetime(2026, 1, 15) + timedelta(days=i)).strftime('%Y-%m-%d')
        })
    return pd.DataFrame(inv_data), pd.DataFrame(bank_data)

if 'ledger' not in st.session_state or 'bank' not in st.session_state:
    ledger_df, bank_df = load_institutional_data()
    st.session_state.ledger = ledger_df
    st.session_state.bank = bank_df

def handle_clear():
    st.session_key = "" # Clears the internal state
    st.session_state.search_key = ""
    st.session_state.chat_key = ""

# --- 3. UI CONFIG ---
st.set_page_config(page_title="SmartCash AI | Treasury Command", page_icon="🏦", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b1117; color: #e6edf3; }
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #58a6ff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #161b22; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. HEADER & SEARCH ---
st.title("🏦 SmartCash AI | Treasury Command")
h_col1, h_col2, h_col3 = st.columns([3, 3, 1])
with h_col1:
    search_term = st.text_input("🔍 Global Search", key="search_key", placeholder="Search Customer or Invoice ID...")
with h_col2:
    chat_term = st.text_input("🤖 AI Assistant", key="chat_key", placeholder="Ask me about a customer...")
with h_col3:
    st.write(" ")
    st.button("🗑️ Clear All", on_click=handle_clear)

st.divider()

# --- 5. SEARCH & FILTER LOGIC (FIXED) ---
view_df = st.session_state.ledger.copy()

# Unify both search bars so they both filter the app
active_query = search_term if search_term else chat_term

if active_query:
    view_df = view_df[view_df['Customer'].str.contains(active_query, case=False) | 
                     view_df['Invoice_ID'].str.contains(active_query, case=False)]

with st.sidebar:
    st.header("⚙️ Controls")
    menu = st.radio("Workspace", ["📈 Dashboard", "🛡️ Risk Radar", "⚡ Workbench", "📜 Audit"])
    latency = st.slider("Collection Latency (Days)", 0, 90, 15)
    ent_f = st.selectbox("Company Entity", ["Consolidated"] + list(st.session_state.ledger['Company_Code'].unique()))

if ent_f != "Consolidated":
    view_df = view_df[view_df['Company_Code'] == ent_f]

liq_pool = (view_df['Amount_Remaining'].sum() / 1e6) - (latency * 0.12)
today = datetime(2026, 1, 30)

# --- 6. WORKSPACE ---
if menu == "📈 Dashboard":
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("BoA Liquidity Tier", "Level 1 (Strong)", "0.02% Var")
    m2.metric("Filtered Liquidity", f"${liq_pool:.2f}M")
    m3.metric("Adjusted DSO", f"{34+latency}d")
    m4.metric("Matching Items", len(view_df))
    st.divider()

    st.subheader("⏳ Accounts Receivable Ageing Analysis")
    ov = view_df[view_df['Status'] == 'Overdue'].copy()
    if not ov.empty:
        def get_bucket(d):
            days = (today - datetime.strptime(d, '%Y-%m-%d')).days
            if days <= 15: return "0-15"
            elif days <= 30: return "16-30"
            elif days <= 60: return "31-60"
            elif days <= 90: return "61-90"
            elif days <= 120: return "91-120"
            elif days <= 180: return "121-180"
            elif days <= 360: return "181-360"
            else: return "361-540"
        ov['Bucket'] = ov['Due_Date'].apply(get_bucket)
        order = ["0-15", "16-30", "31-60", "61-90", "91-120", "121-180", "181-360", "361-540"]
        age_data = ov.groupby('Bucket')['Amount_Remaining'].sum().reindex(order, fill_value=0).reset_index()
        fig_age = px.bar(age_data, x='Bucket', y='Amount_Remaining', color='Amount_Remaining', color_continuous_scale='Turbo')
        fig_age.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig_age, use_container_width=True)

    st.divider()
    st.subheader("🔥 Interactive Stress Matrix (FX vs Hedge)")
    fx_range = np.array([-15, -10, -5, -2, 0, 5, 10])
    hedge_range = np.array([0, 25, 50, 75, 100])
    z_data = [[round(liq_pool * (1 + (fx/100) * (1 - (h/100))), 2) for h in hedge_range] for fx in fx_range]
    fig_h = go.Figure(data=go.Heatmap(z=z_data, x=[f"{h}% Hedge" for h in hedge_range], y=[f"{fx}% Vol" for fx in fx_range], colorscale='RdYlGn', text=z_data, texttemplate="$%{text}M"))
    fig_h.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_h, use_container_width=True)

elif menu == "🛡️ Risk Radar":
    weights = {'AAA':0.05, 'AA':0.1, 'A':0.2, 'B':0.4, 'C':0.6, 'D':0.9}
    view_df['Exposure'] = view_df['Amount_Remaining'] * view_df['ESG_Score'].map(weights)
    fig_s = px.sunburst(view_df, path=['Company_Code', 'Currency', 'ESG_Score', 'Customer'], values='Exposure', color='ESG_Score')
    fig_s.update_layout(height=700, template="plotly_dark")
    st.plotly_chart(fig_s, use_container_width=True)

elif menu == "⚡ Workbench":
    st.subheader("⚡ Operational Command")
    t1, t2, t3 = st.tabs(["🧩 AI Matcher", "📩 Dunning Center", "🛠️ Dispute Resolver"])
    with t1:
        st.dataframe(st.session_state.bank, use_container_width=True)
    with t2:
        ov = view_df[view_df['Status'] == 'Overdue']
        if not ov.empty:
            target = st.selectbox("Select Debtor", ov['Customer'].unique())
            inv = ov[ov['Customer'] == target].iloc[0]
            email = f"Subject: URGENT: Payment Overdue {inv['Invoice_ID']}\n\nDear {target},\nBalance of {inv['Currency']} {inv['Amount_Remaining']} is past due."
            st.text_area("Notice Draft", email, height=200)
            if st.button("📤 Dispatch"): st.success("Notice sent.")
    with t3:
        to_f = st.selectbox("Invoice to Freeze", view_df['Invoice_ID'])
        if st.button("🚩 Freeze"): st.warning(f"Invoice {to_f} frozen.")

elif menu == "📜 Audit":
    st.table(pd.DataFrame(st.session_state.audit))
