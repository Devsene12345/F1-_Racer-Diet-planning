from components.Style import inject_css
import pandas as pd
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Dashboard · F1 Diet",
    page_icon="📊",
    layout="wide",
)
inject_css()

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown(
    '<span class="f1-badge">Session history</span>',
    unsafe_allow_html=True,
)
st.title("Performance Dashboard")
st.markdown(
    "<h2>All predictions made this session</h2>",
    unsafe_allow_html=True,
)
st.markdown("<hr class='f1-hr'>", unsafe_allow_html=True)

# ── Empty state ───────────────────────────────────────────────────────────────

history = st.session_state.get("history", [])

if not history:
    st.markdown(
        """
        <div style="
            background:#141414; border:1px dashed #2A2A2A; border-radius:2px;
            padding:4rem 2rem; text-align:center; margin-top:1rem;
        ">
            <div style="font-size:2rem; margin-bottom:1rem;">📊</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                        letter-spacing:3px;text-transform:uppercase;color:#444;">
                No predictions yet
            </div>
            <div style="font-family:'Rajdhani',sans-serif;font-size:1rem;
                        color:#555;margin-top:0.5rem;">
                Go to the Predict page to run your first analysis
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ── Build summary dataframe ───────────────────────────────────────────────────

rows = []
for i, entry in enumerate(history):
    r = entry["result"]
    inp = entry["inputs"]
    rows.append(
        {
            "#":             i + 1,
            "Time":          entry["timestamp"],
            "Calories":      r.calories_burned,
            "Tier":          r.diet_tier.upper(),
            "BMI":           r.bmi,
            "HR %":          r.hr_intensity_pct,
            "Duration (min)": inp["duration"],
            "Heart Rate":    inp["heart_rate"],
            "Body Temp (°C)": inp["body_temp"],
            "Daily Target":  r.meal_plan.daily_target_kcal,
        }
    )

df = pd.DataFrame(rows)

# ── KPI metrics ───────────────────────────────────────────────────────────────

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total predictions",    len(df))
c2.metric("Avg calories burned",  f"{df['Calories'].mean():.0f} kcal")
c3.metric("Max calories burned",  f"{df['Calories'].max():.0f} kcal")
c4.metric("Avg HR intensity",     f"{df['HR %'].mean():.0f}%")

st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

# ── Charts via tabs ───────────────────────────────────────────────────────────

tab1, tab2, tab3 = st.tabs(
    ["Calories trend", "HR vs Calories", "Session table"])

with tab1:
    st.markdown(
        '<div class="f1-label" style="margin-bottom:0.5rem;">'
        "Calories burned — session over session"
        "</div>",
        unsafe_allow_html=True,
    )
    chart_df = df[["#", "Calories"]].set_index("#")
    st.line_chart(
        chart_df,
        use_container_width=True,
        height=280,
        color="#E10600",
    )

with tab2:
    st.markdown(
        '<div class="f1-label" style="margin-bottom:0.5rem;">'
        "Heart rate intensity % vs calories burned"
        "</div>",
        unsafe_allow_html=True,
    )
    scatter_df = df[["HR %", "Calories"]].rename(
        columns={"HR %": "HR intensity (%)", "Calories": "Calories burned"}
    )
    st.scatter_chart(
        scatter_df,
        x="HR intensity (%)",
        y="Calories burned",
        use_container_width=True,
        height=280,
    )

with tab3:
    st.markdown(
        '<div class="f1-label" style="margin-bottom:0.75rem;">All sessions</div>',
        unsafe_allow_html=True,
    )

    def _tier_colour(val):
        if val == "HIGH":
            return "color: #E10600"
        if val == "MEDIUM":
            return "color: #FFC906"
        if val == "LOW":
            return "color: #39FF14"
        return ""

    styled = (
        df.style
        .format(
            {
                "Calories":       "{:.0f}",
                "BMI":            "{:.1f}",
                "HR %":           "{:.0f}%",
                "Daily Target":   "{:.0f}",
                "Body Temp (°C)": "{:.1f}",
            }
        )
        .map(_tier_colour, subset=["Tier"])
    )

    st.dataframe(styled, use_container_width=True, hide_index=True)

# ── Session log ───────────────────────────────────────────────────────────────

st.markdown("<hr class='f1-hr' style='margin-top:1.5rem'>",
            unsafe_allow_html=True)
st.markdown(
    '<div class="f1-label" style="margin-bottom:0.75rem;">Session log</div>',
    unsafe_allow_html=True,
)

_tier_color_map = {
    "low":    "#39FF14",
    "medium": "#FFC906",
    "high":   "#E10600",
}

for entry in reversed(history):
    r = entry["result"]
    color = _tier_color_map.get(r.diet_tier, "#888")
    label = r.diet_tier.upper() + " INTENSITY"

    col_time, col_card = st.columns([1, 8])

    with col_time:
        st.markdown(
            f"""
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                        color:#555;padding-top:0.7rem;">
                {entry['timestamp']}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_card:
        st.markdown(
            f"""
            <div style="
                display:flex; align-items:center; gap:1rem;
                background:#141414; border:1px solid #2A2A2A;
                border-left:3px solid {color};
                padding:0.6rem 1rem; border-radius:2px; margin-bottom:0.4rem;
            ">
                <span style="font-family:'Rajdhani',sans-serif;font-size:1.3rem;
                             font-weight:700;color:#FFC906;min-width:80px;">
                    {r.calories_burned:.0f} kcal
                </span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                             color:{color};letter-spacing:2px;">
                    {label}
                </span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                             color:#888;margin-left:auto;">
                    BMI {r.bmi:.1f} &nbsp;·&nbsp; HR {r.hr_intensity_pct:.0f}%
                    &nbsp;·&nbsp; {r.meal_plan.hydration_ml} ml hydration
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
