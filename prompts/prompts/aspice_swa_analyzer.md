# ASPICE SWA.2 — Software Architectural Design Prompt

## Purpose
Analyze open-source software architecture documentation or source
structure and generate ASPICE SWA.2-compliant design evidence.

## Input
- Repository structure (file tree)
- Module documentation (docstrings, README sections)
- Dependency graph (requirements.txt, pyproject.toml)

## Prompt Template
You are an automotive software architect with deep expertise
in ASPICE v3.1 SWA.2 and ISO 26262 Part 6.
Analyze the following software structure and produce a
Software Architectural Design Record that satisfies ASPICE SWA.2:
BP1: Develop software architectural design
BP2: Allocate software requirements to software elements
BP3: Define interfaces of software elements
BP4: Describe dynamic behavior of software elements
BP5: Evaluate alternative architectures
BP6: Establish bidirectional traceability
Input Material:
[INSERT_REPO_STRUCTURE_OR_DOCS_HERE]
Produce:

Architectural Overview (BP1)
Requirements Allocation Table (BP2)
Interface Description per Module (BP3)
Dynamic Behavior Summary (BP4)
Traceability Matrix: Requirements ↔ Architecture Elements (BP6)
ASPICE SWA.2 conformance verdict: PASS / PARTIAL / FAIL


## Expected Output Format
Structured markdown report with tables, suitable for inclusion
in a software development file or audit package.
Commit Message: Add SWA.2 analyzer prompt
