"""
Pytest configuration and shared fixtures.

Provides common test fixtures and configuration for all tests.
"""

import pytest
import pandas as pd


@pytest.fixture
def sample_customer_csv():
    """Provide sample customer CSV data for testing."""
    data = """Customer ID,Age,Gender,Tenure,Support Calls,Payment Delay,Subscription Type,Contract Length,Total Spend,Churn
C001,25,Male,12,5,5,Basic,Month-to-Month,500,0
C002,30,Female,24,3,10,Standard,1 Year,1000,1
C003,35,Male,36,2,3,Premium,2 Years,1500,0
C004,40,Female,48,4,7,Basic,1 Year,800,1
C005,45,Male,60,1,2,Premium,3 Years,2000,0
C006,28,Female,8,6,8,Basic,Month-to-Month,450,1
C007,32,Male,20,4,4,Standard,1 Year,900,0
C008,38,Female,42,2,1,Premium,3 Years,1800,0
C009,26,Male,5,7,12,Basic,Month-to-Month,350,1
C010,44,Male,55,1,1,Premium,2 Years,2200,0
"""
    return data


@pytest.fixture
def invalid_customer_csv():
    """Provide invalid CSV with missing required columns."""
    data = """Customer ID,Age,Gender
C001,25,Male
C002,30,Female
"""
    return data


@pytest.fixture
def malformed_customer_csv():
    """Provide CSV with invalid data types and values."""
    data = """Customer ID,Age,Gender,Tenure,Support Calls,Payment Delay,Subscription Type,Contract Length,Total Spend,Churn
C001,not_a_number,Male,12,5,5,Basic,Month-to-Month,500,0
C002,30,InvalidGender,24,3,10,Standard,1 Year,1000,1
C003,35,Male,-36,2,3,Premium,2 Years,1500,0
C004,200,Female,48,4,7,InvalidSub,1 Year,800,1
"""
    return data
