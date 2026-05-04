# Setup Instructions - Customer Churn Dashboard v2

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A CSV file with customer data

## Step 1: Install Python Dependencies

Open terminal/command prompt and navigate to project directory:

```bash
cd "Customer-Churn-Dashboard-v2"
```

Install all required packages:

```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed streamlit pandas numpy scikit-learn matplotlib plotly ...
```

**Troubleshooting:**
- If pip is not found, try `python -m pip install -r requirements.txt`
- On Mac/Linux, you might need `pip3` instead of `pip`

## Step 2: Verify Installation

Test that Streamlit is installed:

```bash
streamlit --version
```

Should show version 1.28 or higher.

## Step 3: Prepare Your Data

The application requires a CSV file with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| CustomerID | String | Unique customer ID |
| Age | Integer | Customer age (18-80) |
| Tenure | Integer | Months as customer (0-80) |
| MonthlyCharges | Float | Monthly billing ($0-150) |
| TotalCharges | Float | Lifetime billing ($0-10000) |
| Churn | String | "Yes" or "No" |

**Optional columns** (recommended for better predictions):
- Contract, InternetService, OnlineSecurity, TechSupport, StreamingTV

**Example CSV format:**
```
CustomerID,Age,Tenure,MonthlyCharges,TotalCharges,Churn
C001,32,12,65.50,786.00,No
C002,45,8,95.25,762.00,Yes
C003,28,24,45.00,1080.00,No
```

## Step 4: Run the Application

### Option A: Recommended (Enhanced UI)

```bash
streamlit run app_improved.py
```

### Option B: Original Version

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Step 5: Upload Data

1. Click on **Settings** in the sidebar
2. Click **Upload CSV File**
3. Select your prepared CSV file
4. Wait for validation to complete
5. Review data quality report

## Step 6: Explore Dashboard

Navigate through the pages:
- **Dashboard** - Overview of key metrics
- **Analytics** - Detailed statistics and exploration
- **Settings** - Upload data and validation
- **Predictions** - ML-powered churn predictions

## Step 7 (Optional): Train ML Models

For ML predictions, train models on your data:

```bash
python scripts/train_churn_model.py --data your_data.csv --output ml/models/
```

This will:
- Engineer advanced features
- Train 5 different models
- Compare performance
- Save the best model
- Generate training report

**Parameters:**
- `--data` (required): Path to CSV file
- `--output` (optional): Where to save models (default: `ml/models/`)
- `--verbose` (optional): Show detailed output

**Example:**
```bash
python scripts/train_churn_model.py --data customer_data.csv --output ml/models/ --verbose
```

## Step 8: Customize Configuration (Optional)

Edit `src/config.py` to customize:

```python
# Change column names if different in your CSV
COLUMN_MAPPING = ColumnMapping(
    customer_id="YourIDColumn",
    age="YourAgeColumn",
    # ... other columns
)

# Adjust risk thresholds
RISK_THRESHOLDS = {
    "high": 0.7,
    "medium": 0.4,
    "low": 0.0
}
```

## Running Tests

To verify everything is working correctly:

```bash
pytest tests/ -v
```

Should show all tests passing.

## Common Issues & Solutions

### Issue: "Module not found" error

**Solution:** Ensure you're in the correct directory:
```bash
cd "Customer-Churn-Dashboard-v2"
```

### Issue: Streamlit not found

**Solution:** Reinstall dependencies:
```bash
pip install streamlit --upgrade
```

### Issue: CSV upload fails with "Column X not found"

**Solution:** Check that your CSV has exactly these columns:
- CustomerID
- Age
- Tenure
- MonthlyCharges
- TotalCharges
- Churn

If your columns have different names, edit `src/config.py` and update `COLUMN_MAPPING`.

### Issue: App runs but shows no data

**Solution:** 
1. Go to Settings page
2. Upload a CSV file
3. Wait for validation to complete
4. Return to Dashboard

### Issue: Predictions page shows "No model found"

**Solution:** Train the ML model first:
```bash
python scripts/train_churn_model.py --data your_data.csv
```

## Project Structure

```
Customer-Churn-Dashboard-v2/
├── app_improved.py           ← Run this (recommended)
├── src/                       ← Core logic
├── pages/                     ← Streamlit pages
├── ml/                        ← Machine learning
├── scripts/                   ← Training scripts
├── tests/                     ← Unit tests
├── requirements.txt           ← Dependencies
├── GETTING_STARTED.md        ← Quick start guide
├── QUICK_REFERENCE.md        ← Command reference
└── Documentation/            ← Detailed guides
```

## Data Flow

```
1. Upload CSV via Settings
   ↓
2. Validation & Preprocessing (src/data_loader.py)
   ↓
3. Analysis & Metrics (src/analytics.py)
   ↓
4. Display in Dashboard (pages/dashboard.py)
   ↓
5. Optional: Train ML Model (scripts/train_churn_model.py)
   ↓
6. Make Predictions (pages/predictions.py)
```

## Next Steps

1. ✅ Install dependencies (`pip install -r requirements.txt`)
2. ✅ Prepare CSV data
3. ✅ Run app (`streamlit run app_improved.py`)
4. ✅ Upload data via Settings page
5. ✅ Explore Dashboard and Analytics
6. ✅ (Optional) Train ML models
7. ✅ (Optional) Make predictions

## Documentation

For more details, see:
- `GETTING_STARTED.md` - Complete getting started guide
- `QUICK_REFERENCE.md` - Quick command reference
- `CODE_STRUCTURE.md` - Architecture and design
- `ML_IMPROVEMENTS.md` - ML technical details
- `PROJECT_COMPARISON.md` - Original vs v2 comparison

## Support

If you encounter issues:
1. Check error messages in app (usually have solutions)
2. Review Streamlit console output for logs
3. See troubleshooting section above
4. Check documentation in `Documentation/` folder

## Performance Tips

- **First run:** May take a few seconds to load
- **Data size:** Handles 100k+ rows smoothly
- **ML training:** ~30-60 seconds depending on data size
- **Predictions:** Instant after model is trained

## Stopping the App

Press `Ctrl+C` in terminal to stop Streamlit server

---

**Version:** 2.0 (Production-Grade)  
**Created:** May 2, 2026  
**Last Updated:** May 2, 2026
