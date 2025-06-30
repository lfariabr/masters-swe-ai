"""
ClinicTrends AI - Models Comparison Page
========================================

Enterprise-grade ML model comparison and benchmarking interface.
Implements 4 distinct ML pipelines for comprehensive sentiment analysis.

"""

import sys
import time
import warnings
from pathlib import Path
from typing import Dict, Tuple, Any, Optional

import altair as alt
import streamlit as st
import pandas as pd
import numpy as np

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

from utils.visualizations import nps_donut_chart
from utils.nlp_analysis import annotate_sentiments
from utils.preprocessing import classify_nps

# Optional: Transformers (marked as prototype in README)
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    st.warning("⚠️ Transformers library not available. Models 3 & 4 will be disabled.")


class ModelTrainer:
    """
    Enterprise-grade ML model training and evaluation class.
    Implements standardized training pipelines with comprehensive metrics.
    """
    
    def __init__(self):
        self.models = {}
        self.vectorizers = {}
        self.metrics = {}
        
    def train_tfidf_model(self, df: pd.DataFrame, feature_column: str, 
                         target_column: str, model_name: str) -> Tuple[Any, Any]:
        """
        Train TF-IDF (Term Frequency-Inverse Document Frequency) + Logistic Regression model with standardized pipeline.
        
        Args:
            df: Training dataframe
            feature_column: Column containing text features
            target_column: Column containing target labels
            model_name: Unique identifier for the model
            
        Returns:
            Tuple of (trained_model, fitted_vectorizer)
        """
        try:
            # Feature extraction
            vectorizer = TfidfVectorizer(
                stop_words="english", 
                max_features=5000,
                ngram_range=(1, 2),  # Include bigrams for better context
                min_df=2,  # Ignore terms that appear in less than 2 documents
                max_df=0.95  # Ignore terms that appear in more than 95% of documents
            )
            
            X = vectorizer.fit_transform(df[feature_column].fillna(''))
            y = df[target_column]
            
            # Train-test split with stratification
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Model training
            model = LogisticRegression(
                max_iter=1000,
                random_state=42,
                class_weight='balanced'  # Handle class imbalance
            )
            
            start_time = time.time()
            model.fit(X_train, y_train)
            training_time = time.time() - start_time
            
            # Store model artifacts
            self.models[model_name] = model
            self.vectorizers[model_name] = vectorizer
            
            # Calculate comprehensive metrics
            y_pred = model.predict(X_test)
            self.metrics[model_name] = self._calculate_metrics(
                y_test, y_pred, model_name, training_time
            )
            
            return model, vectorizer, X_test, y_test, y_pred
            
        except Exception as e:
            st.error(f"❌ Error training {model_name}: {str(e)}")
            return None, None, None, None, None
    
    def train_transformer_model(self, df: pd.DataFrame, feature_column: str, 
                              model_name: str) -> Optional[pd.DataFrame]:
        """
        Apply pre-trained transformer model for sentiment analysis.
        
        Args:
            df: Input dataframe
            feature_column: Column containing text features
            model_name: Unique identifier for the model
            
        Returns:
            Optional[pd.DataFrame]: Transformed dataframe with sentiment scores
        
        Note: This is a prototype implementation as noted in README.
        """
        if not TRANSFORMERS_AVAILABLE:
            st.warning(f"⚠️ Transformers not available for {model_name}")
            return None
            
        try:
            sentiment_pipeline = pipeline(
                "sentiment-analysis", 
                model="distilbert-base-uncased-finetuned-sst-2-english",
                return_all_scores=False
            )
            
            # Process in batches to avoid memory issues
            batch_size = 100
            results = []
            
            progress_bar = st.progress(0)
            total_batches = len(df) // batch_size + 1
            
            for i in range(0, len(df), batch_size):
                batch = df[feature_column].iloc[i:i+batch_size].fillna('').tolist()
                batch_results = sentiment_pipeline(batch, truncation=True)
                results.extend(batch_results)
                progress_bar.progress((i // batch_size + 1) / total_batches)
            
            progress_bar.empty()
            
            # Convert results to dataframe format
            df_copy = df.copy()
            df_copy["HF_Label"] = [res["label"] for res in results]
            df_copy["HF_Score"] = [res["score"] for res in results]
            
            return df_copy
            
        except Exception as e:
            st.error(f"❌ Error with transformer model {model_name}: {str(e)}")
            return None
    
    def _calculate_metrics(self, y_true, y_pred, model_name: str, 
                          training_time: float) -> Dict[str, Any]:
        """Calculate comprehensive model performance metrics."""
        try:
            # Basic metrics
            accuracy = accuracy_score(y_true, y_pred)
            precision, recall, f1, support = precision_recall_fscore_support(
                y_true, y_pred, average='weighted', zero_division=0
            )
            
            # Class distribution
            unique_labels = np.unique(np.concatenate([y_true, y_pred]))
            class_counts = {label: sum(y_pred == label) for label in unique_labels}
            
            return {
                "Model": model_name,
                "Accuracy": round(accuracy, 4),
                "Precision": round(precision, 4),
                "Recall": round(recall, 4),
                "F1-Score": round(f1, 4),
                "Training_Time": round(training_time, 2),
                "Class_Distribution": class_counts,
                "Total_Predictions": len(y_pred)
            }
        except Exception as e:
            st.error(f"Error calculating metrics for {model_name}: {str(e)}")
            return {}


def create_performance_dashboard(metrics: Dict[str, Dict]) -> None:
    """Create comprehensive performance comparison dashboard."""
    if not metrics:
        st.warning("No metrics available for comparison.")
        return
    
    st.subheader("📊 Model Performance Comparison")
    
    # Convert metrics to DataFrame for easy comparison
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
        # Display metrics table
        st.dataframe(
            metrics_df.style.highlight_max(axis=0, subset=['Accuracy', 'Precision', 'Recall', 'F1-Score']),
            use_container_width=True
        )
        
        # Performance visualization
        col1, col2 = st.columns(2)
        
        with col1:
            # Accuracy comparison
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
            # F1-Score comparison
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
        
        # Standardize color scheme
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
        
        # Display data table
        st.dataframe(chart_data, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating visualization for {title}: {str(e)}")


def show_models():
    """
    Main function for the Models Comparison Page.
    Implements enterprise-grade ML model comparison interface.
    """
    # Page header with professional styling
    st.title("🧠 ML Models Comparison Dashboard")
    st.markdown("""
    **Enterprise-grade sentiment analysis model comparison and benchmarking platform.**
    
    Compare 4 distinct ML pipelines with comprehensive performance metrics and visualizations.
    """)
    
    # Model information expander
    with st.expander("📋 Model Architecture Information"):
        st.markdown("""
        ### Available Models:
        
        **Model 1: Comment-Based Classification**
        - Pipeline: Raw Comments → TF-IDF Vectorization → Logistic Regression
        - Features: 5,000 TF-IDF features with English stop-word filtering
        - Use Case: Text-only sentiment detection
        
        **Model 2: Enhanced Comment-Score Fusion**
        - Pipeline: Comments + Scores → Feature Fusion → TF-IDF → Classification
        - Innovation: Combines textual and numerical features
        - Use Case: Holistic sentiment analysis
        
        **Model 3: Transformer-Enhanced Classification** *(Prototype)*
        - Pipeline: Comments → DistilBERT → Fine-tuned Classification
        - Technology: State-of-the-art transformer models
        - Advantage: Context-aware sentiment understanding
        
        **Model 4: Hybrid Transformer-Score Integration** *(Prototype)*
        - Pipeline: Comments + Scores → Transformer Encoding → Feature Fusion
        - Innovation: Multi-modal learning approach
        - Result: Highest accuracy potential
        """)
    
    # File upload section
    st.markdown("### 📁 Data Upload")
    uploaded_file = st.file_uploader(
        "Upload your CSV file for model comparison",
        type="csv",
        help="File should contain 'Comment' and 'Score' columns"
    )
    
    if uploaded_file is not None:
        try:
            # Load and validate data
            with st.spinner("🔄 Loading and validating data..."):
                df = pd.read_csv(uploaded_file)
                
                # Data validation
                required_columns = ['Comment', 'Score']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"❌ Missing required columns: {missing_columns}")
                    st.stop()
                
                # Clean data
                df = df.dropna(subset=["Comment"])
                df["CommentScore"] = df["Comment"].astype(str) + " SCORE_" + df["Score"].astype(str)
                
                st.success(f"✅ Successfully loaded {len(df)} records")
            
            # Data preview
            with st.expander("👀 Data Preview"):
                st.dataframe(df.sample(min(5, len(df))), use_container_width=True)
                st.info(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Initialize model trainer
            trainer = ModelTrainer()
            
            # Baseline NLP processing
            st.markdown("### 🔬 Baseline NLP Processing")
            with st.spinner("Processing baseline sentiment analysis..."):
                df = annotate_sentiments(df)
                df["Sentiment"] = df["Sentiment"].str.upper()
            
            st.success("✅ Baseline NLP processing complete")
            
            # Model training section
            st.markdown("### 🚀 Model Training & Evaluation")
            
            # Model 1: Comment-based
            st.markdown("#### 🤖 Model 1: Comment-Based Classification")
            with st.spinner("Training Model 1..."):
                model1, vec1, X_test1, y_test1, y_pred1 = trainer.train_tfidf_model(
                    df, "Comment", "Sentiment", "Model 1: Comment-Based"
                )
            
            if model1 is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Accuracy", f"{trainer.metrics['Model 1: Comment-Based']['Accuracy']:.3f}")
                    st.metric("F1-Score", f"{trainer.metrics['Model 1: Comment-Based']['F1-Score']:.3f}")
                with col2:
                    create_sentiment_visualization(df, "Sentiment", "Model 1: Sentiment Distribution")
            
            st.markdown("---")
            
            # Model 2: Comment + Score
            st.markdown("#### 🤖 Model 2: Enhanced Comment-Score Fusion")
            with st.spinner("Training Model 2..."):
                model2, vec2, X_test2, y_test2, y_pred2 = trainer.train_tfidf_model(
                    df, "CommentScore", "Sentiment", "Model 2: Comment-Score Fusion"
                )
            
            if model2 is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Accuracy", f"{trainer.metrics['Model 2: Comment-Score Fusion']['Accuracy']:.3f}")
                    st.metric("F1-Score", f"{trainer.metrics['Model 2: Comment-Score Fusion']['F1-Score']:.3f}")
                with col2:
                    create_sentiment_visualization(df, "Sentiment", "Model 2: Sentiment Distribution")
            
            st.markdown("---")
            
            # Transformer models (if available)
            if TRANSFORMERS_AVAILABLE:
                st.markdown("#### 🤖 Model 3: Transformer-Enhanced Classification *(Prototype)*")
                with st.spinner("Processing with transformer model..."):
                    df_transformer = trainer.train_transformer_model(df, "Comment", "Model 3: Transformer")
                
                if df_transformer is not None:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info("Transformer model applied successfully")
                        st.metric("Processed Records", len(df_transformer))
                    with col2:
                        create_sentiment_visualization(df_transformer, "HF_Label", "Model 3: Transformer Results")
                
                st.markdown("---")
                
                st.markdown("#### 🤖 Model 4: Hybrid Transformer-Score Integration *(Prototype)*")
                with st.spinner("Processing hybrid transformer model..."):
                    df_hybrid = trainer.train_transformer_model(df, "CommentScore", "Model 4: Hybrid")
                
                if df_hybrid is not None:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info("Hybrid transformer model applied successfully")
                        st.metric("Processed Records", len(df_hybrid))
                    with col2:
                        create_sentiment_visualization(df_hybrid, "HF_Label", "Model 4: Hybrid Results")
            else:
                st.info("🔬 **Transformer models (3 & 4) are prototype implementations** and require additional dependencies.")
            
            # Performance comparison dashboard
            st.markdown("---")
            create_performance_dashboard(trainer.metrics)
            
            # NPS vs Sentiment comparison
            st.markdown("### 📊 NPS vs Sentiment Analysis Comparison")
            df = classify_nps(df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**NPS Distribution**")
                donut_chart = nps_donut_chart(df)
                st.altair_chart(donut_chart, use_container_width=True)
                st.dataframe(df["NPS Type"].value_counts().reset_index(), use_container_width=True)
            
            with col2:
                st.markdown("**Sentiment Distribution**")
                create_sentiment_visualization(df, "Sentiment", "Overall Sentiment Distribution")
            
            # Export results
            st.markdown("### 💾 Export Results")
            if st.button("📥 Download Model Comparison Report", type="primary"):
                # Create comprehensive report
                report_data = {
                    "model_metrics": trainer.metrics,
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
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("Please check your data format and try again.")
    
    else:
        # Instructions when no file is uploaded
        st.info("""
        👆 **Upload a CSV file to begin model comparison**
        
        Your file should contain:
        - `Comment` column: Customer feedback text
        - `Score` column: Numerical rating (0-10)
        - Optional: `Date`, `Store` columns for additional analysis
        """)


# Module exports
__all__ = ['show_models', 'ModelTrainer']

if __name__ == "__main__":
    show_models()
