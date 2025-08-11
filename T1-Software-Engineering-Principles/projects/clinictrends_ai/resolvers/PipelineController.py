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
    Also responsible to train the models and display the results in a user-friendly way!
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
                
            uploaded_file.seek(0)            
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
        create_model_summary_cards(self.model_trainer.metrics)
        create_detailed_metrics_table(self.model_trainer.metrics)
    
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
        with st.spinner("Processing with transformer model..."):
            df3 = self.model_trainer.train_transformer_model(
                self.df, "Comment", "Model 3: Transformer"
            )
        if df3 is not None:
            map_to_nps = {"POSITIVE": "Promoter", "NEGATIVE": "Detractor", "NEUTRAL": "Passive"}
            # align by index to be safe
            self.df.loc[df3.index, "Model_3_Prediction"] = (
                df3["HF_Label"].str.upper().map(map_to_nps).fillna("Passive")
            )

    def train_model_4(self):
        with st.spinner("Processing hybrid transformer model..."):
            df4 = self.model_trainer.train_transformer_model(
                self.df, "CommentScore", "Model 4: Hybrid"
            )
        if df4 is not None:
            map_to_nps = {"POSITIVE": "Promoter", "NEGATIVE": "Detractor", "NEUTRAL": "Passive"}
            self.df.loc[df4.index, "Model_4_Prediction"] = (
                df4["HF_Label"].str.upper().map(map_to_nps).fillna("Passive")
            )
    
    def run_topic_modeling(self):
        """Run topic modeling using BERTopic."""
        
        with st.spinner("🔍 Training BERTopic model..."):
            try:
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
                    from utils.visualizations import clean_topic_name
                    self.topics_df["Name"] = self.topics_df.apply(
                        lambda row: "Outliers" if row["Topic"] == -1 else clean_topic_name(row["Name"]),
                        axis=1
                    )
                            
                    # Merge topic names with main dataframe
                    self.df = self.df.merge(
                                self.topics_df[["Topic", "Name"]], 
                                on="Topic", 
                                how="left"
                            )
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
        st.markdown("#### Topic Analysis Results")

        # --- Topic overview (compact & pretty) ---
        top_n = 10

        # Clean names (use the helper we added earlier)
        def _safe_clean(x):
            try:
                return clean_topic_name(x)
            except Exception:
                return x

        topics_info = self.topics_df.copy()
        topics_info["CleanName"] = topics_info["Name"].apply(_safe_clean)

        # Basic stats
        in_scope_mask = topics_info["Topic"] != -1
        total_found = int(in_scope_mask.sum())                    # number of non-outlier topics
        outliers = int((self.df["Topic"] == -1).sum()) if "Topic" in self.df.columns else 0
        coverage = ((len(self.df) - outliers) / len(self.df) * 100) if len(self.df) else 0.0

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("**Topics Discovered**")

            # Build display table
            base = topics_info.loc[in_scope_mask, ["Topic", "CleanName", "Count"]]

            table = (
                base.sort_values("Count", ascending=False)
                    .head(top_n)
                    .reset_index(drop=True)
            )

            # rank + share
            table.index = table.index + 1
            table.insert(0, "Rank", table.index)
            table["Share %"] = (table["Count"] / base["Count"].sum() * 100).round(1)

            # ensuring unique column names: keep numeric topic as ID, cleaned as Topic
            table = table.rename(columns={"Topic": "ID", "CleanName": "Topic"})
            table = table[["Rank", "ID", "Topic", "Count", "Share %"]]

            # Rendering
            styled = (
                table.style
                    .format({"Share %": "{:.1f}%"})
                    .bar(subset=["Count"], align="left")
            )

            st.dataframe(styled, hide_index=True, use_container_width=True)
            st.caption(f"Showing top {len(table)} of {len(base)} topics.")

        with col2:
            st.markdown("**Topic Statistics**")
            st.metric("Topics Found", total_found)
            st.metric("Outliers", outliers)
            st.metric("Coverage", f"{coverage:.1f}%")

        # Download full table (cleaned names)
        with st.expander("Full Topic List (See or Download)"):
            full_table = (
                topics_info.loc[in_scope_mask, ["Topic", "CleanName", "Count"]]
                        .sort_values("Count", ascending=False)
                        .rename(columns={"CleanName": "Topic Name"})
            )
            st.dataframe(full_table.head(50), hide_index=True, use_container_width=True)
            st.download_button(
                "⬇️ Download all topics (CSV)",
                data=full_table.to_csv(index=False).encode("utf-8"),
                file_name="topics_overview.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    def generate_business_insights(self):
        """Generate actionable business insights from topics and ML models."""
        if self.df is None or "Topic" not in self.df.columns:
            return
        
        st.markdown("---")
        st.markdown("#### Business Insights")
        
        # Calculate NPS per topic
        topic_insights = (
            self.df[self.df["Topic"] != -1]  # Exclude outliers
            .groupby("Name")
            .agg(
                Comment_Count=("Comment", "count"),
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
                return 'background-color: #98FB98'  # Light green for great NPS (Promoter)
            elif 60 <= val < 80:
                return 'background-color: #fff0b3'  # Soft yellow for neutral NPS (Passive)
            else:
                return 'background-color: #f8d7da'  # Light red for poor NPS (Detractor)
        
        # Only show top 15 in main table
        top_15_insights = topic_insights.head(15)
        styled_top_15 = (
            top_15_insights
            .style
            .applymap(color_nps, subset=['NPS_Score'])
            .format(fmt_map)
        )

        st.caption("**Top 15 Topics by Comment Volume:**")
        st.dataframe(styled_top_15, use_container_width=False, hide_index=True)

        total_rows = len(topic_insights)
        with st.expander(f"🔎 Show full topic insights table ({total_rows} rows)", expanded=False):
            full_styled = topic_insights.style.format(fmt_map)
            st.dataframe(full_styled, use_container_width=False, hide_index=True)
        
        # Generate specific recommendations
        self.generate_recommendations(topic_insights)
    
    def generate_recommendations(self, topic_insights: pd.DataFrame, top_k: int = 5):
        """Generate compact, user-friendly recommendations (two small tables)."""

        st.markdown("#### Actionable Recommendations")

        # ---------- helpers ----------
        nps_promoter = 81
        nps_passive = 61
        nps_detractor = 60
        
        def _shorten(s: str, n: int = 32) -> str:
            s = str(s)
            return s if len(s) <= n else s[: n - 1] + "…"

        def _urgency_badge(nps: float) -> str:
            if nps < -1:
                return "🔥 Critical"
            if nps < 0:
                return "⚠ High"
            if nps <= nps_passive:
                return "⚠ Medium"
            return "—"

        def _success_badge(nps: float) -> str:
            if nps >= nps_promoter:
                return "🏆 Exceptional"
            if nps > nps_passive:
                return "⭐ Excellent"
            return "—"

        # ---------- pick top K lists ----------
        median_cut = topic_insights["Comment_Count"].quantile(0.5)
        problematic_topics = (
            topic_insights[(topic_insights["Comment_Count"] >= median_cut) & (topic_insights["NPS_Score"] < 0)]
            .sort_values(["NPS_Score", "Comment_Count"], ascending=[True, False])
            .head(top_k)
            .copy()
        )

        success_topics = (
            topic_insights[topic_insights["NPS_Score"] >= nps_promoter]
            .sort_values("NPS_Score", ascending=False)
            .head(top_k)
            .copy()
        )

        # ---------- KPIs ----------
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Topics", int(len(topic_insights)))
        col2.metric("Critical Issues", int(len(problematic_topics)))
        col3.metric("Success Areas", int(len(success_topics)))

        # ---------- build compact tables ----------
        critical_df = (
            problematic_topics
            .assign(
                Topic=lambda d: d["Name"].apply(_shorten),
                NPS=lambda d: d["NPS_Score"].round(1),
                Comments=lambda d: d["Comment_Count"].astype(int),
                Urgency=lambda d: d["NPS_Score"].apply(_urgency_badge),
            )[["Topic", "NPS", "Comments", "Urgency"]]
            .sort_values("Comments", ascending=False)
        )

        success_df = (
            success_topics
            .assign(
                Topic=lambda d: d["Name"].apply(_shorten),
                NPS=lambda d: d["NPS_Score"].round(1),
                Comments=lambda d: d["Comment_Count"].astype(int),
                Badge=lambda d: d["NPS_Score"].apply(_success_badge),
            )[["Topic", "NPS", "Comments", "Badge"]]
            .sort_values("Comments", ascending=False)
        )

        # ---------- render side-by-side, compact ----------
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**🚨 Top {len(critical_df)} Critical/High (< 0 NPS)**")
            if len(critical_df) == 0:
                st.success("No critical issues found.")
            else:
                st.dataframe(critical_df, use_container_width=True, hide_index=True)
        with c2:
            st.markdown(f"**🏆 Top {len(success_df)} Success/Excellent (>{nps_promoter} NPS)**")
            if len(success_df) == 0:
                st.info("No success areas found.")
            else:
                st.dataframe(success_df, use_container_width=True, hide_index=True)

        # ---------- details ----------
        with st.expander("Show full topic table"):
            full_df = topic_insights.rename(
                columns={"Name": "Topic", "NPS_Score": "NPS", "Comment_Count": "Comments"}
            )[["Topic", "NPS", "Comments"]].copy()
            full_df["Topic"] = full_df["Topic"].apply(_shorten, n=64)  # slightly longer in the full table
            st.dataframe(full_df, use_container_width=True, hide_index=True)

        st.caption(
            f"Legend: 🔥 Critical (< -1) · ⚠ High (< 0) · ⚠ Medium (0–≤ {nps_passive}) · "
            f"⭐ Excellent (>{nps_passive}) · 🏆 Exceptional (>{nps_promoter})"
        )
    
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
