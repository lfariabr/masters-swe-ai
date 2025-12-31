"""Main Streamlit application."""
import streamlit as st
from datetime import datetime

from data_loader import load_ledger
from filters import apply_filters
from analytics import show_summary_metrics, show_analytics


def main():
    """Main application entry point."""
    st.set_page_config(page_title="South B Ledger Analysis", layout="wide")
    
    st.title("🏢 South B Ledger Analysis")
    
    # File upload
    uploaded_file = st.file_uploader("Upload Ledger Excel File", type=["xlsx"])
    if uploaded_file is None:
        st.info("Please upload an Excel file to proceed.")
        st.stop()
    
    # Load data
    ledger_data = load_ledger(uploaded_file)
    
    # Sidebar - Sheet selection
    st.sidebar.header("📋 Navigation")
    sheet_names = list(ledger_data.keys())
    selected_sheet = st.sidebar.selectbox("Select Building/Location:", sheet_names)
    
    # Get selected data
    df = ledger_data[selected_sheet].copy()
    
    st.header(f"📊 {selected_sheet}")
    
    # Apply filters
    df = apply_filters(df)
    
    # Summary metrics
    show_summary_metrics(df)
    
    # Display data
    st.subheader("📋 Filtered Data")
    with st.expander("Show/Hide Data Table"):
        st.dataframe(df, width='stretch', height=400)
    
    # Download filtered data
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name=f"{selected_sheet}_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    # Analytics
    show_analytics(df)


if __name__ == "__main__":
    main()
