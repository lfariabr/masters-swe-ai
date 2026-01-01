# South B Ledger Analysis - Modular Structure

## File Structure

```
southB/
├── app.py              # Main entry point
├── data_loader.py      # Data loading and processing
├── filters.py          # Filter components
├── analytics.py        # Analytics and visualizations
└── README.MD           # This file
```

## Module Responsibilities

### `app.py`
- Main application entry point
- Orchestrates the UI flow
- Handles file upload
- Calls functions from other modules

### `data_loader.py`
- `load_ledger()`: Loads Excel file and processes data
- Normalizes column names
- Converts data types (dates, amounts)
- Cleans text fields

### `filters.py`
- `apply_filters()`: Renders sidebar filters and applies them to dataframe
- Year filter
- Date range filter
- Contractor filter
- Service filter
- Invoice search
- Amount range slider

### `analytics.py`
- `show_summary_metrics()`: Display key metrics (total records, amount, contractors, services)
- `show_contractor_spending()`: Bar chart and table of spending by contractor
- `show_spending_over_time()`: Line chart and table of monthly spending
- `show_analytics()`: Main analytics orchestration function

## How to Run

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
streamlit run app.py
```

## Benefits of Modular Structure

1. **Maintainability**: Each module has a single responsibility
2. **Testability**: Functions can be unit tested independently
3. **Reusability**: Components can be used in other projects
4. **Readability**: Easier to understand and navigate
5. **Collaboration**: Multiple developers can work on different modules