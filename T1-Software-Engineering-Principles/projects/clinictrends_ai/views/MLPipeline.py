"""
ClinicTrends AI - Complete ML Pipeline
=====================================

Enhanced ML pipeline integrating 4 sentiment models + BERTopic topic modeling.
Pipeline: Data → Preprocessing → Multi-Model Sentiment Analysis → Topic Modeling → Business Actions

Author: Luis Faria
Version: v2.8.5 - Complete BERTopic Integration with ML Models
"""

import sys
import warnings
from pathlib import Path
from typing import Dict, Optional

import streamlit as st
import pandas as pd
import numpy as np

# ML/AI Libraries
from sklearn.metrics import accuracy_score, classification_report

warnings.filterwarnings('ignore')
sys.path.append(str(Path(__file__).parent.parent))

# Core imports
from resolvers.ModelTrainer import ModelTrainer
from resolvers.BERTopicModel import train_bertopic_model
from utils.nlp_analysis import annotate_sentiments
from utils.preprocessing import classify_nps, calculate_nps
from utils.data_upload import data_upload
from utils.alerts import send_discord_message
from utils.visualizations import (
    create_model_explanations,
    create_sentiment_visualization,
    create_performance_charts,
    display_nps_sentiment_agreement,
    create_model_summary_cards,
    create_detailed_metrics_table
)
from utils.crosstab_analysis import enhanced_crosstab_analysis

