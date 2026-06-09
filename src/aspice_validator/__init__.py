"""aspice_validator — Claude-native ASPICE/ISO 26262 compliance pipeline.

The package turns the prompt templates in ``prompts/`` into a runnable pipeline:

    raw engineering input
        -> deterministic guardrail (mechanical INCOSE/metric pre-pass)
        -> Claude (judgement-heavy analysis the guardrail cannot do)
        -> audit-ready compliance artifact

The deterministic layer (``parser/``) owns everything that must never be
hallucinated (IDs, numeric checks, FMEDA metrics). Claude owns the analysis that
needs reasoning (Necessary / Feasible / Implementation-free, ISO 26262 grading).
That separation is the whole point — see ``docs/architecture.md``.
"""

__version__ = "0.1.0"

from .pipeline import PipelineResult, run_hwe1  # noqa: E402,F401
