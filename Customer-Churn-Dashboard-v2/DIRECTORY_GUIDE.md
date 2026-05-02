# Directory Guide - Customer Churn Dashboard v2

## 📍 You Are Here

```
📦 Customer-Churn-Dashboard-v2/
   ├── 👈 YOU ARE HERE
```

## 🚀 Getting Started Files

Read these first, in order:

| File | Time | Purpose |
|------|------|---------|
| `START_HERE.md` | 2-3 min | Quick overview & navigation |
| `SETUP_INSTRUCTIONS.md` | 5 min | Step-by-step installation |
| `GETTING_STARTED.md` | 10 min | Detailed getting started guide |
| `QUICK_REFERENCE.md` | 2 min | Commands & quick tasks |

## 📁 Folder Structure

### `src/` - Core Application Logic (1,140 lines)

The heart of the application. All business logic lives here.

```
src/
├── __init__.py          Package initialization
├── config.py            Configuration, constants, thresholds
├── models.py            Pydantic validation models
├── data_loader.py       CSV loading and preprocessing
├── analytics.py         Calculations and metrics
├── visualizations.py    Chart generation (Matplotlib, Plotly)
└── utils.py             Helper functions, formatting, logging
```

**When to modify:**
- `config.py` - Change column names, thresholds, colors
- `models.py` - Add validation rules
- `analytics.py` - Add new metrics or calculations
- `visualizations.py` - Modify or add charts
- `utils.py` - Add helper functions

### `pages/` - Streamlit UI Pages (505+ lines)

Multi-page Streamlit app. Each file is a separate page/tab.

```
pages/
├── __init__.py          Package initialization
├── dashboard.py         🏠 Main dashboard (metrics, charts)
├── analytics.py         📊 Deep analytics (statistics, projections)
├── settings.py          ⚙️  Data upload and validation
└── predictions.py       🤖 ML predictions (when trained)
```

**Page Flow:**
1. Settings → Upload CSV
2. Dashboard → View metrics
3. Analytics → Explore data
4. Predictions → ML forecasts (after training)

**When to modify:**
- `dashboard.py` - Change dashboard layout/metrics
- `analytics.py` - Add new analytics tabs/features
- `settings.py` - Modify upload/validation flow
- `predictions.py` - Integrate new ML features

### `ml/` - Machine Learning Pipeline (750+ lines)

ML model training, feature engineering, and predictions.

```
ml/
├── __init__.py                Package initialization
├── feature_engineering.py     Feature creation (50+ features)
├── models_pipeline.py         Model training and inference
├── models/                    📂 Trained models storage
│   ├── best_model.pkl
│   ├── feature_importance.pkl
│   └── ...
└── features/                  📂 Feature definitions (reserved)
```

**When to modify:**
- `feature_engineering.py` - Add new features
- `models_pipeline.py` - Change ML algorithms or tuning
- Training output → `ml/models/` (auto-generated)

**Files Generated After Training:**
- `ml/models/best_model.pkl` - Trained model
- `ml/models/feature_importance.pkl` - Feature rankings
- `ml/models/training_report.json` - Performance metrics

### `scripts/` - Standalone Utilities

Independent scripts for one-time or batch tasks.

```
scripts/
└── train_churn_model.py     🎓 ML model training script
```

**Usage:**
```bash
python scripts/train_churn_model.py --data your_data.csv --output ml/models/
```

### `tests/` - Unit Tests (325+ lines)

Automated tests ensuring code quality and reliability.

```
tests/
├── conftest.py          Pytest fixtures and setup
└── test_analytics.py    Tests for analytics module
```

**Run tests:**
```bash
pytest tests/ -v          # All tests
pytest tests/test_analytics.py -v  # Specific test
```

## 📚 Documentation Files

Comprehensive guides for understanding and extending the project.

| File | Size | Purpose |
|------|------|---------|
| `CODE_STRUCTURE.md` | 450+ lines | Architecture & design patterns |
| `ML_IMPROVEMENTS.md` | 600+ lines | ML technical details |
| `STREAMLIT_UI_IMPROVEMENTS.md` | 400+ lines | UI/UX implementation |
| `PROJECT_COMPARISON.md` | 800+ lines | Original vs v2 analysis |
| `IMPROVEMENT_PLAN.md` | 800+ lines | Complete roadmap |
| `DETAILED_CHANGELOG.md` | 600+ lines | Line-by-line changes |
| `MIGRATION_GUIDE.md` | 400+ lines | Upgrade instructions |
| `REFACTORING_SUMMARY.md` | 600+ lines | File-by-file breakdown |

## 🐍 Main Application Files

| File | Purpose | Run? |
|------|---------|------|
| `app_improved.py` | Enhanced main entry point | ✅ **YES** (Recommended) |
| `app.py` | Original entry point | Alternative |
| `requirements.txt` | Python dependencies | `pip install -r` |

## 📄 Reference Files

| File | Purpose |
|------|---------|
| `PROJECT_SUMMARY.txt` | This project at a glance |
| `README.md` | Project overview |
| `COMPLETION_SUMMARY.txt` | Work completed |
| `ML_COMPLETE_SUMMARY.txt` | ML system summary |
| `STREAMLIT_FINAL_SUMMARY.txt` | UI summary |

