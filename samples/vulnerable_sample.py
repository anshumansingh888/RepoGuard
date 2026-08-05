import os
import sqlite3
import hashlib
import subprocess

# 1. HARDCODED SECRET
# Sensitive access token exposed directly in source code
STRIPE_SECRET_KEY = "sk_test_placeholder_key_for_testing"

def hash_user_password(password: str) -> str:
    """
    2. WEAK CRYPTOGRAPHY:
    Uses SHA-1 to hash user passwords, which is cryptographically broken and vulnerable to collisions.
    """
    return hashlib.sha1(password.encode("utf-8")).hexdigest()

def search_user_by_email(user_email: str):
    """
    3. SQL INJECTION:
    Uses f-strings to construct raw SQL queries dynamically instead of parameterized queries.
    """
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    query = f"SELECT id, username, email FROM users WHERE email = '{user_email}'"
    cursor.execute(query)
    return cursor.fetchone()

def download_user_document(document_name: str) -> str:
    """
    4. PATH TRAVERSAL:
    Opens files directly from user input without resolving absolute paths 
    or verifying boundary constraints using pathlib/is_relative_to.
    """
    file_path = f"./documents/{document_name}"
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def run_network_ping(host_address: str) -> None:
    """
    5. OS COMMAND INJECTION:
    Executes subprocess with shell=True and dynamic string formatting.
    """
    command = f"ping -c 2 {host_address}"
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"Network error: {e}")

def track_user_session(event_name: str, session_logs=[]) -> list:
    """
    6. ANTI-PATTERN (Mutable Default Argument):
    Uses a mutable default list (`session_logs=[]`), which retains state across function calls.
    """
    session_logs.append(event_name)
    return session_logs