import threading
import requests
import time
import sys
import os
import base64
import sqlite3
from flask import Flask, render_template_string, make_response, request, redirect, session, url_for

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, url TEXT, score REAL, memory TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    try:
        c.execute("SELECT memory FROM history LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("ALTER TABLE history ADD COLUMN memory TEXT")
    
    conn.commit()
    conn.close()

init_db()

# --- APP 1: THE GENERATOR (Port 5001) ---
generator = Flask("Generator")
@generator.route('/')
def gen_index():
    # This is the updated creative HTML for the target site
    html_content = """
    <div style="background:#0a0a0a; color:#00ff41; font-family:monospace; height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center;">
        <h1 style="font-size:3.5rem; filter: drop-shadow(0 0 10px #00ff41);">🍪 COOKIE LAB</h1>
        <div style="border-left: 3px solid #00ff41; padding: 20px; background:rgba(0,255,65,0.05); text-align:left; border-radius: 0 15px 15px 0;">
            <p style="margin:5px 0;">> INITIALIZING 10 SECURITY PAYLOADS...</p>
            <p style="margin:5px 0;">> INJECTING: HTTP_ONLY & SECURE FLAGS...</p>
            <p style="margin:5px 0; color: #fff;">> STATUS: ALL 10 COOKIES PLANTED [OK]</p>
        </div>
        <p style="margin-top:30px; opacity:0.7;">Audit Target: <code style="background:#222; padding:8px; color:#00ff41; border: 1px solid #333;">http://127.0.0.1:5001</code></p>
    </div>
    """
    resp = make_response(html_content)
    
    # --- 10 COOKIES TOTAL ---
    
    # 7 SECURE COOKIES (These keep your score high)
    resp.set_cookie('strictly_secure', 'auth_v1_992', secure=True, httponly=True, samesite='Strict')
    resp.set_cookie('session_id', 'sess_001', secure=True, httponly=True)
    resp.set_cookie('token_vault', 'tk_882', secure=True, httponly=True)
    resp.set_cookie('user_region', 'Mysuru_IN', secure=True, httponly=True)
    resp.set_cookie('app_theme', 'dark_mode', secure=True)
    resp.set_cookie('login_status', 'active', secure=True)
    resp.set_cookie('device_id', 'dev_441', secure=True, httponly=True)

    # 2 INSECURE COOKIES (-1.5 each = -3.0 total)
    resp.set_cookie('insecure_val', 'light_mode', secure=False)
    resp.set_cookie('legacy_id', 'old_992', secure=False)

    # 1 TRACKING COOKIE (-1.0 total)
    resp.set_cookie('marketing_track', 'campaign_01', secure=True, httponly=False)

    return resp
    
    # 1-3: Your Original Cookies
    resp.set_cookie('strictly_secure', 'auth_v1_992837465', secure=True, httponly=True, samesite='Strict')
    resp.set_cookie('insecure_val', 'user_pref_light_mode', secure=False)
    resp.set_cookie('js_exposed', 'temp_token_00192837465', httponly=False)
    
    # 4-10: New Cookies to make the list 10
    resp.set_cookie('session_id', 'sess_9928374', secure=True, httponly=True)
    resp.set_cookie('track_user', 'marketing_id_882', secure=False, httponly=False) # High Risk
    resp.set_cookie('ad_pref', 'sports_news_tech', secure=True) # Tracking
    resp.set_cookie('legacy_token', 'old_auth_data', secure=False) # High Risk
    resp.set_cookie('theme_color', 'emerald_green', secure=True, httponly=True)
    resp.set_cookie('region_code', 'IN_KA_MYS', secure=True)
    resp.set_cookie('visit_count', '42', secure=False) # High Risk

    return resp

# --- APP 2: THE ANALYZER (Port 5000) ---
analyzer = Flask("Analyzer")
analyzer.secret_key = "hackathon_pro_key"

def get_base64_logo():
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_path, "static", "logo.png")
        with open(logo_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except: return ""

LOGO_DATA = get_base64_logo()

ENHANCED_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: linear-gradient(135deg, #0c0c1a 0%, #1a0d2e 50%, #0f0f23 100%);
    --bg-secondary: linear-gradient(145deg, rgba(20, 20, 40, 0.8), rgba(10, 10, 25, 0.9));
    --glass: rgba(255, 255, 255, 0.05);
    --glass-glow: rgba(255, 255, 255, 0.1);
    --accent-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --accent-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --accent-success: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --accent-warning: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    --accent-danger: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    --text-primary: #ffffff;
    --text-secondary: rgba(255, 255, 255, 0.7);
    --text-muted: rgba(255, 255, 255, 0.4);
    --border-glass: rgba(255, 255, 255, 0.12);
    --shadow-lg: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    --shadow-xl: 0 35px 60px -12px rgba(0, 0, 0, 0.8);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body { 
    background: var(--bg-primary);
    color: var(--text-primary);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
}

body::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
    z-index: -1; animation: bgShift 20s ease-in-out infinite;
}

@keyframes bgShift { 0%, 100% { transform: scale(1) rotate(0deg); } 50% { transform: scale(1.1) rotate(180deg); } }

/* --- SIDEBAR --- */
.sidebar { 
    width: 72px; height: 100vh; 
    background: rgba(15, 15, 35, 0.9);
    backdrop-filter: blur(30px); border-right: 1px solid var(--border-glass);
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex; flex-direction: column; position: fixed; z-index: 1000;
    box-shadow: var(--shadow-lg);
}
.sidebar.expanded { width: 280px; }
.nav-item { 
    color: var(--text-secondary); text-decoration: none; padding: 20px 24px; 
    display: flex; align-items: center; gap: 20px; position: relative;
    transition: all 0.3s ease; font-weight: 500; font-size: 15px;
}
.nav-item::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
    background: var(--accent-primary); transform: scaleY(0); transition: 0.3s ease;
}
.nav-item:hover { background: rgba(255, 255, 255, 0.08); color: var(--text-primary); padding-left: 32px; }
.nav-item:hover::before, .nav-item.active::before { transform: scaleY(1); }
.nav-text { opacity: 0; transition: 0.3s ease; white-space: nowrap; }
.sidebar.expanded .nav-text { opacity: 1; }

