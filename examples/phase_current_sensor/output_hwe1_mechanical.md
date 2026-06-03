# ASPICE v4.0 HWE.1 — Hardware Requirements Specification (draft)

**Generated:** 2026-06-03T12:00:28
**Tool:** hwe1_to_aspice.py (mechanical pass — INCOSE heuristics only)

> This is a structural skeleton. The mechanical INCOSE subset is checked
> here; Necessary / Feasible / Implementation-free / full Completeness
> require the `aspice_hwe1_analyzer.md` prompt or a human reviewer.

## Summary
| Metric | Value |
|--------|-------|
| Requirements | 8 |
| Pass (no heuristic finding) | 2 |
| Partial (>=1 finding) | 6 |
| Safety-relevant (ASIL A-D) | 8 |

**Mechanical verdict:** `FAIL`

## Requirements

### HW-REQ-SEN-001  (from raw `RAW-001`)
```
ID:      HW-REQ-SEN-001
Status:  Draft
ASIL:    C
Source:  SG-INV-002

Statement:
  Sensor must measure phase current up to plus/minus 400 A

Rationale:
  Close the torque control loop on peak phase current

Acceptance Criteria:
  - TODO (reviewer/prompt): add measurable criteria
Verification method:   TODO
Verification level:    Component
Traceability:          Upward SG-INV-002; Downward TBD (HWE.2); Test TBD (HWE.4)
```

**INCOSE:** Pass (mechanical heuristics)

### HW-REQ-SEN-002  (from raw `RAW-002`)
```
ID:      HW-REQ-SEN-002
Status:  Draft
ASIL:    C
Source:  SG-INV-002

Statement:
  Sensor must be accurate enough to detect uncontrolled torque

Rationale:
  Detect fault before torque exceeds 20 Nm

Acceptance Criteria:
  - TODO (reviewer/prompt): add measurable criteria
Verification method:   TODO
Verification level:    Component
Traceability:          Upward SG-INV-002; Downward TBD (HWE.2); Test TBD (HWE.4)
```

**INCOSE findings (Partial):**
- `Unambiguous` — vague term 'enough' — quantify it
- `Verifiable` — no numeric value/unit — likely untestable

### HW-REQ-SEN-003  (from raw `RAW-003`)
```
ID:      HW-REQ-SEN-003
Status:  Draft
ASIL:    C
Source:  SG-INV-002

Statement:
  Sensor must be fast enough for the inverter control loop

Rationale:
  Control loop bandwidth needs headroom

Acceptance Criteria:
  - TODO (reviewer/prompt): add measurable criteria
Verification method:   TODO
Verification level:    Component
Traceability:          Upward SG-INV-002; Downward TBD (HWE.2); Test TBD (HWE.4)
```

**INCOSE findings (Partial):**
- `Unambiguous` — vague term 'fast' — quantify it
- `Verifiable` — no numeric value/unit — likely untestable

### HW-REQ-SEN-004  (from raw `RAW-004`)
```
ID:      HW-REQ-SEN-004
Status:  Draft
ASIL:    C
Source:  SG-INV-002

Statement:
  Sensor must isolate HV from LV side

Rationale:
  DC-link is 400-800 V

Acceptance Criteria:
  - TODO (reviewer/prompt): add measurable criteria
Verification method:   TODO
Verification level:    Component
Traceability:          Upward SG-INV-002; Downward TBD (HWE.2); Test TBD (HWE.4)
```

**INCOSE findings (Partial):**
- `Verifiable` — no numeric value/unit — likely untestable

### HW-REQ-SEN-005  (from raw `RAW-005`)
```
ID:      HW-REQ-SEN-005
Status:  Draft
ASIL:    C
Source:  SG-INV-002, ISO 26262-5

Statement:
  Sensor must detect its own failures and report them

Rationale:
  ASIL C needs a safety mechanism

Acceptance Criteria:
  - TODO (reviewer/prompt): add measurable criteria
Verification method:   TODO
Verification level:    Component
Traceability:          Upward SG-INV-002, ISO 26262-5; Downward TBD (HWE.2); Test TBD (HWE.4)
```

**INCOSE findings (Partial):**
- `Singular` — conjunction present — consider splitting
- `Verifiable` — no numeric value/unit — likely untestable

### HW-REQ-SEN-006  (from raw `RAW-006`)
```
ID:      HW-REQ-SEN-006
Status:  Draft
ASIL:    C
Source:  ISO 26262-5

Statement:
  Sensor must reach the required diagnostic coverage

Rationale:
  Meet SPFM target for ASIL C

Acceptance Criteria:
  - TODO (reviewer/prompt): add measurable criteria
Verification method:   TODO
Verification level:    Component
Traceability:          Upward ISO 26262-5; Downward TBD (HWE.2); Test TBD (HWE.4)
```

**INCOSE findings (Partial):**
- `Verifiable` — no numeric value/unit — likely untestable

### HW-REQ-SEN-007  (from raw `RAW-007`)
```
ID:      HW-REQ-SEN-007
Status:  Draft
ASIL:    C
Source:  SYS-REQ-PWR-003

Statement:
  Sensor runs from the control-unit 5 V rail

Rationale:
  Standard analog reference rail

Acceptance Criteria:
  - TODO (reviewer/prompt): add measurable criteria
Verification method:   TODO
Verification level:    Component
Traceability:          Upward SYS-REQ-PWR-003; Downward TBD (HWE.2); Test TBD (HWE.4)
```

**INCOSE:** Pass (mechanical heuristics)

### HW-REQ-SEN-008  (from raw `RAW-008`)
```
ID:      HW-REQ-SEN-008
Status:  Draft
ASIL:    C
Source:  SYS-REQ-ENV-001

Statement:
  Sensor must work across the powertrain temperature range

Rationale:
  Powertrain-near mounting position

Acceptance Criteria:
  - TODO (reviewer/prompt): add measurable criteria
Verification method:   TODO
Verification level:    Component
Traceability:          Upward SYS-REQ-ENV-001; Downward TBD (HWE.2); Test TBD (HWE.4)
```

**INCOSE findings (Partial):**
- `Verifiable` — no numeric value/unit — likely untestable

## INCOSE heuristic matrix

| Requirement | Result | Findings |
|---|---|---|
| HW-REQ-SEN-001 | Pass | — |
| HW-REQ-SEN-002 | Partial | Unambiguous; Verifiable |
| HW-REQ-SEN-003 | Partial | Unambiguous; Verifiable |
| HW-REQ-SEN-004 | Partial | Verifiable |
| HW-REQ-SEN-005 | Partial | Singular; Verifiable |
| HW-REQ-SEN-006 | Partial | Verifiable |
| HW-REQ-SEN-007 | Pass | — |
| HW-REQ-SEN-008 | Partial | Verifiable |

---
*Generated by aspice-oss-validator — https://github.com/falkodoehler-boop/aspice-oss-validator*