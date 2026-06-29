import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

profile_df = pd.read_csv("outputs/final/demand_profile.csv")
inventory_df = pd.read_csv("outputs/final/inventory_optimization.csv")
recommendation_df = pd.read_csv("outputs/final/recommendations.csv")
abc_df = pd.read_csv("outputs/final/abc_analysis.csv")

st.write("Profile:", profile_df.shape)
st.write("Inventory:", inventory_df.shape)
st.write("Recommendation:", recommendation_df.shape)
st.write("ABC:", abc_df.shape)

st.write("Inventory duplicate Warehouse+Part:",
         inventory_df.duplicated(subset=["Warehouse", "Part_No"]).sum())

st.write("Recommendation duplicate Warehouse+Part:",
         recommendation_df.duplicated(subset=["Warehouse", "Part_No"]).sum())

st.write("ABC duplicate Warehouse+Part:",
         abc_df.duplicated(subset=["Warehouse", "Part_No"]).sum())

st.stop()