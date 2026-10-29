import os
from pathlib import Path
import sqlite3
import hashlib
import subprocess

# 1. COMPLIANT SECRET HANDLING: Reads from environment without hardcoded fallback
API_KEY = os.getenv("APP_ENCRYPTION_KEY")

def hash_user_password(password: str, salt: bytes) -> str:
    """
    2. COMPLIANT CRYPTOGRAPHY:
    Uses standard library PBKDF2-HMAC-SHA256 with user salt and high iteration count.
    """
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000).hex()

def fetch_user_by_role(role_name: str):
    """
    3. COMPLIANT DATABASE QUERY:
    Uses parameterized query placeholders (?) to prevent SQL injection.
    """
    conn = sqlite3.connect("production.db")
    cursor = conn.cursor()
    query = "SELECT id, username, email FROM accounts WHERE role = ?"
    cursor.execute(query, (role_name,))
    return cursor.fetchall()

def load_user_document(file_name: str) -> str:
    """
    4. COMPLIANT FILE PATH RESOLUTION:
    Enforces boundary check with is_relative_to() to prevent path traversal attacks.
    """
    base_dir = Path("/var/data/uploads").resolve()
    target_file = (base_dir / file_name).resolve()
    
    if not target_file.is_relative_to(base_dir):
        raise ValueError("Security violation: Path traversal attempt detected.")
        
    with open(target_file, "r", encoding="utf-8") as f:
        return f.read()

def run_diagnostic_ping(target_host: str) -> None:
    """
    5. COMPLIANT OS COMMAND EXECUTION:
    Uses list-based argument arrays without shell=True to eliminate command injection.
    """
    command = ["ping", "-c", "1", target_host]
    try:
        subprocess.run(command, check=True)
    except subprocess.SubprocessError as exc:
        print(f"Diagnostic error: {exc}")

def append_audit_event(event_name: str, audit_trail=None) -> list:
    """
    6. COMPLIANT STATE HANDLING:
    Avoids mutable default argument by initializing list inside the function scope.
    """
    if audit_trail is None:
        audit_trail = []
    audit_trail.append(event_name)
    return audit_trail
