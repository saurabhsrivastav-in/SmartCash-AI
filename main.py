import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. INITIALIZE SESSION STATE (CRITICAL FOR STABILITY) ---
if 'search_key' not in st.session_state:
    st.session_state.search_key = ""
if 'chat_key' not in st.session_state:
    st.session_state.chat_key = ""
if 'audit' not in st.session_state:
    st.session_state.audit = []
if 'ledger' not in st.session_state:
    st.session_state.ledger = None

# --- 2. FIXED CLEAR LOGIC ---
def handle_clear():
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

# --- 4. DATA ENGINE ---
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
    for i in range(50):
        ent = np.random.choice(entities)
        bank_data.append({
            'Bank_ID': f"TXN-{8000+i}",
            'Customer': np.random.choice(customers),
            'Amount_Received': round(np.random.uniform(20000, 1500000), 2)
        })
    return pd.DataFrame(inv_data), pd.DataFrame(bank_data)

if st.session_state.ledger is None:
    st.session_state.ledger, st.session_state.bank = load_institutional_data()

# --- 5. HEADER & SEARCH LOGIC ---
st.title("🏦 SmartCash AI | Treasury Command")
h_col1, h_col2, h_col3 = st.columns([3, 3, 1])
with h_col1:
    search_term = st.text_input("🔍 Global Search (Customer or Invoice #)", key="search_key")
with h_col2:
    chat_term = st.text_input("🤖 AI Assistant", key="chat_key")
with h_col3:
    st.write(" ")
    st.button("🗑️ Clear All", on_click=handle_clear)

st.divider()

# --- 6. DATA FILTERING (THE WORKING SEARCH) ---
# We apply search FIRST, then Entity filters
view_df = st.session_state.ledger.copy()

if search_term:
    view_df = view_df[
        view_df['Customer'].str.contains(search_term, case=False) | 
        view_df['Invoice_ID'].str.contains(search_term, case=False)
    ]

# Sidebar for Entity filter
with st.sidebar:
    st.header("⚙️ Controls")
    menu = st.radio("Workspace", ["📈 Dashboard", "🛡️ Risk Radar", "⚡ Workbench", "📜 Audit"])
    latency = st.slider("Collection Latency (Days)", 0, 90, 15)
    ent_f = st.selectbox("Company Entity", ["Consolidated"] + list(st.session_state.ledger['Company_Code'].unique()))

if ent_f != "Consolidated":
    view_df = view_df[view_df['Company_Code'] == ent_f]

# Calculations based on the dynamic View
liq_pool = (view_df['Amount_Remaining'].sum() / 1e6) - (latency * 0.12)
today = datetime(2026, 1, 30)

# --- 7. WORKSPACE ---

if menu == "📈 Dashboard":
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("BoA Liquidity Tier", "Level 1 (Strong)", "0.02% Var")
    m2.metric("Filtered Liquidity", f"${liq_pool:.2f}M")
    m3.metric("Adjusted DSO", f"{34+latency}d")
    m4.metric("Active Results", len(view_df))

    st.divider()

    # AGEING CHART
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
        
        fig_age = px.bar(age_data, x='Bucket', y='Amount_Remaining', 
                         labels={'Bucket': 'Days Past Due (DPD)', 'Amount_Remaining': 'Balance ($)'},
                         color='Amount_Remaining', color_continuous_scale='Blues')
        fig_age.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_age, use_container_width=True)
    else:
        st.info("No overdue items matching search criteria.")

    st.divider()

    # HEATMAP
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("🛡️ Data Confidence")
        fig_g = go.Figure(go.Indicator(mode="gauge+number", value=max(0, 100-latency),
            gauge={'bar':{'color':"#58a6ff"}, 'steps':[{'range':[0,50], 'color':"#f85149"}]}))
        fig_g.update_layout(height=350, template="plotly_dark")
        st.plotly_chart(fig_g, use_container_width=True)
    
    with c2:
        st.subheader("🔥 Interactive Stress Matrix (Filtered)")
        fx_range = np.array([-15, -10, -5, -2, 0, 5])
        hedge_range = np.array([0, 25, 50, 75, 100])
        z_data = [[round(liq_pool * (1 + (fx/100) * (1 - (h/100))), 2) for h in hedge_range] for fx in fx_range]
        fig_h = go.Figure(data=go.Heatmap(z=z_data, x=[f"{h}% Hedge" for h in hedge_range], y=[f"{fx}% Vol" for fx in fx_range],
            colorscale='RdYlGn', text=z_data, texttemplate="$%{text}M"))
        fig_h.update_layout(template="plotly_dark", height=350, xaxis_title="Hedge Ratio", yaxis_title="FX Vol (%)")
        st.plotly_chart(fig_h, use_container_width=True)

elif menu == "🛡️ Risk Radar":
    # Restored Radar
    weights = {'AAA':0.05, 'AA':0.1, 'A':0.2, 'B':0.4, 'C':0.6, 'D':0.9}
    view_df['Exposure'] = view_df['Amount_Remaining'] * view_df['ESG_Score'].map(weights)
    fig_s = px.sunburst(view_df, path=['Company_Code', 'Currency', 'ESG_Score', 'Customer'], 
                        values='Exposure', color='ESG_Score',
                        color_discrete_map={'AAA':'#238636', 'AA':'#2ea043', 'A':'#d29922', 'B':'#db6d28', 'C':'#f85149', 'D':'#b62323'})
    fig_s.update_layout(height=700, template="plotly_dark")
    st.plotly_chart(fig_s, use_container_width=True)

elif menu == "⚡ Workbench":
    st.subheader("⚡ Operational Command")
    t1, t2, t3 = st.tabs(["🧩 AI Matcher", "📩 Dunning Center", "🛠️ Dispute Resolver"])
    
    with t1:
        st.dataframe(st.session_state.bank, use_container_width=True)
        st.info("Select a transaction from the list to begin AI Matching.")

    with t2:
        ov = view_df[view_df['Status'] == 'Overdue']
        if not ov.empty:
            cust = st.selectbox("Select Debtor", ov['Customer'].unique())
            inv = ov[ov['Customer'] == cust].iloc[0]
            email = f"Subject: Overdue Notice: {inv['Invoice_ID']}\n\nDear {cust},\nYour balance of {inv['Currency']} {inv['Amount_Remaining']} is overdue."
            st.text_area("Email Draft", email, height=200)
            if st.button("📤 Send Notice"):
                st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "DUNNING", "ID": inv['Invoice_ID']})
        else: st.info("Search filter returned no overdue items for dunning.")

    with t3:
        to_f = st.selectbox("Invoice ID", view_df['Invoice_ID'])
        if st.button("🚩 Flag Dispute"):
            st.session_state.audit.insert(0, {"Time": datetime.now().strftime("%H:%M"), "Action": "DISPUTE", "ID": to_f})

elif menu == "📜 Audit":
    st.table(pd.DataFrame(st.session_state.audit))
