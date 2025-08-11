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

class MLpipelineController:
    """
    This gentleman is responsible for the the first ML Pipeline I'm implementing for ClinicTrends AI
    It is responsible to integrate 4 sentiment analysis models as well as topic modeling for comprehensive insights on the data uploaded by the user
    It is also responsible to train the models and display the results in a user-friendly way
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
                
            # Reset file pointer to beginning - CRUCIAL FIX!
            # This is needed because the file may have been read already in NPSPage
            uploaded_file.seek(0)
            
            self.df = pd.read_csv(uploaded_file)
            # st.dataframe(self.df, use_container_width=True)
            
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
            # with st.expander("👀 Data Preview"):
            #     st.dataframe(self.df.sample(min(5, len(self.df))), use_container_width=True)
            #     st.info(f"Dataset shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns")
            #     st.success(f"Total records loaded: {len(self.df)}")
            
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
    
    def train_bertopic(self):
        """Train BERTopic model and assign topics to dataframe."""
        
        with st.spinner("Training BERTopic model..."):
            self.topics_model, topics, probs, embeddings = train_bertopic_model(self.df["Comment"])
            print(topics)
            print(probs)
            print(embeddings)
            print(self.topics_model)

            self.run_topic_modeling()
        
        if self.topics_model is not None:
            self.df["Topic"] = topics
            self.topics_df = pd.DataFrame({"Topic": topics, "Probs": probs})
    
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
        """Run topic modeling using BERTopic."""
        
        with st.spinner("🔍 Training BERTopic model..."):
            try:
                # Import the topic modeling function
                from resolvers.BERTopicModel import train_bertopic_model
                
                # Filter valid comments
                valid_mask = self.df["Comment"].notna() & self.df["Comment"].str.strip().ne("")
                valid_comments = self.df.loc[valid_mask, "Comment"]
                        
                if len(valid_comments) < 10:
                    st.warning("⚠️ Need at least 10 valid comments for topic modeling")
                else:
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
                            
                    # Display results and generate insights
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
            st.write("**Topics Discovered:**")
            st.write("---")
            display_topics = self.topics_df.head(10)[["Topic", "Name", "Count"]]
            st.dataframe(display_topics, use_container_width=True, hide_index=True)
        
        with col2:
            total_topics = len(self.topics_df[self.topics_df["Topic"] != -1])
            outliers = len(self.df[self.df["Topic"] == -1]) if "Topic" in self.df.columns else 0
            
            st.write("**Topic Statistics:**")
            st.write("---")
            st.metric("Topics Found", total_topics)
            st.metric("Outliers", outliers)
            if len(self.df) > 0:
                st.metric("Coverage", f"{((len(self.df) - outliers) / len(self.df) * 100):.1f}%")
    
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
                # Avg_Score=("Score", "mean"),
                NPS_Score=("NPS Type", lambda x: calculate_nps(pd.DataFrame({"NPS Type": x})))
            )
            .reset_index()
            .sort_values(by="Comment_Count", ascending=False)
        )
        
        # Add ML model agreement analysis if models were trained (dynamic for all Model_*_Prediction)
        if self.models_trained:
            pred_cols = [c for c in self.df.columns if c.startswith("Model_") and c.endswith("_Prediction")]
            if pred_cols:
                per_topic = self.df[self.df["Topic"] != -1][["Name", "NPS Type"] + pred_cols].copy()

                acc_frames = []
                for col in pred_cols:
                    acc = (
                        per_topic
                        .assign(_hit=lambda d: (d[col] == d["NPS Type"]).astype(float))
                        .groupby("Name", as_index=False)["_hit"].mean()
                        .rename(columns={"_hit": f"{col.replace('_Prediction','')}_Accuracy"})
                    )
                    acc_frames.append(acc)

                from functools import reduce
                model_topic_analysis = reduce(lambda l, r: l.merge(r, on="Name", how="left"), acc_frames)
                topic_insights = topic_insights.merge(model_topic_analysis, on="Name", how="left")
        
        # Display insights table
        st.write("**Performance Analysis:**")

        # Format the insights for better readability
        topic_insights["NPS_Score"] = topic_insights["NPS_Score"].round(1)

        # Dynamically format all *_Accuracy columns
        acc_cols = [c for c in topic_insights.columns if c.endswith("_Accuracy")]
        for c in acc_cols:
            topic_insights[c] = (topic_insights[c] * 100).round(1)

        fmt_map = {"NPS_Score": "{:.1f}"}
        fmt_map.update({c: "{:.1f}" for c in acc_cols})
        
        # Color code based on NPS scores
        def color_nps(val):
            if val >= 80:
                return 'background-color: #98FB98'  # Light green (great NPS)
            elif 70 <= val < 80:
                return 'background-color: #fff0b3'  # Soft yellow (slightly stronger than #fff3cd)
            else:
                return 'background-color: #f8d7da'  # Light red (poor NPS)
        
        # Only show top 15 in main table
        top_15_insights = topic_insights.head(15)
        styled_top_15 = (
            top_15_insights
            .style
            .applymap(color_nps, subset=['NPS_Score'])
            .format(fmt_map)
        )

        # Display top 15 styled rows
        st.caption("**Top 15 Topics by Comment Volume:**")
        st.dataframe(styled_top_15, use_container_width=False, hide_index=True)

        # Show full unstyled table in expander
        total_rows = len(topic_insights)
        with st.expander(f"🔎 Show full topic insights table ({total_rows} rows)", expanded=False):
            full_styled = topic_insights.style.format(fmt_map)
            st.dataframe(full_styled, use_container_width=False, hide_index=True)
        
        # Generate specific recommendations
        self.generate_recommendations(topic_insights)
    
    def generate_recommendations(self, topic_insights: pd.DataFrame):
        """Generate specific business recommendations based on topic and ML analysis."""
        
        st.write("**Actionable Recommendations**")
        
        # Sort and limit data for better UX
        problematic_topics = topic_insights[
            (topic_insights["Comment_Count"] >= topic_insights["Comment_Count"].quantile(0.5)) &
            (topic_insights["NPS_Score"] < 0)
        ].sort_values(['NPS_Score', 'Comment_Count'], ascending=[True, False]).head(5)

        success_topics = topic_insights[
            topic_insights["NPS_Score"] >= 50
        ].sort_values('NPS_Score', ascending=False).head(5)
        
        # Quick stats summary
        total_topics = len(topic_insights)
        critical_topics = len(problematic_topics)
        success_count = len(success_topics)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Topics", total_topics)
        with col2:
            st.metric("Critical Issues", critical_topics, delta=f"-{critical_topics}" if critical_topics > 0 else "0")
        with col3:
            st.metric("Success Areas", success_count, delta=f"+{success_count}")
        
        col1, col2 = st.columns(2)
        with col1:
            # Priority Issues Section
            if len(problematic_topics) > 0:
                st.warning(f"🚨 **Top {len(problematic_topics)} Priority Issues Requiring Immediate Attention:**")
                
                for idx, (_, topic) in enumerate(problematic_topics.iterrows(), 1):
                    urgency = "🔥 CRITICAL" if topic['NPS_Score'] < -1 else "⚠️ HIGH"
                    st.write(f"{idx}. **{topic['Name']}** ({urgency})")
                    st.write(f"   📊 {topic['Comment_Count']} comments | NPS: {topic['NPS_Score']}")
                
                # Add actionable insight based on severity
                if topic['NPS_Score'] < -1:
                    st.write(f"   💡 *Immediate escalation needed - consider emergency response team*")
                else:
                    st.write(f"   💡 *Schedule improvement initiative within 30 days*")
            
            if len(topic_insights[(topic_insights["Comment_Count"] >= topic_insights["Comment_Count"].quantile(0.5)) & 
                                (topic_insights["NPS_Score"] < 0)]) > 5:
                st.info("ℹ️ Showing top 5 priority issues. Full analysis available in detailed view.")
            else:
                st.success("✅ No critical priority issues identified!")
        
        with col2:
            # Success Areas Section
            if len(success_topics) > 0:
                st.success(f"✅ **Top {len(success_topics)} Success Areas to Leverage:**")
            
            for idx, (_, topic) in enumerate(success_topics.iterrows(), 1):
                excellence = "🏆 EXCEPTIONAL" if topic['NPS_Score'] >= 75 else "⭐ EXCELLENT"
                st.write(f"{idx}. **{topic['Name']}** ({excellence})")
                st.write(f"   📊 {topic['Comment_Count']} comments | NPS: {topic['NPS_Score']}")
            
            st.write(f"   💡 *Recommendation: Use as best practice template for underperforming areas*")
            
            if len(topic_insights[topic_insights["NPS_Score"] >= 50]) > 5:
                st.info("ℹ️ Showing top 5 success areas. Additional high-performers available in detailed view.")
        
        with st.expander("Detailed view of comments per topic"):
            if self.df is not None and "Topic" in self.df.columns and "Name" in self.df.columns:
                dissection_df = self.df[["Comment", "Score", "NPS Type", "Topic", "Name"]].copy()
                dissection_df = dissection_df.sort_values(by="Topic")
                st.dataframe(dissection_df, use_container_width=True, hide_index=True)
            else:
                st.warning("⚠️ Cannot display detailed data: missing Topic or Name columns.")

        # Enhanced Overall Insights
        st.markdown("---")
        st.markdown("#### 📈 Strategic Insights")
        
        avg_nps = topic_insights["NPS_Score"].mean()
        median_nps = topic_insights["NPS_Score"].median()
        nps_std = topic_insights["NPS_Score"].std()
        
        if avg_nps < -20:
            st.error("🚨 **Crisis Mode**: Immediate systematic review required across all touchpoints")
            st.write("• Establish daily monitoring dashboard")
            st.write("• Create cross-functional crisis response team")
            st.write("• Implement weekly customer pulse surveys")
        elif avg_nps < 60:
            st.warning("🔄 **Recovery Focus**: Address negative feedback themes systematically")
            st.write("• Prioritize top 3 critical issues for immediate action")
            st.write("• Implement bi-weekly improvement sprints")
            st.write("• Set up customer feedback loop closure process")
        elif avg_nps <= 80:
            st.info("📈 **Growth Mode**: Convert satisfied customers to promoters")
            st.write("• Focus on enhancing good-performing areas")
            st.write("• Implement customer success programs")
            st.write("• Create referral and advocacy opportunities")
        else:
            st.success("🎉 **Excellence Mode**: Maintain and scale successful practices")
            st.write("• Document and replicate best practices")
            st.write("• Expand successful initiatives")
            st.write("• Consider premium service offerings")
        
        # Data quality insights
        if nps_std > 40:
            st.warning("⚠️ **High Variability Detected**: Inconsistent experience across topics")
            st.write("• Focus on standardizing service delivery")
            st.write("• Investigate root causes of performance gaps")
        
        # ROI prioritization
        if len(problematic_topics) > 0 and len(success_topics) > 0:
            st.info("💡 **Quick Win Opportunity**: Apply successful practices from high-NPS topics to critical issues")
            
            # Suggest specific matches if possible
            top_success = success_topics.iloc[0]['Name'] if len(success_topics) > 0 else None
            top_priority = problematic_topics.iloc[0]['Name'] if len(problematic_topics) > 0 else None
            
            if top_success and top_priority:
                st.write(f"• Consider: What makes **'{top_success}'** successful that could improve **'{top_priority}'**?")

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
    pipeline = MLpipelineController()
    
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
            # if pipeline.df is not None:
            #     st.markdown("---")
            #     st.markdown("### 📊 Step 3: Advanced Analytics")
                
            #     # Use tabs to avoid expander nesting issues
            #     tab1, tab2, tab3 = st.tabs(["📋 Cross-Tabulation", "🤝 NPS vs Sentiment", "🔎 Complete Dataset"])
                
            #     with tab1:
            #         st.markdown("#### Cross-Tabulation Analysis")
            #         enhanced_crosstab_analysis(pipeline.df)
                
            #     with tab2:
            #         st.markdown("#### NPS vs Sentiment Agreement")
            #         display_nps_sentiment_agreement(pipeline.df)
                
            #     with tab3:
            #         st.markdown("#### Complete Dataset with All Predictions")
            #         st.dataframe(pipeline.df, use_container_width=True)
                
            #     # Export functionality
            #     st.markdown("---")
            #     st.markdown("### 💾 Export Complete Analysis")
            #     if st.button("📥 Download Enhanced Analysis Report", type="primary"):
            #         # Prepare comprehensive export data
            #         export_data = {
            #             "pipeline_summary": {
            #                 "total_records": len(pipeline.df),
            #                 "models_trained": pipeline.models_trained,
            #                 "topics_discovered": len(pipeline.topics_df) if pipeline.topics_df is not None else 0
            #             },
            #             "sentiment_analysis": {
            #                 "sentiment_distribution": pipeline.df["Sentiment"].value_counts().to_dict(),
            #                 "nps_distribution": pipeline.df["NPS Type"].value_counts().to_dict()
            #             }
            #         }
                    
            #         # Add ML model metrics if available
            #         if pipeline.models_trained:
            #             export_data["ml_models"] = pipeline.model_trainer.metrics
                    
            #         # Add topic data if available
            #         if "Topic" in pipeline.df.columns:
            #             export_data["topic_analysis"] = {
            #                 "total_topics": len(pipeline.topics_df[pipeline.topics_df["Topic"] != -1]) if pipeline.topics_df is not None else 0,
            #                 "topic_distribution": pipeline.df["Name"].value_counts().to_dict() if "Name" in pipeline.df.columns else {}
            #             }
                    
            #         st.download_button(
            #             label="Download Enhanced Pipeline Report",
            #             data=pd.Series(export_data).to_json(indent=2),
            #             file_name=f"enhanced_ml_pipeline_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
            #             mime="application/json"
            #         )
    
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
