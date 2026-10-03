"""
Loads the trained model + scaler from the /model folder and makes predictions.

This module does not import Django, so it can also be tested on its own.
"""
import json
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"
MODEL_FILE = MODEL_DIR / "heart_disease_model.pkl"
SCALER_FILE = MODEL_DIR / "scaler.pkl"
INFO_FILE = MODEL_DIR / "model_info.json"

FEATURES = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
            "thalach", "exang", "oldpeak", "slope", "ca", "thal"]

LOW_LIMIT = 0.30      # below 30%  -> LOW
HIGH_LIMIT = 0.60     # 60% and up -> HIGH, in between -> MODERATE


class ModelNotAvailable(Exception):
    """Raised when the model files are missing or cannot be loaded."""


_cache = {}


def _load():
    if "model" not in _cache:
        try:
            _cache["model"] = joblib.load(MODEL_FILE)
            _cache["scaler"] = joblib.load(SCALER_FILE)
        except Exception as exc:  # missing file, or pickle from another scikit-learn version
            raise ModelNotAvailable(
                "The prediction model could not be loaded. "
                "Run 'python train_model.py' in the project folder and restart the server."
            ) from exc
    return _cache["model"], _cache["scaler"]


def risk_level(probability):
    """probability is a number between 0 and 1."""
    if probability < LOW_LIMIT:
        return "LOW"
    if probability < HIGH_LIMIT:
        return "MODERATE"
    return "HIGH"


def predict_probability(values):
    """values: dict with the 13 feature names. Returns probability (0-1) of heart disease."""
    model, scaler = _load()
    row = pd.DataFrame([[values[name] for name in FEATURES]], columns=FEATURES)
    scaled = scaler.transform(row)
    return float(model.predict_proba(scaled)[0][1])


def model_info():
    """Details written by train_model.py (empty dict if the file does not exist)."""
    try:
        return json.loads(INFO_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
