"""
Trains the heart disease model and saves it for the Django app.

Run from the project folder:   python train_model.py

Output (in /model):
    heart_disease_model.pkl   the selected classifier
    scaler.pkl                the fitted StandardScaler
    model_info.json           metrics and details shown on the home page
"""
import json
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

BASE_DIR = Path(__file__).resolve().parent
DATASET = BASE_DIR / "dataset" / "heart.csv"
DEMO_MARKER = BASE_DIR / "dataset" / "DEMO_DATA.txt"
MODEL_DIR = BASE_DIR / "model"

FEATURES = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
            "thalach", "exang", "oldpeak", "slope", "ca", "thal"]


def load_data():
    df = pd.read_csv(DATASET).drop_duplicates()
    for name in ("target", "condition", "num"):        # target column name differs between copies
        if name in df.columns:
            df = df.rename(columns={name: "target"})
            break
    missing = [c for c in FEATURES + ["target"] if c not in df.columns]
    if missing:
        raise SystemExit(f"heart.csv is missing these columns: {missing}")
    df["target"] = (df["target"] > 0).astype(int)        # 1 = heart disease present
    df = df.dropna(subset=FEATURES + ["target"])
    return df[FEATURES], df["target"]


def main():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42)

    candidates = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=7),
        "Support Vector Machine": SVC(probability=True, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=4, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    }

    # Choose the model by 5-fold cross-validation on the TRAINING data only
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = {}
    for name, clf in candidates.items():
        pipe = make_pipeline(StandardScaler(), clf)
        cv_scores[name] = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="roc_auc").mean()
        print(f"{name:<24} CV ROC-AUC = {cv_scores[name]:.3f}")

    best_name = max(cv_scores, key=cv_scores.get)
    print("\nSelected model:", best_name)

    # Final training: scaler and classifier are saved separately
    scaler = StandardScaler().fit(X_train)
    model = candidates[best_name].fit(scaler.transform(X_train), y_train)

    X_test_scaled = scaler.transform(X_test)
    pred = model.predict(X_test_scaled)
    prob = model.predict_proba(X_test_scaled)[:, 1]
    metrics = {
        "accuracy": round(accuracy_score(y_test, pred), 3),
        "precision": round(precision_score(y_test, pred), 3),
        "recall": round(recall_score(y_test, pred), 3),
        "f1": round(f1_score(y_test, pred), 3),
        "roc_auc": round(roc_auc_score(y_test, prob), 3),
    }
    print("Test-set metrics:", metrics)

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "heart_disease_model.pkl")
    joblib.dump(scaler, MODEL_DIR / "scaler.pkl")
    info = {
        "best_model": best_name,
        "features": FEATURES,
        "rows": int(len(X)),
        "cv_roc_auc": {k: round(v, 3) for k, v in cv_scores.items()},
        "metrics": metrics,
        "demo_data": DEMO_MARKER.exists(),
        "scikit_learn": sklearn.__version__,
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    (MODEL_DIR / "model_info.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    print("Saved model files in", MODEL_DIR)
    if info["demo_data"]:
        print("\nNOTE: DEMO_DATA.txt exists, so the model was trained on synthetic demo data.")


if __name__ == "__main__":
    main()