/* --- MAIN CONTENT --- */
.main-container {
    margin-left: 72px; min-height: 100vh; padding: 2rem; transition: margin-left 0.5s ease;
}
.sidebar.expanded ~ .main-container { margin-left: 280px; }

/* --- GLASS CARDS --- */
.glass-card { 
    background: var(--glass); backdrop-filter: blur(35px); 
    border: 1px solid var(--border-glass); border-radius: 24px;
    box-shadow: var(--shadow-xl); position: relative; overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.glass-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: var(--glass-glow); transform: scaleX(0); transition: 0.4s ease;
}
.glass-card:hover::before { transform: scaleX(1); }
.glass-card:hover { transform: translateY(-8px); box-shadow: 0 45px 80px -20px rgba(0, 0, 0, 0.6); }

/* --- ANIMATIONS --- */
@keyframes floatIn { from { opacity: 0; transform: translateY(30px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }
@keyframes pulseGlow { 0%, 100% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.3); } 50% { box-shadow: 0 0 40px rgba(102, 126, 234, 0.6); } }
.fade-in { animation: floatIn 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards; opacity: 0; }
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }

/* --- BUTTONS --- */
.btn-gradient {
    background: var(--accent-primary); color: white; border: none;
    padding: 18px 36px; border-radius: 16px; font-weight: 700; cursor: pointer;
    font-size: 15px; text-transform: uppercase; letter-spacing: 1px;
    position: relative; overflow: hidden; transition: all 0.4s ease;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}
.btn-gradient:hover { transform: translateY(-4px); box-shadow: 0 20px 40px rgba(102, 126, 234, 0.6); }
.btn-gradient:active { transform: translateY(-2px); }

