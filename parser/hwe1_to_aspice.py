"""
hwe1_to_aspice.py
-----------------
Parses a raw hardware-requirement CSV and maps it to an ASPICE v4.0 HWE.1
Hardware Requirements Specification skeleton, applying the mechanically
checkable subset of the INCOSE 8 quality criteria.

This is the hardware-engineering counterpart to pytest_to_aspice.py. Where
that parser maps test results to SWQ.1, this one maps raw requirement lines
to HWE.1 records and flags quality defects an LLM/reviewer must then resolve.

What it CAN check mechanically (heuristics):
    - Unambiguous : flags vague terms (adequate, sufficient, fast, robust, ...)
    - Singular    : flags " and " / " or " conjunctions in the statement
    - Verifiable  : flags statements with no numeric value / unit
    - Conforming  : flags non-normative "should" instead of "shall"
    - ASIL present on safety-relevant rows

What it CANNOT check (left to the prompt / reviewer, emitted as TODO):
    - Necessary, Feasible, Implementation-free, full Completeness

Usage:
    python hwe1_to_aspice.py input_requirements.csv [--out spec.md]

Input CSV columns (header required):
    ID, Statement, Rationale, ASIL, Source

Output:
    aspice_hwe1_spec.md   (or the path given with --out)
"""

import argparse
import csv
import re
import sys
from datetime import datetime

VAGUE_TERMS = [
    "adequate", "sufficient", "appropriate", "fast", "slow", "robust",
    "reliable", "user-friendly", "as needed", "etc", "high", "low",
    "good", "reasonable", "minimal", "maximal", "enough",
]
NON_NORMATIVE = ["should", "may", "could", "might", "would"]
NUMERIC_RE = re.compile(r"\d")
DOMAIN_RE = re.compile(r"[^A-Za-z0-9]+")

VALID_ASIL = {"QM", "A", "B", "C", "D"}


def load_rows(path: str) -> list:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = {"ID", "Statement", "ASIL"} - set(reader.fieldnames or [])
        if missing:
            raise ValueError(
                f"CSV missing required column(s): {', '.join(sorted(missing))}. "
                f"Expected header: ID, Statement, Rationale, ASIL, Source"
            )
        return list(reader)


def derive_domain(source: str, statement: str) -> str:
    """Best-effort 3-letter domain code for the HW-REQ ID."""
    text = f"{source or ''} {statement or ''}".lower()
    if any(k in text for k in ("sensor", "measure", "current", "voltage")):
        return "SEN"
    if any(k in text for k in ("power", "supply", "rail")):
        return "PWR"
    if any(k in text for k in ("isolation", "safety", "fault", "diagnostic")):
        return "SAF"
    if any(k in text for k in ("temperature", "thermal", "environment")):
        return "ENV"
    return "GEN"


def incose_check(statement: str, asil: str) -> list:
    """Return a list of (criterion, finding) heuristic violations."""
    findings = []
    low = statement.lower()

    for term in VAGUE_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", low):
            findings.append(("Unambiguous", f"vague term '{term}' — quantify it"))
            break

    for word in NON_NORMATIVE:
        if re.search(rf"\b{word}\b", low):
            findings.append(("Conforming", f"non-normative '{word}' — use 'shall'"))
            break

    if " and " in low or " or " in low:
        findings.append(("Singular", "conjunction present — consider splitting"))

    if not NUMERIC_RE.search(statement):
        findings.append(("Verifiable", "no numeric value/unit — likely untestable"))

    if asil.upper() not in VALID_ASIL:
        findings.append(("ASIL", f"invalid/missing ASIL '{asil}'"))

    return findings


