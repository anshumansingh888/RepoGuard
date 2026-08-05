import json
import re
import ollama

MY_LOCAL_MODEL = "qwen2.5-coder:7b"

SYSTEM_PROMPT = """You are Agent 2 (The Fixer), an expert secure-coding and software engineering assistant for RepoGuard.
Your primary task is to take a Python source file along with its security vulnerability report and rewrite the original code securely.

--- Strict Coding & Remediation Rules ---
1. REPORTED VULNERABILITIES: Resolve all issues outlined in the JSON vulnerability report using secure design patterns (e.g., environment variables for secrets, parameterized queries, and salted, slow password hashing).
2. PRESERVE COMPLIANT CODE & STRUCTURE: Do NOT alter or remove existing working logic, function names, or module imports that are not flawed. Keep code modifications strictly surgical and non-destructive.
3. GENERAL CODE AUDIT & BUG FIXING: Fix inherent Python anti-patterns, such as mutable default arguments (e.g., change `def func(lst=[])` to `lst=None`), missing exception handling, or unclosed file resources.
4. SYNTAX & SCOPE GUARANTEE: The returned output must be 100% valid, syntactically correct Python code. Do NOT create or invent brand-new unused helper functions that were not in the original input file.
5. EXHAUSTIVE FIX REQUIREMENT: You MUST process and fix every single vulnerability listed in the JSON report array before finalizing the code.
6. SANITIZE DOCSTRINGS & COMMENTS: You MUST rewrite or remove outdated docstrings and inline comments that mention legacy vulnerabilities (e.g., replace "Uses SHA-1" with "Uses PBKDF2-HMAC-SHA256", or "SQL Injection" with "Parameterized SQL").

--- Remediation Guardrails & Security Patterns ---
1. SECRETS HANDLING: When using `os.environ.get()` or `os.getenv()`, NEVER pass hardcoded secret strings or API keys as default fallback values. Default to `None` or raise an exception if a required secret is missing.
2. AUTHENTICATION & PASSWORD STORAGE: NEVER use or advocate plain/unsalted hashing (such as MD5, SHA-1, or plain SHA-256) for password/credential storage. You MUST use `hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()` — this is the ONLY sanctioned algorithm; it is stdlib and requires no new dependency. Do NOT use `bcrypt` or `argon2`, since those packages are not installed in this project. Specifically:
   - Never generate a new random salt (e.g., `os.urandom()`) inside a login or credential verification function.
   - In login functions, fetch the user's existing salt/hash from the database first, then compute the hash using that retrieved salt.
   - Use `os.urandom()` strictly during account creation, registration, or password setup logic.
3. PATH TRAVERSAL & PATHLIB: When normalizing paths, use idiomatic path resolution and validation. If using `Path`, ensure `from pathlib import Path` is explicitly imported at the top of the file. Use `file_path.resolve().is_relative_to(base_path.resolve())` or convert paths to strings (`str(path).startswith(...)`).
4. DATABASE CONNECTIONS: Do not invent or import unnecessary external encryption wrappers (such as Fernet) to encrypt database connection strings. Connect directly to file-based databases like SQLite without adding arbitrary credential URIs.
5. COMMAND INJECTION: Never leave `os.system()` or `os.popen()` with string formatting or concatenation in place. Replace with `subprocess.run()` using a list of string arguments, or use native Python operations.
6. MANDATORY IMPORTS GUARANTEE: Ensure all imported modules match the functions used. If you use a module or class (e.g. `subprocess`, `os`, `hashlib`, `from pathlib import Path`), you MUST ensure the corresponding `import` statement is at the top of the file.
7. IDIOMATIC ARCHITECTURE: Apply security patterns that are idiomatic to the target file's existing architecture. Adapt to existing variable names, function signatures, and code organization.

--- Output Constraint ---
Output ONLY the raw, repaired Python code enclosed inside a single markdown code block (```python ... ```). 
Do NOT include any introduction, explanations, or concluding text.
"""

def fix_code_vulnerabilities(target_file: str, original_code: str, vulnerability_report) -> str:
    """
    Agent 2 (The Fixer) takes the original code and the vulnerability report,
    then uses qwen2.5-coder:7b to rewrite the code securely.
    """
    if isinstance(vulnerability_report, dict):
        report_str = json.dumps(vulnerability_report, indent=2)
    else:
        report_str = str(vulnerability_report)

    user_prompt = f"""Target File: {target_file}

--- Original Code ---
{original_code}

--- Vulnerability Report (JSON) ---
{report_str}

Please generate the secure, refactored Python code following all remediation rules.
"""

    response = ollama.chat(
        model=MY_LOCAL_MODEL,
        options={
            "num_ctx": 4096,
            "temperature": 0.0,  # Forces deterministic code output
            "seed": 42,
        },
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    raw_content = response['message']['content']
    
    # Extract Python code block using regex
    code_block_match = re.search(r"```python\s*(.*?)\s*```", raw_content, re.DOTALL | re.IGNORECASE)
    if code_block_match:
        return code_block_match.group(1).strip()
    
    # Fallback to cleaning if no exact match or standard fence is used
    code_block_match_generic = re.search(r"```\s*(.*?)\s*```", raw_content, re.DOTALL)
    if code_block_match_generic:
        return code_block_match_generic.group(1).strip()
        
    return raw_content.strip()

if __name__ == "__main__":
    target_path = "samples/vulnerable_sample.py"
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            target_code = f.read()
        dummy_report = {"vulnerabilities": []}
        fixed_output = fix_code_vulnerabilities(target_path, target_code, dummy_report)
        print("✅ Agent 2 Output Test Passed:")
        print(fixed_output[:200] + "...")
    except Exception as e:
        print(f"❌ Agent 2 Test Error: {e}")