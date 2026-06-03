import os
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")
TIMEOUT = 10


def check_health() -> dict | None:
    """Ping GET /health. Returns response dict or None on failure."""
    try:
        r = requests.get(f"{API_BASE}/health", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def predict(
    sex: str,
    age: int,
    height: float,
    weight: float,
    duration: float,
    heart_rate: float,
    body_temp: float,
) -> dict | None:
    """
    POST /predict with the 7 raw user inputs.
    Returns the full PredictResponse dict on success, or None on failure.
    Displays a Streamlit error message automatically on failure.

    Response shape:
    {
        "calories_burned":  float,
        "diet_tier":        "low"|"medium"|"high",
        "bmi":              float,
        "hr_intensity_pct": float,
        "meal_plan": {
            "pre_session":       str,
            "post_session":      str,
            "hydration_ml":      int,
            "daily_target_kcal": float,
            "macros": {
                "protein_g": float, "carbs_g": float,
                "fat_g": float, "total_kcal": float
            }
        },
        "advice": str
    }
    """
    payload = {
        "sex": sex, "age": age, "height": height, "weight": weight,
        "duration": duration, "heart_rate": heart_rate, "body_temp": body_temp,
    }
    try:
        r = requests.post(f"{API_BASE}/predict", json=payload, timeout=TIMEOUT)
        if r.status_code == 422:
            detail = r.json().get("detail", [])
            msgs = [
                f"• {e.get('loc', ['?'])[-1]}: {e.get('msg', '')}"
                for e in (detail if isinstance(detail, list) else [])
            ]
            st.error("Input validation error:\n" +
                     ("\n".join(msgs) if msgs else str(detail)))
            return None
        if r.status_code == 503:
            st.error(
                "The prediction model is not loaded on the backend. "
                "Make sure `f1_diet_model.pkl` is in the `models/` folder and restart the server."
            )
            return None
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error(
            f"Cannot reach the backend at `{API_BASE}`. "
            "Start it with: `uvicorn main:app --reload --port 8000`"
        )
        return None
    except requests.exceptions.Timeout:
        st.error("Request timed out. The backend took too long to respond.")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None
