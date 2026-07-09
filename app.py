import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="SmartEDA", page_icon="📊", layout="wide")

# ══════════════════════════════════════════
# CSS + ANIMATIONS
# ══════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body { background: transparent !important; }

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 900px 700px at 5% 10%, rgba(6,182,212,0.18) 0%, transparent 55%),
        radial-gradient(ellipse 700px 600px at 95% 90%, rgba(16,185,129,0.15) 0%, transparent 55%),
        radial-gradient(ellipse 500px 500px at 50% 50%, rgba(99,102,241,0.07) 0%, transparent 55%),
        #f0fdf9 !important;
    animation: bgBreath 12s ease-in-out infinite alternate;
}
@keyframes bgBreath {
    0%   { filter: hue-rotate(0deg) brightness(1); }
    100% { filter: hue-rotate(6deg) brightness(1.02); }
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: -200px; left: -200px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(6,182,212,0.16) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none; z-index: 0;
    animation: blob1 14s ease-in-out infinite;
}
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    bottom: -150px; right: -150px;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(16,185,129,0.14) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none; z-index: 0;
    animation: blob2 18s ease-in-out infinite;
}
@keyframes blob1 {
    0%,100% { transform: translate(0,0) scale(1); }
    33%      { transform: translate(80px,60px) scale(1.08); }
    66%      { transform: translate(-40px,80px) scale(0.94); }
}
@keyframes blob2 {
    0%,100% { transform: translate(0,0) scale(1); }
    33%      { transform: translate(-60px,-40px) scale(1.06); }
    66%      { transform: translate(40px,-60px) scale(0.96); }
}

