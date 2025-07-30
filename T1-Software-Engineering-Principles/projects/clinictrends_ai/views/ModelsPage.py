"""
ClinicTrends AI - Models Comparison Page
========================================

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

warnings.filterwarnings('ignore')
sys.path.append(str(Path(__file__).parent.parent))


from resolvers.ModelTrainer import ModelTrainer
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    st.warning("⚠️ Transformers library not available. Models 3 & 4 will be disabled.")

from utils.visualizations import nps_donut_chart, monthly_nps_trend_chart
from utils.nlp_analysis import annotate_sentiments, display_wordcloud
from utils.preprocessing import classify_nps
from utils.alerts import send_discord_message
from utils.data_upload import data_upload
from utils.visualizations import (
    create_sentiment_visualization,
    create_model_explanations,
    create_model_summary_cards, 
    create_detailed_metrics_table,
    create_performance_charts,
    crate_nps_vs_sentiment_analysis,
    model_architecture_info,
    display_nps_sentiment_agreement
)
from utils.crosstab_analysis import enhanced_crosstab_analysis

def show_models():
    """
    Main function for the Models Comparison Page.
    Implements enterprise-grade ML model comparison interface.
    """
    st.title("🧠 ML Models Dashboard")
    st.markdown("""
    **Compare 4 distinct ML pipelines** with comprehensive performance metrics and interactive visualizations.
    """)
    
    create_model_explanations()
    
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
                            
            with st.expander("👀 Data Preview (just in case you want to check it)"):
                st.dataframe(df.sample(min(5, len(df))), use_container_width=True)
                total_records = len(df)
                st.info(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
                st.success(f"Total records loaded: {total_records}")
            
            model_trainer = ModelTrainer()
            df = annotate_sentiments(df)                
            df["Sentiment"] = df["Sentiment"].str.upper()
            
            st.markdown("---")
            st.markdown("###### Model Navigation Tabs: pick your color: 🔴🟡🟢🔵")
            model_architecture_info()
            df = classify_nps(df)
            
            
            tab1, tab2, tab3, tab4 = st.tabs(["🔴 Comment-Based", "🟡 Comment-Score Fusion", "🟢 Transformer-Enhanced", "🔵 Hybrid Transformer-Score Integration"])

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
                    
                    with st.expander("Model 1 Predictions Sample"):
                        st.dataframe(
                            df[["Comment", "Score", "NPS Type", "Sentiment", "Model_1_Prediction"]].sample(min(100, len(df))),
                            use_container_width=True
                        )
            
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
                    
                    with st.expander("Model 2 Predictions Sample"):
                        st.dataframe(
                            df[["CommentScore", "Score", "NPS Type", "Sentiment", "Model_2_Prediction"]].sample(min(100, len(df))),
                            use_container_width=True
                        )

            if TRANSFORMERS_AVAILABLE:
                with tab3:
                    st.markdown("#### 🤖 Model 3: Transformer-Enhanced Classification *(Prototype)*")
                    with st.spinner("Processing with transformer model..."):
                        df_transformer = model_trainer.train_transformer_model(df, "Comment", "Model 3: Transformer")
                    
                    if df_transformer is not None:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info("Transformer model applied successfully")
                            st.metric("Processed Records", len(df_transformer))
                        with col2:
                            create_sentiment_visualization(df_transformer, "HF_Label", "Model 3: Transformer Results")
                        
                        with st.expander("Model 3 Predictions Sample"):
                            # DEBUG cross checking prediction vs original NPS Type
                            st.dataframe(
                                df_transformer[
                                    ["Comment", "Score", "NPS Type", "Sentiment", "HF_Label", "HF_Score"]
                                ].sample(min(10, len(df_transformer))),
                            use_container_width=True
                        )
                
                with tab4:
                    st.markdown("#### 🤖 Model 4: Hybrid Transformer-Score Integration *(Prototype)*")
                    with st.spinner("Processing hybrid transformer model..."):
                        df_hybrid = model_trainer.train_transformer_model(df, "CommentScore", "Model 4: Hybrid")
                    
                    if df_hybrid is not None:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info("Hybrid transformer model applied successfully")
                            st.metric("Processed Records", len(df_hybrid))
                        with col2:
                            create_sentiment_visualization(df_hybrid, "HF_Label", "Model 4: Hybrid Results")
                        
                        with st.expander("Model 4 Predictions Sample"):
                            # DEBUG cross checking prediction vs original NPS Type
                            st.dataframe(
                                df_hybrid[
                                    ["CommentScore", "NPS Type", "Sentiment", "HF_Label", "HF_Score"]
                                ].sample(min(10, len(df_hybrid))),
                            use_container_width=True
                        )
            else:
                st.info("🔬 Transformer models (3 & 4) are prototype implementations and require additional dependencies.")
            st.markdown("---")
            
            # Model Performance Overview
            create_model_summary_cards(model_trainer.metrics)
            st.markdown("---")
            
            # Detailed Performance Metrics
            create_detailed_metrics_table(model_trainer.metrics)
            st.markdown("---")
            
            # Performance Visualizations
            create_performance_charts(model_trainer.metrics)
            st.markdown("---")
            
            # NPS vs Sentiment Analysis Comparison
            crate_nps_vs_sentiment_analysis(df)
            st.markdown("---")
            
            # Enhanced Cross-Tabulation Analysis
            enhanced_crosstab_analysis(df)
            
            # NPS vs Sentiment Agreement Analysis
            display_nps_sentiment_agreement(df)
            st.markdown("---")

            st.markdown("### 💾 Export Results")
            if st.button("📥 Download Model Comparison Report", type="primary", key="export"):
                report_data = {
                    "model_metrics": model_trainer.metrics,
                    "data_summary": {
                        "total_records": len(df),
                        "columns": list(df.columns),
                        "nps_distribution": df["NPS Type"].value_counts().to_dict(),
                        "sentiment_distribution": df["Sentiment"].value_counts().to_dict()
                    }
                }
                
                st.download_button(
                    label="Download JSON Report",
                    data=pd.Series(report_data).to_json(),
                    file_name=f"model_comparison_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            with st.expander("🔎 Full DataFrame with All Predictions"):
                st.dataframe(df, use_container_width=True)
            
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
__all__ = ['show_models']

if __name__ == "__main__":
    show_models()