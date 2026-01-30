import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_risk_radar(df):
    """
    Renders the Institutional Risk Radar (Sunburst).
    Preserves the Currency -> Customer -> ESG hierarchy.
    """
    st.subheader("Institutional Risk Radar")
    
    # Ensuring data exists for the sunburst path
    fig = px.sunburst(
        df, 
        path=['Currency', 'Customer_Name', 'ESG_Score'], 
        values='Amount',
        color='ESG_Score',
        color_discrete_map={
            'AA': '#1a9641', # Deep Green
            'A': '#a6d96a',  # Light Green
            'B': '#fdae61',  # Orange
            'C': '#d7191c'   # Red
        },
        template="plotly_dark",
        maxdepth=2
    )
    
    fig.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)



def render_liquidity_waterfall(opening_cash, expected_ar, stressed_ar):
    """
    Renders the Liquidity Bridge (Waterfall).
    Visualizes the gap between expected and stressed cash flow.
    """
    st.subheader("Liquidity Bridge (Stressed)")
    
    fig = go.Figure(go.Waterfall(
        name="Liquidity", orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=["Opening Cash", "Collections (Expected)", "Stress Haircut", "Net Position"],
        textposition="outside",
        text=[f"${opening_cash}M", f"+${expected_ar}M", f"-${stressed_ar}M", "Total"],
        y=[opening_cash, expected_ar, -stressed_ar, 0],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        increasing={"marker": {"color": "#2ea043"}},
        decreasing={"marker": {"color": "#da3633"}},
        totals={"marker": {"color": "#58a6ff"}}
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, l=20, r=20, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)
