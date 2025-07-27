"""
ClinicTrends AI - Enhanced Models Page
======================================

Enterprise-grade ML model comparison and benchmarking interface.
Implements 4 distinct ML pipelines for comprehensive sentiment analysis.

"""

import sys
import warnings
from pathlib import Path
from typing import Dict

import altair as alt
import streamlit as st
import pandas as pd
import numpy as np
import requests

# ML/AI Libraries
import sklearn
from sklearn.metrics import (
    classification_report, 
    accuracy_score, 
    precision_recall_fscore_support,
    confusion_matrix
)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))

from utils.visualizations import nps_donut_chart, monthly_nps_trend_chart
from utils.nlp_analysis import annotate_sentiments, display_wordcloud
from utils.preprocessing import classify_nps
from utils.alerts import send_discord_message
from utils.data_upload import data_upload

# Optional: Transformers (marked as prototype in README)
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    st.warning("⚠️ Transformers library not available. Models 3 & 4 will be disabled.")

# Import ModelTrainer from resolvers
from resolvers.EnhancedTrainer import EnhancedTrainer


def create_performance_dashboard(metrics: Dict[str, Dict]) -> None:
    """Create comprehensive performance comparison dashboard."""
    if not metrics:
        st.warning("No metrics available for comparison.")
        return
    
    st.subheader("📊 Model Performance Comparison")
    
    metrics_df = pd.DataFrame([
        {
            "Model": data["Model"],
            "Accuracy": data["Accuracy"],
            "Precision": data["Precision"],
            "Recall": data["Recall"],
            "F1-Score": data["F1-Score"],
            "Training Time (s)": data["Training_Time"],
            "Total Predictions": data["Total_Predictions"]
        }
        for data in metrics.values() if data
    ])
    
    if not metrics_df.empty:
        st.dataframe(
            metrics_df.style.highlight_max(axis=0, subset=['Accuracy', 'Precision', 'Recall', 'F1-Score']),
            use_container_width=True
        )
        
        # Performance visualization
        col1, col2 = st.columns(2)
        
        with col1:
            accuracy_chart = alt.Chart(metrics_df).mark_bar().encode(
                x=alt.X('Model:N', sort='-y'),
                y=alt.Y('Accuracy:Q', scale=alt.Scale(domain=[0, 1])),
                color=alt.Color('Model:N', legend=None),
                tooltip=['Model', 'Accuracy']
            ).properties(
                title="Model Accuracy Comparison",
                width=300,
                height=200
            )
            st.altair_chart(accuracy_chart, use_container_width=True)
        
        with col2:
            f1_chart = alt.Chart(metrics_df).mark_bar().encode(
                x=alt.X('Model:N', sort='-y'),
                y=alt.Y('F1-Score:Q', scale=alt.Scale(domain=[0, 1])),
                color=alt.Color('Model:N', legend=None),
                tooltip=['Model', 'F1-Score']
            ).properties(
                title="Model F1-Score Comparison",
                width=300,
                height=200
            )
            st.altair_chart(f1_chart, use_container_width=True)


