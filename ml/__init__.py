"""
ML Pipeline Package - Complete Machine Learning Infrastructure

Modules:
- feature_engineering: Advanced feature creation and transformation
- models_pipeline: Multiple model architectures and training
"""

from ml.feature_engineering import FeatureEngineer
from ml.models_pipeline import ChurnModelPipeline, ModelPerformance

__version__ = "1.0.0"
__all__ = [
    "FeatureEngineer",
    "ChurnModelPipeline",
    "ModelPerformance",
]
