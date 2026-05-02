# Quick Reference Guide

## Running the App

```bash
# Recommended (enhanced version with professional UI)
streamlit run app_improved.py

# Alternative (original version)
streamlit run app.py
```

## File Navigation

| File | Purpose | When to Use |
|------|---------|-----------|
| `src/config.py` | Settings & constants | Customize column names, thresholds |
| `src/models.py` | Data validation | Understand validation rules |
| `src/data_loader.py` | Data loading | Debug data import issues |
| `src/analytics.py` | Calculations | Find metric formulas |
| `src/visualizations.py` | Charts | Modify visualizations |
| `pages/dashboard.py` | Main view | Customize dashboard layout |
| `pages/analytics.py` | Deep dive | Add new analytics |
| `pages/settings.py` | Upload & validate | Change upload behavior |
| `pages/predictions.py` | ML predictions | Integrate new models |
| `ml/feature_engineering.py` | Feature creation | Add new features |
| `ml/models_pipeline.py` | Model training | Tune ML models |

## Common Tasks

### Change Dashboard Colors
Edit `src/config.py` → `DASHBOARD_THEME` dictionary

### Add New Metric
1. Add calculation in `src/analytics.py`
2. Display in `pages/dashboard.py`
3. Add test in `tests/test_analytics.py`

### Customize Column Names
Edit `src/config.py` → `ColumnMapping` dataclass

### Adjust Risk Thresholds
Edit `src/config.py` → Risk ranges in `ProjectionConfig`

### Train New ML Model
```bash
python scripts/train_churn_model.py --data your_data.csv
```

### Run Tests
```bash
pytest tests/ -v          # All tests
pytest tests/test_analytics.py -v  # Specific test
pytest -k "churn" -v      # Tests matching pattern
```

## Key Metrics Explained

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| Churn Rate | (Churned / Total) × 100 | % of customers who left |
| At-Risk Count | Predicted churn predictions | Customers likely to churn |
| Avg Tenure | Sum(Tenure) / Count | Average customer lifetime |
| Revenue Impact | At-Risk × Avg Charges | Revenue at risk |
| Retention Rate | 100 - Churn Rate | % of customers retained |

## ML Models Available

| Model | Accuracy | Speed | Best For |
|-------|----------|-------|----------|
| Logistic Regression | ~82% | Fast | Baseline, interpretability |
| Random Forest | ~85% | Medium | Robustness, feature importance |
| Gradient Boosting | ~87% | Medium | Best accuracy, production |
| Histogram GB | ~86% | Fast | Large datasets |
| AdaBoost | ~84% | Medium | Ensemble diversity |

## Data Schema

Required columns in CSV:
```
CustomerID, Age, Tenure, MonthlyCharges, TotalCharges, Churn
```

Optional but recommended:
```
Contract, InternetService, OnlineSecurity, TechSupport, StreamingTV
```

## Error Messages & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Column X not found" | CSV missing required column | Check column names in CSV |
| "No data to display" | Empty CSV or all rows invalid | Verify CSV has data rows |
| "Model not found" | ML models not trained | Run `train_churn_model.py` |
| "Validation failed" | Data doesn't match schema | Check data types in CSV |

## Directory Usage

- `src/` → Core business logic (read/modify for customization)
- `pages/` → Streamlit UI pages (modify for layout changes)
- `ml/` → Machine learning (modify for model changes)
- `scripts/` → Standalone utilities (run for training)
- `tests/` → Unit tests (run to verify changes)
- `ml/models/` → Trained model storage (auto-generated)

## Useful Imports

```python
# For adding features
from src.analytics import ChurnAnalytics

# For validation
from src.models import CustomerRecord, DataValidationResult

# For loading data
from src.data_loader import DataLoader

# For ML
from ml.feature_engineering import FeatureEngineer
from ml.models_pipeline import ChurnModelsPipeline
```

## Configuration Options

Edit `src/config.py`:

```python
# Column mapping
COLUMN_MAPPING = ColumnMapping(
    customer_id="CustomerID",
    age="Age",
    tenure="Tenure",
    monthly_charges="MonthlyCharges",
    total_charges="TotalCharges",
    churn="Churn"
)

# Risk thresholds
RISK_THRESHOLDS = {
    "high": 0.7,      # > 70% churn probability
    "medium": 0.4,    # 40-70% churn probability
    "low": 0.0        # < 40% churn probability
}

# UI Theme
DASHBOARD_THEME = {
    "primary_color": "#1f77b4",
    "secondary_color": "#ff7f0e"
}
```

## Performance Tips

1. **Data Size:** App handles 100k+ rows efficiently
2. **Upload Speed:** Depends on file size and internet
3. **Predictions:** First prediction trains model (~30s), subsequent are instant
4. **Caching:** Streamlit caches data and models automatically

## Next Steps

1. Review `GETTING_STARTED.md` for full setup
2. Check `Documentation/` for detailed guides
3. Upload sample data and explore
4. Train ML models on your data
5. Customize to your needs

---

**Version:** 2.0  
**Last Updated:** May 2, 2026
