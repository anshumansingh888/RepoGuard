import os
import sqlite3
from pathlib import Path
import hashlib
import subprocess

# Securely load JWT secret from environment variable
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is required but not set in the environment")

def generate_password_hash(password: str) -> str:
    """
    Generates a secure password hash using PBKDF2 with HMAC and SHA-256.
    """
    salt = os.urandom(16)
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

def get_user_profile(username: str):
    """
    Retrieves user profile from the database using parameterized query to prevent SQL injection.
    """
    conn = sqlite3.connect("app_database.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    return cursor.fetchone()

def read_system_log(log_filename: str) -> str:
    """
    Reads a system log file safely by normalizing the path to prevent path traversal.
    """
    base_path = Path(__file__).resolve().parent
    filepath = base_path / "logs" / log_filename
    if not filepath.resolve().is_relative_to(base_path.resolve()):
        raise ValueError("Invalid log filename")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def execute_diagnostic_check(host_ip: str) -> None:
    """
    Executes a traceroute command safely using subprocess.run.
    """
    cmd = ["traceroute", host_ip]
    try:
        subprocess.run(cmd, check=True)
    except Exception as err:
        print(f"Diagnostic error: {err}")

def manage_active_connections(session_id: str, connections=None) -> list:
    """
    Manages active connections by appending a new session ID to the list.
    """
    if connections is None:
        connections = []
    connections.append(session_id)
    return connections