.btn-secondary { background: transparent; color: var(--text-primary); border: 2px solid var(--glass-glow); }
.btn-secondary:hover { background: rgba(255, 255, 255, 0.1); }

/* --- INPUTS --- */
.input-glass {
    width: 100%; padding: 20px; background: rgba(255, 255, 255, 0.03);
    border: 2px solid var(--border-glass); border-radius: 16px;
    color: var(--text-primary); font-size: 16px; font-weight: 500;
    transition: all 0.3s ease; backdrop-filter: blur(10px);
}
.input-glass:focus {
    outline: none; border-color: var(--accent-primary);
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2);
    background: rgba(255, 255, 255, 0.08);
}

/* --- METRICS CARDS --- */
.metric-card {
    background: var(--glass); backdrop-filter: blur(25px);
    border: 1px solid var(--border-glass); border-radius: 20px;
    padding: 2rem; text-align: center; flex: 1; transition: all 0.4s ease;
}
.metric-number { font-size: 3.5rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; line-height: 1; }
.metric-label { font-size: 0.85rem; opacity: 0.8; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.5rem; }

/* --- TABLES --- */
.table-container { width: 100%; margin-top: 2rem; }
table { width: 100%; border-collapse: separate; border-spacing: 0 12px; font-size: 15px; }
th { 
    text-align: left; padding: 20px; color: var(--text-muted); 
    font-weight: 600; font-size: 0.85rem; text-transform: uppercase;
    letter-spacing: 1px; background: transparent;
}
td { 
    background: var(--glass); padding: 20px; border-radius: 16px;
    backdrop-filter: blur(20px); border: 1px solid var(--border-glass);
    transition: all 0.3s ease;
}
tr:hover td { transform: scale(1.02); background: rgba(255, 255, 255, 0.1); }

