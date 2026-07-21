import os
import sys
import json

# Ensure Python can resolve the src module cleanly regardless of execution context
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.agent1_hacker import scan_code_for_vulnerabilities
from src.agents.agent2_fixer import fix_code_vulnerabilities

def run_repoguard_pipeline(target_path: str, output_path: str):
    print(f"🚀 [RepoGuard] Starting automated secure cleanup pipeline for: '{target_path}'")
    
    # 1. Read the target file that needs checking
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            target_code = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not find target file '{target_path}'.")
        return

    # 2. Execute Agent 1 (The Hacker)
    print("\n🔍 Running Agent 1 (The Hacker) to intercept flaws...")
    try:
        report_object = scan_code_for_vulnerabilities(target_path, target_code)
        print("✅ Agent 1 identified flaws and generated a structured report.")
    except Exception as e:
        print(f"❌ Pipeline stopped. Agent 1 failed: {e}")
        return

    # Extract the JSON text directly from the Pydantic object
    report_json_string = report_object.model_dump_json(indent=2)

    # 3. Execute Agent 2 (The Fixer) using the prepared JSON string
    print("\n🛠️ Handoff: Passing report directly to Agent 2 (The Fixer) for auto-repair...")
    fixed_code_output = fix_code_vulnerabilities(target_path, target_code, report_json_string)

    # 4. Strip LLM markdown wrapping lines to isolate clean Python code
    clean_code = fixed_code_output.strip()
    if clean_code.startswith("```python"):
        clean_code = clean_code.split("```python", 1)[1]
    if clean_code.endswith("```"):
        clean_code = clean_code.rsplit("```", 1)[0]
    clean_code = clean_code.strip()

    # 5. Automatically write the fixed code out to the file system
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(clean_code)
        
    print(f"\n=======================================================")
    print(f"✅ SUCCESS: Secure version generated at '{output_path}'!")
    print(f"👉 No manual editing required. Ready for review and 'git push'!")
    print(f"=======================================================")

if __name__ == "__main__":
    TARGET = "test_scratchpad.py"
    OUTPUT = "fixed_sample.py"
    
    run_repoguard_pipeline(TARGET, OUTPUT)