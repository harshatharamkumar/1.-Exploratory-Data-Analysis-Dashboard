import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Interactive Charts")

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"],
)

if uploaded_file is None:
    st.info("Upload a CSV file to view interactive charts.")
    st.stop()

# Load data after upload
df = pd.read_csv(uploaded_file)

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

if not numeric_cols:
    st.warning("No numeric columns found.")
    st.stop()

# Defaults
x_default = numeric_cols[0]
y_default = numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]
color_default = None

# Column selectors
x_col = st.selectbox("X-axis", options=numeric_cols, index=0)
y_col = st.selectbox("Y-axis", options=numeric_cols, index=1 if len(numeric_cols) > 1 else 0)

# Optional grouping by non-numeric column
cat_cols = df.select_dtypes(exclude=["int64", "float64"]).columns.tolist()
color_col = st.selectbox(
    "Color by (optional)",
    options=["None"] + cat_cols,
    index=0,
)

color_by = None if color_col == "None" else color_col

# Chart type
# --- Most important section: interactive plot controls ---
st.subheader("Interactive Plotly Dashboard")

# x/y dropdowns (use all columns)
x_axis = st.selectbox("X Axis", options=df.columns, index=df.columns.get_loc(x_col))
y_axis = st.selectbox("Y Axis", options=df.columns, index=df.columns.get_loc(y_col))

# Chart type
chart_type = st.radio(
    "Chart type",
    options=["Scatter", "Bar", "Box"],
    index=0,
    horizontal=True,
)

if chart_type == "Scatter":
    fig = px.scatter(df, x=x_axis, y=y_axis)
    st.plotly_chart(fig, use_container_width=True)

elif chart_type == "Bar":
    # For bar, y should be numeric ideally; Plotly will aggregate if needed.
    fig = px.bar(df, x=x_axis, y=y_axis)
    st.plotly_chart(fig, use_container_width=True)

else:  # Box
    fig = px.box(df, x=x_axis, y=y_axis)
    st.plotly_chart(fig, use_container_width=True)

with st.expander("Preview data"):
    st.dataframe(df.head(50), use_container_width=True)


