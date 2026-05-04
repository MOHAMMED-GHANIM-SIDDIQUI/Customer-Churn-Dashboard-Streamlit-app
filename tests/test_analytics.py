"""
Unit tests for analytics module.

Tests core analytics functions with sample data.
"""

import pytest
import pandas as pd
from src.analytics import ChurnAnalytics
from src.config import ColumnMapping, ProjectionConfig


@pytest.fixture
def sample_dataframe():
    """Create a sample customer DataFrame for testing."""
    return pd.DataFrame({
        'Customer ID': ['C001', 'C002', 'C003', 'C004', 'C005'],
        'Age': [25, 30, 35, 40, 45],
        'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
        'Tenure': [12, 24, 36, 48, 60],
        'Support Calls': [5, 3, 2, 4, 1],
        'Payment Delay': [5, 10, 3, 7, 2],
        'Subscription Type': ['Basic', 'Standard', 'Premium', 'Basic', 'Premium'],
        'Contract Length': ['Month-to-Month', '1 Year', '2 Years', '1 Year', '3 Years'],
        'Total Spend': [500, 1000, 1500, 800, 2000],
        'Churn': [0, 1, 0, 1, 0],
    })


@pytest.fixture
def analytics_engine(sample_dataframe):
    """Create analytics engine with sample data."""
    return ChurnAnalytics(sample_dataframe)


class TestChurnAnalyticsBasicStatistics:
    """Tests for basic statistics calculation."""
    
    def test_calculate_basic_statistics_returns_dict(self, analytics_engine):
        """Test that calculate_basic_statistics returns a dictionary."""
        stats = analytics_engine.calculate_basic_statistics()
        assert isinstance(stats, dict)
    
    def test_calculate_basic_statistics_has_required_keys(self, analytics_engine):
        """Test that all required metrics are present."""
        stats = analytics_engine.calculate_basic_statistics()
        required_keys = [
            'average_age',
            'average_tenure',
            'total_spend',
            'average_spend',
            'average_support_calls',
            'churn_rate_percent',
            'payment_delay_std_dev',
        ]
        for key in required_keys:
            assert key in stats, f"Missing metric: {key}"
    
    def test_average_age_calculation(self, sample_dataframe, analytics_engine):
        """Test average age is calculated correctly."""
        stats = analytics_engine.calculate_basic_statistics()
        expected_avg = sample_dataframe['Age'].mean()
        assert stats['average_age'] == pytest.approx(expected_avg, rel=0.01)
    
    def test_churn_rate_is_percentage(self, analytics_engine):
        """Test that churn rate is a percentage (0-100)."""
        stats = analytics_engine.calculate_basic_statistics()
        assert 0 <= stats['churn_rate_percent'] <= 100


class TestChurnAnalyticsProjections:
    """Tests for future projections."""
    
    def test_calculate_projections_returns_dict(self, analytics_engine):
        """Test that projections return a dictionary."""
        projections = analytics_engine.calculate_projections_next_year()
        assert isinstance(projections, dict)
    
    def test_projections_have_required_keys(self, analytics_engine):
        """Test that all required projection metrics are present."""
        projections = analytics_engine.calculate_projections_next_year()
        required_keys = [
            'projected_total_spend_next_year',
            'projected_churn_count_next_year',
            'projected_support_calls_increase',
            'projected_payment_delay_increase',
            'projected_subscription_upgrades',
            'projected_tenure_growth',
        ]
        for key in required_keys:
            assert key in projections, f"Missing projection: {key}"
    
    def test_projections_are_positive(self, analytics_engine):
        """Test that projections produce positive values."""
        projections = analytics_engine.calculate_projections_next_year()
        for key, value in projections.items():
            assert value >= 0, f"Projection {key} is negative: {value}"


class TestChurnAnalyticsSegmentation:
    """Tests for customer segmentation."""
    
    def test_segment_by_risk_returns_dataframe(self, analytics_engine):
        """Test that segmentation returns a DataFrame."""
        segments = analytics_engine.segment_customers_by_risk()
        assert isinstance(segments, pd.DataFrame)
    
    def test_segment_by_risk_has_required_columns(self, analytics_engine):
        """Test that risk segmentation has required columns."""
        segments = analytics_engine.segment_customers_by_risk()
        assert 'risk_score' in segments.columns
        assert 'risk_category' in segments.columns
    
    def test_risk_score_range(self, analytics_engine):
        """Test that risk scores are between 0 and 1."""
        segments = analytics_engine.segment_customers_by_risk()
        assert (segments['risk_score'] >= 0).all()
        assert (segments['risk_score'] <= 1).all()
    
    def test_risk_categories_are_valid(self, analytics_engine):
        """Test that risk categories are valid labels."""
        segments = analytics_engine.segment_customers_by_risk()
        valid_categories = ['Low', 'Medium', 'High']
        assert segments['risk_category'].isin(valid_categories).all()


class TestChurnAnalyticsBreakdowns:
    """Tests for various breakdown analyses."""
    
    def test_churn_rate_by_gender(self, analytics_engine):
        """Test churn rate breakdown by gender."""
        churn_by_gender = analytics_engine.get_churn_rate_by_gender()
        assert isinstance(churn_by_gender, pd.Series)
        assert len(churn_by_gender) > 0
    
    def test_average_spend_by_subscription(self, analytics_engine):
        """Test average spend by subscription type."""
        spend_by_sub = analytics_engine.get_average_spend_by_subscription()
        assert isinstance(spend_by_sub, pd.Series)
        assert (spend_by_sub >= 0).all()
    
    def test_spend_distribution_by_contract(self, analytics_engine):
        """Test total spend distribution by contract length."""
        spend_by_contract = analytics_engine.get_spend_distribution_by_contract()
        assert isinstance(spend_by_contract, pd.Series)
        assert (spend_by_contract >= 0).all()


class TestChurnAnalyticsSummary:
    """Tests for dataframe summary functions."""
    
    def test_get_dataframe_summary(self, analytics_engine):
        """Test getting DataFrame summary."""
        summary = analytics_engine.get_dataframe_summary()
        assert isinstance(summary, dict)
        assert 'shape' in summary
        assert 'size' in summary
        assert 'statistics' in summary
    
    def test_get_customer_sample(self, analytics_engine, sample_dataframe):
        """Test getting random customer sample."""
        sample = analytics_engine.get_customer_sample(n_rows=3)
        assert isinstance(sample, pd.DataFrame)
        assert len(sample) <= 3
        assert len(sample) <= len(sample_dataframe)
