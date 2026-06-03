from enum import Enum
from pydantic import BaseModel, Field, field_validator


# ── Enums ─────────────────────────────────────────────────────────────────────

class SexEnum(str, Enum):
    male = "male"
    female = "female"


class DietTier(str, Enum):
    low = "low"       # < 100 kcal burned
    medium = "medium"    # 100–200 kcal burned
    high = "high"      # > 200 kcal burned


# ── Request ───────────────────────────────────────────────────────────────────

class PredictRequest(BaseModel):
    """
    Raw user inputs — exactly the 7 fields a user fills in on the website.
    All feature engineering happens server-side in model.py.
    """
    sex:        SexEnum = Field(...,
                                description="Biological sex", example="male")
    age:        int = Field(..., ge=15,  le=80,
                            description="Age in years",        example=28)
    height:     float = Field(..., ge=140, le=220,
                              description="Height in cm",         example=175.0)
    weight:     float = Field(..., ge=40,  le=160,
                              description="Weight in kg",         example=70.0)
    duration:   float = Field(..., ge=1,   le=300,
                              description="Session duration (min)", example=30.0)
    heart_rate: float = Field(..., ge=60,  le=220,
                              description="Heart rate in BPM",   example=140.0)
    body_temp:  float = Field(..., ge=36,  le=43,
                              description="Body temperature °C", example=39.5)

    @field_validator("heart_rate")
    @classmethod
    def heart_rate_below_max(cls, v, info):
        """Heart rate must be less than age-predicted maximum (220 - age)."""
        age = info.data.get("age")
        if age and v >= (220 - age):
            raise ValueError(
                f"Heart rate {v} BPM must be below age-predicted max "
                f"({220 - age} BPM for age {age})"
            )
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "sex": "male",
                "age": 28,
                "height": 175.0,
                "weight": 70.0,
                "duration": 30.0,
                "heart_rate": 140.0,
                "body_temp": 39.5,
            }
        }
    }


# ── Meal sub-models ───────────────────────────────────────────────────────────

class Macros(BaseModel):
    protein_g:  float = Field(..., description="Protein in grams")
    carbs_g:    float = Field(..., description="Carbohydrates in grams")
    fat_g:      float = Field(..., description="Fat in grams")
    total_kcal: float = Field(..., description="Total meal calories")


class MealPlan(BaseModel):
    pre_session:  str = Field(..., description="Recommended pre-session meal")
    post_session: str = Field(...,
                              description="Recommended post-session recovery meal")
    hydration_ml: int = Field(...,
                              description="Estimated fluid replacement in ml")
    daily_target_kcal: float = Field(...,
                                     description="Recommended total daily calories")
    macros:       Macros


# ── Response ──────────────────────────────────────────────────────────────────

class PredictResponse(BaseModel):
    """Full prediction result returned to the frontend."""
    calories_burned:    float = Field(...,
                                      description="Predicted calories burned (kcal)")
    diet_tier:          DietTier = Field(...,
                                         description="Session intensity tier")
    bmi:                float = Field(..., description="Calculated BMI")
    hr_intensity_pct:   float = Field(...,
                                      description="Heart rate as % of predicted max HR")
    meal_plan:          MealPlan
    advice:             str = Field(...,
                                    description="Personalised recovery advice")

    model_config = {
        "json_schema_extra": {
            "example": {
                "calories_burned": 152.34,
                "diet_tier": "medium",
                "bmi": 22.9,
                "hr_intensity_pct": 74.1,
                "meal_plan": {
                    "pre_session": "Banana + oat bar (1–2 hrs before)",
                    "post_session": "Grilled chicken, white rice, steamed broccoli",
                    "hydration_ml": 600,
                    "daily_target_kcal": 2652.34,
                    "macros": {
                        "protein_g": 38.1,
                        "carbs_g": 57.1,
                        "fat_g": 12.7,
                        "total_kcal": 500.0,
                    },
                },
                "advice": "Good medium-intensity session. Prioritise carbohydrate replenishment within 30 minutes.",
            }
        }
    }


# ── Health check ──────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status:       str = Field(..., example="ok")
    model_loaded: bool
    version:      str = Field(..., example="1.0.0")
