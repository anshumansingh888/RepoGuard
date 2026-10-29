"""
Unified Pipeline Orchestrator for RepoGuard.
Coordinates the iterative dual-agent SAST audit and remediation loop,
enforcing gatekeeper convergence, AST syntax validation, and deterministic post-processing.
"""
import re
from typing import List, Dict, Any, Optional, Callable
from pydantic import BaseModel, Field

from src.config import settings
from src.core.validator import validate_python_syntax
from src.agents.agent1_hacker import scan_code_for_vulnerabilities, SecurityScanReport
from src.agents.agent2_fixer import fix_code_vulnerabilities


class PipelineResult(BaseModel):
    """Encapsulates the complete result of a RepoGuard pipeline execution."""
    original_code: str
    final_code: str
    converged: bool
    iterations_used: int
    initial_report: SecurityScanReport
    final_report: SecurityScanReport
    audit_history: List[Dict[str, Any]] = Field(default_factory=list)
    syntax_errors: List[str] = Field(default_factory=list)


class RepoGuardPipeline:
    """Supervisory pipeline orchestrator implementing the closed-loop gatekeeper."""

    def __init__(self, max_iterations: Optional[int] = None):
        self.max_iterations = max_iterations if max_iterations is not None else settings.max_iterations

    @staticmethod
    def clean_markdown_fences(code: str) -> str:
        """Removes surrounding markdown code fences (```python ... ```) from LLM output."""
        clean = code.strip()
        clean = re.sub(r"^```(?:python)?\s*\n?", "", clean, flags=re.MULTILINE)
        clean = re.sub(r"\n?```\s*$", "", clean, flags=re.MULTILINE)
        return clean.strip()

    @staticmethod
    def inject_missing_imports(code: str) -> str:
        """
        Deterministically verifies and injects essential standard library imports
        if their corresponding symbols were introduced by remediation.
        """
        required_imports: List[str] = []

        if "subprocess." in code and "import subprocess" not in code:
            required_imports.append("import subprocess")
        if "os." in code and "import os" not in code:
            required_imports.append("import os")
        if "Path(" in code and "from pathlib import Path" not in code and "import pathlib" not in code:
            required_imports.append("from pathlib import Path")
        if "hashlib." in code and "import hashlib" not in code:
            required_imports.append("import hashlib")

        if required_imports:
            return "\n".join(required_imports) + "\n" + code
        return code

    def run(
        self,
        filename: str,
        source_code: str,
        on_step: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> PipelineResult:
        """
        Executes the closed-loop SAST scan and remediation lifecycle.
        
        Args:
            filename: Target file name or path.
            source_code: Source Python code to audit and remediate.
            on_step: Optional callback receiving lifecycle event dictionaries.
            
        Returns:
            PipelineResult containing telemetry, reports, and remediated code.
        """
        current_code = source_code
        audit_history: List[Dict[str, Any]] = []
        syntax_errors: List[str] = []
        initial_report: Optional[SecurityScanReport] = None
        final_report: Optional[SecurityScanReport] = None
        converged = False

        for iteration in range(1, self.max_iterations + 1):
            if on_step:
                on_step({
                    "event": "audit_start",
                    "pass_num": iteration,
                    "max_passes": self.max_iterations
                })

            report = scan_code_for_vulnerabilities(filename, current_code)
            if iteration == 1:
                initial_report = report

            count = len(report.vulnerabilities)
            audit_history.append({"pass": iteration, "count": count})
            final_report = report

            if on_step:
                on_step({
                    "event": "audit_complete",
                    "pass_num": iteration,
                    "vulnerabilities": count,
                    "report": report
                })

            # GATEKEEPER ZERO-FLAW CHECK
            if count == 0:
                converged = True
                if on_step:
                    on_step({
                        "event": "fast_path_exit" if iteration == 1 else "convergence_exit",
                        "pass_num": iteration,
                        "report": report
                    })
                break

            # REMEDIATION CYCLE VIA AGENT 2 (THE FIXER)
            if on_step:
                on_step({
                    "event": "fix_start",
                    "pass_num": iteration,
                    "vulnerabilities": count
                })

            fixed_raw = fix_code_vulnerabilities(filename, current_code, report.model_dump())
            clean_fixed = self.clean_markdown_fences(fixed_raw)
            clean_fixed = self.inject_missing_imports(clean_fixed)

            # AST SYNTAX GATEKEEPER
            is_valid, syntax_error = validate_python_syntax(clean_fixed)
            if not is_valid and syntax_error:
                syntax_errors.append(f"Pass {iteration}: {syntax_error}")
                if on_step:
                    on_step({
                        "event": "syntax_error",
                        "pass_num": iteration,
                        "error": syntax_error
                    })
            else:
                current_code = clean_fixed

            if on_step:
                on_step({
                    "event": "fix_complete",
                    "pass_num": iteration,
                    "syntax_valid": is_valid
                })

        # FINAL VERIFICATION RE-AUDIT
        # If the code was modified by Agent 2 but convergence wasn't checked on the final iteration
        if not converged and current_code != source_code:
            if on_step:
                on_step({
                    "event": "audit_start",
                    "pass_num": len(audit_history) + 1,
                    "max_passes": self.max_iterations
                })

            verify_report = scan_code_for_vulnerabilities(filename, current_code)
            verify_count = len(verify_report.vulnerabilities)
            audit_history.append({"pass": len(audit_history) + 1, "count": verify_count})
            final_report = verify_report

            if verify_count == 0:
                converged = True
                if on_step:
                    on_step({
                        "event": "convergence_exit",
                        "pass_num": len(audit_history),
                        "report": verify_report
                    })
            else:
                if on_step:
                    on_step({
                        "event": "max_iterations_reached",
                        "pass_num": len(audit_history),
                        "vulnerabilities": verify_count,
                        "report": verify_report
                    })

        # Ensure fallback report object exists
        dummy_report = SecurityScanReport(target_file=filename, vulnerabilities=[])
        resolved_initial_report = initial_report or dummy_report
        resolved_final_report = final_report or dummy_report

        return PipelineResult(
            original_code=source_code,
            final_code=current_code,
            converged=converged,
            iterations_used=len(audit_history),
            initial_report=resolved_initial_report,
            final_report=resolved_final_report,
            audit_history=audit_history,
            syntax_errors=syntax_errors
        )
