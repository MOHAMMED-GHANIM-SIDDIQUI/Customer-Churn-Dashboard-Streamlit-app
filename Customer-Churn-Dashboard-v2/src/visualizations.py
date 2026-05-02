"""
Visualization module using Matplotlib and Plotly.

Creates charts for customer analysis with consistent styling.
"""

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Tuple

from src.config import ColumnMapping, get_column_mapping


class ChartGenerator:
    """
    Generates various charts for customer analysis.
    
    Provides both matplotlib (simpler) and plotly (interactive) options.
    """

    def __init__(self, column_mapping: ColumnMapping = None):
        """
        Initialize chart generator.
        
        Args:
            column_mapping: Column name mappings (uses default if None)
        """
        self.cols = column_mapping or get_column_mapping()
        self.color_palette = {
            'primary': '#1f77b4',
            'success': '#2ca02c',
            'warning': '#ff7f0e',
            'danger': '#d62728',
            'info': '#17becf',
        }

    def create_age_distribution(self, df: pd.DataFrame, use_plotly: bool = False):
        """
        Create age distribution histogram.
        
        Args:
            df: Customer DataFrame
            use_plotly: If True, returns Plotly figure; else matplotlib
            
        Returns:
            Chart object (matplotlib Figure or Plotly Figure)
        """
        if use_plotly:
            return px.histogram(
                df,
                x=self.cols.age,
                nbins=20,
                title='Distribution of Customer Age',
                labels={self.cols.age: 'Age'},
                color_discrete_sequence=[self.color_palette['primary']]
            )
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            df[self.cols.age].plot(
                kind='hist',
                bins=20,
                color=self.color_palette['primary'],
                edgecolor='black',
                ax=ax
            )
            ax.set_title('Distribution of Customer Age', fontsize=14, fontweight='bold')
            ax.set_xlabel('Age')
            ax.set_ylabel('Frequency')
            ax.grid(axis='y', alpha=0.3)
            return fig

    def create_spend_by_subscription(self, df: pd.DataFrame, use_plotly: bool = False):
        """
        Create average spend by subscription type bar chart.
        
        Args:
            df: Customer DataFrame
            use_plotly: If True, returns Plotly figure; else matplotlib
            
        Returns:
            Chart object
        """
        spend_by_sub = df.groupby(self.cols.subscription_type)[self.cols.total_spend].mean()

        if use_plotly:
            return px.bar(
                spend_by_sub.reset_index(),
                x=self.cols.subscription_type,
                y=self.cols.total_spend,
                title='Average Total Spend by Subscription Type',
                labels={
                    self.cols.subscription_type: 'Subscription Type',
                    self.cols.total_spend: 'Average Spend ($)'
                },
                color_discrete_sequence=[self.color_palette['success']]
            )
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            spend_by_sub.plot(
                kind='bar',
                color=self.color_palette['success'],
                ax=ax,
                edgecolor='black'
            )
            ax.set_title('Average Total Spend by Subscription Type', 
                         fontsize=14, fontweight='bold')
            ax.set_xlabel('Subscription Type')
            ax.set_ylabel('Average Spend ($)')
            ax.grid(axis='y', alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            return fig

    def create_gender_distribution(self, df: pd.DataFrame, use_plotly: bool = False):
        """
        Create gender distribution pie chart.
        
        Args:
            df: Customer DataFrame
            use_plotly: If True, returns Plotly figure; else matplotlib
            
        Returns:
            Chart object
        """
        gender_counts = df[self.cols.gender].value_counts()

        if use_plotly:
            return px.pie(
                names=gender_counts.index,
                values=gender_counts.values,
                title='Gender Distribution',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
        else:
            fig, ax = plt.subplots(figsize=(8, 8))
            gender_counts.plot(
                kind='pie',
                autopct='%1.1f%%',
                ax=ax,
                colors=[self.color_palette['info'], self.color_palette['warning']]
            )
            ax.set_title('Gender Distribution', fontsize=14, fontweight='bold')
            ax.set_ylabel('')
            return fig

    def create_spend_by_contract_length(self, df: pd.DataFrame, use_plotly: bool = False):
        """
        Create spend distribution by contract length pie chart.
        
        Args:
            df: Customer DataFrame
            use_plotly: If True, returns Plotly figure; else matplotlib
            
        Returns:
            Chart object
        """
        spend_by_contract = df.groupby(self.cols.contract_length)[self.cols.total_spend].sum()

        if use_plotly:
            return px.pie(
                names=spend_by_contract.index,
                values=spend_by_contract.values,
                title='Total Spend Distribution by Contract Length',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
        else:
            fig, ax = plt.subplots(figsize=(10, 8))
            colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
            spend_by_contract.plot(
                kind='pie',
                autopct='%1.1f%%',
                colors=colors[:len(spend_by_contract)],
                ax=ax
            )
            ax.set_title('Total Spend Distribution by Contract Length',
                         fontsize=14, fontweight='bold')
            ax.set_ylabel('')
            return fig

    def create_churn_rate_by_gender(self, df: pd.DataFrame, use_plotly: bool = False):
        """
        Create churn rate comparison by gender bar chart.
        
        Args:
            df: Customer DataFrame
            use_plotly: If True, returns Plotly figure; else matplotlib
            
        Returns:
            Chart object
        """
        churn_by_gender = (df.groupby(self.cols.gender)[self.cols.churn].mean() * 100)

        if use_plotly:
            return px.bar(
                churn_by_gender.reset_index(),
                x=self.cols.gender,
                y=self.cols.churn,
                title='Churn Rate by Gender',
                labels={
                    self.cols.gender: 'Gender',
                    self.cols.churn: 'Churn Rate (%)'
                },
                color_discrete_sequence=[self.color_palette['danger']]
            )
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            churn_by_gender.plot(
                kind='bar',
                color=self.color_palette['danger'],
                ax=ax,
                edgecolor='black'
            )
            ax.set_title('Churn Rate by Gender', fontsize=14, fontweight='bold')
            ax.set_xlabel('Gender')
            ax.set_ylabel('Churn Rate (%)')
            ax.grid(axis='y', alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            return fig

    def create_age_distribution_by_gender(self, df: pd.DataFrame, 
                                          use_plotly: bool = False):
        """
        Create overlaid age distribution histograms by gender.
        
        Args:
            df: Customer DataFrame
            use_plotly: If True, returns Plotly figure; else matplotlib
            
        Returns:
            Chart object
        """
        if use_plotly:
            return px.histogram(
                df,
                x=self.cols.age,
                color=self.cols.gender,
                nbins=20,
                title='Age Distribution by Gender',
                labels={self.cols.age: 'Age'},
                barmode='overlay',
                opacity=0.7
            )
        else:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            male_data = df[df[self.cols.gender] == 'Male'][self.cols.age]
            female_data = df[df[self.cols.gender] == 'Female'][self.cols.age]
            
            ax.hist(male_data, bins=20, alpha=0.5, 
                   color=self.color_palette['primary'], label='Male', edgecolor='black')
            ax.hist(female_data, bins=20, alpha=0.5, 
                   color=self.color_palette['warning'], label='Female', edgecolor='black')
            
            ax.set_title('Age Distribution by Gender', fontsize=14, fontweight='bold')
            ax.set_xlabel('Age')
            ax.set_ylabel('Frequency')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            return fig

    def create_risk_distribution(self, risk_df: pd.DataFrame, use_plotly: bool = False):
        """
        Create pie chart showing customer risk distribution.
        
        Args:
            risk_df: DataFrame with 'risk_category' column (from segment_customers_by_risk)
            use_plotly: If True, returns Plotly figure; else matplotlib
            
        Returns:
            Chart object
        """
        risk_counts = risk_df['risk_category'].value_counts()

        if use_plotly:
            colors = {
                'Low': self.color_palette['success'],
                'Medium': self.color_palette['warning'],
                'High': self.color_palette['danger'],
            }
            return px.pie(
                names=risk_counts.index,
                values=risk_counts.values,
                title='Customer Risk Distribution',
                color_discrete_map=colors
            )
        else:
            fig, ax = plt.subplots(figsize=(8, 8))
            colors_list = [self.color_palette['success'], 
                          self.color_palette['warning'], 
                          self.color_palette['danger']]
            risk_counts.plot(
                kind='pie',
                autopct='%1.1f%%',
                colors=colors_list[:len(risk_counts)],
                ax=ax
            )
            ax.set_title('Customer Risk Distribution', fontsize=14, fontweight='bold')
            ax.set_ylabel('')
            return fig
