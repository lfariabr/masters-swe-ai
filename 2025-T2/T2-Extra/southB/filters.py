"""Filter components for the Streamlit app."""
import streamlit as st
import pandas as pd


def apply_filters(df):
    """
    Apply sidebar filters to the dataframe.
    
    Args:
        df: DataFrame to filter
        
    Returns:
        DataFrame: Filtered dataframe
    """
    st.sidebar.write("---")
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
    
    return df
