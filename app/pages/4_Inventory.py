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
    page_title="Inventory Optimization",
    page_icon="📦",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

inventory_df = pd.read_csv(
    "app/data/inventory_optimization.csv"
)

recommendation_df = pd.read_csv(
    "app/data/recommendations.csv"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📦 Inventory Optimization Dashboard")

st.markdown("---")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Filters")

warehouse = st.sidebar.selectbox(
    "Warehouse",
    ["All"] + sorted(
        inventory_df["Warehouse"].astype(str).unique().tolist()
    )
)

risk = st.sidebar.selectbox(
    "Inventory Risk",
    ["All"] + sorted(
        inventory_df["Inventory_Risk"].unique().tolist()
    )
)

demand = st.sidebar.selectbox(
    "Demand Class",
    ["All"] + sorted(
        inventory_df["Demand_Class"].unique().tolist()
    )
)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = inventory_df.copy()

if warehouse != "All":
    filtered_df = filtered_df[
        filtered_df["Warehouse"].astype(str) == warehouse
    ]

if risk != "All":
    filtered_df = filtered_df[
        filtered_df["Inventory_Risk"] == risk
    ]

if demand != "All":
    filtered_df = filtered_df[
        filtered_df["Demand_Class"] == demand
    ]

# --------------------------------------------------
# KPIs
# --------------------------------------------------

total_parts = len(filtered_df)

high_risk = len(
    filtered_df[
        filtered_df["Inventory_Risk"] == "High Risk"
    ]
)

dead_inventory = len(
    filtered_df[
        filtered_df["Inventory_Risk"] == "Dead Inventory"
    ]
)

avg_safety_stock = filtered_df[
    "Safety_Stock"
].mean()

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

avg_reorder_point = filtered_df["Reorder_Point"].mean()

total_warehouses = filtered_df["Warehouse"].nunique()

col1, col2, col3 = st.columns(3)

col4, col5, col6 = st.columns(3)

col1.metric(
    "Total Parts",
    f"{total_parts:,}"
)

col2.metric(
    "High Risk Parts",
    f"{high_risk:,}"
)

col3.metric(
    "Dead Inventory",
    f"{dead_inventory:,}"
)

col4.metric(
    "Avg Safety Stock",
    f"{avg_safety_stock:.2f}"
)

col5.metric(
    "Avg Reorder Point",
    f"{avg_reorder_point:.2f}"
)

col6.metric(
    "Warehouses",
    total_warehouses
)

st.markdown("---")
# --------------------------------------------------
# CHARTS
# --------------------------------------------------

left, right = st.columns(2)

# ------------------------
# Inventory Risk
# ------------------------

with left:

    risk_df = (
        filtered_df["Inventory_Risk"]
        .value_counts()
        .reset_index()
    )

    risk_df.columns = [
        "Inventory_Risk",
        "Count"
    ]

    fig = px.pie(
        risk_df,
        names="Inventory_Risk",
        values="Count",
        title="Inventory Risk Distribution"
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ------------------------
# Demand Class
# ------------------------

with right:

    demand_df = (
        filtered_df["Demand_Class"]
        .value_counts()
        .reset_index()
    )

    demand_df.columns = [
        "Demand_Class",
        "Count"
    ]

    fig = px.bar(
        demand_df,
        x="Demand_Class",
        y="Count",
        color="Demand_Class",
        text_auto=True,
        title="Demand Class Distribution"
    )

    fig.update_layout(
        height=450,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# --------------------------------------------------
# SAFETY STOCK & REORDER POINT
# --------------------------------------------------

left, right = st.columns(2)

# ------------------------
# Safety Stock Distribution
# ------------------------

with left:

    fig = px.histogram(
        filtered_df,
        x="Safety_Stock",
        nbins=40,
        title="Safety Stock Distribution"
    )

    fig.update_layout(
        height=450,
        xaxis_title="Safety Stock",
        yaxis_title="Number of Parts"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="safety_stock_hist"
    )

# ------------------------
# Reorder Point Distribution
# ------------------------

with right:

    fig = px.histogram(
        filtered_df,
        x="Reorder_Point",
        nbins=40,
        title="Reorder Point Distribution"
    )

    fig.update_layout(
        height=450,
        xaxis_title="Reorder Point",
        yaxis_title="Number of Parts"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="reorder_point_hist"
    )

st.markdown("---")
# --------------------------------------------------
# WAREHOUSE-WISE HIGH RISK ANALYSIS
# --------------------------------------------------

st.subheader("🏭 Warehouse-wise High Risk Parts")

high_risk_df = (
    filtered_df[
        filtered_df["Inventory_Risk"] == "High Risk"
    ]
    .groupby("Warehouse")
    .size()
    .reset_index(name="High_Risk_Count")
)

fig = px.bar(
    high_risk_df,
    x="Warehouse",
    y="High_Risk_Count",
    color="Warehouse",
    text_auto=True,
    title="High Risk Parts by Warehouse"
)

fig.update_layout(
    height=500,
    showlegend=False,
    xaxis_title="Warehouse",
    yaxis_title="Number of High Risk Parts"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="warehouse_high_risk"
)

st.markdown("---")
# --------------------------------------------------
# TOP 10 REORDER POINTS
# --------------------------------------------------

st.markdown("---")

st.subheader("📦 Top 10 Parts with Highest Reorder Point")

top_reorder = (
    filtered_df
    .sort_values(
        by="Reorder_Point",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top_reorder,
    x="Part_No",
    y="Reorder_Point",
    color="Inventory_Risk",
    text_auto=".2f",
    title="Top 10 Parts by Reorder Point"
)

fig.update_layout(
    height=500,
    xaxis_title="Part Number",
    yaxis_title="Reorder Point"
)

st.plotly_chart(
    fig,
    use_container_width=True,
    key="top_reorder_parts"
)
# --------------------------------------------------
# WAREHOUSE INVENTORY SUMMARY
# --------------------------------------------------

st.markdown("---")

st.subheader("🏭 Warehouse Inventory Summary")

warehouse_summary = (
    filtered_df
    .groupby("Warehouse")
    .agg(
        Total_Parts=("Part_No", "count"),
        Avg_Safety_Stock=("Safety_Stock", "mean"),
        Avg_Reorder_Point=("Reorder_Point", "mean"),
        High_Risk_Parts=(
            "Inventory_Risk",
            lambda x: (x == "High Risk").sum()
        )
    )
    .reset_index()
)

st.dataframe(
    warehouse_summary,
    use_container_width=True,
    hide_index=True
) 
# --------------------------------------------------
# EXECUTIVE INVENTORY SUMMARY
# --------------------------------------------------

st.markdown("---")

st.subheader("📋 Executive Inventory Summary")

st.success(
    f"""
### Inventory Overview

• Total Parts Analysed: **{total_parts:,}**

• Warehouses Covered: **{total_warehouses}**

• High Risk Parts: **{high_risk:,}**

• Dead Inventory: **{dead_inventory:,}**

• Average Safety Stock: **{avg_safety_stock:.2f}**

• Average Reorder Point: **{avg_reorder_point:.2f}**

### Recommended Actions

✅ Prioritize replenishment of High Risk inventory.

✅ Review Dead Inventory for disposal, transfer, or demand reassessment.

✅ Monitor warehouse-level inventory trends regularly.

✅ Recalculate Safety Stock and Reorder Point periodically based on forecasted demand.
"""
)
# --------------------------
# ------------------------
# DATA PREVIEW
# --------------------------------------------------

st.subheader("🚨 Top High Risk Parts")

top_parts = (
    filtered_df
    .sort_values(
        by="Reorder_Point",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_parts[
        [
            "Warehouse",
            "Part_No",
            "Demand_Class",
            "Safety_Stock",
            "Reorder_Point",
            "Inventory_Risk"
        ]
    ],
    use_container_width=True
)