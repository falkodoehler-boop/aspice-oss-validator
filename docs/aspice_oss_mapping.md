# ASPICE ↔ Open-Source Tool Mapping

This document maps ASPICE v3.1 Software Engineering process areas
to open-source tools that can provide compliant evidence artifacts
when used together with aspice-oss-validator.

---

## SWE.1 — Software Requirements Analysis

| ASPICE BP | Evidence Required | OSS Tool | Validator Support |
|-----------|-------------------|----------|-------------------|
| BP1 — Establish software requirements | Requirements list with attributes | `doors-ng-oss`, `strictdoc` | Prompt: planned |
| BP2 — Allocate to components | Traceability matrix | `strictdoc` | Prompt: planned |
| BP3 — Evaluate requirements | Review records | Manual + LLM | Prompt: `aspice_swa_analyzer.md` |
| BP4 — Define criteria for acceptance | Acceptance test spec | `pytest` | Parser: `pytest_to_aspice.py` |

---

## SWE.2 — Software Architectural Design

| ASPICE BP | Evidence Required | OSS Tool | Validator Support |
|-----------|-------------------|----------|-------------------|
| BP1 — Develop architectural design | Architecture document | `sphinx`, `mkdocs` | Prompt: `aspice_swa_analyzer.md` |
| BP2 — Allocate requirements | Allocation table | `strictdoc` | Prompt: `aspice_swa_analyzer.md` |
| BP3 — Define interfaces | Interface control document | `pydantic`, docstrings | Prompt: `aspice_swa_analyzer.md` |
| BP6 — Establish traceability | Traceability matrix | `strictdoc` | Prompt: `aspice_swa_analyzer.md` |

---

## SWE.4 — Software Unit Verification

| ASPICE BP | Evidence Required | OSS Tool | Validator Support |
|-----------|-------------------|----------|-------------------|
| BP1 — Develop unit verification plan | Test plan document | `pytest` | Prompt: planned |
| BP2 — Select verification criteria | Coverage thresholds | `coverage.py` | Parser: planned |
| BP3 — Perform unit verification | Test execution records | `pytest` | Parser: `pytest_to_aspice.py` |
| BP4 — Evaluate verification results | Pass/fail evidence | `pytest` + `pylint` | Parser: `pytest_to_aspice.py` |

---

## SWE.5 — Software Integration and Integration Test

| ASPICE BP | Evidence Required | OSS Tool | Validator Support |
|-----------|-------------------|----------|-------------------|
| BP1 — Develop integration test plan | Integration test spec | `pytest` | Prompt: planned |
| BP3 — Perform integration test | Test execution records | `pytest` | Parser: `pytest_to_aspice.py` |
| BP5 — Ensure consistency | Traceability | `strictdoc` | Prompt: planned |

---

## SWE.6 — Software Qualification Test

| ASPICE BP | Evidence Required | OSS Tool | Validator Support |
|-----------|-------------------|----------|-------------------|
| BP1 — Develop qualification test spec | Test specification | `pytest` | Prompt: planned |
| BP3 — Perform qualification test | Test execution records | `pytest` | Parser: `pytest_to_aspice.py` |
| BP4 — Evaluate test results | QA evidence record | `pytest` + `coverage.py` | Parser: `pytest_to_aspice.py` |

---

## SUP.1 — Quality Assurance

| ASPICE BP | Evidence Required | OSS Tool | Validator Support |
|-----------|-------------------|----------|-------------------|
| BP1 — Develop QA plan | QA plan document | Manual | Prompt: planned |
| BP2 — Ensure adherence | Audit records | `pylint`, `flake8` | Prompt: `aspice_swq_validator.md` |
| BP3 — Assure work product quality | QA evidence record | `pytest` | Parser: `pytest_to_aspice.py` |
| BP4 — Assure process quality | Deviation log | `pytest` | Parser: `pytest_to_aspice.py` |

---

## Roadmap

- [ ] coverage.py → ASPICE SWE.4 BP2 parser
- [ ] pylint → SUP.1 BP2 parser  
- [ ] strictdoc → SWE.1 traceability prompt
- [ ] GitHub Actions workflow: full ASPICE evidence pipeline
- [ ] ISO 26262 Part 6 mapping table

---

*Maintained by aspice-oss-validator — contributions welcome.*

Commit Message: Add ASPICE-to-OSS mapping documentation
