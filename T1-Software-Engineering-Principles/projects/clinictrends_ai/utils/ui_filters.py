import streamlit as st
import pandas as pd

def get_year_store_filters(df: pd.DataFrame):
    years = sorted(list(set(str(y).replace(",", "") for y in df["Year"].dropna())))
    years.append("All")

    stores = df['Store'].dropna().unique()
    stores = sorted(list(set(str(s).replace(",", "") for s in stores)))
    stores.append("All")

    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.selectbox("Select a year", years, index=years.index("All"))
    with col2:
        selected_store = st.selectbox("Select a store", stores, index=stores.index("All"))

    return selected_year, selected_store