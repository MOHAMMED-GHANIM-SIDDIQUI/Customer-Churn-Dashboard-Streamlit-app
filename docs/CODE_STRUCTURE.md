# Code Structure & Architecture Documentation

## Overview

The refactored Customer Churn Dashboard follows a clean architecture with clear separation of concerns. This document explains the design decisions and module relationships.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│               Streamlit UI Layer                    │
│  (app.py, pages/dashboard.py, pages/analytics.py)  │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
┌────────────┐ ┌──────────┐ ┌──────────────┐
│  Config    │ │ DataLoader│ │ Analytics   │
│  (config.py)│ │(data_...py)│ │(analytics.py)│
└────────────┘ └──────────┘ └──────────────┘
        │          │          │
        │          ▼          │
        │     ┌─────────────┐ │
        │     │  Models     │ │
        │     │ (models.py) │ │
        │     └─────────────┘ │
        │                      │
        └──────────┬───────────┘
                   │
        ┌──────────┴─────────┐
        │                    │
        ▼                    ▼
┌──────────────┐     ┌────────────────┐
│  Visualizations │   │    Utils       │
│ (visualizations)│   │   (utils.py)   │
└──────────────┘     └────────────────┘
```

## Module Descriptions

### 1. **config.py** - Configuration Management
**Purpose**: Centralize all configuration and magic numbers.

**Key Classes**:
- `ColumnMapping`: Maps CSV column names (source of truth for column references)
- `ProjectionConfig`: Business logic parameters for future projections
- `AppConfig`: General app settings

**Why Separate**:
- Non-developers can adjust business logic without touching code
- Easy to test different configurations
- Supports multiple environments (dev/prod)

**Example Usage**:
```python
config = get_column_mapping()
avg_age = df[config.age].mean()  # Uses named column, not index
```

### 2. **models.py** - Data Validation
**Purpose**: Define data schema and validation rules.

**Key Classes**:
- `CustomerRecord`: Pydantic model for single customer validation
- `DataValidationResult`: Report of validation results
- `validate_dataframe_records()`: Validate entire dataset
- `validate_required_columns()`: Check for missing columns

**Why Separate**:
- Validation logic isolated from business logic
- Reusable for API endpoints or batch processing
- Clear error messages for users
- Type safety throughout application

**Benefits**:
- Catches bad data early
- Fails fast with clear errors
- Impossible to process invalid data

### 3. **data_loader.py** - Data Input Layer
**Purpose**: Handle CSV loading and preprocessing.

**Key Class**:
- `DataLoader`: Orchestrates loading, validation, and cleaning
- `DataLoadError`: Custom exception for data issues

**Methods**:
- `load_from_uploaded_file()`: Load Streamlit file object
- `validate_schema()`: Check required columns present
- `validate_data_quality()`: Generate quality report
- `clean_data()`: Remove duplicates and handle missing values
- `load_and_validate()`: Complete pipeline

**Why Separate**:
- Decouples data input from business logic
- Easy to add new file formats (Parquet, Excel, etc.)
- Testable in isolation
- Clear error handling at entry point

**Example Flow**:
```python
loader = DataLoader()
df, report = loader.load_and_validate(uploaded_file)
# Returns cleaned data + quality report
```

### 4. **analytics.py** - Core Business Logic
**Purpose**: Pure analytics functions with no side effects.

**Key Class**:
- `ChurnAnalytics`: Encapsulates all customer analysis

**Key Methods**:
- `calculate_basic_statistics()`: Key metrics
- `calculate_projections_next_year()`: Future forecasts
- `segment_customers_by_risk()`: Risk categorization
- `get_churn_rate_by_gender()`: Demographic breakdowns
- `get_average_spend_by_subscription()`: Spending analysis

**Why Pure Functions**:
- No side effects (don't modify state)
- Fully testable
- Can be called from anywhere
- Results reproducible
- Easy to parallelize/optimize

**Design Pattern** - Class-based for convenience:
```python
analytics = ChurnAnalytics(df, config, projections_config)
stats = analytics.calculate_basic_statistics()
# Stats are computed fresh each time (no caching here)
# Caching happens at Streamlit layer
```

### 5. **visualizations.py** - Chart Generation
**Purpose**: Create charts with consistent styling.

**Key Class**:
- `ChartGenerator`: Creates various visualization types

**Key Methods**:
- `create_age_distribution()`: Age histogram
- `create_gender_distribution()`: Gender pie chart
- `create_churn_rate_by_gender()`: Churn comparison
- `create_risk_distribution()`: Risk pie chart
- Plus 3 more analysis charts

**Design Features**:
- `use_plotly` parameter for interactive vs static charts
- Consistent color palette
- Named column usage (not indices)
- Reusable across pages

**Example**:
```python
chart_gen = ChartGenerator()
fig = chart_gen.create_age_distribution(df, use_plotly=True)
st.plotly_chart(fig)
```

### 6. **utils.py** - Helper Functions
**Purpose**: Utility functions and cross-cutting concerns.

**Key Functions**:
- `setup_logging()`: Configure logging
- `handle_errors()`: Error handling decorator
- `streamlit_cache_with_ttl()`: Caching decorator
- `format_currency()`, `format_percentage()`: Formatting
- `get_risk_color()`: Color mapping for UI
- `validate_dataframe_not_empty()`: DataFrame checks

**Why Separate**:
- Reusable helpers across modules
- Logging and error handling centralized
- Formatting consistency
- Easy to test

### 7. **app.py** - Main Entry Point
**Purpose**: Configure and orchestrate the Streamlit app.

**Key Functions**:
- `configure_app()`: Page settings
- `initialize_session_state()`: Session setup
- `render_home_page()`: Landing page
- `main()`: Page routing

**Design**:
- Single page routing logic
- Session state management
- Conditional rendering based on data availability

### 8. **pages/dashboard.py** - Dashboard Page
**Purpose**: Display customer visualizations.

**Layout**:
- Key metrics cards (4 columns)
- 6 analysis charts (3 rows × 2 columns)
- Risk breakdown
- Export buttons

**Data Flow**:
```
Session State DataFrame
    ↓
