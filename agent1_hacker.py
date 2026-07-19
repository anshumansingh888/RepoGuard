import json
from pydantic import BaseModel
from typing import List
import ollama

# TODO: Change this to match the exact model name you pulled in Ollama!
MY_LOCAL_MODEL = "llama3.2:3b" 

# Define what a single vulnerability structure looks like (Our Team Data Contract)
class VulnerabilityItem(BaseModel):
    id: str
    type: str          # e.g., "SQL_INJECTION", "HARDCODED_SECRET"
    line_number: int
    severity: str      # CRITICAL | HIGH | MEDIUM | LOW
    description: str   # Explanation of how the flaw occurs
    poc_exploit: str   # Example payload or method to break it

# Define the top-level structure matching your team's Data Contract
class SecurityScanReport(BaseModel):
    target_file: str
    vulnerabilities: List[VulnerabilityItem]

SYSTEM_PROMPT = """
You are an elite, highly aggressive Penetration Tester and Application Security Auditor. 
Your job is to mercilessly dissect the provided source code and find security vulnerabilities.

Look specifically for:
1. Hardcoded developer credentials, tokens, or API keys.
2. Unvalidated inputs leading to SQL Injection or Command Injection.
3. Weak cryptography or insecure hashing algorithms.

CRITICAL: You must return your findings matching the requested JSON schema EXACTLY. 
Do not include any introductory text, pleasantries, or markdown formatting outside of the JSON structure.
"""

def scan_code_for_vulnerabilities(file_name: str, code_contents: str) -> SecurityScanReport:
    user_prompt = f"Analyze the following file named '{file_name}' and generate the security report:\n\n{code_contents}"
    
    # Send data to your local Ollama engine
    response = ollama.chat(
        model=MY_LOCAL_MODEL,
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_prompt}
        ],
        format=SecurityScanReport.model_json_schema()
    )
    
    # Validate and turn the raw text back into a structured object
    return SecurityScanReport.model_validate_json(response['message']['content'])

if __name__ == "__main__":
    target_path = "vulnerable_sample.py"
    
    # 1. Read our target practice file
    try:
        with open(target_path, "r") as f:
            target_code = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find '{target_path}'.")
        exit(1)
        
    print(f"🤖 Agent 1 (The Hacker) is attacking '{target_path}' using local model '{MY_LOCAL_MODEL}'...")
    
    # 2. Run the agent attack loop
    try:
        report = scan_code_for_vulnerabilities(target_path, target_code)
        print("\n✅ Successfully generated data-compliant report JSON:")
        print(report.model_dump_json(indent=2))
    except Exception as e:
        print(f"\n❌ Error parsing model response: {e}")