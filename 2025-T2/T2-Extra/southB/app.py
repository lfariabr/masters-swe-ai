import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="South B Ledger Analysis", layout="wide")

st.title("🏢 South B Ledger Analysis")

# Load ledger data
@st.cache_data
def load_ledger(file_path):
    df = pd.read_excel(file_path, sheet_name=None)
    
    for sheet_name, data in df.items():
        # Normalize column names - replace newlines and extra spaces
        data.columns = data.columns.str.replace('\n', ' ').str.replace(r'\s+', ' ', regex=True).str.strip()
        
        # Convert all object columns to string to prevent Arrow serialization issues
        for col in data.columns:
            if data[col].dtype == 'object':
                data[col] = data[col].astype(str).str.strip()
                data[col] = data[col].str.replace(r'\s+', ' ', regex=True)
                data[col] = data[col].replace('nan', pd.NA)
        
        # Convert Date columns to datetime
        if 'Date' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        
        # Convert Amount columns to numeric
        if 'Amount inc GST' in data.columns:
            data['Amount inc GST'] = pd.to_numeric(data['Amount inc GST'], errors='coerce')
    
    return df

# ledger_data = load_ledger("/workspaces/msters-swe-ai/2025-T2/T2-Extra/southB/ledger.xlsx")
# replace data loader with data uploader
uploaded_file = st.file_uploader("Upload Ledger Excel File", type=["xlsx"])
if uploaded_file is not None:
    ledger_data = load_ledger(uploaded_file)
else:
    st.info("Please upload an Excel file to proceed.")
    st.stop()
# Sidebar - Sheet selection
st.sidebar.header("📋 Navigation")
sheet_names = list(ledger_data.keys())
selected_sheet = st.sidebar.selectbox("Select Building/Location:", sheet_names)

# Get selected data
df = ledger_data[selected_sheet].copy()

st.header(f"📊 {selected_sheet}")

# Filters Section
st.sidebar.header("🔍 Filters")

# Year filter
if 'Date' in df.columns and df['Date'].notna().any():
    df['Year'] = df['Date'].dt.year
    available_years = sorted(df['Year'].dropna().unique().astype(int).tolist())
    
    if available_years:
        selected_years = st.sidebar.multiselect(
            "Year(s):",
            options=available_years,
            default=available_years
        )
        if selected_years:
            df = df[df['Year'].isin(selected_years)]

# Date range filter
if 'Date' in df.columns and df['Date'].notna().any():
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    date_range = st.sidebar.date_input(
        "Date Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        df = df[(df['Date'] >= pd.Timestamp(date_range[0])) & 
                (df['Date'] <= pd.Timestamp(date_range[1]))]

# Contractor filter
if 'Contractor' in df.columns:
    contractors = ['All'] + sorted(df['Contractor'].dropna().unique().tolist())
    selected_contractor = st.sidebar.selectbox("Contractor:", contractors)
    if selected_contractor != 'All':
        df = df[df['Contractor'] == selected_contractor]

# Service filter
if 'Service' in df.columns:
    services = ['All'] + sorted(df['Service'].dropna().unique().tolist())
    selected_service = st.sidebar.selectbox("Service:", services)
    if selected_service != 'All':
        df = df[df['Service'].str.contains(selected_service, case=False, na=False)]

# Invoice filter
if 'Invoice #' in df.columns:
    invoice_search = st.sidebar.text_input("Search Invoice #:")
    if invoice_search:
        df = df[df['Invoice #'].astype(str).str.contains(invoice_search, case=False, na=False)]

# Amount filter
if 'Amount inc GST' in df.columns:
    df['Amount inc GST'] = pd.to_numeric(df['Amount inc GST'], errors='coerce')
    
    if df['Amount inc GST'].notna().any():
        min_amount = float(df['Amount inc GST'].min())
        max_amount = float(df['Amount inc GST'].max())
        
        amount_range = st.sidebar.slider(
            "Amount Range (GST inc):",
            min_value=min_amount,
            max_value=max_amount,
            value=(min_amount, max_amount)
        )
        df = df[(df['Amount inc GST'] >= amount_range[0]) & 
                (df['Amount inc GST'] <= amount_range[1])]

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", len(df))

with col2:
    if 'Amount inc GST' in df.columns:
        total_amount = df['Amount inc GST'].sum()
        st.metric("Total Amount", f"${total_amount:,.2f}")

with col3:
    if 'Contractor' in df.columns:
        unique_contractors = df['Contractor'].nunique()
        st.metric("Contractors", unique_contractors)

with col4:
    if 'Service' in df.columns:
        unique_services = df['Service'].nunique()
        st.metric("Services", unique_services)

# Display data
st.subheader("📋 Filtered Data")
with st.expander("Show/Hide Data Table"):
    st.dataframe(df, width='stretch', height=400)

# Additional analytics
st.subheader("📈 Analytics")

# Debug info - remove after fixing
# with st.expander("🔍 Debug Info"):
#     st.write(f"Total rows after filtering: {len(df)}")
#     st.write(f"Columns: {list(df.columns)}")
#     if 'Amount inc GST' in df.columns:
#         st.write(f"Amount inc GST - Non-null count: {df['Amount inc GST'].notna().sum()}")
#         st.write(f"Amount inc GST - Sum: ${df['Amount inc GST'].sum():,.2f}")
#         st.write(f"Amount inc GST - Data type: {df['Amount inc GST'].dtype}")
#     if 'Contractor' in df.columns:
#         st.write(f"Contractors with data: {df['Contractor'].notna().sum()}")
#         st.write(f"Unique contractors: {df['Contractor'].nunique()}")

col1, col2 = st.columns(2)

with col1:
    if 'Contractor' in df.columns and 'Amount inc GST' in df.columns:
        st.write("**Spending by Contractor**")
        
        # Filter out rows without contractor or amount
        df_valid = df[(df['Contractor'].notna()) & (df['Amount inc GST'].notna())].copy()
        
        if len(df_valid) > 0:
            contractor_spending = df_valid.groupby('Contractor')['Amount inc GST'].sum().sort_values(ascending=False)
            
            if not contractor_spending.empty and contractor_spending.sum() > 0:
                # Create a proper dataframe for display
                contractor_df = pd.DataFrame({
                    'Contractor': contractor_spending.index,
                    'Total Spent': contractor_spending.values
                })
                st.dataframe(contractor_df.style.format({'Total Spent': '${:,.2f}'}), width='stretch', hide_index=True)
                st.bar_chart(contractor_spending)
            else:
                st.info("No spending data to display")
        else:
            st.info("No valid contractor/amount data for selected filters")

with col2:
    if 'Date' in df.columns and 'Amount inc GST' in df.columns:
        st.write("**Spending Over Time**")
        
        # Filter out rows without dates or amounts
        df_with_dates = df[(df['Date'].notna()) & (df['Amount inc GST'].notna())].copy()
        
        if not df_with_dates.empty:
            monthly_spending = df_with_dates.set_index('Date').resample('M')['Amount inc GST'].sum()
            
            if not monthly_spending.empty and monthly_spending.sum() > 0:
                st.line_chart(monthly_spending)
                
                # Show monthly breakdown
                monthly_df = pd.DataFrame({
                    'Month': monthly_spending.index.strftime('%Y-%m'),
                    'Amount': monthly_spending.values
                })
                st.dataframe(monthly_df.style.format({'Amount': '${:,.2f}'}), width='stretch')
            else:
                st.info("No spending data available for the date range")
        else:
            st.info("No valid date/amount data for selected filters")