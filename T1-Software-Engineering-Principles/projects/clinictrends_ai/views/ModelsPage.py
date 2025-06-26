import sys
import altair as alt
from pathlib import Path
import streamlit as st
import pandas as pd

from utils.visualizations import nps_donut_chart
from utils.nlp_analysis import annotate_sentiments
from utils.preprocessing import classify_nps

import sklearn
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from transformers import pipeline

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))

def train_model(df):
    """Train a model."""
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    X = vectorizer.fit_transform(df["CommentScore"])
    y = df["Sentiment"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    return model, vectorizer

def show_sentiment_donut(df, sentiment_column, title):
    """Plot donut chart for a given sentiment column."""
    chart_data = df[sentiment_column].value_counts().reset_index()
    chart_data.columns = ["Sentiment", "Count"]

    chart = alt.Chart(chart_data).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Sentiment", type="nominal",
                        scale=alt.Scale(domain=["POSITIVE", "NEGATIVE", "NEUTRAL"],
                                       range=["#2ecc71", "#e74c3c", "#f1c40f"])),
        tooltip=["Sentiment", "Count"]
    ).properties(title=title)

    st.altair_chart(chart, use_container_width=True)

def show_models():
    """Show the models page content."""
    st.title("Models Page ")
    st.write("In this page you can compare the models available. Have fun!")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)  # use your actual file path
        df = df.dropna(subset=["Comment"])
        df["CommentScore"] = df["Comment"].astype(str) + " SCORE_" + df["Score"].astype(str)

        st.write('Data preview')
        st.write(df.sample(5))

        # NLP
        ############################
        df = annotate_sentiments(df)
        df["Sentiment"] = df["Sentiment"].str.upper()
        st.write("---")
        ############################

        # ML - Custom Model 1 - TfidfVectorizer @ Comment column + LogisticRegression 
        ############################
        model, vectorizer = train_model(df)
        X = vectorizer.transform(df["Comment"])
        y = df["Sentiment"]

        X_train, X_test, y_train, y_test_custom1 = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        st.markdown("#### Custom Model 1 - TfidfVectorizer @ Comment column + LogisticRegression")
        st.markdown("#### Model accuracy")
        st.write(model.score(X_test, y_test_custom1))

        y_pred_custom1 = model.predict(X_test)
        st.markdown("#### Classification report")
        st.write(classification_report(y_test_custom1, y_pred_custom1))

        show_sentiment_donut(df, "Sentiment", "Sentiment Distribution - Custom Model 1")

        st.write("---")
        ############################

        # ML - Custom Model 2 - TfidfVectorizer @ Comment + Score column + LogisticRegression
        ############################
        model, vectorizer = train_model(df)
        X = vectorizer.transform(df["CommentScore"])
        y = df["Sentiment"]

        X_train, X_test, y_train, y_test_custom2 = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        st.markdown("#### Custom Model 2 - TfidfVectorizer @ Comment + Score column + LogisticRegression")
        st.markdown("#### Model accuracy")
        st.write(model.score(X_test, y_test_custom2))

        y_pred_custom2 = model.predict(X_test)
        st.markdown("#### Classification report")
        st.write(classification_report(y_test_custom2, y_pred_custom2))

        show_sentiment_donut(df, "Sentiment", "Sentiment Distribution - Custom Model 2")

        st.write("---")
        ############################

        # ML - Custom Model 3 - TfidfVectorizer @ Comment + Score column + Hugging Face Transformers
        ############################
        model, vectorizer = train_model(df)
        X = vectorizer.transform(df["Comment"])

        sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        hf_results = sentiment_pipeline(df["Comment"].tolist(), truncation=True)
        df["HF_Label"] = [res["label"].upper() for res in hf_results]
        y = df["HF_Label"]

        X_train, X_test, y_train, y_test_custom3 = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        df["ML_Sentiment"] = model.predict(vectorizer.transform(df["Comment"]))

        st.markdown("#### Custom Model 3 - TfidfVectorizer @ Comment + Hugging Face Transformers")
        st.markdown("#### Model accuracy")
        st.write(model.score(X_test, y_test_custom3))

        y_pred_custom3 = model.predict(X_test)
        st.markdown("#### Classification report")
        st.write(classification_report(y_test_custom3, y_pred_custom3))

        show_sentiment_donut(df, "HF_Label", "Sentiment Distribution - Custom Model 3")

        st.write("---")
        ############################

        # ML - Custom Model 4 - TfidfVectorizer @ Comment + Score column + Hugging Face Transformers
        ############################
        model, vectorizer = train_model(df)
        X = vectorizer.transform(df["CommentScore"])

        sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        hf_results = sentiment_pipeline(df["CommentScore"].tolist(), truncation=True)
        df["HF_Label"] = [res["label"] for res in hf_results]
        y = df["HF_Label"]

        X_train, X_test, y_train, y_test_custom4 = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)

        df["ML_Sentiment"] = model.predict(vectorizer.transform(df["CommentScore"]))

        st.markdown("#### Custom Model 4 - TfidfVectorizer @ Comment + Score column + Hugging Face Transformers")
        st.markdown("#### Model accuracy")
        st.write(model.score(X_test, y_test_custom4))

        y_pred_custom4 = model.predict(X_test)
        st.markdown("#### Classification report")
        st.write(classification_report(y_test_custom4, y_pred_custom4))

        show_sentiment_donut(df, "HF_Label", "Sentiment Distribution - Custom Model 4")

        st.write("---")

# === Final Metrics Table ===
    st.subheader("📊 Final Model Comparison Table")
    from sklearn.metrics import precision_recall_fscore_support, accuracy_score

    def collect_metrics(y_true, y_pred, model_name):
        labels = ["POSITIVE", "NEGATIVE", "NEUTRAL"]
        metrics = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
        accuracy = accuracy_score(y_true, y_pred)
        return {
            "Model": model_name,
            "POSITIVE": sum(pd.Series(y_pred) == "POSITIVE"),
            "NEGATIVE": sum(pd.Series(y_pred) == "NEGATIVE"),
            "NEUTRAL": sum(pd.Series(y_pred) == "NEUTRAL"),
            "Accuracy": accuracy,
            "Precision": metrics[0].mean(),
            "Recall": metrics[1].mean(),
            "F1-Score": metrics[2].mean()
        }
    
    def nps_to_sentiment(nps_type):
        if nps_type == "Promoter":
            return "POSITIVE"
        elif nps_type == "Passive":
            return "NEUTRAL"
        elif nps_type == "Detractor":
            return "NEGATIVE"
        else:
            return "UNKNOWN"

    df = classify_nps(df)
    df["NPS_Sentiment"] = df["NPS Type"].apply(nps_to_sentiment)

    results = []
    results.append(collect_metrics(df["NPS_Sentiment"], df["Sentiment"], "NPS Original"))

    results.append(collect_metrics(df["Sentiment"], df["Sentiment"], "NLP (Annotated)"))
    results.append(collect_metrics(y_test_custom1, y_pred_custom1, "Custom Model 1"))
    results.append(collect_metrics(y_test_custom2, y_pred_custom2, "Custom Model 2"))
    results.append(collect_metrics(y_test_custom3, y_pred_custom3, "Custom Model 3"))
    results.append(collect_metrics(y_test_custom4, y_pred_custom4, "Custom Model 4"))

    df_results = pd.DataFrame(results)
    st.dataframe(df_results)

if __name__ == "__main__":
    show_models()
