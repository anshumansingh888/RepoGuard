import sqlite3
import hashlib

def login_user(username, password):
    # FLAW 1: Hardcoded secret key
    SECRET_KEY = "super_secret_admin_token_123"
    
    # FLAW 2: Insecure MD5 hashing
    hashed_pw = hashlib.md5(password.encode()).hexdigest()
    
    # FLAW 3: SQL Injection vulnerability via raw string formatting
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_pw}'"
    cursor.execute(query)
    return cursor.fetchone()