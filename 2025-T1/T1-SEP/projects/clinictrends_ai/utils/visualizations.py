import altair as alt
import pandas as pd
from typing import Dict, Optional
import streamlit as st
from utils.preprocessing import classify_nps
import numpy as np
import re

def nps_donut_chart(filtered_df: pd.DataFrame):
    chart_data = filtered_df["NPS Type"].value_counts().reset_index()
    chart_data.columns = ["NPS Type", "Count"]

    color_scale = alt.Scale(
        domain=["Detractor", "Passive", "Promoter"],
        range=["#e74c3c", "#f1c40f", "#2ecc71"]
    )

    chart = alt.Chart(chart_data).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="NPS Type", type="nominal", scale=color_scale),
        tooltip=["NPS Type", "Count"]
    ).properties(
        title="NPS Type Distribution"
    )

    return chart


def monthly_nps_trend_chart(filtered_df: pd.DataFrame, calculate_nps_func):
    monthly_summary = (
        filtered_df.groupby("Month")
        .apply(lambda x: calculate_nps_func(x))
        .reset_index()
    )
    monthly_summary.columns = ["Month", "NPS"]

    chart = alt.Chart(monthly_summary).mark_line(point=True).encode(
        x="Month",
        y=alt.Y("NPS", scale=alt.Scale(domain=[0, 100])),
        tooltip=["Month", "NPS"]
    )

    return chart

def create_model_summary_cards(metrics: Dict[str, Dict]) -> None:
    """Compact, ranked model cards with badges, deltas, and safe formatting."""
    if not metrics:
        st.warning("No metrics available for comparison.")
        return

    st.markdown("#### Model Performance Overview")

    # ---- normalize -> list of dicts, add safe defaults ----
    rows = []
    for k, d in metrics.items():
        if not d:
            continue
        rows.append({
            "key": k,
            "name": d.get("Model", k),
            "acc": d.get("Accuracy"),
            "f1": d.get("F1-Score"),
            "time": d.get("Training_Time"),
            "n": d.get("Total_Predictions"),
        })

    if not rows:
        st.info("No completed models to display.")
        return

    # ---- find bests for ranking / badges / deltas ----
    acc_values = [r["acc"] for r in rows if r["acc"] is not None]
    f1_values  = [r["f1"]  for r in rows if r["f1"]  is not None]
    best_acc = max(acc_values) if acc_values else None
    best_f1  = max(f1_values)  if f1_values else None

    # Rank primarily by accuracy, then by F1 (desc)
    def sort_key(r):
        return (
            -1 if r["acc"] is None else -r["acc"],
            -1 if r["f1"]  is None else -r["f1"],
        )
    rows = sorted(rows, key=sort_key)

    # ---- helpers ----
    def perf_dot(v: Optional[float]) -> str:
        if v is None: return "⚪"
        if v >= 0.85: return "🟢"
        if v >= 0.70: return "🟡"
        return "🔴"

    def fmt_pct(v: Optional[float]) -> str:
        return f"{v:.1%}" if v is not None else "N/A"

    def fmt_f1(v: Optional[float]) -> str:
        return f"{v:.3f}" if v is not None else "N/A"

    def fmt_time(s: Optional[float]) -> str:
        if s is None: return "N/A"
        if s < 0.005: return "<0.01s"
        return f"{s:.2f}s"

    def fmt_int(n: Optional[int]) -> str:
        return f"{n:,}" if n is not None else "N/A"

    def delta_to_best(v: Optional[float], best: Optional[float]) -> Optional[str]:
        if v is None or best is None: return None
        diff = v - best
        if abs(diff) < 1e-9:
            return "best"
        sign = "+" if diff > 0 else ""
        return f"{sign}{diff:.1%}"

    # ---- render grid (wrap after 4 per row) ----
    per_row = min(4, max(1, len(rows)))
    cols = st.columns(per_row)

    for i, r in enumerate(rows):
        col = cols[i % per_row]
        with col:
            with st.container(border=True):
                # header with BEST badge
                is_best = (best_acc is not None and r["acc"] == best_acc)
                badge = " 🥇" if is_best else ""
                st.markdown(f"**{r['name']}{badge}**")

                # Accuracy (with color and delta to calculated best)
                acc_dot = perf_dot(r["acc"])
                acc_delta = delta_to_best(r["acc"], best_acc)
                st.metric(
                    label=f"{acc_dot} Accuracy",
                    value=fmt_pct(r["acc"]),
                    delta=(None if acc_delta in (None, "best") else acc_delta),
                    help=("Best accuracy" if acc_delta == "best" else None)
                )
                # tiny bar for accuracy for quick visual scan
                if r["acc"] is not None:
                    st.progress(int(round(r["acc"] * 100)))

                # F1 (with color and delta to calculated best F1)
                f1_dot = perf_dot(r["f1"])
                f1_delta = delta_to_best(r["f1"], best_f1)
                st.metric(
                    label=f"{f1_dot} F1-Score",
                    value=fmt_f1(r["f1"]),
                    delta=(None if f1_delta in (None, "best") else f1_delta),
                    help=("Best F1-Score" if f1_delta == "best" else None)
                )

                # Training time & predictions (compact)
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("⏱️ Time", fmt_time(r["time"]))
                with c2:
                    st.metric("📊 Predictions", fmt_int(r["n"]))

