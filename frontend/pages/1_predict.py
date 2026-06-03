from frontend.Api_Client import get_prediction
from components.Style import inject_css
from datetime import datetime
import streamlit as st
import sys
import os

# Make the components folder importable from this page file
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Predict · F1 Diet",
    page_icon="🏎️",
    layout="wide",
)
inject_css()

# ── Session state guard ────────────────────────────────────────────────────────

if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ── Page header ───────────────────────────────────────────────────────────────

st.markdown(
    '<span class="f1-badge">Session analysis</span>',
    unsafe_allow_html=True,
)
st.title("Calorie Predictor")
st.markdown(
    "<h2>Enter your biometric and session data below</h2>",
    unsafe_allow_html=True,
)
st.markdown("<hr class='f1-hr'>", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────

left, right = st.columns([1, 1], gap="large")

# ─── LEFT: Input form ────────────────────────────────────────────────────────

with left:
    st.markdown(
        '<div class="f1-label" style="margin-bottom:0.75rem;">Input parameters</div>',
        unsafe_allow_html=True,
    )

    # Sex
    sex = st.radio(
        "Sex",
        options=["male", "female"],
        horizontal=True,
        help="Biological sex — affects BMR calculation",
    )

    st.markdown("<div style='margin-top:0.5rem'></div>",
                unsafe_allow_html=True)

    # Age | Height | Weight
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input(
            "Age (years)",
            min_value=15,
            max_value=80,
            value=28,
            step=1,
        )
    with col2:
        height = st.number_input(
            "Height (cm)",
            min_value=140.0,
            max_value=220.0,
            value=175.0,
            step=0.5,
            format="%.1f",
        )
    with col3:
        weight = st.number_input(
            "Weight (kg)",
            min_value=40.0,
            max_value=160.0,
            value=70.0,
            step=0.5,
            format="%.1f",
        )

    # Duration
    duration = st.slider(
        "Session duration (minutes)",
        min_value=1,
        max_value=120,
        value=30,
        step=1,
    )

    # Heart rate | Body temp
    max_hr = int(220 - age)
    col4, col5 = st.columns(2)
    with col4:
        heart_rate = st.slider(
            f"Heart rate (BPM)  ·  max: {max_hr}",
            min_value=60,
            max_value=max_hr - 1,
            value=min(140, max_hr - 10),
            step=1,
            help=f"Age-predicted max HR = {max_hr} BPM",
        )
    with col5:
        body_temp = st.slider(
            "Body temperature (°C)",
            min_value=36.0,
            max_value=42.5,
            value=39.0,
            step=0.1,
            format="%.1f",
        )

    # Live biometric preview
    bmi_live = weight / ((height / 100) ** 2)
    hr_pct_live = (heart_rate / max_hr) * 100
    bmi_cat = (
        "Underweight" if bmi_live < 18.5
        else "Normal" if bmi_live < 25
        else "Overweight" if bmi_live < 30
        else "Obese"
    )
    bmi_color = (
        "#FFC906" if bmi_cat == "Normal"
        else "#E10600" if bmi_cat in ("Obese", "Underweight")
        else "#888"
    )

    st.markdown(
        f"""
        <div style="
            background:#1C1C1C; border:1px solid #2A2A2A; border-radius:2px;
            padding:0.75rem 1rem; margin-top:0.75rem;
            display:flex; gap:2rem; flex-wrap:wrap;
        ">
            <div>
                <div class="f1-label">BMI</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:1.2rem;
                            font-weight:700;color:{bmi_color};">
                    {bmi_live:.1f}
                    <span style="font-size:0.75rem;color:#888;"> — {bmi_cat}</span>
                </div>
            </div>
            <div>
                <div class="f1-label">Max HR</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:1.2rem;
                            font-weight:700;color:#E8E8E8;">
                    {max_hr} BPM
                </div>
            </div>
            <div>
                <div class="f1-label">HR intensity</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:1.2rem;
                            font-weight:700;color:#E8E8E8;">
                    {hr_pct_live:.0f}%
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
    run = st.button("⚡  Analyse Session", key="run_predict")

# ─── RIGHT: Result display ───────────────────────────────────────────────────

with right:
    st.markdown(
        '<div class="f1-label" style="margin-bottom:0.75rem;">Prediction result</div>',
        unsafe_allow_html=True,
    )
    result_placeholder = st.empty()

    if run:
        with st.spinner("Running prediction..."):
            try:
                result, warning = get_prediction(
                    sex=sex,
                    age=age,
                    height=height,
                    weight=weight,
                    duration=duration,
                    heart_rate=heart_rate,
                    body_temp=body_temp,
                )

                if warning:
                    st.warning(warning)

                # Save to session history
                st.session_state.history.append(
                    {
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "inputs": {
                            "sex": sex, "age": age, "height": height,
                            "weight": weight, "duration": duration,
                            "heart_rate": heart_rate, "body_temp": body_temp,
                        },
                        "result": result,
                    }
                )
                st.session_state.last_result = result

            except Exception as err:
                st.error(f"Prediction failed: {err}")
                st.stop()

    # Render result card
    if st.session_state.last_result:
        r = st.session_state.last_result
        mp = r.meal_plan
        m = mp.macros

        # Tier colours
        tier_color = {
            "low":    "#39FF14",
            "medium": "#FFC906",
            "high":   "#E10600",
        }.get(r.diet_tier, "#888")

        tier_label = {
            "low":    "Low intensity",
            "medium": "Medium intensity",
            "high":   "High intensity",
        }.get(r.diet_tier, r.diet_tier)

        tier_pct = {"low": 25, "medium": 60, "high": 92}.get(r.diet_tier, 50)

        with result_placeholder.container():

            # Hero number
            st.markdown(
                f"""
                <div class="hero-cal">
                    <div class="hc-num">{r.calories_burned:.0f}</div>
                    <div class="hc-unit">kcal burned this session</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Intensity bar
            st.markdown(
                f"""
                <div style="margin-bottom:1.25rem;">
                    <div style="display:flex;justify-content:space-between;
                                align-items:center;margin-bottom:4px;">
                        <span class="f1-label">Session intensity</span>
                        <span style="font-family:'JetBrains Mono',monospace;
                                     font-size:0.65rem;font-weight:600;
                                     color:{tier_color};letter-spacing:2px;">
                            {tier_label.upper()}
                        </span>
                    </div>
                    <div style="background:#1C1C1C;border:1px solid #2A2A2A;
                                border-radius:1px;height:5px;overflow:hidden;">
                        <div style="width:{tier_pct}%;height:100%;
                                    background:{tier_color};border-radius:1px;">
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Biometric metric row
            c1, c2, c3 = st.columns(3)
            c1.metric("BMI",          f"{r.bmi:.1f}")
            c2.metric("HR intensity", f"{r.hr_intensity_pct:.0f}%")
            c3.metric("Daily target", f"{mp.daily_target_kcal:.0f} kcal")

            st.markdown("<div style='margin-top:1rem'></div>",
                        unsafe_allow_html=True)

            # Macros card
            st.markdown(
                f"""
                <div class="f1-card-gold">
                    <div class="f1-label" style="margin-bottom:0.6rem;">
                        Post-session meal macros · {m.total_kcal:.0f} kcal target
                    </div>
                    <div class="macro-row">
                        <div class="macro-pill">
                            <div class="mp-val">{m.protein_g:.0f}g</div>
                            <div class="mp-lbl">Protein</div>
                        </div>
                        <div class="macro-pill">
                            <div class="mp-val">{m.carbs_g:.0f}g</div>
                            <div class="mp-lbl">Carbs</div>
                        </div>
                        <div class="macro-pill">
                            <div class="mp-val">{m.fat_g:.0f}g</div>
                            <div class="mp-lbl">Fat</div>
                        </div>
                        <div class="macro-pill">
                            <div class="mp-val">{mp.hydration_ml} ml</div>
                            <div class="mp-lbl">Hydration</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Meal plan cards
            st.markdown(
                f"""
                <div class="f1-card">
                    <div class="f1-label" style="margin-bottom:0.5rem;">Pre-session</div>
                    <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;
                                color:#E8E8E8;line-height:1.5;">
                        {mp.pre_session}
                    </div>
                </div>
                <div class="f1-card">
                    <div class="f1-label" style="margin-bottom:0.5rem;">Post-session recovery</div>
                    <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;
                                color:#E8E8E8;line-height:1.5;">
                        {mp.post_session}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Advice card
            st.markdown(
                f"""
                <div class="f1-card-green">
                    <div class="f1-label" style="margin-bottom:0.5rem;">Recovery advice</div>
                    <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;
                                color:#E8E8E8;line-height:1.6;">
                        {r.advice}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:
        # Empty state
        result_placeholder.markdown(
            """
            <div style="
                background:#141414; border:1px dashed #2A2A2A; border-radius:2px;
                padding:3rem 2rem; text-align:center; margin-top:1rem;
            ">
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                            letter-spacing:3px;text-transform:uppercase;color:#444;">
                    Awaiting first prediction
                </div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;
                            color:#555;margin-top:0.5rem;">
                    Fill in the form and hit Analyse Session
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Feature engineering expander ──────────────────────────────────────────────

st.markdown("<hr class='f1-hr' style='margin-top:2rem'>",
            unsafe_allow_html=True)

with st.expander("How the model uses your inputs — feature engineering"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            """
            **Raw inputs (7)**
            - `Sex` → encoded as `Sex_enc` (1 = male, 0 = female)
            - `Age`, `Height`, `Weight`
            - `Duration`, `Heart_Rate`, `Body_Temp`
            """
        )
    with col_b:
        st.markdown(
            """
            **Engineered features (9 new)**
            - `BMI` = Weight / (Height/100)²
            - `Max_HR` = 220 − Age
            - `HR_Intensity` = Heart_Rate / Max_HR
            - `Duration_x_HR`, `Duration_x_Weight`
            - `Duration_x_Temp`, `HR_x_Temp`
            - `Weight_x_HR`, `Age_Group` (binned 0–4)
            """
        )
