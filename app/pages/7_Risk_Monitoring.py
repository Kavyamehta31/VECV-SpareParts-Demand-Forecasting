import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Risk Monitoring",
    page_icon="⚠",
    layout="wide"
)

st.title("⚠ Risk Monitoring Dashboard")

st.markdown("---")

inventory_df = pd.read_csv(
    "outputs/final/inventory_optimization.csv"
)
high_risk = (
    inventory_df["Inventory_Risk"] == "High Risk"
).sum()

medium_risk = (
    inventory_df["Inventory_Risk"] == "Medium Risk"
).sum()

low_risk = (
    inventory_df["Inventory_Risk"] == "Low Risk"
).sum()

dead_inventory = (
    inventory_df["Inventory_Risk"] == "Dead Inventory"
).sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "High Risk",
    f"{high_risk:,}"
)

c2.metric(
    "Medium Risk",
    f"{medium_risk:,}"
)

c3.metric(
    "Low Risk",
    f"{low_risk:,}"
)

c4.metric(
    "Dead Inventory",
    f"{dead_inventory:,}"
)

st.markdown("---")
left, right = st.columns(2)

with left:

    risk_counts = (
        inventory_df["Inventory_Risk"]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "Risk",
        "Count"
    ]

    fig = px.pie(
        risk_counts,
        names="Risk",
        values="Count",
        hole=0.45,
        title="Inventory Risk Distribution"
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
with right:

    warehouse_risk = (

        inventory_df

        .groupby(["Warehouse", "Inventory_Risk"])

        .size()

        .reset_index(name="Count")

    )

    warehouse_risk["Warehouse"] = (
        warehouse_risk["Warehouse"].astype(str)
    )

    fig = px.bar(

        warehouse_risk,

        x="Warehouse",

        y="Count",

        color="Inventory_Risk",

        barmode="stack",

        text="Count",

        title="Inventory Risk by Warehouse"

    )

    fig.update_layout(
        height=500,
        xaxis_title="Warehouse",
        yaxis_title="Number of Parts"
    )

    fig.update_traces(
        textposition="inside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")
st.subheader("📦 Inventory Coverage")

fig = px.histogram(

    inventory_df,

    x="Inventory_Coverage",

    nbins=30,

    title="Inventory Coverage Distribution"

)

fig.update_layout(

    height=450,

    xaxis_title="Inventory Coverage (Months)",

    yaxis_title="Number of Parts"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")
st.subheader("📦 Top Inventory Coverage")

top_coverage = (

    inventory_df

    .sort_values(
        "Inventory_Coverage",
        ascending=False
    )

    .head(10)

)

fig = px.bar(

    top_coverage,

    x="Inventory_Coverage",

    y="Part_No",

    orientation="h",

    color="Inventory_Coverage",

    text="Inventory_Coverage",

    title="Top 10 Parts by Inventory Coverage"

)

fig.update_layout(
    height=500,
    yaxis=dict(categoryorder="total ascending")
)

fig.update_traces(
    texttemplate="%{text:.1f}",
    textposition="outside"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")
high_risk = (
    inventory_df["Inventory_Risk"] == "High Risk"
).sum()

dead_inventory = (
    inventory_df["Inventory_Risk"] == "Dead Inventory"
).sum()

avg_coverage = inventory_df["Inventory_Coverage"].mean()

st.subheader("📋 Executive Insights")

st.success(f"""
### Inventory Risk Summary

✔ High Risk Parts: **{high_risk:,}**

✔ Medium Risk Parts: **{medium_risk:,}**

✔ Low Risk Parts: **{low_risk:,}**

✔ Dead Inventory: **{dead_inventory:,}**

✔ Average Inventory Coverage: **{avg_coverage:.2f} Months**
""")

st.info("""
### Recommendations

• Prioritize replenishment for High Risk parts.

• Review Dead Inventory for disposal or liquidation.

• Maintain adequate safety stock for Fast Moving items.

• Continuously monitor inventory coverage to reduce stock-outs and overstock situations.
""")