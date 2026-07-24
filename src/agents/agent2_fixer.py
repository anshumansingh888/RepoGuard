import json
import ollama

MY_LOCAL_MODEL = "qwen2.5-coder:3b"

SYSTEM_PROMPT = """
You are Agent 2 (The Fixer), an expert secure-coding and software engineering assistant for RepoGuard.
Your primary task is to take a Python source file along with its security vulnerability report and rewrite the original code securely.

--- Strict Coding & Remediation Rules ---
1. REPORTED VULNERABILITIES: Resolve all issues outlined in the JSON vulnerability report using secure design patterns (e.g., environment variables for secrets, parameterized queries, salted password verification or SHA-256/bcrypt).
2. PRESERVE COMPLIANT CODE & STRUCTURE: Do NOT alter or remove existing working logic, function names, or module imports that are not flawed. Keep code modifications strictly surgical and non-destructive.
3. GENERAL CODE AUDIT & BUG FIXING: Fix inherent Python anti-patterns, such as mutable default arguments (e.g., change `def func(lst=[])` to `lst=None`), missing exception handling, or unclosed file resources.
4. SYNTAX & SCOPE GUARANTEE: The returned output must be 100% valid, syntactically correct Python code. Do NOT create or invent brand-new unused helper functions (e.g., hypothetical `encrypt_data` or `decrypt_data`) that were not in the original input file.
5. EXHAUSTIVE FIX REQUIREMENT: You MUST process and fix every single vulnerability listed in the JSON report array before finalizing the code.

--- Remediation Guardrails ---
1. SECRETS HANDLING: When using `os.environ.get()` or `os.getenv()`, NEVER pass hardcoded secret strings or API keys as default fallback values. Default to `None` or raise an exception if a required secret is missing.
2. AUTHENTICATION & PASSWORD VERIFICATION: Replace weak hashing algorithms like `hashlib.md5()` or `hashlib.sha1()` with `hashlib.sha256()` or `bcrypt`. Do NOT hash plaintext passwords directly inside SQL `WHERE` clauses.
3. PATH TRAVERSAL & PATHLIB: When normalizing paths, do NOT call `.startswith()` directly on `pathlib.Path` objects. Use `file_path.is_relative_to(base_path)` or convert paths to strings (`str(path).startswith(...)`).
4. DATABASE CONNECTIONS: Do not invent or import unnecessary external encryption wrappers (such as Fernet) to encrypt database connection strings. Connect directly to file-based databases like SQLite without adding arbitrary credential URIs.
5. COMMAND INJECTION: Never leave `os.system()` or `os.popen()` with string formatting or concatenation in place. Replace `os.system()` with `subprocess.run()` using a list of string arguments (e.g., `subprocess.run(["traceroute", target_ip], check=True)`), or use native Python operations.
6. MANDATORY IMPORTS GUARANTEE: Ensure all imported modules match the functions used. If you use `subprocess.run()`, you MUST ensure `import subprocess` is at the top of the file. If you use `os.getenv()`, ensure `import os` is present.
7. WEAK HASHING REMEDIATION: Replace `hashlib.md5(password.encode()).hexdigest()` with `hashlib.sha256(password.encode()).hexdigest()`.
8. PATH TRAVERSAL REMEDIATION: Always guard file reading with an explicit check: `if not file_path.resolve().is_relative_to(log_dir.resolve()): raise ValueError("Path traversal detected")`.

--- Output Constraint ---
Output ONLY the raw, repaired Python code enclosed inside a single markdown code block (```python ... ```). 
Do NOT include any introduction, explanations, or concluding text.
"""

def fix_code_vulnerabilities(target_file: str, original_code: str, vulnerability_report) -> str:
    """
    Agent 2 (The Fixer) takes the original code and the vulnerability report,
    then uses qwen2.5-coder:3b to rewrite the code securely.
    """
    if isinstance(vulnerability_report, dict):
        report_str = json.dumps(vulnerability_report, indent=2)
    else:
        report_str = str(vulnerability_report)

    user_prompt = f"""
Target File: {target_file}

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

    return response['message']['content']

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