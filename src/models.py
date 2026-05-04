"""
Data validation models using Pydantic.

Defines expected data types and validation rules for customer data.
"""

from pydantic import BaseModel, field_validator, ValidationError
from typing import List, Optional
import pandas as pd


class CustomerRecord(BaseModel):
    """
    Represents a single customer record with validation.
    
    Ensures data integrity before processing in analytics.
    """
    
    customer_id: str
    age: int
    gender: str
    tenure: int
    support_calls: int
    payment_delay: int
    subscription_type: str
    contract_length: str
    total_spend: float
    churn: bool

    @field_validator('age')
    @classmethod
    def validate_age(cls, value: int) -> int:
        """Age must be between 0 and 150 years."""
        if not (0 <= value <= 150):
            raise ValueError(f'Age must be between 0 and 150, got {value}')
        return value

    @field_validator('tenure')
    @classmethod
    def validate_tenure(cls, value: int) -> int:
        """Tenure (months) cannot be negative."""
        if value < 0:
            raise ValueError(f'Tenure cannot be negative, got {value}')
        return value

    @field_validator('support_calls')
    @classmethod
    def validate_support_calls(cls, value: int) -> int:
        """Support calls cannot be negative."""
        if value < 0:
            raise ValueError(f'Support calls cannot be negative, got {value}')
        return value

    @field_validator('payment_delay')
    @classmethod
    def validate_payment_delay(cls, value: int) -> int:
        """Payment delay (days) cannot be negative."""
        if value < 0:
            raise ValueError(f'Payment delay cannot be negative, got {value}')
        return value

    @field_validator('total_spend')
    @classmethod
    def validate_total_spend(cls, value: float) -> float:
        """Total spend cannot be negative."""
        if value < 0:
            raise ValueError(f'Total spend cannot be negative, got {value}')
        return value

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, value: str) -> str:
        """Gender must be one of: Male, Female, Other."""
        valid_genders = ['Male', 'Female', 'Other']
        if value not in valid_genders:
            raise ValueError(f'Invalid gender: {value}. Must be one of {valid_genders}')
        return value

    @field_validator('subscription_type')
    @classmethod
    def validate_subscription_type(cls, value: str) -> str:
        """Subscription type must be valid."""
        valid_types = ['Basic', 'Standard', 'Premium']
        if value not in valid_types:
            raise ValueError(f'Invalid subscription type: {value}. Must be one of {valid_types}')
        return value

    @field_validator('contract_length')
    @classmethod
    def validate_contract_length(cls, value: str) -> str:
        """Contract length must be valid."""
        valid_lengths = ['Month-to-Month', '1 Year', '2 Years', '3 Years']
        if value not in valid_lengths:
            raise ValueError(f'Invalid contract length: {value}. Must be one of {valid_lengths}')
        return value


class DataValidationResult(BaseModel):
    """
    Result of validating an entire dataset.
    
    Provides detailed feedback on data quality and issues.
    """
    
    is_valid: bool
    """Whether all records are valid"""
    
    total_records: int
    """Total records in dataset"""
    
    valid_records: int
    """Number of valid records"""
    
    invalid_records: int
    """Number of invalid records"""
    
    errors: List[dict] = []
    """List of validation errors with details"""
    
    warnings: List[str] = []
    """List of warnings (e.g., missing values, unusual distributions)"""


def validate_dataframe_records(df: pd.DataFrame) -> DataValidationResult:
    """
    Validate all records in a DataFrame.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        DataValidationResult with validation status and details
    """
    total_records = len(df)
    valid_records = 0
    invalid_records = 0
    errors = []

    for idx, row in df.iterrows():
        try:
            customer_dict = row.to_dict()
            CustomerRecord(**customer_dict)
            valid_records += 1
        except ValidationError as e:
            invalid_records += 1
            errors.append({
                'row': idx,
                'errors': e.errors()
            })

    warnings = []
    
    # Check for unusually high churn rate
    churn_rate = df['Churn'].mean()
    if churn_rate > 0.5:
        warnings.append(f'High churn rate detected: {churn_rate:.1%}')
    
    # Check for missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        warnings.append(f'Found {missing_count} missing values in dataset')

    return DataValidationResult(
        is_valid=(invalid_records == 0),
        total_records=total_records,
        valid_records=valid_records,
        invalid_records=invalid_records,
        errors=errors,
        warnings=warnings
    )


def validate_required_columns(df: pd.DataFrame, required_columns: list[str]) -> tuple[bool, list[str]]:
    """
    Check if DataFrame contains all required columns.
    
    Args:
        df: DataFrame to check
        required_columns: List of column names that must be present
        
    Returns:
        Tuple of (is_valid, missing_columns)
    """
    missing = [col for col in required_columns if col not in df.columns]
    return (len(missing) == 0, missing)
