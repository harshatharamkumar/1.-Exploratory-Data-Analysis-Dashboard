#loading the streamlit library with its alias
import streamlit as st

st.set_page_config(
    page_title="EDA Dashboard", 
    layout="wide"
)

st.title("Exploratory Data Analysis Dashboard")

st.write(
"""
upload any CSV and generate 
automatic EDA reports.
"""
)

