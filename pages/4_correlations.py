import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Correlations")

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"],
)

if uploaded_file is None:
    st.info("Upload a CSV file to view correlations.")
    st.stop()

# Load data after upload
df = pd.read_csv(uploaded_file)

corr_matrix = df.corr(numeric_only=True)

if corr_matrix.empty:
    st.warning("No numeric columns found to compute correlations.")
    st.stop()

# Heatmap
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Correlation pairs (sorted)
upper = corr_matrix.where(~pd.isna(corr_matrix))

corr_pairs = (
    upper.unstack()
    .sort_values(ascending=False)
)

st.write(corr_pairs)

