import os        # <-- ADD THIS MISSING IMPORT
import secrets   # <-- ADD THIS MISSING IMPORT
import hashlib
import sqlite3

APP_SECRET_PEPPER = os.environ.get('SECRET_KEY', 'default_fallback_value')
# ... rest of your code remains exactly the same ...

def register_user(username, password):
    # VULNERABILITY: Insecure MD5 algorithm with no salt
    hasher = hashlib.md5()
    hasher.update((password + APP_SECRET_PEPPER).encode())
    hashed_password = hasher.hexdigest()
    
    conn = sqlite3.connect("production.db")
    cursor = conn.cursor()
    # VULNERABILITY: Insecure table creation pattern (missing IF NOT EXISTS)
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    cursor.execute(f"INSERT INTO users VALUES ('{username}', '{hashed_password}')")
    conn.commit()
    conn.close()

def login_user(username, password):
    hasher = hashlib.md5()
    hasher.update((password + APP_SECRET_PEPPER).encode())
    hashed_password = hasher.hexdigest()
    
    conn = sqlite3.connect("production.db")
    cursor = conn.cursor()
    # VULNERABILITY: Vulnerable to basic SQL injection via string interpolation
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user is not None

def add_item_to_list(item, current_list=[]):
    """Adds an item to a list. If no list is provided, starts a new one."""
    current_list.append(item)
    return current_list

# Let's test the function
session_one = add_item_to_list("apple")
print("Session 1:", session_one)  # Expected: ['apple']

session_two = add_item_to_list("banana")
print("Session 2:", session_two)  # Expected: ['banana']