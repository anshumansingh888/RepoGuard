"""
RepoGuard CLI Entry Point.
Executes the autonomous SAST audit and remediation pipeline via RepoGuardPipeline.
"""
import sys
from src.config import settings
from src.core.pipeline import RepoGuardPipeline, PipelineResult

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Backward-compatibility aliases
MAX_ITERATIONS = settings.max_iterations
clean_markdown_fences = RepoGuardPipeline.clean_markdown_fences


def run_repoguard_pipeline(
    target_path: str = "samples/vulnerable_sample.py", 
    output_path: str = "fixed_sample.py",
    max_iterations: int = settings.max_iterations,
    verify_fix: bool = True
) -> PipelineResult:
    """Executes the RepoGuard pipeline from the CLI and writes the secure output."""
    print(f"🚀 [RepoGuard] Starting pipeline scan for: '{target_path}'")
    
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Could not locate '{target_path}'.")
        sys.exit(1)

    pipeline = RepoGuardPipeline(max_iterations=max_iterations)

    def cli_progress_handler(event: dict):
        kind = event.get("event")
        pass_num = event.get("pass_num", 1)
        
        if kind == "audit_start":
            print(f"\n-------------------------------------------------------")
            print(f"🔍 [Pass {pass_num}/{max_iterations}] Running Agent 1 (The Auditor)...")
        elif kind == "audit_complete":
            count = event.get("vulnerabilities", 0)
            if count > 0:
                print(f"⚠️  Agent 1 detected {count} issue(s) on Pass {pass_num}.")
        elif kind == "fast_path_exit":
            print("\n=======================================================")
            print("✅ SUCCESS: Target file is fully compliant! (Agent 2 skipped)")
            print(f"   Writing secure code to '{output_path}'...")
            print("=======================================================")
        elif kind == "convergence_exit":
            print("\n=======================================================")
            if event.get("fast_mode"):
                print("⚡ FAST MODE: Remediation applied & verified valid by AST Gatekeeper! (Re-audit skipped)")
            else:
                print(f"✅ REPAIR VERIFIED: Code passed audit on Iteration {pass_num}!")
            print(f"   Writing secure code to '{output_path}'...")
            print("=======================================================")
        elif kind == "fix_start":
            print(f"🛠️  Passing report to Agent 2 (The Fixer) for Pass {pass_num}...")
        elif kind == "syntax_error":
            print(f"⚠️  [AST Gatekeeper Warning] {event.get('error')}")
        elif kind == "max_iterations_reached":
            print(f"🛑 Reached maximum iteration limit ({max_iterations}). Writing best-effort output...")

    result = pipeline.run(target_path, source_code, on_step=cli_progress_handler, verify_fix=verify_fix)

    # Persist the output code
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.final_code)

    if not result.converged and result.iterations_used >= max_iterations:
        print(f"\n=======================================================")
        print(f"⚠️  PIPELINE FINISHED (Max Attempts Reached): Saved output to '{output_path}'")
        print(f"=======================================================")

    return result


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "samples/vulnerable_sample.py"
    output = sys.argv[2] if len(sys.argv) > 2 else "fixed_sample.py"
    run_repoguard_pipeline(target, output)


if __name__ == "__main__":
    main()
