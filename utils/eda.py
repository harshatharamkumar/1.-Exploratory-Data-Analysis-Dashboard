import pandas as pd


def get_numeric_columns(df: pd.DataFrame):
    """Return numeric column names."""
    return df.select_dtypes(include=["int64", "float64"]).columns


def compute_iqr_bounds(df: pd.DataFrame, col: str, multiplier: float = 1.5):
    """Compute IQR-based lower/upper bounds for outliers."""
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - multiplier * iqr
    upper = q3 + multiplier * iqr
    return q1, q3, iqr, lower, upper


def detect_outliers(df: pd.DataFrame, col: str, multiplier: float = 1.5):
    """Return rows that are outliers in `col` using the IQR rule."""
    _, _, _, lower, upper = compute_iqr_bounds(df, col, multiplier=multiplier)
    return df[(df[col] < lower) | (df[col] > upper)]

