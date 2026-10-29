from docx.enum.text import WD_ALIGN_PARAGRAPH
from scripts.report_helpers import (
    add_chapter_title, add_section_title, add_subsection_title,
    add_p, add_bullet, add_table_with_caption, add_figure_box,
    add_code_snippet, add_algorithm_box
)

def write_chapter_2(doc):
    add_chapter_title(doc, "2", "Proposed Methodology")
    
    add_section_title(doc, "2.1", "Architectural Blueprint of the RepoGuard Framework")
    add_p(doc,
        "The RepoGuard architecture is engineered around the principle of decentralized, agentic separation of concerns. "
        "Rather than relying on a single monolithic language model to simultaneously identify, analyze, and repair security flaws, "
        "RepoGuard deploys two specialized, non-overlapping autonomous agents orchestrated by a deterministic supervisory engine "
        "designated as the Gatekeeper. Figure 2.1 provides the comprehensive architectural blueprint of the framework.")
    
    diagram_arch = [
        "+--------------------------------------------------------------------------------+",
        "|                             TARGET PYTHON SOURCE CODE                          |",
        "+--------------------------------------------------------------------------------+",
        "                                       |",
        "                                       v",
        "                 +-------------------------------------------+",
        "                 |        AGENT 1: THE AUDITOR (SAST)        |",
        "                 | - Qwen 2.5 Coder 7B (Ollama Local Daemon) |",
        "                 | - Greedy Taint-to-Sink Abstract Analysis  |",
        "                 | - Ground-Truth False-Positive Filter Rules|",
        "                 +-------------------------------------------+",
        "                                       |",
        "                                       v",
        "                 +-------------------------------------------+",
        "                 |       PYDANTIC DATA CONTRACT SCHEMA       |",
        "                 | Structured JSON Validation (Zero Chatter) |",
        "                 +-------------------------------------------+",
        "                                       |",
        "                                       v",
        "                            +--------------------+",
        "                            |  GATEKEEPER ENGINE |",
        "                            | (Convergence Check)|",
        "                            +--------------------+",
        "                              /                \\",
        "           [Vulnerabilities == 0]            [Vulnerabilities > 0]",
        "                    /                                    \\",
        "                   v                                      v",
        "    +----------------------------+         +-------------------------------+",
        "    |     FAST-PATH BYPASS       |         |   AGENT 2: THE FIXER ENGINE   |",
        "    | - Agent 2 is skipped       |         | - Surgical Remediation Rules  |",
        "    | - Zero mutation applied    |         | - Sanctioned Stdlib Cryptography|",
        "    | - Verbatim code emission   |         | - Docstring Sanitization Clean |",
        "    +----------------------------+         +-------------------------------+",
        "                   |                                      |",
        "                   |                                      v",
        "                   |                       +-------------------------------+",
        "                   |                       |    IMPORT POST-PROCESSOR      |",
        "                   |                       | - Subprocess / Pathlib Guarante|",
        "                   |                       +-------------------------------+",
        "                   |                                      |",
        "                   |                        [Re-audit Code / Loop Pass+1]  |",
        "                   |                                      |",
        "                   |               +----------------------+",
        "                   |               | (Iterative Convergence Feedback Loop)",
        "                   |               v",
        "                   |     +--------------------+",
        "                   +---->| FINAL SECURE CODE  |<--------------------------------+",
        "                         +--------------------+"
    ]
    add_figure_box(doc, "Figure 2.1: Architectural Blueprint and Execution Pipeline of RepoGuard Framework", diagram_arch)

    add_p(doc,
        "As illustrated in Figure 2.1, the pipeline executes in three distinct, sequential phases: "
        "(1) Taint Auditing and Schema Validation, (2) Gatekeeper Evaluation and Convergence Assessment, and "
        "(3) Surgical Remediation and AST Normalization. This iterative cycle repeats until formal convergence is "
        "attained or the hard boundary of three iterations is reached.")

    add_section_title(doc, "2.2", "Theoretical Foundations of Static Taint Analysis")
    add_p(doc,
        "Static taint analysis is a formal program analysis methodology designed to evaluate information flow security. "
        "Formally, a program P is represented as a directed Control Flow Graph (CFG), defined as G = (V, E), where vertices V "
        "represent program statements or basic blocks, and directed edges E represent transfer of execution control. "
        "Taint analysis models data propagation from un-sanitized external entry points to critical operational sinks [10].")
    add_p(doc,
        "Let S_src denote the set of taint Sources (e.g., HTTP request bodies, CLI arguments, environment inputs, or file uploads). "
        "Let S_snk denote the set of critical execution Sinks (e.g., database query execution functions, OS shell dispatchers, "
        "file system read/write routines, or hashing digests). An execution trace tau is defined as a sequence of operations "
        "tau = <v_1, v_2, ..., v_n> where v_i in V. An information flow path is vulnerable if and only if there exists a data "
        "dependence path between a source and a sink that does not intersect an authoritative Sanitizer predicate S_san:", bold_prefix="Mathematical Taint Formulation: ")
    
    add_p(doc,
        "    Vulnerable(tau) <=> exists (v_src, v_snk) such that (v_src in S_src) ^ (v_snk in S_snk) ^ (v_src ->* v_snk) ^ (Path(v_src, v_snk) intersect S_san = emptyset)\n",
        italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    
    add_p(doc,
        "Traditional SAST tools struggle with the formulation of S_san. If a developer sanitizes a path using a custom wrapper, "
        "pattern-matching tools frequently trigger false alarms. RepoGuard leverages the semantic comprehension of Qwen 2.5 Coder "
        "to accurately model whether the path between v_src and v_snk contains a mathematically sound sanitizer, such as query "
        "parameterization or path containment predicates.")

    add_section_title(doc, "2.3", "Agent 1 (The Security Auditor): Design and Prompt Engineering")
    add_p(doc,
        "Agent 1 operates as the dedicated security auditor. Its cognitive persona is strictly bounded: it does NOT attempt to "
        "rewrite code, suggest design patterns, or converse with the user. Its sole objective is to inspect the raw Python "
        "source code, identify authentic taint-sink violations, and emit a structured Pydantic report [11].")
    add_p(doc,
        "To ensure uncompromising precision, Agent 1's system prompt incorporates a rigorous 'Taint Analysis Methodology' instruction "
        "and a 'Zero-Vulnerability Expectation'. If the code follows secure coding standards, the model is strictly commanded to return "
        "an empty vulnerability list rather than hallucinating hypothetical risks.")

    add_section_title(doc, "2.4", "Strict Pydantic Data Contracts and Validated JSON Schemas")
    add_p(doc,
        "A chronic failure mode in standard LLM applications is 'output drift'—where models interleave natural language greetings, "
        "explanations, and markdown tags around JSON responses. In RepoGuard, this failure mode is eliminated by coupling Pydantic v2 "
        "data models directly with the Ollama API's native JSON Schema validation engine.")
    
    schema_code = (
        "class VulnerabilityItem(BaseModel):\n"
        "    id: str\n"
        "    type: str          # SQL_INJECTION, COMMAND_INJECTION, PATH_TRAVERSAL, etc.\n"
        "    line_number: int\n"
        "    severity: str      # CRITICAL | HIGH | MEDIUM | LOW\n"
        "    description: str   # Root cause explanation of flaw\n"
        "    poc_exploit: str   # Proof-of-concept payload demonstrating breach\n\n"
        "class SecurityScanReport(BaseModel):\n"
        "    target_file: str\n"
        "    vulnerabilities: List[VulnerabilityItem]\n"
    )
    add_code_snippet(doc, "Listing 2.1: Pydantic Data Contract Schema for Agent 1 Audit Reports", schema_code)

    add_p(doc,
        "During execution, the Pydantic schema is serialized into a JSON Schema definition and passed via the format parameter "
        "in the ollama.chat() API call. The local inference engine applies grammar-guided constrained decoding, forcing the logits "
        "to conform strictly to the Pydantic state machine. The resulting response is parsed via SecurityScanReport.model_validate_json(), "
        "guaranteeing 100% type-safe, parseable objects with zero extraction failures.")

    add_section_title(doc, "2.5", "Deterministic Sampling Parameters")
    add_p(doc,
        "Non-deterministic outputs are fatal in security auditing. If identical code evaluated across multiple CI runs emits "
        "differing vulnerability lists, the security gatekeeper loses all trustworthiness. RepoGuard enforces total execution "
        "determinism through two explicit hyperparameter constraints in both agents:")
    add_bullet(doc, "Greedy Decoding (temperature = 0.0): ", "Sets the softmax temperature to zero, causing the language model to deterministically select the token with the highest logit probability at every generation step (argmax decoding).")
    add_bullet(doc, "Fixed Pseudo-Random Seed (seed = 42): ", "Locks the initialization state of the pseudo-random number generator within the llama.cpp engine, eliminating inter-run variance across hardware invocations.")

    add_section_title(doc, "2.6", "Ground-Truth Exclusion Rules (False-Positive Suppression)")
    add_p(doc,
        "To solve the chronic 'alert fatigue' caused by conventional SAST tools, Agent 1's system prompt encodes eight explicit, "
        "non-negotiable Ground-Truth Exclusion Rules. These rules establish a formal contract defining what constitutes compliant code:")
    
    headers_rules = ["Rule #", "Target Pattern", "Compliant Implementation Recognized", "Exclusion Rationale"]
    rows_rules = [
        ["Rule 1", "Secret Retrieval", "os.getenv('KEY') / os.environ.get('KEY')", "Retrieving secrets from environment variables is the Gold Standard for 12-factor apps; never flag as hardcoded."],
        ["Rule 2", "SQL Queries", "cursor.execute(query, (param,)) with (?)", "Parameterized queries separate query logic from data, rendering SQL injection mathematically impossible."],
        ["Rule 3", "Path Containment", "Path.resolve().is_relative_to(base) or startswith", "Directory containment checks prevent directory traversal by validating canonical absolute paths."],
        ["Rule 4", "Command Dispatch", "subprocess.run(['cmd', arg]) without shell=True", "Argument list arrays bypass shell command parsing, preventing shell metacharacter injection."],
        ["Rule 5", "Cryptographic Hash", "hashlib.pbkdf2_hmac(...) or sha256()", "Salted, high-iteration PBKDF2-HMAC is compliant for passwords; standalone sha256 is acceptable for non-secrets."],
        ["Rule 6", "State Arguments", "history_list = None with internal init []", "Instantiating default collections inside the function body eliminates mutable state leakage across calls."],
        ["Rule 7", "Speculative Claims", "Hypothetical claims ('could be hardened')", "Auditor is strictly forbidden from flagging safe code based on subjective, hypothetical security advice."],
        ["Rule 8", "Comment Words", "Docstring keywords ('SQL INJECTION:')", "Auditor evaluates executable AST logic only, completely ignoring words found inside comments or docstrings."]
    ]
    add_table_with_caption(doc, "Table 2.1: Formal Ground-Truth False-Positive Exclusion Rules in Agent 1", headers_rules, rows_rules, [0.8, 1.2, 2.2, 2.3])

    add_section_title(doc, "2.7", "The Autonomous Gatekeeper Decision Mechanism")
    add_p(doc,
        "The supervisory logic connecting the two agents resides in the Gatekeeper engine (implemented in src/main.py and app.py). "
        "The Gatekeeper acts as an objective arbiter that evaluates the cardinality and contents of the vulnerability report. "
        "It prevents unconstrained loops and enforces convergence criteria through strict conditional branching:")
    add_bullet(doc, "Branch A (Zero Flaws - Convergence Reached): ", "If the vulnerability list is empty, the Gatekeeper terminates execution, marks the codebase as compliant, and writes the verified source code to the output target.")
    add_bullet(doc, "Branch B (Flaws Detected - Iteration Cap Not Reached): ", "If flaws are present and iteration < MAX_ITERATIONS, the report and code are dispatched to Agent 2 for remediation.")
    add_bullet(doc, "Branch C (Iteration Cap Reached - Fallback): ", "If flaws remain upon reaching MAX_ITERATIONS (default = 3), the pipeline halts to prevent infinite oscillation and saves the best-effort state with a telemetry warning.")

    add_section_title(doc, "2.8", "Fast-Path Zero-Vulnerability Bypass Logic")
    add_p(doc,
        "A critical innovation in RepoGuard is the 'Fast-Path Exit'. In standard AI-based code editors, clean code is routinely "
        "passed through a rewrite model, which frequently introduces formatting changes, alters docstrings, or introduces syntax regressions. "
        "RepoGuard's Gatekeeper enforces that compliant code is NEVER exposed to the fixer model. If Agent 1 returns zero vulnerabilities "
        "on Pass 1, Agent 2 is completely bypassed, and the original file is preserved verbatim. This guarantees 100% preservation "
        "of already secure software assets.")

    add_section_title(doc, "2.9", "Agent 2 (The Secure Fixer): Surgical Patch Synthesis")
    add_p(doc,
        "Agent 2 (The Fixer) receives the original source code along with Agent 1's structured JSON report. Its operational prompt "
        "is engineered to enforce surgical code modifications: it must resolve every vulnerability identified in the report without "
        "altering surrounding non-flawed business logic, renaming variables, or modifying function signatures.")
    add_p(doc,
        "Agent 2 operates under a 'Minimal AST Mutation' constraint. It treats the original code as an immutable baseline, replacing "
        "only the tainted AST subtrees with secure idioms. The output is constrained to a single fenced markdown block (```python ... ```), "
        "which is extracted via regular expression parsing to eliminate conversational preamble.")

    add_section_title(doc, "2.10", "Standard Library Security Guardrails")
    add_p(doc,
        "A major limitation of commercial LLM code assistants is the hallucination of non-existent packages or the introduction of "
        "heavy external dependencies (such as bcrypt, argon2-cffi, cryptography.fernet) that break deployments due to missing packages. "
        "RepoGuard enforces strict Standard Library (stdlib) Guardrails:")
    
    add_subsection_title(doc, "2.10.1", "Password Cryptography: PBKDF2-HMAC-SHA256")
    add_p(doc,
        "When weak hashing (MD5 or SHA-1) is identified, Agent 2 is strictly forbidden from importing bcrypt or argon2. "
        "Instead, it is mandated to use Python's built-in hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex(). "
        "This algorithm is natively available in the standard library, cryptographically secure with a high iteration work factor, "
        "and requires zero new packages installed in the runtime environment.")

    add_subsection_title(doc, "2.10.2", "Parameterized SQL Query Formulation")
    add_p(doc,
        "Dynamic SQL query strings utilizing Python f-strings, format(), or % operators are converted into parameterized database "
        "calls. For sqlite3, queries are formatted as cursor.execute('SELECT ... WHERE id = ?', (user_id,)). The query structure "
        "is compiled once by the database engine, ensuring untrusted input is treated strictly as literal data rather than executable code.")

    add_subsection_title(doc, "2.10.3", "Directory Traversal Prevention: Pathlib Resolution")
    add_p(doc,
        "To neutralize Path Traversal (CWE-22), Agent 2 wraps file path operations using Python's standard pathlib module. "
        "Paths are resolved to their canonical absolute forms using .resolve(), and directory containment is verified via "
        "file_path.resolve().is_relative_to(base_dir.resolve()). If an input contains traversal sequences (such as ../../etc/passwd), "
        "is_relative_to returns False, and the code raises a security exception.")

    add_subsection_title(doc, "2.10.4", "Command Injection Mitigation: Argument Vectorization")
    add_p(doc,
        "Dangerous shell execution functions such as os.system() and subprocess.run(..., shell=True) are replaced with vector-based "
        "list argument arrays: subprocess.run(['ping', '-c', '1', target_host], check=True). By setting shell=False (the default), "
        "the operating system dispatches the executable directly without invoking the system shell (/bin/sh or cmd.exe), completely "
        "neutralizing shell metacharacter chaining attacks (e.g., ; rm -rf /).")

    add_subsection_title(doc, "2.10.5", "State Isolation: Mutable Default Argument Remediation")
    add_p(doc,
        "Python functions utilizing mutable default arguments (such as def func(audit_trail=[])) leak state across invocations because "
        "the list is bound at function definition time. Agent 2 rectifies this anti-pattern by assigning None as the default argument "
        "and instantiating a fresh list within the local scope if the parameter is None.")

    add_section_title(doc, "2.11", "Docstring and Comment Sanitization Protocol")
    add_p(doc,
        "During iterative code generation, language models frequently reproduce comments from the original code that contain words like "
        "'# 3. SQL INJECTION (SQLi)' or '# 5. OS COMMAND INJECTION'. During subsequent re-audits in Pass 2, Agent 1's attention mechanism "
        "can become biased by these textual headers, triggering false-positive alerts despite the code logic being completely secure. "
        "To resolve this, Agent 2 enforces a strict Docstring Sanitization Protocol: all historical vulnerability headings in comments "
        "are stripped or rewritten to describe the secure functionality cleanly, ensuring that re-audits evaluate only executable logic.")

    add_section_title(doc, "2.12", "Post-Processing Engine and Mandatory Import Injection")
    add_p(doc,
        "Although Agent 2 is instructed to include all necessary imports, generative models occasionally emit code calling Path() or "
        "subprocess.run() without including the corresponding import statements. To guarantee 100% syntactically runnable code, "
        "RepoGuard integrates a deterministic Post-Processing Import Injector directly into the pipeline:")
    
    post_code = (
        "# Deterministic AST Import Post-Processor (src/main.py)\n"
        "required_imports = []\n"
        "if 'subprocess.' in clean_code and 'import subprocess' not in clean_code:\n"
        "    required_imports.append('import subprocess')\n"
        "if 'os.' in clean_code and 'import os' not in clean_code:\n"
        "    required_imports.append('import os')\n"
        "if 'Path(' in clean_code and 'from pathlib import Path' not in clean_code:\n"
        "    required_imports.append('from pathlib import Path')\n\n"
        "if required_imports:\n"
        "    clean_code = '\\n'.join(required_imports) + '\\n' + clean_code\n"
    )
    add_code_snippet(doc, "Listing 2.2: Deterministic Import Injection Post-Processing Routine", post_code)

    add_section_title(doc, "2.13", "Closed-Loop Self-Healing Convergence Mechanism")
    add_p(doc,
        "The defining algorithmic innovation of RepoGuard is its multi-pass feedback convergence loop. "
        "Let C_0 denote the original vulnerable source code. At each iteration i in {1, 2, ..., N_max}:")
    add_bullet(doc, "Step 1 (Audit): ", "R_i = Scan(C_{i-1}). R_i represents the structured SecurityScanReport emitted by Agent 1.")
    add_bullet(doc, "Step 2 (Verification): ", "If |R_i.vulnerabilities| == 0, the state has converged. Return C_{i-1} as verified secure.")
    add_bullet(doc, "Step 3 (Remediation): ", "If |R_i.vulnerabilities| > 0, generate C'_i = Fix(C_{i-1}, R_i) via Agent 2.")
    add_bullet(doc, "Step 4 (Post-Process): ", "Apply import injection: C_i = PostProcess(C'_i). Increment i and loop back to Step 1.")

    add_section_title(doc, "2.14", "Algorithmic Formulations")
    add_p(doc,
        "The following formal algorithms define the operational behavior of the RepoGuard autonomous pipeline:")

    algo1_steps = [
        "Construct prompt P_auditor with SYSTEM_PROMPT, Exclusion Rules, and Target Code C.",
        "Set inference parameters: temperature = 0.0, seed = 42, context = 4096.",
        "Serialize Pydantic SecurityScanReport into JSON Schema format S_json.",
        "Dispatch chat request to Ollama daemon: resp = ollama.chat(model='qwen2.5-coder:7b', format=S_json).",
        "Validate response payload against schema: report = SecurityScanReport.model_validate_json(resp.content).",
        "Return structured report object containing validated VulnerabilityItem records."
    ]
    add_algorithm_box(doc, "1", "Autonomous Static Taint Analysis & Schema Validation", 
                      "Target Source Code C, File Identifier F_name", 
                      "Validated Pydantic SecurityScanReport Object R", algo1_steps)

    algo2_steps = [
        "Initialize current_code C = C_0, iteration i = 1, converged = False.",
        "While i <= MAX_ITERATIONS (3) do:",
        "    Execute Algorithm 1: report = ScanCode(current_code).",
        "    If len(report.vulnerabilities) == 0 then:",
        "        converged = True; Break from loop.",
        "    Else if i == MAX_ITERATIONS then:",
        "        Log warning: Maximum loop iterations reached; Break from loop.",
        "    End If",
        "    Dispatch remediation request to Agent 2: raw_fixed = FixCode(current_code, report).",
        "    Clean markdown fences using regular expressions: clean_code = StripFences(raw_fixed).",
        "    Execute PostProcessImports(clean_code) to ensure required imports exist.",
        "    Update current_code = clean_code; Increment iteration i = i + 1.",
        "End While",
        "Write current_code to output destination; Return (converged, current_code)."
    ]
    add_algorithm_box(doc, "2", "Closed-Loop Gatekeeper Convergence & Verification", 
                      "Vulnerable Source Code C_0, Max Passes N_max", 
                      "Convergence Status Boolean, Remediated Source Code C_final", algo2_steps)

    add_section_title(doc, "2.15", "Interactive Streamlit Web Interface and Telemetry Architecture")
    add_p(doc,
        "To deliver a production-grade developer experience, RepoGuard provides an interactive web application built on Streamlit "
        "featuring a modern cyberpunk dark-mode aesthetic. The interface components include:", bold_prefix="UI Architecture: ")
    add_bullet(doc, "Real-Time Telemetry Cards: ", "Displaying Initial Flaw Count, Convergence Loop Passes Taken, Residual Flaws, and Gatekeeper Verification Badges.")
    add_bullet(doc, "Multi-Preset Sample Loader: ", "Allowing single-click evaluation across clean code, SQLi demos, command injection scenarios, or custom user-pasted scripts.")
    add_bullet(doc, "Comparative Side-by-Side Review: ", "Presenting original vulnerable source code directly adjacent to the remediated code with synchronized scrolling.")
    add_bullet(doc, "Unified Git Diff Viewer: ", "Rendering standard git patch diffs with red deletions and green insertions generated via Python's difflib module.")
    add_bullet(doc, "Vulnerability Breakdown Cards: ", "Collapsible accordions displaying root cause explanations, severity tags, line numbers, and proof-of-concept exploits.")

    print("Chapter 2 written successfully.")
