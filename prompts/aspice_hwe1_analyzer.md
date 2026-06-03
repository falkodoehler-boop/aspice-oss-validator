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
Hardware Requirements Specification that satisfies ASPICE v4.0 HWE.1
base practices:

  BP1: Specify hardware requirements (atomic, one capability per statement)
  BP2: Structure hardware requirements (by domain and by ASIL)
  BP3: Analyze hardware requirements (quality, feasibility, testability)
  BP4: Analyze impact on the operating environment
  BP5: Ensure consistency and bidirectional traceability
  BP6: Communicate agreed hardware requirements

Safety goal / source:  [INSERT_SAFETY_GOAL_OR_SOURCE]
Target ASIL:           [INSERT_ASIL — QM | A | B | C | D]
Raw requirement input: [INSERT_REQUIREMENT_INPUT_HERE]

For EACH requirement, produce a record in this structure:

  ID:      HW-REQ-<domain>-<seq>
  Status:  Draft
  ASIL:    <inherited from source; never silently downgraded>
  Source:  <upstream artifact ID>
  Type:    <Functional | Performance | Interface | Environmental | Safety | Reliability>
  Statement:           The <subject> shall <action> <object> <constraint>.
  Rationale:           <1-3 sentences>
  Acceptance Criteria: <measurable, individually verifiable bullets>
  Verification method: <Test | Analysis | Inspection | Demonstration | Simulation>
  Verification level:  <Component | Module | Integration | System>
  Traceability:        Upward <source>, Downward TBD (HWE.2), Test TBD (HWE.4)

Then apply the INCOSE 8-criteria quality check to every requirement
(Unambiguous, Complete, Singular, Feasible, Verifiable, Conforming,
Necessary, Implementation-free) and report Pass / Partial / Fail per
requirement with the specific finding for any non-pass.

For any ASIL A–D requirement, apply ISO 26262-5 constraints:
  - Reference the originating safety goal / TSC with a trace ID
  - Specify a safety mechanism (ISO 26262-5 §6.4.5)
  - State the Diagnostic Coverage (DC) target where required
  - Reference the PMHF / FIT budget if applicable
  - Document any ASIL decomposition (ISO 26262-9 §5) explicitly

Produce:

  1. Hardware Requirements Specification (all requirement records)
  2. INCOSE 8-criteria quality matrix
  3. ASIL inheritance / decomposition statement
  4. Open Action Items (any release-blocking gaps, e.g. missing k_T, FIT budget)
  5. Overall ASPICE HWE.1 conformance verdict: PASS / PARTIAL / FAIL

## Behavioral Rules
- Never fabricate an ASIL. If the target ASIL is unknown, STOP and demand the
  HARA / safety-goal reference.
- Never silently downgrade ASIL — decomposition must be documented with an
  independence argument.
- Reject "should" in normative statements; require "shall".
- Block any safety-relevant requirement that lacks an acceptance criterion,
  a verification method, or an ASIL tag.
- Flag — do not invent — missing numeric inputs (e.g. torque constant k_T,
  PMHF budget) as explicit Action Items.

## Expected Output Format
Structured Markdown specification, suitable for direct inclusion in a
technical safety file, a DOORS/Polarion/Codebeamer import (via ReqIF), or
an ASPICE assessment package. Close with an explicit confidence statement:
High / Moderate / Low / Unknown, with the reason.
