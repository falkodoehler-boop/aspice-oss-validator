# Example — Phase Current Sensor (HWE.1)

End-to-end HWE.1 example: a phase current sensor for a drive inverter,
range ±400 A, **ASIL C**, derived from a fictional safety goal
**SG-INV-002** (*protection against uncontrolled torque > 20 Nm in the
fault case*).

## Files

| File | Role |
|---|---|
| [`input_requirements.csv`](input_requirements.csv) | Raw, unstructured requirement input (the kind exported from a draft sheet) |
| [`output_hwe1_spec.md`](output_hwe1_spec.md) | ASPICE v4.0 HWE.1 specification produced from the input |

## How it was produced

The raw CSV was fed through the [`aspice_hwe1_analyzer.md`](../../prompts/aspice_hwe1_analyzer.md)
prompt. The prompt:

1. Structured 8 raw lines into atomic HW-REQ records (ID, ASIL, statement,
   acceptance criteria, verification method, traceability).
2. Applied the **INCOSE 8-criteria** quality check — flagging 3 requirements
   as *Partial*.
3. Applied **ISO 26262-5** constraints — a safety mechanism (§6.4.5) and a
   diagnostic-coverage target (Table D.1) for the ASIL C sensor.
4. Surfaced 5 **release-blocking Action Items** instead of inventing missing
   numbers (e.g. the torque constant k_T and the PMHF/FIT budget).

## What this demonstrates

- The validator pattern extends cleanly from **software** (pytest → SWQ.1)
  to **hardware** (raw requirements → HWE.1).
- Missing safety inputs are **flagged, not fabricated** — the artifact is
  honest about what blocks release.
- The same spec is the input to the downstream HWE.2 → HWE.3 → HWE.4 prompts.
