import altair as alt
import pandas as pd

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