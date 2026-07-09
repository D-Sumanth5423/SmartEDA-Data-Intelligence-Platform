import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

def get_overview(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_cells": int(df.isnull().sum().sum()),
        "missing_pct": round(df.isnull().sum().sum() / df.size * 100, 2),
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_cols": len(df.select_dtypes(include=np.number).columns),
        "categorical_cols": len(df.select_dtypes(include="object").columns),
    }

def get_column_stats(df):
    stats_list = []
    for col in df.columns:
        s = {
            "column": col,
            "dtype": str(df[col].dtype),
            "missing": int(df[col].isnull().sum()),
            "missing_pct": round(df[col].isnull().sum() / len(df) * 100, 1),
            "unique": int(df[col].nunique()),
        }
        if pd.api.types.is_numeric_dtype(df[col]):
            s.update({
                "mean": round(df[col].mean(), 3),
                "median": round(df[col].median(), 3),
                "std": round(df[col].std(), 3),
                "min": round(df[col].min(), 3),
                "max": round(df[col].max(), 3),
                "skewness": round(df[col].skew(), 3),
            })
        else:
            s.update({
                "mean": None, "median": None, "std": None,
                "min": None, "max": None, "skewness": None,
                "top_value": str(df[col].mode()[0]) if len(df[col].mode()) > 0 else "N/A"
            })
        stats_list.append(s)
    return pd.DataFrame(stats_list)

def detect_outliers(df):
    results = {}
    for col in df.select_dtypes(include=np.number).columns:
        clean = df[col].dropna()
        Q1, Q3 = clean.quantile(0.25), clean.quantile(0.75)
        IQR = Q3 - Q1
        count = int(((clean < Q1 - 1.5 * IQR) | (clean > Q3 + 1.5 * IQR)).sum())
        results[col] = count
    return results

def get_auto_insights(df):
    insights = []
    num_cols = df.select_dtypes(include=np.number).columns
    cat_cols = df.select_dtypes(include="object").columns

    # Missing value insights
    for col in df.columns:
        pct = round(df[col].isnull().sum() / len(df) * 100, 1)
        if pct > 20:
            insights.append(("warning", f"Column '{col}' has {pct}% missing values — data quality issue."))
        elif pct > 0:
            insights.append(("info", f"Column '{col}' has {pct}% missing values."))

    # Skewness insights
    for col in num_cols:
        skew = df[col].skew()
        if skew > 1:
            insights.append(("info", f"Column '{col}' is right-skewed (skewness={round(skew,2)}) — consider log transform."))
        elif skew < -1:
            insights.append(("info", f"Column '{col}' is left-skewed (skewness={round(skew,2)})."))

    # Outlier insights
    outliers = detect_outliers(df)
    for col, count in outliers.items():
        if count > 0:
            pct = round(count / len(df) * 100, 1)
            insights.append(("warning", f"Column '{col}' has {count} outliers ({pct}% of rows)."))

    # Correlation insights
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        pairs = []
        for i in range(len(corr.columns)):
            for j in range(i+1, len(corr.columns)):
                val = corr.iloc[i, j]
                if abs(val) > 0.7:
                    pairs.append((corr.columns[i], corr.columns[j], round(val, 2)))
        for a, b, v in pairs[:3]:
            direction = "positive" if v > 0 else "negative"
            insights.append(("success", f"Strong {direction} correlation ({v}) between '{a}' and '{b}'."))

    # Categorical insights
    for col in cat_cols:
        top = df[col].value_counts().iloc[0]
        top_pct = round(top / len(df) * 100, 1)
        top_val = df[col].value_counts().index[0]
        if top_pct > 70:
            insights.append(("warning", f"Column '{col}' is dominated by '{top_val}' ({top_pct}%) — low diversity."))
        else:
            insights.append(("info", f"Column '{col}' top value: '{top_val}' ({top_pct}%)."))

    # Duplicate insight
    dups = df.duplicated().sum()
    if dups > 0:
        insights.append(("warning", f"{dups} duplicate rows found — consider removing them."))

    if not insights:
        insights.append(("success", "Dataset looks clean — no major issues detected!"))

    return insights

def get_top_correlations(df, n=5):
    num_df = df.select_dtypes(include=np.number)
    if num_df.shape[1] < 2:
        return []
    corr = num_df.corr().abs()
    pairs = []
    cols = corr.columns
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            pairs.append((cols[i], cols[j], round(corr.iloc[i,j], 3)))
    pairs.sort(key=lambda x: x[2], reverse=True)
    return pairs[:n]