[data-testid="stMain"] {
    background:
        linear-gradient(rgba(6,182,212,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(6,182,212,0.035) 1px, transparent 1px) !important;
    background-size: 52px 52px !important;
    animation: gridMove 28s linear infinite;
}
@keyframes gridMove {
    0%   { background-position: 0 0, 0 0; }
    100% { background-position: 52px 52px, 52px 52px; }
}

.stApp { font-family: 'Plus Jakarta Sans', sans-serif; }

/* Floating particles */
.particle-layer {
    position: fixed; inset: 0;
    pointer-events: none; z-index: 0; overflow: hidden;
}
.particle {
    position: absolute; bottom: -20px;
    border-radius: 50%;
    animation: floatUp linear infinite;
    opacity: 0;
}
@keyframes floatUp {
    0%   { transform: translateY(0) scale(0.5); opacity: 0; }
    10%  { opacity: 0.8; }
    90%  { opacity: 0.4; }
    100% { transform: translateY(-105vh) scale(1.3); opacity: 0; }
}

/* ── Login card ── */
.login-card {
    max-width: 430px; margin: 2.5rem auto 0;
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(6,182,212,0.22); border-radius: 28px;
    padding: 2.5rem 2.5rem 2rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 20px 60px rgba(6,182,212,0.14), 0 4px 20px rgba(0,0,0,0.05);
    animation: cardIn 0.7s cubic-bezier(0.34,1.56,0.64,1) forwards;
    position: relative; z-index: 2;
}
@keyframes cardIn {
    from { opacity:0; transform:translateY(40px) scale(0.94); }
    to   { opacity:1; transform:translateY(0) scale(1); }
}
.logo-icon {
    width:68px; height:68px; border-radius:22px;
    background:linear-gradient(135deg,#06b6d4,#10b981);
    display:flex; align-items:center; justify-content:center;
    font-size:30px; margin:0 auto 1rem;
    box-shadow:0 8px 28px rgba(6,182,212,0.4);
    animation:iconBounce 0.6s 0.25s cubic-bezier(0.34,1.56,0.64,1) both;
}
@keyframes iconBounce {
    from { opacity:0; transform:scale(0.3) rotate(-20deg); }
    to   { opacity:1; transform:scale(1) rotate(0deg); }
}
.logo-title {
    font-family:'Playfair Display',serif; font-size:36px;
    background:linear-gradient(135deg,#0891b2,#059669);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; text-align:center; margin-bottom:4px;
}
.logo-sub { font-size:13px; color:#64748b; text-align:center; margin-bottom:1.25rem; }
.badge-row { display:flex; justify-content:center; gap:8px; flex-wrap:wrap; margin-bottom:1.5rem; }
.badge { font-size:11px; padding:4px 12px; border-radius:99px; font-weight:600; }
.bc  { background:#e0f7fa; color:#0891b2; border:1px solid #b2ebf2; }
.bg2 { background:#e8f5e9; color:#059669; border:1px solid #c8e6c9; }

/* ── All content above bg ── */
section[data-testid="stSidebar"],
section[data-testid="stMain"] > div,
.block-container { position:relative; z-index:1; }

/* ── Inputs ── */
.stTextInput input {
    background:rgba(255,255,255,0.95) !important;
    border:1.5px solid rgba(6,182,212,0.28) !important;
    border-radius:12px !important; color:#1e293b !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    padding:12px 16px !important; transition:all 0.2s !important;
}
.stTextInput input:focus {
    border-color:#06b6d4 !important;
    box-shadow:0 0 0 3px rgba(6,182,212,0.14) !important;
}
.stTextInput label { color:#475569 !important; font-size:12px !important; font-weight:600 !important; }

/* ── Buttons ── */
.stButton > button {
    background:linear-gradient(135deg,#06b6d4,#0891b2) !important;
    color:#fff !important; border:none !important;
    border-radius:14px !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    font-weight:700 !important; font-size:13px !important;
    transition:all 0.25s !important;
    box-shadow:0 4px 18px rgba(6,182,212,0.35) !important;
}
.stButton > button:hover {
    transform:translateY(-3px) !important;
    box-shadow:0 10px 30px rgba(6,182,212,0.52) !important;
    background:linear-gradient(135deg,#0891b2,#059669) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background:rgba(255,255,255,0.82) !important;
    border:1px solid rgba(6,182,212,0.16) !important;
    border-radius:14px !important; padding:4px !important;
}
.stTabs [data-baseweb="tab"] {
    color:#64748b !important; font-weight:600 !important;
    font-family:'Plus Jakarta Sans',sans-serif !important;
    border-radius:10px !important; font-size:12px !important;
}
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#06b6d4,#10b981) !important;
    color:#fff !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background:rgba(236,254,255,0.97) !important;
    border-right:1px solid rgba(6,182,212,0.18) !important;
    backdrop-filter:blur(12px);
}

/* ── Metric containers ── */
div[data-testid="metric-container"] {
    background:rgba(255,255,255,0.9) !important;
    border:1px solid rgba(6,182,212,0.15) !important;
    border-radius:12px !important; padding:14px !important;
    box-shadow:0 2px 10px rgba(0,0,0,0.04) !important;
}
div[data-testid="metric-container"] label {
    color:#64748b !important; font-size:11px !important; font-weight:600 !important;
}

/* ── File uploader ── */
.stFileUploader {
    background:rgba(255,255,255,0.8) !important;
    border:1.5px dashed rgba(6,182,212,0.38) !important;
    border-radius:14px !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius:12px !important; overflow:hidden !important;
    box-shadow:0 2px 14px rgba(0,0,0,0.06) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background:rgba(255,255,255,0.92) !important;
    border:1.5px solid rgba(6,182,212,0.22) !important;
    border-radius:10px !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background:rgba(255,255,255,0.8) !important;
    border-radius:12px !important;
    border:1px solid rgba(6,182,212,0.15) !important;
}

::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-thumb { background:rgba(6,182,212,0.35); border-radius:99px; }
#MainMenu, footer, header { visibility:hidden; }
hr { border-color:rgba(6,182,212,0.14) !important; }
</style>

<!-- Floating particles -->
<div class="particle-layer">
  <div class="particle" style="left:8%;width:8px;height:8px;background:rgba(6,182,212,0.4);animation-duration:13s;animation-delay:0s;"></div>
  <div class="particle" style="left:20%;width:5px;height:5px;background:rgba(16,185,129,0.35);animation-duration:17s;animation-delay:2s;"></div>
  <div class="particle" style="left:33%;width:10px;height:10px;background:rgba(6,182,212,0.28);animation-duration:15s;animation-delay:4s;"></div>
  <div class="particle" style="left:48%;width:6px;height:6px;background:rgba(16,185,129,0.38);animation-duration:19s;animation-delay:1s;"></div>
  <div class="particle" style="left:62%;width:9px;height:9px;background:rgba(99,102,241,0.28);animation-duration:14s;animation-delay:3s;"></div>
  <div class="particle" style="left:75%;width:5px;height:5px;background:rgba(6,182,212,0.35);animation-duration:16s;animation-delay:5s;"></div>
  <div class="particle" style="left:88%;width:7px;height:7px;background:rgba(16,185,129,0.32);animation-duration:18s;animation-delay:7s;"></div>
  <div class="particle" style="left:15%;width:6px;height:6px;background:rgba(6,182,212,0.25);animation-duration:12s;animation-delay:6s;"></div>
  <div class="particle" style="left:55%;width:8px;height:8px;background:rgba(16,185,129,0.3);animation-duration:20s;animation-delay:9s;"></div>
  <div class="particle" style="left:40%;width:5px;height:5px;background:rgba(99,102,241,0.22);animation-duration:11s;animation-delay:8s;"></div>
  <div class="particle" style="left:92%;width:7px;height:7px;background:rgba(6,182,212,0.3);animation-duration:16s;animation-delay:4s;"></div>
  <div class="particle" style="left:3%;width:9px;height:9px;background:rgba(16,185,129,0.25);animation-duration:14s;animation-delay:10s;"></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
for key, val in [
    ("df_original", None),
    ("df", None),
    ("cleaning_log", []),
    ("history", []),
    ("ml_results", None),
    ("analysis_started", False)
]:
    if key not in st.session_state:
        st.session_state[key] = val     

# ══════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════
if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-card">
        <div class="logo-icon">📊</div>
        <p class="logo-title">SmartEDA</p>
        <p class="logo-sub">AI-powered Data Intelligence Platform</p>
        <div class="badge-row">
            <span class="badge bc">✦ Free Forever</span>
            <span class="badge bg2">✦ No Setup</span>
            <span class="badge bc">✦ Instant Analysis</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Create Account"])

        with tab1:
            email = st.text_input("Email address", key="li_email", placeholder="you@email.com")
            password = st.text_input("Password", type="password", key="li_pass", placeholder="••••••••")
            if st.button("Login →", use_container_width=True, key="li_btn"):
                if email and len(password) >= 4:
                    st.session_state.user = {"email": email}
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Enter a valid email and password (min 4 characters)")

        with tab2:
            email2 = st.text_input("Email address", key="su_email", placeholder="you@email.com")
            password2 = st.text_input("Password (min 6 chars)", type="password", key="su_pass", placeholder="••••••••")
            if st.button("Create Account →", use_container_width=True, key="su_btn"):
                if email2 and len(password2) >= 6:
                    st.session_state.user = {"email": email2}
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Enter a valid email and at least 6 character password")

        st.markdown("""
        <p style="text-align:center;font-size:11px;color:#94a3b8;margin-top:1rem;">
        Demo mode — enter any email and password to continue
        </p>""", unsafe_allow_html=True)

# ══════════════════════════════════════════
# MAIN APP (after login)
# ══════════════════════════════════════════
else:
    from eda_engine import (
        get_overview, get_column_stats, detect_outliers,
        get_auto_insights, get_top_correlations,
        plot_distribution, plot_scatter, plot_correlation,
        plot_missing, plot_categorical,
        suggest_problem_type, data_quality_score,
        clean_remove_nulls, clean_fill_mean, clean_fill_median,
        clean_fill_mode, clean_remove_duplicates, clean_remove_outliers,
        mini_query
    )
    from ml_engine import (
        detect_problem_type, get_problem_label,
        run_auto_ml, plot_feature_importance, plot_confusion_matrix,
        run_kmeans, get_recommendations, generate_resume_bullet
    )
    from report_gen import generate_pdf

    email = st.session_state.user["email"]

    # ── Helper functions
    def mcard(label, value, color="#0f172a"):
        return f'''<div style="background:rgba(255,255,255,0.92);border:1px solid rgba(6,182,212,0.18);
            border-radius:16px;padding:1rem 1.25rem;text-align:center;
            box-shadow:0 2px 12px rgba(6,182,212,0.07);
            transition:transform 0.25s,box-shadow 0.25s;">
            <div style="font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;font-weight:700;margin-bottom:6px;">{label}</div>
            <div style="font-size:26px;font-weight:800;color:{color};">{value}</div>
            </div>'''

    def stitle(t):
        return f'<p style="font-family:Playfair Display,serif;font-size:20px;color:#0f172a;margin:1.25rem 0 0.75rem;padding-bottom:8px;border-bottom:2px solid rgba(6,182,212,0.15);">{t}</p>'

    def iw(t): return f'<div style="background:#fff7ed;border-left:3px solid #f97316;border-radius:0 10px 10px 0;padding:10px 14px;margin:6px 0;font-size:13px;color:#9a3412;display:flex;gap:10px;align-items:flex-start;">⚠️<span>{t}</span></div>'
    def ii(t): return f'<div style="background:#f0f9ff;border-left:3px solid #06b6d4;border-radius:0 10px 10px 0;padding:10px 14px;margin:6px 0;font-size:13px;color:#0c4a6e;display:flex;gap:10px;align-items:flex-start;">ℹ️<span>{t}</span></div>'
    def io(t): return f'<div style="background:#f0fdf4;border-left:3px solid #10b981;border-radius:0 10px 10px 0;padding:10px 14px;margin:6px 0;font-size:13px;color:#064e3b;display:flex;gap:10px;align-items:flex-start;">✅<span>{t}</span></div>'

    # ── Voice assistant
    voice_html = """<!DOCTYPE html><html><head>
    <style>
    body{margin:0;padding:0;background:transparent;font-family:sans-serif;overflow:hidden;}
    #btn{
        position:fixed;bottom:24px;right:24px;width:56px;height:56px;border-radius:50%;
        background:linear-gradient(135deg,#06b6d4,#10b981);border:none;cursor:pointer;
        font-size:22px;box-shadow:0 6px 22px rgba(6,182,212,0.55);
        transition:all 0.2s;z-index:9999;
        animation:vPulse 2.5s ease-in-out infinite;
    }
    #btn:hover{transform:scale(1.12);}
    #btn.on{background:linear-gradient(135deg,#ef4444,#f97316);animation:rPulse 1s ease-in-out infinite;}
    @keyframes vPulse{0%,100%{box-shadow:0 6px 22px rgba(6,182,212,0.55);}50%{box-shadow:0 6px 32px rgba(6,182,212,0.9),0 0 0 12px rgba(6,182,212,0.08);}}
    @keyframes rPulse{0%,100%{box-shadow:0 0 0 0 rgba(239,68,68,0.6);}50%{box-shadow:0 0 0 16px rgba(239,68,68,0);}}
    #helpbtn{
        position:fixed;bottom:24px;right:92px;width:36px;height:36px;border-radius:50%;
        background:rgba(255,255,255,0.95);border:1px solid rgba(6,182,212,0.3);
        cursor:pointer;font-size:15px;z-index:9999;
        box-shadow:0 2px 10px rgba(6,182,212,0.18);
    }
    #popup{
        position:fixed;bottom:92px;right:24px;width:300px;
        background:rgba(255,255,255,0.98);border:1px solid rgba(6,182,212,0.25);
        border-radius:16px;padding:14px 16px;font-size:12px;color:#0f172a;
        box-shadow:0 8px 28px rgba(6,182,212,0.18);display:none;z-index:9998;
        animation:slideUp 0.3s ease;
    }
    @keyframes slideUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
    #help{
        position:fixed;bottom:70px;right:92px;background:rgba(255,255,255,0.98);
        border:1px solid rgba(6,182,212,0.2);border-radius:12px;padding:12px 16px;
        font-size:11px;color:#475569;line-height:2;display:none;max-width:220px;
        box-shadow:0 4px 16px rgba(6,182,212,0.14);z-index:9998;
    }
    .tag{font-size:10px;font-weight:700;color:#06b6d4;text-transform:uppercase;letter-spacing:.1em;margin-bottom:3px;}
    .cmd{font-weight:700;color:#0f172a;margin-bottom:4px;}
    .resp{color:#64748b;line-height:1.55;}
    </style></head><body>
    <div id="popup"><div class="tag">Voice Command</div><div class="cmd" id="cmd"></div><div class="resp" id="resp"></div></div>
    <div id="help">
        <strong style="color:#0891b2;">Say these commands:</strong><br>
        "show overview"<br>"show insights"<br>"show charts"<br>
        "show ML model"<br>"show clustering"<br>"show recommendations"<br>
        "show cleaning"<br>"show column analyzer"<br>"show export"<br>
        "mean of salary"<br>"scroll down"<br>"scroll up"<br>"help"
    </div>
    <button id="helpbtn" onclick="toggleHelp()" title="Voice commands">❓</button>
    <button id="btn" onclick="toggleVoice()" title="Click to speak a command">🎤</button>
    <script>
    let rec=null,on=false;
    const btn=document.getElementById('btn');
    const popup=document.getElementById('popup');
    function toggleHelp(){const h=document.getElementById('help');h.style.display=h.style.display==='block'?'none':'block';}
    function show(c,r){
        document.getElementById('cmd').textContent=c;
        document.getElementById('resp').textContent=r;
        popup.style.display='block';
        clearTimeout(window._t);
        window._t=setTimeout(()=>{popup.style.display='none';},5500);
    }
    function toggleVoice(){
        if(!('webkitSpeechRecognition'in window||'SpeechRecognition'in window)){
            show('Not supported','Please use Google Chrome for voice commands.');return;
        }
        on?stop():go();
    }
    function go(){
        const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
        rec=new SR();rec.lang='en-US';rec.continuous=false;rec.interimResults=false;
        rec.onstart=()=>{on=true;btn.classList.add('on');btn.textContent='⏹';show('Listening...','Speak your command now...');};
        rec.onresult=e=>run(e.results[0][0].transcript.toLowerCase().trim());
        rec.onerror=()=>{stop();show('Error','Could not hear. Try again.');};
        rec.onend=()=>stop();
        rec.start();
    }
    function stop(){on=false;btn.classList.remove('on');btn.textContent='🎤';try{rec&&rec.stop();}catch(e){}}
    function clickTab(i){
        try{
            const tabs=window.parent.document.querySelectorAll('[data-baseweb="tab"]');
            if(tabs[i])tabs[i].click();
        }catch(e){}
    }
    function run(cmd){
        let resp='';
        const map={
            'overview':0,'summary':0,
            'insight':1,'auto insight':1,
            'chart':2,'graph':2,'visual':2,
            'ml':3,'model':3,'machine learning':3,'predict':3,'pipeline':3,
            'cluster':4,'group':4,'kmeans':4,
            'recommend':5,'suggestion':5,
            'clean':6,'null':6,'duplicate':6,
            'column':7,'analyzer':7,
            'export':8,'download':8,'report':8,'resume':8
        };
        let idx=-1;
        for(const[k,v]of Object.entries(map)){if(cmd.includes(k)){idx=v;break;}}
        const names=['Overview','Insights','Charts','ML Pipeline','Clustering','Recommendations','Cleaning','Column Analyzer','Export'];
        if(idx>=0){resp='Navigating to '+names[idx]+' tab.';clickTab(idx);}
        else if(cmd.includes('scroll down')||cmd.includes('go down')){window.parent.scrollBy({top:500,behavior:'smooth'});resp='Scrolled down.';}
        else if(cmd.includes('scroll up')||cmd.includes('top')){window.parent.scrollTo({top:0,behavior:'smooth'});resp='Scrolled to top.';}
        else if(cmd.includes('help')||cmd.includes('command')){toggleHelp();resp='Commands list shown next to mic button.';}
        else if(cmd.includes('mean')||cmd.includes('max')||cmd.includes('min')||cmd.includes('sum')||cmd.includes('missing')||cmd.includes('median')||cmd.includes('std')||cmd.includes('count')){
            resp='Go to Insights tab → Mini Query box → type: '+cmd;
            clickTab(1);
        }
        else{resp='Heard: "'+cmd+'". Say "help" to see all commands.';}
        show(cmd,resp);
    }
    </script></body></html>"""

    components.html(voice_html, height=0, scrolling=False)

    # ── Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:0.5rem 0 0.75rem;">
            <p style="font-family:'Playfair Display',serif;font-size:22px;
               background:linear-gradient(135deg,#0891b2,#059669);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;font-weight:700;margin-bottom:2px;">SmartEDA</p>
            <p style="font-size:11px;color:#64748b;">Data Intelligence Platform</p>
        </div>
        <div style="background:linear-gradient(135deg,rgba(6,182,212,0.08),rgba(16,185,129,0.06));
             border:1px solid rgba(6,182,212,0.2);border-radius:12px;
             padding:10px 14px;margin-bottom:0.75rem;">
            <p style="font-size:10px;color:#64748b;font-weight:700;text-transform:uppercase;
               letter-spacing:0.06em;margin-bottom:2px;">Logged in as</p>
            <p style="font-size:13px;color:#0891b2;font-weight:600;">{email}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.df is not None:
            ov = get_overview(st.session_state.df)
            sc = data_quality_score(st.session_state.df)
            st.metric("Rows", f"{ov['rows']:,}")
            st.metric("Columns", ov["columns"])
            st.metric("Quality Score", f"{sc}/100")
            st.divider()

        if st.button("Logout", use_container_width=True):
            for k in ["user","df","df_original","cleaning_log","ml_results"]:
                st.session_state[k] = None
            st.session_state.logged_in = False
            st.session_state.cleaning_log = []
            st.session_state.history = []
            st.rerun()

    # ── Page hero
    st.markdown("""
    <div style="background:rgba(255,255,255,0.82);border:1px solid rgba(6,182,212,0.2);
         border-radius:20px;padding:1.5rem 2rem;margin-bottom:1.5rem;
         backdrop-filter:blur(16px);box-shadow:0 4px 24px rgba(6,182,212,0.09);
         animation:heroIn 0.5s ease forwards;">
        <p style="font-family:'Playfair Display',serif;font-size:28px;
           background:linear-gradient(135deg,#0891b2,#059669);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
           background-clip:text;margin-bottom:4px;">Data Intelligence Platform</p>
        <p style="font-size:13px;color:#64748b;margin-bottom:8px;">
            Upload any CSV — get instant insights, ML models, and professional reports</p>
        <span style="display:inline-flex;align-items:center;gap:6px;
              background:rgba(6,182,212,0.08);border:1px solid rgba(6,182,212,0.2);
              border-radius:99px;padding:4px 14px;font-size:11px;color:#0891b2;font-weight:600;
              animation:pulseBadge 2.5s ease-in-out infinite;">
            🎤 Voice ready — click the mic button at bottom right to speak commands
        </span>
    </div>
    <style>
    @keyframes heroIn{from{opacity:0;transform:translateY(-12px)}to{opacity:1;transform:translateY(0)}}
    @keyframes pulseBadge{0%,100%{box-shadow:0 0 0 0 rgba(6,182,212,0.2);}50%{box-shadow:0 0 0 8px rgba(6,182,212,0);}}
    </style>
    """, unsafe_allow_html=True)

    # ── Sample datasets
    with st.expander("🧪 Try a sample dataset — no upload needed"):
        sc_choice = st.selectbox("Choose a dataset", [
            "None", "Titanic (classification)",
            "Iris (multi-class)", "Sales (regression)"
        ])
        if st.button("Load sample") and sc_choice != "None":
            np.random.seed(42)
            if sc_choice == "Titanic (classification)":
                try:
                    df_s = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
                except:
                    n = 300
                    df_s = pd.DataFrame({
                        "Survived": np.random.randint(0,2,n),
                        "Pclass": np.random.choice([1,2,3],n),
                        "Age": np.random.normal(30,12,n).round(1),
                        "Fare": np.random.exponential(30,n).round(2),
                        "SibSp": np.random.randint(0,5,n),
                        "Sex": np.random.choice(["male","female"],n),
                        "Embarked": np.random.choice(["S","C","Q"],n)
                    })
            elif sc_choice == "Iris (multi-class)":
                sp = np.repeat(["setosa","versicolor","virginica"], 50)
                df_s = pd.DataFrame({
                    "sepal_length": np.concatenate([np.random.normal(5.0,.35,50),np.random.normal(5.9,.52,50),np.random.normal(6.6,.64,50)]),
                    "sepal_width":  np.concatenate([np.random.normal(3.4,.38,50),np.random.normal(2.8,.31,50),np.random.normal(3.0,.32,50)]),
                    "petal_length": np.concatenate([np.random.normal(1.5,.17,50),np.random.normal(4.3,.47,50),np.random.normal(5.6,.55,50)]),
                    "petal_width":  np.concatenate([np.random.normal(.25,.11,50),np.random.normal(1.3,.2,50),np.random.normal(2.0,.27,50)]),
                    "species": sp
                })
            else:
                n = 300
                df_s = pd.DataFrame({
                    "Month":   np.random.choice(["Jan","Feb","Mar","Apr","May","Jun"],n),
                    "Region":  np.random.choice(["North","South","East","West"],n),
                    "Product": np.random.choice(["A","B","C"],n),
                    "Sales":   np.random.normal(50000,12000,n).round(2),
                    "Units":   np.random.randint(10,500,n),
                    "Discount":np.random.uniform(0,.3,n).round(3),
                    "Profit":  np.random.normal(12000,4000,n).round(2),
                })
            st.session_state.df_original = df_s
            st.session_state.df = df_s.copy()
            st.session_state.cleaning_log = []
            st.session_state.ml_results = None
            st.session_state.history.append({
                "name": sc_choice,
                "time": datetime.datetime.now().strftime("%H:%M"),
                "rows": len(df_s), "cols": len(df_s.columns)
            })
            st.rerun()

    # ── File upload
    # ── File upload with Start Analysis button
uploaded = st.file_uploader(
    "Or upload your own CSV file",
    type=["csv"],
    key="csv_uploader"
)

if uploaded is not None:

    file_size = uploaded.size / 1024

    st.success(f"✅ File selected: {uploaded.name}")
    st.caption(f"File size: {file_size:.2f} KB")

    if st.button(
        "🚀 Start Analysis",
        use_container_width=True,
        key="start_analysis_btn"
    ):

        try:
            with st.spinner("Analyzing your dataset..."):

                df_new = pd.read_csv(uploaded)

                if df_new.empty:
                    st.error("The uploaded CSV file is empty.")
                    st.stop()

                st.session_state.df_original = df_new.copy()
                st.session_state.df = df_new.copy()

                st.session_state.cleaning_log = []
                st.session_state.ml_results = None

                st.session_state.history.append({
                    "name": uploaded.name,
                    "time": datetime.datetime.now().strftime("%H:%M"),
                    "rows": len(df_new),
                    "cols": len(df_new.columns)
                })

            st.rerun()

        except pd.errors.EmptyDataError:
            st.error("The CSV file contains no data.")

        except pd.errors.ParserError:
            st.error("Unable to read the CSV file.")

        except UnicodeDecodeError:
            st.error("Unable to read the file encoding.")

        except Exception as e:
            st.error(f"Error while reading CSV: {e}")

    # ── No data state
    if st.session_state.df is None:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.82);border:1px solid rgba(6,182,212,0.15);
             border-radius:18px;padding:3.5rem;text-align:center;margin-top:1rem;
             backdrop-filter:blur(12px);">
            <p style="font-size:52px;margin-bottom:1rem;">📊</p>
            <p style="font-size:17px;color:#475569;font-weight:700;">
                Upload a CSV or load a sample dataset to begin</p>
            <p style="font-size:12px;color:#94a3b8;margin-top:8px;">
                Supports any CSV — sales, health, student records, surveys, finance</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    df = st.session_state.df
    overview = get_overview(df)
    score = data_quality_score(df)
    score_color = "#059669" if score>=80 else "#d97706" if score>=50 else "#dc2626"

    # ── Top metric bar
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(mcard("Rows", f"{overview['rows']:,}"), unsafe_allow_html=True)
    with c2: st.markdown(mcard("Columns", overview["columns"]), unsafe_allow_html=True)
    with c3: st.markdown(mcard("Missing", f"{overview['missing_pct']}%"), unsafe_allow_html=True)
    with c4: st.markdown(mcard("Duplicates", overview["duplicate_rows"]), unsafe_allow_html=True)
    with c5: st.markdown(mcard("Quality", f"{score}/100", score_color), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # TABS
    # ══════════════════════════════════════════
    t1,t2,t3,t4,t5,t6,t7,t8,t9 = st.tabs([
        "📋 Overview", "🧠 Insights", "📊 Charts",
        "🤖 ML Pipeline", "🧬 Clustering", "💡 Recommendations",
        "🧹 Cleaning", "🔍 Column Analyzer", "📄 Export"
    ])

    # ─── TAB 1 — OVERVIEW ───────────────────────
    with t1:
        st.markdown(stitle("Column Summary"), unsafe_allow_html=True)
        st.dataframe(get_column_stats(df), use_container_width=True, height=340)
        with st.expander("Preview raw data (first 50 rows)"):
            st.dataframe(df.head(50), use_container_width=True)

    # ─── TAB 2 — INSIGHTS ───────────────────────
    with t2:
        st.markdown(stitle("Auto Insights"), unsafe_allow_html=True)
        insights = get_auto_insights(df)
        w = sum(1 for t,_ in insights if t=="warning")
        i = sum(1 for t,_ in insights if t=="info")
        o = sum(1 for t,_ in insights if t=="success")
        c1,c2,c3 = st.columns(3)
        c1.metric("Issues found", w)
        c2.metric("Observations", i)
        c3.metric("Positive signals", o)
        st.divider()
        for itype, text in insights:
            if itype=="warning":   st.markdown(iw(text), unsafe_allow_html=True)
            elif itype=="info":    st.markdown(ii(text), unsafe_allow_html=True)
            else:                  st.markdown(io(text), unsafe_allow_html=True)

        st.divider()
        st.markdown(stitle("Mini Query System"), unsafe_allow_html=True)
        st.caption('Ask without any AI API. Try: "mean of salary" / "max of age" / "missing of price"')
        q = st.text_input("", placeholder="mean of salary", key="mini_q")
        if q:
            results = mini_query(df, q)
            for r in results:
                st.success(r)

    # ─── TAB 3 — CHARTS ─────────────────────────
    with t3:
        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()
        ct = st.radio("Select chart type",
                      ["Distribution","Scatter","Correlation","Missing","Categorical","Dashboard"],
                      horizontal=True, key="chart_radio")
        st.divider()

        if ct == "Distribution":
            if num_cols:
                c1,c2 = st.columns(2)
                cs    = c1.selectbox("Column", num_cols, key="dist_col")
                ctype = c2.selectbox("Chart style", ["Histogram","Box plot","Violin"], key="dist_type")
                st.plotly_chart(plot_distribution(df, cs, ctype), use_container_width=True, key="dist_chart")
                c1,c2,c3,c4 = st.columns(4)
                c1.metric("Mean",   round(df[cs].mean(),2))
                c2.metric("Median", round(df[cs].median(),2))
                c3.metric("Std",    round(df[cs].std(),2))
                c4.metric("Skew",   round(df[cs].skew(),2))
            else:
                st.warning("No numeric columns found.")

        elif ct == "Scatter":
            if len(num_cols) >= 2:
                c1,c2,c3 = st.columns(3)
                xc = c1.selectbox("X axis", num_cols, key="sc_x")
                yc = c2.selectbox("Y axis", num_cols, index=min(1,len(num_cols)-1), key="sc_y")
                cc = c3.selectbox("Color by", ["None"]+cat_cols, key="sc_c")
                st.plotly_chart(plot_scatter(df, xc, yc, None if cc=="None" else cc),
                                use_container_width=True, key="scatter_chart")
            else:
                st.warning("Need at least 2 numeric columns.")

        elif ct == "Correlation":
            f = plot_correlation(df)
            if f: st.plotly_chart(f, use_container_width=True, key="corr_chart")
            else: st.info("Need at least 2 numeric columns.")

        elif ct == "Missing":
            f = plot_missing(df)
            if f: st.plotly_chart(f, use_container_width=True, key="miss_chart")
            else: st.success("No missing values in this dataset!")

        elif ct == "Categorical":
            if cat_cols:
                cs = st.selectbox("Select column", cat_cols, key="cat_col")
                st.plotly_chart(plot_categorical(df, cs), use_container_width=True, key="cat_chart")
            else:
                st.warning("No categorical columns found.")

        elif ct == "Dashboard":
            if len(num_cols) >= 2:
                c1,c2 = st.columns(2)
                with c1: st.plotly_chart(plot_distribution(df, num_cols[0]), use_container_width=True, key="dash1")
                with c2: st.plotly_chart(plot_distribution(df, num_cols[1], "Box plot"), use_container_width=True, key="dash2")
                c1,c2 = st.columns(2)
                with c1:
                    cf = plot_correlation(df)
                    if cf: st.plotly_chart(cf, use_container_width=True, key="dash3")
                with c2:
                    mf = plot_missing(df)
                    if mf: st.plotly_chart(mf, use_container_width=True, key="dash4")
                    else:  st.success("No missing values!")
            else:
                st.info("Need at least 2 numeric columns for dashboard view.")

    # ─── TAB 4 — ML PIPELINE ────────────────────
    with t4:
        st.markdown(stitle("Auto ML Pipeline"), unsafe_allow_html=True)
        st.caption("Select a target column → click Run → get model accuracy + XAI feature importance automatically.")
        all_cols = df.columns.tolist()

        if len(all_cols) < 2:
            st.warning("Need at least 2 columns to run ML.")
        else:
            c1,c2 = st.columns([2,1])
            with c1:
                target_col = st.selectbox("Target column (what to predict)", all_cols, key="ml_target")
            with c2:
                st.markdown("<br>", unsafe_allow_html=True)
                run_btn = st.button("▶ Run Auto Model", use_container_width=True, key="ml_run")

            if target_col:
                prob = detect_problem_type(df, target_col)
                lbl, desc, col = get_problem_label(prob)
                st.markdown(f"""
                <div style="display:inline-flex;align-items:center;gap:10px;
                     background:rgba(6,182,212,0.08);border:1px solid rgba(6,182,212,0.2);
                     border-radius:10px;padding:8px 16px;margin:8px 0;font-size:13px;">
                    <span style="font-weight:700;color:{col};">{lbl}</span>
                    <span style="color:#94a3b8;">—</span>
                    <span style="color:#64748b;">{desc}</span>
                </div>""", unsafe_allow_html=True)

            if run_btn:
                with st.spinner("Training model... please wait"):
                    results, err = run_auto_ml(df, target_col)
                if err:
                    st.error(err)
                else:
                    st.session_state.ml_results = results
                    st.success("Model trained successfully!")

            if st.session_state.ml_results:
                r = st.session_state.ml_results
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,rgba(6,182,212,0.08),rgba(16,185,129,0.06));
                     border:1px solid rgba(6,182,212,0.25);border-radius:20px;
                     padding:2rem;text-align:center;margin:1rem 0;
                     animation:popIn 0.6s cubic-bezier(0.34,1.56,0.64,1) forwards;">
                    <p style="font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.12em;margin-bottom:8px;">{r['metric_label']}</p>
                    <p style="font-family:'Playfair Display',serif;font-size:58px;
                       background:linear-gradient(135deg,#0891b2,#059669);
                       -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{r['metric_value']}</p>
                    <p style="font-size:12px;color:#64748b;">{r['model_name']} · {r['n_train']} training rows · {r['n_test']} test rows</p>
                </div>
                <style>@keyframes popIn{{from{{opacity:0;transform:scale(0.92)}}to{{opacity:1;transform:scale(1)}}}}</style>
                """, unsafe_allow_html=True)

                c1,c2,c3 = st.columns(3)
                c1.metric("Training rows", r["n_train"])
                c2.metric("Test rows",     r["n_test"])
                c3.metric("Features used", len(r["features"]))

                st.divider()
                st.markdown(stitle("Feature Importance (XAI — Explainable AI)"), unsafe_allow_html=True)
                st.caption("Which columns have the most influence on the prediction?")
                st.plotly_chart(plot_feature_importance(r["feature_importance"]),
                                use_container_width=True, key="feat_imp")

                top = r["feature_importance"].iloc[0]
                st.markdown(io(f'Most important feature: <strong>{top["Feature"]}</strong> — importance score {round(top["Importance"],3)}'), unsafe_allow_html=True)

                if r["problem_type"] == "classification" and "confusion" in r:
                    st.divider()
                    st.markdown(stitle("Confusion Matrix"), unsafe_allow_html=True)
                    classes = r.get("classes", list(range(len(r["confusion"]))))
                    if len(classes) <= 10:
                        st.plotly_chart(plot_confusion_matrix(r["confusion"], classes),
                                        use_container_width=True, key="conf_mat")

                if "report" in r:
                    st.divider()
                    st.markdown(stitle("Classification Report"), unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(r["report"]).transpose().round(3),
                                 use_container_width=True)

                if "rmse" in r:
                    st.metric("RMSE (Root Mean Squared Error)", r["rmse"])

    # ─── TAB 5 — CLUSTERING ─────────────────────
    with t5:
        st.markdown(stitle("K-Means Clustering"), unsafe_allow_html=True)
        st.caption("Unsupervised ML — groups similar rows together without needing labels.")
        num_cols = df.select_dtypes(include="number").columns.tolist()

        if len(num_cols) < 2:
            st.warning("Need at least 2 numeric columns for clustering.")
        else:
            c1,c2,c3 = st.columns(3)
            x = c1.selectbox("X axis", num_cols, key="km_x")
            y = c2.selectbox("Y axis", num_cols, index=min(1,len(num_cols)-1), key="km_y")
            k = c3.slider("Number of clusters (K)", 2, 8, 3, key="km_k")

            if st.button("▶ Run K-Means Clustering", key="km_run"):
                with st.spinner("Running K-Means..."):
                    fig_km, summary, _ = run_kmeans(df, x, y, k)
                st.plotly_chart(fig_km, use_container_width=True, key="km_chart")
                st.markdown(stitle("Cluster Summary"), unsafe_allow_html=True)
                st.dataframe(summary, use_container_width=True)
                st.markdown(io(f'Found <strong>{k} distinct clusters</strong> in your data based on <strong>{x}</strong> and <strong>{y}</strong>.'), unsafe_allow_html=True)

    # ─── TAB 6 — RECOMMENDATIONS ────────────────
    with t6:
        st.markdown(stitle("Smart Recommendations Engine"), unsafe_allow_html=True)
        st.caption("Rule-based engine — tells you exactly what to fix before running any ML model.")
        recs = get_recommendations(df)
        h = [r for r in recs if r["priority"]=="HIGH"]
        m = [r for r in recs if r["priority"]=="MEDIUM"]
        l = [r for r in recs if r["priority"]=="LOW"]
        c1,c2,c3 = st.columns(3)
        c1.metric("High priority", len(h))
        c2.metric("Medium priority", len(m))
        c3.metric("Low priority", len(l))
        st.divider()
        colors  = {"HIGH":"#fff7ed","MEDIUM":"#fffbeb","LOW":"#f0f9ff"}
        borders = {"HIGH":"#f97316","MEDIUM":"#f59e0b","LOW":"#06b6d4"}
        for rec in recs:
            p = rec["priority"]
            st.markdown(f"""
            <div style="background:{colors[p]};border-left:3px solid {borders[p]};
                 border-radius:0 12px 12px 0;padding:12px 16px;margin:6px 0;">
                <div style="font-weight:700;color:#0f172a;margin-bottom:3px;font-size:13px;">
                    {rec['icon']} {rec['action']}
                    <span style="font-size:10px;font-weight:500;color:#94a3b8;margin-left:8px;">{p}</span>
                </div>
                <div style="color:#64748b;font-size:12px;">{rec['reason']}</div>
            </div>""", unsafe_allow_html=True)

    # ─── TAB 7 — CLEANING ───────────────────────
    with t7:
        st.markdown(stitle("Data Cleaning Panel"), unsafe_allow_html=True)
        cur = get_overview(df)
        c1,c2,c3 = st.columns(3)
        c1.metric("Current rows",    cur["rows"])
        c2.metric("Missing cells",   cur["missing_cells"])
        c3.metric("Duplicate rows",  cur["duplicate_rows"])
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Handle missing values**")
            if st.button("Remove rows with nulls", use_container_width=True, key="cn1"):
                b = len(st.session_state.df)
                st.session_state.df = clean_remove_nulls(st.session_state.df)
                st.session_state.cleaning_log.append(f"Removed {b-len(st.session_state.df)} rows with null values")
                st.rerun()
            if st.button("Fill nulls with Mean", use_container_width=True, key="cn2"):
                st.session_state.df = clean_fill_mean(st.session_state.df)
                st.session_state.cleaning_log.append("Filled numeric nulls with column mean")
                st.rerun()
            if st.button("Fill nulls with Median", use_container_width=True, key="cn3"):
                st.session_state.df = clean_fill_median(st.session_state.df)
                st.session_state.cleaning_log.append("Filled numeric nulls with column median")
                st.rerun()
            if st.button("Fill nulls with Mode", use_container_width=True, key="cn4"):
                st.session_state.df = clean_fill_mode(st.session_state.df)
                st.session_state.cleaning_log.append("Filled all nulls with column mode")
                st.rerun()

        with col2:
            st.markdown("**Handle rows and outliers**")
            if st.button("Remove duplicate rows", use_container_width=True, key="cn5"):
                b = len(st.session_state.df)
                st.session_state.df = clean_remove_duplicates(st.session_state.df)
                st.session_state.cleaning_log.append(f"Removed {b-len(st.session_state.df)} duplicate rows")
                st.rerun()
            if st.button("Remove outliers (IQR method)", use_container_width=True, key="cn6"):
                b = len(st.session_state.df)
                st.session_state.df = clean_remove_outliers(st.session_state.df)
                st.session_state.cleaning_log.append(f"Removed {b-len(st.session_state.df)} outlier rows using IQR")
                st.rerun()
            if st.button("Reset to original data", use_container_width=True, key="cn7"):
                st.session_state.df = st.session_state.df_original.copy()
                st.session_state.cleaning_log = []
                st.rerun()

        if st.session_state.cleaning_log:
            st.divider()
            st.markdown("**Steps applied this session:**")
            for i, s in enumerate(st.session_state.cleaning_log, 1):
                st.markdown(io(f"{i}. {s}"), unsafe_allow_html=True)

        st.divider()
        cleaned_csv = st.session_state.df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Cleaned CSV",
            cleaned_csv, "smarteda_cleaned.csv", "text/csv",
            use_container_width=True
        )

    # ─── TAB 8 — COLUMN ANALYZER ────────────────
    with t8:
        st.markdown(stitle("Smart Column Analyzer"), unsafe_allow_html=True)
        st.caption("Select any column and get a complete deep-dive analysis.")
        sel = st.selectbox("Select a column to analyze", df.columns.tolist(), key="col_sel")
        cd = df[sel]
        is_num = pd.api.types.is_numeric_dtype(cd)

        c1,c2,c3 = st.columns(3)
        with c1: st.markdown(mcard("Type", "Numeric" if is_num else "Categorical"), unsafe_allow_html=True)
        with c2: st.markdown(mcard("Missing", cd.isnull().sum()), unsafe_allow_html=True)
        with c3: st.markdown(mcard("Unique values", cd.nunique()), unsafe_allow_html=True)

        if is_num:
            st.divider()
            c1,c2,c3,c4,c5 = st.columns(5)
            c1.metric("Mean",     round(cd.mean(),3))
            c2.metric("Median",   round(cd.median(),3))
            c3.metric("Std dev",  round(cd.std(),3))
            c4.metric("Min",      round(cd.min(),3))
            c5.metric("Max",      round(cd.max(),3))
            st.plotly_chart(plot_distribution(df, sel), use_container_width=True, key="col_dist")
            skew = cd.skew()
            if abs(skew) < 0.5:
                st.markdown(io(f"Skewness = {round(skew,2)} — fairly symmetric distribution. Good for most ML models."), unsafe_allow_html=True)
            elif skew > 1:
                st.markdown(iw(f"Skewness = {round(skew,2)} — highly right-skewed. Apply log transform before using in ML."), unsafe_allow_html=True)
            elif skew < -1:
                st.markdown(iw(f"Skewness = {round(skew,2)} — highly left-skewed. Consider sqrt or power transform."), unsafe_allow_html=True)
            else:
                st.markdown(ii(f"Skewness = {round(skew,2)} — mildly skewed. May need transform for linear models."), unsafe_allow_html=True)
        else:
            st.plotly_chart(plot_categorical(df, sel), use_container_width=True, key="col_cat")
            st.dataframe(cd.value_counts().reset_index(), use_container_width=True)

    # ─── TAB 9 — EXPORT ─────────────────────────
    with t9:
        st.markdown(stitle("Export and Resume Mode"), unsafe_allow_html=True)

        # Resume Mode
        st.markdown("#### 🎯 Resume Mode")
        st.caption("One click — auto-generates a professional resume bullet point using your actual data stats and ML results.")
        if st.button("✨ Generate My Resume Bullet Point", key="resume_btn"):
            bullet = generate_resume_bullet(df, st.session_state.ml_results)
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(6,182,212,0.05),rgba(16,185,129,0.05));
                 border:1px solid rgba(6,182,212,0.2);border-radius:14px;
                 padding:1.25rem;font-size:13px;color:#1e293b;
                 line-height:1.9;white-space:pre-wrap;
                 font-family:'Plus Jakarta Sans',sans-serif;">
{bullet}
            </div>
            """, unsafe_allow_html=True)
            st.caption("Copy this into your resume, LinkedIn profile, or interview answer.")

        st.divider()

        # PDF Report
        st.markdown("#### 📑 Full PDF Report")
        st.caption("Includes overview, auto insights, column stats, correlations, outliers, and ML suggestions.")
        pdf_bytes = generate_pdf(
            overview=get_overview(df),
            col_stats_df=get_column_stats(df),
            outliers=detect_outliers(df),
            suggestions=suggest_problem_type(df),
            quality_score=score,
            insights=get_auto_insights(df),
            top_corr=get_top_correlations(df),
            cleaning_log=st.session_state.cleaning_log
        )
        st.download_button(
            "Download PDF Report", pdf_bytes,
            "smarteda_full_report.pdf", "application/pdf",
            use_container_width=True
        )

        st.divider()

        # Cleaned CSV
        st.markdown("#### 💾 Download Cleaned Dataset")
        st.download_button(
            "Download Cleaned CSV",
            df.to_csv(index=False).encode("utf-8"),
            "smarteda_cleaned.csv", "text/csv",
            use_container_width=True, key="dl_csv_export"
        )

        # Session history
        if st.session_state.history:
            st.divider()
            st.markdown("#### 🕐 Session History")
            st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)

        # Top correlations
        st.divider()
        st.markdown("#### 🔗 Top Correlations")
        top_corr = get_top_correlations(df)
        if top_corr:
            for a, b, v in top_corr:
                strength = "Strong" if v > 0.7 else "Moderate"
                st.markdown(ii(f"<strong>{a}</strong> ↔ <strong>{b}</strong>: {strength} correlation (r = {v})"), unsafe_allow_html=True)
        else:
            st.info("Need at least 2 numeric columns for correlation analysis.")