"""
HealthTrackAI — Main Streamlit Application
Run: streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="HealthTrackAI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# PWA & STARTUP POPUP
# ══════════════════════════════════════════════════════════════════════════════
if "startup_popup_shown" not in st.session_state:
    st.session_state.startup_popup_shown = False

# Check if running in standalone mode (PWA) or already visited via query param
if st.query_params.get("mode") == "standalone" or st.query_params.get("visited") == "true":
    st.session_state.startup_popup_shown = True

@st.dialog("Welcome to HealthTrackAI 🧬")
def show_startup_popup():
    st.markdown("""
    <div style="text-align:center">
        <div style="font-size:60px;margin-bottom:10px">👋</div>
        <h3 style="color:#00C9A7">Your AI Health Companion</h3>
        <p style="color:#8899AA;font-size:15px;margin-bottom:20px">
            Analyze lab reports, track vitals, and get personalized health insights instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # PWA Install hint
    st.info("📲 **To Install App:** Tap 'Share' → 'Add to Home Screen' on iOS, or 'Install App' on Chrome/Android.")
    
    if st.button("Get Started 🚀", type="primary", use_container_width=True):
        st.session_state.startup_popup_shown = True
        st.query_params["visited"] = "true"
        st.rerun()

if not st.session_state.startup_popup_shown:
    show_startup_popup()

