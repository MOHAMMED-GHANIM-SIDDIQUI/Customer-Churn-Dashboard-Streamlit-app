"""
Utility functions and helpers.

Logging, caching, and other helper functions used throughout the application.
"""

import logging
import functools
from typing import Callable, Any, Optional, Tuple
import streamlit as st


logger = logging.getLogger(__name__)


def setup_logging(debug_mode: bool = False) -> None:
    """
    Configure logging for the application.
    
    Args:
        debug_mode: If True, enables DEBUG level logging
    """
    level = logging.DEBUG if debug_mode else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
        ]
    )


def log_error(func_name: str, error: Exception, context: str = "") -> None:
    """
    Log an error with context.
    
    Args:
        func_name: Name of function where error occurred
        error: Exception object
        context: Additional context about the error
    """
    logger.error(
        f"Error in {func_name}: {str(error)}. Context: {context}",
        exc_info=True
    )


def handle_errors(func: Callable) -> Callable:
    """
    Decorator to wrap function execution with error handling.
    
    Catches exceptions and logs them with traceback.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_error(func.__name__, e, f"args={args}, kwargs={kwargs}")
            raise
    return wrapper


def streamlit_cache_with_ttl(ttl_seconds: int = 3600):
    """
    Decorator combining Streamlit caching with TTL (time-to-live).
    
    Uses Streamlit's @st.cache_data with specified TTL.
    
    Args:
        ttl_seconds: Cache TTL in seconds (default 1 hour)
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        return st.cache_data(ttl=ttl_seconds)(func)
    return decorator


def format_currency(value: float, currency_symbol: str = "$") -> str:
    """
    Format number as currency string.
    
    Args:
        value: Numeric value to format
        currency_symbol: Currency symbol (default "$")
        
    Returns:
        Formatted currency string
    """
    return f"{currency_symbol}{value:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format number as percentage string.
    
    Args:
        value: Numeric value between 0 and 1
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def format_integer_with_commas(value: int) -> str:
    """
    Format integer with thousands separators.
    
    Args:
        value: Integer to format
        
    Returns:
        Formatted string
    """
    return f"{value:,}"


def get_risk_color(risk_category: str) -> str:
    """
    Get color code for risk category.
    
    Args:
        risk_category: One of 'Low', 'Medium', 'High'
        
    Returns:
        Hex color code
    """
    colors = {
        'Low': '#2ca02c',      # Green
        'Medium': '#ff7f0e',   # Orange
        'High': '#d62728',     # Red
    }
    return colors.get(risk_category, '#cccccc')  # Gray default


def get_metric_label_description(metric_name: str) -> Tuple[str, str]:
    """
    Get display label and description for a metric.
    
    Args:
        metric_name: Metric key name
        
    Returns:
        Tuple of (display_label, description)
    """
    metric_descriptions = {
        'average_age': ('Average Customer Age', 'Mean age of all customers'),
        'average_tenure': ('Average Tenure', 'Mean months as customer'),
        'total_spend': ('Total Spend', 'Sum of all customer spending'),
        'average_spend': ('Average Spend', 'Mean spend per customer'),
        'average_support_calls': ('Avg Support Calls', 'Mean support contacts per customer'),
        'churn_rate_percent': ('Churn Rate', 'Percentage of customers who left'),
        'payment_delay_std_dev': ('Payment Delay Std Dev', 'Variability in payment delays'),
    }
    
    if metric_name in metric_descriptions:
        return metric_descriptions[metric_name]
    
    return (metric_name, "")


def validate_dataframe_not_empty(df) -> bool:
    """
    Check if DataFrame has data.
    
    Args:
        df: DataFrame to check
        
    Returns:
        True if DataFrame has rows, False otherwise
    """
    if df is None or len(df) == 0:
        return False
    return True


def safe_divide(numerator: float, denominator: float, 
                default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Value to return if denominator is 0
        
    Returns:
        Result of division or default value
    """
    if denominator == 0:
        return default
    return numerator / denominator
