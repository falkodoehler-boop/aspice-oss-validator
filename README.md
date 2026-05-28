# aspice-oss-validator

**AI-powered compliance bridge for open-source tools in regulated automotive environments.**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![ASPICE](https://img.shields.io/badge/ASPICE-v3.1%20%2F%20v4.0-green.svg)]()
[![ISO 26262](https://img.shields.io/badge/ISO%2026262-Part%206-orange.svg)]()

---

## The Problem

Automotive OEMs and Tier-1 suppliers want to use open-source tools —
pytest, coverage.py, pylint, strictdoc — but cannot.

Not because the tools are technically insufficient.
Because they produce no compliant evidence artifacts.

No ASPICE work product mapping. No safety argumentation. No traceability.
Quality and legal teams block adoption. Projects fall back to expensive
proprietary toolchains.

**This repository is the missing compliance layer.**

---

## What This Does

`aspice-oss-validator` provides:

- **AI Prompts** — Structured prompt templates that analyze OSS tool output
  and generate ASPICE-compliant work products (SWA, SWI, SWQ, SWV)
- **Parsers** — Python modules that map pytest, coverage.py, and pylint
  results to ASPICE base practices with structured evidence records
- **Mapping Tables** — Normative documentation linking ASPICE process areas
  to open-source tools and their evidence artifacts
- **Examples** — End-to-end examples showing raw tool output transformed
  into audit-ready compliance records

---

## Repository Structure
aspice-oss-validator/
├── prompts/
│   ├── aspice_swq_validator.md      # SWQ.1 Quality Assurance prompt
│   └── aspice_swa_analyzer.md       # SWA.2 Architectural Design prompt
├── parser/
│   └── pytest_to_aspice.py          # pytest JSON → ASPICE SWQ.1 evidence
├── docs/
│   └── aspice_oss_mapping.md        # ASPICE BP ↔ OSS tool mapping table
└── examples/
└── example_evidence_output.md   # End-to-end example

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/falkodoehler-boop/aspice-oss-validator
cd aspice-oss-validator

# Install pytest JSON report plugin
pip install pytest-json-report

# Run your test suite
pytest --json-report --json-report-file=report.json

# Generate ASPICE SWQ.1 evidence record
python parser/pytest_to_aspice.py report.json

# Output: aspice_swq_evidence.md — ready for audit package
```

---

## ASPICE Coverage

| Process Area | BP Coverage | Status |
|---|---|---|
| SWE.2 — Software Architectural Design | BP1, BP2, BP3, BP6 | ✅ Prompt available |
| SWE.4 — Software Unit Verification | BP1, BP3, BP4 | ✅ Parser + Prompt |
| SWE.6 — Software Qualification Test | BP1, BP3, BP4 | ✅ Parser available |
| SUP.1 — Quality Assurance | BP2, BP3, BP4 | ✅ Parser + Prompt |
| SWE.1 — Software Requirements Analysis | BP1, BP2, BP4 | 🔄 In progress |
| SWE.5 — Software Integration Test | BP1, BP3, BP5 | 🔄 In progress |

---

## Who This Is For

- **Automotive software teams** evaluating open-source tools for regulated projects
- **Safety managers** needing evidence artifacts for ISO 26262 assessments
- **ASPICE assessors** reviewing tool qualification documentation
- **Open-source maintainers** wanting their tools adopted in automotive contexts

---

## Roadmap

- [ ] coverage.py → ASPICE SWE.4 BP2 parser
- [ ] pylint → SUP.1 BP2 parser
- [ ] strictdoc → SWE.1 traceability prompt
- [ ] GitHub Actions workflow: automated full ASPICE evidence pipeline
- [ ] ISO 26262 Part 6 mapping table
- [ ] Web interface for evidence generation

---

## Background

The automotive industry operates under hard regulatory requirements —
ASPICE v3.1/v4.0 and ISO 26262 — that define exactly what evidence
must exist for every software work product.

Open-source tools are technically capable. The compliance documentation
is not. This repository exists to close that gap systematically,
using AI-assisted analysis and structured prompt engineering.

---

## Contributing

Contributions welcome — especially from:
- Automotive engineers with ASPICE assessment experience
- Open-source maintainers of tools used in safety-critical contexts
- Safety managers with documentation requirements to share

Please open an issue before submitting large PRs.

---

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

---

*If your team is trying to get open-source tools past a safety audit,
open an issue. That's exactly what this project exists for.*
Commit Message: Update README with full project documentation
