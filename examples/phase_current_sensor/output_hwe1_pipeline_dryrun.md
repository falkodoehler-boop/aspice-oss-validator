<!-- aspice-oss-validator pipeline | 2026-06-09T07:00:07+00:00 | DRY-RUN — no API call; prompt + deterministic pre-pass only -->
> **Provenance:** DRY-RUN — no API call; prompt + deterministic pre-pass only. Deterministic pre-pass: `parser/hwe1_to_aspice.py`.

## DRY-RUN: assembled prompt (not sent)

### System (durable instructions, abbreviated)

# ASPICE HWE.1 — Hardware Requirements Analysis Prompt

## Purpose
Analyze raw hardware requirement inputs (DOORS/ReqIF exports, CSV tables,
or plain-text specifications) and generate **ASPICE v4.0 HWE.1**-compliant
Hardware Requirements Specification artifacts, with INCOSE requirements
quality checks and ISO 26262-5 functional-safety constraints applied.

This is the hardware-engineering counterpart to `aspice_swq_validator.md`.
Where the SWQ prompt validates *software* tool output, this prompt structures,
analyzes, and quality-gates *hardware* requirements.

## Input
- Source: HARA-derived safety goal / system requirement (SYS.3 allocation),
  or an existing draft hardware requirement set
- Raw input: requirement statements in any of:
  - ReqIF `Object Text` + attributes
  - CSV / table (columns: ID, Statement, Rationale, ASIL, Source)
  - Plain-text or Markdown requirement list

## Prompt Template

You are an automotive hardware requirements engineer with deep expertise in
ASPICE v4.0 Hardware Engineering (HWE.1), INCOSE/IREB requirements quality
criteria, and ISO 26262-5:2018 functional safety.

Analyze the following hardware requirement input and produce a structured
Hardware

[... full template in prompts/aspice_hwe1_analyzer.md ...]

### User (per-run input)

```
Analyze this hardware requirement input under the rules above.

Safety goal / source:  SG-INV-002
Target ASIL:           D

Raw requirement input (CSV-derived, plus the deterministic pre-pass already computed by the guardrail — do NOT re-derive the mechanical findings; focus on the criteria the guardrail cannot check: Necessary, Feasible, Implementation-free, full Completeness, and the ISO 26262-5 graded analysis):

ID,Statement,Rationale,ASIL,Source
RAW-001,Sensor must measure phase current up to plus/minus 400 A,Close the torque control loop on peak phase current,D,SG-INV-002
RAW-002,Sensor must be accurate enough to detect uncontrolled torque,Detect fault before torque exceeds 20 Nm,D,SG-INV-002
RAW-003,Sensor must be fast enough for the inverter control loop,Control loop bandwidth needs headroom,D,SG-INV-002
RAW-004,Sensor must isolate HV from LV side,DC-link is 400-800 V,D,SG-INV-002
RAW-005,Sensor must detect its own failures and report them,ASIL D needs a safety mechanism,D,"SG-INV-002, ISO 26262-5"
RAW-006,Sensor must reach the required diagnostic coverage,Meet SPFM target for ASIL D,D,ISO 26262-5
RAW-007,Sensor runs from the control-unit 5 V rail,Standard analog reference rail,D,SYS-REQ-PWR-003
RAW-008,Sensor must work across the powertrain temperature range,Powertrain-near mounting position,D,SYS-REQ-ENV-001

MECHANICAL PRE-PASS (deterministic, from parser/hwe1_to_aspice.py — treat as established fact, do not re-derive):
- requirements: 8  | clean: 2  | flagged: 6  | safety-relevant (ASIL A-D): 8
- mechanical verdict: FAIL
- per-requirement mechanical findings:
    HW-REQ-SEN-001 (raw RAW-001, ASIL D): none
    HW-REQ-SEN-002 (raw RAW-002, ASIL D): Unambiguous: vague term 'enough' — quantify it; Verifiable: no numeric value/unit — likely untestable
    HW-REQ-SEN-003 (raw RAW-003, ASIL D): Unambiguous: vague term 'fast' — quantify it; Verifiable: no numeric value/unit — likely untestable
    HW-REQ-SEN-004 (raw RAW-004, ASIL D): Verifiable: no numeric value/unit — likely untestable
    HW-REQ-SEN-005 (raw RAW-005, ASIL D): Singular: conjunction present — consider splitting; Verifiable: no numeric value/unit — likely untestable
    HW-REQ-SEN-006 (raw RAW-006, ASIL D): Verifiable: no numeric value/unit — likely untestable
    HW-REQ-SEN-007 (raw RAW-007, ASIL D): none
    HW-REQ-SEN-008 (raw RAW-008, ASIL D): Verifiable: no numeric value/unit — likely untestable

```

