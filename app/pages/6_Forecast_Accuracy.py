import streamlit as st
import pandas as pd
import plotly.express as px
with open("app/assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
st.set_page_config(
    page_title="Forecast Accuracy",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Forecast Accuracy Dashboard")

st.markdown("---")
best_model_df = pd.read_csv(
    "outputs/final/best_model_by_part.csv"
)
total_parts = len(best_model_df)

avg_accuracy = best_model_df["Accuracy"].mean()

best_accuracy = best_model_df["Accuracy"].max()

median_mape = best_model_df["MAPE"].median()

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Parts",
    f"{total_parts:,}"
)

col2.metric(
    "Average Accuracy",
    f"{avg_accuracy:.2f}%"
)

col3.metric(
    "Best Accuracy",
    f"{best_accuracy:.2f}%"
)

col4.metric(
    "Median MAPE",
    f"{median_mape:.2f}%"
)

st.markdown("---")
# --------------------------------------------------
# MODEL DISTRIBUTION & ACCURACY DISTRIBUTION
# --------------------------------------------------

left, right = st.columns(2)

# ---------------------------
# Best Model Distribution
# ---------------------------

with left:

    model_counts = (
        best_model_df["Best_Model"]
        .value_counts()
        .reset_index()
    )

    model_counts.columns = [
        "Model",
        "Count"
    ]

    fig = px.pie(
        model_counts,
        names="Model",
        values="Count",
        title="Best Forecasting Model Distribution"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------
# Accuracy Distribution
# ---------------------------

with right:

    fig = px.histogram(
        best_model_df,
        x="Accuracy",
        nbins=20,
        title="Forecast Accuracy Distribution"
    )

    fig.update_layout(
        height=500,
        xaxis_title="Accuracy (%)",
        yaxis_title="Number of Parts"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")
# --------------------------------------------------
# TOP & LOWEST ACCURACY PARTS
# --------------------------------------------------

left, right = st.columns(2)

# -----------------------------
# Lowest 10 Parts
# -----------------------------

with right:

    st.subheader("⚠ Highest Forecast Error")

    low_parts = (
        best_model_df
        .sort_values("MAPE", ascending=False)
        .head(10)
    )

    fig = px.bar(
        low_parts,
        x="MAPE",
        y="Part_No",
        orientation="h",
        color="MAPE",
        text="MAPE",
        title="Highest Forecast Error (MAPE)"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        height=500,
        yaxis=dict(categoryorder="total ascending"),
        xaxis_title="MAPE (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# --------------------------------------------------
# ERROR METRICS ANALYSIS
# --------------------------------------------------

st.subheader("📊 Forecast Error Metrics")

left, right = st.columns(2)

# -----------------------------
# MAE
# -----------------------------

with left:

    fig = px.box(
        best_model_df,
        y="MAE",
        points="outliers",
        title="MAE Distribution"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# RMSE
# -----------------------------

with right:

    fig = px.box(
        best_model_df,
        y="RMSE",
        points="outliers",
        title="RMSE Distribution"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# -----------------------------
# MAPE Distribution
# -----------------------------

fig = px.histogram(
    best_model_df,
    x="MAPE",
    nbins=20,
    title="MAPE Distribution"
)

fig.update_layout(
    height=450,
    xaxis_title="MAPE (%)",
    yaxis_title="Number of Parts"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")
# --------------------------------------------------
# EXECUTIVE INSIGHTS
# --------------------------------------------------

best_part = best_model_df.loc[
    best_model_df["Accuracy"].idxmax()
]

worst_part = best_model_df.loc[
    best_model_df["Accuracy"].idxmin()
]

st.subheader("📋 Executive Insights")

st.success(
    f"""
### Forecast Performance Summary

✔ Total Parts Evaluated: **{total_parts}**

✔ Average Forecast Accuracy: **{avg_accuracy:.2f}%**

✔ Best Performing Part: **{best_part['Part_No']}**
({best_part['Accuracy']:.2f}% Accuracy)

✔ Lowest Performing Part: **{worst_part['Part_No']}**
({worst_part['Accuracy']:.2f}% Accuracy)

✔ Median MAPE: **{median_mape:.2f}%**
"""
)

st.info(
    """
### Recommendations

• Review parts with consistently low forecasting accuracy.

• Investigate intermittent demand patterns for poorly performing parts.

• Re-evaluate model selection periodically as new demand data becomes available.

• Continue monitoring forecast error metrics (MAE, RMSE, and MAPE) to improve planning accuracy.
"""
)