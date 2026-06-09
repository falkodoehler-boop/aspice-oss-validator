"""Tests for the Claude-native pipeline's deterministic (dry-run) path.

These run with no API key and no `anthropic` install: they prove the guardrail +
prompt assembly are reproducible and that no network call happens in dry-run.
"""
import os

from aspice_validator import pipeline, guardrail

EXAMPLE_CSV = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "examples", "phase_current_sensor", "input_requirements.csv",
)


def test_guardrail_prepass_is_deterministic():
    a = guardrail.hwe1_prepass(EXAMPLE_CSV)
    b = guardrail.hwe1_prepass(EXAMPLE_CSV)
    assert a["verdict"] == b["verdict"]
    assert [r["id"] for r in a["requirements"]] == [r["id"] for r in b["requirements"]]
    assert a["total"] > 0


def test_dry_run_emits_prompt_without_api(tmp_path):
    out = tmp_path / "artifact.md"
    result = pipeline.run_hwe1(
        EXAMPLE_CSV, asil="D", safety_goal="SG-INV-002",
        dry_run=True, out_path=str(out),
    )
    assert result.used_api is False
    assert result.model is None
    assert result.prepass_verdict in {"PASS", "PARTIAL", "FAIL"}
    text = out.read_text(encoding="utf-8")
    assert "DRY-RUN" in text
    assert "MECHANICAL PRE-PASS" in text       # guardrail findings injected
    assert "Target ASIL:           D" in text  # placeholder bound


def test_prepass_summary_lists_every_requirement():
    data = guardrail.hwe1_prepass(EXAMPLE_CSV)
    summary = guardrail.prepass_summary(data)
    for r in data["requirements"]:
        assert r["id"] in summary
