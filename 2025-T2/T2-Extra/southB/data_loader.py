"""Data loading and processing functions."""
import pandas as pd
import streamlit as st


@st.cache_data
def load_ledger(file_path):
    """
    Load and process ledger data from Excel file.
    
    Args:
        file_path: Path or file object to Excel file
        
    Returns:
        dict: Dictionary of DataFrames, one per sheet
    """
    df = pd.read_excel(file_path, sheet_name=None)
    
    for sheet_name, data in df.items():
        # Normalize column names - replace newlines and extra spaces
        data.columns = (
            data.columns.str.replace('\n', ' ')
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
        )
        
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
