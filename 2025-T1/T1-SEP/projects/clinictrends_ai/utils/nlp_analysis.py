import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from textblob import TextBlob
from wordcloud import WordCloud
# from transformers import pipeline

def analyze_sentiment(text: str):
    if not isinstance(text, str):
        return 0.0
    blob = TextBlob(text)
    return blob.sentiment.polarity # Range from -1 (bad) to 1 (good)

def annotate_sentiments(df: pd.DataFrame, comment_col="Comment", pos_thresh=0.05, neg_thresh=-0.05):
    df = df.copy()
    df["Polarity"] = df[comment_col].fillna("").apply(analyze_sentiment)
    df["Sentiment"] = df["Polarity"].apply(
        lambda x: "Positive" if x > pos_thresh else "Negative" if x < neg_thresh else "Neutral"
    )
    return df

import plotly.express as px
NPS_COLORS = {
    "Positive": "#2ecc71",  # green (Promoters vibe)
    "Neutral":  "#f1c40f",  # yellow (Passives vibe)
    "Negative": "#e74c3c",  # red (Detractors vibe)
}

def display_sentiment_distribution(df: pd.DataFrame):
    sentiment_counts = df["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    # Ensure consistent order in legend & pie
    order = ["Positive", "Neutral", "Negative"]
    sentiment_counts["Sentiment"] = pd.Categorical(sentiment_counts["Sentiment"], categories=order, ordered=True)
    sentiment_counts = sentiment_counts.sort_values("Sentiment")

    fig = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count",
        color="Sentiment",
        color_discrete_map=NPS_COLORS,
        hole=0.4,  # keep as full pie; tweak if you want a donut
        title="Sentiment Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

def get_sentiment_distribution_figure(df: pd.DataFrame):
    sentiment_counts = df["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    order = ["Positive", "Neutral", "Negative"]
    sentiment_counts["Sentiment"] = pd.Categorical(sentiment_counts["Sentiment"], categories=order, ordered=True)
    sentiment_counts = sentiment_counts.sort_values("Sentiment")

    fig = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count",
        color="Sentiment",
        color_discrete_map=NPS_COLORS,
        title="Sentiment Distribution"
    )
    return fig

def display_wordcloud(df: pd.DataFrame, comment_col="Comment"):
    text = " ".join(df[comment_col].dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)