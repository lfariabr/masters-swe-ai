import altair as alt
import pandas as pd
from typing import Dict
import streamlit as st
from utils.preprocessing import classify_nps
import numpy as np

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
    """Create summary cards for each model with key metrics."""
    if not metrics:
        st.warning("No metrics available for comparison.")
        return
    
    st.subheader("🎯 Model Performance Overview")
    
    # Create columns for model cards
    cols = st.columns(len(metrics))
    
    for idx, (model_key, data) in enumerate(metrics.items()):
        if data:
            with cols[idx]:
                with st.container():
                    st.markdown(f"##### {data['Model']}")
                    
                    # Key metrics with color coding
                    accuracy = data['Accuracy']
                    f1_score = data['F1-Score']
                    
                    # Color code based on performance
                    acc_color = "🟢" if accuracy > 0.8 else "🟡" if accuracy > 0.6 else "🔴"
                    f1_color = "🟢" if f1_score > 0.8 else "🟡" if f1_score > 0.6 else "🔴"
                    
                    st.metric(
                        label=f"{acc_color} Accuracy",
                        value=f"{accuracy:.1%}"
                    )
                    st.metric(
                        label=f"{f1_color} F1-Score",
                        value=f"{f1_score:.3f}"
                    )
                    st.metric(
                        label="⏱️ Training Time",
                        value=f"{data['Training_Time']:.2f}s"
                    )
                    st.metric(
                        label="📊 Predictions",
                        value=f"{data['Total_Predictions']:,}"
                    )


def create_detailed_metrics_table(metrics: Dict[str, Dict]) -> None:
    """Create detailed metrics comparison table."""
    if not metrics:
        return
    
    st.subheader("📋 Detailed Performance Metrics")
    
    metrics_df = pd.DataFrame([
        {
            "Model": data["Model"],
            "Accuracy": f"{data['Accuracy']:.1%}",
            "Precision": f"{data['Precision']:.3f}",
            "Recall": f"{data['Recall']:.3f}",
            "F1-Score": f"{data['F1-Score']:.3f}",
            "Training Time": f"{data['Training_Time']:.2f}s",
            "Predictions": f"{data['Total_Predictions']:,}"
        }
        for data in metrics.values() if data
    ])
    
    if not metrics_df.empty:
        # Find best performing model for each metric
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
        
        # Highlight best performers
        def highlight_best(s):
            if s.name in ['Accuracy', 'Precision', 'Recall', 'F1-Score']:
                max_val = raw_metrics[s.name].max()
                return [f'background-color: #90EE90' if float(v.rstrip('%').replace(',', '')) == max_val * (100 if s.name == 'Accuracy' else 1) else '' for v in s]
            elif s.name == 'Training_Time':
                min_val = raw_metrics['Training_Time'].min()
                return [f'background-color: #90EE90' if float(v.rstrip('s')) == min_val else '' for v in s]
            return ['' for _ in s]
        
        styled_df = metrics_df.style.apply(highlight_best, axis=0)
        st.dataframe(styled_df, use_container_width=True)
        
        # Performance insights
        best_accuracy = raw_metrics.loc[raw_metrics['Accuracy'].idxmax(), 'Model']
        best_f1 = raw_metrics.loc[raw_metrics['F1-Score'].idxmax(), 'Model']
        fastest = raw_metrics.loc[raw_metrics['Training_Time'].idxmin(), 'Model']
        
        st.info(f"🏆 **Best Accuracy**: {best_accuracy} | **Best F1-Score**: {best_f1} | **Fastest Training**: {fastest}")

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
    