def create_sentiment_visualization(df: pd.DataFrame, sentiment_column: str, 
                                   title: str) -> None:
    """Create standardized sentiment distribution visualization."""
    try:
        chart_data = df[sentiment_column].value_counts().reset_index()
        chart_data.columns = ["Sentiment", "Count"]
        
        color_scale = alt.Scale(
            domain=["POSITIVE", "NEGATIVE", "NEUTRAL", "Positive", "Negative", "Neutral"],
            range=["#2ecc71", "#e74c3c", "#f1c40f", "#2ecc71", "#e74c3c", "#f1c40f"]
        )
        
        chart = alt.Chart(chart_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Sentiment", type="nominal", scale=color_scale),
            tooltip=["Sentiment", "Count"]
        ).properties(
            title=title,
            width=300,
            height=300
        )
        
        st.altair_chart(chart, use_container_width=True)
        st.dataframe(chart_data, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating visualization for {title}: {str(e)}")


def show_enhanced_models():
    """
    Main function for the Models Comparison Page.
    Implements enterprise-grade ML model comparison interface.
    """
    st.title("ML Experiments 🧪")
    st.markdown("""
    Experiments with Training.
    """)
    col1, col2 = st.columns(2)
    
    with col1:
        data_upload()
    
    with col2:
        uploaded_file = st.file_uploader(
       "Upload your CSV file or use the sample data",
        type="csv",
        help="File should contain 'Comment' and 'Score' columns"
    )
    
    if uploaded_file is not None:
        try:
            with st.spinner("🔄 Loading and validating data..."):
                send_discord_message("🔄 Starting data upload and validation process at Models Page")
                df = pd.read_csv(uploaded_file)
                
                required_columns = ['Comment', 'Score']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"❌ Missing required columns: {missing_columns}")
                    st.stop()
                
                df = df.dropna(subset=["Comment"])
                df["CommentScore"] = df["Comment"].astype(str) + " SCORE_" + df["Score"].astype(str)
                df = classify_nps(df)
                            
            with st.expander("👀 Data Preview (just in case you want to check it)"):
                st.dataframe(df.sample(min(5, len(df))), use_container_width=True)
                total_records = len(df)
                st.info(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
                st.success(f"Total records loaded: {total_records}")

            
            model_trainer = EnhancedTrainer()
            df = annotate_sentiments(df)                
            df["Sentiment"] = df["Sentiment"].str.upper()
            
            st.markdown("---")
            st.markdown("### Model Training & Evaluation")
    
            st.write("Delete later, just debugging")
            st.dataframe(df.sample(min(5, len(df))), use_container_width=True)

            st.markdown("###### Model Training Tabs: pick your color: 🔵🟢")
            with st.expander("📋 Quick Information about Models"):
                st.markdown("""
                ### Available Models:
                
                **Model 1: Comment-Based Classification**
                - Pipeline: Raw Comments → TF-IDF Vectorization → Logistic Regression
                - Features: 5,000 TF-IDF features
                
                **Model 2: Enhanced Comment-Score Fusion**
                - Pipeline: Comments + Scores → TF-IDF → Classification
                - Innovation: Combines textual and numerical features
                """)
            tab1, tab2 = st.tabs(["🔵 Model 1", "🟢 Model 2"])
            
            with tab1:
                st.markdown("#### 🤖 Model 1: Comment-Based Classification")
                with st.spinner("Training Model 1..."):
                    model1, vec1, X_test1, y_test1, y_pred1 = model_trainer.train_tfidf_model(
                        df, "Comment", "NPS Type", "Model 1: Comment-Based"
                    )
                st.success("✅ Model 1 training complete")
            
                if model1 is not None:
                    df["Model_1_Prediction"] = model1.predict(vec1.transform(df["Comment"]))
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Accuracy", f"{model_trainer.metrics['Model 1: Comment-Based']['Accuracy']:.3f}")
                        st.metric("F1-Score", f"{model_trainer.metrics['Model 1: Comment-Based']['F1-Score']:.3f}")
                    with col2:
                        create_sentiment_visualization(df, "Sentiment", "Model 1: Sentiment Distribution")
                    # DEBUG cross checking prediction vs original NPS Type
                    st.warning("#### 📝 Model 1 Predictions Sample")
                    st.dataframe(
                        df[["Comment", "Score", "NPS Type", "Sentiment", "Model_1_Prediction"]].sample(min(100, len(df))),
                        use_container_width=True
                    )
                
                st.markdown("---")
            
            with tab2:
                st.markdown("#### 🤖 Model 2: Enhanced Comment-Score Fusion")
                with st.spinner("Training Model 2..."):
                    model2, vec2, X_test2, y_test2, y_pred2 = model_trainer.train_tfidf_model(
                        df, "CommentScore", "NPS Type", "Model 2: Comment-Score Fusion"
                    )
                st.success("✅ Model 2 training complete")
            
                if model2 is not None:
                    df["Model_2_Prediction"] = model2.predict(vec2.transform(df["CommentScore"]))
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Accuracy", f"{model_trainer.metrics['Model 2: Comment-Score Fusion']['Accuracy']:.3f}")
                        st.metric("F1-Score", f"{model_trainer.metrics['Model 2: Comment-Score Fusion']['F1-Score']:.3f}")
                with col2:
                    create_sentiment_visualization(df, "Sentiment", "Model 2: Sentiment Distribution")
                # DEBUG cross checking prediction vs original NPS Type
                st.warning("#### 📝 Model 2 Predictions Sample")
                st.dataframe(
                    df[["CommentScore", "Score", "NPS Type", "Sentiment", "Model_2_Prediction"]].sample(min(100, len(df))),
                    use_container_width=True
                )
            
            st.markdown("---")
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please check your data format and try again.")
    
    else:
        st.info("""
        👆 **Upload a CSV file to begin model comparison**
        
        Your file should contain:
        - `Comment` column: Customer feedback text
        - `Score` column: Numerical rating (0-10)
        - Optional: `Date`, `Store` columns for additional analysis
        """)


# Module exports
__all__ = ['show_enhanced_models']

if __name__ == "__main__":
    show_enhanced_models()
