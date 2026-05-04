"""
Analytics Page - Statistical Analysis and Insights

Displays detailed statistics, projections, and data exploration.
"""

import streamlit as st
from src.analytics import ChurnAnalytics
from src.config import get_column_mapping, get_projection_config
from src.utils import format_currency, format_percentage, format_integer_with_commas


def show_analytics():
    """Render the Analytics page with detailed statistics and insights."""
    st.title("📈 Analytics & Insights")
    st.markdown("Deep dive into customer metrics and trends")
    st.markdown("---")
    
    # Get dataframe from session state
    df = st.session_state.dataframe
    
    # Initialize analytics engine
    analytics = ChurnAnalytics(df)
    
    # Create tabs for different analysis views
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Statistics", "🔮 Projections", "🔍 Data Explorer", "ℹ️ About Dataset"]
    )
    
    # TAB 1: Customer Statistics
    with tab1:
        render_statistics_tab(analytics)
    
    # TAB 2: Future Projections
    with tab2:
        render_projections_tab(analytics)
    
    # TAB 3: Data Explorer
    with tab3:
        render_data_explorer_tab(analytics)
    
    # TAB 4: Dataset Info
    with tab4:
        render_about_dataset_tab(analytics)


def render_statistics_tab(analytics: ChurnAnalytics):
    """
    Render customer statistics in a formatted grid.
    
    Args:
        analytics: ChurnAnalytics instance
    """
    st.subheader("Customer Statistics")
    
    stats = analytics.calculate_basic_statistics()
    
    # Display as metric grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Average Age",
            f"{stats['average_age']:.1f} years",
            help="Mean age of all customers"
        )
    
    with col2:
        st.metric(
            "Average Tenure",
            f"{stats['average_tenure']:.1f} months",
            help="Mean months as customer"
        )
    
    with col3:
        st.metric(
            "Total Spend",
            format_currency(stats['total_spend']),
            help="Sum of all customer spending"
        )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Average Spend",
            format_currency(stats['average_spend']),
            help="Mean spend per customer"
        )
    
    with col2:
        st.metric(
            "Avg Support Calls",
            f"{stats['average_support_calls']:.2f}",
            help="Mean support contacts per customer"
        )
    
    with col3:
        st.metric(
            "Churn Rate",
            f"{stats['churn_rate_percent']:.2f}%",
            help="Percentage of customers who churned"
        )
    
    # Additional metrics
    st.write("")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Payment Delay Std Dev",
            f"{stats['payment_delay_std_dev']:.2f} days",
            help="Variability in payment delays"
        )
    
    # Breakdown by subscription type
    st.subheader("Breakdown by Subscription Type")
    spend_by_sub = analytics.get_average_spend_by_subscription()
    
    col1, col2, col3 = st.columns(3)
    for i, (sub_type, avg_spend) in enumerate(spend_by_sub.items()):
        if i % 3 == 0:
            col = col1
        elif i % 3 == 1:
            col = col2
        else:
            col = col3
        
        with col:
            st.metric(
                f"{sub_type} Avg Spend",
                format_currency(avg_spend)
            )
    
    # Churn rate by gender
    st.subheader("Churn Rate by Gender")
    churn_by_gender = analytics.get_churn_rate_by_gender()
    
    col1, col2, col3 = st.columns(3)
    for i, (gender, rate) in enumerate(churn_by_gender.items()):
        with [col1, col2, col3][i]:
            st.metric(
                f"{gender} Churn Rate",
                format_percentage(rate / 100)
            )