/* --- BADGES --- */
.badge {
    padding: 8px 16px; border-radius: 20px; font-size: 0.8rem;
    font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;
    backdrop-filter: blur(10px);
}
.badge-safe { background: rgba(79, 172, 254, 0.2); color: #4facfe; border: 1px solid rgba(79, 172, 254, 0.4); }
.badge-risk { background: rgba(255, 107, 107, 0.2); color: #ff6b6b; border: 1px solid rgba(255, 107, 107, 0.4); }
.badge-tracking { background: rgba(250, 112, 154, 0.2); color: #fa709a; border: 1px solid rgba(250, 112, 154, 0.4); }

/* --- RESPONSIVE --- */
@media (max-width: 768px) {
    .sidebar { width: 72px !important; }
    .main-container { margin-left: 72px !important; padding: 1rem; }
    .metric-card { margin-bottom: 1rem; }
}
</style>
"""

def get_layout(content, show_sidebar=True):
    logo_src = f"data:image/png;base64,{LOGO_DATA}"
    sidebar_html = ""
    if show_sidebar:
        sidebar_html = f"""
        <div class="sidebar" id="sidebar">
            <div style="padding: 24px 24px 16px;"><div style="width:24px;height:24px;background:var(--accent-primary);border-radius:8px;"></div></div>
            <a href="/" class="nav-item active"><span style="font-size:20px;">🏠</span><span class="nav-text">Dashboard</span></a>
            <a href="/history" class="nav-item"><span style="font-size:20px;">📊</span><span class="nav-text">History</span></a>
            <a href="/logout" class="nav-item" style="margin-top:auto;"><span style="font-size:20px;color:#ff6b6b;">🚪</span><span class="nav-text">Sign Out</span></a>
        </div>
        <div class="main-container">
            {content}
        </div>
        <script>
        const sidebar = document.getElementById('sidebar');
        sidebar.addEventListener('mouseenter', () => sidebar.classList.add('expanded'));
        sidebar.addEventListener('mouseleave', () => sidebar.classList.remove('expanded'));
        </script>
        """
    return render_template_string(f"{ENHANCED_STYLE} {sidebar_html}")

@analyzer.route('/')
def home():
    if 'user' not in session: return redirect(url_for('login'))
    return get_layout(f"""
        <div style="display: flex; flex-direction: column; align-items: center; min-height: 80vh; justify-content: center;">
            <div class="glass-card fade-in delay-1" style="max-width: 500px; width: 100%; padding: 3rem; text-align: center;">
                <div style="background: var(--accent-primary); width: 80px; height: 80px; border-radius: 24px; margin: 0 auto 2rem; display: flex; align-items: center; justify-content: center; box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);">
                    <span style="font-size: 32px;">🔍</span>
                </div>
                <h1 style="font-size: 2.5rem; font-weight: 800; background: var(--accent-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 1rem; letter-spacing: -0.02em;">Security Audit</h1>
                <p style="color: var(--text-secondary); font-size: 1.2rem; margin-bottom: 2.5rem; line-height: 1.6;">Analyze cookies & security posture of any domain</p>
                <form action="/analyze" method="POST" style="width: 100%;">
                    <input type="text" name="url" value="http://127.0.0.1:5001" class="input-glass" placeholder="Enter target URL (e.g. http://127.0.0.1:5001)" required style="margin-bottom: 1.5rem;">
                    <button type="submit" class="btn-gradient" style="width: 100%;">🚀 Launch Analysis</button>
                </form>
            </div>
        </div>
    """)

@analyzer.route('/login', methods=['GET', 'POST'])
def login():
    logo_src = f"data:image/png;base64,{LOGO_DATA}"
    if request.method == 'POST':
        user, pwd = request.form['user'], request.form['pwd']
        conn = sqlite3.connect('users.db'); c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
        if c.fetchone():
            session['user'] = user
            return redirect(url_for('home'))
        return "Invalid Credentials!"
    return f"""
    {ENHANCED_STYLE}
    <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem;">
        <div class="glass-card fade-in" style="max-width: 420px; width: 100%; padding: 3.5rem; text-align: center;">
            {f'<img src="{logo_src}" style="width: 120px; margin-bottom: 2rem; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.3));">' if logo_src else '<div style="width:120px;height:120px;background:var(--accent-primary);border-radius:24px;margin:0 auto 2rem;"></div>'}
            <h1 style="font-size: 2.2rem; font-weight: 800; margin-bottom: 2rem; letter-spacing: -0.02em;">System Access</h1>
            <form method='POST' style="width: 100%;">
                <input name='user' class="input-glass" placeholder='Username' required style="margin-bottom: 1.5rem;">
                <input type='password' name='pwd' class="input-glass" placeholder='Password' required style="margin-bottom: 2rem;">
                <button class='btn-gradient' style="width: 100%;">🔐 Authorize Access</button>
            </form>
            <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--border-glass);">
                <a href="/signup" style="color: var(--text-secondary); text-decoration: none; font-weight: 500;">New user? Create Account</a>
            </div>
        </div>
    </div>
    """

@analyzer.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user, pwd = request.form['user'], request.form['pwd']
        conn = sqlite3.connect('users.db'); c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?)", (user, pwd))
        conn.commit(); conn.close()
        return redirect(url_for('login'))
    return f"""
    {ENHANCED_STYLE}
    <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem;">
        <div class="glass-card fade-in" style="max-width: 420px; width: 100%; padding: 3.5rem; text-align: center;">
            <h1 style="font-size: 2.2rem; font-weight: 800; margin-bottom: 1rem; background: var(--accent-secondary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Create Account</h1>
            <p style="color: var(--text-secondary); margin-bottom: 2.5rem;">Join the security audit platform</p>
            <form method='POST' style="width: 100%;">
                <input name='user' class="input-glass" placeholder='Choose Username' required style="margin-bottom: 1.5rem;">
                <input type='password' name='pwd' class="input-glass" placeholder='Choose Password' required style="margin-bottom: 2rem;">
                <button class='btn-gradient' style="width: 100%;">🎉 Create Account</button>
            </form>
            <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--border-glass);">
                <a href="/login" style="color: var(--text-secondary); text-decoration: none; font-weight: 500;">← Back to Login</a>
            </div>
        </div>
    </div>
    """

@analyzer.route('/analyze', methods=['POST'])
def analyze():
    if 'user' not in session: return redirect(url_for('login'))
    target = request.form.get('url')
    try:
        r = requests.get(target, timeout=3)
        cookies = r.cookies
        rows = []
        total_memory = 0
        score = 10.0
        for c in cookies:
            risk = "Safe"; color = "var(--accent-success)"; badge_class = "badge-safe"
            mem_usage = sys.getsizeof(c.name) + sys.getsizeof(c.value)
            total_memory += mem_usage
            is_httponly = 'HttpOnly' in c._rest or c.has_nonstandard_attr('HttpOnly')
            if not c.secure: 
                risk = "High Risk"; score -= 1.5; color = "var(--accent-danger)"; badge_class = "badge-risk"
            elif "ads" in c.name.lower() or "track" in c.name.lower(): 
                risk = "Tracking"; score -= 1.0; color = "var(--accent-warning)"; badge_class = "badge-tracking"
            rows.append(f"""
                <tr>
                    <td style="font-weight: 600; font-family: 'JetBrains Mono', monospace;">{c.name}</td>
                    <td><span style="font-size: 18px;">{'🔒' if c.secure else '🔓'}</span></td>
                    <td><span style="font-size: 18px;">{'🚫' if is_httponly else '📄'}</span></td>
                    <td style="color: var(--accent-primary); font-family: 'JetBrains Mono', monospace; font-weight: 600;">{mem_usage} B</td>
                    <td><span class='badge {badge_class}'>{risk}</span></td>
                </tr>
            """)
            # --- NEW: HEADER SECURITY CHECK (Insert here) ---
        headers = r.headers
        header_rows = []
        security_headers = {
            'Content-Security-Policy': 'Prevents XSS Attacks',
            'Strict-Transport-Security': 'Forces HTTPS',
            'X-Frame-Options': 'Prevents Clickjacking'
        }
        
        for header, description in security_headers.items():
            exists = header in headers
            h_status = "✅ PROTECTED" if exists else "❌ VULNERABLE"
            h_color = "var(--accent-success)" if exists else "var(--accent-danger)"
            if not exists: score -= 1.0 # Deducting points for missing headers
            
            header_rows.append(f"""
                <tr>
                    <td style="font-weight: 600;">{header}</td>
                    <td style="font-size: 0.85rem; opacity: 0.7;">{description}</td>
                    <td style="color: {h_color}; font-weight: 800; font-family: 'JetBrains Mono', monospace;">{h_status}</td>
                </tr>
            """)
        
        # SAVE TO DB
        conn = sqlite3.connect('users.db', check_same_thread=False); c = conn.cursor()
        c.execute("INSERT INTO history (username, url, score, memory) VALUES (?, ?, ?, ?)", (session['user'], target, round(score, 1), f"{total_memory} B"))
        conn.commit(); conn.close()

        score_display = max(0.5, round(score, 1))
        score_color = "var(--accent-success)" if score_display >= 7 else "var(--accent-warning)" if score_display >= 4 else "var(--accent-danger)"

        res_header = f"""
        <div style="display: flex; gap: 2rem; flex-wrap: wrap; justify-content: center; margin-bottom: 3rem;">
            <div class="glass-card fade-in metric-card" style="min-width: 280px;">
                <div class="metric-number" style="background: var(--accent-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{target}</div>
                <div class="metric-label">Target Analyzed</div>
            </div>
            <div class="glass-card fade-in metric-card delay-1" style="min-width: 280px;">
                <div class="metric-number" style="color: {score_color};">{score_display}/10</div>
                <div class="metric-label">Privacy Score</div>
            </div>
            <div class="glass-card fade-in metric-card delay-2" style="min-width: 280px;">
                <div class="metric-number" style="color: var(--accent-secondary);">{total_memory} B</div>
                <div class="metric-label">Memory Footprint</div>
            </div>
        </div>
        <div class="table-container fade-in delay-1">
            <div class="glass-card" style="padding: 2rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
                    <h2 style="font-size: 1.8rem; font-weight: 800; margin: 0;">Cookie Analysis</h2>
                    <span style="background: rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 12px; font-size: 0.9rem;">{len(rows)} cookies found</span>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th style="width: 30%;">Cookie Name</th>
                            <th style="width: 12%;">Secure</th>
                            <th style="width: 12%;">HttpOnly</th>
                            <th style="width: 16%;">Memory</th>
                            <th>Risk Level</th>
                        </tr>
                    </thead>
                    <tbody>{''.join(rows)}</tbody>
                </table>
            </div>
        </div>
        <div style="text-align: center; margin-top: 3rem;">
            <a href="/" class="btn-gradient" style="padding: 20px 48px; font-size: 16px; text-decoration: none;">← New Analysis</a>
        </div>
        
        """
        return get_layout(res_header)
    except Exception as e: 
        return get_layout(f"<div class='glass-card' style='max-width:500px; margin: 2rem auto; padding: 3rem; text-align:center;'><h2 style='color: var(--accent-danger);'>Analysis Error</h2><p style='color: var(--text-secondary);'>{str(e)}</p><a href='/' class='btn-gradient' style='display:inline-block; margin-top:2rem;'>Try Again</a></div>")

@analyzer.route('/history')
def history():
    if 'user' not in session: return redirect(url_for('login'))
    conn = sqlite3.connect('users.db', check_same_thread=False); c = conn.cursor()
    c.execute("SELECT url, score, memory, timestamp FROM history WHERE username=? ORDER BY timestamp DESC LIMIT 50", (session['user'],))
    data = c.fetchall()
    conn.close()
    
    if not data:
        content = """
        <div style="text-align: center; padding: 4rem 2rem;">
            <div class="glass-card" style="display: inline-block; padding: 4rem; max-width: 500px;">
                <span style="font-size: 6rem; display: block; margin-bottom: 2rem;">📊</span>
                <h2 style="font-size: 2rem; margin-bottom: 1rem;">No Audit History</h2>
                <p style="color: var(--text-secondary); font-size: 1.1rem;">Run your first security analysis to see results here</p>
                <a href="/" class="btn-gradient" style="margin-top: 2rem; display: inline-block; padding: 18px 36px;">🚀 Start Analysis</a>
            </div>
        </div>
        """
    else:
        h_rows = "".join([f"""
            <tr>
                <td style="font-weight: 600; max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{row[0]}</td>
                <td><span style="background: rgba(79,172,254,0.2); color: #4facfe; padding: 6px 12px; border-radius: 20px; font-weight: 700;">{row[1]}/10</span></td>
                <td style="font-family: 'JetBrains Mono', monospace; color: var(--accent-secondary);">{row[2]}</td>
                <td style="font-size: 0.85rem; color: var(--text-muted);">{row[3]}</td>
            </tr>
        """ for row in data])
        
        content = f"""
        <div style="margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; background: var(--accent-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Audit History</h1>
            <p style="color: var(--text-secondary);">Your recent security scans</p>
        </div>
        <div class="glass-card table-container fade-in">
            <table>
                <thead>
                    <tr>
                        <th>Target URL</th>
                        <th>Privacy Score</th>
                        <th>Memory Usage</th>
                        <th>Timestamp</th>
                    </tr>
                </thead>
                <tbody>{h_rows}</tbody>
            </table>
        </div>
        """
    
    return get_layout(content)

@analyzer.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    t1 = threading.Thread(target=lambda: generator.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False))
    t2 = threading.Thread(target=lambda: analyzer.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False))
    t1.daemon = t2.daemon = True
    t1.start(); t2.start()
    while True: time.sleep(1)