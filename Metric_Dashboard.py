import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore

# Importing and Cleaning Data

df_stats = pd.read_excel('ANTHRO.xlsx', sheet_name = "Sheet1")


df_position = pd.read_excel('ANTHRO.xlsx', sheet_name = "Control_Panel")


df_stats = df_stats[["Name","ID","Height","Hand Size","Wingspan"]].dropna(how='all')



df_position = df_position.dropna(subset=["Position", "Group"])


df = df_position.merge(df_stats, on = ["ID","Name"])

# Sidebar filters
st.sidebar.header("Filters")

# Add 'All' option to position and group filters
position_options = ['All'] + sorted(df["Position"].dropna().unique())
group_options = ['All'] + sorted(df["Group"].dropna().unique())

position = st.sidebar.selectbox("Position", position_options)
group = st.sidebar.selectbox("Group", group_options)
df_filtered = df
# Apply filters with logic for 'All'
if position != 'All':
    df_filtered = df_filtered[df_filtered["Position"] == position]
if group != 'All':
    df_filtered = df_filtered[df_filtered["Group"] == group]

# User inputs
st.sidebar.header("Enter Player Metrics")
height = st.sidebar.number_input("Height (format: 6003 = 6'0\"3)", min_value=5000.0, max_value=7000.0, step=1.0)
hand_size = st.sidebar.number_input("Hand Size (inches)", min_value=5.0, max_value=13.0, step=0.1)
wingspan = st.sidebar.number_input("Wingspan (inches)", min_value=60.0, max_value=90.0, step=0.1)
custom_metric = st.sidebar.number_input("Custom Metric (example placeholder)", min_value=0.0, max_value=100.0, step=0.1)


metrics = {
    "Height": height,
    "Hand Size": hand_size,
    "Wingspan": wingspan,
    "Custom": custom_metric
}

# UCLA colors
UCLA_BLUE = "#2774AE"
UCLA_GOLD = "#FFD100"

# Plotting function
def plot_percentile(data, value, metric):
    percentile = percentileofscore(data, value)
    fig, ax = plt.subplots()
    sns.kdeplot(data, fill=True, color=UCLA_GOLD, ax=ax)
    ax.axvline(value, color=UCLA_BLUE, linestyle="--")
    ax.text(value + 0.2, ax.get_ylim()[1] * 0.05, f"{value} \n{percentile:.1f}th pct", color=UCLA_BLUE, fontweight='bold')
    ax.set_title(f"{metric} Distribution")
    ax.set_xlabel(metric)
    ax.set_ylabel("Density")
    return fig

# Show plots in a 2x2 grid
st.header("Percentile Visualizations")

cols = st.columns(2)
metric_names = list(metrics.keys())

for i, metric in enumerate(metric_names):
    value = metrics[metric]
    with cols[i % 2]:
        if metric in df_filtered.columns and df_filtered[metric].notna().sum() > 0:
            fig = plot_percentile(df_filtered[metric].dropna(), value, metric)
            st.pyplot(fig)
        else:
            st.write(f"{metric} not found or insufficient data.")
