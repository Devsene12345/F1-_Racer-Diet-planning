import streamlit as st

# ── Page config (must be first Streamlit call) ────────────────────────────────

st.set_page_config(
    page_title="F1 Racer Diet Planner",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "F1 Racer Diet Planning — AI-powered calorie & nutrition planner.",
    },
)

# ── Global CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    section[data-testid="stSidebar"] { min-width: 240px; }
    [data-testid="stMetricValue"] { font-size: 2rem !important; font-weight: 600; }
    .block-container { padding-top: 1.5rem; }
    .result-card {
        background: #f8f9fa; border-radius: 12px;
        padding: 1.25rem 1.5rem; border: 1px solid #e9ecef; margin-bottom: 1rem;
    }
    .tier-low    { color: #2e7d32; background: #e8f5e9; padding: 3px 10px;
                   border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
    .tier-medium { color: #e65100; background: #fff3e0; padding: 3px 10px;
                   border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
    .tier-high   { color: #b71c1c; background: #ffebee; padding: 3px 10px;
                   border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
    .macro-pill { display: inline-block; padding: 4px 12px; border-radius: 20px;
                  font-size: 0.82rem; font-weight: 600; margin: 2px; }
    .macro-protein { background: #e3f2fd; color: #1565c0; }
    .macro-carbs   { background: #f3e5f5; color: #6a1b9a; }
    .macro-fat     { background: #fff8e1; color: #f57f17; }
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## F1 Diet Planner")
    st.markdown("---")
    st.markdown("**Navigate**")
    st.page_link("app.py",                  label="Home",      icon="🏠")
    st.page_link("pages/1_predict.py",      label="Predict",   icon="🔮")
    st.page_link("pages/2_dashboard.py",    label="Dashboard", icon="📊")
    st.page_link("pages/3_about.py",        label="About",     icon="ℹ️")
    st.markdown("---")
    st.caption("Powered by LightGBM · FastAPI · Streamlit")

# ── Home page ─────────────────────────────────────────────────────────────────

st.markdown("# F1 Racer Diet Planning")
st.markdown(
    "##### AI-powered calorie prediction and personalised nutrition for racing athletes")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### Predict")
    st.markdown(
        "Enter your biometric and session data to instantly predict "
        "calories burned and receive a tailored diet plan."
    )
    st.page_link("pages/1_predict.py", label="Open predictor →")

with col2:
    st.markdown("### Dashboard")
    st.markdown(
        "Track your prediction history across sessions. "
        "Visualise calorie trends, macro splits, and intensity over time."
    )
    st.page_link("pages/2_dashboard.py", label="Open dashboard →")

with col3:
    st.markdown("### About")
    st.markdown(
        "Learn about the Kaggle dataset, the LightGBM model, "
        "feature engineering, and model performance metrics."
    )
    st.page_link("pages/3_about.py", label="Learn more →")

st.markdown("---")
st.markdown("#### How it works")
cols = st.columns(4)
steps = [
    ("1", "Enter data",     "Fill in 7 biometric & session fields"),
    ("2", "AI predicts",    "LightGBM model estimates calories burned"),
    ("3", "Get plan",       "Receive meal recommendations & macros"),
    ("4", "Track progress", "Log sessions and view your dashboard"),
]
for col, (num, title, desc) in zip(cols, steps):
    with col:
        st.markdown(f"**Step {num} — {title}**")
        st.caption(desc)
