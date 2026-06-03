# Lessons Learned Register

Curated, auditable record of real findings, false positives/negatives, and
anomalies observed when applying the validator to actual artifacts. This is the
**learning loop** of the project — deliberately human-curated, not ML-driven,
so that every rule change remains traceable for an ASPICE assessor.

## How the loop works

```
Review / real use  →  anomaly or finding  →  entry in this register
        ↓
   decide the fix:  rule change (config/review_rules.json)
                  | parser code fix
                  | prompt-template change
                  | "won't fix" (documented rationale)
        ↓
   apply, reference the LL-id in the commit and in review_rules.json "lesson_ref"
        ↓
   mark Status = Closed
```

A rule in `config/review_rules.json` should cite the `LL-id` that justified it.
A reviewer can then walk backwards from any heuristic to the evidence for it.

## ID scheme

`LL-<year>-<seq>` — e.g. `LL-2026-0007`.

## Register

| LL-id | Date | Source | Severity | Observation | Resolution | Target | Status |
|---|---|---|---|---|---|---|---|
| LL-2026-0001 | 2026-06-03 | Self-test (phase current sensor) | Low | `derive_domain()` only read the `Source` column, so a "phase current **sensor**" requirement was filed as `GEN` instead of `SEN`. | Combine `Source` + `Statement` for domain inference. | `parser/hwe1_to_aspice.py` | Closed |
| LL-2026-0002 | 2026-06-03 | Self-test (Windows console) | Cosmetic | Em-dash in `print()` rendered as `�` on the Windows console (cp1252). | Use ASCII `-` in stdout; keep Unicode only in file output. | `parser/hwe_trace_to_aspice.py` | Closed |
| LL-2026-0003 | 2026-06-03 | Example raw requirements | Medium | Vague raw lines ("fast enough", "accurate enough") passed structural parsing but are untestable; needed an explicit screen. | Maintain the `vague_terms` / `non_normative_terms` lists in `review_rules.json`; flag as INCOSE `Unambiguous`/`Verifiable`. | `config/review_rules.json` | Closed |
| LL-2026-0004 | 2026-06-03 | Mapping review | Info | No mature OSS tool computes FMEDA metrics (PMHF/SPFM); risk of implying coverage we cannot provide. | State the gap explicitly; add FMEDA hook to roadmap, do not fake it. | `docs/aspice_hwe_mapping.md` | Closed |
| LL-2026-0007 | 2026-06-03 | ASIL-D review | Major | Artifacts were ASIL-aware but did not enforce the ASIL-D architectural-metric targets (SPFM >= 99 %, LFM >= 90 %, PMHF < 10 FIT); a design could pass coverage yet be non-compliant for ASIL D. | Add the per-ASIL metric table to `review_rules.json`; build `fmeda_to_aspice.py` to compute and gate SPFM/LFM/PMHF; make the metrics mandatory (not "if applicable") in the HWE.1/HWE.3 prompts. | `config/review_rules.json`, `parser/fmeda_to_aspice.py`, prompts | Closed |

| LL-2026-0010 | 2026-06-03 | Code review (PR #1) | Major | `coverage_thresholds.element_coverage_min` / `requirement_coverage_min` existed in `review_rules.json` but no parser consumed them — a configured threshold did not bite. | Wire both into `hwe_trace_to_aspice.py`: derive the design ASIL (max), compare element/requirement coverage to the per-ASIL target, raise a finding when below. | `parser/hwe_trace_to_aspice.py` | Closed |
| LL-2026-0011 | 2026-06-03 | Code review (PR #1) | Major | The parsers had no automated tests; verification was manual CLI runs only — ironic for a test-evidence tool. | Add `tests/` with pytest unit tests for all three HWE parsers (PASS cases + regression cases for prior lessons). | `tests/` | Closed |

## Open / candidate lessons

| LL-id | Date | Source | Observation | Proposed action | Status |
|---|---|---|---|---|---|
| LL-2026-0005 | 2026-06-03 | Design review | Heuristic vague-term list is English-only; German requirement sets (e.g. "ausreichend", "geeignet") slip through. | Add a `de` term list to `review_rules.json` and language detection. | Open |
| LL-2026-0006 | 2026-06-03 | Design review | Trace parser treats any `verifies_id` mismatch as a hard finding; partial/redundant allocations may need softer handling. | Evaluate against a real multi-channel (decomposed) design before changing. | Open |
| LL-2026-0008 | 2026-06-03 | ASIL-D review | PMHF is reported as a residual single-point proxy only; full PMHF needs dual-point (latent/detected) contributions with exposure/test intervals (ISO 26262-5 Clause 9 / Annex F). | Extend `fmeda_to_aspice.py` with dual-point inputs, or integrate an external FMEDA tool; keep labelling the proxy until then. | Open |
| LL-2026-0009 | 2026-06-03 | ASIL-D review | Dependent Failure Analysis (DFA) and freedom-from-interference (ISO 26262-9 §6/§7) are referenced in prompts but not mechanically checkable; mixed-ASIL coexistence has no parser support. | Add a DFA/coexistence checklist artifact and consider a parser for documented common-cause initiators. | Open |
| LL-2026-0012 | 2026-06-03 | Code review (PR #1) | `vague_terms` includes "high"/"low", which over-flag legitimate technical phrasing ("high-side driver", "low-ESR"). | Make these context-sensitive (only when standalone) or move to a separate, toggleable list. | Open |
| LL-2026-0013 | 2026-06-03 | Code review (PR #1) | Verifiability heuristic accepts any digit, so "comply with ISO 26262" passes falsely. | Require a unit or comparison operator near the number, not just any digit. | Open |

## Contribution note

When you hit a real-world finding, add a row before changing any rule. The
register entry is the audit evidence; the code/config change is the remediation.
A change to a heuristic without a matching `LL-id` should be rejected in review.
