"""
Complete ML Pipeline Training Script

End-to-end training workflow:
1. Load and validate data
2. Engineer features (domain, transformed, interactions)
3. Train multiple models
4. Compare performance
5. Tune best model
6. Save results
7. Generate report

Usage:
    python scripts/train_churn_model.py <path_to_csv>

Example:
    python scripts/train_churn_model.py "churn_data.csv"
"""

import pandas as pd
import numpy as np
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import DataLoader, DataLoadError
from src.config import get_column_mapping
from ml.feature_engineering import FeatureEngineer
from ml.models_pipeline import ChurnModelPipeline


def load_and_prepare_data(csv_path: str) -> tuple[pd.DataFrame, pd.Series]:
    """
    Load CSV and prepare data for modeling.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        Tuple of (features_df, target_series)
    """
    print("📂 Loading data...")
    
    # Load CSV
    df = pd.read_csv(csv_path)
    cols = get_column_mapping()
    
    print(f"   ✓ Loaded {len(df):,} records with {len(df.columns)} columns")
    
    # Validate data
    required_cols = cols.get_all_columns()
    missing = [c for c in required_cols if c not in df.columns]
    
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Extract target and features
    y = df[cols.churn].astype(int)
    X = df.drop(columns=[cols.churn, cols.customer_id])
    
    # Check class distribution
    class_dist = y.value_counts()
    print(f"   Class distribution:")
    print(f"     - Retained: {class_dist[0]:,} ({class_dist[0]/len(y)*100:.1f}%)")
    print(f"     - Churned: {class_dist[1]:,} ({class_dist[1]/len(y)*100:.1f}%)")
    
    return X, y


def engineer_features(X: pd.DataFrame) -> pd.DataFrame:
    """
    Apply feature engineering.
    
    Args:
        X: Features DataFrame
        
    Returns:
        DataFrame with engineered features
    """
    print("\n⚙️ Engineering features...")
    
    fe = FeatureEngineer()
    
    # Create all types of features
    X_engineered = fe.engineer_all_features(
        X,
        include_domain=True,
        include_transformed=True,
        include_interactions=True,
        include_binned=False  # Can enable for more features
    )
    
    # Handle any NaN values created
    X_engineered = X_engineered.fillna(X_engineered.median(numeric_only=True))
    
    print(f"   ✓ Created {len(X_engineered.columns)} features")
    print(f"     Original: {len(X.columns)} features")
    print(f"     New: {len(X_engineered.columns) - len(X.columns)} features")
    
    return X_engineered


def train_models(X: pd.DataFrame, y: pd.Series) -> dict:
    """
    Train all models and return performances.
    
    Args:
        X: Features DataFrame
        y: Target Series
        
    Returns:
        Dictionary of ModelPerformance objects
    """
    print("\n🤖 Training models...")
    
    pipeline = ChurnModelPipeline()
    performances = pipeline.train_all_models(X, y)
    
    return pipeline, performances


def compare_models(performances: dict) -> str:
    """
    Compare model performances and return ranking.
    
    Args:
        performances: Dictionary of ModelPerformance objects
        
    Returns:
        Formatted comparison string
    """
    print("\n📊 Model Comparison")
    print("─" * 80)
    
    # Sort by AUC-ROC
    sorted_models = sorted(
        performances.items(),
        key=lambda x: x[1].auc_roc,
        reverse=True
    )
    
    comparison = "Rank | Model                          | AUC-ROC | F1    | Precision | Recall\n"
    comparison += "─" * 80 + "\n"
    
    for rank, (model_name, perf) in enumerate(sorted_models, 1):
        comparison += (
            f"{rank:4d} | {model_name:30s} | "
            f"{perf.auc_roc:.4f}  | {perf.f1:.4f} | "
            f"{perf.precision:.4f}    | {perf.recall:.4f}\n"
        )
    
    print(comparison)
    return comparison


def tune_best_model(pipeline: ChurnModelPipeline, 
                    X: pd.DataFrame, 
                    y: pd.Series) -> dict:
    """
    Tune hyperparameters of best model.
    
    Args:
        pipeline: ChurnModelPipeline instance
        X: Features
        y: Target
        
    Returns:
        Dictionary of best parameters
    """
    print("\n🔧 Hyperparameter Tuning")
    
    best_params = pipeline.tune_best_model(X, y)
    
    return best_params


