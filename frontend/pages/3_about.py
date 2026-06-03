from components.Style import inject_css
import pandas as pd
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="About · F1 Diet",
    page_icon="ℹ️",
    layout="wide",
)
inject_css()

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown(
    '<span class="f1-badge">Project info</span>',
    unsafe_allow_html=True,
)
st.title("About This App")
st.markdown(
    "<h2>Model, dataset, and methodology</h2>",
    unsafe_allow_html=True,
)
st.markdown("<hr class='f1-hr'>", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────

col_main, col_side = st.columns([2, 1], gap="large")

# ─── MAIN COLUMN ─────────────────────────────────────────────────────────────

with col_main:

    # Overview card
    st.markdown(
        """
        <div class="f1-card">
            <div class="f1-label" style="margin-bottom:0.5rem;">Overview</div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;
                        color:#E8E8E8;line-height:1.7;">
                This application uses a machine learning model trained on the
                <strong>F1 Racer Diet Planning Kaggle competition dataset</strong>
                to predict calories burned during a racing or training session,
                then generates a personalised nutrition plan based on that prediction.
                The backend is a FastAPI server; the frontend is built entirely in Python
                using Streamlit.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Dataset KPIs
    st.markdown(
        '<div class="f1-label" style="margin:1.25rem 0 0.5rem;">Dataset</div>',
        unsafe_allow_html=True,
    )
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Training rows",  "750,000")
    d2.metric("Test rows",      "250,000")
    d3.metric("Raw features",   "7")
    d4.metric("Target",         "Calories")

    st.markdown(
        """
        <div style="font-family:'Rajdhani',sans-serif;font-size:0.95rem;color:#888;
                    margin-top:1rem;line-height:1.7;">
            The dataset contains biometric and session data for F1 racers:
            sex, age, height, weight, session duration, heart rate, and body temperature.
            The regression target is <strong style="color:#FFC906;">Calories</strong> —
            the number of calories burned per session.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # All 16 features table
    st.markdown(
        '<div class="f1-label" style="margin:1.5rem 0 0.75rem;">'
        "All 16 model features — from feature_cols.pkl"
        "</div>",
        unsafe_allow_html=True,
    )

    feat_df = pd.DataFrame(
        [
            {
                "Feature":     "Age",
                "Source":      "Raw input",
                "Type":        "int",
                "Description": "Racer age in years",
            },
            {
                "Feature":     "Height",
                "Source":      "Raw input",
                "Type":        "float",
                "Description": "Height in cm",
            },
            {
                "Feature":     "Weight",
                "Source":      "Raw input",
                "Type":        "float",
                "Description": "Weight in kg",
            },
            {
                "Feature":     "Duration",
                "Source":      "Raw input",
                "Type":        "float",
                "Description": "Session duration in minutes",
            },
            {
                "Feature":     "Heart_Rate",
                "Source":      "Raw input",
                "Type":        "float",
                "Description": "Heart rate in BPM during session",
            },
            {
                "Feature":     "Body_Temp",
                "Source":      "Raw input",
                "Type":        "float",
                "Description": "Body temperature in °C",
            },
            {
                "Feature":     "Sex_enc",
                "Source":      "Encoded",
                "Type":        "int",
                "Description": "1 = male, 0 = female",
            },
            {
                "Feature":     "BMI",
                "Source":      "Engineered",
                "Type":        "float",
                "Description": "Weight / (Height / 100)²",
            },
            {
                "Feature":     "Max_HR",
                "Source":      "Engineered",
                "Type":        "float",
                "Description": "220 − Age (age-predicted max heart rate)",
            },
            {
                "Feature":     "HR_Intensity",
                "Source":      "Engineered",
                "Type":        "float",
                "Description": "Heart_Rate / Max_HR",
            },
            {
                "Feature":     "Duration_x_HR",
                "Source":      "Interaction",
                "Type":        "float",
                "Description": "Duration × Heart_Rate (cardiac effort)",
            },
            {
                "Feature":     "Duration_x_Weight",
                "Source":      "Interaction",
                "Type":        "float",
                "Description": "Duration × Weight (work done against body mass)",
            },
            {
                "Feature":     "Duration_x_Temp",
                "Source":      "Interaction",
                "Type":        "float",
                "Description": "Duration × Body_Temp (sustained heat load)",
            },
            {
                "Feature":     "HR_x_Temp",
                "Source":      "Interaction",
                "Type":        "float",
                "Description": "Heart_Rate × Body_Temp (intensity + heat)",
            },
            {
                "Feature":     "Weight_x_HR",
                "Source":      "Interaction",
                "Type":        "float",
                "Description": "Weight × Heart_Rate",
            },
            {
                "Feature":     "Age_Group",
                "Source":      "Binned",
                "Type":        "int",
                "Description": "0 = <25 yrs · 1 = 25–35 · 2 = 35–45 · 3 = 45–55 · 4 = 55+",
            },
        ]
    )

    def _source_style(val):
        return {
            "Raw input":   "color:#E8E8E8",
            "Encoded":     "color:#888888",
            "Engineered":  "color:#FFC906",
            "Interaction": "color:#E10600",
            "Binned":      "color:#39FF14",
        }.get(val, "")

    styled_feat = feat_df.style.map(_source_style, subset=["Source"])
    st.dataframe(styled_feat, use_container_width=True,
                 hide_index=True, height=520)

# ─── SIDE COLUMN ─────────────────────────────────────────────────────────────

with col_side:

    # Model hyperparameters
    st.markdown(
        """
        <div class="f1-card-gold">
            <div class="f1-label" style="margin-bottom:0.75rem;">Model</div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:1.05rem;
                        font-weight:600;color:#E8E8E8;margin-bottom:0.3rem;">
                LightGBM Regressor
            </div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                        color:#888;line-height:2.1;">
                Strategy: XGBoost + LightGBM ensemble<br>
                CV: 5-fold cross-validation<br>
                Early stopping: 100 rounds<br>
                n_estimators: 2 000<br>
                learning_rate: 0.03<br>
                max_depth: 7<br>
                num_leaves: 127<br>
                subsample: 0.85<br>
                colsample_bytree: 0.85
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tech stack
    st.markdown(
        """
        <div class="f1-card">
            <div class="f1-label" style="margin-bottom:0.75rem;">Tech stack</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                        color:#888;line-height:2.1;">
                <span style="color:#E10600;">Backend</span><br>
                FastAPI 0.111<br>
                Uvicorn (ASGI server)<br>
                LightGBM + joblib<br>
                pandas + numpy<br>
                Pydantic v2<br><br>
                <span style="color:#FFC906;">Frontend</span><br>
                Streamlit 1.35<br>
                Rajdhani + JetBrains Mono<br><br>
                <span style="color:#39FF14;">Training</span><br>
                Google Colab (T4 GPU)<br>
                XGBoost + LightGBM<br>
                scikit-learn
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Diet intensity tiers
    st.markdown(
        '<div class="f1-label" style="margin-bottom:0.5rem;">Diet intensity tiers</div>',
        unsafe_allow_html=True,
    )

    for color, tier, rng, desc in [
        (
            "#39FF14", "Low",    "< 100 kcal",
            "Light protein snack within 45 min",
        ),
        (
            "#FFC906", "Medium", "100 – 200 kcal",
            "Carb replenishment within 30 min",
        ),
        (
            "#E10600", "High",   "> 200 kcal",
            "Fast carbs + protein within 20 min",
        ),
    ]:
        st.markdown(
            f"""
            <div style="background:#141414;border:1px solid #2A2A2A;
                        border-left:3px solid {color};padding:0.6rem 0.75rem;
                        margin-bottom:0.4rem;border-radius:2px;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                    <span style="font-family:'Rajdhani',sans-serif;font-weight:700;
                                 color:{color};font-size:0.95rem;">{tier}</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                                 color:#888;">{rng}</span>
                </div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:0.85rem;
                            color:#888;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Dataset link
    st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="f1-card">
            <div class="f1-label" style="margin-bottom:0.5rem;">Kaggle competition</div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:0.9rem;
                        color:#888;line-height:1.6;">
                F1 Racer Diet Planning<br>
                <a href="https://www.kaggle.com/competitions/f-1-racer-diet-planning"
                   target="_blank"
                   style="color:#E10600;font-family:'JetBrains Mono',monospace;
                          font-size:0.65rem;">
                    kaggle.com/competitions/f-1-racer-diet-planning
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
