import streamlit as st
import time
import difflib
from src.config import settings
from src.core.pipeline import RepoGuardPipeline

# --- PAGE SETUP ---
st.set_page_config(
    page_title="RepoGuard AI | Autonomous AppSec Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN CYBERPUNK / APPSEC THEME INJECTION ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Background Canvas */
    .stApp {
        background-color: #090d14;
        background-image: 
            radial-gradient(at 0% 0%, rgba(31, 111, 235, 0.12) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(56, 139, 253, 0.08) 0px, transparent 40%),
            radial-gradient(at 50% 100%, rgba(46, 160, 67, 0.06) 0px, transparent 50%);
        color: #e6edf3;
    }

    /* Branded Hero Ribbon */
    .hero-container {
        position: relative;
        background: rgba(22, 27, 34, 0.85);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 14px;
        padding: 22px 28px;
        margin-bottom: 22px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    }
    .hero-container::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, #1f6feb, #388bfd, #2ea043, #58a6ff);
    }
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(56, 139, 253, 0.12);
        border: 1px solid rgba(56, 139, 253, 0.3);
        padding: 3px 10px;
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #58a6ff;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .pulse-dot {
        width: 7px;
        height: 7px;
        background: #3fb950;
        border-radius: 50%;
        box-shadow: 0 0 8px #3fb950;
        display: inline-block;
    }

    /* Architecture Visualizer Stepper */
    .agent-pipeline-bar {
        display: flex;
        gap: 12px;
        margin-bottom: 22px;
    }
    .agent-box {
        flex: 1;
        background: rgba(22, 27, 34, 0.75);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 10px;
        padding: 12px 16px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .agent-icon {
        font-size: 1.4rem;
    }
    .agent-title {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8b949e;
        font-weight: 700;
    }
    .agent-subtitle {
        font-size: 0.85rem;
        font-weight: 700;
        color: #f0f6fc;
    }

    /* Mock IDE Window for Code Area */
    .ide-header {
        background: #161b22;
        border: 1px solid #30363d;
        border-bottom: none;
        border-radius: 10px 10px 0 0;
        padding: 8px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .ide-dots {
        display: flex;
        gap: 6px;
    }
    .ide-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }
    .dot-r { background: #ff5f56; }
    .dot-y { background: #ffbd2e; }
    .dot-g { background: #27c93f; }

    /* Custom Textarea Styling */
    .stTextArea textarea {
        background-color: #0d1117 !important;
        color: #e6edf3 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13px !important;
        border: 1px solid #30363d !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        padding: 14px !important;
    }
    .stTextArea textarea:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 10px rgba(88, 166, 255, 0.25) !important;
    }

    /* Glassmorphism Metric Cards */
    .glass-card {
        background: rgba(22, 27, 34, 0.75);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 12px;
        padding: 18px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .glass-card:hover {
        border-color: #58a6ff;
        transform: translateY(-2px);
    }
    .card-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #8b949e;
        margin-bottom: 6px;
        font-weight: 600;
    }
    .card-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #f0f6fc;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Badge Pills */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-family: 'JetBrains Mono', monospace;
    }
    .badge-critical { background: rgba(248, 81, 73, 0.15); color: #f85149; border: 1px solid #f85149; }
    .badge-high { background: rgba(210, 153, 34, 0.15); color: #d29922; border: 1px solid #d29922; }
    .badge-success { background: rgba(46, 160, 67, 0.15); color: #3fb950; border: 1px solid #3fb950; }

    /* Button Glow Styling */
    .stButton > button {
        background: linear-gradient(135deg, #1f6feb 0%, #238636 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.65rem 1.6rem !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 15px rgba(31, 111, 235, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(35, 134, 54, 0.45) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DEMO SAMPLES ---
SAMPLE_CODE = '''import os
import sqlite3
import hashlib
import subprocess

# 1. HARDCODED SENSITIVE SECRET / API TOKEN
DATABASE_BACKUP_KEY = "sk_test_9948572019485710293847561029"
ADMIN_SESSION_SALT = "static_salt_constant_for_auth"

def compute_user_password_hash(password: str) -> str:
    """
    2. WEAK CRYPTOGRAPHY & INSECURE HASHING:
    Uses single-pass, fast MD5 hashing for credential storage without salt/KDF.
    """
    return hashlib.md5(password.encode("utf-8")).hexdigest()

def fetch_user_record(account_id: str):
    """
    3. SQL INJECTION (SQLi):
    Tainted input from user argument directly interpolated into raw SQL statement.
    """
    conn = sqlite3.connect("production.db")
    cursor = conn.cursor()
    query = f"SELECT id, username, email FROM accounts WHERE id = '{account_id}'"
    cursor.execute(query)
    return cursor.fetchone()

def load_user_document(file_name: str) -> str:
    """
    4. PATH TRAVERSAL (Arbitrary File Read):
    Concatenates untrusted user-supplied filename without directory boundary validation.
    """
    target_path = f"/var/data/uploads/{file_name}"
    with open(target_path, "r", encoding="utf-8") as f:
        return f.read()

def run_server_ping(target_host: str) -> None:
    """
    5. OS COMMAND INJECTION:
    Executes raw string command with shell=True allowing command chaining (e.g., '; rm -rf /').
    """
    command = f"ping -c 1 {target_host}"
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as exc:
        print(f"Network check error: {exc}")

def track_user_actions(action_name: str, audit_trail=[]) -> list:
    """
    6. PYTHON ANTI-PATTERN (Mutable Default Argument):
    `audit_trail=[]` is instantiated at function definition time, leaking state across invocations.
    """
    audit_trail.append(action_name)
    return audit_trail
'''

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown("### 🛡️ **RepoGuard Ops**")
    st.caption("Autonomous SAST & Code Remediation")
    st.markdown("---")
    
    st.markdown("**Core Configuration**")
    model_choice = st.selectbox("LLM Inference Engine", [settings.model_name], index=0)
    max_passes = st.slider("Convergence Loop Depth", min_value=1, max_value=5, value=settings.max_iterations)
    
    st.markdown("---")
    st.markdown("**Sample Selection**")
    mode = st.radio(
        "Source Target", 
        [
            "⚡ Full Vulnerability Bundle (6 Flaws)",
            "🛡️ Clean Compliant Code (Fast-Path Exit)",
            "🗄️ SQL Injection & Insecure Auth",
            "💻 Command Injection & Path Traversal",
            "✍️ Custom Code Editor (Paste/Type)"
        ]
    )

# --- NEW MODERN HERO HEADER ---
st.markdown("""
<div class="hero-container">
    <div class="hero-pill">
        <span class="pulse-dot"></span> AUTONOMOUS MULTI-AGENT APPSec READY
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; background: linear-gradient(90deg, #58a6ff, #3fb950); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                RepoGuard Autonomous Security Platform
            </h1>
            <p style="color: #8b949e; font-size: 0.95rem; margin: 6px 0 0 0;">
                Production-grade Taint Flow Analysis with Iterative Auto-Remediation & Zero-Flaw Convergence
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- VISUAL ARCHITECTURE PIPELINE PREVIEW ---
st.markdown("""
<div class="agent-pipeline-bar">
    <div class="agent-box">
        <span class="agent-icon">🔍</span>
        <div>
            <div class="agent-title">Agent 1: Auditor</div>
            <div class="agent-subtitle">AST Taint & Sink Detection</div>
        </div>
    </div>
    <div class="agent-box">
        <span class="agent-icon">⚖️</span>
        <div>
            <div class="agent-title">Gatekeeper Loop</div>
            <div class="agent-subtitle">Convergence & Bypass Check</div>
        </div>
    </div>
    <div class="agent-box">
        <span class="agent-icon">🛠️</span>
        <div>
            <div class="agent-title">Agent 2: Fixer</div>
            <div class="agent-subtitle">Surgical AST Sanitization</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Code Input Logic
target_code = ""
target_filename = "vulnerable_target.py"

# Custom IDE window bar
st.markdown("""
<div class="ide-header">
    <div class="ide-dots">
        <span class="ide-dot dot-r"></span>
        <span class="ide-dot dot-y"></span>
        <span class="ide-dot dot-g"></span>
    </div>
    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #8b949e;">target_source.py (Python 3)</span>
    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #58a6ff;">READY TO AUDIT</span>
</div>
""", unsafe_allow_html=True)

if mode == "✍️ Custom Code Editor (Paste/Type)":
    target_code = st.text_area(
        label="Code Input Panel",
        value="""# Paste your Python code here
import sqlite3

def find_account(user_id):
    conn = sqlite3.connect("data.db")
    query = f"SELECT * FROM accounts WHERE id = '{user_id}'"
    return conn.cursor().execute(query).fetchall()
""",
        height=280,
        help="Type or paste any Python snippet directly.",
        label_visibility="collapsed"
    )
    target_filename = "custom_script.py"
elif mode == "🛡️ Clean Compliant Code (Fast-Path Exit)":
    try:
        with open("samples/clean_sample.py", "r", encoding="utf-8") as f:
            clean_preset = f.read()
    except Exception:
        clean_preset = "# clean_sample.py"
    target_code = st.text_area(
        label="Code Input Panel",
        value=clean_preset,
        height=280,
        label_visibility="collapsed"
    )
    target_filename = "samples/clean_sample.py"
    st.caption("Loaded preset: 0 vulnerabilities. Demonstrates zero-flaw gatekeeper bypass (Agent 2 skipped).")
elif mode == "🗄️ SQL Injection & Insecure Auth":
    try:
        with open("samples/sqli_demo.py", "r", encoding="utf-8") as f:
            sqli_preset = f.read()
    except Exception:
        sqli_preset = "# sqli_demo.py"
    target_code = st.text_area(
        label="Code Input Panel",
        value=sqli_preset,
        height=280,
        label_visibility="collapsed"
    )
    target_filename = "samples/sqli_demo.py"
    st.caption("Loaded preset: SQL Injection, Hardcoded Secrets, and Weak MD5 password storage.")
elif mode == "💻 Command Injection & Path Traversal":
    try:
        with open("samples/command_exec_demo.py", "r", encoding="utf-8") as f:
            cmd_preset = f.read()
    except Exception:
        cmd_preset = "# command_exec_demo.py"
    target_code = st.text_area(
        label="Code Input Panel",
        value=cmd_preset,
        height=280,
        label_visibility="collapsed"
    )
    target_filename = "samples/command_exec_demo.py"
    st.caption("Loaded preset: OS Command Injection (`shell=True`), `os.system()`, and arbitrary Path Traversal.")
else:
    target_code = st.text_area(
        label="Code Input Panel",
        value=SAMPLE_CODE,
        height=280,
        label_visibility="collapsed"
    )
    target_filename = "samples/vulnerable_sample.py"
    st.caption("Loaded preset: 6 security issues (Hardcoded Secrets, MD5 Hash, SQLi, Path Traversal, Command Injection, Mutable Arg).")

# --- ACTION & SCAN WORKSPACE ---
if target_code:
    st.markdown("<br>", unsafe_allow_html=True)
    scan_triggered = st.button("🚀 Run Autonomous Remediation Pipeline", use_container_width=True)
    
    if scan_triggered:
        st.markdown("#### 🔄 **Execution Trace**")
        status_box = st.status("Initializing Security Pipeline...", expanded=True)
        
        pipeline = RepoGuardPipeline(max_iterations=max_passes)

        def streamlit_trace_handler(event: dict):
            kind = event.get("event")
            pass_num = event.get("pass_num", 1)
            
            if kind == "audit_start":
                status_box.write(f"🔎 **Pass {pass_num}/{max_passes}: Agent 1 (Auditor) analyzing taint-sinks...**")
            elif kind == "fast_path_exit":
                status_box.write("✅ **Fast-path Exit:** No vulnerabilities found. Source code is secure.")
            elif kind == "convergence_exit":
                status_box.write(f"🎉 **Convergence Reached on Pass {pass_num}:** Re-audit verified 0 residual flaws!")
            elif kind == "fix_start":
                count = event.get("vulnerabilities", 0)
                status_box.write(f"⚠️ **Pass {pass_num}: Flagged {count} vulnerability(ies). Dispatching Agent 2 (Fixer)...**")
            elif kind == "syntax_error":
                status_box.write(f"⚠️ **AST Gatekeeper Notice:** Syntax issue detected in candidate fix; preserving parseable code state.")
            elif kind == "max_iterations_reached":
                count = event.get("vulnerabilities", 0)
                status_box.write(f"🛑 **Maximum Passes Reached ({max_passes}):** {count} residual flaw(s) remain.")

        start_time = time.time()
        result = pipeline.run(target_filename, target_code, on_step=streamlit_trace_handler)
        elapsed_time = round(time.time() - start_time, 2)
        status_box.update(label=f"Pipeline Completed in {elapsed_time}s", state="complete", expanded=False)

        current_code = result.final_code
        audit_history = result.audit_history
        is_converged = result.converged
        final_report = result.final_report
        initial_report = result.initial_report

        # --- EXECUTIVE DASHBOARD METRICS ---
        st.markdown("### 📊 **Audit Summary & Telemetry**")
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            initial_count = audit_history[0]['count'] if audit_history else 0
            st.markdown(f"""
                <div class="glass-card">
                    <div class="card-title">Initial Vulnerabilities</div>
                    <div class="card-value" style="color: #f85149;">{initial_count}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with m2:
            st.markdown(f"""
                <div class="glass-card">
                    <div class="card-title">Loop Iterations</div>
                    <div class="card-value" style="color: #58a6ff;">{len(audit_history)} / {max_passes}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with m3:
            residual = 0 if is_converged else (audit_history[-1]['count'] if audit_history else 0)
            color = "#3fb950" if residual == 0 else "#f85149"
            st.markdown(f"""
                <div class="glass-card">
                    <div class="card-title">Residual Vulnerabilities</div>
                    <div class="card-value" style="color: {color};">{residual}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with m4:
            badge = '<span class="badge badge-success">CLEAN / VERIFIED</span>' if is_converged else '<span class="badge badge-critical">ACTION NEEDED</span>'
            st.markdown(f"""
                <div class="glass-card">
                    <div class="card-title">Final Gatekeeper Status</div>
                    <div style="margin-top: 10px;">{badge}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # --- TABS FOR DETAILED INSPECTION ---
        tab_inspect, tab_findings, tab_unified_diff, tab_download = st.tabs([
            "🔎 Side-by-Side Review & Copy", 
            "📋 Identified Flaws", 
            "📑 Unified Diff View", 
            "💾 Export Fixed Script"
        ])

        with tab_inspect:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### 🚨 **Original Vulnerable Source**")
                st.code(target_code, language="python", line_numbers=True)
            with c2:
                st.markdown("##### 🛡️ **RepoGuard Remediated Source**")
                st.code(current_code, language="python", line_numbers=True)

        with tab_findings:
            report_to_show = initial_report if (initial_report and initial_report.vulnerabilities) else final_report
            if report_to_show and report_to_show.vulnerabilities:
                st.markdown("#### Detected Weaknesses & Sinks")
                if is_converged and initial_report and initial_report.vulnerabilities:
                    st.success("✅ All detected vulnerabilities below were autonomously resolved by Agent 2 and verified by Agent 1!")
                for item in report_to_show.vulnerabilities:
                    badge_style = "badge-critical" if item.severity.upper() in ["CRITICAL", "HIGH"] else "badge-high"
                    status_tag = " [VERIFIED RESOLVED]" if is_converged else ""
                    with st.expander(f"[{item.severity.upper()}]{status_tag} Line {item.line_number}: {item.type}"):
                        st.markdown(f'<span class="badge {badge_style}">{item.severity.upper()}</span>', unsafe_allow_html=True)
                        st.markdown(f"**Vulnerability Type:** `{item.type}`")
                        st.write(f"**Root Cause Analysis:** {item.description}")
                        st.markdown("**Proof of Concept Exploit Vector:**")
                        st.code(item.poc_exploit, language="bash")
            else:
                st.success("Zero security issues reported.")

        with tab_unified_diff:
            st.markdown("##### **Git-Style Patch Comparison**")
            st.caption("Native git patch: Red lines (`-`) indicate vulnerable logic removed; Green lines (`+`) indicate security remediations.")
            diff_lines = list(difflib.unified_diff(
                target_code.splitlines(),
                current_code.splitlines(),
                fromfile="vulnerable_source.py",
                tofile="remediated_source.py",
                lineterm=""
            ))
            if diff_lines:
                st.code("\n".join(diff_lines), language="diff", line_numbers=True)
            else:
                st.info("No modifications were necessary.")

        with tab_download:
            st.markdown("##### **Download Remediated Code**")
            st.download_button(
                label="⬇️ Download Verified Python Script",
                data=current_code,
                file_name="remediated_" + target_filename,
                mime="text/x-python",
                use_container_width=True
            )
