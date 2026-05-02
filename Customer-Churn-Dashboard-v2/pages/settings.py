"""
Settings Page - Data Upload and Configuration

Handles CSV upload, data validation, and quality reporting.
"""

import streamlit as st
from src.data_loader import DataLoader, DataLoadError
from src.utils import format_integer_with_commas


def show_settings():
    """Render the Settings page for data upload and management."""
    st.title("⚙️ Settings & Data Management")
    st.markdown("---")
    
    # Upload section
    st.subheader("📥 Upload Customer Data")
    st.markdown(
        "Upload a CSV file containing customer data. "
        "The file must contain all required columns."
    )
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="CSV file with customer data including: Age, Gender, Tenure, etc."
    )
    
    if uploaded_file is not None:
        render_upload_results(uploaded_file)
    else:
        st.info("👆 Upload a CSV file to begin")


def render_upload_results(uploaded_file):
    """
    Process uploaded file and display results.
    
    Args:
        uploaded_file: Streamlit uploaded file object
    """
    try:
        # Load and validate data
        data_loader = DataLoader()
        df, validation_report = data_loader.load_and_validate(uploaded_file)
        
        # Store in session state
        st.session_state.dataframe = df
        st.session_state.validation_report = validation_report
        st.session_state.uploaded_filename = uploaded_file.name
        
        st.success(f"✅ Successfully loaded {format_integer_with_commas(len(df))} records")
        
        # Display validation report
        st.subheader("📊 Data Quality Report")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", format_integer_with_commas(len(df)))
        with col2:
            missing = validation_report['missing_values']
            st.metric("Missing Values", missing)
        with col3:
            duplicates = validation_report['duplicate_rows']
            st.metric("Duplicates Removed", duplicates)
        with col4:
            pct_valid = (validation_report['valid_records'] / 
                        validation_report['total_records'] * 100)
            st.metric("Valid Records %", f"{pct_valid:.1f}%")
        
        # Show warnings if any
        if validation_report['warnings']:
            st.warning("⚠️ Warnings")
            for warning in validation_report['warnings']:
                st.write(f"• {warning}")
        
        # Show errors if any
        if validation_report['invalid_records'] > 0:
            st.error(
                f"❌ {validation_report['invalid_records']} invalid records found. "
                "These were removed from the dataset."
            )
            with st.expander("View validation errors"):
                for error_info in validation_report['errors'][:10]:
                    st.write(f"Row {error_info['row']}: {error_info['errors']}")
                
                if len(validation_report['errors']) > 10:
                    st.write(f"... and {len(validation_report['errors']) - 10} more errors")
        
        # Display data preview
        st.subheader("📋 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Display column information
        st.subheader("📌 Column Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Total Columns:** {len(df.columns)}")
            st.write("**Column Names:**")
            for col in df.columns:
                st.write(f"• {col}")
        
        with col2:
            st.write("**Data Types:**")
            for col, dtype in df.dtypes.items():
                st.write(f"• {col}: {dtype}")
        
        # Statistics
        st.subheader("📈 Basic Statistics")
        st.dataframe(df.describe(), use_container_width=True)
    
    except DataLoadError as e:
        st.error(f"❌ Data Loading Error: {str(e)}")
        st.info(
            "Please check that your CSV file contains all required columns "
            "and data is in the correct format."
        )
    
    except Exception as e:
        st.error(f"❌ Unexpected Error: {str(e)}")
        if st.checkbox("Show error details"):
            st.code(str(e), language='python')
