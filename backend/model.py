import os
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# ── Module-level singletons (populated by load_artifacts) ────────────────────
_model = None
_feature_cols = None
_model_loaded = False


# ── Paths ─────────────────────────────────────────────────────────────────────

MODELS_DIR = Path(os.getenv("MODELS_DIR", Path(__file__).parent / "models"))
MODEL_PATH = MODELS_DIR / "f1_diet_model.pkl"
COLS_PATH = MODELS_DIR / "feature_cols.pkl"


# ── Load ──────────────────────────────────────────────────────────────────────

def load_artifacts() -> None:
    """
    Load model and feature column list into module-level singletons.
    Called once during FastAPI lifespan startup.
    Raises FileNotFoundError if either .pkl file is missing.
    """
    global _model, _feature_cols, _model_loaded

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}\n"
            "Download f1_diet_model.pkl from your Colab training run "
            "and place it in the models/ folder."
        )
    if not COLS_PATH.exists():
        raise FileNotFoundError(
            f"Feature columns file not found: {COLS_PATH}\n"
            "Download feature_cols.pkl from your Colab training run "
            "and place it in the models/ folder."
        )

    _model = joblib.load(MODEL_PATH)
    _feature_cols = joblib.load(COLS_PATH)
    _model_loaded = True

    print(f"  Model     : {MODEL_PATH.name}")
    print(f"  Features  : {len(_feature_cols)} columns -> {_feature_cols}")


def is_loaded() -> bool:
    return _model_loaded


# ── Feature engineering ───────────────────────────────────────────────────────

def engineer_features(
    sex: str,
    age: int,
    height: float,
    weight: float,
    duration: float,
    heart_rate: float,
    body_temp: float,
) -> pd.DataFrame:
    """
    Build the full 16-feature DataFrame from 7 raw inputs.
    Must exactly mirror the engineering done during training.

    Parameters
    ----------
    sex        : 'male' or 'female'
    age        : years
    height     : cm
    weight     : kg
    duration   : session minutes
    heart_rate : BPM
    body_temp  : °C

    Returns
    -------
    pd.DataFrame with columns matching feature_cols.pkl, shape (1, 16)
    """
    row = pd.DataFrame([{
        "Age":        age,
        "Height":     height,
        "Weight":     weight,
        "Duration":   duration,
        "Heart_Rate": heart_rate,
        "Body_Temp":  body_temp,
    }])

    # --- Categorical encoding ---
    row["Sex_enc"] = 1 if sex.lower() == "male" else 0

    # --- Body composition ---
    row["BMI"] = weight / ((height / 100) ** 2)

    # --- Heart rate metrics ---
    row["Max_HR"] = 220 - age
    row["HR_Intensity"] = heart_rate / row["Max_HR"]

    # --- Interaction terms (the main calorie drivers) ---
    row["Duration_x_HR"] = duration * heart_rate
    row["Duration_x_Weight"] = duration * weight
    row["Duration_x_Temp"] = duration * body_temp
    row["HR_x_Temp"] = heart_rate * body_temp
    row["Weight_x_HR"] = weight * heart_rate

    # --- Age group (binned) ---
    row["Age_Group"] = pd.cut(
        row["Age"],
        bins=[0, 25, 35, 45, 55, 100],
        labels=[0, 1, 2, 3, 4],
    ).astype(int)

    # Return only the columns the model was trained on, in the correct order
    return row[_feature_cols]


# ── Inference ─────────────────────────────────────────────────────────────────

def predict_calories(
    sex: str,
    age: int,
    height: float,
    weight: float,
    duration: float,
    heart_rate: float,
    body_temp: float,
) -> float:
    """
    Run model inference and return predicted calories burned.

    Returns
    -------
    float — calories burned (always >= 0)
    """
    if not _model_loaded:
        raise RuntimeError("Model is not loaded. Call load_artifacts() first.")

    X = engineer_features(sex, age, height, weight,
                          duration, heart_rate, body_temp)
    raw = float(_model.predict(X.values)[0])
    return max(0.0, round(raw, 2))


# ── Helper accessors (used by diet_advisor.py) ────────────────────────────────

def calc_bmi(height: float, weight: float) -> float:
    """Return BMI rounded to 1 decimal place."""
    return round(weight / ((height / 100) ** 2), 1)


def calc_hr_intensity_pct(age: int, heart_rate: float) -> float:
    """Return heart rate as a percentage of age-predicted max HR."""
    max_hr = 220 - age
    return round((heart_rate / max_hr) * 100, 1)
