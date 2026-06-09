"""End-to-end orchestration: raw input -> guardrail -> Claude -> artifact.

The pipeline is deliberately honest about cost and reproducibility:

  * ``--dry-run`` (or no API key / no SDK) assembles the full prompt and the
    deterministic pre-pass and writes them to the artifact WITHOUT calling the
    API. An evaluator can therefore run the whole pipeline end-to-end for free
    and see exactly what would be sent to Claude.
  * A live run prepends a provenance header naming the model and token usage, so
    every generated artifact is traceable to the model that produced it.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone

from . import client, guardrail, prompts


@dataclass
class PipelineResult:
    process: str
    artifact: str
    used_api: bool
    model: str | None
    prepass_verdict: str
    out_path: str | None = None


def _provenance(used_api: bool, model: str | None, resp=None) -> str:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if used_api:
        tokens = ""
        if resp and (resp.input_tokens or resp.output_tokens):
            tokens = f" | tokens in/out: {resp.input_tokens}/{resp.output_tokens}"
        mode = f"Claude analysis — model `{model}`{tokens}"
    else:
        mode = "DRY-RUN — no API call; prompt + deterministic pre-pass only"
    return (
        f"<!-- aspice-oss-validator pipeline | {stamp} | {mode} -->\n"
        f"> **Provenance:** {mode}. Deterministic pre-pass: "
        f"`parser/hwe1_to_aspice.py`.\n"
    )


def run_hwe1(
    csv_path: str,
    *,
    asil: str,
    safety_goal: str | None = None,
    model: str = client.MODEL_DEFAULT,
    max_tokens: int = client.MAX_TOKENS_DEFAULT,
    dry_run: bool = False,
    config: str | None = None,
    out_path: str | None = None,
) -> PipelineResult:
    """Run the HWE.1 analysis pipeline for a raw requirements CSV."""
    data = guardrail.hwe1_prepass(csv_path, config=config)
    prepass = guardrail.prepass_summary(data)

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        raw_csv = f.read().strip()

    requirement_input = f"{raw_csv}\n\n{prepass}"
    template = prompts.load_template("hwe1")
    system, user = prompts.build_hwe1_messages(
        template,
        safety_goal=safety_goal or "(not supplied — flag as missing upstream trace)",
        asil=asil,
        requirement_input=requirement_input,
    )

    go_live = not dry_run and client.api_key_present()

    if go_live:
        resp = client.complete(system, user, model=model, max_tokens=max_tokens)
        body = resp.text
        header = _provenance(True, model, resp)
        used_api, used_model = True, model
    else:
        body = (
            "## DRY-RUN: assembled prompt (not sent)\n\n"
            "### System (durable instructions, abbreviated)\n\n"
            f"{system[:1200].rstrip()}\n\n[... full template in "
            "prompts/aspice_hwe1_analyzer.md ...]\n\n"
            "### User (per-run input)\n\n"
            "```\n" + user + "\n```\n"
        )
        header = _provenance(False, None)
        used_api, used_model = False, None

    artifact = f"{header}\n{body}\n"
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(artifact)

    return PipelineResult(
        process="hwe1",
        artifact=artifact,
        used_api=used_api,
        model=used_model,
        prepass_verdict=data["verdict"],
        out_path=out_path,
    )
