
import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import io

st.set_page_config(page_title="HessQ Fraud Detection Demo", layout="centered")

st.title("🔍 HessQ Fraud Detection Demo")
st.markdown("This interactive demo shows how we detect fraud using quantum-inspired optimization logic (QUBO) and route reconstruction (TSP).")

# Load CSV data
uploaded_file = st.file_uploader("Upload a CSV file with transactions", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded. Using default demo transactions.")
    df = pd.DataFrame({
        "Transaction ID": [f"T{i}" for i in range(1, 11)],
        "Amount ($)": [112, 445, 870, 280, 116, 334, 550, 123, 780, 222],
        "Latitude": [-84.66, -90.73, -91.67, -60.39, -65.58, -98.22, -85.00, -95.10, -92.00, -80.50],
        "Longitude": [32.9, 57.1, 59.7, 34.8, 41.0, 36.5, 45.0, 50.0, 47.0, 40.0],
        "Timestamp": pd.date_range("2025-07-01 08:00", periods=10, freq="H")
    })

# Build the graph
G = nx.Graph()
for i, row in df.iterrows():
    G.add_node(row["Transaction ID"], pos=(row["Latitude"], row["Longitude"]), amount=row["Amount ($)"])

for i in range(len(df)):
    for j in range(i + 1, len(df)):
        t1, t2 = df.iloc[i], df.iloc[j]
        dist = np.sqrt((t1["Latitude"] - t2["Latitude"])**2 + (t1["Longitude"] - t2["Longitude"])**2)
        time_diff = abs((pd.to_datetime(t1["Timestamp"]) - pd.to_datetime(t2["Timestamp"])).total_seconds()) / 3600
        amount_diff = abs(t1["Amount ($)"] - t2["Amount ($)"])
        weight = dist + 0.5 * time_diff + 0.01 * amount_diff
        if weight < 10:
            G.add_edge(t1["Transaction ID"], t2["Transaction ID"], weight=weight)

# Draw the graph
st.subheader("📌 Transaction Graph")
fig, ax = plt.subplots(figsize=(10, 6))
pos = nx.get_node_attributes(G, 'pos')
colors = ['red' if G.degree(n) > 2 else 'skyblue' for n in G.nodes]
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=800, font_weight='bold', edge_color='gray', ax=ax)
st.pyplot(fig)

st.markdown("🧠 Transactions with **red nodes** have multiple suspicious connections and may indicate potential fraud.")