def create_detailed_metrics_table(metrics: Dict[str, Dict]) -> None:
    """Create detailed metrics comparison table."""
    if not metrics:
        return    
    # Helper function to safely format metrics
    def safe_format(value, format_type="float"):
        if value is None:
            return "N/A"
        if format_type == "percentage":
            return f"{value:.1%}"
        elif format_type == "float":
            return f"{value:.3f}"
        elif format_type == "time":
            return f"{value:.2f}s"
        elif format_type == "int":
            return f"{value:,}"
        return str(value)
    
    metrics_df = pd.DataFrame([
        {
            "Model": data["Model"],
            "Accuracy": safe_format(data['Accuracy'], "percentage"),
            "Precision": safe_format(data['Precision'], "float"),
            "Recall": safe_format(data['Recall'], "float"),
            "F1-Score": safe_format(data['F1-Score'], "float"),
            "Training Time": safe_format(data['Training_Time'], "time"),
            "Predictions": safe_format(data['Total_Predictions'], "int")
        }
        for data in metrics.values() if data
    ])
    
    if not metrics_df.empty:
        # Find best performing model for each metric (only for non-None values)
        raw_metrics = pd.DataFrame([
            {
                "Model": data["Model"],
                "Accuracy": data['Accuracy'],
                "Precision": data['Precision'],
                "Recall": data['Recall'],
                "F1-Score": data['F1-Score'],
                "Training_Time": data['Training_Time']
            }
            for data in metrics.values() if data
        ])
        
        # Highlight best performers (only for non-None values)
        def highlight_best(s):
            if s.name in ['Accuracy', 'Precision', 'Recall', 'F1-Score']:
                # Only highlight if we have valid values to compare
                valid_values = raw_metrics[s.name].dropna()
                if valid_values.empty:
                    return ['' for _ in s]
                
                max_val = valid_values.max()
                highlighted = []
                for i, v in enumerate(s):
                    if v == "N/A":
                        highlighted.append('')
                    else:
                        # Extract numeric value for comparison
                        if s.name == 'Accuracy':
                            numeric_val = float(v.rstrip('%')) / 100
                        else:
                            numeric_val = float(v)
                        
                        if abs(numeric_val - max_val) < 0.001:  # Account for floating point precision
                            highlighted.append('background-color: #2e6930; color: white')
                        else:
                            highlighted.append('')
                return highlighted
                
            elif s.name == 'Training Time':
                valid_values = raw_metrics['Training_Time'].dropna()
                if valid_values.empty:
                    return ['' for _ in s]
                
                min_val = valid_values.min()
                highlighted = []
                for v in s:
                    if v == "N/A":
                        highlighted.append('')
                    else:
                        numeric_val = float(v.rstrip('s'))
                        if abs(numeric_val - min_val) < 0.01:
                            highlighted.append('background-color: #2e6930; color: white')
                        else:
                            highlighted.append('')
                return highlighted
            
            return ['' for _ in s]
        
        styled_df = metrics_df.style.apply(highlight_best, axis=0)
        with st.expander("📋 Detailed Performance Metrics"):
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Performance insights (only for models with valid metrics)
        valid_accuracy = raw_metrics.dropna(subset=['Accuracy'])
        valid_f1 = raw_metrics.dropna(subset=['F1-Score'])
        valid_time = raw_metrics.dropna(subset=['Training_Time'])
        
        insights = []
        if not valid_accuracy.empty:
            best_accuracy = valid_accuracy.loc[valid_accuracy['Accuracy'].idxmax(), 'Model']
            insights.append(f"Best Accuracy 🎯: {best_accuracy}")
        
        if not valid_f1.empty:
            best_f1 = valid_f1.loc[valid_f1['F1-Score'].idxmax(), 'Model']
            insights.append(f"Best F1-Score 🧠: {best_f1}")
        
        if not valid_time.empty:
            fastest = valid_time.loc[valid_time['Training_Time'].idxmin(), 'Model']
            insights.append(f"Fastest Training ⚡: {fastest}")
    
    else:
        st.warning("No metrics available to display.")


