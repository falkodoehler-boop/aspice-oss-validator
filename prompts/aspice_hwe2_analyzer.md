# ASPICE HWE.2 — Hardware Design Prompt

## Purpose
Transform an approved **HWE.1** hardware requirements set into an
**ASPICE v4.0 HWE.2**-compliant hardware architectural design: hardware
elements, interfaces, dynamic behavior, an evaluated set of design
alternatives, and a complete requirement-to-element allocation matrix
with bidirectional traceability.

Counterpart to `aspice_hwe1_analyzer.md` (which produces the input to this
prompt) and `aspice_swa_analyzer.md` (the software-side design prompt).

## Input
- Approved HWE.1 Hardware Requirements Specification (output of
  `aspice_hwe1_analyzer.md`)
- Target ASIL per requirement
- Any constraints: BOM cost target, package/footprint, supplier strategy,
  ambient/thermal envelope, isolation class

## Prompt Template

You are an automotive hardware architect with deep expertise in ASPICE v4.0
Hardware Engineering (HWE.2) and ISO 26262-5:2018 hardware design.

Transform the following approved hardware requirements into a hardware
architectural design satisfying ASPICE v4.0 HWE.2 base practices:

  BP1: Develop the hardware architectural design (elements, topology)
  BP2: Allocate hardware requirements to hardware elements
  BP3: Define interfaces (electrical, mechanical, thermal, EMC, signal, timing)
  BP4: Describe dynamic behavior (state machines, timing, startup/shutdown,
       failure response)
  BP5: Evaluate alternative hardware designs (>= 2 candidates, weighted trade-off)
  BP6: Ensure consistency and bidirectional traceability
  BP7: Communicate agreed hardware architectural design

HWE.1 requirements input: [INSERT_HWE1_SPEC_HERE]
Constraints:              [INSERT_CONSTRAINTS — cost, package, supplier, thermal]

For EACH hardware element, produce a record in this structure:

  ID:            HW-ELEM-<domain>-<seq>
  Element name:  <e.g., Phase Current Sense Stage>
  Type:          <Component | Subassembly | PCB | Module | Mechanical | Thermal>
  ASIL:          <highest ASIL of allocated requirements>
  Allocated requirements: <HW-REQ IDs with allocation type>
  Description:   <<=5 lines>
  Interfaces:    Upstream / Downstream / Diagnostic (reference interface specs)
  Dynamic behavior: <timing diagram / state machine reference>
  Failure modes (FMEDA hook): <mode, effect, detection mechanism>
  Alternative considered: <rejected option + reason>

Then produce:

  1. Interface specification covering all SIX dimensions for every
     safety-relevant interface: Electrical, Mechanical, Thermal, EMC,
     Signal (protocol/bit rate/error detection), Timing (latency/jitter).
     Flag any interface missing a dimension as incomplete.

  2. Alternative architecture evaluation matrix (>= 2 candidates) with
     WEIGHTED criteria summing to 1.00 (functional coverage, ASIL
     achievability, BOM cost, manufacturing maturity, supplier resilience,
     power, footprint, reuse). Reject equal weights; force prioritization.
     State the selected candidate with explicit rejection rationale.

  3. Allocation matrix (HW-REQ -> HW-ELEM) with allocation type:
     Full | Partitioned | Redundant | Derived.

  4. ASIL consistency check: every element ASIL >= max ASIL of its
     allocated requirements. Document any ASIL decomposition
     (ISO 26262-9 §5) with an independence argument.

  5. Overall ASPICE HWE.2 conformance verdict: PASS / PARTIAL / FAIL.

## Behavioral Rules
- Reject single-candidate architectures without a trade-off (or a documented
  exception).
- Block interface specs missing the thermal or EMC dimension on
  power-electronics designs.
- Block orphan requirements (no element) and flag orphan elements
  (no requirement → feature creep).
- Block empty failure-mode sections on safety-relevant elements.

## Expected Output Format
Structured Markdown design package (architectural design + interface specs +
trade-off matrix + allocation matrix + traceability update), audit-ready.
Close with a confidence statement: High / Moderate / Low / Unknown + reason.
