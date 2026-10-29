from scripts.report_helpers import (
    add_chapter_title, add_section_title, add_subsection_title,
    add_p, add_bullet, add_table_with_caption, add_figure_box
)

def write_chapter_1(doc):
    add_chapter_title(doc, "1", "Introduction")
    
    add_section_title(doc, "1.1", "Background and Overview of Application Security")
    add_p(doc, 
        "In the contemporary landscape of digital transformation, software applications constitute the operational backbone "
        "of global commerce, governance, healthcare, and critical infrastructure. As organizations transition toward rapid, "
        "continuous delivery cycles powered by agile methodologies and DevOps practices, the volume, complexity, and velocity "
        "of codebase expansion have accelerated exponentially. However, this unprecedented acceleration has introduced severe "
        "systemic challenges in maintaining software security integrity. Application-layer vulnerabilities have emerged as the "
        "predominant attack vector exploited by malicious adversaries, resulting in catastrophic data breaches, financial extortion, "
        "regulatory non-compliance penalties, and severe erosion of institutional trust [1].")
    add_p(doc,
        "Historically, software security was treated as an isolated, post-development gatekeeping phase conducted immediately "
        "prior to production release. Security specialists performed point-in-time penetration testing and manual source code "
        "audits. While thorough, this manual inspection methodology is inherently non-scalable, labor-intensive, error-prone, "
        "and fundamentally incompatible with modern agile software engineering. A typical enterprise software system consists "
        "of hundreds of thousands—often millions—of lines of source code distributed across microservices, polyglot repositories, "
        "and intricate third-party package dependencies. Security auditing teams are severely outnumbered by development teams, "
        "often at ratios exceeding one security engineer per seventy-five developers [2]. Consequently, software security "
        "auditing must evolve from manual human oversight into autonomous, machine-driven, and highly verifiable processes.")

    add_section_title(doc, "1.2", "Evolution of Application Security Testing Paradigms")
    add_p(doc,
        "To contextualize the operational necessity of autonomous security systems, it is essential to examine the historical "
        "evolution of Application Security Testing (AST) paradigms across software engineering history. AST methodologies are "
        "categorized into four primary quadrants: Static Application Security Testing (SAST), Dynamic Application Security "
        "Testing (DAST), Interactive Application Security Testing (IAST), and Runtime Application Self-Protection (RASP) [3].")
    
    headers_ast = ["Testing Paradigm", "Execution Context", "Access Level", "Strengths", "Critical Weaknesses"]
    rows_ast = [
        ["SAST (Static)", "Compile-time / Pre-commit", "White-Box (Source Code)", "Full code coverage; early flaw detection; line-level precision", "High false-positive noise; lacks runtime context; zero remediation ability"],
        ["DAST (Dynamic)", "Runtime / Staging", "Black-Box (External Endpoints)", "Identifies live deployment issues; evaluates firewall & TLS", "Late in lifecycle; misses backend logic; cannot pinpoint source code line"],
        ["IAST (Interactive)", "Runtime Instrumentation", "Glass-Box (Agent in Runtime)", "Low false positives; correlates execution with source code", "Heavy runtime overhead; complex setup; requires high test suite coverage"],
        ["Autonomous SAST (RepoGuard)", "Pre-commit / IDE / CI-CD", "White-Box (Semantic Agentic)", "Deterministic detection, root-cause explanation, and autonomous surgical code repair", "Requires localized LLM inference compute (GPU/NPU or >=8GB RAM)"]
    ]
    add_table_with_caption(doc, "Table 1.1: Comparative Taxonomy of Application Security Testing (AST) Paradigms", headers_ast, rows_ast, [1.1, 1.1, 1.2, 1.6, 1.5])
    
    add_p(doc,
        "As delineated in Table 1.1, conventional SAST tools analyze raw uncompiled or compiled source code without executing "
        "the application. This white-box visibility provides unparalleled broad code coverage across an entire software repository. "
        "However, legacy SAST solutions rely on rudimentary Abstract Syntax Tree (AST) pattern matching, regex heuristics, and "
        "coarse-grained control flow graph traversals. These conventional heuristics suffer from chronic deficiencies: they emit "
        "an overwhelming volume of false-positive alerts, lack semantic context regarding sanitization wrappers, and—most "
        "critically—are fundamentally passive. They inform developers that a vulnerability exists but place the entire burden "
        "of researching, synthesizing, testing, and applying the remediation patch squarely on the developer's shoulders [4].")

    add_section_title(doc, "1.3", "The Shift-Left Paradigm and DevSecOps Integration")
    add_p(doc,
        "The software engineering industry has responded to the crisis of late-stage vulnerability discovery through the "
        "'Shift-Left' security philosophy. Under this paradigm, security controls and validation gates are migrated from the "
        "tail end of the deployment pipeline directly into the earliest phases of the Software Development Life Cycle (SDLC)—namely, "
        "the local Integrated Development Environment (IDE), pre-commit hooks, and initial Continuous Integration (CI) build triggers [5].")
    add_p(doc,
        "According to empirical studies conducted by the National Institute of Standards and Technology (NIST), the cost of "
        "remediating a software defect scales exponentially across the SDLC. Remedying an architectural security flaw during the "
        "coding or initial commit phase is approximately thirty times less expensive than attempting to patch the defect after "
        "production deployment, and hundreds of times less costly than mitigating an active exploit in the wild [6]. However, "
        "merely shifting conventional, noisy SAST scanners left has resulted in acute 'developer alert fatigue.' When developers "
        "are bombarded by false-positive security warnings, they routinely bypass, disable, or ignore scanner outputs. Therefore, "
        "an effective Shift-Left framework must satisfy three fundamental criteria: extreme accuracy (near-zero false positives), "
        "instantaneous actionable explanations, and automated, verified remediation.")

    add_section_title(doc, "1.4", "Problem Statement: The Remediation Void in Modern SAST")
    add_p(doc,
        "The central problem addressed by this research project is the pervasive 'Remediation Void' in modern software security. "
        "While automated tools for vulnerability *detection* have reached commercial ubiquity, tools for automated *remediation* "
        "remain almost completely absent from mainstream developer workflows. When a static scanner flags a critical weakness—such "
        "as a SQL Injection (CWE-89), an OS Command Injection (CWE-78), or an Arbitrary Path Traversal (CWE-22)—the human engineer "
        "must navigate a complex multi-step triage process:", bold_prefix="Problem Definition: ")
    
    add_bullet(doc, "1. Context Switching & Investigation: ", "The engineer must disengage from active feature development to trace the data flow reported by the scanner through multiple modules.")
    add_bullet(doc, "2. Domain-Specific Vulnerability Research: ", "The developer must identify the appropriate defensive coding pattern (e.g., parameterized queries, secure hash algorithms with high work factors, path containment predicates).")
    add_bullet(doc, "3. Manual Patch Synthesis: ", "The engineer must modify the code without breaking existing business logic, altering function signatures, or violating architectural conventions.")
    add_bullet(doc, "4. Verification & Regression Testing: ", "The engineer must manually verify that the applied patch successfully neutralized the vulnerability without introducing secondary security weaknesses.")
    
    add_p(doc,
        "This manual remediation loop accounts for over 65% of the total engineering effort expended on application security. "
        "In fast-paced sprint cycles, security tickets frequently languish in project backlogs for months, leaving vulnerable "
        "code paths exposed in production. A critical need exists for an intelligent, autonomous pipeline capable of not only "
        "identifying security flaws with high precision but also synthesizing surgically sound, syntactically valid, and "
        "formally verified code patches.")

    add_section_title(doc, "1.5", "Critical Analysis of Existing Tools and State-of-the-Art")
    add_p(doc,
        "To establish the novelty and necessity of RepoGuard, an extensive comparative audit was conducted across existing "
        "commercial and open-source static analysis utilities widely deployed in Python ecosystems [7]:")
    
    add_bullet(doc, "Bandit: ", "An open-source SAST tool designed specifically for Python. Bandit parses the Python AST and inspects nodes using pre-configured heuristic plugins. While lightweight and fast, Bandit exhibits zero semantic understanding of user taint sources. For example, it frequently flags harmless uses of hashlib.md5 used for non-cryptographic checksums, yet fails to recognize dynamic SQL string concatenations passed through helper functions. Furthermore, Bandit provides zero code remediation capabilities.")
    add_bullet(doc, "SonarQube: ", "An enterprise static analysis platform that utilizes SonarSource analyzers to calculate code smell, security vulnerabilities, and technical debt. SonarQube features advanced data flow rules, but its rulesets are rigid, expensive to deploy on-premise, and provide only generic text descriptions of remediations rather than direct, context-aware code patches.")
    add_bullet(doc, "Flake8 & Pylint (Security Plugins): ", "Linters that enforce PEP 8 style standards and rudimentary bug patterns. They lack deep inter-procedural taint propagation analysis and are incapable of reasoning about complex cryptographic or multi-line path traversal vectors.")
    add_bullet(doc, "Semgrep: ", "A semantic pattern-matching engine that allows engineers to query codebases using code-like syntax. While a substantial improvement over regular expressions, Semgrep rule maintenance requires specialized domain knowledge, and its automated autofix features are strictly limited to simple single-line text substitutions.")

    add_section_title(doc, "1.6", "Security and Privacy Risks of Cloud-Hosted Code LLMs")
    add_p(doc,
        "With the recent emergence of Large Language Models (LLMs) such as OpenAI's GPT-4, Anthropic's Claude, and Google's "
        "Gemini, software developers have increasingly turned to conversational AI to assist in code generation and debugging. "
        "However, integrating cloud-hosted LLM APIs into enterprise security pipelines introduces catastrophic privacy and legal "
        "hazards [8]:")
    add_p(doc,
        "1. Intellectual Property (IP) Exfiltration: Transmitting proprietary source code over public internet endpoints to "
        "third-party infrastructure violates corporate non-disclosure agreements, data governance policies, and sovereign data "
        "residency mandates (such as GDPR, HIPAA, and India's Digital Personal Data Protection Act).", bold_prefix="Data Sovereignty: ")
    add_p(doc,
        "2. Training Data Ingestion & Model Poisoning: Public LLM providers may ingest transmitted user snippets for future "
        "model training passes, creating the risk that proprietary algorithms, cryptographic keys, or internal API structures "
        "could be inadvertently memorized and reproduced in prompts answered to competitors.", bold_prefix="Privacy Leakage: ")
    add_p(doc,
        "3. Telemetry & Financial Overhead: Cloud API billing models charge per input/output token. In continuous integration "
        "pipelines scanning repositories containing millions of tokens per commit, operational API costs become prohibitively "
        "expensive.", bold_prefix="Economic Viability: ")
    add_p(doc,
        "These systemic hazards demand that next-generation automated security systems operate entirely within the local air-gapped "
        "perimeter of the developer's machine or self-hosted enterprise infrastructure, utilizing optimized open-weights models.")

    add_section_title(doc, "1.7", "Research Motivation and Architectural Rationale")
    add_p(doc,
        "The driving motivation behind RepoGuard is the convergence of two breakthrough technologies: (1) state-of-the-art "
        "compact open-weights code language models, specifically Alibaba Cloud's Qwen 2.5 Coder 7B, which achieve code reasoning "
        "parity with legacy 70B models while executing efficiently on consumer-grade hardware via Ollama; and (2) Multi-Agent "
        "Collaborative Systems that decouple complex cognitive workflows into specialized, non-overlapping autonomous personas [9].")
    add_p(doc,
        "A single, unconstrained LLM prompted to 'find and fix all security bugs' inevitably fails in real-world environments. "
        "When forced to act simultaneously as an auditor and a coder, single models exhibit high hallucination rates: they "
        "invent non-existent helper functions, alter working business logic, strip necessary comments, and fail to verify whether "
        "their generated fixes successfully resolved the underlying flaw. RepoGuard overcomes these architectural limitations "
        "by dividing the security workflow into two independent agents governed by a closed-loop Gatekeeper verification engine.")

    add_section_title(doc, "1.8", "Specific Project Objectives")
    add_p(doc,
        "The overarching goal of the RepoGuard project is to design, develop, evaluate, and deploy an autonomous, local-LLM-driven "
        "SAST and automated remediation platform. To achieve this, the project establishes the following specific objectives:", bold_prefix="Primary Aims: ")
    
    add_bullet(doc, "Objective 1: Multi-Agent Architecture Design: ", "Implement a decoupled two-agent paradigm consisting of an Auditor Agent (Agent 1) dedicated exclusively to AST taint analysis and a Fixer Agent (Agent 2) dedicated to surgical code remediation.")
    add_bullet(doc, "Objective 2: Structured Data Contract Enforcement: ", "Establish rigid Pydantic JSON schema validation for all auditor outputs, eliminating unstructured natural language chatter and ensuring seamless programmatic parsing.")
    add_bullet(doc, "Objective 3: False-Positive Suppression: ", "Engineer a comprehensive set of ground-truth exclusion rules that prevent the auditor from flagging compliant defensive coding patterns (parameterized queries, environment variable loading, path boundary checks).")
    add_bullet(doc, "Objective 4: Autonomous Closed-Loop Verification: ", "Construct an iterative Gatekeeper loop that automatically re-audits remediated code up to three convergence passes, guaranteeing verified zero-residual vulnerability states.")
    add_bullet(doc, "Objective 5: Standard Library Remediation Guardrails: ", "Constrain the Fixer Agent to strictly sanctioned standard library primitives (e.g., hashlib.pbkdf2_hmac, list-form subprocess.run, Path.resolve().is_relative_to), eliminating broken external runtime dependencies.")
    add_bullet(doc, "Objective 6: Interactive Developer Telemetry: ", "Deliver an intuitive, high-performance Streamlit dashboard featuring live telemetry metrics, unified Git diff patch visualization, side-by-side comparative inspection, and single-click script export.")

    add_section_title(doc, "1.9", "Scope and Assumptions")
    add_p(doc,
        "The scope of this B.Tech 5th-semester mini project encompasses static application security analysis and remediation "
        "for Python 3 source files. The system is designed to identify and remediate the six most prevalent CWE vulnerability classes: "
        "Hardcoded Secrets (CWE-798), Weak Cryptography & Insecure Hashing (CWE-327/CWE-328), SQL Injection (CWE-89), Path Traversal "
        "(CWE-22), OS Command Injection (CWE-78), and Insecure State Handling via Mutable Default Arguments (CWE-665).")
    add_p(doc,
        "The operational assumptions underlying this implementation include:", bold_prefix="Underlying Assumptions: ")
    add_bullet(doc, "Local Environment: ", "The host machine possesses an active installation of the Ollama model server with the qwen2.5-coder:7b model pulled locally.")
    add_bullet(doc, "Runtime Specs: ", "A minimum hardware configuration of 8 GB RAM and a modern 4-core CPU (or consumer GPU with >=6GB VRAM) for responsive local inference.")
    add_bullet(doc, "Source Code: ", "Target input files consist of syntactically valid Python 3 code.")

    add_section_title(doc, "1.10", "Organization of the Report")
    add_p(doc,
        "The remainder of this mini project report is structured into the following subsequent chapters: "
        "Chapter 2 (Proposed Methodology) details the system architecture, mathematical taint analysis foundations, Pydantic schema contracts, "
        "remediation guardrails, convergence algorithms, and user interface engineering. Chapter 3 (Results and Discussions) presents the "
        "empirical benchmark evaluation across diverse vulnerability classes, comparative performance matrices against traditional tools, "
        "and telemetry observations. Chapter 4 (Conclusion and Future Scope) summarizes the research findings, details engineering learnings, "
        "outlines practical constraints, and charts the development roadmap for future major project expansion.")

    print("Chapter 1 written successfully.")
