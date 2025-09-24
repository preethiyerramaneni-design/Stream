import streamlit as st
import pandas as pd
import plotly.express as px

# Load preprocessed measurements CSV (not metadata)
df = pd.read_csv("argo_data/argo_master_clean.csv")  # <- change here

st.title("🌊 ARGO Ocean Profiles Dashboard")

# Select float
float_ids = df['float_id'].unique()
selected_float = st.selectbox("Select Float ID", float_ids)

# Filter data for selected float
float_data = df[df['float_id'] == selected_float]

# Plot Temperature vs Depth
fig_temp = px.line(
    float_data, x="temperature_C", y="depth_dbar",
    title="🌡 Temperature Profile",
    labels={"temperature_C": "Temperature (°C)", "depth_dbar": "Depth (dbar)"}
)
fig_temp.update_yaxes(autorange="reversed")  # Depth increases downward
st.plotly_chart(fig_temp, use_container_width=True)

# Plot Salinity vs Depth
fig_sal = px.line(
    float_data, x="salinity_psu", y="depth_dbar",
    title="💧 Salinity Profile",
    labels={"salinity_psu": "Salinity (PSU)", "depth_dbar": "Depth (dbar)"},
    color_discrete_sequence=['orange']
)
fig_sal.update_yaxes(autorange="reversed")
st.plotly_chart(fig_sal, use_container_width=True)

# Optional: show raw table
st.subheader("Raw Data")
st.dataframe(float_data)
