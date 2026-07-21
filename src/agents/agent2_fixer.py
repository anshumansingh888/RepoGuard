import json
import ollama

def fix_code_vulnerabilities(target_file: str, original_code: str, vulnerability_report: dict) -> str:
    """
    Agent 2 (The Fixer) takes the original code and the JSON vulnerability report,
    then asks llama3.2:3b to rewrite the code securely based on a strict blueprint.
    """
    
    prompt = f"""
    You are Agent 2 (The Fixer), an expert secure-coding and software engineering assistant for RepoGuard.
    Your task is to take a Python file, fix the reported vulnerabilities, and completely audit the entire file for logical flaws, bugs, or anti-patterns (such as mutable default arguments). Return a clean, 100% syntactically correct version.
    
    Target File: {target_file}
    
    --- Original Code ---
    {original_code}
    
    --- Vulnerability Report (JSON) ---
    {json.dumps(vulnerability_report, indent=2)}
    
    --- Mandatory Reference Blueprint Layout ---
    When rewriting authentication or database tasks, you MUST copy the exact logic patterns shown here:
    ```python
    # (Keep your existing security blueprint code block here...)
    ```

    --- Strict Coding & Remediation Rules ---
    1. REPORTED VULNERABILITIES: Resolve all issues outlined in the JSON vulnerability report using the secure design patterns from the blueprint.
    2. GENERAL CODE AUDIT & BUG FIXING: You must carefully read every single function in the file. Fix any inherent logic bugs, runtime errors, or Python anti-patterns. 
    3. MUTABLE DEFAULT ARGUMENTS: If any function uses a mutable default argument like `current_list=[]` or `data={{}}`, you MUST rewrite it using the `argument=None` pattern to prevent side effects across execution states.
    4. PRESERVE COMPLIANT CODE: Maintain unrelated functional blocks, but ensure they are clean, modern, and free of bugs.
    
    --- Output Constraint ---
    Output ONLY the raw, completely repaired Python code inside a single standard markdown code block. Do not write any greetings, explanations, or notes.
    """

    print(f"🛠️ Agent 2 (The Fixer) is repairing '{target_file}' using llama3.2:3b...")
    
    response = ollama.generate(
        model="llama3.2:3b",
        prompt=prompt
    )
    
    return response['response']

if __name__ == "__main__":
    target_path = "vulnerable_sample.py"
    
    # 1. Read the target file that needs fixing
    try:
        with open(target_path, "r") as f:
            target_code = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find '{target_path}'.")
        exit(1)
        
    # 2. Simulate getting the report from Agent 1
    sample_agent1_report = {
        "vulnerabilities": [
            {
                "type": "Hardcoded Secret",
                "line": 5,
                "description": "Exposed API key or credential found in plaintext."
            },
            {
                "type": "Weak Cryptography / Missing Salt",
                "line": 8,
                "description": "Plain SHA-256 password hashing without salt or iteration parameters."
            }
        ]
    }
    
    # 3. Run the Fixer Agent
    fixed_code_output = fix_code_vulnerabilities(target_path, target_code, sample_agent1_report)
    
    # 4. Clean up LLM markdown blocks if present before saving
    clean_code = fixed_code_output.strip()
    if clean_code.startswith("```python"):
        clean_code = clean_code.split("```python", 1)[1]
    if clean_code.endswith("```"):
        clean_code = clean_code.rsplit("```", 1)[0]
    clean_code = clean_code.strip()
    
    # 5. Save the secured code to fixed_sample.py
    output_path = "fixed_sample.py"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(clean_code)
        
    print(f"✅ Successfully generated secure code! Saved to '{output_path}'.")