# Check for transformers availability
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class EnhancedMLPipeline:
    """
    Enhanced ML Pipeline for ClinicTrends AI
    Integrates 4 sentiment analysis models with topic modeling for comprehensive insights.
    """
    
    def __init__(self):
        self.model_trainer = ModelTrainer()
        self.df = None
        self.topics_model = None
        self.topics_df = None
        self.models_trained = False
    
    def load_and_validate_data(self, uploaded_file) -> bool:
        """Load and validate uploaded CSV data."""
        try:
            with st.spinner("🔄 Loading and validating data..."):
                send_discord_message("🔄 Starting enhanced ML pipeline data validation")
                
            self.df = pd.read_csv(uploaded_file)
            
            # Validate required columns
            required_columns = ['Comment', 'Score']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            
            if missing_columns:
                st.error(f"❌ Missing required columns: {missing_columns}")
                return False
            
            # Clean data
            self.df = self.df.dropna(subset=["Comment"])
            self.df["CommentScore"] = self.df["Comment"].astype(str) + " SCORE_" + self.df["Score"].astype(str)
            
            # Display data preview
            with st.expander("👀 Data Preview"):
                st.dataframe(self.df.sample(min(5, len(self.df))), use_container_width=True)
                st.info(f"Dataset shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns")
                st.success(f"Total records loaded: {len(self.df)}")
            
            return True
            
        except Exception as e:
            st.error(f"❌ Data loading error: {str(e)}")
            return False
    
    def run_sentiment_analysis(self):
        """Execute comprehensive sentiment analysis using all 4 models."""
        
        with st.spinner("🔄 Preprocessing and annotating sentiments..."):
            # Basic sentiment annotation and NPS classification
            self.df = annotate_sentiments(self.df)
            self.df["Sentiment"] = self.df["Sentiment"].str.upper()
            self.df = classify_nps(self.df)
        
        # Train all 4 ML models
        if st.button("🚀 Train All ML Models", type="primary"):
            self.train_all_models()
    
    def train_all_models(self):
        """Train all 4 ML models and display results."""
        
        self.train_model_1()        
        self.train_model_2()
        
        if TRANSFORMERS_AVAILABLE:
            self.train_model_3()    
            self.train_model_4()
        else:
            st.warning("⚠️ Transformers library not available. Models 3 & 4 require additional dependencies.")
        
        self.models_trained = True
        
        # Show model performance summary
        st.success("✅ All models trained successfully")
        create_detailed_metrics_table(self.model_trainer.metrics)
        create_model_summary_cards(self.model_trainer.metrics)
    
    def train_model_1(self):
        """Train Model 1: Comment-Based Classification."""
        
        with st.spinner("Training Model 1..."):
            model1, vec1, X_test1, y_test1, y_pred1 = self.model_trainer.train_tfidf_model(
                self.df, "Comment", "NPS Type", "Model 1: Comment-Based"
            )
        
        if model1 is not None:
            self.df["Model_1_Prediction"] = model1.predict(vec1.transform(self.df["Comment"]))
            
    def train_model_2(self):
        """Train Model 2: Comment-Score Fusion."""
        
        with st.spinner("Training Model 2..."):
            model2, vec2, X_test2, y_test2, y_pred2 = self.model_trainer.train_tfidf_model(
                self.df, "CommentScore", "NPS Type", "Model 2: Comment-Score Fusion"
            )
        
        if model2 is not None:
            self.df["Model_2_Prediction"] = model2.predict(vec2.transform(self.df["CommentScore"]))
            
    def train_model_3(self):
        """Train Model 3: Transformer-Enhanced."""
        
        with st.spinner("Processing with transformer model..."):
            df_transformer = self.model_trainer.train_transformer_model(
                self.df, "Comment", "Model 3: Transformer"
            )
        
    def train_model_4(self):
        """Train Model 4: Hybrid Transformer-Score."""
        
        with st.spinner("Processing hybrid transformer model..."):
            df_hybrid = self.model_trainer.train_transformer_model(
                self.df, "CommentScore", "Model 4: Hybrid"
            )
    
    def run_topic_modeling(self):
        """Execute BERTopic topic modeling pipeline."""
        st.markdown("#### 🔍 Topic Discovery & Analysis")
        
        if not self.models_trained:
            st.info("💡 **Tip**: Train ML models first to get the most comprehensive analysis!")
        
        if st.button("🤖 Discover Topics with BERTopic", type="primary"):
            with st.spinner("🔍 Training BERTopic model..."):
                try:
                    # Filter valid comments
                    valid_mask = self.df["Comment"].notna() & self.df["Comment"].str.strip().ne("")
                    valid_comments = self.df.loc[valid_mask, "Comment"]
                    
                    if len(valid_comments) < 10:
                        st.warning("⚠️ Need at least 10 valid comments for topic modeling")
                        return
                    
                    # Train BERTopic model
                    self.topics_model, topics, probs, embeddings = train_bertopic_model(valid_comments)
                    
                    # Assign topics to dataframe
                    self.df.loc[valid_mask, "Topic"] = topics
                    self.topics_df = self.topics_model.get_topic_info()
                    
                    # Clean topic names
                    self.topics_df["Name"] = self.topics_df.apply(
                        lambda row: "Outliers" if row["Topic"] == -1 else row["Name"], axis=1
                    )
                    
                    # Merge topic names with main dataframe
                    self.df = self.df.merge(
                        self.topics_df[["Topic", "Name"]], 
                        on="Topic", 
                        how="left"
                    )
                    
                    st.success("✅ Topic modeling completed!")
                    self.display_topic_results()
                    self.generate_business_insights()
                    
                except Exception as e:
                    st.error(f"❌ Topic modeling error: {str(e)}")
    
    def display_topic_results(self):
        """Display topic modeling results and visualizations."""
        if self.topics_model is None or self.topics_df is None:
            return
        
        st.markdown("---")
        st.markdown("### 📊 Topic Analysis Results")
        
        # Topic overview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Top Topics Discovered:**")
            display_topics = self.topics_df.head(10)[["Topic", "Name", "Count"]]
            st.dataframe(display_topics, use_container_width=True)
        
        with col2:
            total_topics = len(self.topics_df[self.topics_df["Topic"] != -1])
            outliers = len(self.df[self.df["Topic"] == -1]) if "Topic" in self.df.columns else 0
            
            st.metric("Topics Found", total_topics)
            st.metric("Outliers", outliers)
            if len(self.df) > 0:
                st.metric("Coverage", f"{((len(self.df) - outliers) / len(self.df) * 100):.1f}%")
        
        # Topic visualizations
        try:
            st.markdown("#### 📈 Topic Visualizations")
            
            # Bar chart of top topics
            fig_bar = self.topics_model.visualize_barchart(top_n_topics=8, height=400)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Topic similarity heatmap (if enough topics)
            total_topics = len(self.topics_df[self.topics_df["Topic"] != -1])
            if total_topics > 3:
                with st.expander("🔥 Topic Similarity Heatmap"):
                    fig_heatmap = self.topics_model.visualize_heatmap(height=500)
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                    
        except Exception as e:
            st.warning(f"⚠️ Visualization error: {str(e)}")
    
    def generate_business_insights(self):
        """Generate actionable business insights from topics and ML models."""
        if self.df is None or "Topic" not in self.df.columns:
            return
        
        st.markdown("---")
        st.markdown("### 💡 Business Insights & Recommendations")
        
        # Calculate NPS per topic
        topic_insights = (
            self.df[self.df["Topic"] != -1]  # Exclude outliers
            .groupby("Name")
            .agg(
                Comment_Count=("Comment", "count"),
                Avg_Score=("Score", "mean"),
                NPS_Score=("NPS Type", lambda x: calculate_nps(pd.DataFrame({"NPS Type": x})))
            )
            .reset_index()
            .sort_values(by="Comment_Count", ascending=False)
        )
        
        # Add ML model agreement analysis if models were trained
        if self.models_trained and "Model_1_Prediction" in self.df.columns:
            st.markdown("#### 🤝 ML Model vs Topic Analysis")
            
            # Calculate model agreement per topic
            model_topic_analysis = (
                self.df[self.df["Topic"] != -1]
                .groupby("Name")
                .agg(
                    Model1_Accuracy=("Model_1_Prediction", lambda x: (x == self.df.loc[x.index, "NPS Type"]).mean()),
                    Avg_Confidence=("Score", "mean")
                )
                .reset_index()
            )
            
            # Merge with topic insights
            topic_insights = topic_insights.merge(model_topic_analysis, on="Name", how="left")
        
        # Display insights table
        st.write("**Topic Performance Analysis:**")
        
        # Format the insights for better readability
        topic_insights["Avg_Score"] = topic_insights["Avg_Score"].round(2)
        topic_insights["NPS_Score"] = topic_insights["NPS_Score"].round(1)
        
        if "Model1_Accuracy" in topic_insights.columns:
            topic_insights["Model1_Accuracy"] = (topic_insights["Model1_Accuracy"] * 100).round(1)
        
        # Color code based on NPS scores
        def color_nps(val):
            if val >= 50:
                return 'background-color: #2e6930'  # Green for good NPS
            elif val >= 0:
                return 'background-color: #fff3cd'  # Yellow for neutral
            else:
                return 'background-color: #f8d7da'  # Red for poor NPS
        
        styled_insights = topic_insights.style.applymap(
            color_nps, subset=['NPS_Score']
        )
        
        st.dataframe(styled_insights, use_container_width=True)
        
        # Generate specific recommendations
        self.generate_recommendations(topic_insights)
    
    def generate_recommendations(self, topic_insights: pd.DataFrame):
        """Generate specific business recommendations based on topic and ML analysis."""
        st.markdown("#### 🎯 Actionable Recommendations")
        
        # Identify priority topics (high volume + low NPS)
        priority_topics = topic_insights[
            (topic_insights["Comment_Count"] >= topic_insights["Comment_Count"].quantile(0.5)) &
            (topic_insights["NPS_Score"] < 0)
        ]
        
        if len(priority_topics) > 0:
            st.warning("🚨 **Priority Issues Requiring Immediate Attention:**")
            for _, topic in priority_topics.iterrows():
                st.write(f"- **{topic['Name']}**: {topic['Comment_Count']} comments, NPS: {topic['NPS_Score']:.1f}")
                
                # Add ML model insights if available
                if "Model1_Accuracy" in topic.index:
                    st.write(f"  � *ML Model Accuracy: {topic['Model1_Accuracy']:.1f}%*")
                
                st.write(f"  �💡 *Recommendation: Investigate and address issues in this area immediately*")
        
        # Identify success areas (high NPS)
        success_topics = topic_insights[topic_insights["NPS_Score"] >= 50]
        
        if len(success_topics) > 0:
            st.success("✅ **Success Areas to Leverage:**")
            for _, topic in success_topics.iterrows():
                st.write(f"- **{topic['Name']}**: NPS: {topic['NPS_Score']:.1f}")
                st.write(f"  💡 *Recommendation: Replicate these successful practices across other areas*")
        
        # Overall insights
        avg_nps = topic_insights["NPS_Score"].mean()
        st.info(f"📊 **Overall Topic-based NPS: {avg_nps:.1f}**")
        
        if avg_nps < 0:
            st.write("🔄 *Focus on addressing negative feedback themes to improve overall satisfaction*")
        elif avg_nps < 50:
            st.write("📈 *Good foundation - focus on converting passives to promoters*")
        else:
            st.write("🎉 *Excellent performance - maintain current strategies and scale successful practices*")