ChurnAnalytics (computes metrics & risk)
    ↓
ChartGenerator (creates visualizations)
    ↓
Streamlit renders (metrics + charts + exports)
```

### 9. **pages/analytics.py** - Analytics Page
**Purpose**: Detailed statistics and exploration.

**Tabs**:
1. **Statistics**: Key metrics in grid layout
2. **Projections**: 12-month forecasts with methodology
3. **Data Explorer**: Sample records and risk segments
4. **About Dataset**: Schema and statistics

### 10. **pages/settings.py** - Settings Page
**Purpose**: Data upload and validation.

**Functions**:
- File uploader with error handling
- Data quality report generation
- Column information display
- Statistics summary

## Data Flow Examples

### Example 1: User Uploads CSV
```
User clicks Upload
    ↓
Streamlit file_uploader returns file object
    ↓
DataLoader.load_and_validate()
    ├─ load_from_uploaded_file() - reads CSV
    ├─ validate_schema() - checks columns exist
    ├─ validate_data_quality() - validates values
    └─ clean_data() - removes duplicates/nulls
    ↓
Returns (cleaned_df, quality_report)
    ↓
Stored in st.session_state
    ↓
Page refreshes, shows success + report
```

### Example 2: User Clicks Dashboard Button
```
User navigates to Dashboard page
    ↓
Streamlit calls show_dashboard()
    ↓
Retrieve df from st.session_state
    ↓
Create ChurnAnalytics(df)
    ├─ calculate_basic_statistics()
    ├─ segment_customers_by_risk()
    └─ (other analyses)
    ↓
Create ChartGenerator()
    ├─ create_age_distribution()
    ├─ create_gender_distribution()
    └─ (other charts)
    ↓
st.metric() and st.pyplot() render results
    ↓
User sees dashboard with all visualizations
```

### Example 3: Data Validation Process
```
CSV File Loaded
    ↓
validate_required_columns() ✓
    ↓
validate_dataframe_records() 
    ├─ For each row: CustomerRecord(**row) validation
    ├─ Age: must be 0-150
    ├─ Gender: must be Male/Female/Other
    ├─ Tenure: must be >= 0
    └─ ... other field validations
    ↓
