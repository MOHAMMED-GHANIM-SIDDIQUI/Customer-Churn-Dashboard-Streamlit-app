# Customer Churn Dashboard v2 - Getting Started

## Overview

This is a production-grade Customer Churn Analytics Dashboard built with Streamlit. It provides:
- Advanced machine learning predictions for customer churn
- Interactive visualizations and analytics
- Comprehensive data validation and error handling
- Professional UI/UX with custom styling

## Project Structure

```
Customer-Churn-Dashboard-v2/
├── src/                          # Core modules
│   ├── config.py                # Configuration & constants
│   ├── models.py                # Pydantic validation models
│   ├── data_loader.py           # CSV loading & preprocessing
│   ├── analytics.py             # Analytics computations
│   ├── visualizations.py        # Chart generation
│   ├── utils.py                 # Helper functions
│   └── __init__.py
│
├── pages/                        # Streamlit multi-page app
│   ├── dashboard.py             # Main dashboard
│   ├── analytics.py             # Statistics & exploration
│   ├── settings.py              # Data upload & validation
│   └── predictions.py           # ML predictions
│
├── ml/                           # Machine learning pipeline
│   ├── feature_engineering.py   # Feature creation
│   ├── models_pipeline.py       # Model training & inference
│   └── models/                  # Trained model storage
│
├── scripts/
│   └── train_churn_model.py     # Model training script
│
├── tests/                        # Unit tests
│   ├── test_analytics.py
│   └── conftest.py
│
├── app_improved.py              # Main entry point (recommended)
├── app.py                        # Original entry point
├── requirements.txt             # Dependencies
└── Documentation/               # Complete guides & references
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Data

Create a CSV file with customer data. Required columns:
- `CustomerID`: Unique customer identifier
- `Age`: Customer age
- `Tenure`: Months as customer
- `MonthlyCharges`: Monthly billing amount
- `TotalCharges`: Total lifetime charges
- `Churn`: Yes/No indicator

### 3. Run the Application

```bash
# Using improved version (recommended)
streamlit run app_improved.py

# Or using original version
streamlit run app.py
```

### 4. Upload Data

1. Go to Settings page
2. Upload your CSV file
3. Review validation report
4. Proceed to Dashboard

## Key Features

### Dashboard Page
- Key metrics (total customers, churn rate, at-risk count)
- Churn distribution visualization
- Risk segment analysis
- Customer overview

### Analytics Page
- Statistical summaries
- Revenue projections
- Data explorer with filtering
- System information

### Settings Page
- CSV upload with validation
- Data quality checks
- Schema validation
- Error reporting

### Predictions Page (ML-Powered)
- Individual customer churn predictions
- Feature importance visualization
- Risk scoring
- Bulk prediction capability

## Data Validation

The application automatically validates:
- Required columns presence
- Data types (numeric, categorical)
- Missing values
- Outliers and anomalies
- Duplicate records

## Model Training

To train ML models on your data:

```bash
python scripts/train_churn_model.py --data your_data.csv --output models/
```

This will:
- Engineer 50+ features
- Train 5 different models
- Compare performance via cross-validation
- Save best model and feature importance
- Generate training report

## Configuration

Edit `src/config.py` to customize:
- Column mappings
- Risk thresholds
- UI styling
- Validation rules
- ML parameters

## Testing

Run tests to verify functionality:

```bash
pytest tests/ -v
```

## Documentation

- **CODE_STRUCTURE.md** - Architecture and design patterns
- **IMPROVEMENT_PLAN.md** - Detailed improvement roadmap
- **ML_IMPROVEMENTS.md** - Machine learning technical details
- **STREAMLIT_UI_IMPROVEMENTS.md** - UI/UX enhancements
- **PROJECT_COMPARISON.md** - Original vs v2 comparison

## Troubleshooting

### CSV Upload Issues
- Ensure CSV has required columns
- Check for encoding issues (use UTF-8)
- Verify no empty rows at end

### Missing Data
- Application handles missing values automatically
- Check "Data Quality" metrics in Settings
- Rows with critical missing values are excluded

### ML Model Not Found
- Train models first: `python scripts/train_churn_model.py --data your_data.csv`
- Check `ml/models/` directory for trained models
- Review training logs for errors

## Next Steps

1. ✅ Install dependencies
2. ✅ Prepare CSV data
3. ✅ Run the app
4. ✅ Upload data via Settings
5. ✅ Train ML models (optional)
6. ✅ Explore dashboards and analytics
7. ✅ Make predictions

## Support

For issues or questions:
- Check documentation in `Documentation/` folder
- Review error messages in app (usually provide recovery steps)
- Check logs in Streamlit console output

## Requirements

- Python 3.8+
- Streamlit 1.28+
- pandas, numpy, scikit-learn
- matplotlib, plotly
- See `requirements.txt` for full list

---

**Version:** 2.0 (Production-Grade)  
**Last Updated:** May 2, 2026
