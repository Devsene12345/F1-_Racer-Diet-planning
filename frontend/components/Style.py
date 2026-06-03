import streamlit as st


def inject_css() -> None:
    """Inject the full F1 dark theme CSS into the current page."""
    st.markdown(_CSS, unsafe_allow_html=True)


_CSS = """
<style>
 
/* ── Google Fonts ───────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
 
/* ── CSS Variables ──────────────────────────────────────────────────── */
:root {
    --f1-red    : #E10600;
    --f1-gold   : #FFC906;
    --f1-dark   : #0A0A0A;
    --f1-card   : #141414;
    --f1-card2  : #1C1C1C;
    --f1-border : #2A2A2A;
    --f1-text   : #E8E8E8;
    --f1-muted  : #888888;
    --f1-green  : #39FF14;
}
 
/* ── Base ───────────────────────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--f1-dark) !important;
    font-family: 'Rajdhani', sans-serif !important;
}
[data-testid="stSidebar"] {
    background-color: #0D0D0D !important;
    border-right: 1px solid var(--f1-border) !important;
}
 
/* ── Hide default Streamlit chrome ──────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stToolbar"]    { display: none; }
 
/* ── Headings ───────────────────────────────────────────────────────── */
h1, h2, h3 {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--f1-text) !important;
}
h1 { font-size: 2rem !important; }
h2 { font-size: 1.3rem !important; color: var(--f1-muted) !important; }
 
/* ── Metric cards ───────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background    : var(--f1-card) !important;
    border        : 1px solid var(--f1-border) !important;
    border-top    : 3px solid var(--f1-red) !important;
    padding       : 1rem !important;
    border-radius : 2px !important;
}
[data-testid="metric-container"] label {
    font-family  : 'JetBrains Mono', monospace !important;
    font-size    : 0.6rem !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color        : var(--f1-muted) !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family : 'Rajdhani', sans-serif !important;
    font-weight : 700 !important;
    font-size   : 1.9rem !important;
    color       : var(--f1-gold) !important;
}
 
/* ── Primary button ─────────────────────────────────────────────────── */
.stButton > button {
    background     : var(--f1-red) !important;
    color          : white !important;
    border         : none !important;
    font-family    : 'JetBrains Mono', monospace !important;
    font-size      : 0.72rem !important;
    font-weight    : 600 !important;
    letter-spacing : 3px !important;
    text-transform : uppercase !important;
    padding        : 0.8rem 2rem !important;
    border-radius  : 1px !important;
    width          : 100% !important;
    transition     : background 0.15s !important;
}
.stButton > button:hover   { background: #FF1800 !important; }
.stButton > button:active  { background: #C00500 !important; }
 
/* ── Sliders ────────────────────────────────────────────────────────── */
[data-testid="stSlider"] > div > div > div > div {
    background: var(--f1-red) !important;
}
 
/* ── Selectbox / number input ───────────────────────────────────────── */
[data-baseweb="select"] > div {
    background    : var(--f1-card) !important;
    border        : 1px solid var(--f1-border) !important;
    border-radius : 2px !important;
    color         : var(--f1-text) !important;
}
input[type="number"] {
    background    : var(--f1-card) !important;
    border        : 1px solid var(--f1-border) !important;
    color         : var(--f1-text) !important;
    border-radius : 2px !important;
}
 
/* ── Radio buttons ──────────────────────────────────────────────────── */
[data-testid="stRadio"] label {
    font-family : 'Rajdhani', sans-serif !important;
    font-size   : 1rem !important;
    color       : var(--f1-text) !important;
}
 
/* ── Tabs ───────────────────────────────────────────────────────────── */
[data-baseweb="tab-list"] {
    border-bottom: 1px solid var(--f1-border) !important;
    gap: 0 !important;
}
[data-baseweb="tab"] {
    font-family    : 'JetBrains Mono', monospace !important;
    font-size      : 0.68rem !important;
    letter-spacing : 2px !important;
    text-transform : uppercase !important;
    color          : var(--f1-muted) !important;
    border-bottom  : 2px solid transparent !important;
    padding        : 0.75rem 1.25rem !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    color             : var(--f1-text) !important;
    border-bottom-color: var(--f1-red) !important;
    background        : transparent !important;
}
 
/* ── Expander ───────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background    : var(--f1-card) !important;
    border        : 1px solid var(--f1-border) !important;
    border-radius : 2px !important;
}
[data-testid="stExpander"] summary {
    font-family    : 'JetBrains Mono', monospace !important;
    font-size      : 0.7rem !important;
    letter-spacing : 2px !important;
    text-transform : uppercase !important;
    color          : var(--f1-muted) !important;
}
 
/* ── Sidebar nav ────────────────────────────────────────────────────── */
[data-testid="stSidebarNav"] a {
    font-family    : 'JetBrains Mono', monospace !important;
    font-size      : 0.7rem !important;
    letter-spacing : 2px !important;
    text-transform : uppercase !important;
    color          : var(--f1-muted) !important;
}
[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNav"] a[aria-current="page"] {
    color: var(--f1-red) !important;
}
 
/* ── Dataframe table ────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--f1-border) !important;
}
 
/* ── Alerts / info boxes ────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius    : 2px !important;
    border-left-width: 4px !important;
    font-family      : 'Rajdhani', sans-serif !important;
}
 
/* ───────────────────────────────────────────────────────────────────── */
/*  UTILITY HTML CLASSES  (used with st.markdown unsafe_allow_html=True) */
/* ───────────────────────────────────────────────────────────────────── */
 
/* Cards */
.f1-card {
    background    : var(--f1-card);
    border        : 1px solid var(--f1-border);
    border-left   : 4px solid var(--f1-red);
    padding       : 1.25rem 1.5rem;
    margin-bottom : 1rem;
    border-radius : 2px;
}
.f1-card-gold {
    background    : var(--f1-card);
    border        : 1px solid var(--f1-border);
    border-left   : 4px solid var(--f1-gold);
    padding       : 1.25rem 1.5rem;
    margin-bottom : 1rem;
    border-radius : 2px;
}
.f1-card-green {
    background    : var(--f1-card);
    border        : 1px solid var(--f1-border);
    border-left   : 4px solid var(--f1-green);
    padding       : 1.25rem 1.5rem;
    margin-bottom : 1rem;
    border-radius : 2px;
}
 
/* Labels & values */
.f1-label {
    font-family    : 'JetBrains Mono', monospace;
    font-size      : 0.6rem;
    letter-spacing : 3px;
    text-transform : uppercase;
    color          : #888;
    margin-bottom  : 4px;
}
.f1-value {
    font-family : 'Rajdhani', sans-serif;
    font-size   : 1.6rem;
    font-weight : 700;
    color       : var(--f1-gold);
    line-height : 1.1;
}
 
/* Badges */
.f1-badge {
    display        : inline-block;
    background     : var(--f1-red);
    color          : white;
    font-family    : 'JetBrains Mono', monospace;
    font-size      : 0.58rem;
    font-weight    : 600;
    letter-spacing : 3px;
    text-transform : uppercase;
    padding        : 3px 10px;
    border-radius  : 1px;
}
.f1-badge-gold {
    display        : inline-block;
    background     : var(--f1-gold);
    color          : #0A0A0A;
    font-family    : 'JetBrains Mono', monospace;
    font-size      : 0.58rem;
    font-weight    : 600;
    letter-spacing : 3px;
    text-transform : uppercase;
    padding        : 3px 10px;
    border-radius  : 1px;
}
 
/* Hero calorie display */
.hero-cal { text-align: center; padding: 1.75rem 0 1.25rem; }
.hero-cal .hc-num {
    font-family : 'Rajdhani', sans-serif;
    font-size   : 5rem;
    font-weight : 700;
    color       : var(--f1-gold);
    line-height : 1;
}
.hero-cal .hc-unit {
    font-family    : 'JetBrains Mono', monospace;
    font-size      : 0.7rem;
    letter-spacing : 4px;
    text-transform : uppercase;
    color          : #888;
    margin-top     : 4px;
}
 
/* Macro pills */
.macro-row  { display: flex; gap: 0.75rem; margin: 0.5rem 0; }
.macro-pill {
    flex          : 1;
    background    : var(--f1-card2);
    border        : 1px solid var(--f1-border);
    padding       : 0.5rem;
    border-radius : 2px;
    text-align    : center;
}
.macro-pill .mp-val {
    font-family : 'Rajdhani', sans-serif;
    font-size   : 1.2rem;
    font-weight : 700;
    color       : var(--f1-text);
}
.macro-pill .mp-lbl {
    font-family    : 'JetBrains Mono', monospace;
    font-size      : 0.52rem;
    letter-spacing : 2px;
    text-transform : uppercase;
    color          : #888;
}
 
/* Sidebar logo block */
.sidebar-logo {
    text-align    : center;
    padding       : 1.5rem 0 1rem;
    border-bottom : 1px solid var(--f1-border);
    margin-bottom : 1rem;
}
.sidebar-logo .sl-title {
    font-family    : 'Rajdhani', sans-serif;
    font-size      : 1.1rem;
    font-weight    : 700;
    letter-spacing : 4px;
    text-transform : uppercase;
    color          : var(--f1-red);
}
.sidebar-logo .sl-sub {
    font-family    : 'JetBrains Mono', monospace;
    font-size      : 0.58rem;
    letter-spacing : 3px;
    color          : #555;
    text-transform : uppercase;
    margin-top     : 2px;
}
 
/* Stat boxes (used in dashboard) */
.stat-box {
    background    : var(--f1-card2);
    border        : 1px solid var(--f1-border);
    border-radius : 2px;
    padding       : 0.6rem 0.75rem;
}
.stat-box .sb-lbl {
    font-family    : 'JetBrains Mono', monospace;
    font-size      : 0.55rem;
    letter-spacing : 2px;
    text-transform : uppercase;
    color          : #888;
}
.stat-box .sb-val {
    font-family : 'Rajdhani', sans-serif;
    font-size   : 1.3rem;
    font-weight : 700;
    color       : var(--f1-text);
}
 
/* Horizontal rule */
.f1-hr {
    border     : none;
    border-top : 1px solid var(--f1-border);
    margin     : 1.25rem 0;
}
 
/* Inline code style */
.f1-code {
    font-family   : 'JetBrains Mono', monospace;
    font-size     : 0.75rem;
    background    : var(--f1-card2);
    border        : 1px solid var(--f1-border);
    padding       : 1px 6px;
    border-radius : 2px;
    color         : var(--f1-gold);
}
 
</style>
"""
