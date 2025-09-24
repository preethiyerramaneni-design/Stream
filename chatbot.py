import streamlit as st
import pandas as pd
import plotly.express as px
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# -------------------------------
# Streamlit title
# -------------------------------
st.set_page_config(page_title="ARGO AI Chatbot", layout="wide")
st.title("🤖 ARGO AI Chatbot with Plots")

# -------------------------------
# Load preprocessed CSV & metadata
# -------------------------------
try:
    df = pd.read_csv("argo_data/argo_master_clean.csv")
    metadata = pd.read_csv("argo_data/argo_metadata.csv")
except FileNotFoundError:
    st.error("❌ CSV files not found. Please run preprocessing first.")
    st.stop()

if df.empty or metadata.empty:
    st.error("❌ CSVs are empty. Please check Step 1-3.")
    st.stop()

# -------------------------------
# Ensure float_id exists
# -------------------------------
if 'float_id' not in df.columns:
    df['float_id'] = 'float_1'
if 'float_id' not in metadata.columns:
    metadata['float_id'] = 'float_1'

# -------------------------------
# Embeddings & FAISS index
# -------------------------------
model = SentenceTransformer('all-MiniLM-L6-v2')
metadata_embeddings = model.encode(metadata['summary'].tolist(), convert_to_numpy=True)

dim = metadata_embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(metadata_embeddings)

# -------------------------------
# User Input
# -------------------------------
user_query = st.text_input(
    "Ask me about ARGO floats!", 
    placeholder="Example: Show me salinity profile near equator"
)

if user_query:
    # Encode user query
    query_embedding = model.encode([user_query], convert_to_numpy=True).reshape(1, -1)
    
    # FAISS search
    D, I = index.search(query_embedding, k=1)
    matched_idx = I[0][0]
    
    matched_summary = metadata.iloc[matched_idx]['summary']
    float_id = metadata.iloc[matched_idx]['float_id']
    
    st.subheader("Top Match Summary")
    st.write(matched_summary)
    
    # Filter float data
    float_data = df[df['float_id'] == float_id]
    
    if float_data.empty:
        st.warning(f"No measurements found for {float_id}")
    else:
        st.subheader(f"Measurements for {float_id}")
        st.dataframe(float_data)
        
        # Plot Temperature vs Depth
        fig_temp = px.line(
            float_data, x="temperature_C", y="depth_dbar",
            title="🌡 Temperature Profile",
            labels={"temperature_C": "Temperature (°C)", "depth_dbar": "Depth (dbar)"}
        )
        fig_temp.update_yaxes(autorange="reversed")
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

else:
    st.info("Type a query above to see float data and plots.")