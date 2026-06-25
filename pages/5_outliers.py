import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Outliers")

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"],
)

if uploaded_file is None:
    st.info("Upload a CSV file to view outliers.")
    st.stop()

# Load data after upload
df = pd.read_csv(uploaded_file)

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

if len(numeric_cols) == 0:
    st.warning("No numeric columns found to detect outliers.")
    st.stop()

st.write(f"Numeric columns found: {len(numeric_cols)}")

# --- Outlier detection (IQR) ---
mult = st.slider("IQR multiplier", min_value=0.5, max_value=3.0, value=1.5, step=0.1)

results = []

for col in numeric_cols:
    s = df[col]
    s_nonnull = s.dropna()
    if s_nonnull.empty:
        continue

    q1 = s_nonnull.quantile(0.25)
    q3 = s_nonnull.quantile(0.75)
    iqr = q3 - q1
    if iqr == 0:
        continue

    lower = q1 - mult * iqr
    upper = q3 + mult * iqr

    out_mask = (s < lower) | (s > upper)
    out_count = int(out_mask.sum())

    results.append(
        {
            "column": col,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "lower_bound": lower,
            "upper_bound": upper,
            "outlier_count": out_count,
        }
    )

outliers_df = pd.DataFrame(results).sort_values("outlier_count", ascending=False)

if outliers_df.empty:
    st.warning("Could not compute outliers (maybe all numeric columns have zero IQR).")
    st.stop()

st.subheader("Outlier summary (IQR method)")
st.dataframe(outliers_df)

# --- Visualize ---
plot_col = st.selectbox(
    "Select a numeric column to visualize outliers",
    options=outliers_df["column"].tolist(),
)

q1 = outliers_df.loc[outliers_df["column"] == plot_col, "q1"].iloc[0]
q3 = outliers_df.loc[outliers_df["column"] == plot_col, "q3"].iloc[0]
iqr = outliers_df.loc[outliers_df["column"] == plot_col, "iqr"].iloc[0]
lower = outliers_df.loc[outliers_df["column"] == plot_col, "lower_bound"].iloc[0]
upper = outliers_df.loc[outliers_df["column"] == plot_col, "upper_bound"].iloc[0]

plot_df = df[[plot_col]].copy()
plot_df = plot_df.dropna()

# Label outliers for coloring
plot_df["is_outlier"] = np.where((plot_df[plot_col] < lower) | (plot_df[plot_col] > upper), "Outlier", "Inlier")

fig = px.scatter(
    plot_df,
    x=plot_df.index,
    y=plot_df[plot_col],
    color="is_outlier",
    color_discrete_map={"Outlier": "crimson", "Inlier": "steelblue"},
    labels={"x": "Row index", plot_col: plot_col},
)

# Add bounds lines
fig.add_hline(y=lower, line_width=1, line_dash="dash", line_color="gray")
fig.add_hline(y=upper, line_width=1, line_dash="dash", line_color="gray")

st.subheader("Outliers scatter plot")
st.plotly_chart(fig, use_container_width=True)

st.caption(f"Outlier bounds for {plot_col}: [{lower:.4g}, {upper:.4g}] (multiplier={mult})")