def crate_nps_vs_sentiment_analysis(df: pd.DataFrame):
    st.markdown("### 📊 NPS vs Sentiment Analysis Comparison")
    df = classify_nps(df)
            
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**NPS Distribution**")
        donut_chart = nps_donut_chart(df)
        st.altair_chart(donut_chart, use_container_width=True)
        # st.dataframe(df["NPS Type"].value_counts().reset_index(), use_container_width=True)
            
    with col2:
        st.markdown("**Sentiment Distribution**")
        create_sentiment_visualization(df, "Sentiment", "Overall Sentiment Distribution")
    

def create_performance_charts(metrics: Dict[str, Dict]) -> None:
    """Create comprehensive performance visualization charts."""
    if not metrics:
        return
        
    st.subheader("📈 Performance Visualizations")
    
    metrics_df = pd.DataFrame([
        {
            "Model": data["Model"],
            "Accuracy": data["Accuracy"],
            "Precision": data["Precision"],
            "Recall": data["Recall"],
            "F1-Score": data["F1-Score"],
            "Training_Time": data["Training_Time"]
        }
        for data in metrics.values() if data
    ])
    
    if not metrics_df.empty:
        # Create tabs for different chart types
        chart_tab1, chart_tab2, chart_tab3 = st.tabs(["📊 Performance Metrics", "⏱️ Training Time", "🎯 Radar Chart"])
        
        with chart_tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Accuracy comparison
                accuracy_chart = alt.Chart(metrics_df).mark_bar(color='steelblue').encode(
                    x=alt.X('Model:N', sort='-y', title='Model'),
                    y=alt.Y('Accuracy:Q', scale=alt.Scale(domain=[0, 1]), title='Accuracy'),
                    tooltip=['Model', alt.Tooltip('Accuracy:Q', format='.1%')]
                ).properties(
                    title="Model Accuracy Comparison",
                    width=300,
                    height=250
                )
                st.altair_chart(accuracy_chart, use_container_width=True)
            
            with col2:
                # F1-Score comparison
                f1_chart = alt.Chart(metrics_df).mark_bar(color='orange').encode(
                    x=alt.X('Model:N', sort='-y', title='Model'),
                    y=alt.Y('F1-Score:Q', scale=alt.Scale(domain=[0, 1]), title='F1-Score'),
                    tooltip=['Model', alt.Tooltip('F1-Score:Q', format='.3f')]
                ).properties(
                    title="Model F1-Score Comparison",
                    width=300,
                    height=250
                )
                st.altair_chart(f1_chart, use_container_width=True)
        
        with chart_tab2:
            # Training time comparison
            time_chart = alt.Chart(metrics_df).mark_bar(color='green').encode(
                x=alt.X('Model:N', sort='y', title='Model'),
                y=alt.Y('Training_Time:Q', title='Training Time (seconds)'),
                tooltip=['Model', alt.Tooltip('Training_Time:Q', format='.2f')]
            ).properties(
                title="Training Time Comparison (Lower is Better)",
                width=600,
                height=300
            )
            st.altair_chart(time_chart, use_container_width=True)
        
        with chart_tab3:
            # Radar chart data preparation
            st.markdown("**Multi-dimensional Performance Comparison**")
            
            # Normalize metrics for radar chart (0-1 scale)
            normalized_df = metrics_df.copy()
            # Invert training time (lower is better)
            max_time = normalized_df['Training_Time'].max()
            normalized_df['Training_Speed'] = 1 - (normalized_df['Training_Time'] / max_time)
            
            # Create a simple comparison table for radar-like view
            radar_metrics = normalized_df[['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score', 'Training_Speed']]
            
            # Style the dataframe to look like a radar chart alternative
            def color_scale(val):
                if isinstance(val, (int, float)):
                    if val >= 0.8:
                        return 'background-color: #2ecc71; color: white'
                    elif val >= 0.6:
                        return 'background-color: #f1c40f; color: black'
                    else:
                        return 'background-color: #e74c3c; color: white'
                return ''
            
            styled_radar = radar_metrics.style.applymap(color_scale, subset=['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Training_Speed'])
            st.dataframe(styled_radar, use_container_width=True)
            
            st.caption("🟢 Excellent (≥80%) | 🟡 Good (≥60%) | 🔴 Needs Improvement (<60%)")


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
        # st.dataframe(chart_data, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating visualization for {title}: {str(e)}")

def model_architecture_info():
    with st.expander("📋 Model Architecture Information"):
                st.markdown("""                
                **🔴 Model 1: Comment-Based Classification**
                - Pipeline: Raw Comments → TF-IDF Vectorization → Logistic Regression
                - Features: 5,000 TF-IDF features
                
                **🟡 Model 2: Enhanced Comment-Score Fusion**
                - Pipeline: Comments + Scores → TF-IDF → Classification
                - Innovation: Combines textual and numerical features
                
                **🟢 Model 3: Transformer-Enhanced Classification** *(Prototype)*
                - Pipeline: Comments → DistilBERT → Fine-tuned Classification
                
                **🔵 Model 4: Hybrid Transformer-Score Integration** *(Prototype)*
                - Pipeline: Comments + Scores → Transformer Encoding → Feature Fusion
                """)

