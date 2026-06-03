"""Unit tests for parser/hwe1_to_aspice.py (HWE.1 INCOSE screen)."""
import hwe1_to_aspice as h


def test_derive_domain_uses_statement_not_only_source():
    # Regression for LL-2026-0001: a sensor requirement must map to SEN even
    # when the Source column does not contain the keyword.
    assert h.derive_domain("SG-INV-002", "phase current sensor") == "SEN"
    assert h.derive_domain("SYS-REQ-PWR-003", "5 V supply rail") == "PWR"


def test_incose_flags_vague_conjunction_and_unverifiable():
    findings = dict(h.incose_check("The sensor shall be fast and robust", "D"))
    assert "Unambiguous" in findings   # "fast"/"robust"
    assert "Singular" in findings      # " and "
    assert "Verifiable" in findings    # no numeric value


def test_incose_flags_non_normative_should():
    findings = dict(h.incose_check("The sensor should provide 5 V", "D"))
    assert "Conforming" in findings


def test_incose_clean_requirement_has_no_findings():
    findings = h.incose_check("The sensor shall measure 400 A within 2 us", "D")
    assert findings == []


def test_incose_flags_invalid_asil():
    findings = dict(h.incose_check("shall measure 400 A", "X"))
    assert "ASIL" in findings


def test_map_rows_assigns_ids_and_verdict():
    rows = [
        {"ID": "RAW-1", "Statement": "shall measure 400 A within 2 us",
         "Rationale": "", "ASIL": "D", "Source": "sensor"},
        {"ID": "RAW-2", "Statement": "shall be adequate", "Rationale": "",
         "ASIL": "D", "Source": "sensor"},
    ]
    data = h.map_rows(rows)
    assert data["total"] == 2
    ids = [r["id"] for r in data["requirements"]]
    assert ids == ["HW-REQ-SEN-001", "HW-REQ-SEN-002"]
    assert data["requirements"][0]["result"] == "Pass"
    assert data["requirements"][1]["result"] == "Partial"
