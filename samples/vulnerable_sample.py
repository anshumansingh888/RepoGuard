import os
import sqlite3
import hashlib
import subprocess

# 1. HARDCODED SENSITIVE SECRET / API TOKEN
# Insecure static assignment instead of environment variable loading
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