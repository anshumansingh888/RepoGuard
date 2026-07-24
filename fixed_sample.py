import os
import sqlite3
import hashlib
from pathlib import Path
import subprocess

# 1. Environment-based secret loading without hardcoded fallbacks
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not configured.")

def hash_user_password(password: str) -> str:
    """Hashes password securely using SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def get_user_record(username: str):
    """Safely retrieves user profile using parameterized SQL queries."""
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # Parameterized query prevents SQL Injection
    query = "SELECT id, username, email FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchone()

def read_app_log(log_filename: str) -> str:
    """Safely reads log file within allowed directory using pathlib resolution."""
    log_dir = Path("./app_logs").resolve()
    file_path = (log_dir / log_filename).resolve()
    
    # Prevents Path Traversal directory escape
    if not file_path.is_relative_to(log_dir):
        raise ValueError("Access denied: Path traversal attempt detected.")
        
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def run_system_diagnostic(target_ip: str) -> None:
    """Safely executes network ping/traceroute using subprocess list arguments."""
    command = ["traceroute", target_ip]
    try:
        # Prevents Command Injection by avoiding shell execution
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Diagnostic failed for host {target_ip}: {e}")

def collect_system_metrics(metric_name: str, history_list=None) -> list:
    """Uses immutable default argument and explicit exception handling."""
    if history_list is None:
        history_list = []
        
    try:
        history_list.append(metric_name)
        return history_list
    except Exception as e:
        print(f"Error collecting metric '{metric_name}': {e}")
        return history_list