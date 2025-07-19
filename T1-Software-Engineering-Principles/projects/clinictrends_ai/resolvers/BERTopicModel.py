# bertopic_model.py

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import pandas as pd
import streamlit as st

def train_bertopic_model(comments: pd.Series):
    cleaned_comments = comments.dropna().astype(str)
    cleaned_comments = cleaned_comments[cleaned_comments.str.strip() != ""]
    
    if cleaned_comments.empty:
        st.warning("No valid comments to analyze.")
        st.stop()
    
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedding_model.encode(cleaned_comments.tolist(), show_progress_bar=True)

    topic_model = BERTopic(language="english")
    topics, probs = topic_model.fit_transform(cleaned_comments.tolist(), embeddings)

    return topic_model, topics, probs, embeddings