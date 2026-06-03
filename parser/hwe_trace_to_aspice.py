"""
hwe_trace_to_aspice.py
----------------------
Mechanical traceability & coverage checker spanning ASPICE v4.0
HWE.2 (design/allocation), HWE.3 (verification vs design) and
HWE.4 (verification vs requirements).

Where hwe1_to_aspice.py screens requirement *text*, this parser checks the
*relationships* between requirements, design elements and test cases — which
is fully deterministic (set joins over IDs), not language heuristics.

Checks performed:
  HWE.2  - every requirement is allocated to >= 1 element (no orphan req)
         - every element allocates >= 1 requirement (no orphan element)
         - element ASIL >= max ASIL of its allocated requirements
         - allocated_req_ids reference existing requirements
  HWE.3  - element coverage: every element has >= 1 design test case (TC-D)
         - fault injection present for every ASIL C/D element
  HWE.4  - requirement coverage: every requirement has >= 1 requirement
           test case (TC-R) — must be 100%, no threshold below it

Usage:
    python hwe_trace_to_aspice.py \
        --requirements requirements.csv \
        --elements elements.csv \
        --testcases testcases.csv \
        [--out hwe_trace_report.md]

CSV schemas (headers required):
    requirements.csv : ID, ASIL
    elements.csv     : ID, Name, ASIL, allocated_req_ids, allocation_type
                       (allocated_req_ids = semicolon-separated requirement IDs)
    testcases.csv    : ID, type, verifies_id, ASIL, fault_injection
                       (type = D for HWE.3 [verifies element], R for HWE.4
                        [verifies requirement]; fault_injection = yes/no)
"""

import argparse
import csv
import sys
from datetime import datetime

ASIL_ORDER = {"QM": 0, "A": 1, "B": 2, "C": 3, "D": 4}


def load_csv(path: str, required: set) -> list:
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(
                f"{path}: missing column(s): {', '.join(sorted(missing))}"
            )
        return [ {k: (v or '').strip() for k, v in row.items()} for row in reader ]


def split_ids(field: str) -> list:
    return [x.strip() for x in field.replace(",", ";").split(";") if x.strip()]


def asil_rank(asil: str) -> int:
    return ASIL_ORDER.get(asil.upper(), -1)


def analyze(reqs, elems, tcs) -> dict:
    req_ids = {r["ID"] for r in reqs}
    req_asil = {r["ID"]: r["ASIL"] for r in reqs}
    elem_ids = {e["ID"] for e in elems}

    findings = {"hwe2": [], "hwe3": [], "hwe4": []}

    # ---- HWE.2: allocation ----
    allocated_reqs = set()
    for e in elems:
        alloc = split_ids(e.get("allocated_req_ids", ""))
        if not alloc:
            findings["hwe2"].append(
                f"Orphan element {e['ID']} ({e.get('Name','')}) — allocates no requirement"
            )
        for rid in alloc:
            allocated_reqs.add(rid)
            if rid not in req_ids:
                findings["hwe2"].append(
                    f"Element {e['ID']} allocates unknown requirement {rid}"
                )
        # ASIL consistency: element ASIL >= max allocated requirement ASIL
        known = [r for r in alloc if r in req_asil]
        if known:
            max_req = max(known, key=lambda r: asil_rank(req_asil[r]))
            if asil_rank(e.get("ASIL", "")) < asil_rank(req_asil[max_req]):
                findings["hwe2"].append(
                    f"Element {e['ID']} ASIL {e.get('ASIL','?')} < allocated "
                    f"requirement {max_req} ASIL {req_asil[max_req]}"
                )
    for rid in sorted(req_ids - allocated_reqs):
        findings["hwe2"].append(f"Orphan requirement {rid} — not allocated to any element")

    # ---- HWE.3: design test coverage (TC-D verifies elements) ----
    tc_d = [t for t in tcs if t.get("type", "").upper() == "D"]
    covered_elems = {t["verifies_id"] for t in tc_d if t.get("verifies_id")}
    for e in elems:
        if e["ID"] not in covered_elems:
            findings["hwe3"].append(f"Element {e['ID']} has no design test case (TC-D)")
    for t in tc_d:
        if t.get("verifies_id") and t["verifies_id"] not in elem_ids:
            findings["hwe3"].append(
                f"Test case {t['ID']} verifies unknown element {t['verifies_id']}"
            )
    # fault injection for ASIL C/D elements
    fi_elems = {t["verifies_id"] for t in tc_d
                if t.get("fault_injection", "").lower() in ("yes", "true", "1")}
    for e in elems:
        if asil_rank(e.get("ASIL", "")) >= ASIL_ORDER["C"] and e["ID"] not in fi_elems:
            findings["hwe3"].append(
                f"ASIL {e.get('ASIL')} element {e['ID']} has no fault-injection test case"
            )

    # ---- HWE.4: requirement test coverage (TC-R verifies requirements) ----
    tc_r = [t for t in tcs if t.get("type", "").upper() == "R"]
    covered_reqs = {t["verifies_id"] for t in tc_r if t.get("verifies_id")}
    for rid in sorted(req_ids - covered_reqs):
        findings["hwe4"].append(f"Requirement {rid} has no requirement test case (TC-R)")
    for t in tc_r:
        if t.get("verifies_id") and t["verifies_id"] not in req_ids:
            findings["hwe4"].append(
                f"Test case {t['ID']} verifies unknown requirement {t['verifies_id']}"
            )

    # ---- coverage metrics ----
    elem_cov = (len(covered_elems & elem_ids) / len(elem_ids) * 100) if elem_ids else 100.0
    req_cov = (len(covered_reqs & req_ids) / len(req_ids) * 100) if req_ids else 100.0

    def verdict(fs):
        return "PASS" if not fs else "FAIL"

    overall = "PASS" if not any(findings.values()) else \
              "PARTIAL" if req_cov >= 50 else "FAIL"

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "counts": {"req": len(reqs), "elem": len(elems),
                   "tc_d": len(tc_d), "tc_r": len(tc_r)},
        "elem_coverage": round(elem_cov, 1),
        "req_coverage": round(req_cov, 1),
        "findings": findings,
        "verdicts": {k: verdict(v) for k, v in findings.items()},
        "overall": overall,
        "reqs": reqs, "elems": elems, "tcs": tcs,
    }


