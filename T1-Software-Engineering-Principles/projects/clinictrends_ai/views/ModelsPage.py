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

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))

from utils.visualizations import nps_donut_chart, monthly_nps_trend_chart
from utils.nlp_analysis import annotate_sentiments, display_wordcloud
from utils.preprocessing import classify_nps
from utils.alerts import send_discord_message

# Optional: Transformers (marked as prototype in README)
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    st.warning("⚠️ Transformers library not available. Models 3 & 4 will be disabled.")

# Import ModelTrainer from resolvers
from resolvers.ModelTrainer import ModelTrainer


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


def show_models():
    """
    Main function for the Models Comparison Page.
    Implements enterprise-grade ML model comparison interface.
    """
    st.title("🧠 ML Models Comparison Dashboard")
    st.markdown("""
    Compare 4 distinct ML pipelines with comprehensive performance metrics and visualizations.
    """)
    
    st.markdown("### 📁 Data Upload")
    csv_url = "https://raw.githubusercontent.com/lfariabr/masters-swe-ai/master/T1-Software-Engineering-Principles/projects/clinictrends_ai/public/clinicTrendsAiSample.csv"
    response = requests.get(csv_url)

    if response.status_code == 200:
        st.download_button(
            label="⬇️ Download Sample CSV Data",
            data=response.content,
            file_name="clinicTrendsAiSample.csv",
            mime="text/csv"
        )
    else:
        st.error("Sample CSV file not found!")
        
    uploaded_file = st.file_uploader(
        "Upload your CSV file with customer feedback or use the sample data",
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
                
                st.success(f"✅ Successfully loaded {len(df)} records")
            
            with st.expander("👀 Data Preview (just in case you want to check it)"):
                st.dataframe(df.sample(min(5, len(df))), use_container_width=True)
                st.info(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
            
            model_trainer = ModelTrainer()
            df = annotate_sentiments(df)                
            df["Sentiment"] = df["Sentiment"].str.upper()
            
            st.markdown("---")
            st.markdown("### 🚀 Model Training & Evaluation")
            st.write("Quick information about models")
            
            with st.expander("📋 Model Architecture Information"):
                st.markdown("""
                ### Available Models:
                
                **Model 1: Comment-Based Classification**
                - Pipeline: Raw Comments → TF-IDF Vectorization → Logistic Regression
                - Features: 5,000 TF-IDF features
                
                **Model 2: Enhanced Comment-Score Fusion**
                - Pipeline: Comments + Scores → TF-IDF → Classification
                - Innovation: Combines textual and numerical features
                
                **Model 3: Transformer-Enhanced Classification** *(Prototype)*
                - Pipeline: Comments → DistilBERT → Fine-tuned Classification
                
                **Model 4: Hybrid Transformer-Score Integration** *(Prototype)*
                - Pipeline: Comments + Scores → Transformer Encoding → Feature Fusion
                """)
            
            st.markdown("---")
            df = classify_nps(df)

            st.markdown("#### 🤖 Model 1: Comment-Based Classification")
            with st.spinner("Training Model 1..."):
                model1, vec1, X_test1, y_test1, y_pred1 = model_trainer.train_tfidf_model(
                    df, "Comment", "Sentiment", "Model 1: Comment-Based"
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
                    df[["Comment", "Score", "NPS Type", "Sentiment", "Model_1_Prediction"]].sample(min(10, len(df))),
                    use_container_width=True
                )
            
            st.markdown("---")
            
            st.markdown("#### 🤖 Model 2: Enhanced Comment-Score Fusion")
            with st.spinner("Training Model 2..."):
                model2, vec2, X_test2, y_test2, y_pred2 = model_trainer.train_tfidf_model(
                    df, "CommentScore", "Sentiment", "Model 2: Comment-Score Fusion"
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
                    df[["CommentScore", "NPS Type", "Sentiment", "Model_2_Prediction"]].sample(min(10, len(df))),
                    use_container_width=True
                )
            
            st.markdown("---")
            
            st.info("Transformer models are a work in progress. Stay tuned!")
            st.markdown("---")
            
            # if TRANSFORMERS_AVAILABLE:
            #     st.markdown("#### 🤖 Model 3: Transformer-Enhanced Classification *(Prototype)*")
            #     with st.spinner("Processing with transformer model..."):
            #         df_transformer = model_trainer.train_transformer_model(df, "Comment", "Model 3: Transformer")
                
            #     if df_transformer is not None:
            #         col1, col2 = st.columns(2)
            #         with col1:
            #             st.info("Transformer model applied successfully")
            #             st.metric("Processed Records", len(df_transformer))
            #         with col2:
            #             create_sentiment_visualization(df_transformer, "HF_Label", "Model 3: Transformer Results")
            #         # DEBUG cross checking prediction vs original NPS Type
            #         st.warning("#### 📝 Model 3 Predictions Sample")
            #         st.dataframe(
            #             df_transformer[
            #                 ["Comment", "Score", "NPS Type", "Sentiment", "HF_Label", "HF_Score"]
            #             ].sample(min(10, len(df_transformer))),
            #             use_container_width=True
            #         )
                
            #     st.markdown("---")
                
            #     st.markdown("#### 🤖 Model 4: Hybrid Transformer-Score Integration *(Prototype)*")
            #     with st.spinner("Processing hybrid transformer model..."):
            #         df_hybrid = model_trainer.train_transformer_model(df, "CommentScore", "Model 4: Hybrid")
                
            #     if df_hybrid is not None:
            #         col1, col2 = st.columns(2)
            #         with col1:
            #             st.info("Hybrid transformer model applied successfully")
            #             st.metric("Processed Records", len(df_hybrid))
            #         with col2:
            #             create_sentiment_visualization(df_hybrid, "HF_Label", "Model 4: Hybrid Results")
            #         # DEBUG cross checking prediction vs original NPS Type
            #         st.warning("#### 📝 Model 4 Predictions Sample")
            #         st.dataframe(
            #             df_hybrid[
            #                 ["CommentScore", "NPS Type", "Sentiment", "HF_Label", "HF_Score"]
            #             ].sample(min(10, len(df_hybrid))),
            #             use_container_width=True
            #         )
            # else:
            #     st.info("🔬 Transformer models (3 & 4) are prototype implementations and require additional dependencies.")
            
            # st.markdown("---")
            
            # create_performance_dashboard(model_trainer.metrics)
            
            # st.markdown("### 📊 NPS vs Sentiment Analysis Comparison")
            # df = classify_nps(df)
            
            # col1, col2 = st.columns(2)
            # with col1:
            #     st.markdown("**NPS Distribution**")
            #     donut_chart = nps_donut_chart(df)
            #     st.altair_chart(donut_chart, use_container_width=True)
            #     st.dataframe(df["NPS Type"].value_counts().reset_index(), use_container_width=True)
            
            # with col2:
            #     st.markdown("**Sentiment Distribution**")
            #     create_sentiment_visualization(df, "Sentiment", "Overall Sentiment Distribution")
            
            # st.markdown("---")
            # st.markdown("### 📊 Crosstab Analysis")
            
            # crosstab = pd.crosstab(df["NPS Type"], df["Sentiment"])
            # st.dataframe(crosstab, use_container_width=True)

            # ct_melted = crosstab.reset_index().melt(id_vars="NPS Type", var_name="Sentiment", value_name="Count")

            # heatmap = alt.Chart(ct_melted).mark_rect().encode(
            #     x=alt.X('Sentiment:N'),
            #     y=alt.Y('NPS Type:N'),
            #     color=alt.Color('Count:Q', scale=alt.Scale(scheme='blues')),
            #     tooltip=['NPS Type', 'Sentiment', 'Count']
            # ).properties(
            #     title="Heatmap - NPS Type vs Sentiment"
            # )

            # st.altair_chart(heatmap, use_container_width=True)

            # nps_sentiment_map = {
            #     "Promoter": "POSITIVE",
            #     "Passive": "NEUTRAL",
            #     "Detractor": "NEGATIVE"
            # }

            # df["NPS_Sentiment"] = df["NPS Type"].map(nps_sentiment_map)

            # agreement_rate = np.mean(df["NPS_Sentiment"] == df["Sentiment"])
            # st.write(f"✅ The agreement between NPS and sentiment is: {agreement_rate:.2%}")
            
            # st.markdown("---")

            # st.markdown("### 💾 Export Results")
            # if st.button("📥 Download Model Comparison Report", type="primary", key="export"):
            #     report_data = {
            #         "model_metrics": model_trainer.metrics,
            #         "data_summary": {
            #             "total_records": len(df),
            #             "columns": list(df.columns),
            #             "nps_distribution": df["NPS Type"].value_counts().to_dict(),
            #             "sentiment_distribution": df["Sentiment"].value_counts().to_dict()
            #         }
            #     }
                
            #     st.download_button(
            #         label="Download JSON Report",
            #         data=pd.Series(report_data).to_json(),
            #         file_name=f"model_comparison_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
            #         mime="application/json"
            #     )
            
            # with st.expander("🔎 Full DataFrame with All Predictions"):
            #     st.dataframe(df, use_container_width=True)
            
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