def show_ml_pipeline():
    """
    Main function for the enhanced ML Pipeline with complete model integration.
    """
    st.title("🧠 Enhanced ML Pipeline")
    st.markdown("""
    **Complete ML Pipeline:** Data → Multi-Model Sentiment Analysis → Topic Modeling → Business Intelligence
    
    *Integrates 4 ML models with BERTopic for comprehensive customer feedback analysis.*
    """)
    
    # Initialize enhanced pipeline
    pipeline = EnhancedMLPipeline()
    
    # Model explanations
    create_model_explanations()
    
    # Data upload section
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
    
    # Main pipeline execution
    if uploaded_file is not None:
        # Step 1: Load and validate data
        if pipeline.load_and_validate_data(uploaded_file):
            
            # Step 2: Run sentiment analysis with all models
            st.markdown("---")
            st.markdown("### 🧠 Step 1: Multi-Model Sentiment Analysis")
            pipeline.run_sentiment_analysis()
            
            # Step 3: Topic modeling
            st.markdown("---")
            st.markdown("### 🔍 Step 2: Topic Modeling & Discovery")
            pipeline.run_topic_modeling()
            
            # Step 4: Advanced analytics (if data processed)
            if pipeline.df is not None:
                st.markdown("---")
                st.markdown("### 📊 Step 3: Advanced Analytics")
                
                # Use tabs to avoid expander nesting issues
                tab1, tab2, tab3 = st.tabs(["📋 Cross-Tabulation", "🤝 NPS vs Sentiment", "🔎 Complete Dataset"])
                
                with tab1:
                    st.markdown("#### Cross-Tabulation Analysis")
                    enhanced_crosstab_analysis(pipeline.df)
                
                with tab2:
                    st.markdown("#### NPS vs Sentiment Agreement")
                    display_nps_sentiment_agreement(pipeline.df)
                
                with tab3:
                    st.markdown("#### Complete Dataset with All Predictions")
                    st.dataframe(pipeline.df, use_container_width=True)
                
                # Export functionality
                st.markdown("---")
                st.markdown("### 💾 Export Complete Analysis")
                if st.button("📥 Download Enhanced Analysis Report", type="primary"):
                    # Prepare comprehensive export data
                    export_data = {
                        "pipeline_summary": {
                            "total_records": len(pipeline.df),
                            "models_trained": pipeline.models_trained,
                            "topics_discovered": len(pipeline.topics_df) if pipeline.topics_df is not None else 0
                        },
                        "sentiment_analysis": {
                            "sentiment_distribution": pipeline.df["Sentiment"].value_counts().to_dict(),
                            "nps_distribution": pipeline.df["NPS Type"].value_counts().to_dict()
                        }
                    }
                    
                    # Add ML model metrics if available
                    if pipeline.models_trained:
                        export_data["ml_models"] = pipeline.model_trainer.metrics
                    
                    # Add topic data if available
                    if "Topic" in pipeline.df.columns:
                        export_data["topic_analysis"] = {
                            "total_topics": len(pipeline.topics_df[pipeline.topics_df["Topic"] != -1]) if pipeline.topics_df is not None else 0,
                            "topic_distribution": pipeline.df["Name"].value_counts().to_dict() if "Name" in pipeline.df.columns else {}
                        }
                    
                    st.download_button(
                        label="Download Enhanced Pipeline Report",
                        data=pd.Series(export_data).to_json(indent=2),
                        file_name=f"enhanced_ml_pipeline_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
    
    else:
        st.info("""
        👆 **Upload a CSV file to begin the enhanced ML pipeline**
        
        Your file should contain:
        - `Comment` column: Customer feedback text
        - `Score` column: Numerical rating (0-10)
        - Optional: `Date`, `Store` columns for additional analysis
        
        **Enhanced Pipeline Features:**
        1. **Multi-Model Sentiment Analysis** - Train and compare 4 different ML approaches
        2. **Topic Discovery** - Use BERTopic to find key themes in feedback
        3. **Integrated Insights** - Combine ML predictions with topic analysis
        4. **Business Intelligence** - Generate actionable recommendations
        """)

# Module exports
__all__ = ['show_ml_pipeline']

if __name__ == "__main__":
    show_ml_pipeline()
