import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Distributions")

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"],
)

if uploaded_file is None:
    st.info("Upload a CSV file to view distributions.")
    st.stop()

# Load data after the user uploads the file
df = pd.read_csv(uploaded_file)

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

if len(numeric_cols) == 0:
    st.warning("No numeric columns found to plot.")
    st.stop()

for col in numeric_cols:
    fig, ax = plt.subplots()
    sns.histplot(df[col].dropna(), kde=True, ax=ax)
    ax.set_title(col)
    st.pyplot(fig)

