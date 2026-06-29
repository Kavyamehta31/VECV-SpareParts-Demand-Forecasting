import streamlit as st
import pandas as pd
import plotly.express as px
with open("app/assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)
st.sidebar.image("app/assets/vecv_logo.png", width=180)
st.sidebar.caption("Enterprise Spare Parts Platform")

st.sidebar.markdown("---")
st.title("📊 Executive Dashboard")
st.markdown("### Enterprise Spare Parts Demand Forecasting & Inventory Optimization Platform")
st.markdown("---")
# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

profile_df = pd.read_csv(
    "outputs/final/demand_profile.csv"
)

inventory_df = pd.read_csv(
    "outputs/final/inventory_optimization.csv"
)

recommendation_df = pd.read_csv(
    "outputs/final/recommendations.csv"
)

forecast_df = pd.read_csv(
    "outputs/final/best_model_by_part.csv"
)

abc_df = pd.read_csv(
    "outputs/final/abc_analysis.csv"
)
# ----------------------------------------------------
# EXECUTIVE KPIs
# ----------------------------------------------------

total_parts = len(profile_df)

total_warehouses = profile_df["Warehouse"].nunique()

forecast_accuracy = forecast_df["Accuracy"].mean()

high_risk_parts = (
    inventory_df["Inventory_Risk"] == "High Risk"
).sum()

dead_stock = (
    profile_df["Demand_Class"] == "Dead Stock"
).sum()

recommendations = len(recommendation_df)
c1, c2, c3 = st.columns(3)

c4, c5, c6 = st.columns(3)

c1.metric(
    "Total Parts",
    f"{total_parts:,}"
)

c2.metric(
    "Warehouses",
    total_warehouses
)

c3.metric(
    "Forecast Accuracy",
    f"{forecast_accuracy:.1f}%"
)

c4.metric(
    "High Risk Parts",
    f"{high_risk_parts:,}"
)

c5.metric(
    "Dead Stock",
    f"{dead_stock:,}"
)

c6.metric(
    "Recommendations",
    f"{recommendations:,}"
)
st.markdown("---")

left, right = st.columns(2)

with left:

    demand_counts = (
        profile_df["Demand_Class"]
        .value_counts()
        .reset_index()
    )

    demand_counts.columns = [
        "Demand Class",
        "Count"
    ]

    fig = px.pie(
        demand_counts,
        names="Demand Class",
        values="Count",
        title="Demand Profile Distribution",
        hole=0.45
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

with right:

    risk_counts = (
        inventory_df["Inventory_Risk"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "Risk",
        "Count"
    ]

    fig = px.bar(
        risk_counts,
        x="Risk",
        y="Count",
        color="Risk",
        title="Inventory Risk Distribution",
        text="Count"
    )

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

abc = (
    abc_df["ABC_Class"]
    .value_counts()
    .reset_index()
)

abc.columns = [
    "ABC Class",
    "Count"
]

fig = px.bar(
    abc,
    x="ABC Class",
    y="Count",
    color="ABC Class",
    text="Count",
    title="ABC Inventory Classification"
)

fig.update_layout(height=450)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

warehouse_summary = (
    profile_df
    .groupby("Warehouse")
    .agg(
        Total_Parts=("Part_No", "count"),
        Total_Demand=("Total_Demand", "sum")
    )
    .reset_index()
)

# Create a text column for plotting
warehouse_summary["Warehouse_Name"] = warehouse_summary["Warehouse"].astype(str)

fig = px.bar(
    warehouse_summary,
    x="Warehouse_Name",
    y="Total_Demand",
    color="Warehouse_Name",
    text="Total_Demand",
    title="Warehouse-wise Total Demand"
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    height=500,
    xaxis_title="Warehouse",
    yaxis_title="Total Demand",
    showlegend=False,
    xaxis=dict(type="category")
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

model_counts = (
    forecast_df["Best_Model"]
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
    hole=0.45,
    title="Forecast Model Distribution"
)

fig.update_layout(height=450)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

recommendation_counts = (
    recommendation_df["Recommendation"]
    .value_counts()
    .reset_index()
)

recommendation_counts.columns = [
    "Recommendation",
    "Count"
]

fig = px.bar(
    recommendation_counts,
    x="Count",
    y="Recommendation",
    orientation="h",
    color="Count",
    text="Count",
    title="Recommendation Summary"
)

fig.update_layout(
    height=500,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("---")

best_warehouse = warehouse_summary.loc[
    warehouse_summary["Total_Demand"].idxmax(),
    "Warehouse_Name"
]

best_model = forecast_df["Best_Model"].mode()[0]

highest_risk = inventory_df["Inventory_Risk"].value_counts().idxmax()

st.subheader("📋 Executive Summary")

st.success(f"""
### Key Business Insights

- Total Spare Parts Analysed: **{total_parts:,}**
- Warehouses Covered: **{total_warehouses}**
- Average Forecast Accuracy: **{forecast_accuracy:.2f}%**
- Highest Demand Warehouse: **{best_warehouse}**
- Most Frequently Selected Forecasting Model: **{best_model}**
- High Risk Parts: **{high_risk_parts:,}**
- Dead Stock Parts: **{dead_stock:,}**
- Total Recommendations Generated: **{recommendations:,}**
- Most Common Inventory Risk: **{highest_risk}**
""")