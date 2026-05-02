"""
Configuration module for Customer Churn Dashboard.

Centralized settings for column mapping, projection logic, and app configuration.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ColumnMapping:
    """
    Maps expected CSV column names.
    
    Provides a single source of truth for column references across the application.
    If CSV column names differ, update these mappings.
    """
    customer_id: str = "Customer ID"
    age: str = "Age"
    gender: str = "Gender"
    tenure: str = "Tenure"
    support_calls: str = "Support Calls"
    payment_delay: str = "Payment Delay"
    subscription_type: str = "Subscription Type"
    contract_length: str = "Contract Length"
    total_spend: str = "Total Spend"
    churn: str = "Churn"

    def get_all_columns(self) -> list[str]:
        """Return list of all expected column names."""
        return [
            self.customer_id,
            self.age,
            self.gender,
            self.tenure,
            self.support_calls,
            self.payment_delay,
            self.subscription_type,
            self.contract_length,
            self.total_spend,
            self.churn,
        ]


@dataclass
class ProjectionConfig:
    """
    Business logic parameters for future projections.
    
    These values are used to estimate next-year metrics. Adjust based on
    historical company growth patterns.
    """
    
    monthly_growth_rate: float = 0.05
    """Expected monthly revenue growth rate (5%)"""
    
    support_call_increase_multiplier: float = 1.1
    """Factor for projected support calls increase (10% increase)"""
    
    payment_delay_increase_multiplier: float = 1.05
    """Factor for projected payment delays (5% increase)"""
    
    subscription_upgrade_rate: float = 0.15
    """Percentage of Standard/Basic subscribers expected to upgrade (15%)"""
    
    tenure_growth_multiplier: float = 1.2
    """Factor for expected customer tenure growth (20% longer retention)"""


@dataclass
class AppConfig:
    """
    General application configuration.
    
    Controls Streamlit app behavior, caching, and constraints.
    """
    
    max_upload_size_mb: int = 100
    """Maximum file upload size in megabytes"""
    
    debug_mode: bool = False
    """Enable debug logging and error details"""
    
    app_title: str = "Customer Churn Dashboard"
    """Main application title"""
    
    app_description: str = "Data Analysis and Customer Insights"
    """Application subtitle"""


DASHBOARD_THEME = {
    "primary_color": "#1f77b4",
    "secondary_color": "#ff7f0e",
    "background_color": "#f8f9fa",
    "success_color": "#2ca02c",
    "warning_color": "#ff7f0e",
    "error_color": "#d62728",
}


def get_column_mapping() -> ColumnMapping:
    """
    Factory function to get column mapping.
    
    Allows for future enhancement (e.g., loading from environment variables).
    """
    return ColumnMapping()


def get_projection_config() -> ProjectionConfig:
    """
    Factory function to get projection configuration.
    
    Allows for future enhancement (e.g., loading from database).
    """
    return ProjectionConfig()


def get_app_config() -> AppConfig:
    """
    Factory function to get app configuration.
    
    Allows for future enhancement (e.g., loading from .env file).
    """
    return AppConfig()
