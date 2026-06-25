import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader(
    "Upload CSV",
      type=["csv"]
)


if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Dataset")
    st.dataframe(df.head())
    st.subheader("Shape")
    st.write(df.shape)
    st.subheader("Data Types")
    st.write(df.dtypes)
    st.subheader("Statistics")
    st.write(df.describe())
