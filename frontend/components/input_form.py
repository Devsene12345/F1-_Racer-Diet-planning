import streamlit as st


def render_form() -> dict | None:
    """
    Renders the full input form inside a Streamlit form block.
    Returns a dict of inputs on submit, or None if not yet submitted.
    """
    with st.form("prediction_form", clear_on_submit=False):
        st.markdown("#### Racer profile")
        col1, col2 = st.columns(2)

        with col1:
            sex = st.selectbox(
                "Sex",
                options=["male", "female"],
                index=0,
                help="Biological sex (affects BMR calculation)",
            )
            age = st.number_input(
                "Age (years)",
                min_value=15, max_value=80, value=28, step=1,
            )
            height = st.number_input(
                "Height (cm)",
                min_value=140.0, max_value=220.0, value=175.0,
                step=0.5, format="%.1f",
            )
            weight = st.number_input(
                "Weight (kg)",
                min_value=40.0, max_value=160.0, value=70.0,
                step=0.5, format="%.1f",
            )

        with col2:
            st.markdown("#### Session data")
            duration = st.slider(
                "Session duration (min)",
                min_value=1, max_value=300, value=30, step=1,
            )
            max_hr = 220 - int(age)
            heart_rate = st.slider(
                "Heart rate (BPM)",
                min_value=60, max_value=max_hr - 1,
                value=min(140, max_hr - 1), step=1,
                help=f"Max for age {int(age)}: {max_hr} BPM",
            )
            body_temp = st.slider(
                "Body temperature (°C)",
                min_value=36.0, max_value=43.0, value=39.5,
                step=0.1, format="%.1f",
            )

        st.markdown("")
        submitted = st.form_submit_button(
            "🔮 Predict calories & get diet plan",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        return {
            "sex":        sex,
            "age":        int(age),
            "height":     float(height),
            "weight":     float(weight),
            "duration":   float(duration),
            "heart_rate": float(heart_rate),
            "body_temp":  float(body_temp),
        }
    return None
