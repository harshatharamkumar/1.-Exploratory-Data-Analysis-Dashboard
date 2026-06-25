import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt 

numeric_cols = df.select_dtypes(
    include=['int64', 'float64']
    ).columns

for col in numeric_cols:
    fig, ax = plt.subplots()
    sns.histplot(
        df[col],
        kde=True,
        ax=ax
    )

    st.pyplot(fig)