def map_rows(rows: list) -> dict:
    seq = {}
    requirements = []
    pass_count = 0

    for row in rows:
        statement = (row.get("Statement") or "").strip()
        asil = (row.get("ASIL") or "").strip()
        source = (row.get("Source") or "TBD").strip()
        rationale = (row.get("Rationale") or "").strip()
        domain = derive_domain(source, statement)
        seq[domain] = seq.get(domain, 0) + 1
        req_id = f"HW-REQ-{domain}-{seq[domain]:03d}"

        findings = incose_check(statement, asil)
        result = "Pass" if not findings else "Partial"
        if result == "Pass":
            pass_count += 1

        requirements.append({
            "id": req_id,
            "raw_id": (row.get("ID") or "").strip(),
            "asil": asil,
            "source": source,
            "statement": statement,
            "rationale": rationale,
            "findings": findings,
            "result": result,
        })

    safety_rows = [r for r in requirements if r["asil"].upper() in {"A", "B", "C", "D"}]
    verdict = "PASS" if pass_count == len(requirements) else \
              "PARTIAL" if pass_count >= len(requirements) * 0.5 else "FAIL"

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "total": len(requirements),
        "pass": pass_count,
        "partial": len(requirements) - pass_count,
        "safety_count": len(safety_rows),
        "requirements": requirements,
        "verdict": verdict,
    }


def generate_markdown(data: dict) -> str:
    lines = [
        "# ASPICE v4.0 HWE.1 — Hardware Requirements Specification (draft)",
        f"\n**Generated:** {data['timestamp']}",
        "**Tool:** hwe1_to_aspice.py (mechanical pass — INCOSE heuristics only)\n",
        "> This is a structural skeleton. The mechanical INCOSE subset is checked",
        "> here; Necessary / Feasible / Implementation-free / full Completeness",
        "> require the `aspice_hwe1_analyzer.md` prompt or a human reviewer.\n",
        "## Summary",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Requirements | {data['total']} |",
        f"| Pass (no heuristic finding) | {data['pass']} |",
        f"| Partial (>=1 finding) | {data['partial']} |",
        f"| Safety-relevant (ASIL A-D) | {data['safety_count']} |",
        f"\n**Mechanical verdict:** `{data['verdict']}`\n",
        "## Requirements\n",
    ]

    for r in data["requirements"]:
        lines.append(f"### {r['id']}  (from raw `{r['raw_id']}`)")
        lines.append("```")
        lines.append(f"ID:      {r['id']}")
        lines.append("Status:  Draft")
        lines.append(f"ASIL:    {r['asil']}")
        lines.append(f"Source:  {r['source']}")
        lines.append("")
        lines.append(f"Statement:\n  {r['statement']}")
        if r["rationale"]:
            lines.append(f"\nRationale:\n  {r['rationale']}")
        lines.append("\nAcceptance Criteria:\n  - TODO (reviewer/prompt): add measurable criteria")
        lines.append("Verification method:   TODO")
        lines.append("Verification level:    Component")
        lines.append("Traceability:          Upward "
                     f"{r['source']}; Downward TBD (HWE.2); Test TBD (HWE.4)")
        lines.append("```")
        if r["findings"]:
            lines.append(f"\n**INCOSE findings ({r['result']}):**")
            for crit, msg in r["findings"]:
                lines.append(f"- `{crit}` — {msg}")
        else:
            lines.append(f"\n**INCOSE:** Pass (mechanical heuristics)")
        lines.append("")

    lines.append("## INCOSE heuristic matrix\n")
    lines.append("| Requirement | Result | Findings |")
    lines.append("|---|---|---|")
    for r in data["requirements"]:
        f = "; ".join(c for c, _ in r["findings"]) or "—"
        lines.append(f"| {r['id']} | {r['result']} | {f} |")

    lines.append(
        f"\n---\n*Generated by aspice-oss-validator — "
        f"https://github.com/falkodoehler-boop/aspice-oss-validator*"
    )
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Map raw HW requirements CSV to ASPICE HWE.1.")
    ap.add_argument("csv_path", help="Input requirements CSV (ID,Statement,Rationale,ASIL,Source)")
    ap.add_argument("--out", default="aspice_hwe1_spec.md", help="Output Markdown path")
    args = ap.parse_args()

    try:
        rows = load_rows(args.csv_path)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    if not rows:
        print("error: no requirement rows found in CSV", file=sys.stderr)
        sys.exit(1)

    data = map_rows(rows)
    markdown = generate_markdown(data)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"HWE.1 spec written to: {args.out}")
    print(f"Mechanical verdict: {data['verdict']} "
          f"({data['pass']}/{data['total']} pass, {data['safety_count']} safety-relevant)")


if __name__ == "__main__":
    main()
