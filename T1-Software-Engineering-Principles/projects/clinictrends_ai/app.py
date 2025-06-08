import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
from utils.preprocessing import load_and_process_csv, calculate_nps
import altair as alt
import pandas as pd

st.set_page_config(page_title="ClinicTrends AI", page_icon=":hospital:", layout="wide")

st.title("ClinicTrends AI")
st.subheader("NPS Feedback Analyzer at the palm of your hand")
st.write("Upload your NPS survey data and  let ClinicTrends AI analyze it for you.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = load_and_process_csv(uploaded_file)
    df["Year"] = df["Year"].astype(str).str.replace(",", "")
    df["Date"] = pd.to_datetime(df["Date"])  # Parse the Date column
    df["Month"] = df["Date"].dt.to_period("M").astype(str)    # Create a Month column

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
    
    filtered_df = df.copy()

    if selected_year != "All":
        filtered_df = filtered_df[filtered_df["Year"].astype(str) == selected_year]

    if selected_store != "All":
        filtered_df = filtered_df[filtered_df["Store"].astype(str) == selected_store]

    if not filtered_df.empty:
        nps_score = calculate_nps(filtered_df)
        st.write(f"NPS Score: {nps_score}")
        
        st.write("---")
        st.write("Data Preview")
        st.write(filtered_df.head(3))
        total_records = len(filtered_df)
        st.write(f"Total Records: {total_records}")
        
        st.write("---")
        chart_data = filtered_df["NPS Type"].value_counts().reset_index()
        chart_data.columns = ["NPS Type", "Count"]

        # Define color mapping
        color_scale = alt.Scale(domain=["Detractor", "Passive", "Promoter"],
                                range=["#e74c3c", "#f1c40f", "#2ecc71"])  # red, yellow, green

        donut_chart = alt.Chart(chart_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="NPS Type", type="nominal", scale=color_scale),
            tooltip=["NPS Type", "Count"]
        ).properties(
            title="NPS Type Distribution"
        )

        st.altair_chart(donut_chart, use_container_width=True)
    
        st.write("---")
        st.subheader("📈 NPS Over Time (Monthly)")
        st.dataframe(filtered_df)
        monthly_df = filtered_df.copy()
        monthly_df = monthly_df[monthly_df["NPS Type"] != "Unknown"]
        monthly_summary = monthly_df.groupby("Month").apply(lambda x: calculate_nps(x)).reset_index()
        monthly_summary.columns = ["Month", "NPS"]

        line_chart = alt.Chart(monthly_summary).mark_line(point=True).encode(
            x="Month",
            y=alt.Y("NPS", scale=alt.Scale(domain=[-100, 100])),
            tooltip=["Month", "NPS"]
        ).properties(
            title="Monthly NPS Trend"
        )

        st.altair_chart(line_chart, use_container_width=True)
    
    else:
        st.warning("No data found for the selected filters.")
