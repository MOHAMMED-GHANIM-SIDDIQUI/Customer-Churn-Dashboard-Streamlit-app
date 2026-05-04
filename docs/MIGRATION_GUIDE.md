# Migration Guide - From v1.0 to v2.0

This guide explains the changes from the original monolithic dashboard to the refactored v2.0 architecture.

## What Changed

### File Structure

**Before (v1.0)**:
```
customer-churn-dashboard/
├── dashboard.py          (189 lines, monolithic)
├── churn dataset.csv
└── requirements.txt
```

**After (v2.0)**:
```
customer-churn-dashboard/
├── src/
│   ├── config.py
│   ├── models.py
│   ├── data_loader.py
│   ├── analytics.py
│   ├── visualizations.py
│   ├── utils.py
│   └── __init__.py
├── pages/
│   ├── dashboard.py
│   ├── analytics.py
│   ├── settings.py
│   └── __init__.py
├── tests/
│   ├── test_analytics.py
│   └── conftest.py
├── app.py                (Entry point)
├── requirements.txt
├── README.md
└── CODE_STRUCTURE.md
```

## Code Mapping

### Original Functions → New Modules

#### `about_df()` → `DataLoader.load_and_validate()`
```python
# v1.0
def about_df(df):
    df_sample = df.sample(10)
    size = df.shape[0]
    # ... etc
    return df_sample, size, info, columns, missing_values, stats

# v2.0
loader = DataLoader()
df, quality_report = loader.load_and_validate(uploaded_file)
# quality_report contains all metadata
```

**Improvements**:
- Returns structured report (dict), not tuple of 6 values
- Includes duplicate detection
- Validates data types
- Provides warnings

#### `customer_statistics()` → `ChurnAnalytics.calculate_basic_statistics()`
```python
# v1.0
def customer_statistics(df):
    average_age = df.iloc[:, 1].mean()
    # ... uses hardcoded column indices!
    
# v2.0
analytics = ChurnAnalytics(df)
stats = analytics.calculate_basic_statistics()
# Uses named columns from config
```

**Improvements**:
- Uses named columns (not indices)
- Returns dict with all 7 metrics
- No silent failures on wrong column order

#### `future_insights()` → `ChurnAnalytics.calculate_projections_next_year()`
```python
# v1.0
def future_insights(df):
    average_monthly_spend = df.iloc[:, 9].mean()
    # ... magic numbers embedded
    
# v2.0
projections = analytics.calculate_projections_next_year()
# Config magic numbers in ProjectionConfig class
```

**Improvements**:
- Projections stored in ProjectionConfig
- Easier to adjust business logic
- Well-documented parameters

#### Chart Functions → `ChartGenerator` Methods
```python
# v1.0
def age_distribution_graph(df):
    fig, ax = plt.subplots()
    df['Age'].plot(kind='hist', ...)
    return fig

# v2.0
chart_gen = ChartGenerator()
fig = chart_gen.create_age_distribution(df, use_plotly=False)
# OR for interactive charts:
fig = chart_gen.create_age_distribution(df, use_plotly=True)
```

**Improvements**:
- Single ChartGenerator class
- Supports both matplotlib and Plotly
- Consistent color palette
- Better error handling

## Data Flow Changes

### Old (v1.0)
```
CSV Upload
    ↓
pd.read_csv() (no validation)
    ↓
User clicks button → recalculates all stats (no caching)
    ↓
display result
    ↓
If error: crashes with cryptic pandas error
```

### New (v2.0)
```
CSV Upload
    ↓
DataLoader.load_and_validate()
    ├─ Schema validation (columns exist)
    ├─ Type validation (Pydantic models)
    ├─ Data quality checks (missing, duplicates)
    └─ Returns quality report
    ↓
If invalid: User sees clear error message + which rows failed
    ↓
Store cleaned_df in session_state (persistent)
    ↓
User navigates pages (no re-upload needed)
    ↓
@st.cache_data prevents recalculation
    ↓
Results displayed with context
```

## User Experience Changes

### Before (v1.0)
```
Home page with no options
Sidebar with 4 buttons:
  - About Dataset
  - Customer Statistics
  - Future Insights
  - Dashboard
```

**Issues**:
- No clear data upload flow
- Must click each button to see results
- No persistence between views
- No error messages

### After (v2.0)
```
Home page with navigation
Sidebar with 4 pages:
  - Home (landing page)
  - Dashboard (main visualizations)
  - Analytics (statistics & projections)
  - Settings (data upload)
```

**Benefits**:
- Clear "upload data first" in Settings
- Multi-page prevents clicks
- Session state persists data
- Detailed error reporting

## Configuration Changes

### Before (v1.0)
Magic numbers scattered throughout code:
```python
# Hardcoded in 6 different places
df.iloc[:, 1]  # Which column is this?
churn_rate * len(df)  # What does this calculate?
* 1.1  # Why 10% increase?
df.iloc[:, 7] == 'Standard'  # Fragile string check
```