# Service Worker Registration
st.markdown("""
<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/app/static/sw.js').then(function(registration) {
      console.log('ServiceWorker registration successful with scope: ', registration.scope);
    }, function(err) {
      console.log('ServiceWorker registration failed: ', err);
    });
  });
}
</script>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — The design system
# ══════════════════════════════════════════════════════════════════════════════
# PWA Support Link
st.markdown('<link rel="manifest" href="app/static/manifest.json">', unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #080D18 !important;
    color: #E8EDF5 !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }
header { 
    background-color: transparent !important;
}
.stDeployButton { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1628 0%, #080D18 100%) !important;
    border-right: 1px solid rgba(0,201,167,0.12) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
section[data-testid="stSidebar"] .block-container { padding: 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,201,167,0.25); border-radius: 10px; }

/* ── Main container ── */
.main .block-container {
    padding: 0 2rem 2rem 2rem !important;
    max-width: 100% !important;
}

/* ── Metric override ── */
[data-testid="metric-container"] {
    background: #0F1A2E !important;
    border: 1px solid rgba(0,201,167,0.15) !important;
    border-radius: 14px !important;
    padding: 18px !important;
}
[data-testid="metric-container"] label { color: #8899AA !important; font-size: 12px !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #E8EDF5 !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    border: none !important;
    transition: all 0.2s ease !important;
    padding: 8px 18px !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00C9A7, #0096FF) !important;
    color: white !important;
    box-shadow: 0 4px 20px rgba(0,201,167,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 25px rgba(0,201,167,0.45) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(0,201,167,0.08) !important;
    color: #00C9A7 !important;
    border: 1px solid rgba(0,201,167,0.25) !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(0,201,167,0.15) !important;
    border-color: #00C9A7 !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(0,201,167,0.03) !important;
    border: 2px dashed rgba(0,201,167,0.25) !important;
    border-radius: 16px !important;
    padding: 8px !important;
    transition: all 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,201,167,0.5) !important;
    background: rgba(0,201,167,0.06) !important;
}

/* ── Text inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #0F1A2E !important;
    border: 1px solid rgba(0,201,167,0.2) !important;
    border-radius: 10px !important;
    color: #E8EDF5 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #00C9A7 !important;
    box-shadow: 0 0 0 3px rgba(0,201,167,0.12) !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] > div {
    background: #0F1A2E !important;
    border: 1px solid rgba(0,201,167,0.25) !important;
    border-radius: 14px !important;
}
[data-testid="stChatInput"] textarea {
    color: #E8EDF5 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Progress bars ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00C9A7, #0096FF) !important;
    border-radius: 10px !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #0F1A2E !important;
    border: 1px solid rgba(0,201,167,0.12) !important;
    border-radius: 12px !important;
    color: #E8EDF5 !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: #0A1628 !important;
    border: 1px solid rgba(0,201,167,0.08) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0F1A2E !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(0,201,167,0.1) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #8899AA !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0,201,167,0.2), rgba(0,150,255,0.15)) !important;
    color: #00C9A7 !important;
    font-weight: 600 !important;
}

/* ── Divider ── */
hr { border-color: rgba(0,201,167,0.1) !important; margin: 1.2rem 0 !important; }

/* ── Alerts ── */
.stAlert {
    background: #0F1A2E !important;
    border-radius: 12px !important;
    border-left-width: 3px !important;
}
.stSuccess { border-left-color: #00C9A7 !important; }
.stError   { border-left-color: #FF4B6E !important; }
.stWarning { border-left-color: #FFAA00 !important; }
.stInfo    { border-left-color: #0096FF !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] > div { border-top-color: #00C9A7 !important; }

/* ══════════════════════════════════════════════════════════════ */
/* CUSTOM COMPONENTS                                             */
/* ══════════════════════════════════════════════════════════════ */

/* ── Page header banner ── */
.page-header {
    background: linear-gradient(135deg, #0A1628 0%, #0F1E35 50%, #091428 100%);
    border: 1px solid rgba(0,201,167,0.15);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.page-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(0,201,167,0.08), transparent 70%);
    pointer-events: none;
}
.page-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 20%;
    width: 250px; height: 150px;
    background: radial-gradient(circle, rgba(0,150,255,0.06), transparent 70%);
    pointer-events: none;
}
.page-header h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    margin: 0 0 6px 0 !important;
    background: linear-gradient(135deg, #FFFFFF, #A8C8FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.page-header p {
    font-size: 14px !important;
    color: #6A8099 !important;
    margin: 0 !important;
}

/* ── Score ring ── */
.score-ring-wrap {
    display: flex; flex-direction: column; align-items: center;
    background: linear-gradient(135deg, #0A1628, #0F1E35);
    border: 1px solid rgba(0,201,167,0.15);
    border-radius: 20px; padding: 24px;
}
.score-big {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 56px; font-weight: 700;
    line-height: 1;
}
.score-label-text { font-size: 13px; color: #8899AA; margin-top: 4px; }

/* ── Stat card ── */
.stat-card {
    background: #0F1A2E;
    border: 1px solid rgba(0,201,167,0.12);
    border-radius: 16px; padding: 20px;
    transition: border-color 0.2s, transform 0.2s;
    height: 100%;
}
.stat-card:hover { border-color: rgba(0,201,167,0.3); transform: translateY(-2px); }
.stat-card .icon { font-size: 26px; margin-bottom: 10px; }
.stat-card .value { font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 700; }
.stat-card .label { font-size: 12px; color: #6A8099; margin-top: 4px; font-weight: 500; letter-spacing: 0.04em; text-transform: uppercase; }

/* ── Report item card ── */
.report-card {
    background: #0F1A2E;
    border: 1px solid rgba(0,201,167,0.1);
    border-left: 4px solid #00C9A7;
    border-radius: 0 14px 14px 0;
    padding: 16px 20px;
    margin-bottom: 10px;
    transition: all 0.2s;
}
.report-card:hover { border-left-color: #0096FF; background: #111E33; }
.report-card .rc-name { font-weight: 600; font-size: 14px; }
.report-card .rc-meta { font-size: 12px; color: #6A8099; margin-top: 4px; }

/* ── Chat bubble ── */
.chat-user {
    background: linear-gradient(135deg, #1A2E50, #162540);
    border: 1px solid rgba(0,150,255,0.2);
    border-radius: 18px 4px 18px 18px;
    padding: 14px 18px; margin: 6px 0;
    margin-left: 12%; font-size: 14px; line-height: 1.75;
    position: relative;
}
.chat-ai {
    background: linear-gradient(135deg, #0A1628, #0F1E35);
    border: 1px solid rgba(0,201,167,0.15);
    border-radius: 4px 18px 18px 18px;
    padding: 14px 18px; margin: 6px 0;
    margin-right: 6%; font-size: 14px; line-height: 1.75;
}
.chat-avatar {
    font-size: 18px;
    display: inline-flex; align-items: center; justify-content: center;
    width: 32px; height: 32px;
    background: linear-gradient(135deg,rgba(0,201,167,0.2),rgba(0,150,255,0.2));
    border: 1px solid rgba(0,201,167,0.3);
    border-radius: 8px; margin-bottom: 6px;
}

/* ── Badge ── */
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.04em;
}
.badge-ok   { background: rgba(0,201,167,0.12); color: #00C9A7; }
.badge-warn { background: rgba(255,170,0,0.12);  color: #FFAA00; }
.badge-high { background: rgba(255,75,110,0.12); color: #FF4B6E; }
.badge-info { background: rgba(0,150,255,0.12);  color: #0096FF; }

/* ── Finding card ── */
.finding-row {
    display: flex; align-items: center; justify-content: space-between;
    background: #0A1628;
    border: 1px solid rgba(0,201,167,0.08);
    border-radius: 10px; padding: 12px 16px; margin-bottom: 8px;
}
.finding-name { font-size: 13px; font-weight: 600; }
.finding-val  { font-size: 14px; font-weight: 700; font-family: 'Space Grotesk', sans-serif; }
.finding-range { font-size: 11px; color: #6A8099; }

/* ── Quick pill button ── */
.pill-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0; }
.pill {
    background: rgba(0,201,167,0.08); border: 1px solid rgba(0,201,167,0.2);
    border-radius: 20px; padding: 6px 14px;
    font-size: 12px; font-weight: 500; color: #00C9A7;
    cursor: pointer; transition: all 0.15s; display: inline-block;
}
.pill:hover { background: rgba(0,201,167,0.18); border-color: #00C9A7; }

/* ── Risk item ── */
.risk-item {
    background: rgba(255,75,110,0.05);
    border-left: 3px solid #FF4B6E;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px; margin-bottom: 8px;
}
.risk-item.medium { background: rgba(255,170,0,0.05); border-left-color: #FFAA00; }
.risk-item.low    { background: rgba(0,201,167,0.05); border-left-color: #00C9A7; }

/* ── Med card ── */
.med-card {
    background: rgba(128,90,213,0.07);
    border-left: 3px solid #805AD5;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px; margin-bottom: 8px;
}

/* ── Habit card ── */
.habit-card {
    background: rgba(0,150,255,0.05);
    border-left: 3px solid #0096FF;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px; margin-bottom: 8px;
}

/* ── Sidebar logo ── */
.sidebar-logo {
    padding: 24px 20px 16px;
    border-bottom: 1px solid rgba(0,201,167,0.1);
    margin-bottom: 8px;
}
.sidebar-logo .brand {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px; font-weight: 700;
    background: linear-gradient(135deg, #00C9A7, #0096FF);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.sidebar-logo .tagline { font-size: 11px; color: #4A6080; margin-top: 2px; letter-spacing: 0.06em; }

/* ── Status pill ── */
.status-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 10px; border-radius: 20px;
    font-size: 11px; font-weight: 600;
}
.status-on  { background: rgba(0,201,167,0.12); color: #00C9A7; }
.status-off { background: rgba(255,75,110,0.12); color: #FF4B6E; }
.status-warn{ background: rgba(255,170,0,0.12);  color: #FFAA00; }
.pulse { width: 6px; height: 6px; border-radius: 50%; background: currentColor;
         animation: pulse-anim 2s infinite; }
@keyframes pulse-anim {
    0%,100% { opacity: 1; } 50% { opacity: 0.3; }
}

/* ── Welcome card ── */
.welcome-card {
    background: linear-gradient(135deg, #0A1628 0%, #0E1F38 60%, #091428 100%);
    border: 1px solid rgba(0,201,167,0.15);
    border-radius: 20px; padding: 32px;
    text-align: center; margin-bottom: 24px;
    position: relative; overflow: hidden;
}
.welcome-card .glow {
    position: absolute; top: -60px; left: 50%; transform: translateX(-50%);
    width: 300px; height: 200px;
    background: radial-gradient(ellipse, rgba(0,201,167,0.1), transparent 70%);
    pointer-events: none;
}

/* ── Section title ── */
.section-title {
    font-size: 11px; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #4A6080;
    margin: 16px 0 10px; padding-left: 2px;
}

/* ── Nav item ── */
.nav-item {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 16px; border-radius: 10px;
    cursor: pointer; transition: all 0.15s;
    font-size: 14px; font-weight: 500; color: #6A8099;
    margin: 2px 0;
}
.nav-item:hover { background: rgba(0,201,167,0.07); color: #E8EDF5; }
.nav-item.active {
    background: linear-gradient(135deg, rgba(0,201,167,0.15), rgba(0,150,255,0.1));
    color: #00C9A7; font-weight: 600;
    border: 1px solid rgba(0,201,167,0.2);
}

/* ── Upload zone custom ── */
.upload-hint {
    text-align: center; padding: 8px;
    font-size: 12px; color: #4A6080;
}

/* ── Analysis block ── */
.analysis-content {
    font-size: 14px; line-height: 1.8; color: #CDD9E8;
}
.analysis-content h3 { color: #00C9A7 !important; font-size: 15px !important;
                        margin: 20px 0 10px !important; font-weight: 600 !important; }
.analysis-content strong { color: #E8EDF5 !important; }
.analysis-content li { margin: 4px 0 !important; }

/* ── Disclaimer box ── */
.disclaimer {
    background: rgba(255,170,0,0.06); border: 1px solid rgba(255,170,0,0.2);
    border-radius: 12px; padding: 12px 16px; margin-top: 16px;
    font-size: 12px; color: #FFAA00;
}

/* ── Tesseract info ── */
.ocr-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(0,150,255,0.08); border: 1px solid rgba(0,150,255,0.2);
    border-radius: 8px; padding: 4px 10px;
    font-size: 11px; color: #0096FF; font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "logged_in": False, "username": None,
        "user_id": None, "user_name": "Friend", "user_age": 0, "user_gender": "",
        "chat_history": [], "session_id": "s001",
        "current_page": "chat", "uploaded_reports": [],
        "analysis_result": None, "show_analysis": False,
        "role": "user",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ══════════════════════════════════════════════════════════════════════════════
import os, sys
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Cloud compatibility: Inject secrets into environment
try:
    # Safely check if running in Streamlit and secrets are available
    if hasattr(st, "secrets"):
        for key in ["GOOGLE_API_KEY", "MONGODB_URI", "MONGODB_DB", "ADMIN_USERNAME", "ADMIN_EMAIL"]:
            if key in st.secrets and key not in os.environ:
                os.environ[key] = st.secrets[key]
except Exception:
    pass

sys.path.insert(0, os.path.dirname(__file__))

from utils.database import (
    ping_db, upsert_user, get_user, get_reports, get_latest_health_score,
    get_health_scores, save_report, save_health_score,
    save_message, get_chat_history, clear_chat_history, delete_report,
    get_all_users, log_operation, get_logs,
    create_user, authenticate_user,
    update_user_role, delete_user_full, get_system_stats
)
from utils.file_parser import extract_text_from_file, detect_report_type, get_report_icon, extract_from_url
from agents.health_agent import get_agent

API_OK = bool(os.getenv("GOOGLE_API_KEY","") not in ("","your_google_gemini_api_key_here"))
DB_OK  = ping_db()

# ══════════════════════════════════════════════════════════════════════════════
# DATA HOOKS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=300)
def _cached_reports(user_id, is_db_ok):
    if not is_db_ok: return st.session_state.get("uploaded_reports", [])
    return get_reports(user_id)

@st.cache_data(ttl=600)
def _cached_score(user_id, is_db_ok):
    if not is_db_ok: return None
    return get_latest_health_score(user_id)

@st.cache_data(ttl=3600)
def _cached_user(user_id, is_db_ok):
    if not is_db_ok: return {}
    return get_user(user_id)

if not st.session_state.logged_in:
    tab_si, tab_su = st.tabs(["🔐 Sign In", "📝 Create Account"])
    with tab_si:
        st.markdown('<div class="page-header"><h1>🔐 Sign In</h1><p>Welcome back to HealthTrackAI</p></div>', unsafe_allow_html=True)
        si_user = st.text_input("Username", key="si_u")
        si_pass = st.text_input("Password", type="password", key="si_p")
        if st.button("Sign In", type="primary", use_container_width=True):
            if not DB_OK:
                st.error("MongoDB is offline — Authentication requires database access.")
            else:
                user = authenticate_user(si_user, si_pass)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user["username"]
                    st.session_state.user_id = str(user.get("user_id", user["username"]))
                    st.session_state.user_name = user.get("name", "Friend")
                    st.session_state.user_age = user.get("age", 0)
                    st.session_state.user_gender = user.get("gender", "")
                    st.session_state.role = user.get("role", "user")
                    log_operation(st.session_state.user_id, "Sign In", "Success")
                    st.success(f"Welcome back, {st.session_state.user_name}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    with tab_su:
        st.markdown('<div class="page-header"><h1>📝 Create Account</h1><p>Join HealthTrackAI today</p></div>', unsafe_allow_html=True)
        su_name = st.text_input("Full Name", key="su_n")
        su_user = st.text_input("Username", key="su_u")
        su_email = st.text_input("Email", key="su_e")
        su_pass = st.text_input("Password", type="password", key="su_p")
        if st.button("Create Account", type="primary", use_container_width=True):
            if not DB_OK:
                st.error("MongoDB is offline — Registration requires database access.")
            elif not su_user or not su_pass or not su_name:
                st.warning("Please fill in required fields")
            else:
                user = create_user(su_user, su_pass, su_name, su_email)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = user["username"]
                    st.session_state.user_id = str(user.get("user_id", user["username"]))
                    st.session_state.user_name = user.get("name", "Friend")
                    st.session_state.user_age = user.get("age", 0)
                    st.session_state.user_gender = user.get("gender", "")
                    st.session_state.role = user.get("role", "user")
                    log_operation(st.session_state.user_id, "Account Created", "Success")
                    st.success("Account created! Welcome.")
                    st.rerun()
                else:
                    st.error("Username already taken")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # ── Logo ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:28px;margin-bottom:6px">🧬</div>
        <div class="brand">HealthTrackAI</div>
        <div class="tagline">INTELLIGENT HEALTH COMPANION</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Status pills ──────────────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    c1.markdown(f'<div class="status-pill {"status-on" if API_OK else "status-off"}"><span class="pulse"></span>{"Gemini 3.1 Flash Lite ✓" if API_OK else "No API Key"}</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="status-pill {"status-on" if DB_OK else "status-warn"}"><span class="pulse"></span>{"MongoDB ✓" if DB_OK else "Offline"}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not API_OK:
        st.warning("⚠️ Add GOOGLE_API_KEY to your .env file")

    # ── Health Score ───────────────────────────────────────────────────────────
    score_data = _cached_score(st.session_state.user_id, DB_OK)
    if not score_data and st.session_state.uploaded_reports:
        scores = [r.get("health_score", 0) for r in st.session_state.uploaded_reports if r.get("health_score")]
        if scores:
            score_data = {"score": int(sum(scores)/len(scores)), "breakdown": {}}

    if score_data:
        score = score_data["score"]
        if score >= 75:   color, emoji, lbl = "#00C9A7", "🟢", "Good Health"
        elif score >= 55: color, emoji, lbl = "#FFAA00", "🟡", "Fair Health"
        else:             color, emoji, lbl = "#FF4B6E", "🔴", "Needs Attention"

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0A1628,#0F1E35);
                    border:1px solid rgba(0,201,167,0.15);border-radius:18px;
                    padding:20px;text-align:center;margin-bottom:4px">
            <div style="font-size:12px;color:#6A8099;letter-spacing:.08em;
                        text-transform:uppercase;font-weight:600;margin-bottom:8px">
                Health Score
            </div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:52px;
                        font-weight:800;color:{color};line-height:1">{score}</div>
            <div style="font-size:13px;color:{color};margin-top:6px;font-weight:600">
                {emoji} {lbl}
            </div>
        </div>
        """, unsafe_allow_html=True)

        bd = score_data.get("breakdown", {})
        if bd:
            vitals = bd.get("vitals", 70)
            nutrition = bd.get("nutrition", 65)
            risk = bd.get("risk", 40)
            st.markdown('<div style="font-size:11px;color:#4A6080;margin:12px 0 6px;font-weight:600">BREAKDOWN</div>', unsafe_allow_html=True)
            st.progress(vitals/100, text=f"💓 Vitals — {vitals}%")
            st.progress(nutrition/100, text=f"🥗 Nutrition — {nutrition}%")
            st.progress(risk/100, text=f"⚠️ Risk Level — {risk}%")
    else:
        st.markdown("""
        <div style="background:#0F1A2E;border:1px dashed rgba(0,201,167,0.15);
                    border-radius:14px;padding:20px;text-align:center;margin-bottom:4px">
            <div style="font-size:24px;margin-bottom:8px">📊</div>
            <div style="font-size:13px;color:#4A6080">Upload a report to<br>calculate your Health Score</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Navigation ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)
    
    if st.session_state.get("role") == "admin":
        nav_items = [
            ("admin", "🔒", "Admin Panel"),
            ("settings","⚙️", "Settings"),
        ]
        # Force switch if on user page
        if st.session_state.current_page in ["chat", "upload", "reports", "trends", "profile"]:
            st.session_state.current_page = "admin"
            st.rerun()
    else:
        nav_items = [
            ("chat",    "💬", "AI Health Chat"),
            ("upload",  "📋", "Upload Reports"),
            ("reports", "📁", "My Reports"),
            ("trends",  "📈", "Health Trends"),
            ("profile", "👤", "Profile"),
            ("settings","⚙️", "Settings"),
        ]

    for key, icon, label in nav_items:
        active = "active" if st.session_state.current_page == key else ""
        if st.button(f"{icon}  {label}", key=f"nav_{key}",
                     use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.current_page = key
            st.rerun()

    st.divider()

    # ── Reports count ─────────────────────────────────────────────────────────
    rpts = _cached_reports(st.session_state.user_id, DB_OK)
    n = len(rpts)
    st.markdown(f"""
    <div style="text-align:center;font-size:12px;color:#4A6080">
        {n} report{"s" if n!=1 else ""} on file
        {"| MongoDB live" if DB_OK else "| Session mode"}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<br><div style="text-align:center;font-size:10px;color:#2A3A50">⚕️ For informational use only.<br>Always consult a physician.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def _save_chat(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})
    if DB_OK:
        save_message(st.session_state.user_id, role, content, st.session_state.session_id)
        if role == "user":
            log_operation(st.session_state.user_id, "Chat", content[:50])

