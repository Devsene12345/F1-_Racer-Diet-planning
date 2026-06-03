import streamlit as st
import pandas as pd

TIER_CONFIG = {
    "low":    {"label": "Low intensity",    "icon": "🟢", "color": "#2e7d32"},
    "medium": {"label": "Medium intensity", "icon": "🟠", "color": "#e65100"},
    "high":   {"label": "High intensity",   "icon": "🔴", "color": "#b71c1c"},
}


def render_result(result: dict, inputs: dict) -> None:
    """
    Render the complete prediction result card.

    Parameters
    ----------
    result : dict  — PredictResponse JSON from the backend
    inputs : dict  — original user inputs (for the session summary)
    """
    calories = result["calories_burned"]
    tier = result["diet_tier"]
    bmi = result["bmi"]
    hr_pct = result["hr_intensity_pct"]
    meal_plan = result["meal_plan"]
    macros = meal_plan["macros"]
    advice = result["advice"]

    st.markdown("---")
    st.markdown("### Your Results")

    # ── Key metrics ───────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Calories burned", f"{calories:.0f} kcal")
    with m2:
        cfg = TIER_CONFIG.get(tier, TIER_CONFIG["medium"])
        st.metric("Session tier", f"{cfg['icon']} {tier.capitalize()}")
    with m3:
        bmi_cat = (
            "Underweight" if bmi < 18.5 else
            "Normal" if bmi < 25.0 else
            "Overweight" if bmi < 30.0 else "Obese"
        )
        st.metric("BMI", f"{bmi:.1f}", delta=bmi_cat, delta_color="off")
    with m4:
        st.metric("HR intensity", f"{hr_pct:.1f}%",
                  help="Heart rate as % of age-predicted max (220 − age)")

    # ── Advice banner ─────────────────────────────────────────────────────────
    tier_color = TIER_CONFIG.get(tier, TIER_CONFIG["medium"])["color"]
    st.markdown(
        f'<div style="border-left:4px solid {tier_color};padding:0.75rem 1rem;'
        f'background:#f8f9fa;border-radius:0 8px 8px 0;margin:1rem 0">'
        f'<strong>Recovery advice</strong><br>{advice}</div>',
        unsafe_allow_html=True,
    )

    # ── Meal plan ─────────────────────────────────────────────────────────────
    st.markdown("#### Meal Plan")
    mp1, mp2 = st.columns(2)

    with mp1:
        st.markdown("**Pre-session meal**")
        st.info(meal_plan["pre_session"])
        st.markdown("**Post-session recovery meal**")
        st.success(meal_plan["post_session"])

    with mp2:
        st.markdown("**Daily targets**")
        d1, d2 = st.columns(2)
        with d1:
            st.metric("Daily calorie target",
                      f"{meal_plan['daily_target_kcal']:,.0f} kcal")
        with d2:
            st.metric("Fluid replacement",
                      f"{meal_plan['hydration_ml'] / 1000:.2f} L")
        st.caption(
            f"BMR × 1.55 activity factor + {calories:.0f} kcal burned today"
        )

    # ── Macros ────────────────────────────────────────────────────────────────
    st.markdown("#### Post-Session Meal Macros")
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.metric("Protein",
                  f"{macros['protein_g']:.1f} g",   help="~30% of meal")
    with mc2:
        st.metric("Carbohydrates",
                  f"{macros['carbs_g']:.1f} g",     help="~45% of meal")
    with mc3:
        st.metric(
            "Fat",           f"{macros['fat_g']:.1f} g",       help="~25% of meal")
    with mc4:
        st.metric("Meal total",    f"{macros['total_kcal']:.0f} kcal")

    macro_df = pd.DataFrame({
        "Macronutrient": ["Protein", "Carbohydrates", "Fat"],
        "Grams":         [macros["protein_g"], macros["carbs_g"], macros["fat_g"]],
    })
    st.bar_chart(macro_df.set_index("Macronutrient"), color=["#378ADD"])

    # ── Session summary expander ──────────────────────────────────────────────
    with st.expander("Session summary", expanded=False):
        st.table(pd.DataFrame({
            "Field": ["Sex", "Age", "Height", "Weight", "Duration", "Heart rate", "Body temp"],
            "Value": [
                inputs["sex"].capitalize(),
                f"{inputs['age']} years",
                f"{inputs['height']:.1f} cm",
                f"{inputs['weight']:.1f} kg",
                f"{inputs['duration']:.0f} min",
                f"{inputs['heart_rate']:.0f} BPM",
                f"{inputs['body_temp']:.1f} °C",
            ],
        }))
