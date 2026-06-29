import streamlit as st
import pandas as pd
import plotly.express as px
with open("app/assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Forecasting",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📈 Demand Forecasting Dashboard")

st.markdown("---")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

forecast_df = pd.read_csv(
    "outputs/final/top_a_parts.csv"
)

forecast_df["Date"] = pd.to_datetime(
    forecast_df["Date"],
    format="%Y-%m"
)

# --------------------------------------------------
# LOAD MODEL RESULTS
# --------------------------------------------------

best_model_df = pd.read_csv(
    "outputs/final/best_model_by_part.csv"
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header(
    "Forecast Settings"
)

selected_part = st.sidebar.selectbox(
    "Select Part Number",
    sorted(
        forecast_df["Part_No"].unique()
    )
)
forecast_horizon = st.sidebar.selectbox(
    "Forecast Horizon",
    [1, 3, 6, 12]
)
forecast_results = pd.read_csv(
    f"outputs/final/forecast_results_{forecast_horizon}.csv"
)
# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

part_df = forecast_df[
    forecast_df["Part_No"] == selected_part
].copy()

part_df = part_df.sort_values(
    "Date"
)

# --------------------------------------------------
# KPIs
# --------------------------------------------------

# --------------------------------------------------
# PART MODEL DETAILS
# --------------------------------------------------

part_model = best_model_df[
    best_model_df["Part_No"] == selected_part
].iloc[0]

best_model = part_model["Best_Model"]

best_accuracy = part_model["Accuracy"]

latest_demand = part_df["Demand"].iloc[-1]

total_demand = part_df["Demand"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Selected Part",
    selected_part
)

col2.metric(
    "Best Model",
    best_model
)

col3.metric(
    "Forecast Accuracy",
    f"{best_accuracy:.2f}%"
)

col4.metric(
    "Total Demand",
    f"{total_demand:,.0f}"
)
col5.metric(
    "Forecast Horizon",
    f"{forecast_horizon} Month{'s' if forecast_horizon > 1 else ''}"
)
st.markdown("---")
# --------------------------------------------------
# FORECAST RESULTS
# --------------------------------------------------

# --------------------------------------------------
# NEXT 3 MONTH FORECAST
# --------------------------------------------------

part_forecast = forecast_results[
    forecast_results["Part_No"] == selected_part
].copy()

# Get last historical month
last_month = part_df["Date"].max()

future_months = pd.date_range(
    start=last_month + pd.DateOffset(months=1),
    periods=len(part_forecast),
    freq="MS"
)

# Create a copy ONLY for displaying
display_forecast = part_forecast.copy()

display_forecast["Forecast Month"] = future_months.strftime("%b %Y")

display_forecast["Forecast Demand"] = display_forecast["Forecast_Value"]

st.subheader(
    f"📅 Next {forecast_horizon}-Month Forecast"
)

st.dataframe(
    display_forecast[
        [
            "Forecast Month",
            "Forecast Demand"
        ]
    ],
    width="stretch",
    hide_index=True
)

# --------------------------------------------------
# HISTORICAL + FORECAST CHART
# --------------------------------------------------

st.subheader("📈 Historical Demand & Future Forecast")

# Historical demand
history = part_df[["Date", "Demand"]].copy()
history.columns = ["Month", "Value"]
history["Type"] = "Historical"

# Last historical date
last_date = history["Month"].max()

# Forecast values
future = part_forecast.copy()

future["Month"] = pd.date_range(
    start=last_date + pd.DateOffset(months=1),
    periods=len(future),
    freq="MS"
)

future["Value"] = future["Forecast_Value"]
future["Type"] = "Forecast"

future = future[
    [
        "Month",
        "Value",
        "Type"
    ]
]

# Combine
plot_df = pd.concat(
    [
        history,
        future
    ],
    ignore_index=True
)

fig = px.line(
    plot_df,
    x="Month",
    y="Value",
    color="Type",
    markers=True,
    title=f"Demand Forecast for {selected_part}",
    color_discrete_map={
        "Historical": "#4C78A8",
        "Forecast": "#F58518"
    }
)

# Historical line
fig.data[0].update(
    line=dict(width=3),
    marker=dict(size=6)
)

# Forecast line
fig.data[1].update(
    line=dict(
        width=4,
        dash="dash"
    ),
    marker=dict(size=10)
)

# Vertical separator
fig.add_vline(
    x=last_date,
    line_width=2,
    line_dash="dot",
    line_color="red"
)

# Annotation
fig.add_annotation(
    x=last_date,
    y=max(plot_df["Value"]),
    text="Forecast Starts",
    showarrow=True,
    arrowhead=2,
    yshift=25
)

fig.update_layout(
    height=650,
    xaxis_title="Month",
    yaxis_title="Demand",
    legend_title="Data",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# --------------------------------------------------
# PART DETAILS
# --------------------------------------------------

st.subheader(
    "Recent Demand Records"
)

st.dataframe(
    part_df.tail(12),
    use_container_width=True
)

# --------------------------------------------------
# MODEL COMPARISON
# --------------------------------------------------

# --------------------------------------------------
# MODEL PERFORMANCE
# --------------------------------------------------

st.subheader("📊 Model Performance")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Best Model",
    part_model["Best_Model"]
)

c2.metric(
    "Accuracy",
    f"{part_model['Accuracy']:.2f}%"
)

c3.metric(
    "MAE",
    f"{part_model['MAE']:.2f}"
)

c4.metric(
    "RMSE",
    f"{part_model['RMSE']:.2f}"
)

c5.metric(
    "MAPE",
    f"{part_model['MAPE']:.2f}%"
)

# --------------------------------------------------
# DEMAND STATISTICS
# --------------------------------------------------

st.subheader(
    "Demand Statistics"
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Demand",
    f"{part_df['Demand'].mean():.2f}"
)

col2.metric(
    "Maximum Demand",
    f"{part_df['Demand'].max():.0f}"
)

col3.metric(
    "Latest Demand",
    f"{latest_demand:.0f}"
)

# --------------------------------------------------
# FORECAST INSIGHTS
# --------------------------------------------------

st.subheader(
    "Forecast Insights"
)

st.subheader("📋 Executive Forecast Summary")

trend = "Increasing"

if len(part_forecast) >= 2:
    if part_forecast["Forecast_Value"].iloc[-1] < part_forecast["Forecast_Value"].iloc[0]:
        trend = "Decreasing"
    elif part_forecast["Forecast_Value"].iloc[-1] == part_forecast["Forecast_Value"].iloc[0]:
        trend = "Stable"

st.success(
    f"""
### Executive Summary

**Selected Part:** {selected_part}

**Best Forecasting Model:** {best_model}

**Forecast Accuracy:** {best_accuracy:.2f}%

**Demand Trend:** {trend}

**Forecast Horizon:** 3 Months

### Recommendation

Maintain inventory according to the projected demand while continuously monitoring monthly consumption. Review safety stock and reorder point before the next replenishment cycle.
"""
)