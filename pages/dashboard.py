"""
Dashboard Page - Visual Analytics

Displays key customer visualizations and charts.
"""

import streamlit as st
from src.analytics import ChurnAnalytics
from src.visualizations import ChartGenerator
from src.config import get_column_mapping, get_projection_config


def show_dashboard():
    """Render the Dashboard page with visualizations."""
    st.title("📊 Customer Dashboard")
    st.markdown("Visual analytics and customer insights")
    st.markdown("---")
    
    # Get dataframe from session state
    df = st.session_state.dataframe
    
    # Initialize analytics and visualization engines
    analytics = ChurnAnalytics(df)
    chart_gen = ChartGenerator()
    
    # Get risk segments
    risk_df = analytics.segment_customers_by_risk()
    
    # Dashboard title metrics
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    stats = analytics.calculate_basic_statistics()
    
    with col1:
        st.metric(
            "Total Customers",
            f"{len(df):,}",
            help="Total number of customers in dataset"
        )
    
    with col2:
        st.metric(
            "Churn Rate",
            f"{stats['churn_rate_percent']:.1f}%",
            help="Percentage of customers who churned"
        )
    
    with col3:
        st.metric(
            "Avg Tenure",
            f"{stats['average_tenure']:.1f} mo",
            help="Average customer tenure in months"
        )
    
    with col4:
        st.metric(
            "Total Spend",
            f"${stats['total_spend']:,.0f}",
            help="Sum of all customer spending"
        )
    
    st.markdown("---")
    
    # Charts in 3x2 grid layout
    st.subheader("Customer Demographics & Behavior")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Age Distribution**")
        fig = chart_gen.create_age_distribution(df, use_plotly=False)
        st.pyplot(fig)
    
    with col2:
        st.markdown("**Average Spend by Subscription Type**")
        fig = chart_gen.create_spend_by_subscription(df, use_plotly=False)
        st.pyplot(fig)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Gender Distribution**")
        fig = chart_gen.create_gender_distribution(df, use_plotly=False)
        st.pyplot(fig)
    
    with col2:
        st.markdown("**Total Spend by Contract Length**")
        fig = chart_gen.create_spend_by_contract_length(df, use_plotly=False)
        st.pyplot(fig)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Churn Rate by Gender**")
        fig = chart_gen.create_churn_rate_by_gender(df, use_plotly=False)
        st.pyplot(fig)
    
    with col2:
        st.markdown("**Age Distribution by Gender**")
        fig = chart_gen.create_age_distribution_by_gender(df, use_plotly=False)
        st.pyplot(fig)
    
    st.markdown("---")
    
    # Risk Analysis
    st.subheader("Risk Analysis")
    fig = chart_gen.create_risk_distribution(risk_df, use_plotly=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.pyplot(fig)
    
    with col2:
        risk_counts = risk_df['risk_category'].value_counts()
        st.write("**Risk Breakdown:**")
        for category in ['Low', 'Medium', 'High']:
            if category in risk_counts.index:
                count = risk_counts[category]
                pct = count / len(risk_df) * 100
                st.write(f"• {category}: {count:,} ({pct:.1f}%)")
    
    st.markdown("---")
    
    # Data export section
    st.subheader("📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Customer Data (CSV)",
            data=csv,
            file_name="customer_data.csv",
            mime="text/csv"
        )
    
    with col2:
        risk_csv = risk_df.to_csv(index=False)
        st.download_button(
            label="Download Risk Assessment (CSV)",
            data=risk_csv,
            file_name="customer_risk.csv",
            mime="text/csv"
        )
