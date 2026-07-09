import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (accuracy_score, classification_report,
                              mean_squared_error, r2_score, confusion_matrix)
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")


# ─────────────────────────────────────────
# AUTO PROBLEM TYPE DETECTION
# ─────────────────────────────────────────
def detect_problem_type(df, target_col):
    target = df[target_col].dropna()
    unique_count = target.nunique()
    is_numeric = pd.api.types.is_numeric_dtype(target)

    if not is_numeric:
        return "classification"
    if unique_count <= 10:
        return "classification"
    # Check if values look like dates/time series
    if pd.api.types.is_datetime64_any_dtype(target):
        return "timeseries"
    return "regression"


def get_problem_label(problem_type):
    labels = {
        "classification": ("Classification Dataset", "Predict a category or class label", "#6c5ce7"),
        "regression": ("Regression Dataset", "Predict a continuous numeric value", "#00b894"),
        "timeseries": ("Time Series Dataset", "Predict values over time", "#fdcb6e"),
    }
    return labels.get(problem_type, ("Unknown", "", "#888"))


# ─────────────────────────────────────────
# DATA PREP FOR ML
# ─────────────────────────────────────────
def prepare_data(df, target_col):
    df2 = df.copy().dropna()
    X = df2.drop(columns=[target_col])
    y = df2[target_col]

    # Encode categoricals in X
    le_map = {}
    for col in X.select_dtypes(include="object").columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        le_map[col] = le

    # Encode target if categorical
    target_le = None
    if not pd.api.types.is_numeric_dtype(y):
        target_le = LabelEncoder()
        y = target_le.fit_transform(y.astype(str))

    return X, y, le_map, target_le


# ─────────────────────────────────────────
# AUTO ML PIPELINE
# ─────────────────────────────────────────
def run_auto_ml(df, target_col):
    problem_type = detect_problem_type(df, target_col)
    X, y, le_map, target_le = prepare_data(df, target_col)

    if len(X) < 10:
        return None, "Not enough rows to train a model (need at least 10)."

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    results = {"problem_type": problem_type, "target": target_col,
               "n_train": len(X_train), "n_test": len(X_test),
               "features": list(X.columns)}

    if problem_type == "classification":
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results["model_name"] = "Random Forest Classifier"
        results["accuracy"] = round(accuracy_score(y_test, y_pred) * 100, 2)
        results["metric_label"] = "Accuracy"
        results["metric_value"] = f"{results['accuracy']}%"
        results["report"] = classification_report(
            y_test, y_pred, output_dict=True, zero_division=0
        )
        results["confusion"] = confusion_matrix(y_test, y_pred).tolist()
        results["classes"] = list(map(str, model.classes_))

    else:  # regression
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        r2 = round(r2_score(y_test, y_pred) * 100, 2)
        rmse = round(np.sqrt(mean_squared_error(y_test, y_pred)), 3)
        results["model_name"] = "Random Forest Regressor"
        results["accuracy"] = r2
        results["metric_label"] = "R² Score"
        results["metric_value"] = f"{r2}%"
        results["rmse"] = rmse

    # Feature importance
    importances = model.feature_importances_
    feat_imp = pd.DataFrame({
        "Feature": X.columns,
        "Importance": importances
    }).sort_values("Importance", ascending=False)
    results["feature_importance"] = feat_imp
    results["model"] = model

    return results, None


# ─────────────────────────────────────────
# FEATURE IMPORTANCE CHART (XAI)
# ─────────────────────────────────────────
def plot_feature_importance(feat_imp_df):
    top = feat_imp_df.head(15)
    colors = ["#6c5ce7" if i == 0 else "#a29bfe" if i < 3 else "#ddd6fe"
              for i in range(len(top))]
    fig = go.Figure(go.Bar(
        x=top["Importance"],
        y=top["Feature"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:.3f}" for v in top["Importance"]],
        textposition="outside"
    ))
    fig.update_layout(
        title="Feature Importance (Which columns matter most)",
        xaxis_title="Importance score",
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="#0a0a0f",
        paper_bgcolor="#0a0a0f",
        font=dict(color="#ffffff"),
        title_font=dict(size=15, color="#a29bfe"),
        margin=dict(l=10, r=40, t=50, b=30),
        height=400
    )
    return fig