def build_matrix(reqs, elems, tcs) -> list:
    """Requirement -> elements -> test cases, as report rows."""
    rows = []
    for r in reqs:
        rid = r["ID"]
        elems_for = [e["ID"] for e in elems if rid in split_ids(e.get("allocated_req_ids", ""))]
        tc_r_for = [t["ID"] for t in tcs
                    if t.get("type", "").upper() == "R" and t.get("verifies_id") == rid]
        tc_d_for = [t["ID"] for t in tcs
                    if t.get("type", "").upper() == "D" and t.get("verifies_id") in elems_for]
        rows.append((rid, r.get("ASIL", "?"),
                     ", ".join(elems_for) or "—",
                     ", ".join(tc_d_for) or "—",
                     ", ".join(tc_r_for) or "—"))
    return rows


def generate_markdown(data: dict) -> str:
    c = data["counts"]
    L = [
        "# ASPICE v4.0 HWE.2-HWE.4 — Traceability & Coverage Report",
        f"\n**Generated:** {data['timestamp']}",
        "**Tool:** hwe_trace_to_aspice.py (mechanical relationship checks)\n",
        "## Summary",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Requirements (HWE.1) | {c['req']} |",
        f"| Design elements (HWE.2) | {c['elem']} |",
        f"| Design test cases TC-D (HWE.3) | {c['tc_d']} |",
        f"| Requirement test cases TC-R (HWE.4) | {c['tc_r']} |",
        f"| Element coverage (HWE.3) | {data['elem_coverage']}% |",
        f"| Requirement coverage (HWE.4) | {data['req_coverage']}% (target 100%) |",
        "",
        "| Process | Verdict |",
        "|---------|---------|",
        f"| HWE.2 allocation | `{data['verdicts']['hwe2']}` |",
        f"| HWE.3 design verification | `{data['verdicts']['hwe3']}` |",
        f"| HWE.4 requirement verification | `{data['verdicts']['hwe4']}` |",
        f"\n**Overall verdict:** `{data['overall']}`\n",
    ]

    titles = {"hwe2": "HWE.2 — Allocation findings",
              "hwe3": "HWE.3 — Design verification findings",
              "hwe4": "HWE.4 — Requirement verification findings"}
    for key in ("hwe2", "hwe3", "hwe4"):
        L.append(f"## {titles[key]}")
        fs = data["findings"][key]
        if fs:
            for f in fs:
                L.append(f"- {f}")
        else:
            L.append("- No findings. All checks pass.")
        L.append("")

    L.append("## Bidirectional traceability matrix\n")
    L.append("| Requirement | ASIL | Elements (HWE.2) | TC-D (HWE.3) | TC-R (HWE.4) |")
    L.append("|---|---|---|---|---|")
    for rid, asil, el, tcd, tcr in build_matrix(data["reqs"], data["elems"], data["tcs"]):
        L.append(f"| {rid} | {asil} | {el} | {tcd} | {tcr} |")

    L.append(
        f"\n---\n*Generated by aspice-oss-validator — "
        f"https://github.com/falkodoehler-boop/aspice-oss-validator*"
    )
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="HWE.2-4 traceability & coverage checker.")
    ap.add_argument("--requirements", required=True, help="requirements CSV (ID, ASIL)")
    ap.add_argument("--elements", required=True,
                    help="elements CSV (ID, Name, ASIL, allocated_req_ids, allocation_type)")
    ap.add_argument("--testcases", required=True,
                    help="test cases CSV (ID, type, verifies_id, ASIL, fault_injection)")
    ap.add_argument("--out", default="hwe_trace_report.md", help="output Markdown path")
    args = ap.parse_args()

    try:
        reqs = load_csv(args.requirements, {"ID", "ASIL"})
        elems = load_csv(args.elements, {"ID", "ASIL", "allocated_req_ids"})
        tcs = load_csv(args.testcases, {"ID", "type", "verifies_id"})
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    data = analyze(reqs, elems, tcs)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(generate_markdown(data))

    print(f"Traceability report written to: {args.out}")
    print(f"Overall: {data['overall']} | element cov {data['elem_coverage']}% "
          f"| requirement cov {data['req_coverage']}%")
    print(f"Findings - HWE.2: {len(data['findings']['hwe2'])}, "
          f"HWE.3: {len(data['findings']['hwe3'])}, "
          f"HWE.4: {len(data['findings']['hwe4'])}")


if __name__ == "__main__":
    main()
