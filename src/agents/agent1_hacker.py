import json
from pydantic import BaseModel
from typing import List, Optional
import ollama
from src.config import settings

MY_LOCAL_MODEL = settings.model_name

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

SYSTEM_PROMPT = """You are an expert static application security testing (SAST) auditor for RepoGuard.
Your task is to inspect Python source code for genuine security vulnerabilities and output structured findings.

--- METHODOLOGY: TAINT ANALYSIS ---
Evaluate code by tracing untrusted user inputs (Sources) to execution points (Sinks).
A vulnerability exists ONLY if untrusted data reaches a sensitive sink without adequate sanitization, parametrization, or authorization controls.

--- STRICT GROUND TRUTH EXCLUSION RULES (NEVER FLAG THESE) ---
1. DO NOT flag `os.getenv("KEY")` or `os.environ.get("KEY")` as hardcoded secrets.
2. DO NOT flag parameterized SQL queries using placeholders (e.g. `cursor.execute(query, (param,))`).
3. DO NOT flag path containment checks using `is_relative_to(...)` OR `file_path.startswith(base_path)` as path traversal.
4. DO NOT flag `subprocess.run(["cmd", arg])` using list arrays (without `shell=True`) as command injection.
5. DO NOT flag `hashlib.pbkdf2_hmac(...)` or `hashlib.sha256()` as weak cryptography.
6. DO NOT flag functions where lists are instantiated inside the function body (e.g., `history_list = []`).
7. DO NOT flag secure code with hypothetical claims like "needs extra sanitization" or "potential risks".
8. DO NOT flag code based on words found in comments or docstrings (e.g., if a docstring mentions "SQL INJECTION" or "PATH TRAVERSAL"). Evaluate ONLY the executable Python logic.

--- ZERO-VULNERABILITY EXPECTATION ---
If the target file contains NO genuine security vulnerabilities, you MUST return an empty array for `vulnerabilities`:
{"target_file": "<TARGET_FILE>", "vulnerabilities": []}

--- TOKEN COMPRESSION & OUTPUT REQUIREMENTS ---
1. You MUST strictly output valid JSON conforming to the requested schema without markdown code blocks.
2. ULTRA-CONCISE STRINGS: Keep `description` under 10 words (e.g., "SQL injection via string formatting query"). Keep `poc_exploit` under 25 characters (e.g., "' OR 1=1--")."""

def scan_code_for_vulnerabilities(
    file_name: str, 
    code_contents: str, 
    model: Optional[str] = None
) -> SecurityScanReport:
    """
    Agent 1 (The Auditor) scans target Python code and returns a validated 
    Pydantic SecurityScanReport containing detected issues using the configured model.
    """
    target_model = model or settings.model_name
    
    # Softened prompt to allow the model to return empty findings when appropriate
    user_prompt = (
        f"Inspect '{file_name}'. If the code follows secure coding standards and contains no security flaws, "
        f"return an empty array for vulnerabilities.\n\nSource Code:\n{code_contents}"
    )
    
    response = ollama.chat(
        model=target_model,
        keep_alive=settings.keep_alive,
        options={
            "num_ctx": settings.num_ctx,
            "temperature": settings.temperature,  # Enforces greedy decoding for deterministic output
            "seed": settings.seed,                # Fixed seed eliminates inter-run variance
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
