import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path="docs/RepoGuard_AKTU_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette: Cyberpunk Dark Theme / Academic Tech
    C_BG = RGBColor(10, 14, 23)        # #0a0e17 Dark Slate
    C_PANEL = RGBColor(22, 27, 34)     # #161b22 Card Panel
    C_BLUE = RGBColor(31, 111, 235)     # #1f6feb Primary Tech Blue
    C_CYAN = RGBColor(88, 166, 255)     # #58a6ff Highlight Cyan
    C_GREEN = RGBColor(63, 185, 80)     # #3fb950 Security Green
    C_WHITE = RGBColor(240, 246, 252)   # #f0f6fc Text Primary
    C_MUTED = RGBColor(139, 148, 158)   # #8b949e Text Muted
    C_ACCENT = RGBColor(210, 153, 34)   # #d29922 Amber Accent

    blank_layout = prs.slide_layouts[6]

    def set_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="AKTU B.TECH 5TH SEMESTER MINI PROJECT"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_CYAN

        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

        # Divider line
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.55), Inches(11.7), Inches(0.04))
        div.fill.solid()
        div.fill.fore_color.rgb = C_BLUE
        div.line.fill.background()

    def add_card(slide, left, top, width, height, title="", body_items=None, border_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = C_PANEL
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.color.rgb = RGBColor(48, 54, 61)
            card.line.width = Pt(1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        tf.margin_bottom = Inches(0.2)

        if title:
            p_head = tf.paragraphs[0]
            p_head.text = title
            p_head.font.size = Pt(17)
            p_head.font.bold = True
            p_head.font.color.rgb = C_CYAN
            p_head.space_after = Pt(8)

        if body_items:
            for idx, item in enumerate(body_items):
                p = tf.add_paragraph() if title or idx > 0 else tf.paragraphs[0]
                p.text = "•  " + item
                p.font.size = Pt(13)
                p.font.color.rgb = C_WHITE
                p.space_after = Pt(6)

    # ----------------- SLIDE 1: Title Slide -----------------
    s1 = prs.slides.add_slide(blank_layout)
    set_background(s1)

    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(2.2))
    tf1 = t_box.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "RepoGuard AI"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = C_CYAN

    p2 = tf1.add_paragraph()
    p2.text = "Autonomous Multi-Agent SAST & Automated Vulnerability Remediation"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE
    p2.space_before = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "A Zero-Cost, Local-LLM Static Code Security Platform with Self-Healing Feedback Loop"
    p3.font.size = Pt(14)
    p3.font.color.rgb = C_MUTED
    p3.space_before = Pt(4)

    # Sub details card
    c_meta = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(3.8), Inches(11.3), Inches(2.6))
    c_meta.fill.solid()
    c_meta.fill.fore_color.rgb = C_PANEL
    c_meta.line.color.rgb = C_BLUE
    c_meta.line.width = Pt(1.5)
    tf_meta = c_meta.text_frame
    tf_meta.word_wrap = True
    tf_meta.margin_left = Inches(0.4)
    tf_meta.margin_top = Inches(0.3)

    pm1 = tf_meta.paragraphs[0]
    pm1.text = "ACADEMIC PROJECT SUBMISSION"
    pm1.font.size = Pt(13)
    pm1.font.bold = True
    pm1.font.color.rgb = C_GREEN

    pm2 = tf_meta.add_paragraph()
    pm2.text = "Curriculum: Bachelor of Technology (B.Tech) - 5th Semester Mini Project"
    pm2.font.size = Pt(14)
    pm2.font.color.rgb = C_WHITE
    pm2.space_before = Pt(6)

    pm3 = tf_meta.add_paragraph()
    pm3.text = "Affiliation: Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow, Uttar Pradesh"
    pm3.font.size = Pt(14)
    pm3.font.color.rgb = C_MUTED
    pm3.space_before = Pt(4)

    pm4 = tf_meta.add_paragraph()
    pm4.text = "Domain: Artificial Intelligence, Cybersecurity & DevSecOps Engineering"
    pm4.font.size = Pt(14)
    pm4.font.color.rgb = C_CYAN
    pm4.space_before = Pt(4)

    # ----------------- SLIDE 2: Motivation & Background -----------------
    s2 = prs.slides.add_slide(blank_layout)
    set_background(s2)
    add_header(s2, "Motivation & Industry Background")
    add_card(s2, 0.8, 1.8, 5.6, 5.0, "The DevSecOps Crisis", [
        "Modern applications face escalating code-level attacks: SQL Injection, Command Execution, and Secret Leaks remain in OWASP Top 10.",
        "Manual code reviews are slow, inconsistent, and cannot keep up with rapid agile sprint cycles.",
        "Over 70% of application vulnerabilities stem from preventable software implementation flaws.",
        "Security is often treated as an afterthought during final testing rather than shifted left to code writing."
    ])
    add_card(s2, 6.8, 1.8, 5.7, 5.0, "Why Local Agentic AI?", [
        "Traditional tools detect problems but place 100% of the fixing burden onto developers.",
        "Cloud LLM APIs (OpenAI, Anthropic) pose critical data privacy and IP theft risks when sending proprietary source code.",
        "Local open-weights models (Ollama + Qwen2.5-Coder) ensure complete data confidentiality and zero operational costs.",
        "Autonomous multi-agent loops can bridge the gap from passive flaw detection to active, surgical patch synthesis."
    ])

    # ----------------- SLIDE 3: Problem Statement -----------------
    s3 = prs.slides.add_slide(blank_layout)
    set_background(s3)
    add_header(s3, "Problem Statement & Gap Analysis")
    add_card(s3, 0.8, 1.8, 3.6, 5.0, "Conventional SAST Tools\n(Bandit, SonarQube)", [
        "Rule & Regex based: Lacks semantic comprehension of program control flow.",
        "High False Positive Rate: Flags safe code and floods developers with noise.",
        "Passive Warning Only: Tells you 'what is wrong' but NEVER repairs the code.",
        "No Auto-Remediation: Developer must spend hours context switching to fix."
    ])
    add_card(s3, 4.8, 1.8, 3.6, 5.0, "Direct Single LLM Chat\n(Naive ChatGPT)", [
        "Unconstrained hallucination: Often changes function names and breaks working logic.",
        "Missing Dependencies: Generates code calling non-existent modules or unsafe packages.",
        "Unverified Output: Once code is returned, there is no second check if the fix is actually safe.",
        "Non-deterministic format: Outputs chat prose instead of parseable code patches."
    ])
    add_card(s3, 8.8, 1.8, 3.7, 5.0, "RepoGuard Innovation\n(Proposed System)", [
        "Two Specialized Agents: Clean separation between Hacker/Auditor and Secure Fixer.",
        "Closed-Loop Gatekeeper: Re-audits every generated fix until 0 flaws remain.",
        "Zero Cloud Cost: Runs 100% on local machine using Ollama.",
        "Surgical Guarantee: Preserves function signatures, imports, and program contracts."
    ], border_color=C_GREEN)

    # ----------------- SLIDE 4: Architecture -----------------
    s4 = prs.slides.add_slide(blank_layout)
    set_background(s4)
    add_header(s4, "RepoGuard System Architecture")
    add_card(s4, 0.8, 1.8, 3.6, 5.0, "Phase 1: Agent 1 (Auditor)", [
        "Model: Qwen2.5-Coder:7b (via Ollama)",
        "Taint Analysis: Traces untrusted sources to critical sinks.",
        "Exclusion Filter: Enforces strict ground-truth rules to kill false positives.",
        "Pydantic JSON Contract: Emits typed list of vulnerabilities with line numbers and exploit PoCs."
    ], border_color=C_CYAN)
    add_card(s4, 4.8, 1.8, 3.6, 5.0, "Phase 2: Gatekeeper Loop", [
        "Zero-Flaw Bypass: If 0 vulnerabilities found on Pass 1, Agent 2 is skipped completely (Fast Exit).",
        "Convergence Check: Re-submits remediated code to Agent 1.",
        "Termination Condition: Exits when 0 vulnerabilities remain or Max Passes (3) reached.",
        "Import Post-Processor: Automatically fixes missing imports (pathlib, subprocess, os)."
    ], border_color=C_ACCENT)
    add_card(s4, 8.8, 1.8, 3.7, 5.0, "Phase 3: Agent 2 (Fixer)", [
        "Targeted Remediation: Resolves only flagged vulnerabilities.",
        "Standard Library Guardrails: Uses stdlib PBKDF2-HMAC (bans unavailable bcrypt).",
        "Parameterized Queries: Replaces dynamic SQL concatenations.",
        "Docstring Sanitization: Strips vulnerability titles from comments to prevent self-confusion."
    ], border_color=C_GREEN)

    # ----------------- SLIDE 5: Agent 1 Details -----------------
    s5 = prs.slides.add_slide(blank_layout)
    set_background(s5)
    add_header(s5, "Agent 1: The SAST Auditor & Schema Contract")
    add_card(s5, 0.8, 1.8, 5.6, 5.0, "Taint Analysis & Ground Truth Filter", [
        "Evaluates whether untrusted external data reaches dangerous execution sinks without sanitization.",
        "Strict Exclusion Rules (Eliminating False Positives):",
        "  1. DO NOT flag os.getenv('KEY') as hardcoded secrets.",
        "  2. DO NOT flag parameterized queries with (?) placeholders.",
        "  3. DO NOT flag Path.resolve().is_relative_to() boundary checks.",
        "  4. DO NOT flag list-argument subprocess.run([...]) without shell=True.",
        "  5. DO NOT flag hashlib.pbkdf2_hmac or sha256 as weak cryptography.",
        "  6. DO NOT flag default mutable args if initialized inside function body."
    ])
    add_card(s5, 6.8, 1.8, 5.7, 5.0, "Rigid Pydantic JSON Contract", [
        "Enforces deterministic structured output via Ollama JSON Schema mode:",
        "class VulnerabilityItem(BaseModel):",
        "    id: str",
        "    type: str (SQLi, Command Injection, etc.)",
        "    line_number: int",
        "    severity: CRITICAL | HIGH | MEDIUM | LOW",
        "    description: str (Root-cause explanation)",
        "    poc_exploit: str (Proof-of-concept payload)",
        "",
        "Eliminates free-form model chatter and enables programmatic parsing."
    ])

    # ----------------- SLIDE 6: Agent 2 Details -----------------
    s6 = prs.slides.add_slide(blank_layout)
    set_background(s6)
    add_header(s6, "Agent 2: The Secure Fixer & Remediation Engine")
    add_card(s6, 0.8, 1.8, 5.6, 5.0, "Surgical Code Remediation Rules", [
        "Minimal AST Mutation: Only alters flawed lines, strictly preserving original signatures, variables, and logic.",
        "Sanctioned Cryptography: Automatically upgrades broken MD5/SHA-1 to hashlib.pbkdf2_hmac with 100,000 iterations.",
        "SQL Parameterization: Converts raw string formatting into parameterized database tuples.",
        "Path Normalization: Wraps raw file paths with Path(path).resolve().is_relative_to(base).",
        "Command Sanitization: Replaces os.system() and shell=True with argument list arrays."
    ])
    add_card(s6, 6.8, 1.8, 5.7, 5.0, "Self-Healing & Sanitization Guardrails", [
        "Anti-Pattern Rectification: Automatically repairs mutable default arguments (lst=[] to lst=None).",
        "Docstring Cleansing: Models often copy docstring text containing 'SQL INJECTION' which confuses re-audits; Agent 2 rewrites docstrings cleanly.",
        "Mandatory Imports Injection: Main pipeline guarantees missing imports like 'from pathlib import Path' are prepended if needed.",
        "Single Code Block Output: RegEx extractor isolates raw Python code from markdown tags."
    ])

    # ----------------- SLIDE 7: Self-Correction Loop -----------------
    s7 = prs.slides.add_slide(blank_layout)
    set_background(s7)
    add_header(s7, "Self-Correction & Gatekeeper Convergence")
    add_card(s7, 0.8, 1.8, 5.6, 5.0, "The Multi-Pass Feedback Loop", [
        "Why One Pass Is Not Enough:",
        "  Fixing one vulnerability might introduce a new flaw or leave subtle edge cases unfixed.",
        "RepoGuard's Closed Loop (Max 3 Passes):",
        "  Pass 1: Auditor identifies flaws (e.g. 6 vulnerabilities found).",
        "  Remediation: Fixer rewrites code with security patches.",
        "  Pass 2: Code is fed directly BACK into Auditor to verify fixes.",
        "  Convergence: If flaws = 0, pipeline halts immediately with success.",
        "  Safeguard: If iteration limit reached, saves best-effort verified state."
    ])
    add_card(s7, 6.8, 1.8, 5.7, 5.0, "Convergence Telemetry (Sample Run)", [
        "Pass 1: Auditor detected 6 issues (Secrets, MD5, SQLi, Traversal, Command Injection, Mutable Arg).",
        "Pass 2: Fixer generated secure patches and post-processor injected imports.",
        "Re-Audit (Pass 2): Auditor scanned remediated code against exclusion rules.",
        "Result: 0 residual vulnerabilities found! Pipeline achieved verified convergence.",
        "Zero-Flaw Bypass: Pre-secured files complete in a single pass without touching Agent 2."
    ], border_color=C_GREEN)

    # ----------------- SLIDE 8: Tech Stack -----------------
    s8 = prs.slides.add_slide(blank_layout)
    set_background(s8)
    add_header(s8, "Technical Stack & Implementation")
    add_card(s8, 0.8, 1.8, 3.6, 5.0, "Inference & Agents", [
        "Ollama Runtime: Lightweight local model daemon.",
        "Qwen2.5-Coder:7b: State-of-the-art 7-billion parameter code LLM.",
        "Deterministic Options: Temperature = 0.0, Seed = 42 for repeatable, verifiable scans.",
        "Context Window: 4096 tokens."
    ])
    add_card(s8, 4.8, 1.8, 3.6, 5.0, "Backend & Validation", [
        "Python 3.10+: Core programming language.",
        "Pydantic v2: Strong typing, data validation, and JSON schema generation.",
        "Standard Library Power: Hashlib, Pathlib, Subprocess, Sqlite3, Re.",
        "Difflib: Generates git-style unified diff patches."
    ])
    add_card(s8, 8.8, 1.8, 3.7, 5.0, "Frontend & Telemetry", [
        "Streamlit: Reactive web dashboard.",
        "Cyberpunk Dark UI: JetBrains Mono typography, custom glassmorphism cards.",
        "Telemetry Widgets: Live execution status, loop depth, initial vs residual flaws.",
        "Download Export: One-click export of verified safe Python code."
    ])

    # ----------------- SLIDE 9: Vulnerability Matrix -----------------
    s9 = prs.slides.add_slide(blank_layout)
    set_background(s9)
    add_header(s9, "Vulnerability Coverage & Evaluation Matrix")
    add_card(s9, 0.8, 1.8, 11.7, 5.0, "Tested Vulnerability Classes & Autonomous Remediations", [
        "1. Hardcoded Secrets (CWE-798): Static API keys / tokens replaced with os.getenv('KEY') with no hardcoded fallback.",
        "2. Weak Cryptography (CWE-327 / CWE-328): Fast MD5/SHA-1 password hashing upgraded to slow PBKDF2-HMAC-SHA256 (100k rounds) with salt.",
        "3. SQL Injection (CWE-89): Raw f-string and % formatting queries converted into parameterized SQL statements with (?) placeholders.",
        "4. Path Traversal (CWE-22): Concatenated file paths wrapped with Path(path).resolve().is_relative_to(base) directory boundary guards.",
        "5. OS Command Injection (CWE-78): Unsanitized os.system() and shell=True replaced with list argument arrays via subprocess.run([...]).",
        "6. Mutable Default Arguments (CWE-665): Function arguments like def func(trail=[]) repaired to def func(trail=None)."
    ])

    # ----------------- SLIDE 10: Live Demo Walkthrough -----------------
    s10 = prs.slides.add_slide(blank_layout)
    set_background(s10)
    add_header(s10, "Live Demonstration Walkthrough")
    add_card(s10, 0.8, 1.8, 5.6, 5.0, "Preset Test Scenarios Available in UI", [
        "1. Full Vulnerability Bundle: 6 simultaneous security flaws to test convergence.",
        "2. Clean Compliant Code: Proves zero false positives and triggers the single-pass Fast Exit.",
        "3. SQL Injection & Insecure Auth: Focused demonstration of credential and database attacks.",
        "4. Command Injection & Path Traversal: Demonstrates OS-level boundary and command defenses.",
        "5. Custom Code Editor: Evaluators can paste any Python snippet live during viva."
    ])
    add_card(s10, 6.8, 1.8, 5.7, 5.0, "UI Features for Examiner Inspection", [
        "Telemetry Metrics: Real-time counter of initial flaws, passes taken, and residual flaws.",
        "Side-by-Side Review: Original vulnerable source code placed directly beside remediated code.",
        "Exploit PoC Viewer: Shows exact payload used to trigger each vulnerability.",
        "Git-Style Unified Diff: Visual green/red lines showing surgical code modifications.",
        "One-Click Export: Downloads remediated_source.py directly to disk."
    ])

    # ----------------- SLIDE 11: Limitations & Future Scope -----------------
    s11 = prs.slides.add_slide(blank_layout)
    set_background(s11)
    add_header(s11, "Limitations & Future Roadmap")
    add_card(s11, 0.8, 1.8, 5.6, 5.0, "Current Limitations", [
        "Single File Scope: Current pipeline processes files individually rather than parsing inter-file dependency graphs.",
        "Hardware Dependency: Local 7B model requires at least 8GB RAM / VRAM for smooth inference.",
        "Language Support: Currently specialized for Python 3 AST and security idioms."
    ])
    add_card(s11, 6.8, 1.8, 5.7, 5.0, "Future Enhancements (8th Sem Major Project Scope)", [
        "Repository-Wide Call Graph: Inter-procedural taint analysis across multiple modules and packages.",
        "GitHub Actions CI/CD Bot: Automatically comment and push remediation PRs upon git push.",
        "VS Code Extension: Real-time 'Autonomous Security Linter' offering inline quick-fixes.",
        "Multi-Language Expansion: Adding support for JavaScript/TypeScript, Go, and Java."
    ])

    # ----------------- SLIDE 12: Conclusion -----------------
    s12 = prs.slides.add_slide(blank_layout)
    set_background(s12)
    add_header(s12, "Conclusion & Key Takeaways")
    add_card(s12, 0.8, 1.8, 11.7, 5.0, "Project Summary", [
        "1. True Shift-Left DevSecOps: RepoGuard transforms security from a manual bottleneck into an autonomous, self-healing pipeline.",
        "2. High Practicality & Zero Cost: Operates entirely locally with open-source LLMs without transmitting proprietary source code over cloud networks.",
        "3. High Reliability: Closed-loop multi-agent verification guarantees that patches do not introduce new vulnerabilities or break existing functionality.",
        "4. Strong Engineering Foundation: Combines AST taint principles, Pydantic type safety, and real-time interactive telemetry.",
        "5. Ready for Industry Application: Provides immediate value to developers, automated pull-request reviewers, and academic security researchers."
    ], border_color=C_GREEN)

    # ----------------- SLIDE 13: Q&A & References -----------------
    s13 = prs.slides.add_slide(blank_layout)
    set_background(s13)
    add_header(s13, "Thank You / Questions & Answers")
    add_card(s13, 0.8, 1.8, 6.0, 5.0, "Common Viva Questions Anticipated", [
        "Q: Why use Qwen2.5-Coder instead of OpenAI?",
        "A: Data privacy for proprietary code + zero operational cost on student hardware.",
        "Q: How do you stop model hallucinations?",
        "A: Pydantic JSON schema constraints + greedy temperature=0.0 + exclusion prompt rules.",
        "Q: How is this different from Bandit or SonarQube?",
        "A: Bandit only flags errors; RepoGuard detects and automatically synthesizes verified code patches."
    ])
    add_card(s13, 7.2, 1.8, 5.3, 5.0, "Key Literature & References", [
        "1. OWASP Top 10 Web Application Security Risks (2021/2025).",
        "2. MITRE Common Weakness Enumeration (CWE) Database.",
        "3. Qwen2.5-Coder Technical Report: Alibaba Cloud (2024).",
        "4. Static Program Analysis & Taint Flow (Nielson et al.).",
        "5. Ollama & Pydantic Documentation."
    ])

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Presentation saved successfully to '{output_path}'")

if __name__ == "__main__":
    create_deck()
