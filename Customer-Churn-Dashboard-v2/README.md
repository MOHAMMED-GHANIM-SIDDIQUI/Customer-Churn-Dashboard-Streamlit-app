# Customer Churn Dashboard - Refactored v2.0

A production-ready Streamlit application for analyzing customer churn data, identifying at-risk customers, and providing actionable business insights.

## What's New in v2.0

✨ **Code Structure Improvements**
- Modular architecture with separation of concerns
- Pure analytics functions (fully testable)
- Comprehensive error handling and validation
- Pydantic models for data validation

✨ **Better User Experience**
- Multi-page navigation (Home, Dashboard, Analytics, Settings)
- Interactive data explorer
- Detailed data quality reports
- CSV export functionality

✨ **Enhanced Validation**
- Automatic schema validation
- Data quality reporting
- Clear error messages
- Missing value detection

## Project Structure

```
customer-churn-dashboard/
├── src/
│   ├── __init__.py           # Package exports
│   ├── config.py             # Configuration & constants
│   ├── models.py             # Pydantic validation models
│   ├── data_loader.py        # CSV loading & preprocessing
│   ├── analytics.py          # Core analytics computations
│   ├── visualizations.py     # Chart generation
│   └── utils.py              # Helper functions & logging
├── pages/
│   ├── __init__.py
│   ├── dashboard.py          # Dashboard visualizations
│   ├── analytics.py          # Statistics & projections
│   └── settings.py           # Data upload & management
├── tests/
│   ├── conftest.py           # Pytest configuration
│   └── test_analytics.py     # Analytics unit tests
├── app.py                    # Main Streamlit app entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd customer-churn-dashboard
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your default browser.

## Usage

### 1. Upload Data
- Go to **Settings** page
- Upload your CSV file with customer data
- Review the data quality report

### 2. Explore Dashboard
- View customer demographics
- Analyze spending patterns
- Understand churn distribution
- Assess customer risk levels

### 3. Analyze Statistics
- View detailed customer metrics
- See 12-month projections
- Explore data segments
- Review dataset information

### 4. Export Results
- Download processed data as CSV
- Share customer risk assessments
- Archive analysis results

## Required CSV Columns

Your CSV file must contain these columns:

| Column | Type | Description |
|--------|------|-------------|
| Age | Integer | Customer age (0-150 years) |
| Gender | String | Male, Female, or Other |
| Tenure | Integer | Months as customer |
| Support Calls | Integer | Number of support contacts |
| Payment Delay | Integer | Days of payment delay |
| Subscription Type | String | Basic, Standard, or Premium |
| Contract Length | String | Month-to-Month, 1 Year, 2 Years, or 3 Years |
| Total Spend | Float | Total customer spending ($) |
| Churn | Integer | 0 (retained) or 1 (churned) |

## Configuration

Edit `src/config.py` to adjust:

```python
# Business logic for projections
ProjectionConfig:
  - monthly_growth_rate: Expected revenue growth
  - support_call_increase_multiplier: Support volume growth
  - subscription_upgrade_rate: Customers expected to upgrade
  
# Expected column names
ColumnMapping:
  - Adjust if your CSV uses different column names
```

## Testing

Run unit tests:
```bash
pytest tests/ -v
```

Run specific test:
```bash
pytest tests/test_analytics.py::TestChurnAnalyticsBasicStatistics -v
```

Coverage report:
```bash
pytest tests/ --cov=src
```

## Key Features

### 📊 Dashboard
- Age distribution histogram
- Spending by subscription type
- Gender demographic breakdown
- Contract length spend analysis
- Churn rate by gender
- Risk assessment visualization

### 📈 Analytics
- **Customer Statistics**: Age, tenure, spend, churn rate
- **12-Month Projections**: Revenue, churn count, support volume
- **Data Explorer**: Sample records, risk segments
- **Dataset Info**: Schema, statistics, data types

### ⚙️ Settings
- CSV file upload with validation
- Data quality reporting
- Missing value detection
- Duplicate removal
- Column information display

### 🔒 Data Validation
- Pydantic schema validation
- Age range checks (0-150)
- Type validation for all fields
- Missing value reporting
- Duplicate row detection

## Code Quality

### Naming Conventions
- `snake_case` for variables and functions
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Descriptive names: `calculate_basic_statistics()` not `calc_stats()`

### Documentation
- Module docstrings
- Function docstrings with Args/Returns
- Inline comments for complex logic
- Type hints on all functions

### Error Handling
- Custom exceptions (`DataLoadError`)
- User-friendly error messages
- Validation at data entry points
- Comprehensive logging

## Performance Optimization

Current version uses:
- Pandas for data manipulation
- Matplotlib for static charts
- Streamlit caching for expensive operations
- Session state for data persistence

Future improvements:
- Polars for 10x faster I/O
- Plotly for interactive visualizations
- Database layer for persistence
- ML models for churn prediction

## Common Issues

### "Missing required columns" error
- Verify your CSV has all required columns
- Check column names match exactly (case-sensitive)
- See Required CSV Columns section above

### "No data loaded" warning
- Upload a CSV in the Settings page first
- Check data quality report for issues
- Ensure CSV is valid and not corrupted

### Slow performance with large files
- Consider splitting large datasets
- Current version optimized for <100K rows
- Future versions will support larger datasets

## Contributing

1. Create a feature branch: `git checkout -b feature/new-feature`
2. Make your changes and test them
3. Commit with clear message: `git commit -m "Add new feature"`
4. Push and create a Pull Request

## License

This project is provided as-is for educational and business purposes.

## Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Review the documentation
3. Create a new issue with detailed description

---

**Version**: 2.0.0  
**Last Updated**: 2026-05-02  
**Status**: Production Ready ✅