def _get_report_ctx():
    reports = _cached_reports(st.session_state.user_id, DB_OK)
    if not reports: return ""
    return "\n".join([f"{r.get('report_type','')}: {r.get('analysis','')[:300]}" for r in reports[:4]])

def _format_date(dt):
    if not dt: return "—"
    if hasattr(dt, "strftime"): return dt.strftime("%b %d, %Y")
    return str(dt)[:10]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CHAT
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.current_page == "chat":
    st.markdown(f"""
    <div class="page-header">
        <h1>💬 AI Health Chat</h1>
        <p>Hello, <strong>{st.session_state.user_name}</strong> — ask anything about your health, symptoms, or lab results</p>
    </div>
    """, unsafe_allow_html=True)

    # Load from DB on first run
    if DB_OK and not st.session_state.chat_history:
        st.session_state.chat_history = get_chat_history(
            st.session_state.user_id, st.session_state.session_id)

    # ── Messages ───────────────────────────────────────────────────────────────
    chat_box = st.container(height=440)
    with chat_box:
        if not st.session_state.chat_history:
            st.markdown("""
            <div class="welcome-card">
                <div class="glow"></div>
                <div style="font-size:42px;margin-bottom:12px">🧬</div>
                <h2 style="font-family:'Space Grotesk',sans-serif;font-size:22px;font-weight:700;
                           margin-bottom:8px;color:#E8EDF5">Welcome to HealthTrackAI</h2>
                <p style="color:#6A8099;font-size:14px;max-width:400px;margin:0 auto 20px">
                    I'm your intelligent health companion. Upload lab reports for AI analysis,
                    or ask me anything about your health right now.
                </p>
                <div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center">
                    <span class="badge badge-info">📋 Lab Analysis</span>
                    <span class="badge badge-ok">⚠️ Risk Prediction</span>
                    <span class="badge badge-warn">💊 Medicine Guide</span>
                    <span class="badge badge-info">🥗 Diet Plans</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-user">👤&nbsp; {msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    import markdown
                    html_content = markdown.markdown(msg["content"], extensions=['tables'])
                    st.markdown(f'''
                    <div class="chat-ai">
                        <div class="chat-avatar">🧬</div><br>
                        <div class="analysis-content">{html_content}</div>
                    </div>
                    ''', unsafe_allow_html=True)

    # ── Quick prompts ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Quick Questions</div>', unsafe_allow_html=True)
    q_cols = st.columns(4)
    quick = [
        ("🩸 Blood Results", "Explain my blood test results and what I should focus on improving."),
        ("⚠️ My Risk Factors", "What are my main health risks based on my reports?"),
        ("💊 Medicine & Price", "Recommend medicines or supplements with brand names, approximate prices, and pharmacy stores."),
        ("🏥 Find Care", "What specialist should I see and what are the best hospital types for my condition?"),
    ]
    for i, (lbl, prompt) in enumerate(quick):
        if q_cols[i].button(lbl, use_container_width=True, key=f"qp_{i}"):
            with st.spinner("🧬 Thinking..."):
                reply = get_agent().chat(prompt, st.session_state.chat_history, _get_report_ctx())
            _save_chat("user", prompt)
            _save_chat("assistant", reply)
            st.rerun()

    # ── Chat input ─────────────────────────────────────────────────────────────
    if user_msg := st.chat_input("Ask about your health, symptoms, or lab results…"):
        with st.spinner("🧬 Thinking..."):
            reply = get_agent().chat(user_msg, st.session_state.chat_history, _get_report_ctx())
        _save_chat("user", user_msg)
        _save_chat("assistant", reply)
        st.rerun()

    # Clear chat
    if st.session_state.chat_history:
        if st.button("🗑️ Clear conversation", type="secondary"):
            st.session_state.chat_history = []
            if DB_OK: clear_chat_history(st.session_state.user_id, st.session_state.session_id)
            st.cache_data.clear()
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: UPLOAD
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.current_page == "upload":
    st.markdown("""
    <div class="page-header">
        <h1>📋 Upload Lab Reports</h1>
        <p>Blood tests · Vitamins · Thyroid · Lipids · MRI · Urine · Diabetes · Liver · Hormones</p>
    </div>
    """, unsafe_allow_html=True)

    # OCR info banner
    st.markdown("""
    <div style="background:rgba(0,150,255,0.05);border:1px solid rgba(0,150,255,0.15);
                border-radius:12px;padding:12px 16px;margin-bottom:16px;
                display:flex;align-items:center;gap:10px;font-size:13px;color:#8BBBDD">
        <span style="font-size:18px">🔍</span>
        <span>
            <strong style="color:#0096FF">Tesseract OCR</strong> is used for image & scanned PDF reports —
            100% free, no external API needed.
            Install: <code style="background:#0A1628;padding:2px 6px;border-radius:4px">
            pip install pytesseract</code> + Tesseract binary
            (<a href="https://github.com/UB-Mannheim/tesseract/wiki" target="_blank"
               style="color:#0096FF">Windows</a> /
            <code style="background:#0A1628;padding:2px 6px;border-radius:4px">
            brew install tesseract</code> Mac /
            <code style="background:#0A1628;padding:2px 6px;border-radius:4px">
            apt install tesseract-ocr</code> Linux)
        </span>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop your lab reports here or click to browse",
        type=["pdf", "png", "jpg", "jpeg", "bmp", "tiff", "webp", "docx", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    st.markdown('<div class="upload-hint">📄 PDF · 🖼️ PNG / JPG / BMP / TIFF / WEBP · 📝 DOCX · 📃 TXT &nbsp;|&nbsp; Max 50MB per file</div>', unsafe_allow_html=True)

    # ── URL Upload ──
    st.markdown('<div class="section-title" style="margin-top:24px">🌐 Upload via Image Link</div>', unsafe_allow_html=True)
    url_input = st.text_input("Enter URL of report image or PDF", placeholder="https://example.com/my-report.png")
    url_btn = st.button("📥 Download & Analyze", use_container_width=False, type="secondary")

    if "to_process" not in st.session_state:
        st.session_state.to_process = []

    if uploaded:
        already_names = [f[1] for f in st.session_state.to_process]
        for f in uploaded:
            if f.name not in already_names:
                st.session_state.to_process.append((f.read(), f.name))
    
    if url_btn and url_input:
        with st.spinner("📥 Downloading file from URL..."):
            data, fname, err = extract_from_url(url_input)
            if err:
                st.error(err)
            else:
                st.session_state.to_process.append((data, fname))
                st.success(f"Downloaded: {fname}")

    if st.session_state.to_process:
        for i, (file_bytes, filename) in enumerate(st.session_state.to_process):
            ext = filename.split(".")[-1].upper()
            st.markdown(f"""
            <div class="report-card" style="margin-top:16px">
                <div class="rc-name">{get_report_icon("")} {filename}</div>
                <div class="rc-meta">{ext} · {len(file_bytes)/1024:.1f} KB</div>
            </div>
            """, unsafe_allow_html=True)

            col_a, col_b = st.columns([3, 1])
            with col_b:
                go = st.button("🔍 Analyze Now", key=f"go_{filename}_{i}", type="primary", use_container_width=True)

            if go:
                progress_bar = st.progress(0, text="📖 Reading file…")
                # file_bytes is already available
                progress_bar.progress(25, text="🔍 Extracting text via OCR / parser…")
                raw_text = extract_text_from_file(file_bytes, filename)
                report_type = detect_report_type(filename, raw_text)
                icon = get_report_icon(report_type)

                progress_bar.progress(55, text=f"🧬 Analyzing {report_type} with Gemini 3.1 Flash Lite…")
                result = get_agent().analyze_report(raw_text, filename, report_type)
                progress_bar.progress(90, text="💾 Saving to database…")

                if result.get("error"):
                    st.error(f"Analysis error: {result['error']}")
                    progress_bar.empty()
                else:
                    analysis  = result["analysis"]
                    score     = result["health_score"]
                    breakdown = result["breakdown"]

                    if DB_OK:
                        save_report(st.session_state.user_id, filename, report_type, raw_text, analysis, score, breakdown)
                        save_health_score(st.session_state.user_id, score, breakdown)
                        log_operation(st.session_state.user_id, "Report Upload", f"{filename} - {report_type}")
                        st.cache_data.clear()
                    else:
                        st.session_state.uploaded_reports.append({
                            "filename": filename, "report_type": report_type,
                            "analysis": analysis, "health_score": score,
                            "breakdown": breakdown, "uploaded_at": datetime.utcnow()
                        })

                    progress_bar.progress(100, text="✅ Done!")
                    progress_bar.empty()

                    # Results panel
                    score_col, _, summary_col = st.columns([1, 0.1, 3])
                    with score_col:
                        if score >= 75:   sc, sl = "#00C9A7", "Good"
                        elif score >= 55: sc, sl = "#FFAA00", "Fair"
                        else:             sc, sl = "#FF4B6E", "Needs Care"
                        st.markdown(f"""
                        <div class="score-ring-wrap">
                            <div style="font-size:20px">{icon}</div>
                            <div style="font-size:11px;color:#6A8099;margin:6px 0;font-weight:600;
                                        letter-spacing:.06em">{report_type.upper()}</div>
                            <div class="score-big" style="color:{sc}">{score}</div>
                            <div class="score-label-text">out of 100 · {sl}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if breakdown:
                            st.markdown('<br>', unsafe_allow_html=True)
                            st.progress(breakdown.get("vitals",70)/100, text=f"💓 Vitals {breakdown.get('vitals',70)}%")
                            st.progress(breakdown.get("nutrition",65)/100, text=f"🥗 Nutrition {breakdown.get('nutrition',65)}%")
                            st.progress(breakdown.get("risk",40)/100, text=f"⚠️ Risk {breakdown.get('risk',40)}%")

                    with summary_col:
                        import markdown
                        html_content = markdown.markdown(analysis, extensions=['tables'])
                        st.markdown(f'<div class="analysis-content">{html_content}</div>', unsafe_allow_html=True)
                        st.markdown("""
                        <div class="disclaimer">
                            ⚕️ This analysis is for informational purposes only.
                            Always consult a licensed physician before making any medical decision.
                        </div>
                        """, unsafe_allow_html=True)

                    # Smart questions
                    st.markdown('<div class="section-title" style="margin-top:20px">💡 Ask Follow-up</div>', unsafe_allow_html=True)
                    questions = get_agent().suggest_questions(report_type)
                    qc = st.columns(2)
                    for qi, q in enumerate(questions):
                        if qc[qi%2].button(q, key=f"fq_{filename}_{qi}", use_container_width=True):
                            with st.spinner("🧬 Thinking..."):
                                reply = get_agent().chat(q, [], analysis[:600])
                            _save_chat("user", q)
                            _save_chat("assistant", reply)
                            st.session_state.current_page = "chat"
                            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MY REPORTS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.current_page == "reports":
    # Refetch for deletion
    reports = get_reports(st.session_state.user_id) if DB_OK else st.session_state.uploaded_reports
    
    st.markdown("""
    <div class="page-header">
        <h1>📁 My Reports</h1>
        <p>All uploaded lab reports with full AI analysis history</p>
    </div>
    """, unsafe_allow_html=True)

    reports = _cached_reports(st.session_state.user_id, DB_OK)

    if not reports:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#4A6080">
            <div style="font-size:48px;margin-bottom:16px">📋</div>
            <div style="font-size:18px;font-weight:600;color:#8899AA;margin-bottom:8px">No reports yet</div>
            <div style="font-size:14px">Upload your first lab report to get started</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Summary stats
        avg = sum(r.get("health_score",0) for r in reports) / len(reports)
        s_cols = st.columns(4)
        stats = [
            ("📋", str(len(reports)), "Total Reports"),
            ("📊", f"{avg:.0f}/100", "Avg Score"),
            ("🕒", _format_date(reports[0].get("uploaded_at")), "Latest Upload"),
            ("🔬", reports[0].get("report_type","—")[:16], "Latest Type"),
        ]
        for col, (icon, val, lbl) in zip(s_cols, stats):
            col.markdown(f"""
            <div class="stat-card">
                <div class="icon">{icon}</div>
                <div class="value">{val}</div>
                <div class="label">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Report list
        for r in reports:
            sc = r.get("health_score", 0)
            rt = r.get("report_type", "Report")
            fn = r.get("filename", "Unknown")
            icon = get_report_icon(rt)
            if sc >= 75:   sc_c, sc_l = "#00C9A7", "Good"
            elif sc >= 55: sc_c, sc_l = "#FFAA00", "Fair"
            else:          sc_c, sc_l = "#FF4B6E", "Critical"

            with st.expander(f"{icon}  {fn}   ·   {rt}   ·   Score: {sc}/100"):
                ec1, ec2 = st.columns([3, 1])
                with ec1:
                    st.markdown(f'<div style="font-size:11px;color:#4A6080;margin-bottom:12px">📅 {_format_date(r.get("uploaded_at"))}</div>', unsafe_allow_html=True)
                    analysis = r.get("analysis", "")
                    if analysis:
                        import markdown
                        html_content = markdown.markdown(analysis[:3500], extensions=['tables'])
                        st.markdown(f'<div class="analysis-content">{html_content}</div>', unsafe_allow_html=True)
                with ec2:
                    st.markdown(f"""
                    <div style="text-align:center;background:#0A1628;border:1px solid rgba(0,201,167,0.1);
                                border-radius:14px;padding:20px">
                        <div style="font-size:42px;font-weight:800;color:{sc_c};
                                    font-family:'Space Grotesk',sans-serif">{sc}</div>
                        <div style="font-size:11px;color:{sc_c};margin-top:4px;font-weight:600">{sc_l}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("💬 Chat about this", key=f"chat_r_{r.get('_id','')}{fn}", use_container_width=True):
                        q = f"Tell me more about my {rt} — file: {fn}"
                        with st.spinner("Thinking..."):
                            reply = get_agent().chat(q, [], r.get("analysis","")[:600])
                        _save_chat("user", q); _save_chat("assistant", reply)
                        st.session_state.current_page = "chat"
                        st.rerun()
                    if DB_OK:
                        if st.button("🗑️ Delete", key=f"del_r_{r.get('_id','')}",
                                     use_container_width=True, type="secondary"):
                            delete_report(r["_id"])
                            st.cache_data.clear()
                            st.success("Deleted!"); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TRENDS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.current_page == "trends":
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd

    st.markdown("""
    <div class="page-header">
        <h1>📈 Health Trends</h1>
        <p>Track your health score over time and visualize progress across all reports</p>
    </div>
    """, unsafe_allow_html=True)

    scores_data = get_health_scores(st.session_state.user_id, 30) if DB_OK else []
    reports = _cached_reports(st.session_state.user_id, DB_OK)

    if not scores_data and not reports:
        st.markdown("""
        <div style="text-align:center;padding:60px;color:#4A6080">
            <div style="font-size:48px;margin-bottom:16px">📈</div>
            <div style="font-size:18px;font-weight:600;color:#8899AA">No trend data yet</div>
            <div style="font-size:14px;margin-top:8px">Upload reports to start tracking your health journey</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        tab1, tab2, tab3 = st.tabs(["📊 Score Timeline", "🔬 Report Breakdown", "🧬 AI Summary"])

        with tab1:
            if scores_data:
                df = pd.DataFrame(scores_data)
                fig = go.Figure()
                # Fill area
                fig.add_trace(go.Scatter(
                    x=list(range(len(df))), y=df["score"],
                    fill="tozeroy", fillcolor="rgba(0,201,167,0.06)",
                    line=dict(color="rgba(0,201,167,0)", width=0),
                    showlegend=False, hoverinfo="skip",
                ))
                # Main line
                fig.add_trace(go.Scatter(
                    x=list(range(len(df))), y=df["score"],
                    mode="lines+markers",
                    line=dict(color="#00C9A7", width=3),
                    marker=dict(size=10, color="#00C9A7",
                                line=dict(color="#080D18", width=2)),
                    name="Health Score",
                    hovertemplate="Score: <b>%{y}</b><extra></extra>",
                ))
                # Reference zones
                fig.add_hrect(y0=75, y1=100, fillcolor="rgba(0,201,167,0.04)",
                              line_width=0, annotation_text="Good Zone",
                              annotation_position="top right",
                              annotation_font_color="#00C9A7",
                              annotation_font_size=11)
                fig.add_hrect(y0=55, y1=75, fillcolor="rgba(255,170,0,0.03)",
                              line_width=0)
                fig.add_hrect(y0=0, y1=55, fillcolor="rgba(255,75,110,0.03)",
                              line_width=0)
                fig.update_layout(
                    plot_bgcolor="#0A1628", paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#8899AA", family="Plus Jakarta Sans"),
                    xaxis=dict(showgrid=False, zeroline=False, title="Check-in",
                               color="#4A6080"),
                    yaxis=dict(showgrid=True, gridcolor="rgba(0,201,167,0.06)",
                               zeroline=False, range=[0, 105],
                               title="Health Score", color="#4A6080"),
                    height=340, margin=dict(l=20, r=20, t=20, b=20),
                    hoverlabel=dict(bgcolor="#0F1A2E", font_color="#E8EDF5"),
                )
                st.plotly_chart(fig, use_container_width=True)

                # Breakdown trend
                if len(scores_data) > 1:
                    bd_data = [s.get("breakdown", {}) for s in scores_data]
                    df_bd = pd.DataFrame(bd_data).fillna(0)
                    if "vitals" in df_bd.columns:
                        fig2 = go.Figure()
                        colors = {"vitals": "#00C9A7", "nutrition": "#0096FF", "risk": "#FF4B6E"}
                        for col, color in colors.items():
                            if col in df_bd.columns:
                                fig2.add_trace(go.Scatter(
                                    x=list(range(len(df_bd))), y=df_bd[col],
                                    name=col.capitalize(), mode="lines+markers",
                                    line=dict(color=color, width=2),
                                    marker=dict(size=6),
                                ))
                        fig2.update_layout(
                            plot_bgcolor="#0A1628", paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#8899AA"),
                            xaxis=dict(showgrid=False, color="#4A6080"),
                            yaxis=dict(showgrid=True, gridcolor="rgba(0,201,167,0.06)",
                                       range=[0, 105], color="#4A6080"),
                            height=260, margin=dict(l=20, r=20, t=10, b=20),
                            legend=dict(bgcolor="rgba(0,0,0,0)"),
                        )
                        st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No score history yet — analyze a report to build your timeline.")

        with tab2:
            if reports:
                # Type distribution
                type_counts = {}
                for r in reports:
                    t = r.get("report_type", "Other")
                    type_counts[t] = type_counts.get(t, 0) + 1

                c1, c2 = st.columns(2)
                with c1:
                    fig3 = px.pie(
                        values=list(type_counts.values()),
                        names=list(type_counts.keys()),
                        color_discrete_sequence=["#00C9A7","#0096FF","#A855F7","#FFAA00","#FF4B6E","#06B6D4"],
                        hole=0.5,
                    )
                    fig3.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#8899AA"),
                        height=280, margin=dict(l=10,r=10,t=30,b=10),
                        legend=dict(bgcolor="rgba(0,0,0,0)"),
                        title=dict(text="Report Types", font=dict(color="#8899AA", size=13)),
                    )
                    fig3.update_traces(textfont_color="#E8EDF5")
                    st.plotly_chart(fig3, use_container_width=True)

                with c2:
                    # Score distribution
                    score_vals = [r.get("health_score", 0) for r in reports if r.get("health_score")]
                    if score_vals:
                        fig4 = go.Figure(go.Histogram(
                            x=score_vals, nbinsx=8,
                            marker_color="#00C9A7", opacity=0.8,
                        ))
                        fig4.update_layout(
                            title="Score Distribution",
                            plot_bgcolor="#0A1628", paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#8899AA"),
                            xaxis=dict(showgrid=False, range=[0,100], color="#4A6080"),
                            yaxis=dict(showgrid=True, gridcolor="rgba(0,201,167,0.06)", color="#4A6080"),
                            height=280, margin=dict(l=20,r=10,t=30,b=20),
                        )
                        st.plotly_chart(fig4, use_container_width=True)

        with tab3:
            st.markdown('<div class="section-title">AI-Generated Health Summary</div>', unsafe_allow_html=True)
            if st.button("🔄 Generate Fresh Summary", type="primary"):
                with st.spinner("🧬 Analyzing all your reports..."):
                    summary = get_agent().overall_summary([
                        {"filename": r.get("filename",""), "report_type": r.get("report_type",""),
                         "analysis": r.get("analysis",""), "health_score": r.get("health_score",0)}
                        for r in reports
                    ])
                import markdown
                html_content = markdown.markdown(summary)
                st.markdown(f'<div class="analysis-content">{html_content}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PROFILE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.current_page == "profile":
    st.markdown("""
    <div class="page-header">
        <h1>👤 My Profile</h1>
        <p>Personalize your health profile for better AI recommendations</p>
    </div>
    """, unsafe_allow_html=True)

    existing = _cached_user(st.session_state.user_id, DB_OK)
    c1, c2 = st.columns(2)
    with c1:
        name   = st.text_input("Full Name", value=st.session_state.user_name)
        uid    = st.text_input("User ID", value=st.session_state.user_id)
        email  = st.text_input("Email", value=(existing or {}).get("email",""))
    with c2:
        age    = st.number_input("Age", 0, 120, value=(existing or {}).get("age", 0) or 0)
        gender = st.selectbox("Gender", ["", "Male", "Female", "Other", "Prefer not to say"],
                              index=["","Male","Female","Other","Prefer not to say"].index(
                                  (existing or {}).get("gender","") or ""))

    if st.button("💾 Save Profile", type="primary"):
        st.session_state.user_name = name
        st.session_state.user_id   = uid
        st.session_state.user_age  = age
        st.session_state.user_gender = gender
        if DB_OK:
            upsert_user(uid, name, email, age, gender)
            st.cache_data.clear()
        st.success("✅ Profile saved successfully!")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.current_page == "settings":
    st.markdown("""
    <div class="page-header">
        <h1>⚙️ Settings</h1>
        <p>Configure API keys, database connection, and app preferences</p>
    </div>
    """, unsafe_allow_html=True)

    tab_api, tab_db, tab_ocr, tab_data, tab_auth = st.tabs(["🔑 API Keys", "🗄️ Database", "🔍 OCR / Tesseract", "🗑️ Data", "👤 Account"])

    with tab_api:
        st.markdown('<div class="section-title">Google Gemini API</div>', unsafe_allow_html=True)
        cur = os.getenv("GOOGLE_API_KEY","")
        masked = ("*"*(len(cur)-4) + cur[-4:]) if len(cur) > 4 else "Not configured"
        st.code(f"Current: {masked}")
        st.markdown("Get a free key at [aistudio.google.com](https://aistudio.google.com/app/apikey)", unsafe_allow_html=True)
        new_key = st.text_input("New API Key", type="password", placeholder="AIzaSy…")
        if st.button("💾 Save Key", type="primary") and new_key:
            env_path = os.path.join(os.path.dirname(__file__), ".env")
            try:
                lines = open(env_path).readlines() if os.path.exists(env_path) else []
                updated = False
                for i,l in enumerate(lines):
                    if l.startswith("GOOGLE_API_KEY"):
                        lines[i] = f"GOOGLE_API_KEY={new_key}\n"; updated = True
                if not updated: lines.append(f"GOOGLE_API_KEY={new_key}\n")
                open(env_path,"w").writelines(lines)
                st.success("✅ Saved! Restart the app to apply.")
            except Exception as e:
                st.error(f"Could not write .env: {e}")

    with tab_db:
        st.markdown('<div class="section-title">MongoDB Connection</div>', unsafe_allow_html=True)
        uri = os.getenv("MONGODB_URI","mongodb://localhost:27017")
        db_name = os.getenv("MONGODB_DB","healthtrackAI")
        
        # Mask the URI for security
        masked_uri = "Not configured"
        if uri:
            if "@" in uri:
                # Handle mongodb+srv://user:pass@cluster...
                try:
                    protocol_rest = uri.split("://")
                    protocol = protocol_rest[0]
                    content = protocol_rest[1]
                    parts = content.split("@")
                    masked_uri = f"{protocol}://****:****@{parts[1]}"
                except Exception:
                    masked_uri = "**** (Protected)"
            elif uri.startswith("mongodb://localhost"):
                masked_uri = uri # Safe to show localhost
            else:
                masked_uri = "**** (Protected)"
                
        st.code(f"URI:      {masked_uri}\nDatabase: {db_name}")
        if DB_OK:
            st.success("✅ Connected to MongoDB successfully")
            st.json({"collections": ["users","reports","chat_history","health_scores"], "status": "live"})
        else:
            st.error("❌ MongoDB not reachable")
            st.code("# Start MongoDB:\nmongod --dbpath /data/db\n\n# Or open MongoDB Compass and connect to localhost:27017")

    with tab_ocr:
        st.markdown('<div class="section-title">Tesseract OCR</div>', unsafe_allow_html=True)
        try:
            import pytesseract
            ver = pytesseract.get_tesseract_version()
            st.success(f"✅ Tesseract detected — version {ver}")
        except Exception as e:
            st.warning(f"⚠️ Tesseract not found: {e}")
        st.markdown("""
        **Installation:**
        | OS | Command |
        |----|---------|
        | Ubuntu/Debian | `sudo apt install tesseract-ocr` |
        | macOS | `brew install tesseract` |
        | Windows | [Download installer](https://github.com/UB-Mannheim/tesseract/wiki) |

        After installing on Windows, set in `.env`:
        ```
        TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe
        ```
        """)

    with tab_data:
        st.markdown('<div class="section-title">Manage Your Data</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        if c1.button("🗑️ Clear Chat", type="secondary", use_container_width=True):
            st.session_state.chat_history = []
            if DB_OK: clear_chat_history(st.session_state.user_id)
            st.success("Chat cleared!")
        if c2.button("🗑️ Clear Session", type="secondary", use_container_width=True):
            st.session_state.uploaded_reports = []
            st.success("Session data cleared!")
        if c3.button("🔄 Full Reset", type="secondary", use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.cache_data.clear()
            st.rerun()

    with tab_auth:
        st.markdown('<div class="section-title">Account Management</div>', unsafe_allow_html=True)
        st.write(f"**Logged in as:** {st.session_state.username}")
        st.write(f"**User ID:** `{st.session_state.user_id}`")
        if st.button("🚪 Sign Out", use_container_width=True, type="primary"):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.cache_data.clear()
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ADMIN
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.current_page == "admin":
    if st.session_state.get("role") != "admin":
        st.error("⛔ Access Denied: You do not have administrator privileges.")
        st.stop()
        
    st.markdown("""
    <div class="page-header">
        <h1>🔒 Admin Panel</h1>
        <p>System Overview · User Management · Audit Logs</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not DB_OK:
        st.error("MongoDB is offline. Admin panel requires database connection.")
    else:
        users = get_all_users()
        logs = get_logs(200)
        stats = get_system_stats()
        
        tab_over, tab_users, tab_logs = st.tabs(["📊 Overview", "👥 Users", "📜 Audit Logs"])
        
        with tab_over:
            st.markdown("### System Statistics")
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"""
            <div class="stat-card">
                <div class="icon">👥</div>
                <div class="value">{stats.get('users',0)}</div>
                <div class="label">Total Users</div>
            </div>""", unsafe_allow_html=True)
            c2.markdown(f"""
            <div class="stat-card">
                <div class="icon">📋</div>
                <div class="value">{stats.get('reports',0)}</div>
                <div class="label">Reports Processed</div>
            </div>""", unsafe_allow_html=True)
            c3.markdown(f"""
            <div class="stat-card">
                <div class="icon">💬</div>
                <div class="value">{stats.get('chats',0)}</div>
                <div class="label">Chat Messages</div>
            </div>""", unsafe_allow_html=True)
            c4.markdown(f"""
            <div class="stat-card">
                <div class="icon">📝</div>
                <div class="value">{stats.get('logs',0)}</div>
                <div class="label">System Events</div>
            </div>""", unsafe_allow_html=True)
            
            st.markdown("### Recent Activity Volume")
            # Simple chart for logs over time
            import pandas as pd
            if logs:
                df_logs = pd.DataFrame(logs)
                df_logs["timestamp"] = pd.to_datetime(df_logs["timestamp"])
                df_daily = df_logs.groupby(df_logs["timestamp"].dt.date).size().reset_index(name="counts")
                st.bar_chart(df_daily, x="timestamp", y="counts", color="#00C9A7")

        with tab_users:
            st.markdown(f"### User Management")
            
            if users:
                # Display table
                df_users = pd.DataFrame(users)
                display_cols = ["user_id", "username", "name", "email", "role", "created_at", "last_active"]
                cols = [c for c in display_cols if c in df_users.columns]
                st.dataframe(
                    df_users[cols],
                    use_container_width=True,
                    column_config={
                        "created_at": st.column_config.DatetimeColumn("Created", format="D MMM YYYY"),
                        "last_active": st.column_config.DatetimeColumn("Active", format="D MMM YYYY"),
                    }
                )
                
                st.divider()
                st.markdown("#### User Actions")
                c_act1, c_act2 = st.columns([1,2])
                
                with c_act1:
                    target_uid = st.selectbox("Select User", [u["user_id"] for u in users], format_func=lambda x: next((u["username"] for u in users if u["user_id"]==x), x))
                
                with c_act2:
                    action_col1, action_col2 = st.columns(2)
                    if action_col1.button("👑 Promote to Admin"):
                        update_user_role(target_uid, "admin")
                        st.success(f"User {target_uid} promoted!")
                        st.cache_data.clear(); st.rerun()
                        
                    if action_col2.button("🗑️ Delete User", type="primary"):
                        delete_user_full(target_uid)
                        st.warning(f"User {target_uid} deleted.")
                        st.cache_data.clear(); st.rerun()

            else:
                st.info("No users found.")

        with tab_logs:
            st.markdown(f"### Recent Operations")
            if logs:
                df_logs = pd.DataFrame(logs)
                cols_log = ["timestamp", "user_id", "action", "details"]
                cols_log = [c for c in cols_log if c in df_logs.columns]
                df_logs = df_logs[cols_log]
                
                st.dataframe(
                    df_logs,
                    use_container_width=True,
                    column_config={
                        "timestamp": st.column_config.DatetimeColumn("Timestamp", format="D MMM YYYY, HH:mm:ss"),
                    }
                )
            else:
                st.info("No logs found.")