generate report
    ├─ Total records
    ├─ Valid records
    ├─ Invalid records with errors
    └─ Warnings (missing values, high churn rate)
    ↓
If valid: load data into session
If invalid: show errors to user
```

## Naming Conventions

### Functions
- **Verb-Noun**: `calculate_basic_statistics()`, `create_age_distribution()`
- **Interrogative**: `validate_dataframe_not_empty()`, `validate_required_columns()`
- **Clear intent**: `load_and_validate()` not `process()`, `segment_customers_by_risk()` not `segment()`

### Variables
- **Descriptive**: `average_age` not `avg_a`, `churn_rate_percent` not `churn_pct`
- **Boolean prefix**: `is_valid`, `has_data`, `use_plotly`
- **Plural for collections**: `customers`, `errors`, `projections`

### Classes
- **Noun-based**: `ChurnAnalytics`, `ChartGenerator`, `DataLoader`
- **Suffix for context**: `Error` for exceptions, `Config` for configuration
- **Camel case**: `PascalCase`

### Constants
- **Upper snake case**: `DEFAULT_BATCH_SIZE = 1000`, `MAX_UPLOAD_SIZE_MB = 100`
- **Global config**: in `config.py` as dataclass fields

## Error Handling Strategy

### By Layer:

**Data Layer (data_loader.py)**
- Raises `DataLoadError` with descriptive message
- Catches and translates pandas errors
- Validates before returning data

**Analytics Layer (analytics.py)**
- Assumes valid input (validation happened earlier)
- Returns computed values or raises on logic errors
- No error handling (pure functions)

**UI Layer (pages/*.py)**
- Catches exceptions and displays user-friendly messages
- Uses `st.error()`, `st.warning()`, `st.info()`
- Shows error details in expandable sections

**Example in Settings page**:
```python
try:
    df, report = loader.load_and_validate(file)
    st.session_state.dataframe = df
    st.success("Data loaded!")
except DataLoadError as e:
    st.error(f"Loading Error: {str(e)}")
except Exception as e:
    st.error(f"Unexpected Error: {str(e)}")
```

## Testing Strategy

### Unit Tests (tests/test_analytics.py)
- **Pure function tests**: No dependencies on Streamlit or UI
- **Fixtures**: Sample DataFrames with known values
- **Assertions**: Verify computations, value ranges, structure

### Test Organization:
```python
@pytest.fixture
def sample_dataframe():
    # Create known test data
    
class TestChurnAnalyticsBasicStatistics:
    def test_calculate_basic_statistics_returns_dict(self):
        # Verify structure
    
    def test_average_age_calculation(self):
        # Verify computation accuracy
    
    def test_churn_rate_is_percentage(self):
        # Verify value constraints
```

### What NOT to Test:
- Streamlit rendering (hard to test, rarely breaks)
- External library functions (already tested)
- Configuration values (documentation is enough)

## Performance Considerations

### Current Implementation
- Loads entire CSV into memory
- Recomputes analytics on each page view
- Streamlit caching helps but not optimal

### Future Optimizations
1. **Polars instead of Pandas**: 10-100x faster I/O
2. **Database layer**: Persistent storage, queries
3. **ML predictions**: Pre-computed models
4. **Lazy evaluation**: Only compute viewed charts
5. **Caching strategy**: Smart invalidation with data hashing

### Scalability Limits
- **Current**: ~100K rows comfortably
- **With Polars**: ~10M rows
- **With database**: Unlimited (query-based)

## Extension Points

### Adding New Analysis
1. Add method to `ChurnAnalytics` class
2. Add visualization to `ChartGenerator`
3. Create new page in `pages/`
4. Add navigation in `app.py`

### Adding New Data Source
1. Create method in `DataLoader`
2. Validate using existing Pydantic models
3. Same pipeline thereafter

### Adding New Validation Rule
1. Add `@field_validator` to `CustomerRecord`
2. Define validation logic
3. Returns feedback in validation report

---

**Key Principle**: Clean architecture with clear separation of concerns makes code testable, maintainable, and extensible.
