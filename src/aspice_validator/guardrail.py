"""Deterministic guardrail layer.

Wraps the stdlib-only parsers in ``parser/`` so the pipeline can run the
mechanical pre-pass *before* spending any tokens. Everything here is
reproducible and never hallucinated: requirement IDs, the mechanical INCOSE
subset, the PASS/PARTIAL/FAIL verdict. Claude is then asked to do only the part
this layer provably cannot.
"""

from __future__ import annotations

import os
import sys

# The deterministic parsers intentionally remain a dependency-free, script-style
# module set in parser/. Make them importable without packaging them.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_PARSER_DIR = os.path.join(_REPO_ROOT, "parser")
if _PARSER_DIR not in sys.path:
    sys.path.insert(0, _PARSER_DIR)

import hwe1_to_aspice as _hwe1  # noqa: E402


def hwe1_prepass(csv_path: str, config: str | None = None) -> dict:
    """Run the deterministic HWE.1 INCOSE screen. Returns the parser's data dict."""
    if config:
        _hwe1.load_rules(config)
    rows = _hwe1.load_rows(csv_path)
    if not rows:
        raise ValueError("no requirement rows found in CSV")
    return _hwe1.map_rows(rows)


def prepass_summary(data: dict) -> str:
    """A compact, deterministic findings block to inject into the prompt.

    This is what makes the LLM call cheaper and more focused: Claude receives the
    mechanical findings as established fact and is told not to re-derive them.
    """
    lines = [
        "MECHANICAL PRE-PASS (deterministic, from parser/hwe1_to_aspice.py — "
        "treat as established fact, do not re-derive):",
        f"- requirements: {data['total']}  "
        f"| clean: {data['pass']}  | flagged: {data['partial']}  "
        f"| safety-relevant (ASIL A-D): {data['safety_count']}",
        f"- mechanical verdict: {data['verdict']}",
        "- per-requirement mechanical findings:",
    ]
    for r in data["requirements"]:
        findings = "; ".join(f"{c}: {m}" for c, m in r["findings"]) or "none"
        lines.append(
            f"    {r['id']} (raw {r['raw_id']}, ASIL {r['asil']}): {findings}"
        )
    return "\n".join(lines)