def create_model_explanations():
    """Create expandable sections explaining each model."""    
    with st.expander("📖 Understanding Our ML Models", expanded=False):
        st.markdown("""
        **ClinicTrends AI** implements 4 distinct machine learning pipelines for sentiment analysis:
        
        **Model 1: TextBlob Sentiment Analysis**
        - 📊 **Type**: Rule-based sentiment analysis
        - ⚡ **Speed**: Very fast
        - 🎯 **Best for**: Quick sentiment scoring with good baseline performance
        - 🔧 **Technology**: Pre-trained lexicon-based approach
        
        **Model 2: Custom TF-IDF + Logistic Regression**
        - 📊 **Type**: Traditional machine learning
        - ⚡ **Speed**: Fast training and prediction
        - 🎯 **Best for**: Interpretable results with good performance
        - 🔧 **Technology**: TF-IDF vectorization with balanced class weights
        
        **Model 3: Hugging Face Transformers (Prototype)**
        - 📊 **Type**: Deep learning transformer model
        - ⚡ **Speed**: Slower but more accurate
        - 🎯 **Best for**: State-of-the-art sentiment analysis
        - 🔧 **Technology**: Pre-trained BERT-based models
        - ⚠️ **Note**: Requires additional dependencies
        
        **Model 4: Hybrid Approach (Prototype)**
        - 📊 **Type**: Ensemble of multiple models
        - ⚡ **Speed**: Variable depending on components
        - 🎯 **Best for**: Combining strengths of different approaches
        - 🔧 **Technology**: Weighted combination of Models 1-3
        - ⚠️ **Note**: Experimental implementation
        """)
        
        st.markdown("""
        ### 📈 Performance Metrics Explained
        
        - **Accuracy**: Overall percentage of correct predictions
        - **Precision**: Of all positive predictions, how many were actually positive?
        - **Recall**: Of all actual positives, how many did we correctly identify?
        - **F1-Score**: Harmonic mean of precision and recall (balanced metric)
        - **Training Time**: Time taken to train the model on your dataset
        """)

def create_nps_explanations():
    """Create expandable sections explaining NPS metrics."""    
    with st.expander("📖 Understanding NPS Metrics", expanded=False):
        st.markdown("""
        **Explore powerful insights from your customer feedback.**
        
        ### 📈 NPS Metrics Explained
        
        - **NPS Score**: Percentage of customers who are promoters (9-10) minus detractors (0-6)
        - 🟢 **Promoters**: Customers who are very likely to recommend your product or service
        - 🟡 **Passives**: Customers who are neutral and may be swayed by future experiences
        - 🔴 **Detractors**: Customers who are unlikely to recommend your product or service

        The NPS Analytics Dashboard enables:
        
        - **Track customer feedback trends** over time (monthly, quarterly, yearly)
        - **Visualize NPS performance**: identify Promoters, Passives, and Detractors
        - **Analyze customer comments** using NLP to reveal underlying sentiment patterns
        - **Compare NPS vs. Sentiment Alignment**: detect potential mismatches or hidden insights
        """)

def display_nps_sentiment_agreement(df: pd.DataFrame) -> float:
    """
    Calculate and display the agreement rate between NPS Type and ML-predicted Sentiment.

    Args:
        df (pd.DataFrame): DataFrame containing 'NPS Type' and 'Sentiment' columns.

    Returns:
        float: Agreement rate as a decimal (e.g., 0.86 for 86%)
    """
    nps_sentiment_map = {
        "Promoter": "POSITIVE",
        "Passive": "NEUTRAL",
        "Detractor": "NEGATIVE"
    }

    df["NPS_Sentiment"] = df["NPS Type"].map(nps_sentiment_map)
    agreement_rate = np.mean(df["NPS_Sentiment"] == df["Sentiment"])

    st.info(f"🎯 **Quick Summary**: Overall NPS-Sentiment agreement rate is {agreement_rate:.1%}")

    return agreement_rate

def clean_topic_name(name: str, *, lower: bool = True) -> str:
    """Turn '12_service_great_excellent_good' → 'service great excellent good'."""
    if pd.isna(name):
        return name
    s = str(name).strip()
    s = re.sub(r'^\s*-?\d+_?', '', s)   # drop leading numeric id like 0_, 12_, -1_
    s = s.replace('_', ' ')             # underscores → spaces
    s = re.sub(r'\s+', ' ', s).strip()  # collapse spaces
    return s.lower() if lower else s