"""Command-line entry point for the Claude-native pipeline.

    aspice-validate hwe1 examples/phase_current_sensor/input_requirements.csv \
        --asil D --safety-goal SG-INV-002

Without an ANTHROPIC_API_KEY (or with --dry-run) the pipeline assembles and emits
the prompt + deterministic pre-pass without spending a token.
"""

from __future__ import annotations

import argparse
import sys

from . import client, pipeline


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="aspice-validate",
        description="Claude-native ASPICE/ISO 26262 compliance pipeline.",
    )
    sub = ap.add_subparsers(dest="process", required=True)

    p1 = sub.add_parser("hwe1", help="HWE.1 hardware requirements analysis")
    p1.add_argument("csv_path", help="Raw requirements CSV (ID,Statement,Rationale,ASIL,Source)")
    p1.add_argument("--asil", required=True, choices=["QM", "A", "B", "C", "D"])
    p1.add_argument("--safety-goal", default=None, help="Upstream safety goal / source id")
    p1.add_argument("--model", default=client.MODEL_DEFAULT,
                    help=f"Anthropic model id (default {client.MODEL_DEFAULT}; "
                         f"use {client.MODEL_HIGH_STAKES} for ASIL C/D sign-off)")
    p1.add_argument("--max-tokens", type=int, default=client.MAX_TOKENS_DEFAULT)
    p1.add_argument("--dry-run", action="store_true",
                    help="Assemble the prompt without calling the API")
    p1.add_argument("--config", default=None, help="review_rules.json overrides")
    p1.add_argument("--out", default=None, help="Write the artifact to this path")
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.process == "hwe1":
        result = pipeline.run_hwe1(
            args.csv_path,
            asil=args.asil,
            safety_goal=args.safety_goal,
            model=args.model,
            max_tokens=args.max_tokens,
            dry_run=args.dry_run,
            config=args.config,
            out_path=args.out,
        )
        mode = f"Claude ({result.model})" if result.used_api else "DRY-RUN (no API call)"
        if not result.out_path:
            sys.stdout.write(result.artifact)
        sys.stderr.write(
            f"\n[aspice-validate] hwe1 | mode: {mode} | "
            f"deterministic verdict: {result.prepass_verdict}"
            + (f" | written to {result.out_path}" if result.out_path else "")
            + "\n"
        )
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
