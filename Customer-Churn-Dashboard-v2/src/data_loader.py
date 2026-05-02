"""
Data loading and preprocessing module.

Handles CSV loading, validation, and transformation with comprehensive error handling.
"""

import pandas as pd
from typing import Optional, Tuple
import io

from src.config import ColumnMapping, get_column_mapping
from src.models import validate_dataframe_records, validate_required_columns


class DataLoadError(Exception):
    """Raised when data loading or validation fails."""
    pass


class DataLoader:
    """
    Handles loading and validating customer data from various sources.
    
    Provides a clean API for data ingestion with proper error handling.
    """

    def __init__(self, column_mapping: Optional[ColumnMapping] = None):
        """
        Initialize DataLoader.
        
        Args:
            column_mapping: Column name mappings. Uses default if None.
        """
        self.column_mapping = column_mapping or get_column_mapping()

    def load_from_uploaded_file(self, uploaded_file) -> pd.DataFrame:
        """
        Load data from Streamlit uploaded file object.
        
        Args:
            uploaded_file: File object from st.file_uploader()
            
        Returns:
            Loaded and validated DataFrame
            
        Raises:
            DataLoadError: If file cannot be read or contains invalid data
        """
        try:
            if uploaded_file is None:
                raise DataLoadError("No file provided")

            if uploaded_file.name.endswith('.csv'):
                return self.load_from_csv_bytes(uploaded_file.read())
            else:
                raise DataLoadError(f"Unsupported file type: {uploaded_file.name}")

        except DataLoadError:
            raise
        except Exception as e:
            raise DataLoadError(f"Failed to load file: {str(e)}")

    def load_from_csv_bytes(self, csv_bytes: bytes) -> pd.DataFrame:
        """
        Load CSV data from bytes.
        
        Args:
            csv_bytes: Raw bytes of CSV file
            
        Returns:
            Loaded DataFrame
            
        Raises:
            DataLoadError: If CSV cannot be parsed
        """
        try:
            csv_string = csv_bytes.decode('utf-8')
            df = pd.read_csv(io.StringIO(csv_string))
            return df
        except UnicodeDecodeError as e:
            raise DataLoadError(f"File encoding error: {str(e)}")
        except pd.errors.ParserError as e:
            raise DataLoadError(f"CSV parsing error: {str(e)}")
        except Exception as e:
            raise DataLoadError(f"Unexpected error reading CSV: {str(e)}")

    def validate_schema(self, df: pd.DataFrame) -> Tuple[bool, list[str], str]:
        """
        Validate that DataFrame has required columns.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Tuple of (is_valid, missing_columns, error_message)
        """
        required_cols = self.column_mapping.get_all_columns()
        is_valid, missing = validate_required_columns(df, required_cols)

        if not is_valid:
            error_msg = f"Missing required columns: {', '.join(missing)}"
            return False, missing, error_msg

        return True, [], ""

    def validate_data_quality(self, df: pd.DataFrame) -> dict:
        """
        Validate data quality and return detailed report.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary with validation results
        """
        validation_result = validate_dataframe_records(df)

        return {
            'is_valid': validation_result.is_valid,
            'total_records': validation_result.total_records,
            'valid_records': validation_result.valid_records,
            'invalid_records': validation_result.invalid_records,
            'errors': validation_result.errors,
            'warnings': validation_result.warnings,
            'missing_values': int(df.isnull().sum().sum()),
            'duplicate_rows': int(df.duplicated().sum()),
        }

    def clean_data(self, df: pd.DataFrame, remove_duplicates: bool = True,
                   drop_missing: bool = True) -> pd.DataFrame:
        """
        Clean DataFrame by removing duplicates and handling missing values.
        
        Args:
            df: DataFrame to clean
            remove_duplicates: Whether to remove duplicate rows
            drop_missing: Whether to drop rows with missing values
            
        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()

        if remove_duplicates:
            initial_count = len(df_clean)
            df_clean = df_clean.drop_duplicates()
            removed_count = initial_count - len(df_clean)
            if removed_count > 0:
                print(f"Removed {removed_count} duplicate rows")

        if drop_missing:
            initial_count = len(df_clean)
            df_clean = df_clean.dropna()
            removed_count = initial_count - len(df_clean)
            if removed_count > 0:
                print(f"Dropped {removed_count} rows with missing values")

        return df_clean

    def load_and_validate(self, uploaded_file) -> Tuple[pd.DataFrame, dict]:
        """
        Complete pipeline: load, validate schema, validate data, and clean.
        
        Args:
            uploaded_file: File object from st.file_uploader()
            
        Returns:
            Tuple of (cleaned_dataframe, validation_report)
            
        Raises:
            DataLoadError: If any validation step fails
        """
        # Load CSV
        df = self.load_from_uploaded_file(uploaded_file)

        # Validate schema
        is_valid, missing, error_msg = self.validate_schema(df)
        if not is_valid:
            raise DataLoadError(error_msg)

        # Validate data quality
        quality_report = self.validate_data_quality(df)

        # Clean data
        df_clean = self.clean_data(df)

        return df_clean, quality_report
