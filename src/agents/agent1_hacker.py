import json
from pydantic import BaseModel
from typing import List
import ollama

MY_LOCAL_MODEL = "qwen2.5-coder:3b"

# Define single vulnerability schema (Data Contract)
class VulnerabilityItem(BaseModel):
    id: str
    type: str          # e.g., "SQL_INJECTION", "COMMAND_INJECTION", "PATH_TRAVERSAL", "HARDCODED_SECRET"
    line_number: int
    severity: str      # CRITICAL | HIGH | MEDIUM | LOW
    description: str   # Explanation of how the flaw occurs
    poc_exploit: str   # Theoretical payload or method demonstrating the vulnerability

# Top-level Security Scan Report schema
class SecurityScanReport(BaseModel):
    target_file: str
    vulnerabilities: List[VulnerabilityItem]

SYSTEM_PROMPT = """
You are an expert static application security testing (SAST) auditor.
Your job is to inspect Python source code and report ONLY genuine, actual security vulnerabilities.

--- ZERO-VULNERABILITY EXPECTATION ---
If the target code is compliant and contains NO security vulnerabilities, you MUST output an empty vulnerabilities array exactly like this:
{"target_file": "test_scratchpad.py", "vulnerabilities": []}

--- DO NOT FLAG COMPLIANT PATTERNS ---
1. DO NOT flag `os.getenv("KEY")` checks as hardcoded secrets.
2. DO NOT flag parameterized queries (`cursor.execute(query, (param,))`) as SQL injection.
3. DO NOT flag file access guarded by `is_relative_to(...)` as path traversal.
4. DO NOT flag `subprocess.run(["cmd", arg])` using list arrays as command injection.
5. DO NOT flag functions where `history_list` defaults to `None`.

--- Vulnerability Signatures to Flag ONLY IF PRESENT ---
1. HARDCODED SECRETS: Plaintext key or token strings assigned directly without environment lookups.
2. SQL INJECTION: Dynamic string formatting or f-strings inside SQL queries (`f"SELECT... {var}"`).
3. PATH TRAVERSAL: Unvalidated file reads via `open()` missing path containment checks.
4. OS COMMAND INJECTION: Direct usage of `os.system(...)` or `subprocess.run(..., shell=True)`.
5. WEAK CRYPTOGRAPHY: Active usage of `hashlib.md5()` or `hashlib.sha1()`.

CRITICAL REQUIREMENT:
Output MUST strictly conform to the requested JSON schema without markdown code blocks.
"""

def scan_code_for_vulnerabilities(file_name: str, code_contents: str) -> SecurityScanReport:
    """
    Agent 1 (The Auditor) scans target Python code and returns a validated 
    Pydantic SecurityScanReport containing detected issues.
    """
    user_prompt = f"Analyze every function in '{file_name}' and list ALL vulnerabilities found:\n\n{code_contents}"
    
    response = ollama.chat(
        model=MY_LOCAL_MODEL,
        options={
            "num_ctx": 4096,
            "temperature": 0.0,  # 0.0 enforces greedy decoding for deterministic output
            "seed": 42,          # Fixed seed eliminates inter-run variance
        },
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_prompt}
        ],
        format=SecurityScanReport.model_json_schema()
    )
    
    return SecurityScanReport.model_validate_json(response['message']['content'])

if __name__ == "__main__":
    target_path = "test_scratchpad.py"
    
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            target_code = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{target_path}'.")
        exit(1)
        
    print(f"🤖 Agent 1 (The Auditor) inspecting '{target_path}' using '{MY_LOCAL_MODEL}'...")
    
    try:
        report = scan_code_for_vulnerabilities(target_path, target_code)
        print("\n✅ Successfully generated structured Security Report:")
        print(report.model_dump_json(indent=2))
    except Exception as e:
        print(f"\n❌ Failed to generate report: {e}")