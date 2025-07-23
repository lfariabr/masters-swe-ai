import streamlit as st
from pathlib import Path
import sys
import altair as alt
import requests

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))
from utils.preprocessing import load_and_process_csv, calculate_nps
from utils.visualizations import nps_donut_chart, monthly_nps_trend_chart, create_nps_explanations
from utils.ui_filters import get_year_store_filters
from utils.nlp_analysis import display_sentiment_distribution, display_wordcloud, annotate_sentiments
from utils.alerts import send_discord_message
from utils.data_upload import data_upload


def show_dashboard():
    """Show the dashboard page content."""

    st.title("📈 NPS Analytics Dashboard")
    
    create_nps_explanations()

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        data_upload()

    with col2:
        st.markdown("#### 📁 Data Upload")
        uploaded_file = st.file_uploader(
        "Upload your CSV file or use the sample data",
        type="csv",
        help="File should contain 'Comment' and 'Score' columns"
    )

    if uploaded_file is not None:
        send_discord_message("🔄 Starting data upload and validation process at NPS Page")
        df = load_and_process_csv(uploaded_file)

        with st.expander("👀 Data Preview (just in case you want to check it)"):
            st.dataframe(df.sample(min(5, len(df))), use_container_width=True)
            total_records = len(df)
            st.info(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
            st.success(f"Total records loaded: {total_records}")
        
        st.markdown("---")

        st.subheader("NPS Filters")
        selected_year, selected_store = get_year_store_filters(df)

        st.markdown("---")

        st.subheader("NPS Analysis")

        col1, col2 = st.columns(2)    
        filtered_df = df.copy()

        if selected_year != "All":
            filtered_df = filtered_df[filtered_df["Year"].astype(str) == selected_year]

        if selected_store != "All":
            filtered_df = filtered_df[filtered_df["Store"].astype(str) == selected_store]

        if not filtered_df.empty:
            nps_score = calculate_nps(filtered_df)
            
            col1, col2 = st.columns(2)
            
            with col1:
                donut_chart = nps_donut_chart(filtered_df)
                st.altair_chart(donut_chart, use_container_width=True)
                   
            with col2:
                if "Store" in filtered_df.columns and "NPS Type" in filtered_df.columns:
                    store_nps_type = (
                        filtered_df.groupby(["Store", "NPS Type"])
                        .size()
                        .reset_index(name="Count")
                    )
                    stacked_chart = alt.Chart(store_nps_type).mark_bar().encode(
                        x=alt.X("Store:N", sort=None),
                        y=alt.Y("Count:Q", stack="zero"),
                        color=alt.Color("NPS Type:N", scale=alt.Scale(domain=["Promoter", "Passive", "Detractor"], range=["#2ecc71", "#f1c40f", "#e74c3c"])),
                        tooltip=["Store", "NPS Type", "Count"]
                    ).properties(title="NPS Type Distribution by Store")
                    st.altair_chart(stacked_chart, use_container_width=True)
                else:
                    st.info("No store or NPS type data available for breakdown.")
            
            col3, col4 = st.columns(2)

            with col3:
                st.markdown("#### 📊 Monthly NPS Trend")
                line_chart = monthly_nps_trend_chart(filtered_df, calculate_nps)
                st.altair_chart(line_chart, use_container_width=True)

            with col4:
                st.markdown("#### 🌡️ NPS Status")

                if nps_score < 50:
                    st.error(f"⚠️ ALERT: Your NPS is critically low ({nps_score}). Immediate action is recommended!")
                    send_discord_message(f"🚨 CRITICAL ALERT: NPS is very low ({nps_score}).")
                elif nps_score < 80:
                    st.warning(f"🔔 Caution: Your NPS is {nps_score}. Consider investigating customer issues.")
                else:
                    st.success(f"✅ All good! Your NPS is healthy at {nps_score}.")
                
                annotated_df = annotate_sentiments(
                    filtered_df,
                    comment_col="Comment",
                    pos_thresh=0.05,
                    neg_thresh=-0.05
                )

                neg_rate = (
                    len(annotated_df[annotated_df["Sentiment"] == "Negative"])
                    / len(annotated_df) * 100
                )
                if neg_rate > 30:
                    st.error(f"⚠️ ALERT: High negative sentiment detected ({neg_rate:.1f}%).")
                    send_discord_message(f"🚨 High negative sentiment detected ({neg_rate:.1f}%).")
                elif neg_rate > 10:
                    st.warning(f"🔔 Moderate negative sentiment ({neg_rate:.1f}%). Monitor customer feedback closely.")
                else:
                    st.success(f"✅ Low negative sentiment ({neg_rate:.1f}%). Great job!")

        else:
            st.warning("No data found for the selected filters.")

        st.markdown("---")
    
        st.subheader("Sentiment Distribution")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Adjust these thresholds to fine-tune sentiment classification.")
            st.info("Comments with a polarity score above this value will be classified as POSITIVE. Lower values make the model more sensitive to mildly positive comments.")
            pos_thresh = st.slider("Positive threshold", min_value=0.01, max_value=0.5, value=0.05, step=0.01)
            st.warning("Comments with a polarity score below this value will be classified as NEGATIVE. Lower (more negative) values capture only strongly negative comments, while higher values include milder negativity.")
            neg_thresh = st.slider("Negative threshold", min_value=-0.5, max_value=-0.01, value=-0.05, step=0.01)

        with col2:
            display_sentiment_distribution(annotated_df)
        
        st.markdown("---")

        st.subheader("Word Cloud from Comments")
        display_wordcloud(annotated_df)

        ## DEBUG
        ###############
        # st.subheader("Comments with TextBlob Sentiment")
        # st.dataframe(annotated_df[["Date", "Store", "Comment", "Score", "NPS Type", "Sentiment", "Polarity"]].dropna(), use_container_width=True)
        
        # st.write("---")
        # st.subheader("Positive Comments")
        # st.dataframe(annotated_df[annotated_df["Sentiment"] == "Positive"][["Date", "Store", "Comment", "Score", "NPS Type", "Sentiment", "Polarity"]].dropna(), use_container_width=True)
        # st.subheader("Negative Comments")
        # st.dataframe(annotated_df[annotated_df["Sentiment"] == "Negative"][["Date", "Store", "Comment", "Score", "NPS Type", "Sentiment", "Polarity"]].dropna(), use_container_width=True)

        # st.write("---")
        # st.markdown("### CHECKING NPS DATA vs SENTIMENT")
        # col1, col2 = st.columns(2)
        # with col1:
        #     # NPS pizza graphic
        #     donut_chart = nps_donut_chart(filtered_df)
        #     st.altair_chart(donut_chart, use_container_width=True)
        #     st.dataframe(filtered_df["NPS Type"].value_counts().reset_index(), use_container_width=True)
        # with col2:
        #     # Sentiment distribution graphic
        #     annotated_df["Sentiment"] = annotated_df["Sentiment"].astype(str)
        #     sentiment_distribution_chart = annotated_df.groupby("Sentiment").size().reset_index(name="Count")

        #     bar_chart = alt.Chart(sentiment_distribution_chart).mark_arc(innerRadius=50).encode(
        #         theta=alt.Theta(field="Count", type="quantitative"),
        #         color=alt.Color(field="Sentiment", type="nominal", scale=alt.Scale(domain=["Positive", "Negative", "Neutral"], range=["#2ecc71", "#e74c3c", "#f1c40f"])),
        #         tooltip=["Sentiment", "Count"]
        #     ).properties(
        #         title="Sentiment Distribution - TextBlob"
        #     )

        #     st.altair_chart(bar_chart, use_container_width=True)
        #     st.dataframe(sentiment_distribution_chart, use_container_width=True)

    else:
        st.info("""
        👆 **Upload a CSV file to begin NPS analysis**
        
        Your file should contain:
        - `Comment` column: Customer feedback text
        - `Score` column: Numerical rating (0-10)
        - Optional: `Date`, `Store` columns for additional analysis
        """)

if __name__ == "__main__":
    show_dashboard()