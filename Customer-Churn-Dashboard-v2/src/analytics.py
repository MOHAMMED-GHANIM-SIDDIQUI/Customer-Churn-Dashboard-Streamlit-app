"""
Analytics and computations module.

Pure functions for customer analysis and projections.
These functions have no side effects and are fully testable.
"""

from typing import Dict, Tuple
import pandas as pd
import io

from src.config import ColumnMapping, ProjectionConfig, get_column_mapping, get_projection_config


class ChurnAnalytics:
    """
    Encapsulates all customer analytics computations.
    
    Uses named columns (not indices) for robustness.
    All methods are pure functions with no side effects.
    """

    def __init__(self, df: pd.DataFrame, 
                 column_mapping: ColumnMapping = None,
                 projection_config: ProjectionConfig = None):
        """
        Initialize analytics engine.
        
        Args:
            df: Customer DataFrame
            column_mapping: Column name mappings (uses default if None)
            projection_config: Business logic config (uses default if None)
        """
        self.df = df
        self.cols = column_mapping or get_column_mapping()
        self.config = projection_config or get_projection_config()

    def calculate_basic_statistics(self) -> Dict[str, float]:
        """
        Calculate fundamental customer metrics.
        
        Returns:
            Dictionary with key statistics
        """
        churn_binary = (self.df[self.cols.churn] == 'Yes').astype(int)

        return {
            'average_age': float(self.df[self.cols.age].mean()),
            'average_tenure': float(self.df[self.cols.tenure].mean()),
            'total_spend': float(self.df[self.cols.total_spend].sum()),
            'average_spend': float(self.df[self.cols.total_spend].mean()),
            'average_support_calls': float(self.df[self.cols.support_calls].mean()),
            'churn_rate_percent': float(churn_binary.mean() * 100),
            'payment_delay_std_dev': float(self.df[self.cols.payment_delay].std()),
        }

    def calculate_projections_next_year(self) -> Dict[str, float]:
        """
        Project key metrics for next 12 months using business config.
        
        These projections use configured growth rates and historical data
        to estimate future performance.
        
        Returns:
            Dictionary with projected metrics
        """
        n_customers = len(self.df)
        average_monthly_spend = self.df[self.cols.total_spend].mean()
        churn_rate = self.df[self.cols.churn].astype(int).mean()
        average_support_calls = self.df[self.cols.support_calls].mean()
        average_payment_delay = self.df[self.cols.payment_delay].mean()

        standard_and_basic = self.df[
            self.df[self.cols.subscription_type].isin(['Standard', 'Basic'])
        ]

        return {
            'projected_total_spend_next_year': (
                average_monthly_spend * 12 * self.config.monthly_growth_rate * n_customers
            ),
            'projected_churn_count_next_year': churn_rate * n_customers,
            'projected_support_calls_increase': (
                average_support_calls * self.config.support_call_increase_multiplier
            ),
            'projected_payment_delay_increase': (
                average_payment_delay * self.config.payment_delay_increase_multiplier
            ),
            'projected_subscription_upgrades': (
                len(standard_and_basic) * self.config.subscription_upgrade_rate
            ),
            'projected_tenure_growth': (
                self.df[self.cols.tenure].mean() * self.config.tenure_growth_multiplier
            ),
        }

    def get_churn_rate_by_gender(self) -> pd.Series:
        """
        Calculate churn rate breakdown by gender.
        
        Returns:
            Series with churn rates indexed by gender
        """
        churn_binary = (self.df[self.cols.churn] == 'Yes').astype(int)
        grouped = self.df.groupby(self.cols.gender, observed=True).size()
        churned = self.df[churn_binary.astype(bool)].groupby(self.cols.gender, observed=True).size()
        return (churned.reindex(grouped.index, fill_value=0) / grouped * 100).fillna(0)

    def get_average_spend_by_subscription(self) -> pd.Series:
        """
        Calculate average spending by subscription type.
        
        Returns:
            Series with average spend indexed by subscription type
        """
        return self.df.groupby(self.cols.subscription_type)[self.cols.total_spend].mean()

    def get_spend_distribution_by_contract(self) -> pd.Series:
        """
        Calculate total spending distribution by contract length.
        
        Returns:
            Series with total spend indexed by contract length
        """
        return self.df.groupby(self.cols.contract_length)[self.cols.total_spend].sum()

    def get_dataframe_summary(self) -> Dict:
        """
        Get comprehensive DataFrame summary for data exploration.
        
        Returns:
            Dictionary with DataFrame info, stats, and quality metrics
        """
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        info_str = buffer.getvalue()

        return {
            'shape': self.df.shape,
            'size': len(self.df),
            'info': info_str,
            'column_types': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'statistics': self.df.describe(include='all').to_dict(),
            'sample_rows': self.df.sample(min(10, len(self.df))).to_dict('records'),
        }

    def segment_customers_by_risk(self) -> pd.DataFrame:
        """
        Segment customers into risk categories based on multiple factors.
        
        Risk scoring considers:
        - Whether customer has churned (50% weight)
        - Low tenure (30% weight)
        - High payment delays (20% weight)
        
        Returns:
            DataFrame with customer IDs, risk scores, and categories
        """
        df_result = self.df[[self.cols.customer_id]].copy()

        tenure_normalized = self.df[self.cols.tenure] / self.df[self.cols.tenure].max()
        payment_delay_normalized = (self.df[self.cols.payment_delay] / 
                                    self.df[self.cols.payment_delay].max())
        churn_binary = (self.df[self.cols.churn] == 'Yes').astype(int)

        df_result['risk_score'] = (
            churn_binary * 0.5 +
            (1 - tenure_normalized) * 0.3 +
            payment_delay_normalized * 0.2
        )

        df_result['risk_category'] = pd.cut(
            df_result['risk_score'],
            bins=[0, 0.3, 0.6, 1.0],
            labels=['Low', 'Medium', 'High'],
            include_lowest=True
        )

        return df_result

    def get_customer_sample(self, n_rows: int = 10) -> pd.DataFrame:
        """
        Get random sample of customers.
        
        Args:
            n_rows: Number of rows to sample
            
        Returns:
            Random sample DataFrame
        """
        return self.df.sample(n=min(n_rows, len(self.df)), random_state=42)
