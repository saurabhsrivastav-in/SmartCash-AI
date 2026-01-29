import streamlit as st
import requests

st.set_page_config(page_title="SmartCash AI Dashboard", layout="wide")
st.title("🏦 SmartCash AI: Analyst Workbench")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Process New Payment")
    payer = st.text_input("Payer Name", "Walamrt Inc")
    amt = st.number_input("Amount", value=5000.00)
    ref = st.text_input("Remittance Ref", "INV-1001")
    
    if st.button("Run AI Matcher"):
        # This would call your FastAPI backend
        payload = {"payer_name": payer, "amount": amt, "remittance_ref": ref}
        # For demo purposes, we simulate the logic here
        st.success("STP Successful: Payment applied to INV-1001")

with col2:
    st.subheader("📈 Performance Metrics")
    st.metric("STP Rate", "92%", "+4% vs Last Month")
    st.metric("Unapplied Cash", "$12,450", "-15% improvement")
    st.write("Current Exception Queue: **3 items**")
