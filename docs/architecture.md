# Architecture — the deterministic-guardrail-around-Claude pattern

The hard problem in a compliance tool is not "call an LLM." It is: **how do you use
a probabilistic model to produce evidence an ISO 26262 assessor will accept?** An
assessor rejects two things instantly — hallucinated facts, and non-reproducible
results. So the architecture is built to keep the model away from both.

## The split

```
                 raw engineering input (CSV / ReqIF / table)
                                   │
                 ┌─────────────────▼─────────────────┐
                 │  DETERMINISTIC GUARDRAIL (parser/) │   reproducible, never
                 │  IDs · mechanical INCOSE subset ·  │   hallucinated; this is
                 │  FMEDA SPFM/LFM/PMHF vs ASIL gate   │   the audit baseline
                 └─────────────────┬─────────────────┘
                                   │  pre-pass findings injected as established fact
                 ┌─────────────────▼─────────────────┐
                 │  CLAUDE (prompts/ via pipeline)    │   judgement the guardrail
                 │  Necessary · Feasible ·            │   provably cannot do:
                 │  Implementation-free · Completeness │   reasoning over intent
                 │  · ISO 26262-5 graded analysis      │
                 └─────────────────┬─────────────────┘
                                   │
                 audit-ready artifact (+ provenance: model, tokens, pre-pass source)
```

**The guardrail owns what must be exact.** Requirement IDs, numeric/unit checks,
the PASS/PARTIAL/FAIL verdict, and the architectural-metric gate (SPFM ≥ 99 % /
LFM ≥ 90 % / PMHF < 10 FIT for ASIL D) are computed in plain Python. They are
identical on every run and cite no model. If an assessor asks "where did this
number come from," the answer is a deterministic function, not a generation.

**Claude owns what needs reasoning.** Whether a requirement is *Necessary*,
*Feasible*, or *Implementation-free*, and the ISO 26262-5 graded analysis, require
reading intent — exactly where a heuristic fails and an LLM excels. The guardrail's
findings are injected into the prompt as established fact, so Claude does not
re-derive them: the call is cheaper, more focused, and cannot contradict the
deterministic baseline.

## Why this is the right shape for an LLM in compliance

| Risk in a naive "LLM does everything" tool | How the split removes it |
|---|---|
| Hallucinated metric / ID | Metrics and IDs never leave the deterministic layer |
| Non-reproducible evidence | The audit baseline is a pure function; Claude adds analysis on top, provenance-stamped |
| Unbounded token cost | The pre-pass shrinks and focuses the prompt; mechanical findings are not re-litigated |
| "Which model produced this?" | Every artifact carries a provenance header (model id + token usage) |

## Honest reproducibility: `--dry-run`

The pipeline runs end-to-end with **no API key and no tokens**: `--dry-run` (and the
automatic no-key fallback) emit the fully assembled prompt plus the deterministic
pre-pass. Anyone — including an evaluator — can reproduce exactly what would be sent
to Claude for free, then run it live when they want the analysis. The deterministic
verdict is available either way.

## Model policy

| Use | Model id | Rationale |
|---|---|---|
| Default analysis | `claude-sonnet-4-6` | best cost/quality for requirement-level analysis |
| ASIL C/D sign-off material | `claude-opus-4-8` | highest-stakes reasoning; cost is negligible vs. rework |

The model id is a CLI flag and is recorded in every artifact's provenance header.

## Where the pieces live

```
src/aspice_validator/
  client.py     # lazy Anthropic SDK wrapper; model + token budget explicit
  prompts.py    # loads prompts/ templates, binds placeholders (single audit point)
  guardrail.py  # wraps parser/ — the deterministic pre-pass
  pipeline.py   # guardrail -> Claude -> artifact, with honest dry-run
  cli.py        # `aspice-validate hwe1 ...`
parser/         # deterministic, dependency-free; the audit baseline
prompts/        # the version-controlled spec (see prompt_engineering_methodology.md)
```
