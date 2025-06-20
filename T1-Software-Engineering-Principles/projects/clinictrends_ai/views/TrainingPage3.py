import streamlit as st
from pathlib import Path
import sys
import altair as alt
import pandas as pd
import sklearn
from sklearn.metrics import classification_report
from utils.visualizations import nps_donut_chart
from utils.nlp_analysis import annotate_sentiments
from utils.preprocessing import classify_nps

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))

def show_training3():
    """Show the training page content."""
    st.title("Training Page 3")
    st.write("This is the training page.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)  # use your actual file path
        df = df.dropna(subset=["Comment"])
        
        st.write('Data preview')
        st.write(df)

        st.write("---")

        df = annotate_sentiments(df)

        st.write('Data preview with NLP')
        st.write(df)

        st.write("---")
        # st.write("Vectorizing data")
        from sklearn.feature_extraction.text import TfidfVectorizer

        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        X = vectorizer.fit_transform(df["Comment"])
        # y = df["Sentiment"]
        from transformers import pipeline
        sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        hf_results = sentiment_pipeline(df["Comment"].tolist(), truncation=True)
        df["HF_Label"] = [res["label"] for res in hf_results]
        y = df["HF_Label"]

        # st.write("Vectorized data")

        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        # Predict using trained model
        df["ML_Sentiment"] = model.predict(vectorizer.transform(df["Comment"]))

        # st.write("Model trained")

        st.markdown("## Model accuracy:")
        st.write(model.score(X_test, y_test))

        from sklearn.metrics import classification_report

        y_pred = model.predict(X_test)
        st.markdown("## Classification report:")
        st.write(classification_report(y_test, y_pred))

        st.write("---")
        st.markdown("### CHECKING NPS DATA vs SENTIMENT")
        col1, col2 = st.columns(2)
        df = classify_nps(df)

        # Clean and process date columns
        df["Year"] = df["Year"].astype(str).str.replace(",", "")
        df["Date"] = pd.to_datetime(df["Date"])  
        df["Month"] = df["Date"].dt.to_period("M").astype(str)

        from transformers import pipeline
        sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

        st.subheader("Comments with Hugging Face Transformers Sentiment")

        # Take a sample of comments with non-empty strings
        sample_df = df[["Date", "Store", "Comment", "Sentiment", "Polarity", "Score"]].dropna().sample(50).copy()

        # Apply the Hugging Face model only to the comments
        hf_results = sentiment_pipeline(sample_df["Comment"].tolist(), truncation=True)

        # Extract label and score into separate columns
        sample_df["HF_Label"] = [res["label"] for res in hf_results]
        sample_df["HF_Score"] = [round(res["score"], 3) for res in hf_results]

        # Show the table
        st.dataframe(sample_df, use_container_width=True)
        
        with col1:
            # NPS pizza graphic
            donut_chart = nps_donut_chart(df)
            st.altair_chart(donut_chart, use_container_width=True)
            st.dataframe(df["NPS Type"].value_counts().reset_index(), use_container_width=True)
        with col2:
            # Sentiment distribution graphic
            df["ML_Sentiment"] = df["ML_Sentiment"].astype(str)
            sentiment_distribution_chart = df.groupby("ML_Sentiment").size().reset_index(name="Count")
            sentiment_distribution_chart.columns = ["Sentiment", "Count"]

            bar_chart = alt.Chart(sentiment_distribution_chart).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Sentiment", type="nominal", scale=alt.Scale(domain=["Positive", "Negative", "Neutral"], range=["#2ecc71", "#e74c3c", "#f1c40f"])),
                tooltip=["Sentiment", "Count"]
            ).properties(
                title="Sentiment Distribution - Custom Trained Model"
            )

            st.altair_chart(bar_chart, use_container_width=True)
            st.dataframe(sentiment_distribution_chart, use_container_width=True)
    
if __name__ == "__main__":
    show_training3()