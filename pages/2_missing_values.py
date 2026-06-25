import streamlit as st
import pandas as pd
import plotly.express as px

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    missing = df.isnull().sum()

    st.write(missing)
    
missing_df = pd.DataFrame({
    "Column": missing.index,
    "Missing": missing.values
})

fig = px.bar(
    missing_df,
    x="Column",
    y="Missing"
)
