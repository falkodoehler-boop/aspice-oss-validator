"""Load the prompt templates in ``prompts/`` and fill their placeholders.

The prompt files are the *spec* (version-controlled, human-reviewed). This module
is the only place that binds runtime inputs into them, so there is a single,
auditable point where "what we asked Claude" is constructed.
"""

from __future__ import annotations

import os

# repo_root/src/aspice_validator/prompts.py -> repo_root
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROMPTS_DIR = os.path.join(_REPO_ROOT, "prompts")

PROMPT_FILES = {
    "hwe1": "aspice_hwe1_analyzer.md",
    "hwe2": "aspice_hwe2_analyzer.md",
    "hwe3": "aspice_hwe3_analyzer.md",
    "hwe4": "aspice_hwe4_analyzer.md",
}


def load_template(process: str) -> str:
    """Return the raw Markdown template for a process key (e.g. 'hwe1')."""
    try:
        filename = PROMPT_FILES[process]
    except KeyError:
        raise ValueError(
            f"unknown process '{process}'. Known: {', '.join(sorted(PROMPT_FILES))}"
        )
    path = os.path.join(PROMPTS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_hwe1_messages(
    template: str,
    *,
    safety_goal: str,
    asil: str,
    requirement_input: str,
) -> tuple[str, str]:
    """Split the HWE.1 template into (system, user) and bind the placeholders.

    The template's "## Prompt Template" section onward is the instruction body
    (used as the system prompt); the concrete inputs become the user turn. This
    keeps the durable instructions cacheable and separate from per-run data.
    """
    system = template
    user = (
        "Analyze this hardware requirement input under the rules above.\n\n"
        f"Safety goal / source:  {safety_goal}\n"
        f"Target ASIL:           {asil}\n\n"
        "Raw requirement input (CSV-derived, plus the deterministic pre-pass "
        "already computed by the guardrail — do NOT re-derive the mechanical "
        "findings; focus on the criteria the guardrail cannot check: Necessary, "
        "Feasible, Implementation-free, full Completeness, and the ISO 26262-5 "
        "graded analysis):\n\n"
        f"{requirement_input}\n"
    )
    return system, user