## 🗺️ How to Navigate

### I want to...

**Run the app**
```bash
cd Customer-Churn-Dashboard-v2
streamlit run app_improved.py
```
→ Files: `app_improved.py`, `pages/`, `src/`

**Upload my data**
→ Use Settings page in the app
→ Files: `pages/settings.py`, `src/data_loader.py`

**View dashboard**
→ Use Dashboard page in the app
→ Files: `pages/dashboard.py`, `src/analytics.py`, `src/visualizations.py`

**Explore data**
→ Use Analytics page in the app
→ Files: `pages/analytics.py`

**Train ML models**
```bash
python scripts/train_churn_model.py --data your_data.csv
```
→ Files: `scripts/train_churn_model.py`, `ml/`

**Make predictions**
→ Use Predictions page (after training models)
→ Files: `pages/predictions.py`, `ml/models_pipeline.py`

**Add new feature**
→ Edit `ml/feature_engineering.py`
→ Test in `scripts/train_churn_model.py`

**Change dashboard colors**
→ Edit `src/config.py` → `DASHBOARD_THEME`
→ Modify `pages/dashboard.py`

**Add new metric**
1. Add calculation in `src/analytics.py`
2. Display in `pages/dashboard.py` or `pages/analytics.py`
3. Add test in `tests/test_analytics.py`

**Fix data validation error**
→ Check `src/models.py` (Pydantic models)
→ Update `src/config.py` (validation rules)
→ Test in `src/data_loader.py`

**Modify chart styling**
→ Edit `src/visualizations.py`
→ Or `src/config.py` for theme colors

## 📊 Development Workflow

### Setup Phase
```
1. Read: START_HERE.md
2. Read: SETUP_INSTRUCTIONS.md
3. Run: pip install -r requirements.txt
4. Run: streamlit run app_improved.py
```

### Data Phase
```
1. Prepare CSV with customer data
2. Go to Settings page
3. Upload CSV
4. Review validation report
```

### Exploration Phase
```
1. View Dashboard page
2. Explore Analytics page
3. Understand the data
```

### ML Phase (Optional)
```
1. Run: python scripts/train_churn_model.py --data your.csv
2. Wait for models to train
3. View Predictions page
```

### Development Phase
```
1. Make code changes in src/, pages/, or ml/
2. Restart Streamlit
3. Test changes
4. Run: pytest tests/ -v (verify)
```

## 🔍 Finding Things

**Find a specific function:**
- Check `src/analytics.py` for metrics
- Check `src/visualizations.py` for charts
- Check `pages/*.py` for UI logic

**Find configuration:**
- Check `src/config.py` for all settings

**Find data loading logic:**
- Check `src/data_loader.py`

**Find validation rules:**
- Check `src/models.py`

**Find ML code:**
- Check `ml/feature_engineering.py`
- Check `ml/models_pipeline.py`

**Find tests:**
- Check `tests/test_analytics.py`

## 📞 Quick Help

**Something not working?**
1. Check `SETUP_INSTRUCTIONS.md` troubleshooting section
2. Check `QUICK_REFERENCE.md` for common issues
3. Read the error message (usually has solution)
4. Check relevant source file comments

**Want to customize something?**
1. Find the relevant file from this guide
2. Read `CODE_STRUCTURE.md` for architecture
3. Make your changes
4. Test with `pytest tests/ -v`

**Need more details?**
1. Read appropriate doc: `ML_IMPROVEMENTS.md`, `STREAMLIT_UI_IMPROVEMENTS.md`, etc.
2. Check docstrings in source code
3. Check inline comments

## 🚀 Ready to Start?

1. **First time?** → Read `START_HERE.md`
2. **Setup?** → Read `SETUP_INSTRUCTIONS.md`
3. **Questions?** → Read `QUICK_REFERENCE.md`
4. **Learning?** → Read `CODE_STRUCTURE.md`

## 📍 File Path Reference

```
Customer-Churn-Dashboard-v2/
├── app_improved.py                    ← Run this
├── requirements.txt                   ← Install first
│
├── src/                               ← Core logic
│   ├── config.py                      ← All configuration
│   ├── models.py                      ← Validation rules
│   ├── data_loader.py                 ← Data loading
│   ├── analytics.py                   ← Calculations
│   ├── visualizations.py              ← Charts
│   └── utils.py                       ← Helpers
│
├── pages/                             ← UI pages
│   ├── dashboard.py                   ← Main page
│   ├── analytics.py                   ← Analytics page
│   ├── settings.py                    ← Settings page
│   └── predictions.py                 ← Predictions page
│
├── ml/                                ← ML pipeline
│   ├── feature_engineering.py         ← Features
│   ├── models_pipeline.py             ← Models
│   └── models/                        ← Saved models
│
├── scripts/
│   └── train_churn_model.py           ← Training script
│
├── tests/                             ← Tests
│   ├── test_analytics.py              ← Tests
│   └── conftest.py                    ← Fixtures
│
└── START_HERE.md                      ← Begin here!
```

---

**Version:** 2.0  
**Last Updated:** May 2, 2026

Happy coding! 🚀
