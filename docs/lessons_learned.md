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

## Open / candidate lessons

| LL-id | Date | Source | Observation | Proposed action | Status |
|---|---|---|---|---|---|
| LL-2026-0005 | 2026-06-03 | Design review | Heuristic vague-term list is English-only; German requirement sets (e.g. "ausreichend", "geeignet") slip through. | Add a `de` term list to `review_rules.json` and language detection. | Open |
| LL-2026-0006 | 2026-06-03 | Design review | Trace parser treats any `verifies_id` mismatch as a hard finding; partial/redundant allocations may need softer handling. | Evaluate against a real multi-channel (decomposed) design before changing. | Open |

## Contribution note

When you hit a real-world finding, add a row before changing any rule. The
register entry is the audit evidence; the code/config change is the remediation.
A change to a heuristic without a matching `LL-id` should be rejected in review.
