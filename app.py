"""
Customer Churn Dashboard - Main Application

Entry point for Streamlit multi-page app.
Configures app layout, page settings, and global state.
"""

import streamlit as st
from src.config import get_app_config
from src.utils import setup_logging


def configure_app():
    """Configure Streamlit page settings and layout."""
    app_config = get_app_config()
    
    st.set_page_config(
        page_title=app_config.app_title,
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Setup logging
    setup_logging(debug_mode=app_config.debug_mode)


def initialize_session_state():
    """Initialize session state variables for multi-page app."""
    if 'dataframe' not in st.session_state:
        st.session_state.dataframe = None
    
    if 'validation_report' not in st.session_state:
        st.session_state.validation_report = None
    
    if 'uploaded_filename' not in st.session_state:
        st.session_state.uploaded_filename = None


def render_home_page():
    """Render the home/landing page."""
    st.title("📊 Customer Churn Dashboard")
    st.subheader("Data Analysis and Customer Insights")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### What is this dashboard?
        This application helps you understand customer churn patterns,
        identify at-risk customers, and make data-driven retention decisions.
        
        ### How to get started:
        1. **Upload Data** - Use the Settings page to upload your CSV
        2. **Explore Dashboard** - View customer analytics and visualizations
        3. **Analyze Statistics** - Deep dive into key metrics
        4. **Understand Insights** - See projections and trends
        """)
    
    with col2:
        st.info("""
        #### Requirements
        Your CSV must contain these columns:
        - Age
        - Gender  
        - Tenure
        - Support Calls
        - Total Spend
        - Churn
        
        #### Supported file
        - CSV format (.csv)
        """)


def main():
    """Main app entry point."""
    configure_app()
    initialize_session_state()
    
    # Logo/Title in sidebar
    st.sidebar.title("📊 Churn Dashboard")
    
    # Check if data is loaded
    data_loaded = st.session_state.dataframe is not None
    
    if data_loaded:
        st.sidebar.success(f"✓ Data Loaded: {st.session_state.uploaded_filename}")
    else:
        st.sidebar.warning("⚠ No data loaded. Go to Settings to upload data.")
    
    # Page navigation
    st.sidebar.markdown("---")
    st.sidebar.subheader("Navigation")
    
    page = st.sidebar.radio(
        "Select Page",
        ["Home", "Dashboard", "Analytics", "Settings"],
        label_visibility="collapsed"
    )
    
    # Route to pages
    if page == "Home":
        render_home_page()
    
    elif page == "Dashboard":
        if data_loaded:
            from pages.dashboard import show_dashboard
            show_dashboard()
        else:
            st.error("❌ Please upload data in Settings page first.")
    
    elif page == "Analytics":
        if data_loaded:
            from pages.analytics import show_analytics
            show_analytics()
        else:
            st.error("❌ Please upload data in Settings page first.")
    
    elif page == "Settings":
        from pages.settings import show_settings
        show_settings()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<small style='text-align: center; color: gray;'>"
        "Customer Churn Dashboard v2.0 | Refactored for Production</small>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
