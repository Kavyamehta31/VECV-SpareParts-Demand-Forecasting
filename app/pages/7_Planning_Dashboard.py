import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Planning Dashboard",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Planning Dashboard")
st.markdown("---")

# ------------------------------------
# LOAD DATA
# ------------------------------------

profile_df = pd.read_csv(
    "outputs/final/demand_profile.csv"
)

inventory_df = pd.read_csv(
    "outputs/final/inventory_optimization.csv"
)

recommendation_df = pd.read_csv(
    "outputs/final/recommendations.csv"
)

abc_df = pd.read_csv(
    "outputs/final/abc_analysis.csv"
)

# ------------------------------------
# MERGE DATA
# ------------------------------------

planning_df = profile_df.merge(

    inventory_df[
        [
            "Warehouse",
            "Part_No",
            "Inventory_Risk",
            "Safety_Stock",
            "Reorder_Point",
            "Inventory_Coverage"
        ]
    ],

    on=["Warehouse", "Part_No"],
    how="left"

)

planning_df = planning_df.merge(

    recommendation_df[
        [
            "Warehouse",
            "Part_No",
            "Recommendation"
        ]
    ],

    on=["Warehouse", "Part_No"],
    how="left"

)
# Merge ABC Classification
planning_df = planning_df.merge(

    abc_df[
        [
            "Warehouse",
            "Part_No",
            "ABC_Class"
        ]
    ],

    on=["Warehouse", "Part_No"],
    how="left"

)
st.write(planning_df.shape)
# ------------------------------------
# FILTERS
# ------------------------------------

st.sidebar.header("Planning Filters")

warehouse = st.sidebar.selectbox(

    "Warehouse",

    ["All"] +
    sorted(
        planning_df["Warehouse"]
        .astype(str)
        .unique()
        .tolist()
    )

)

abc = st.sidebar.selectbox(

    "ABC Class",

    ["All"] +
    sorted(
        planning_df["ABC_Class"]
        .dropna()
        .unique()
        .tolist()
    )

)

demand = st.sidebar.selectbox(

    "Demand Class",

    ["All"] +
    sorted(
        planning_df["Demand_Class"]
        .dropna()
        .unique()
        .tolist()
    )

)

risk = st.sidebar.selectbox(

    "Inventory Risk",

    ["All"] +
    sorted(
        planning_df["Inventory_Risk"]
        .dropna()
        .unique()
        .tolist()
    )

)

# ------------------------------------
# APPLY FILTERS
# ------------------------------------

filtered_df = planning_df.copy()

if warehouse != "All":

    filtered_df = filtered_df[
        filtered_df["Warehouse"].astype(str) == warehouse
    ]

if abc != "All":

    filtered_df = filtered_df[
        filtered_df["ABC_Class"] == abc
    ]

if demand != "All":

    filtered_df = filtered_df[
        filtered_df["Demand_Class"] == demand
    ]

if risk != "All":

    filtered_df = filtered_df[
        filtered_df["Inventory_Risk"] == risk
    ]
# ------------------------------------
# PLANNING KPIs
# ------------------------------------

st.markdown("## 📊 Planning Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Parts",
    len(filtered_df)
)

col2.metric(
    "Total Demand",
    f"{filtered_df['Total_Demand'].sum():,.0f}"
)

col3.metric(
    "Avg Safety Stock",
    f"{filtered_df['Safety_Stock'].mean():.2f}"
)

col4.metric(
    "Avg Inventory Coverage",
    f"{filtered_df['Inventory_Coverage'].mean():.2f} Months"
)

st.markdown("---")
# ------------------------------------
# PARTS PLANNING TABLE
# ------------------------------------


planning_table = filtered_df[
    [
        "Warehouse",
        "Part_No",
        "Demand_Class",
        "ABC_Class",
        "Inventory_Risk",
        "Safety_Stock",
        "Reorder_Point",
        "Inventory_Coverage",
        "Recommendation"
    ]
].sort_values(
    ["Warehouse", "Inventory_Risk"]
)


st.subheader("📋 Parts Planning Table")

rows = st.selectbox(
    "Rows to display",
    [25, 50, 100, 250, 500],
    index=2
)

search = st.text_input(
    "Search Part Number"
)

if search:

    planning_table = planning_table[
        planning_table["Part_No"]
        .astype(str)
        .str.contains(search, case=False)
    ]

st.caption(
    f"Showing {min(rows, len(planning_table))} of {len(planning_table):,} matching parts"
)

st.dataframe(
    planning_table.head(rows),
    use_container_width=True,
    hide_index=True
)
st.markdown("---")
st.subheader("📊 Demand Class Distribution")

fig = px.pie(
    filtered_df,
    names="Demand_Class",
    title="Demand Class Distribution",
    hole=0.45
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
st.subheader("📦 ABC Classification")

abc_summary = (
    filtered_df
    .groupby("ABC_Class")
    .size()
    .reset_index(name="Count")
)

fig = px.bar(
    abc_summary,
    x="ABC_Class",
    y="Count",
    color="ABC_Class",
    text="Count",
    title="ABC Inventory Classification"
)

fig.update_traces(textposition="outside")

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
st.subheader("⚠ Inventory Risk Distribution")

risk_summary = (
    filtered_df
    .groupby("Inventory_Risk")
    .size()
    .reset_index(name="Count")
)

fig = px.bar(
    risk_summary,
    x="Inventory_Risk",
    y="Count",
    color="Inventory_Risk",
    text="Count"
)

fig.update_traces(textposition="outside")

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
st.subheader("🛡 Highest Safety Stock Parts")

top_parts = (
    filtered_df
    .nlargest(15, "Safety_Stock")
)

fig = px.bar(
    top_parts,
    x="Safety_Stock",
    y="Part_No",
    orientation="h",
    color="Safety_Stock",
    text="Safety_Stock"
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")

csv = planning_table.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Planning Report",
    data=csv,
    file_name="planning_dashboard_report.csv",
    mime="text/csv"
)