### After (v2.0)
Centralized configuration:
```python
# src/config.py
@dataclass
class ColumnMapping:
    age: str = "Age"  # Clear reference
    subscription_type: str = "Subscription Type"

@dataclass
class ProjectionConfig:
    support_call_increase_multiplier: float = 1.1  # Documented!
```

**Changes**:
- Single source of truth for column names
- Business logic documented and configurable
- Easy for non-developers to adjust

## Validation Changes

### Before (v1.0)
No validation:
```
CSV with wrong columns
    ↓
df.iloc[:, 1].mean() with wrong data
    ↓
Silent error or nonsense result
```

### After (v2.0)
Comprehensive validation:
```
CSV with wrong columns
    ↓
DataLoader.validate_schema()
    ↓
Pydantic validates each record
    ↓
Clear error: "Missing column: 'Age'"
```

**New Validation Checks**:
- Column presence (schema)
- Data type correctness
- Value range constraints (age 0-150)
- Gender values (Male/Female/Other)
- Negative value checks
- Missing value detection
- Duplicate row detection

## Testing Changes

### Before (v1.0)
No tests:
- No way to verify calculations
- Risky to refactor
- Bugs discovered by users only

### After (v2.0)
Comprehensive test suite:
```python
pytest tests/ -v
# test_analytics.py includes:
# - Basic statistics accuracy
# - Projection calculations
# - Risk segmentation logic
# - Value range constraints
# - Data structure validation
```

Run tests:
```bash
pytest tests/ -v              # All tests
pytest tests/test_analytics.py # Single file
pytest --cov=src              # Coverage report
```

## Performance Changes

### Before (v1.0)
- Recalculates all stats on every button click
- No caching
- Slow with medium-sized datasets

### After (v2.0)
- @st.cache_data prevents redundant calculations
- Session state persists data
- Faster navigation between pages
- Cleaner performance profile

**Caching Strategy**:
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def calculate_basic_statistics(df):
    # Called once per hour per input
```

## Error Handling Changes

### Before (v1.0)
```python
# No error handling
df.iloc[:, 1].mean()  # If column missing → IndexError
df.groupby('Gender')['Churn'].mean()  # If column missing → KeyError
# User sees: "KeyError: 'Gender'"  (confusing!)
```

### After (v2.0)
```python
try:
    df, report = loader.load_and_validate(file)
    st.session_state.dataframe = df
except DataLoadError as e:
    st.error(f"❌ Loading Error: {str(e)}")
    # User sees: "❌ Loading Error: Missing required column: 'Age'"
```

## Naming Improvements

### Column References

**Before (v1.0)**:
```python
df.iloc[:, 1]      # Which column is this?
df.iloc[:, 3]      # Still unclear
df['Age']          # Mixed approach - inconsistent!
```

**After (v2.0)**:
```python
df[self.cols.age]           # Clear intent
df[self.cols.tenure]        # Self-documenting
df[self.cols.total_spend]   # No guessing
```

### Function Names

**Before (v1.0)**:
```python
def about_df()           # What does this do?
def customer_statistics  # Singular or plural?
def future_insights      # How far in future?
def age_distribution_graph  # Why just age?
```

**After (v2.0)**:
```python
def load_and_validate()           # Clear action
def calculate_basic_statistics()  # What it calculates
def calculate_projections_next_year()  # When projected
def create_age_distribution()     # What it creates
```

## Migration Checklist

If updating from v1.0 to v2.0:

- [ ] Backup original `dashboard.py`
- [ ] Install new dependencies: `pip install -r requirements.txt`
- [ ] Copy your `churn dataset.csv` to new project
- [ ] Run app: `streamlit run app.py`
- [ ] Upload CSV in Settings page
- [ ] Verify data appears on Dashboard
- [ ] Check Analytics page statistics
- [ ] Review validation report in Settings
- [ ] Export and verify downloaded CSV
- [ ] Run tests: `pytest tests/ -v`

## FAQ

**Q: Will my existing CSV files work?**
A: Yes! v2.0 has more robust validation, but accepts the same column format.

**Q: How do I adjust the growth rate projection?**
A: Edit `src/config.py`, `ProjectionConfig.monthly_growth_rate` (0.05 = 5%)

**Q: Where do I add new analysis functions?**
A: Add methods to `ChurnAnalytics` class in `src/analytics.py`

**Q: How do I add a new visualization?**
A: Add method to `ChartGenerator` class in `src/visualizations.py`, then use in pages

**Q: Can I still use Matplotlib?**
A: Yes! Use `use_plotly=False` in ChartGenerator methods

**Q: How do I run tests?**
A: `pip install pytest` (already in requirements), then `pytest tests/ -v`

**Q: Is the data validated?**
A: Yes! Pydantic models validate every record against schema

---

**Next Steps**: Read `CODE_STRUCTURE.md` for detailed architecture explanation.