def render_projections_tab(analytics: ChurnAnalytics):
    """
    Render future projections for next 12 months.
    
    Args:
        analytics: ChurnAnalytics instance
    """
    st.subheader("12-Month Projections")
    st.info(
        "Based on current trends and configured growth rates. "
        "Update configuration values to adjust projections."
    )
    
    projections = analytics.calculate_projections_next_year()
    
    # Display projections in a readable format
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Projected Revenue (Next Year)",
            format_currency(projections['projected_total_spend_next_year']),
            help="Estimated total spending in next 12 months"
        )
    
    with col2:
        st.metric(
            "Projected Churn Count",
            format_integer_with_commas(
                int(projections['projected_churn_count_next_year'])
            ),
            help="Estimated number of customers who will churn"
        )
    
    with col3:
        st.metric(
            "Projected Support Calls",
            f"{projections['projected_support_calls_increase']:.0f}",
            help="Estimated average support calls increase"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Projected Payment Delay",
            f"{projections['projected_payment_delay_increase']:.1f} days",
            help="Estimated average payment delay increase"
        )
    
    with col2:
        st.metric(
            "Projected Subscription Upgrades",
            format_integer_with_commas(
                int(projections['projected_subscription_upgrades'])
            ),
            help="Estimated Standard/Basic subscribers upgrading to Premium"
        )
    
    # Explanation of methodology
    st.subheader("Projection Methodology")
    
    with st.expander("View calculation details"):
        st.markdown("""
        ### How Projections are Calculated:
        
        1. **Projected Revenue** = Average Monthly Spend × 12 × Growth Rate × Customer Count
        2. **Projected Churn** = Current Churn Rate × Customer Count
        3. **Support Calls** = Current Average × Increase Multiplier
        4. **Payment Delays** = Current Average × Increase Multiplier
        5. **Upgrades** = Standard/Basic Customers × Upgrade Rate
        
        Adjustable parameters in configuration:
        - Monthly Growth Rate: {:.1%}
        - Support Call Increase: {:.0%}
        - Payment Delay Increase: {:.0%}
        - Subscription Upgrade Rate: {:.0%}
        """.format(
            analytics.config.monthly_growth_rate,
            (analytics.config.support_call_increase_multiplier - 1) * 100,
            (analytics.config.payment_delay_increase_multiplier - 1) * 100,
            analytics.config.subscription_upgrade_rate * 100,
        ))


def render_data_explorer_tab(analytics: ChurnAnalytics):
    """
    Render interactive data explorer.
    
    Args:
        analytics: ChurnAnalytics instance
    """
    st.subheader("Data Explorer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Sample Data**")
        sample = analytics.get_customer_sample(n_rows=10)
        st.dataframe(sample, use_container_width=True)
    
    with col2:
        st.write("**Risk Segments**")
        risk_df = analytics.segment_customers_by_risk()
        risk_summary = risk_df['risk_category'].value_counts()
        st.dataframe(risk_summary, use_container_width=True)
        
        st.write("**Risk Scores - Top Customers**")
        top_risk = risk_df.nlargest(5, 'risk_score')
        st.dataframe(top_risk, use_container_width=True)


def render_about_dataset_tab(analytics: ChurnAnalytics):
    """
    Render comprehensive dataset information.
    
    Args:
        analytics: ChurnAnalytics instance
    """
    st.subheader("Dataset Overview")
    
    summary = analytics.get_dataframe_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rows", f"{summary['size']:,}")
    
    with col2:
        st.metric("Total Columns", summary['shape'][1])
    
    with col3:
        missing = sum(summary['missing_values'].values())
        st.metric("Missing Values", missing)
    
    with col4:
        st.metric("Memory Usage", "See info below")
    
    # Column types
    st.subheader("Column Information")
    col_info = []
    for col_name, col_type in summary['column_types'].items():
        missing_count = summary['missing_values'].get(col_name, 0)
        col_info.append({
            'Column': col_name,
            'Type': str(col_type),
            'Missing': missing_count
        })
    
    import pandas as pd
    st.dataframe(pd.DataFrame(col_info), use_container_width=True)
    
    # Statistics
    st.subheader("Statistical Summary")
    if summary['statistics']:
        stats_df = pd.DataFrame(summary['statistics']).T
        st.dataframe(stats_df, use_container_width=True)
    
    # Detailed info
    with st.expander("View detailed DataFrame info"):
        st.code(summary['info'])
