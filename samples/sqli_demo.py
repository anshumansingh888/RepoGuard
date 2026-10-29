import sqlite3
import hashlib

# Vulnerability 1: Hardcoded credentials
DB_ADMIN_PASSWORD = "SuperSecretAdminPassword2026!"

def store_credentials(username: str, plain_pass: str):
    """
    Vulnerability 2: Weak unsalted MD5 password hashing.
    Single pass MD5 can be broken instantly using rainbow tables.
    """
    password_hash = hashlib.md5(plain_pass.encode()).hexdigest()
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password_hash}')")
    conn.commit()

def authenticate_user(username: str, search_query: str):
    """
    Vulnerability 3: Direct string concatenation SQL Injection (SQLi).
    Attacker can supply: ' OR '1'='1' -- to bypass authentication.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    sql_statement = f"SELECT id, username, role FROM users WHERE username = '{username}' AND role = '{search_query}'"
    cursor.execute(sql_statement)
    return cursor.fetchone()