def save_results(pipeline: ChurnModelPipeline,
                X: pd.DataFrame,
                performances: dict,
                output_dir: str = "output/ml/models") -> dict:
    """
    Save trained model and results.
    
    Args:
        pipeline: ChurnModelPipeline instance
        X: Features DataFrame
        performances: Model performances
        output_dir: Output directory
        
    Returns:
        Dictionary with file paths
    """
    print(f"\n💾 Saving results to {output_dir}...")
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Save model
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f"{output_dir}/churn_model_{timestamp}.pkl"
    pipeline.save_model(model_path)
    
    # Save feature importance
    fi_path = f"{output_dir}/feature_importance_{timestamp}.csv"
    feature_importance = pipeline.get_feature_importance(top_n=50)
    feature_importance.to_csv(fi_path, index=False)
    
    # Save report
    report_path = f"{output_dir}/model_report_{timestamp}.txt"
    with open(report_path, 'w') as f:
        f.write(pipeline.get_model_report())
    
    # Save comparison
    comparison_path = f"{output_dir}/model_comparison_{timestamp}.json"
    comparison_data = {
        name: {
            'auc_roc': perf.auc_roc,
            'f1': perf.f1,
            'precision': perf.precision,
            'recall': perf.recall,
            'threshold': perf.threshold,
            'training_time': perf.training_time
        }
        for name, perf in performances.items()
    }
    with open(comparison_path, 'w') as f:
        json.dump(comparison_data, f, indent=2)
    
    print(f"   ✓ Model: {model_path}")
    print(f"   ✓ Feature Importance: {fi_path}")
    print(f"   ✓ Report: {report_path}")
    print(f"   ✓ Comparison: {comparison_path}")
    
    return {
        'model_path': model_path,
        'feature_importance_path': fi_path,
        'report_path': report_path,
        'comparison_path': comparison_path
    }


def generate_summary(pipeline: ChurnModelPipeline,
                    X_engineered: pd.DataFrame,
                    performances: dict) -> str:
    """
    Generate training summary.
    
    Args:
        pipeline: ChurnModelPipeline instance
        X_engineered: Engineered features
        performances: Model performances
        
    Returns:
        Summary string
    """
    best_perf = performances[pipeline.best_model_name]
    
    summary = f"""
╔════════════════════════════════════════════════════════════════╗
║        CHURN PREDICTION MODEL TRAINING - SUMMARY              ║
╚════════════════════════════════════════════════════════════════╝

🎯 BEST MODEL: {pipeline.best_model_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Performance Metrics:
  • AUC-ROC Score:  {best_perf.auc_roc:.4f}
  • F1 Score:       {best_perf.f1:.4f}
  • Precision:      {best_perf.precision:.4f}
  • Recall:         {best_perf.recall:.4f}
  • Optimal Threshold: {best_perf.threshold:.4f}

Model Information:
  • Training Time:  {best_perf.training_time:.2f} seconds
  • Features Used:  {best_perf.feature_count}
  • Cross Validation: 5-Fold Stratified

📊 DATASET STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Features:
  • Total Features: {X_engineered.shape[1]}
  • Numeric Features: {X_engineered.select_dtypes(include=[np.number]).shape[1]}
  • Categorical Features: {X_engineered.select_dtypes(exclude=[np.number]).shape[1]}

📈 FEATURE ENGINEERING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Features Engineered:
  ✓ Domain-specific (business logic)
  ✓ Statistical transformations (log, sqrt, polynomial)
  ✓ Interaction features (feature synergies)
  ✓ Binned features (segmentation)

🔍 TOP 10 MOST IMPORTANT FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{pipeline.get_feature_importance(top_n=10).to_string()}

✅ Model is ready for deployment!
   Save location: output/ml/models/
    """
    
    return summary


def main(csv_path: str):
    """
    Main training pipeline.
    
    Args:
        csv_path: Path to CSV file
    """
    print("\n" + "="*80)
    print("  CHURN PREDICTION MODEL TRAINING PIPELINE")
    print("="*80)
    
    try:
        # Step 1: Load data
        X, y = load_and_prepare_data(csv_path)
        
        # Step 2: Engineer features
        X_engineered = engineer_features(X)
        
        # Step 3: Train models
        pipeline, performances = train_models(X_engineered, y)
        
        # Step 4: Compare models
        comparison = compare_models(performances)
        
        # Step 5: Tune best model (optional, can be slow)
        # Uncomment to enable tuning
        # best_params = tune_best_model(pipeline, X_engineered, y)
        
        # Step 6: Save results
        save_results(pipeline, X_engineered, performances)
        
        # Step 7: Generate summary
        summary = generate_summary(pipeline, X_engineered, performances)
        print(summary)
        
        print("\n✅ Training completed successfully!\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python train_churn_model.py <path_to_csv>")
        print("\nExample:")
        print("  python scripts/train_churn_model.py churn_data.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    if not Path(csv_path).exists():
        print(f"Error: File not found: {csv_path}")
        sys.exit(1)
    
    main(csv_path)
