"""
fmeda_to_aspice.py
------------------
Computes the ISO 26262-5:2018 hardware architectural metrics from a per-element
FMEDA CSV and checks them against the ASIL target (Clause 8: SPFM/LFM,
Clause 9: PMHF). This is the quantitative gate that decides whether a design is
laid out for a given ASIL — in particular ASIL D.

Formulas (ISO 26262-5:2018, Clause 8 / Annex C):
    SPFM = 1 - sum(lambda_spf + lambda_rf) / sum(lambda_total)
    LFM  = 1 - sum(lambda_mpf_latent) / sum(lambda_total - lambda_spf - lambda_rf)
    PMHF (proxy, in FIT) = sum(lambda_spf + lambda_rf)
        NOTE: a rigorous PMHF also accounts for detected/latent dual-point
        failures with their exposure and test intervals (Clause 9 / Annex F).
        This tool reports the residual single-point + residual-fault sum as a
        deterministic lower-bound proxy and labels it as such — it does not
        replace a full PMHF computation.

Targets come from config/review_rules.json -> asil_architectural_metrics.

Usage:
    python fmeda_to_aspice.py fmeda.csv --asil D [--out fmeda_metrics_report.md]

FMEDA CSV columns (header required, failure rates in FIT = 1e-9/h):
    element_id, lambda_total_fit, lambda_spf_fit, lambda_rf_fit, lambda_mpf_latent_fit
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime

DEFAULT_CONFIG = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config", "review_rules.json",
)

REQUIRED_COLS = {
    "element_id", "lambda_total_fit", "lambda_spf_fit",
    "lambda_rf_fit", "lambda_mpf_latent_fit",
}


def load_targets(path: str) -> dict:
    """Load ASIL metric targets from config, with a built-in fallback."""
    fallback = {
        "spfm_min_percent": {"B": 90, "C": 97, "D": 99},
        "lfm_min_percent": {"B": 60, "C": 80, "D": 90},
        "pmhf_max_fit": {"B": 100, "C": 100, "D": 10},
    }
    if not path or not os.path.isfile(path):
        return fallback
    try:
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        return cfg.get("asil_architectural_metrics", fallback)
    except (OSError, ValueError) as exc:
        print(f"warning: ignoring config {path}: {exc}", file=sys.stderr)
        return fallback


def load_fmeda(path: str) -> list:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(
                f"{path}: missing column(s): {', '.join(sorted(missing))}"
            )
        rows = []
        for i, row in enumerate(reader, start=2):
            try:
                rows.append({
                    "id": (row.get("element_id") or "").strip(),
                    "total": float(row["lambda_total_fit"]),
                    "spf": float(row["lambda_spf_fit"]),
                    "rf": float(row["lambda_rf_fit"]),
                    "mpf": float(row["lambda_mpf_latent_fit"]),
                })
            except ValueError as exc:
                raise ValueError(f"{path} line {i}: non-numeric failure rate ({exc})")
        return rows


def compute(rows: list) -> dict:
    sum_total = sum(r["total"] for r in rows)
    sum_spf_rf = sum(r["spf"] + r["rf"] for r in rows)
    sum_mpf = sum(r["mpf"] for r in rows)
    denom_lfm = sum_total - sum_spf_rf

    spfm = (1 - sum_spf_rf / sum_total) * 100 if sum_total else None
    lfm = (1 - sum_mpf / denom_lfm) * 100 if denom_lfm else None
    pmhf_proxy = sum_spf_rf  # FIT

    return {
        "sum_total": sum_total,
        "sum_spf_rf": sum_spf_rf,
        "sum_mpf": sum_mpf,
        "spfm": spfm,
        "lfm": lfm,
        "pmhf_proxy_fit": pmhf_proxy,
    }


def evaluate(metrics: dict, asil: str, targets: dict) -> dict:
    asil = asil.upper()

    def tgt(key):
        return (targets.get(key) or {}).get(asil)

    spfm_t = tgt("spfm_min_percent")
    lfm_t = tgt("lfm_min_percent")
    pmhf_t = tgt("pmhf_max_fit")

    checks = []
    if spfm_t is None and lfm_t is None and pmhf_t is None:
        checks.append(("Architectural metrics", "N/A",
                       f"ASIL {asil} has no architectural-metric target"))
        verdict = "N/A"
    else:
        def chk(name, value, target, higher_is_better):
            if target is None:
                return (name, "N/A", "no target for this ASIL")
            if value is None:
                return (name, "FAIL", "metric not computable")
            ok = value >= target if higher_is_better else value <= target
            rel = ">=" if higher_is_better else "<"
            unit = "%" if higher_is_better else " FIT"
            return (name, "PASS" if ok else "FAIL",
                    f"{value:.2f}{unit} vs target {rel} {target}{unit}")

        checks.append(chk(f"SPFM (ASIL {asil})", metrics["spfm"], spfm_t, True))
        checks.append(chk(f"LFM (ASIL {asil})", metrics["lfm"], lfm_t, True))
        checks.append(chk(f"PMHF proxy (ASIL {asil})",
                          metrics["pmhf_proxy_fit"], pmhf_t, False))
        verdict = "PASS" if all(c[1] in ("PASS", "N/A") for c in checks) else "FAIL"

    return {"asil": asil, "checks": checks, "verdict": verdict}


def generate_markdown(rows, metrics, evaluation) -> str:
    L = [
        "# ISO 26262-5 — Hardware Architectural Metrics Report",
        f"\n**Generated:** {datetime.now().isoformat(timespec='seconds')}",
        f"**Target ASIL:** {evaluation['asil']}",
        "**Tool:** fmeda_to_aspice.py (Clause 8 SPFM/LFM, Clause 9 PMHF proxy)\n",
        "## Per-element FMEDA input (FIT)",
        "| Element | lambda_total | lambda_SPF | lambda_RF | lambda_MPF,latent |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        L.append(f"| {r['id']} | {r['total']:.3g} | {r['spf']:.3g} | "
                 f"{r['rf']:.3g} | {r['mpf']:.3g} |")

    def fmt(v, unit):
        return f"{v:.2f}{unit}" if v is not None else "n/a"

    L += [
        "",
        "## Computed metrics",
        "| Metric | Value |",
        "|---|---|",
        f"| Sum lambda_total | {metrics['sum_total']:.3g} FIT |",
        f"| Sum residual (SPF+RF) | {metrics['sum_spf_rf']:.3g} FIT |",
        f"| SPFM | {fmt(metrics['spfm'], '%')} |",
        f"| LFM | {fmt(metrics['lfm'], '%')} |",
        f"| PMHF (residual proxy) | {metrics['pmhf_proxy_fit']:.3g} FIT |",
        "",
        "## Target evaluation",
        "| Check | Result | Detail |",
        "|---|---|---|",
    ]
    for name, res, detail in evaluation["checks"]:
        L.append(f"| {name} | `{res}` | {detail} |")

    L.append(f"\n**Architectural-metric verdict:** `{evaluation['verdict']}`")
    L.append(
        "\n> PMHF here is the residual single-point + residual-fault sum, a "
        "deterministic lower-bound proxy. A release-grade PMHF must add "
        "dual-point (latent/detected) contributions with exposure and test "
        "intervals per ISO 26262-5 Clause 9 / Annex F."
    )
    L.append(
        f"\n---\n*Generated by aspice-oss-validator — "
        f"https://github.com/falkodoehler-boop/aspice-oss-validator*"
    )
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="ISO 26262-5 architectural metrics from FMEDA CSV.")
    ap.add_argument("fmeda_csv", help="FMEDA CSV (element_id, lambda_*_fit)")
    ap.add_argument("--asil", default="D", help="target ASIL (QM/A/B/C/D), default D")
    ap.add_argument("--out", default="fmeda_metrics_report.md", help="output Markdown path")
    ap.add_argument("--config", default=DEFAULT_CONFIG, help="review_rules.json (optional)")
    args = ap.parse_args()

    try:
        rows = load_fmeda(args.fmeda_csv)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
    if not rows:
        print("error: no FMEDA rows found", file=sys.stderr)
        sys.exit(1)

    targets = load_targets(args.config)
    metrics = compute(rows)
    evaluation = evaluate(metrics, args.asil, targets)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(generate_markdown(rows, metrics, evaluation))

    sp = metrics["spfm"]
    lf = metrics["lfm"]
    print(f"Metrics report written to: {args.out}")
    print(f"ASIL {evaluation['asil']} verdict: {evaluation['verdict']} | "
          f"SPFM {sp:.2f}% | LFM {lf:.2f}% | PMHF~{metrics['pmhf_proxy_fit']:.3g} FIT"
          if sp is not None and lf is not None else
          f"ASIL {evaluation['asil']} verdict: {evaluation['verdict']}")


if __name__ == "__main__":
    main()