def plot_confusion_matrix(conf_matrix, classes):
    fig = px.imshow(
        conf_matrix,
        labels=dict(x="Predicted", y="Actual", color="Count"),
        x=classes, y=classes,
        color_continuous_scale="Purples",
        title="Confusion Matrix",
        text_auto=True
    )
    fig.update_layout(
        plot_bgcolor="#0a0a0f", paper_bgcolor="#0a0a0f",
        font=dict(color="#fff"),
        title_font=dict(color="#a29bfe")
    )
    return fig


# ─────────────────────────────────────────
# K-MEANS CLUSTERING
# ─────────────────────────────────────────
def run_kmeans(df, col1, col2, n_clusters=3):
    data = df[[col1, col2]].dropna()
    scaler = StandardScaler()
    scaled = scaler.fit_transform(data)

    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(scaled)

    data = data.copy()
    data["Cluster"] = [f"Cluster {l+1}" for l in labels]

    fig = px.scatter(
        data, x=col1, y=col2, color="Cluster",
        title=f"K-Means Clustering — {col1} vs {col2}",
        color_discrete_sequence=["#6c5ce7", "#00b894", "#fdcb6e",
                                  "#e17055", "#a29bfe"],
        template="plotly_dark"
    )
    fig.update_traces(marker=dict(size=8, opacity=0.8))
    fig.update_layout(
        plot_bgcolor="#0a0a0f", paper_bgcolor="#0a0a0f",
        font=dict(color="#fff"),
        title_font=dict(color="#a29bfe"),
        height=420
    )

    cluster_summary = data.groupby("Cluster").agg(
        Count=("Cluster", "count"),
        **{f"Avg {col1}": (col1, lambda x: round(x.mean(), 2))},
        **{f"Avg {col2}": (col2, lambda x: round(x.mean(), 2))}
    ).reset_index()

    return fig, cluster_summary, data


# ─────────────────────────────────────────
# SMART RECOMMENDATIONS ENGINE
# ─────────────────────────────────────────
def get_recommendations(df):
    recs = []
    num_cols = df.select_dtypes(include=np.number).columns

    for col in num_cols:
        # Low variance — drop suggestion
        cv = df[col].std() / (df[col].mean() + 1e-9)
        if abs(cv) < 0.01:
            recs.append({
                "priority": "HIGH",
                "icon": "🗑️",
                "action": f"Drop '{col}'",
                "reason": "Extremely low variance (CV < 1%) — adds no predictive value.",
                "color": "#e17055"
            })

        # Normalization suggestion
        skew = df[col].skew()
        if abs(skew) > 1:
            recs.append({
                "priority": "MEDIUM",
                "icon": "📐",
                "action": f"Normalize '{col}'",
                "reason": f"Skewness = {round(skew,2)}. Apply log or sqrt transform before ML.",
                "color": "#fdcb6e"
            })

        # Outlier suggestion
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        outlier_pct = ((df[col] < Q1-1.5*IQR) | (df[col] > Q3+1.5*IQR)).sum() / len(df) * 100
        if outlier_pct > 10:
            recs.append({
                "priority": "HIGH",
                "icon": "⚠️",
                "action": f"Handle outliers in '{col}'",
                "reason": f"{round(outlier_pct,1)}% of values are outliers — will skew model results.",
                "color": "#e17055"
            })

    # Correlation — multicollinearity
    if len(num_cols) >= 2:
        corr = df[num_cols].corr().abs()
        for i in range(len(corr.columns)):
            for j in range(i+1, len(corr.columns)):
                if corr.iloc[i,j] > 0.9:
                    a, b = corr.columns[i], corr.columns[j]
                    recs.append({
                        "priority": "HIGH",
                        "icon": "🔗",
                        "action": f"Drop one of '{a}' or '{b}'",
                        "reason": f"Correlation = {round(corr.iloc[i,j],2)} — multicollinearity risk.",
                        "color": "#e17055"
                    })

    # Missing values
    for col in df.columns:
        pct = df[col].isnull().sum() / len(df) * 100
        if pct > 40:
            recs.append({
                "priority": "HIGH",
                "icon": "🗑️",
                "action": f"Consider dropping '{col}'",
                "reason": f"{round(pct,1)}% missing — too much data loss to impute reliably.",
                "color": "#e17055"
            })
        elif pct > 10:
            recs.append({
                "priority": "MEDIUM",
                "icon": "🔧",
                "action": f"Impute missing values in '{col}'",
                "reason": f"{round(pct,1)}% missing — use median for numeric, mode for categorical.",
                "color": "#fdcb6e"
            })

    # Encode categoricals
    for col in df.select_dtypes(include="object").columns:
        n_unique = df[col].nunique()
        if n_unique <= 10:
            recs.append({
                "priority": "MEDIUM",
                "icon": "🔢",
                "action": f"Label encode '{col}'",
                "reason": f"{n_unique} unique values — safe to label encode for ML.",
                "color": "#fdcb6e"
            })
        elif n_unique > 50:
            recs.append({
                "priority": "LOW",
                "icon": "💡",
                "action": f"Consider dropping or hashing '{col}'",
                "reason": f"{n_unique} unique values — too many for direct encoding.",
                "color": "#a29bfe"
            })

    if not recs:
        recs.append({
            "priority": "LOW",
            "icon": "✅",
            "action": "Dataset looks ML-ready",
            "reason": "No major preprocessing issues detected.",
            "color": "#00b894"
        })

    # Sort by priority
    order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    recs.sort(key=lambda x: order.get(x["priority"], 3))
    return recs


