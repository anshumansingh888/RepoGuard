import json
from src.agents.agent1_hacker import scan_code_for_vulnerabilities
from src.agents.agent2_fixer import fix_code_vulnerabilities

def run_repoguard_pipeline(target_path: str, output_path: str):
    print(f"🚀 [RepoGuard] Starting pipeline scan for: '{target_path}'")
    
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            target_code = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not locate '{target_path}'.")
        return

    # Agent 1 Audit Pass
    print("\n🔍 Running Agent 1 (The Auditor)...")
    try:
        report_object = scan_code_for_vulnerabilities(target_path, target_code)
    except Exception as e:
        print(f"❌ Agent 1 failed during scan: {e}")
        return

    # Gatekeeper Check: If zero vulnerabilities, copy original clean code to output
    if not report_object.vulnerabilities:
        print("\n=======================================================")
        print("✅ SUCCESS: No security vulnerabilities or flaws found!")
        print("   Agent 2 skipped (file is compliant).")
        print(f"   Writing clean target code directly to '{output_path}'...")
        print("=======================================================")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(target_code)
        return

    # Agent 2 Fix Pass (Triggered only if issues exist)
    print(f"\n⚠️  Agent 1 detected {len(report_object.vulnerabilities)} issue(s). Passing to Agent 2...")
    report_dict = report_object.model_dump()

    try:
        fixed_code = fix_code_vulnerabilities(target_path, target_code, report_dict)
    except Exception as e:
        print(f"❌ Agent 2 failed during remediation: {e}")
        return

    # Clean markdown fences if present
    clean_code = fixed_code.strip()
    if clean_code.startswith("```python"):
        clean_code = clean_code.split("```python", 1)[1]
    elif clean_code.startswith("```"):
        clean_code = clean_code.split("```", 1)[1]
    if clean_code.endswith("```"):
        clean_code = clean_code.rsplit("```", 1)[0]
    
    clean_code = clean_code.strip()

    # Post-processing: Add missing imports if used in refactored code
    if "subprocess.run(" in clean_code and "import subprocess" not in clean_code:
        clean_code = "import subprocess\n" + clean_code

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(clean_code)

    print(f"\n=======================================================")
    print(f"✅ REPAIR COMPLETE: Secure output generated at '{output_path}'")
    print(f"=======================================================")

if __name__ == "__main__":
    run_repoguard_pipeline("vulnerable_sample.py", "fixed_sample.py")