"""Analytics and visualization components."""
import streamlit as st
import pandas as pd


def show_summary_metrics(df):
    """Display summary metrics in columns."""
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


def show_contractor_spending(df):
    """Display spending by contractor chart and table."""
    if 'Contractor' not in df.columns or 'Amount inc GST' not in df.columns:
        return
    
    # Add visual header with icon and color
    st.markdown("### 👷 Contractor Breakdown")
    st.markdown("---")
    
    # Filter out rows without contractor or amount
    df_valid = df[(df['Contractor'].notna()) & (df['Amount inc GST'].notna())].copy()
    
    if len(df_valid) > 0:
        contractor_spending = (
            df_valid.groupby('Contractor')['Amount inc GST']
            .sum()
            .sort_values(ascending=False)
        )
        
        if not contractor_spending.empty and contractor_spending.sum() > 0:
            # Create a proper dataframe for display
            contractor_df = pd.DataFrame({
                'Contractor': contractor_spending.index,
                'Total Spent': contractor_spending.values
            })
            
            # Apply color heatmap to the Total Spent column
            styled_df = contractor_df.style.format({'Total Spent': '${:,.2f}'}).background_gradient(
                subset=['Total Spent'],
                cmap='RdYlGn_r',  # Red (high) to Yellow to Green (low)
                vmin=contractor_df['Total Spent'].min(),
                vmax=contractor_df['Total Spent'].max()
            )
            
            st.dataframe(styled_df, width='stretch', hide_index=True)
            st.bar_chart(contractor_spending)
        else:
            st.info("No spending data to display")
    else:
        st.info("No valid contractor/amount data for selected filters")


def show_spending_over_time(df):
    """Display spending over time chart and table."""
    if 'Date' not in df.columns or 'Amount inc GST' not in df.columns:
        return
    
    # Add visual header with icon and color
    st.markdown("### 📅 Monthly Expenses Timeline")
    st.markdown("---")
    
    # Filter out rows without dates or amounts
    df_with_dates = df[(df['Date'].notna()) & (df['Amount inc GST'].notna())].copy()
    
    if not df_with_dates.empty:
        monthly_spending = (
            df_with_dates.set_index('Date')
            .resample('ME')['Amount inc GST']
            .sum()
        )
        
        if not monthly_spending.empty and monthly_spending.sum() > 0:
            st.line_chart(monthly_spending)
            
            # Show monthly breakdown
            monthly_df = pd.DataFrame({
                'Month': monthly_spending.index.strftime('%Y-%m'),
                'Amount': monthly_spending.values
            })
            
            # Apply color heatmap to the Amount column
            styled_monthly = monthly_df.style.format({'Amount': '${:,.2f}'}).background_gradient(
                subset=['Amount'],
                cmap='Reds',  # Light to dark red gradient
                vmin=monthly_df['Amount'].min(),
                vmax=monthly_df['Amount'].max()
            )
            
            st.dataframe(styled_monthly, width='stretch', hide_index=True)
        else:
            st.info("No spending data available for the date range")
    else:
        st.info("No valid date/amount data for selected filters")


def show_analytics(df):
    """Display all analytics sections."""
    st.subheader("📈 Analytics")
    st.markdown("") # Add spacing
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        with st.container(border=True):
            show_contractor_spending(df)
    
    with col2:
        with st.container(border=True):
            show_spending_over_time(df)
