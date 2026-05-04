"""
Customer Churn Dashboard - Source Package

Modules:
- config: Configuration and constants
- models: Data validation using Pydantic
- data_loader: CSV loading and validation
- analytics: Analytics computations
- visualizations: Chart generation
- utils: Helper functions and utilities
"""

from src.config import (
    ColumnMapping,
    ProjectionConfig,
    AppConfig,
    get_column_mapping,
    get_projection_config,
    get_app_config,
)

from src.models import (
    CustomerRecord,
    DataValidationResult,
    validate_dataframe_records,
    validate_required_columns,
)

from src.data_loader import (
    DataLoader,
    DataLoadError,
)

from src.analytics import ChurnAnalytics

from src.visualizations import ChartGenerator

from src.utils import (
    setup_logging,
    log_error,
    handle_errors,
    streamlit_cache_with_ttl,
    format_currency,
    format_percentage,
)

__version__ = "2.0.0"
__author__ = "Refactored by AI"

__all__ = [
    "ColumnMapping",
    "ProjectionConfig",
    "AppConfig",
    "get_column_mapping",
    "get_projection_config",
    "get_app_config",
    "CustomerRecord",
    "DataValidationResult",
    "validate_dataframe_records",
    "validate_required_columns",
    "DataLoader",
    "DataLoadError",
    "ChurnAnalytics",
    "ChartGenerator",
    "setup_logging",
    "log_error",
    "handle_errors",
    "streamlit_cache_with_ttl",
    "format_currency",
    "format_percentage",
]
