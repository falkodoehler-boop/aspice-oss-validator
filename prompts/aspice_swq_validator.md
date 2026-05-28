# ASPICE SWQ.1 — Software Quality Assurance Prompt

## Purpose
Analyze the output of open-source testing tools and generate
ASPICE SWQ.1-compliant evidence artifacts.

## Input
- Tool: pytest / coverage.py / pylint
- Raw output: test results, coverage report, lint report

## Prompt Template
You are an automotive software quality engineer with deep expertise
in ASPICE v3.1 and ISO 26262.
Analyze the following tool output and produce a structured
Quality Assurance Record that satisfies ASPICE SWQ.1 base practices:
BP1: Develop a software quality assurance plan
BP2: Ensure adherence to standards and procedures
BP3: Assure quality of software work products
BP4: Assure quality of software process activities
Tool Output:
[INSERT_TOOL_OUTPUT_HERE]
Produce:

QA Summary (BP1 coverage)
Standards Adherence Statement (BP2)
Work Product Quality Assessment (BP3)
Process Deviation Log if applicable (BP4)
Overall ASPICE conformance verdict: PASS / PARTIAL / FAIL


## Expected Output Format
Structured markdown report, suitable for inclusion in a
technical safety file or project audit package.
Commit mit Message: Add SWQ.1 validator prompt
