import sqlite3
import hashlib
import os

# ==========================================
# DATABASE SETUP (Helper to seed test data)
# ==========================================
def setup_test_db():
    """Creates an in-memory SQLite database and registers a test user."""
    conn = sqlite3.connect("test_users.db")
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            salt BLOB,
            password_hash TEXT
        )
    """)

    # Setup a mock user: "alice" with password "SuperSecret123!"
    test_username = "alice"
    test_password = "SuperSecret123!"
    
    # Registration logic: Generate salt ONCE and store it
    user_salt = os.urandom(16)
    user_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        test_password.encode('utf-8'), 
        user_salt, 
        100000
    ).hex()

    cursor.execute(
        "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
        (test_username, user_salt, user_hash)
    )
    conn.commit()
    conn.close()
    
    print("Database Initialized")
    print(f" Registered User : '{test_username}'")
    print(f" Saved Salt (hex): {user_salt.hex()}")
    print(f" Saved Hash      : {user_hash}\n" + "="*60 + "\n")


# ==========================================
# 1. AGENT 2 GENERATED CODE (BROKEN)
# ==========================================
def agent2_login_user(username, password):
    print("Executing Agent 2 Code (New salt generated per login attempt)...")
    
    # Agent 2's line: Generates a NEW salt on every login call
    salt = os.urandom(16)
    hashed_pw = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

    print(f" Generated Salt  : {salt.hex()}  <-- NEW SALT GENERATED!")
    print(f" Computed Hash   : {hashed_pw}")

    conn = sqlite3.connect("test_users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? AND password_hash = ?"
    cursor.execute(query, (username, hashed_pw))
    result = cursor.fetchone()
    conn.close()
    
    return result


# ==========================================
# 2. FIXED SECURE LOGIC (FUNCTIONAL)
# ==========================================
def fixed_login_user(username, password):
    print("Executing Fixed Logic (Retrieves salt from DB first)...")
    
    conn = sqlite3.connect("test_users.db")
    cursor = conn.cursor()

    # Step 1: Fetch user's stored salt first
    cursor.execute("SELECT salt, password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if not row:
        print(" User not found in database!")
        conn.close()
        return None

    stored_salt, stored_hash = row
    print(f" Retrieved Salt  : {stored_salt.hex()}  <-- FETCHED FROM DB")
    print(f" Stored Hash     : {stored_hash}")

    # Step 2: Hash incoming password using the RETRIEVED salt
    computed_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        stored_salt, 
        100000
    ).hex()

    print(f" Computed Hash   : {computed_hash}")

    # Step 3: Compare
    if computed_hash == stored_hash:
        print(" Password matches!")
        conn.close()
        return (username, stored_salt, stored_hash)
    
    print(" Invalid password!")
    conn.close()
    return None


# ==========================================
# RUN TEST SUITE
# ==========================================
if __name__ == "__main__":
    os.environ["SECRET_KEY"] = "mock_secret_key"
    setup_test_db()

    target_user = "alice"
    correct_password = "SuperSecret123!"

    print(f"--- TEST 1: AGENT 2 GENERATED LOGIC ---")
    print(f"Attempting login for '{target_user}' with correct password...\n")
    res1 = agent2_login_user(target_user, correct_password)
    
    if res1 is None:
        print("\n RESULT: LOGIN FAILED (Expected failure due to random salt mismatch)\n")
    else:
        print("\n RESULT: LOGIN SUCCESS\n")

    print("="*60 + "\n")

    print(f"--- TEST 2: FIXED SECURE LOGIC ---")
    print(f"Attempting login for '{target_user}' with correct password...\n")
    res2 = fixed_login_user(target_user, correct_password)
    
    if res2 is not None:
        print("\n RESULT: LOGIN SUCCESSFUL!\n")
    else:
        print("\n RESULT: LOGIN FAILED\n")

    # Clean up test database file
    if os.path.exists("test_users.db"):
        os.remove("test_users.db")