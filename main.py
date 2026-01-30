import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. ENTERPRISE CONFIG & STYLING ---
st.set_page_config(page_title="SmartCash AI | Treasury Command", page_icon="🏦", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b1117; color: #e6edf3; }
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #58a6ff; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #161b22; border-radius: 5px; }
    .stDataFrame { border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ADVANCED DATA GENERATOR ---
@st.cache_data
def load_institutional_data():
    customers = ['Tesla', 'EcoEnergy', 'GlobalBlue', 'TechRetail', 'Quantum Dyn', 'Alpha Log', 'Nordic Oil', 'Sino Tech', 'Indo Power', 'Euro Mart']
    entities = ['1000 (US)', '2000 (EU)', '3000 (UK)']
    currencies = {'1000 (US)': 'USD', '2000 (EU)': 'EUR', '3000 (UK)': 'GBP'}
    ratings = ['AAA', 'AA', 'A', 'B', 'C', 'D']
    
    # 150 Invoices
    inv_data = []
    for i in range(150):
        ent = np.random.choice(entities)
        amt = np.random.uniform(50000, 2000000)
        # Dates spreading from late 2025 into early 2026
        due = datetime(2026, 1, 30) - timedelta(days=np.random.randint(-30, 100))
        inv_data.append({
            'Invoice_ID': f"INV-{1000+i}",
            'Company_Code': ent,
            'Customer': np.random.choice(customers),
            'Amount': round(amt, 2),
            'Amount_Remaining': round(amt, 2),
            'Currency': currencies[ent],
            'ESG_Score': np.random.choice(ratings),
            'Due_Date': due.strftime('%Y-%m-%d'),
            'Status': 'Overdue' if due < datetime(2026, 1, 30) else 'Open',
            'Is_Disputed': False,
            'Dispute_Reason': 'N/A',
            'Internal_Notes': ''
        })
    
    # 50 Bank Transactions
    bank_data = []
    for i in range(50):
        ent = np.random.choice(entities)
        payer = np.random.choice(customers) if np.random.random() < 0.8 else "Unidentified Payer"
        bank_data.append({
            'Bank_ID': f"TXN-{8000+i}",
            'Customer': payer,
            'Company_Code': ent,
            'Date': (datetime(2026, 1, 15) + timedelta(days=np.random.randint(0, 15))).strftime('%Y-%m-%d'),
            'Amount_Received': round(np.random.uniform(50000, 1500000), 2),
            'Currency': currencies[ent]
        })
    return pd.DataFrame(inv_data), pd.DataFrame(bank_data)

# --- 3. SESSION STATE MANAGEMENT ---
if 'invoice_ledger' not in st.session_state:
    inv_df, bank_df = load_institutional_data()
    st.session_state.invoice_ledger = inv_df
    st.session_state.bank_feed = bank_df
    st.session_state.audit_log = []
    st.session_state.current_match = None

# Local references for ease of use
df = st.session_state.invoice_ledger
bank_feed = st.session_state.bank_feed

# --- 4. GLOBAL HEADER: SEARCH & SMART CHAT ---
st.title("🏦 SmartCash AI Treasury Command")
col_search, col_chat = st.columns([1, 1])

with col_search:
    search_query = st.text_input("🔍 Global Search", placeholder="Search Invoice ID or Customer...")
    if search_query:
        matches = df[df['Invoice_ID'].str.contains(search_query, case=False) | df['Customer'].str.contains(search_query, case=False)]
        if not matches.empty:
            st.dataframe(matches[['Invoice_ID', 'Customer', 'Amount_Remaining', 'Status']], height=150)

with col_chat:
    chat_input = st.text_input("🤖 Smart Assistant", placeholder="e.g. 'Total in dispute?' or 'Top debtor?'")
    if chat_input:
        q = chat_input.lower()
        if "dispute" in q:
            val = df[df['Is_Disputed'] == True]['Amount_Remaining'].sum()
            st.info(f"🚩 Current cash in dispute: ${val/1e6:.2f}M")
        elif "most" in q or "debtor" in q:
            top = df.sort_values('Amount_Remaining', ascending=False).iloc[0]
            st.info(f"🎯 Top debtor is {top['Customer']} with ${top['Amount_Remaining']/1e6:.2f}M outstanding.")

st.divider()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Controls")
    menu = st.radio("Workspace", ["📈 Executive Dashboard", "🛡️ Risk Radar", "⚡ Analyst Workbench", "📜 Audit Ledger"])
    st.divider()
    latency = st.slider("Collection Latency (Days)", 0, 90, 15)
    entity_filter = st.selectbox("Company Entity", ["Consolidated"] + list(df['Company_Code'].unique()))
    
    if entity_filter != "Consolidated":
        df = df[df['Company_Code'] == entity_filter]

# Calculations for metrics
total_liquidity = (df['Amount_Remaining'].sum() / 1e6) - (latency * 0.12)
current_esg_val = df['ESG_Score'].map({'AAA':100, 'AA':85, 'A':75, 'B':50, 'C':30, 'D':0}).mean()

# --- 6. WORKSPACE ROUTING ---

if menu == "📈 Executive Dashboard":
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Adjusted DSO", f"{34 + latency} Days", f"+{latency}d Drift")
    m2.metric("Liquidity Pool", f"${total_liquidity:.2f}M", "Real-time")
    m3.metric("ESG Health", f"{current_esg_val:.1f}", "Portfolio")
    
    # Ageing Logic
    today = datetime(2026, 1, 30)
    df_overdue = df[df['Status'] == 'Overdue'].copy()
    def get_bucket(d):
        delta = (today - datetime.strptime(d, '%Y-%m-%d')).days
        if delta <= 30: return "0-30 Days"
        elif delta <= 60: return "31-60 Days"
        elif delta <= 90: return "61-90 Days"
        else: return "90+ Days"
    
    if not df_overdue.empty:
        df_overdue['Bucket'] = df_overdue['Due_Date'].apply(get_bucket)
        ageing_sum = df_overdue.groupby('Bucket')['Amount_Remaining'].sum().reindex(["0-30 Days", "31-60 Days", "61-90 Days", "90+ Days"], fill_value=0).reset_index()
        m4.metric("90+ Day Risk", f"${ageing_sum.iloc[3]['Amount_Remaining']/1e6:.1f}M", "Critical", delta_color="inverse")
    
    st.subheader("⏳ AR Ageing Analysis")
    fig_age = px.bar(ageing_sum, x='Bucket', y='Amount_Remaining', color='Bucket', 
                     color_discrete_map={"0-30 Days":"#3fb950", "31-60 Days":"#d29922", "61-90 Days":"#db6d28", "90+ Days":"#f85149"})
    st.plotly_chart(fig_age, use_container_width=True)

    # Recovery Simulator
    st.divider()
    c_rec1, c_rec2 = st.columns([1, 2])
    with c_rec1:
        st.subheader("🔮 Recovery Simulator")
        rec_toggle = st.toggle("Simulate 90+ Day Recovery")
        if rec_toggle:
            rate = st.slider("Success Rate (%)", 0, 100, 50)
            potential = (ageing_sum.iloc[3]['Amount_Remaining'] * (rate/100))
            st.success(f"Projected Inflow: ${potential/1e6:.2f}M")
    with c_rec2:
        # FX Advisor
        st.subheader("💱 FX Hedging Advisor")
        fx_toggle = st.toggle("Simulate Strong USD Impact")
        if not df_overdue.empty:
            top_fx = df_overdue.groupby('Currency')['Amount_Remaining'].sum().idxmax()
            if fx_toggle and top_fx != 'USD':
                st.error(f"Strategy: SELL {top_fx} / BUY USD immediately to protect {top_fx} receivables.")
            else:
                st.info(f"Strategy: Hold {top_fx}. No immediate hedging drift detected.")

    st.divider()
    if st.button("📊 Generate Executive Board Deck"):
        st.toast("Compiling charts and logic...")
        st.download_button("📥 Download Report.pdf", data="Mock PDF Content", file_name="Treasury_Board_Deck.pdf")

elif menu == "🛡️ Risk Radar":
    # Smart Summary
    disp_val = df[df['Is_Disputed'] == True]['Amount_Remaining'].sum()
    coll_val = df[(df['Status'] == 'Overdue') & (df['Is_Disputed'] == False)]['Amount_Remaining'].sum()
    
    s1, s2, s3 = st.columns(3)
    s1.metric("🚩 In Dispute", f"${disp_val/1e6:.2f}M", f"{len(df[df['Is_Disputed']])} Items")
    s2.metric("✅ Collectible", f"${coll_val/1e6:.2f}M", "Actionable")
    s3.metric("📈 Dispute Ratio", f"{(disp_val/(df['Amount_Remaining'].sum())*100):.1f}%", "Portfolio Friction")

    st.divider()
    # Ledger with Flags
    st.subheader("🔍 Exposure Ledger")
    display_df = df.copy()
    display_df['Status'] = display_df.apply(lambda x: "🚩 DISPUTED" if x['Is_Disputed'] else x['Status'], axis=1)
    st.dataframe(display_df[['Invoice_ID', 'Customer', 'Amount_Remaining', 'Currency', 'Status', 'Due_Date', 'Dispute_Reason']], use_container_width=True)

elif menu == "⚡ Analyst Workbench":
    st.subheader("⚡ Smart Matching & Dispute Resolver")
    t1, t2, t3 = st.tabs(["🧩 Automated Matching", "📩 Dunning Center", "🛠️ Dispute Resolver"])
    
    with t1:
        bank_feed['display_label'] = bank_feed['Bank_ID'] + " | " + bank_feed['Customer'] + " | " + bank_feed['Company_Code'] + " | " + bank_feed['Date'] + " | $" + bank_feed['Amount_Received'].astype(str)
        selected_bank = st.selectbox("Select Bank Transaction", bank_feed['display_label'])
        txn = bank_feed[bank_feed['display_label'] == selected_bank].iloc[0]
        
        if st.button("🔥 Run AI Matcher"):
            matches = df[(df['Customer'] == txn['Customer']) & (df['Company_Code'] == txn['Company_Code'])]
            if not matches.empty:
                st.session_state.current_match = matches.iloc[0]
                st.success(f"Match Found: {st.session_state.current_match['Invoice_ID']}")
        
        if st.session_state.current_match is not None:
            m = st.session_state.current_match
            col_a, col_b = st.columns(2)
            with col_a:
                partial = st.toggle("Partial Payment Mode")
                pay_amt = st.number_input("Amount to Apply", value=float(txn['Amount_Received'])) if partial else float(m['Amount_Remaining'])
            with col_b:
                if st.button("📤 Post to ERP"):
                    idx = st.session_state.invoice_ledger.index[st.session_state.invoice_ledger['Invoice_ID'] == m['Invoice_ID']][0]
                    if partial and pay_amt < m['Amount_Remaining']:
                        st.session_state.invoice_ledger.at[idx, 'Amount_Remaining'] -= pay_amt
                        st.session_state.audit_log.insert(0, {"Action": "Partial Payment", "Inv": m['Invoice_ID'], "Amt": pay_amt})
                    else:
                        st.session_state.invoice_ledger.drop(idx, inplace=True)
                        st.session_state.audit_log.insert(0, {"Action": "Full Clear", "Inv": m['Invoice_ID'], "Amt": pay_amt})
                    st.session_state.current_match = None
                    st.rerun()
                
                if st.button("🚩 Flag Dispute"):
                    idx = st.session_state.invoice_ledger.index[st.session_state.invoice_ledger['Invoice_ID'] == m['Invoice_ID']][0]
                    st.session_state.invoice_ledger.at[idx, 'Is_Disputed'] = True
                    st.rerun()

    with t2:
        # Professional Dunning Template Logic
        overdue_list = df[(df['Status'] == 'Overdue') & (df['Is_Disputed'] == False)]
        if not overdue_list.empty:
            cust = st.selectbox("Customer", overdue_list['Customer'].unique())
            inv_row = overdue_list[overdue_list['Customer'] == cust].iloc[0]
            st.text_area("Email Draft", f"Subject: Overdue Payment {inv_row['Invoice_ID']}\n\nDear {cust},\n\nOur records show an outstanding balance of {inv_row['Currency']} {inv_row['Amount_Remaining']:,.2f}...")
        else: st.info("No actionable overdue items.")

    with t3:
        disputed = df[df['Is_Disputed'] == True]
        if not disputed.empty:
            target = st.selectbox("Resolve Dispute", disputed['Invoice_ID'])
            reason = st.selectbox("Reason Code", ["Damaged Goods", "Pricing Error", "Short Shipment"])
            notes = st.text_area("Investigation Notes")
            if st.button("✅ Save & Resolve"):
                idx = st.session_state.invoice_ledger.index[st.session_state.invoice_ledger['Invoice_ID'] == target][0]
                st.session_state.invoice_ledger.at[idx, 'Is_Disputed'] = False
                st.session_state.invoice_ledger.at[idx, 'Dispute_Reason'] = reason
                st.rerun()
        else: st.success("No active disputes.")

elif menu == "📜 Audit Ledger":
    st.table(st.session_state.audit_log)