def plot_distribution(df, col, chart_type="Histogram"):
    if chart_type == "Histogram":
        fig = px.histogram(df, x=col, marginal="box",
                           color_discrete_sequence=["#534AB7"],
                           title=f"Distribution of {col}")
    elif chart_type == "Box plot":
        fig = px.box(df, y=col, color_discrete_sequence=["#534AB7"],
                     title=f"Box plot of {col}")
    elif chart_type == "Violin":
        fig = px.violin(df, y=col, box=True,
                        color_discrete_sequence=["#534AB7"],
                        title=f"Violin plot of {col}")
    else:
        fig = px.histogram(df, x=col, color_discrete_sequence=["#534AB7"])
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    return fig

def plot_scatter(df, x_col, y_col, color_col=None):
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                     title=f"{x_col} vs {y_col}",
                     color_discrete_sequence=px.colors.qualitative.Vivid)
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    return fig

def plot_correlation(df):
    num_df = df.select_dtypes(include=np.number)
    if num_df.shape[1] < 2:
        return None
    corr = num_df.corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                    title="Correlation heatmap", aspect="auto")
    fig.update_layout(paper_bgcolor="white")
    return fig

def plot_missing(df):
    missing = df.isnull().sum()
    missing = missing[missing > 0].reset_index()
    missing.columns = ["Column", "Missing count"]
    if missing.empty:
        return None
    fig = px.bar(missing, x="Column", y="Missing count",
                 color_discrete_sequence=["#D85A30"],
                 title="Missing values per column")
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    return fig

def plot_categorical(df, col):
    val_counts = df[col].value_counts().reset_index()
    val_counts.columns = [col, "Count"]
    fig = px.bar(val_counts, x=col, y="Count",
                 color_discrete_sequence=["#1D9E75"],
                 title=f"Value counts — {col}")
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    return fig

def suggest_problem_type(df):
    suggestions = []
    for col in df.select_dtypes(include=np.number).columns:
        unique_ratio = df[col].nunique() / len(df)
        if unique_ratio < 0.05:
            suggestions.append(f"'{col}' could be a classification target ({df[col].nunique()} unique values)")
        elif unique_ratio > 0.8:
            suggestions.append(f"'{col}' looks like a regression target (continuous numeric)")
    return suggestions if suggestions else ["No clear ML targets detected. Try a larger dataset."]

def data_quality_score(df):
    completeness = 1 - df.isnull().sum().sum() / df.size
    no_dups = 1 - df.duplicated().sum() / len(df)
    type_ratio = len(df.select_dtypes(include=np.number).columns) / df.shape[1]
    return round((completeness * 0.5 + no_dups * 0.3 + type_ratio * 0.2) * 100)

def clean_remove_nulls(df):
    return df.dropna()

def clean_fill_mean(df):
    df2 = df.copy()
    for col in df2.select_dtypes(include=np.number).columns:
        df2[col].fillna(df2[col].mean(), inplace=True)
    return df2

def clean_fill_median(df):
    df2 = df.copy()
    for col in df2.select_dtypes(include=np.number).columns:
        df2[col].fillna(df2[col].median(), inplace=True)
    return df2

def clean_fill_mode(df):
    df2 = df.copy()
    for col in df2.columns:
        mode = df2[col].mode()
        if len(mode) > 0:
            df2[col].fillna(mode[0], inplace=True)
    return df2

def clean_remove_duplicates(df):
    return df.drop_duplicates()

def clean_remove_outliers(df):
    df2 = df.copy()
    for col in df2.select_dtypes(include=np.number).columns:
        Q1, Q3 = df2[col].quantile(0.25), df2[col].quantile(0.75)
        IQR = Q3 - Q1
        df2 = df2[(df2[col] >= Q1 - 1.5*IQR) & (df2[col] <= Q3 + 1.5*IQR)]
    return df2

def mini_query(df, query):
    query = query.lower().strip()
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    results = []
    for col in num_cols:
        if col.lower() in query:
            if "mean" in query or "average" in query:
                results.append(f"Mean of '{col}': {round(df[col].mean(), 3)}")
            if "median" in query:
                results.append(f"Median of '{col}': {round(df[col].median(), 3)}")
            if "max" in query or "maximum" in query:
                results.append(f"Max of '{col}': {round(df[col].max(), 3)}")
            if "min" in query or "minimum" in query:
                results.append(f"Min of '{col}': {round(df[col].min(), 3)}")
            if "std" in query or "standard deviation" in query:
                results.append(f"Std of '{col}': {round(df[col].std(), 3)}")
            if "sum" in query:
                results.append(f"Sum of '{col}': {round(df[col].sum(), 3)}")
            if "count" in query:
                results.append(f"Count of '{col}': {df[col].count()}")
            if "missing" in query or "null" in query:
                results.append(f"Missing in '{col}': {df[col].isnull().sum()}")
    if not results:
        results.append("Could not understand query. Try: 'mean of salary' or 'max of age'")
    return results