# ─────────────────────────────────────────
# RESUME MODE
# ─────────────────────────────────────────
def generate_resume_bullet(df, ml_results=None):
    rows = df.shape[0]
    cols = df.shape[1]
    num_cols = len(df.select_dtypes(include=np.number).columns)
    missing_pct = round(df.isnull().sum().sum() / df.size * 100, 1)
    outlier_cols = sum(1 for col in df.select_dtypes(include=np.number).columns
                       if ((df[col] - df[col].mean()).abs() > 3 * df[col].std()).sum() > 0)

    if ml_results:
        model_name = ml_results.get("model_name", "Random Forest")
        metric_label = ml_results.get("metric_label", "Accuracy")
        metric_val = ml_results.get("metric_value", "N/A")
        target = ml_results.get("target", "target column")
        top_feature = ml_results["feature_importance"].iloc[0]["Feature"] if "feature_importance" in ml_results else "key features"

        bullet = f"""• Developed SmartEDA, an AI-powered exploratory data analysis platform using Python, Pandas, Scikit-learn, Plotly, and Streamlit — deployed as a full-stack web application with authentication and real-time analysis.

- Analysed a {rows:,}-row, {cols}-column dataset with {num_cols} numeric features, automated detection of {outlier_cols} outlier-affected columns, and {missing_pct}% missing value handling.

- Implemented a one-click ML pipeline using {model_name} achieving {metric_val} {metric_label} on '{target}' prediction, with explainable AI (XAI) feature importance identifying '{top_feature}' as the most influential predictor.

- Built interactive dashboards with 9 analysis tabs including data cleaning tools, correlation explorer, K-Means clustering, smart recommendations engine, and automated PDF report generation."""

    else:
        bullet = f"""• Developed SmartEDA, an AI-powered exploratory data analysis platform using Python, Pandas, Plotly, and Streamlit — deployed as a full-stack web application with user authentication.

- Automated analysis of {rows:,}-row, {cols}-column datasets — detecting outliers across {outlier_cols} columns, handling {missing_pct}% missing data, and generating professional PDF reports.

- Built 9-tab interactive dashboard with data cleaning tools, correlation explorer, K-Means clustering, rule-based smart recommendations, and auto insight generation — used by live users via Streamlit Cloud."""

    return bullet