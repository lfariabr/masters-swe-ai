# Libs
import sys
import streamlit as st
import altair as alt
import pandas as pd
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

# Utils
from utils.preprocessing import load_and_process_csv, calculate_nps
from utils.visualizations import nps_donut_chart, monthly_nps_trend_chart
from utils.ui_filters import get_year_store_filters

st.set_page_config(page_title="ClinicTrends AI", page_icon="🏆", layout="wide")

st.title("ClinicTrends AI")
st.subheader("NPS Feedback Analyzer at the palm of your hand")
st.write("Upload your NPS survey data and  let ClinicTrends AI analyze it for you.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = load_and_process_csv(uploaded_file)
    selected_year, selected_store = get_year_store_filters(df)

    # Create filters
    col1, col2 = st.columns(2)
    
    with col1:
        selected_year = st.selectbox("Select a year", selected_year, index=selected_year.index("All"))
    with col2:
        selected_store = st.selectbox("Select a store", selected_store, index=selected_store.index("All"))
    
    filtered_df = df.copy()

    if selected_year != "All":
        filtered_df = filtered_df[filtered_df["Year"].astype(str) == selected_year]

    if selected_store != "All":
        filtered_df = filtered_df[filtered_df["Store"].astype(str) == selected_store]

    if not filtered_df.empty:
        nps_score = calculate_nps(filtered_df)
        st.write(f"NPS Score: {nps_score}")
        
        st.write("---")
        st.write("Random Data Preview")
        st.write(filtered_df.sample(3))
        total_records = len(filtered_df)
        st.write(f"Total Records: {total_records}")
        
        st.write("---")

        col1, col2 = st.columns(2)
        
        with col1:
            donut_chart = nps_donut_chart(filtered_df)
            st.altair_chart(donut_chart, use_container_width=True)
        
        with col2:
            line_chart = monthly_nps_trend_chart(filtered_df, calculate_nps)
            st.altair_chart(line_chart, use_container_width=True)
    
    else:
        st.warning("No data found for the selected filters.")
