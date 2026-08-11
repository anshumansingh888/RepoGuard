import json
from src.agents.agent2_fixer import fix_code_vulnerabilities
from src.agents.agent1_hacker import scan_code_for_vulnerabilities

MAX_ITERATIONS = 3

def clean_markdown_fences(code: str) -> str:
    """Removes surrounding markdown code fences from LLM outputs."""
    clean_code = code.strip()
    if clean_code.startswith("```python"):
        clean_code = clean_code.split("```python", 1)[1]
    elif clean_code.startswith("```"):
        clean_code = clean_code.split("```", 1)[1]
    if clean_code.endswith("```"):
        clean_code = clean_code.rsplit("```", 1)[0]
    return clean_code.strip()

def run_repoguard_pipeline(target_path: str = "samples/vulnerable_sample.py", output_path: str = "fixed_sample.py"):
    print(f"🚀 [RepoGuard] Starting pipeline scan for: '{target_path}'")
    
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            current_code = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not locate '{target_path}'.")
        return

    # Iterative Remediation Loop
    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n-------------------------------------------------------")
        print(f"🔍 [Pass {iteration}/{MAX_ITERATIONS}] Running Agent 1 (The Auditor)...")
        
        try:
            report_object = scan_code_for_vulnerabilities(target_path, current_code)
        except Exception as e:
            print(f"❌ Agent 1 failed during scan: {e}")
            return

        # GATEKEEPER / VERIFICATION CHECK
        if not report_object.vulnerabilities:
            print("\n=======================================================")
            if iteration == 1:
                print("✅ SUCCESS: Target file is fully compliant! (Agent 2 skipped)")
            else:
                print(f"✅ REPAIR VERIFIED: Code passed audit on Iteration {iteration}!")
            
            print(f"   Writing secure code to '{output_path}'...")
            print("=======================================================")
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(current_code)
            return

        # IF VULNERABILITIES REMAIN: Pass to Agent 2
        print(f"⚠️  Agent 1 detected {len(report_object.vulnerabilities)} issue(s) on Pass {iteration}.")
        
        if iteration == MAX_ITERATIONS:
            print(f"🛑 Reached maximum iteration limit ({MAX_ITERATIONS}). Writing best-effort output...")
            break

        print(f"🛠️  Passing report to Agent 2 (The Fixer) for Pass {iteration}...")
        report_dict = report_object.model_dump()

        try:
            fixed_code = fix_code_vulnerabilities(target_path, current_code, report_dict)
        except Exception as e:
            print(f"❌ Agent 2 failed during remediation: {e}")
            return

        # Clean code and apply import post-processing
        clean_code = clean_markdown_fences(fixed_code)

        required_imports = []
        if "subprocess." in clean_code and "import subprocess" not in clean_code:
            required_imports.append("import subprocess")
        if "os." in clean_code and "import os" not in clean_code:
            required_imports.append("import os")
        if "Path(" in clean_code and "from pathlib import Path" not in clean_code:
            required_imports.append("from pathlib import Path")

        if required_imports:
            clean_code = "\n".join(required_imports) + "\n" + clean_code

        # Update current_code so the NEXT loop tests Agent 2's fix!
        current_code = clean_code

    # Write final state if loop maxed out
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(current_code)
    
    print(f"\n=======================================================")
    print(f"⚠️  PIPELINE FINISHED (Max Attempts Reached): Saved output to '{output_path}'")
    print(f"=======================================================")

if __name__ == "__main__":
    run_repoguard_pipeline("samples/vulnerable_sample.py", "fixed_sample.py")