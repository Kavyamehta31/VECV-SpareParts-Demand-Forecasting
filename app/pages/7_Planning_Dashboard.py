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

st.subheader("Profile Columns")
st.write(profile_df.columns.tolist())

st.subheader("Inventory Columns")
st.write(inventory_df.columns.tolist())

st.subheader("Recommendation Columns")
st.write(recommendation_df.columns.tolist())

st.subheader("ABC Columns")
st.write(abc_df.columns.tolist())

st.stop()