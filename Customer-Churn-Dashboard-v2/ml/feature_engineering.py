"""
Feature Engineering Module - Advanced Feature Creation and Transformation

Implements modern feature engineering techniques including:
- Polynomial features for non-linear relationships
- Interaction terms for feature synergies
- Log transformations for skewed distributions
- Binning for categorical relationships
- Feature scaling and normalization
- Domain-specific features from business logic
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.preprocessing import StandardScaler, PolynomialFeatures, RobustScaler
from sklearn.decomposition import PCA
from src.config import ColumnMapping, get_column_mapping


class FeatureEngineer:
    """
    Advanced feature engineering for churn prediction.
    
    Modern approach using:
    - Domain knowledge (business-informed features)
    - Statistical transformations (normalization, scaling)
    - Polynomial features (capture non-linearity)
    - Interaction terms (feature synergies)
    - Feature selection (remove noise)
    """

    def __init__(self, column_mapping: Optional[ColumnMapping] = None):
        """
        Initialize feature engineer.
        
        Args:
            column_mapping: Column name mappings
        """
        self.cols = column_mapping or get_column_mapping()
        self.scaler = RobustScaler()  # Better than StandardScaler for outliers
        self.polynomial_features = None
        self.feature_names = []
        self.feature_means = {}
        self.feature_stds = {}

    # =========================================================================
    # DOMAIN-SPECIFIC FEATURES (Business-informed)
    # =========================================================================

    def create_domain_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create features based on business domain knowledge.
        
        These features directly relate to customer behavior patterns
        and churn drivers identified in the business.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with additional domain features
        """
        df_features = df.copy()

        # ---- 1. CUSTOMER LIFECYCLE FEATURES ----
        # Early tenure customers are riskier
        df_features['is_new_customer'] = (df[self.cols.tenure] <= 6).astype(int)
        # Mid-tenure window (typical churn occurs here)
        df_features['is_at_risk_tenure'] = (
            (df[self.cols.tenure] > 6) & (df[self.cols.tenure] <= 24)
        ).astype(int)
        # Established customers (sticky)
        df_features['is_established'] = (df[self.cols.tenure] > 24).astype(int)

        # ---- 2. ENGAGEMENT FEATURES ----
        # Support calls indicate engagement level
        # High support calls = engaged but may indicate frustration
        df_features['support_calls_per_month'] = (
            df[self.cols.support_calls] / (df[self.cols.tenure] + 1)
        )
        # Unusual support pattern (either very high or very low)
        support_mean = df[self.cols.support_calls].mean()
        support_std = df[self.cols.support_calls].std()
        df_features['unusual_support_pattern'] = (
            ((df[self.cols.support_calls] > support_mean + 2*support_std) |
             (df[self.cols.support_calls] < support_mean - 2*support_std))
        ).astype(int)

        # ---- 3. PAYMENT RELIABILITY FEATURES ----
        # Payment delay indicates financial stress or dissatisfaction
        df_features['has_payment_issues'] = (df[self.cols.payment_delay] > 0).astype(int)
        # Severe payment delays (> 15 days)
        df_features['severe_payment_delay'] = (
            df[self.cols.payment_delay] > 15
        ).astype(int)
        # Chronic payment issues
        df_features['chronic_payment_issues'] = (
            df[self.cols.payment_delay] > 10
        ).astype(int)

        # ---- 4. SPENDING FEATURES ----
        # Revenue-based segmentation
        spending_q1 = df[self.cols.total_spend].quantile(0.25)
        spending_q3 = df[self.cols.total_spend].quantile(0.75)
        df_features['low_value_customer'] = (
            df[self.cols.total_spend] < spending_q1
        ).astype(int)
        df_features['high_value_customer'] = (
            df[self.cols.total_spend] > spending_q3
        ).astype(int)

        # Spending per month normalized by tenure
        df_features['spending_velocity'] = (
            df[self.cols.total_spend] / (df[self.cols.tenure] + 1)
        )

        # ---- 5. SUBSCRIPTION FEATURES ----
        # Subscription type encoded as ordinal (business logic)
        subscription_mapping = {'Basic': 1, 'Standard': 2, 'Premium': 3}
        df_features['subscription_level'] = (
            df[self.cols.subscription_type].map(subscription_mapping)
        )
        # Premium customers are stickier
        df_features['is_premium'] = (
            df[self.cols.subscription_type] == 'Premium'
        ).astype(int)

        # ---- 6. CONTRACT FEATURES ----
        # Contract length indicates commitment
        contract_mapping = {
            'Month-to-Month': 1,
            '1 Year': 12,
            '2 Years': 24,
            '3 Years': 36
        }
        df_features['contract_months'] = (
            df[self.cols.contract_length].map(contract_mapping)
        )
        # Long-term commitment reduces churn
        df_features['long_term_contract'] = (
            df[self.cols.contract_length].isin(['2 Years', '3 Years'])
        ).astype(int)

        # ---- 7. DEMOGRAPHIC FEATURES ----
        # Gender encoding
        gender_mapping = {'Male': 0, 'Female': 1, 'Other': 2}
        df_features['gender_encoded'] = (
            df[self.cols.gender].map(gender_mapping)
        )

        # ---- 8. RISK AGGREGATION FEATURES ----
        # Combine multiple risk signals
        df_features['risk_score'] = (
            df_features['is_new_customer'] * 0.15 +
            df_features['has_payment_issues'] * 0.20 +
            df_features['low_value_customer'] * 0.10 +
            df_features['unusual_support_pattern'] * 0.15 +
            (1 - df_features['long_term_contract'] / 1.0) * 0.20 +
            df_features['severe_payment_delay'] * 0.20
        )

        return df_features

    # =========================================================================
    # STATISTICAL TRANSFORMATION FEATURES
    # =========================================================================

    def create_transformed_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create statistically transformed features.
        
        Handles skewed distributions and non-linear relationships
        using log and polynomial transformations.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with transformed features
        """
        df_transformed = df.copy()

        # ---- LOG TRANSFORMATIONS (for right-skewed distributions) ----
        # Total spend often right-skewed
        df_transformed['total_spend_log'] = np.log1p(df[self.cols.total_spend])
        # Payment delay often right-skewed
        df_transformed['payment_delay_log'] = np.log1p(
            df[self.cols.payment_delay] + 1
        )
        # Support calls often right-skewed
        df_transformed['support_calls_log'] = np.log1p(
            df[self.cols.support_calls] + 1
        )
        # Tenure log captures diminishing churn risk
        df_transformed['tenure_log'] = np.log1p(df[self.cols.tenure] + 1)

        # ---- SQUARE ROOT TRANSFORMATIONS (moderate skewness) ----
        df_transformed['total_spend_sqrt'] = np.sqrt(df[self.cols.total_spend])
        df_transformed['tenure_sqrt'] = np.sqrt(df[self.cols.tenure])

        # ---- RECIPROCAL TRANSFORMATION (very skewed) ----
        # For payment delay: lower is better
        df_transformed['payment_delay_inv'] = 1.0 / (
            df[self.cols.payment_delay] + 1
        )

        # ---- POLYNOMIAL FEATURES (capture non-linearity) ----
        # Age^2: Age effects may be non-linear
        df_transformed['age_squared'] = df[self.cols.age] ** 2
        # Tenure^2: Tenure effect levels off
        df_transformed['tenure_squared'] = df[self.cols.tenure] ** 2
        # Age^3 for extreme non-linearity if needed
        df_transformed['age_cubed'] = df[self.cols.age] ** 3

        return df_transformed

    # =========================================================================
    # INTERACTION FEATURES (Feature synergies)
    # =========================================================================

    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create interaction features capturing feature synergies.
        
        Combinations that reveal non-obvious churn drivers.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with interaction features
        """
        df_interactions = df.copy()

        # ---- HIGH-VALUE + LOW TENURE (retention risk) ----
        # Valuable customers who are new = high value loss if churned
        spending_q3 = df[self.cols.total_spend].quantile(0.75)
        df_interactions['high_value_new_customer'] = (
            (df[self.cols.total_spend] > spending_q3) &
            (df[self.cols.tenure] <= 6)
        ).astype(int)

        # ---- HIGH PAYMENT DELAYS + LONG TENURE (problem customers) ----
        # Long-term customers with payment issues may be dissatisfied
        df_interactions['chronic_payment_dissatisfaction'] = (
            (df[self.cols.payment_delay] > 10) &
            (df[self.cols.tenure] > 24)
        ).astype(int)

        # ---- SUPPORT OVERLOAD (frustrated customers) ----
        # High support calls + high payment delays = likely frustrated
        support_mean = df[self.cols.support_calls].mean()
        df_interactions['support_and_payment_stress'] = (
            (df[self.cols.support_calls] > support_mean * 1.5) &
            (df[self.cols.payment_delay] > 10)
        ).astype(int)

        # ---- AGE + SUBSCRIPTION (demographic targeting) ----
        # Younger customers with basic plans = different risk
        df_interactions['young_basic'] = (
            (df[self.cols.age] < 30) &
            (df[self.cols.subscription_type] == 'Basic')
        ).astype(int)
        # Older premium customers = stable segment
        df_interactions['older_premium'] = (
            (df[self.cols.age] > 45) &
            (df[self.cols.subscription_type] == 'Premium')
        ).astype(int)

        # ---- TENURE + CONTRACT (commitment signal) ----
        # Long tenure + month-to-month = risky (no commitment)
        df_interactions['long_tenure_flexible_contract'] = (
            (df[self.cols.tenure] > 24) &
            (df[self.cols.contract_length] == 'Month-to-Month')
        ).astype(int)

        # ---- NUMERIC INTERACTIONS (multiplicative effects) ----
        # Age × Tenure: Older + longer tenure = stronger retention
        df_interactions['age_tenure_interaction'] = (
            df[self.cols.age] * df[self.cols.tenure] / 100
        )

        # Spend × Support calls: Trade-off between engagement and frustration
        df_interactions['spend_support_ratio'] = (
            df[self.cols.total_spend] / (df[self.cols.support_calls] + 1)
        )

        # Age × Payment delay: Age may moderate payment delay impact
        df_interactions['age_payment_interaction'] = (
            (df[self.cols.age] / 10) * (df[self.cols.payment_delay] / 5)
        )

        return df_interactions

    # =========================================================================
    # BINNING / DISCRETIZATION FEATURES
    # =========================================================================

    def create_binned_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create binned/discretized features for categorical relationships.
        
        Useful for capturing non-linear relationships and creating
        natural segments without assuming linearity.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with binned features
        """
        df_binned = df.copy()

        # ---- AGE BINNING ----
        # Age segments: Gen Z, Millennial, Gen X, Boomer
        df_binned['age_group'] = pd.cut(
            df[self.cols.age],
            bins=[0, 25, 40, 55, 100],
            labels=['Young', 'Middle', 'Senior', 'Elderly'],
            include_lowest=True
        )
        # One-hot encode age groups
        age_dummies = pd.get_dummies(
            df_binned['age_group'],
            prefix='age',
            drop_first=True
        )
        df_binned = pd.concat([df_binned, age_dummies], axis=1)

        # ---- TENURE BINNING ----
        # Tenure stages: new, growing, mature, stable
        df_binned['tenure_stage'] = pd.cut(
            df[self.cols.tenure],
            bins=[0, 6, 12, 24, 1000],
            labels=['New', 'Growing', 'Mature', 'Stable'],
            include_lowest=True
        )
        tenure_dummies = pd.get_dummies(
            df_binned['tenure_stage'],
            prefix='tenure',
            drop_first=True
        )
        df_binned = pd.concat([df_binned, tenure_dummies], axis=1)

        # ---- SPENDING BINNING ----
        # Spending segments: low, medium, high, premium
        df_binned['spending_segment'] = pd.qcut(
            df[self.cols.total_spend],
            q=4,
            labels=['Low', 'Medium', 'High', 'Premium'],
            duplicates='drop'
        )
        spending_dummies = pd.get_dummies(
            df_binned['spending_segment'],
            prefix='spend',
            drop_first=True
        )
        df_binned = pd.concat([df_binned, spending_dummies], axis=1)

        return df_binned

    # =========================================================================
    # FEATURE SELECTION
    # =========================================================================

    def get_top_features(self, X: pd.DataFrame, y: pd.Series, 
                        n_features: int = 20,
                        method: str = 'mutual_info') -> List[str]:
        """
        Select top N features using mutual information or other methods.
        
        Modern feature selection using information-theoretic approaches.
        
        Args:
            X: Features DataFrame
            y: Target Series
            n_features: Number of top features to select
            method: Selection method ('mutual_info', 'variance', 'correlation')
            
        Returns:
            List of top feature names
        """
        from sklearn.feature_selection import (
            mutual_info_classif, 
            SelectKBest,
            VarianceThreshold
        )

        if method == 'mutual_info':
            # Mutual information captures non-linear relationships
            # Better than correlation for churn prediction
            selector = SelectKBest(
                score_func=mutual_info_classif,
                k=min(n_features, X.shape[1])
            )
            selector.fit(X, y)
            scores = selector.scores_
        
        elif method == 'variance':
            # Remove low-variance features (noise)
            selector = VarianceThreshold()
            X_selected = selector.fit_transform(X)
            scores = selector.variances_
            
        else:
            raise ValueError(f"Unknown method: {method}")

        # Get top feature indices
        top_indices = np.argsort(scores)[-n_features:][::-1]
        top_features = [X.columns[i] for i in top_indices]

        return top_features

    # =========================================================================
    # COMPLETE FEATURE PIPELINE
    # =========================================================================

    def engineer_all_features(self, df: pd.DataFrame,
                             include_domain: bool = True,
                             include_transformed: bool = True,
                             include_interactions: bool = True,
                             include_binned: bool = False) -> pd.DataFrame:
        """
        Complete feature engineering pipeline.
        
        Applies all feature engineering techniques and returns
        comprehensive feature set.
        
        Args:
            df: Input DataFrame
            include_domain: Include domain-specific features
            include_transformed: Include statistical transformations
            include_interactions: Include interaction features
            include_binned: Include binned features
            
        Returns:
            DataFrame with all engineered features
        """
        df_engineered = df.copy()

        if include_domain:
            domain_features = self.create_domain_features(df)
            # Add only new features
            new_cols = [c for c in domain_features.columns if c not in df_engineered.columns]
            df_engineered = pd.concat([
                df_engineered,
                domain_features[new_cols]
            ], axis=1)

        if include_transformed:
            transformed_features = self.create_transformed_features(df)
            new_cols = [c for c in transformed_features.columns if c not in df_engineered.columns]
            df_engineered = pd.concat([
                df_engineered,
                transformed_features[new_cols]
            ], axis=1)

        if include_interactions:
            interaction_features = self.create_interaction_features(df)
            new_cols = [c for c in interaction_features.columns if c not in df_engineered.columns]
            df_engineered = pd.concat([
                df_engineered,
                interaction_features[new_cols]
            ], axis=1)

        if include_binned:
            binned_features = self.create_binned_features(df)
            new_cols = [c for c in binned_features.columns if c not in df_engineered.columns]
            df_engineered = pd.concat([
                df_engineered,
                binned_features[new_cols]
            ], axis=1)

        return df_engineered

    # =========================================================================
    # SCALING AND NORMALIZATION
    # =========================================================================

    def scale_features(self, X: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        Scale features using RobustScaler (resistant to outliers).
        
        Better than StandardScaler when data has outliers,
        which is common in financial/business data.
        
        Args:
            X: Features to scale
            fit: If True, fit scaler; if False, use existing fit
            
        Returns:
            Scaled features as DataFrame
        """
        if fit:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)

        return pd.DataFrame(X_scaled, columns=X.columns, index=X.index)

    # =========================================================================
    # DIMENSIONALITY REDUCTION
    # =========================================================================

    def reduce_dimensionality(self, X: pd.DataFrame, 
                             n_components: int = 10,
                             method: str = 'pca') -> Tuple[np.ndarray, list]:
        """
        Reduce feature dimensionality while preserving information.
        
        Useful when number of features exceeds samples (curse of dimensionality).
        
        Args:
            X: Features to reduce
            n_components: Number of components to keep
            method: Reduction method ('pca', 'pca_weighted')
            
        Returns:
            Tuple of (reduced_features, component_names)
        """
        if method == 'pca':
            pca = PCA(n_components=min(n_components, X.shape[1]))
            X_reduced = pca.fit_transform(X)
            
            # Variance explained
            variance_explained = pca.explained_variance_ratio_.sum()
            print(f"PCA: {n_components} components explain {variance_explained:.1%} variance")
            
            component_names = [f'PC{i+1}' for i in range(n_components)]
            return X_reduced, component_names
        
        else:
            raise ValueError(f"Unknown method: {method}")
