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
def display_sentiment_distribution(df: pd.DataFrame):
    sentiment_counts = df["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]
    fig = px.bar(sentiment_counts, x="Sentiment", y="Count", color="Sentiment")
    st.plotly_chart(fig, use_container_width=True)

def get_sentiment_distribution_figure(df: pd.DataFrame):
    sentiment_counts = df["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]
    
    fig = px.bar(
        sentiment_counts,
        x="Sentiment",
        y="Count",
        color="Sentiment",
        title="Sentiment Distribution",
    )
    return fig

def display_wordcloud(df: pd.DataFrame, comment_col="Comment"):
    text = " ".join(df[comment_col].dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)