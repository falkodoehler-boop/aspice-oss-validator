# ASPICE v4.0 HWE ↔ Open-Source Tool & Standard Mapping

Companion to [`aspice_oss_mapping.md`](aspice_oss_mapping.md) (software side).
This document maps the four **ASPICE v4.0 Hardware Engineering** processes to
open-source / openly-available tooling and to the relevant functional-safety
standard clauses, and points to the validator artifact that produces evidence.

> Scope note: hardware engineering has far less mature OSS tooling than
> software. Where no credible open tool exists, this is stated explicitly
> rather than papered over — the validator artifact (prompt) carries the load.

---

## Process coverage

| Process | Question answered | Validator artifact | Status |
|---|---|---|---|
| **HWE.1** Hardware Requirements Analysis | What must the hardware do? | `prompts/aspice_hwe1_analyzer.md` + `parser/hwe1_to_aspice.py` | ✅ |
| **HWE.2** Hardware Design | How is it architected? | `prompts/aspice_hwe2_analyzer.md` + `parser/hwe_trace_to_aspice.py` | ✅ |
| **HWE.3** Verification against HW Design | Did we build what we designed? | `prompts/aspice_hwe3_analyzer.md` + `parser/hwe_trace_to_aspice.py` | ✅ |
| **HWE.4** Verification against HW Requirements | Did we build what was specified? | `prompts/aspice_hwe4_analyzer.md` + `parser/hwe_trace_to_aspice.py` | ✅ |

> `hwe_trace_to_aspice.py` performs the **deterministic** subset of HWE.2–4
> assurance — allocation orphans, ASIL consistency, element/requirement
> coverage, and fault-injection presence for ASIL C/D — over CSV exports of
> requirements, elements and test cases. The prompts handle the judgement
> that cannot be reduced to ID joins (is a test case *technically adequate*).

---

## HWE.1 — Hardware Requirements Analysis

| Concern | Open-source / open tool | Evidence artifact |
|---|---|---|
| Requirement authoring & traceability | `strictdoc`, `doorstop` | HW Requirements Specification |
| Interchange with ALM (DOORS/Polarion/Codebeamer) | ReqIF (OMG open format) | ReqIF export skeleton |
| Mechanical quality screen (INCOSE subset) | `parser/hwe1_to_aspice.py` (this repo) | INCOSE heuristic matrix |
| Full INCOSE 8-criteria + ISO 26262-5 gating | `aspice_hwe1_analyzer.md` prompt | Graded spec + Action Items |

**Standard hooks:** ISO 26262-5:2018 §6 (HW safety requirements), §6.4.5
(safety mechanism), Table D.1 (diagnostic coverage classes).

---

## HWE.2 — Hardware Design

| Concern | Open-source / open tool | Evidence artifact |
|---|---|---|
| Schematic / PCB capture | KiCad (EDA) | Architectural design, netlist |
| Circuit simulation | ngspice, Qucs-S | Design-parameter validation |
| Interface / architecture docs | `sphinx`, `mkdocs` | Interface specification |
| Trade-off & allocation | `aspice_hwe2_analyzer.md` prompt | Weighted matrix + allocation matrix |

**Standard hooks:** ISO 26262-5 §7 (HW design), single-point-fault avoidance;
FMEDA failure-mode list feeds the verification stage.

---

## HWE.3 — Verification against Hardware Design

| Concern | Open-source / open tool | Evidence artifact |
|---|---|---|
| Bench automation / instrument control | `PyVISA`, `pyvisa-py` | Test execution records |
| Measurement data capture & analysis | `numpy`, `pandas`, `matplotlib` | Coverage plots, captures |
| Thermal / FEM (where applicable) | Elmer FEM, OpenFOAM | Environmental verification |
| Strategy, coverage, fault injection | `aspice_hwe3_analyzer.md` prompt | 3-dimension coverage report |

**Standard hooks:** ISO 26262-5 §8 (HW integration & verification), fault
injection for ASIL C/D; AEC-Q100/Q200 qualification reports.

---

## HWE.4 — Verification against Hardware Requirements

| Concern | Open-source / open tool | Evidence artifact |
|---|---|---|
| Requirement ↔ test traceability | `strictdoc`, `doorstop` | Coverage matrix (must be 100%) |
| Test execution & evidence capture | `PyVISA`, `pandas` | Requirement-level test records |
| Release gating | `aspice_hwe4_analyzer.md` prompt | Release decision record |

**Standard hooks:** ISO 26262-5 Clause 8 (SPFM/LFM, Tables 4-5) and Clause 9
(PMHF, Table 6); OEM acceptance and homologation reports as accredited evidence.

**Architectural metrics (`parser/fmeda_to_aspice.py`):** computes SPFM, LFM and
a PMHF proxy from a per-element FMEDA CSV and gates them against the ASIL target
from `config/review_rules.json`. ASIL D targets: SPFM >= 99 %, LFM >= 90 %,
PMHF < 10 FIT (vs 97 % / 80 % / 100 FIT at ASIL C). The PMHF figure is a
residual single-point proxy — full PMHF (dual-point with exposure/test
intervals, Clause 9 / Annex F) remains a roadmap item (see LL-2026-0008).

**Dependent Failure Analysis:** ASIL decomposition and mixed-ASIL coexistence
require a DFA and a freedom-from-interference argument (ISO 26262-9 §6/§7). The
prompts demand it; it is not yet mechanically checkable (LL-2026-0009).

---

## ASIL traceability cascade (cross-process)

```
HARA → Safety Goal (ASIL X)
  → Functional Safety Requirement (ASIL X)
    → System Requirement [SYS.3] (ASIL X)
      → HW Requirement [HWE.1] (ASIL X; lower only via documented decomposition)
        → HW Element [HWE.2] (ASIL = max ASIL of allocated requirements)
          → Test Case [HWE.3 / HWE.4] (ASIL = ASIL of target item)
```

ASIL decomposition is permitted only per **ISO 26262-9 §5**, with a documented
independence argument. The validator artifacts block silent ASIL downgrade.

---

## Honest gaps

- No mature OSS tool computes FMEDA metrics (PMHF/SPFM/LFM) end-to-end; the
  prompts *link* to FMEDA results, they do not compute them.
- ReqIF round-trip into commercial ALM tools is export-only here; final import
  is a manual step.
- EMC and accelerated-life evidence inherently requires accredited labs — no
  open substitute exists; the artifacts structure the evidence, not produce it.

---

*Part of aspice-oss-validator — extending the OSS compliance bridge from
software (SWE) into hardware (HWE) and ISO 26262-5.*
