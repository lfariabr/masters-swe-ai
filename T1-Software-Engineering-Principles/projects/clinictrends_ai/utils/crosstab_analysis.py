"""
ClinicTrends AI - Enhanced Cross-Tab Analysis Module
==================================================

Advanced cross-tabulation analysis and heatmap visualizations for NPS vs Sentiment correlation.
Provides comprehensive statistical insights and interactive visualizations.

"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
from scipy.stats import chi2_contingency
from typing import Dict, Tuple


def calculate_statistical_measures(crosstab: pd.DataFrame) -> Dict:
    """Calculate comprehensive statistical measures for cross-tabulation."""
    try:
        # Chi-square test
        chi2, p_value, dof, expected = chi2_contingency(crosstab)
        
        # Cramér's V (effect size) - manual calculation
        n = crosstab.sum().sum()
        cramers_v_value = np.sqrt(chi2 / (n * (min(crosstab.shape) - 1)))
        
        # Row and column percentages
        row_percentages = crosstab.div(crosstab.sum(axis=1), axis=0) * 100
        col_percentages = crosstab.div(crosstab.sum(axis=0), axis=1) * 100
        
        # Total percentages
        total_percentages = crosstab / crosstab.sum().sum() * 100
        
        return {
            'chi2': chi2,
            'p_value': p_value,
            'degrees_of_freedom': dof,
            'cramers_v': cramers_v_value,
            'expected_frequencies': expected,
            'row_percentages': row_percentages,
            'col_percentages': col_percentages,
            'total_percentages': total_percentages,
            'sample_size': n
        }
    except Exception as e:
        st.error(f"Error calculating statistical measures: {str(e)}")
        return {}


def create_enhanced_heatmap(crosstab: pd.DataFrame, title: str = "NPS vs Sentiment Heatmap") -> go.Figure:
    """Create an enhanced interactive heatmap with Plotly."""
    
    # Calculate percentages for better interpretation
    percentages = crosstab.div(crosstab.sum().sum()) * 100
    
    # Create custom hover text
    hover_text = []
    for i in range(len(crosstab.index)):
        hover_row = []
        for j in range(len(crosstab.columns)):
            count = crosstab.iloc[i, j]
            pct = percentages.iloc[i, j]
            hover_row.append(f'Count: {count}<br>Percentage: {pct:.1f}%<br>Row: {crosstab.index[i]}<br>Column: {crosstab.columns[j]}')
        hover_text.append(hover_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=crosstab.values,
        x=crosstab.columns,
        y=crosstab.index,
        colorscale='RdYlBu_r',
        text=crosstab.values,
        texttemplate="%{text}",
        textfont={"size": 14, "color": "white"},
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover_text,
        colorbar=dict(
            title="Count"
        )
    ))
    
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis_title="Sentiment Analysis Result",
        yaxis_title="NPS Classification",
        width=600,
        height=400,
        font=dict(size=12)
    )
    
    return fig


def create_percentage_heatmaps(stats: Dict) -> Tuple[go.Figure, go.Figure, go.Figure]:
    """Create three different percentage-based heatmaps."""
    
    # Row percentages heatmap
    row_fig = go.Figure(data=go.Heatmap(
        z=stats['row_percentages'].values,
        x=stats['row_percentages'].columns,
        y=stats['row_percentages'].index,
        colorscale='Blues',
        text=stats['row_percentages'].round(1).values,
        texttemplate="%{text}%",
        textfont={"size": 12},
        colorbar=dict(title="Row %")
    ))
    row_fig.update_layout(
        title="Row Percentages (% within each NPS Type)",
        xaxis_title="Sentiment",
        yaxis_title="NPS Type",
        height=300
    )
    
    # Column percentages heatmap
    col_fig = go.Figure(data=go.Heatmap(
        z=stats['col_percentages'].values,
        x=stats['col_percentages'].columns,
        y=stats['col_percentages'].index,
        colorscale='Greens',
        text=stats['col_percentages'].round(1).values,
        texttemplate="%{text}%",
        textfont={"size": 12},
        colorbar=dict(title="Col %")
    ))
    col_fig.update_layout(
        title="Column Percentages (% within each Sentiment)",
        xaxis_title="Sentiment",
        yaxis_title="NPS Type",
        height=300
    )
    
    # Total percentages heatmap
    total_fig = go.Figure(data=go.Heatmap(
        z=stats['total_percentages'].values,
        x=stats['total_percentages'].columns,
        y=stats['total_percentages'].index,
        colorscale='Oranges',
        text=stats['total_percentages'].round(1).values,
        texttemplate="%{text}%",
        textfont={"size": 12},
        colorbar=dict(title="Total %")
    ))
    total_fig.update_layout(
        title="Total Percentages (% of entire dataset)",
        xaxis_title="Sentiment",
        yaxis_title="NPS Type",
        height=300
    )
    
    return row_fig, col_fig, total_fig


def create_stacked_bar_charts(crosstab: pd.DataFrame) -> Tuple[go.Figure, go.Figure]:
    """Create stacked bar charts for better proportion visualization."""
    
    # Normalize by rows (NPS Type)
    row_normalized = crosstab.div(crosstab.sum(axis=1), axis=0) * 100
    
    # Normalize by columns (Sentiment)
    col_normalized = crosstab.div(crosstab.sum(axis=0), axis=1) * 100
    
    # Row-normalized stacked bar chart
    fig1 = go.Figure()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    for i, sentiment in enumerate(crosstab.columns):
        fig1.add_trace(go.Bar(
            name=sentiment,
            x=row_normalized.index,
            y=row_normalized[sentiment],
            marker_color=colors[i % len(colors)],
            text=row_normalized[sentiment].round(1),
            texttemplate='%{text}%',
            textposition='inside'
        ))
    
    fig1.update_layout(
        title="Sentiment Distribution within each NPS Type",
        xaxis_title="NPS Type",
        yaxis_title="Percentage",
        barmode='stack',
        height=400,
        showlegend=True
    )
    
    # Column-normalized stacked bar chart
    fig2 = go.Figure()
    
    for i, nps_type in enumerate(crosstab.index):
        fig2.add_trace(go.Bar(
            name=nps_type,
            x=col_normalized.columns,
            y=col_normalized.loc[nps_type],
            marker_color=colors[i % len(colors)],
            text=col_normalized.loc[nps_type].round(1),
            texttemplate='%{text}%',
            textposition='inside'
        ))
    
    fig2.update_layout(
        title="NPS Type Distribution within each Sentiment",
        xaxis_title="Sentiment",
        yaxis_title="Percentage",
        barmode='stack',
        height=400,
        showlegend=True
    )
    
    return fig1, fig2


def create_correlation_insights(stats: Dict, crosstab: pd.DataFrame) -> str:
    """Generate textual insights about the correlation."""
    
    insights = []
    
    # Statistical significance
    if stats['p_value'] < 0.001:
        significance = "highly significant (p < 0.001)"
    elif stats['p_value'] < 0.01:
        significance = "very significant (p < 0.01)"
    elif stats['p_value'] < 0.05:
        significance = "significant (p < 0.05)"
    else:
        significance = "not statistically significant (p ≥ 0.05)"
    
    insights.append(f"🔬 **Statistical Significance**: The relationship is {significance}")
    
    # Effect size interpretation
    if stats['cramers_v'] < 0.1:
        effect_size = "negligible"
    elif stats['cramers_v'] < 0.3:
        effect_size = "small"
    elif stats['cramers_v'] < 0.5:
        effect_size = "medium"
    else:
        effect_size = "large"
    
    insights.append(f"📊 **Effect Size**: Cramér's V = {stats['cramers_v']:.3f} ({effect_size} association)")
    
    # Agreement analysis
    nps_sentiment_map = {"Promoter": "POSITIVE", "Passive": "NEUTRAL", "Detractor": "NEGATIVE"}
    
    # Calculate agreement for each category
    agreements = []
    for nps_type in crosstab.index:
        if nps_type in nps_sentiment_map:
            expected_sentiment = nps_sentiment_map[nps_type]
            if expected_sentiment in crosstab.columns:
                total_nps = crosstab.loc[nps_type].sum()
                matching = crosstab.loc[nps_type, expected_sentiment]
                agreement_pct = (matching / total_nps) * 100 if total_nps > 0 else 0
                agreements.append(f"  - {nps_type} → {expected_sentiment}: {agreement_pct:.1f}%")
    
    if agreements:
        insights.append("🎯 **Expected vs Actual Agreement**:")
        insights.extend(agreements)
    
    # Strongest associations
    row_pct = stats['row_percentages']
    strongest_associations = []
    
    for nps_type in row_pct.index:
        max_sentiment = row_pct.loc[nps_type].idxmax()
        max_pct = row_pct.loc[nps_type].max()
        strongest_associations.append(f"  - {nps_type}: {max_pct:.1f}% → {max_sentiment}")
    
    insights.append("🔗 **Strongest Associations**:")
    insights.extend(strongest_associations)
    
    return "\n".join(insights)


def enhanced_crosstab_analysis(df: pd.DataFrame) -> None:
    """
    Create comprehensive cross-tabulation analysis with enhanced visualizations.
    """
    st.markdown("## 📊 Enhanced Cross-Tabulation Analysis")
    st.markdown("*Deep dive into NPS vs Sentiment correlations with advanced statistical insights*")
    
    # Ensure required columns exist
    if 'NPS Type' not in df.columns or 'Sentiment' not in df.columns:
        st.error("Required columns 'NPS Type' and 'Sentiment' not found in dataset.")
        return
    
    # Create cross-tabulation
    crosstab = pd.crosstab(df["NPS Type"], df["Sentiment"])
    
    # Calculate statistical measures
    stats = calculate_statistical_measures(crosstab)
    
    if not stats:
        return
    
    # Create tabs for different analyses
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Basic Cross-Tab", 
        "🔥 Interactive Heatmaps", 
        "📊 Percentage Analysis",
        "📈 Stacked Charts",
        "🧠 Statistical Insights"
    ])
    
    with tab1:
        st.subheader("📋 Cross-Tabulation Table")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Enhanced table with styling
            styled_crosstab = crosstab.style.background_gradient(cmap='YlOrRd', axis=None)
            st.dataframe(styled_crosstab, use_container_width=True)
            
            # Add marginal totals
            crosstab_with_totals = crosstab.copy()
            crosstab_with_totals['Total'] = crosstab_with_totals.sum(axis=1)
            crosstab_with_totals.loc['Total'] = crosstab_with_totals.sum(axis=0)
            
            st.markdown("**With Marginal Totals:**")
            st.dataframe(crosstab_with_totals, use_container_width=True)
        
        with col2:
            st.markdown("**Quick Stats:**")
            st.metric("Total Observations", stats['sample_size'])
            st.metric("Chi-square", f"{stats['chi2']:.2f}")
            st.metric("p-value", f"{stats['p_value']:.4f}")
            st.metric("Cramér's V", f"{stats['cramers_v']:.3f}")
    
    with tab2:
        st.subheader("🔥 Interactive Heatmaps")
        
        # Main heatmap
        main_heatmap = create_enhanced_heatmap(crosstab)
        st.plotly_chart(main_heatmap, use_container_width=True)
        
        # Alternative Altair heatmap for comparison
        st.markdown("**Alternative Visualization (Altair):**")
        ct_melted = crosstab.reset_index().melt(id_vars="NPS Type", var_name="Sentiment", value_name="Count")
        
        heatmap_alt = alt.Chart(ct_melted).mark_rect().encode(
            x=alt.X('Sentiment:N', title='Sentiment Analysis Result'),
            y=alt.Y('NPS Type:N', title='NPS Classification'),
            color=alt.Color('Count:Q', 
                          scale=alt.Scale(scheme='viridis'),
                          legend=alt.Legend(title="Count")),
            tooltip=['NPS Type:N', 'Sentiment:N', 'Count:Q'],
            stroke=alt.value('white'),
            strokeWidth=alt.value(2)
        ).properties(
            title="NPS vs Sentiment Cross-Tabulation Heatmap",
            width=500,
            height=300
        ).resolve_scale(
            color='independent'
        )
        
        st.altair_chart(heatmap_alt, use_container_width=True)
    
    with tab3:
        st.subheader("📊 Percentage Analysis")
        
        # Create percentage heatmaps
        row_fig, col_fig, total_fig = create_percentage_heatmaps(stats)
        
        st.markdown("**Row Percentages** - *What percentage of each NPS type falls into each sentiment category?*")
        st.plotly_chart(row_fig, use_container_width=True)
        
        st.markdown("**Column Percentages** - *What percentage of each sentiment category comes from each NPS type?*")
        st.plotly_chart(col_fig, use_container_width=True)
        
        st.markdown("**Total Percentages** - *What percentage of the entire dataset does each cell represent?*")
        st.plotly_chart(total_fig, use_container_width=True)
    
    with tab4:
        st.subheader("📈 Stacked Bar Charts")
        
        # Create stacked bar charts
        fig1, fig2 = create_stacked_bar_charts(crosstab)
        
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Additional insights
        st.markdown("### 💡 Chart Interpretation")
        st.info("""
        **Top Chart**: Shows how sentiment is distributed within each NPS category.
        - Perfect alignment would show 100% positive for Promoters, 100% neutral for Passives, etc.
        
        **Bottom Chart**: Shows how NPS types are distributed within each sentiment category.
        - Helps identify which NPS types contribute most to each sentiment.
        """)
    
    with tab5:
        st.subheader("🧠 Statistical Insights & Interpretation")
        
        # Generate and display insights
        insights_text = create_correlation_insights(stats, crosstab)
        st.markdown(insights_text)
        
        # Additional statistical details
        with st.expander("📈 Advanced Statistical Details"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Expected Frequencies (under independence):**")
                expected_df = pd.DataFrame(
                    stats['expected_frequencies'], 
                    index=crosstab.index, 
                    columns=crosstab.columns
                ).round(2)
                st.dataframe(expected_df)
            
            with col2:
                st.markdown("**Residuals (Observed - Expected):**")
                residuals = crosstab - expected_df
                st.dataframe(residuals.round(2))
        
        # Recommendations
        st.markdown("### 🎯 Actionable Recommendations")
        
        if stats['cramers_v'] > 0.3:
            st.success("✅ **Strong correlation detected!** Your NPS and sentiment analysis are well-aligned.")
        elif stats['cramers_v'] > 0.1:
            st.warning("⚠️ **Moderate correlation.** Consider investigating discrepancies between NPS and sentiment.")
        else:
            st.error("❌ **Weak correlation.** NPS and sentiment analysis may be measuring different aspects.")
        
        # Export functionality
        st.markdown("### 💾 Export Analysis")
        if st.button("📥 Download Cross-Tab Analysis Report", key="crosstab_export"):
            report_data = {
                "crosstab": crosstab.to_dict(),
                "statistics": {k: v for k, v in stats.items() if not isinstance(v, pd.DataFrame)},
                "insights": insights_text,
                "sample_size": stats['sample_size']
            }
            
            st.download_button(
                label="Download JSON Report",
                data=pd.Series(report_data).to_json(),
                file_name=f"crosstab_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )


# Module exports
__all__ = ['enhanced_crosstab_analysis']
