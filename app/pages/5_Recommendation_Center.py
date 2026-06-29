import streamlit as st
import pandas as pd
with open("app/assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Recommendation Center",
    page_icon="💡",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

recommendation_df = pd.read_csv(
    "app/data/recommendations.csv"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("💡 Smart Recommendation Center")

st.caption(
    "AI-driven Inventory Decision Support"
)

st.markdown("---")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Filters")

warehouse = st.sidebar.selectbox(
    "Warehouse",
    ["All"] + sorted(
        recommendation_df["Warehouse"].astype(str).unique().tolist()
    )
)

abc = st.sidebar.selectbox(
    "ABC Class",
    ["All"] + sorted(
        recommendation_df["ABC_Class"].unique().tolist()
    )
)

xyz = st.sidebar.selectbox(
    "XYZ Class",
    ["All"] + sorted(
        recommendation_df["XYZ_Class"].unique().tolist()
    )
)

risk = st.sidebar.selectbox(
    "Inventory Risk",
    ["All"] + sorted(
        recommendation_df["Inventory_Risk"].unique().tolist()
    )
)

part = st.sidebar.text_input(
    "Search Part Number"
)

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

filtered_df = recommendation_df.copy()

if warehouse != "All":
    filtered_df = filtered_df[
        filtered_df["Warehouse"].astype(str) == warehouse
    ]

if abc != "All":
    filtered_df = filtered_df[
        filtered_df["ABC_Class"] == abc
    ]

if xyz != "All":
    filtered_df = filtered_df[
        filtered_df["XYZ_Class"] == xyz
    ]

if risk != "All":
    filtered_df = filtered_df[
        filtered_df["Inventory_Risk"] == risk
    ]

if part:
    filtered_df = filtered_df[
        filtered_df["Part_No"]
        .astype(str)
        .str.contains(part, case=False)
    ]

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Matching Parts",
    len(filtered_df)
)

col2.metric(
    "Unique Warehouses",
    filtered_df["Warehouse"].nunique()
)

col3.metric(
    "Recommendations",
    filtered_df["Recommendation"].nunique()
)

st.markdown("---")

# --------------------------------------------------
# PART ANALYSIS
# --------------------------------------------------

st.subheader("🔍 Part Analysis")

if len(filtered_df) > 0:

    selected_part = st.selectbox(
        "Select Part",
        filtered_df["Part_No"].unique()
    )

    part = filtered_df[
        filtered_df["Part_No"] == selected_part
    ].iloc[0]

    # --------------------------------------------------
    # PRIORITY LEVEL
    # --------------------------------------------------

    if (
        part["Inventory_Risk"] == "High Risk"
        and part["ABC_Class"] == "A"
    ):
        priority = "🔴 Critical"

    elif part["Inventory_Risk"] == "High Risk":
        priority = "🟠 High"

    elif part["Inventory_Risk"] == "Medium Risk":
        priority = "🟡 Medium"

    else:
        priority = "🟢 Low"

    # --------------------------------------------------
    # PART KPIs
    # --------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Warehouse",
        str(part["Warehouse"])
    )

    c2.metric(
        "ABC-XYZ",
        f'{part["ABC_Class"]}-{part["XYZ_Class"]}'
    )

    c3.metric(
        "Inventory Risk",
        part["Inventory_Risk"]
    )

    c4.metric(
        "Priority",
        priority
    )

    st.markdown("")

    c1, c2 = st.columns(2)

    c1.metric(
        "Safety Stock",
        f'{part["Safety_Stock"]:.2f}'
    )

    c2.metric(
        "Reorder Point",
        f'{part["Reorder_Point"]:.2f}'
    )

    st.markdown("### 💡 Recommendation")

    st.success(
        part["Recommendation"]
    )

    # --------------------------------------------------
    # EXECUTIVE DECISION
    # --------------------------------------------------

    st.markdown("### 📌 Executive Decision")

    st.info(
        f"""
**Part Number:** {selected_part}

**Priority:** {priority}

**Recommended Action:** {part['Recommendation']}

**Demand Category:** {part['Demand_Class']}

**Safety Stock:** {part['Safety_Stock']:.2f}

**Reorder Point:** {part['Reorder_Point']:.2f}
"""
    )

    # --------------------------------------------------
    # BUSINESS INTERPRETATION
    # --------------------------------------------------

    st.subheader("📊 Business Interpretation")

    st.info(
        f"""
### Selected Part: {selected_part}

• Demand Classification: **{part['Demand_Class']}**

• ABC Category: **{part['ABC_Class']}**

• XYZ Category: **{part['XYZ_Class']}**

• Inventory Risk: **{part['Inventory_Risk']}**

• Safety Stock Recommendation: **{part['Safety_Stock']:.2f}**

• Reorder Point: **{part['Reorder_Point']:.2f}**

### Recommended Action

{part['Recommendation']}
"""
    )

else:

    st.warning(
        "No parts match the selected filters."
    )

# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

st.download_button(
    "📥 Download Recommendations",
    filtered_df.to_csv(index=False),
    "recommendations.csv",
    "text/csv"
)