import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


# ── Fixtures ──────────────────────────────────────────────────────────────────

VALID_PAYLOAD = {
    "sex":        "male",
    "age":        28,
    "height":     175.0,
    "weight":     70.0,
    "duration":   30.0,
    "heart_rate": 140.0,
    "body_temp":  39.5,
}

FEATURE_COLS = [
    "Age", "Height", "Weight", "Duration", "Heart_Rate", "Body_Temp",
    "Sex_enc", "BMI", "Max_HR", "HR_Intensity",
    "Duration_x_HR", "Duration_x_Weight", "Duration_x_Temp",
    "HR_x_Temp", "Weight_x_HR", "Age_Group",
]


@pytest.fixture
def client():
    """
    Creates a test client with a mocked model.
    Replace the mock with real .pkl files for full integration tests.
    """
    mock_model = MagicMock()
    mock_model.predict.return_value = [152.34]

    with patch("model._model",        mock_model), \
            patch("model._feature_cols", FEATURE_COLS), \
            patch("model._model_loaded", True):

        from main import app
        with TestClient(app) as c:
            yield c


# ── Health check ──────────────────────────────────────────────────────────────

def test_health_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True


# ── Predict — happy path ──────────────────────────────────────────────────────

def test_predict_returns_200(client):
    r = client.post("/predict", json=VALID_PAYLOAD)
    assert r.status_code == 200


def test_predict_response_fields(client):
    body = client.post("/predict", json=VALID_PAYLOAD).json()
    assert "calories_burned" in body
    assert "diet_tier" in body
    assert "bmi" in body
    assert "hr_intensity_pct" in body
    assert "meal_plan" in body
    assert "advice" in body


def test_predict_calories_non_negative(client):
    body = client.post("/predict", json=VALID_PAYLOAD).json()
    assert body["calories_burned"] >= 0


def test_predict_diet_tier_valid(client):
    body = client.post("/predict", json=VALID_PAYLOAD).json()
    assert body["diet_tier"] in ("low", "medium", "high")


def test_predict_meal_plan_fields(client):
    mp = client.post("/predict", json=VALID_PAYLOAD).json()["meal_plan"]
    assert "pre_session" in mp
    assert "post_session" in mp
    assert "hydration_ml" in mp
    assert "daily_target_kcal" in mp
    assert "macros" in mp


def test_predict_macros_positive(client):
    macros = client.post(
        "/predict", json=VALID_PAYLOAD).json()["meal_plan"]["macros"]
    assert macros["protein_g"] > 0
    assert macros["carbs_g"] > 0
    assert macros["fat_g"] > 0
    assert macros["total_kcal"] > 0


def test_predict_female(client):
    payload = {**VALID_PAYLOAD, "sex": "female",
               "height": 163.0, "weight": 58.0}
    r = client.post("/predict", json=payload)
    assert r.status_code == 200


# ── Predict — validation errors ───────────────────────────────────────────────

def test_predict_missing_field(client):
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "age"}
    r = client.post("/predict", json=payload)
    assert r.status_code == 422


def test_predict_age_out_of_range(client):
    r = client.post("/predict", json={**VALID_PAYLOAD, "age": 10})
    assert r.status_code == 422


def test_predict_invalid_sex(client):
    r = client.post("/predict", json={**VALID_PAYLOAD, "sex": "unknown"})
    assert r.status_code == 422


def test_predict_body_temp_too_high(client):
    r = client.post("/predict", json={**VALID_PAYLOAD, "body_temp": 50.0})
    assert r.status_code == 422


def test_predict_heart_rate_exceeds_max(client):
    # age=28 → max HR = 192; sending 195 should fail validation
    r = client.post(
        "/predict", json={**VALID_PAYLOAD, "age": 28, "heart_rate": 195.0})
    assert r.status_code == 422


# ── Feature engineering unit test ─────────────────────────────────────────────

def test_engineer_features_shape():
    with patch("model._model",        MagicMock()), \
            patch("model._feature_cols", FEATURE_COLS), \
            patch("model._model_loaded", True):
        from model import engineer_features
        df = engineer_features("male", 28, 175.0, 70.0, 30.0, 140.0, 39.5)
        assert df.shape == (1, 16)
        assert list(df.columns) == FEATURE_COLS


def test_engineer_features_bmi():
    with patch("model._model",        MagicMock()), \
            patch("model._feature_cols", FEATURE_COLS), \
            patch("model._model_loaded", True):
        from model import engineer_features
        df = engineer_features("female", 35, 160.0, 64.0, 20.0, 120.0, 38.5)
        expected_bmi = 64.0 / (1.60 ** 2)
        assert abs(df["BMI"].iloc[0] - expected_bmi) < 0.01
