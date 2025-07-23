import requests
import streamlit as st

def data_upload():
    st.markdown("#### ℹ️ Sample Data")
    csv_url = "https://raw.githubusercontent.com/lfariabr/masters-swe-ai/master/T1-Software-Engineering-Principles/projects/clinictrends_ai/public/clinicTrendsAiSample.csv"
    response = requests.get(csv_url)

    if response.status_code == 200:
        st.download_button(
            label="Download sample csv data",
            data=response.content,
            file_name="clinicTrendsAiSample.csv",
            mime="text/csv",
            help="Click to download a sample CSV data for testing the application."
        )   
        st.caption("💡 File with mock customer reviews for testing purposes.")
    else:
        st.error("Sample CSV file not found!")