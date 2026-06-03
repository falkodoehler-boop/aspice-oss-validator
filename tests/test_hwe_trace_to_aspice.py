"""Unit tests for parser/hwe_trace_to_aspice.py (HWE.2-4 traceability)."""
import hwe_trace_to_aspice as t


def _clean_set():
    reqs = [{"ID": "HW-REQ-1", "ASIL": "D"}]
    elems = [{"ID": "HW-ELEM-1", "Name": "E1", "ASIL": "D",
              "allocated_req_ids": "HW-REQ-1", "allocation_type": "Full"}]
    tcs = [
        {"ID": "TC-D-1", "type": "D", "verifies_id": "HW-ELEM-1",
         "ASIL": "D", "fault_injection": "yes"},
        {"ID": "TC-R-1", "type": "R", "verifies_id": "HW-REQ-1",
         "ASIL": "D", "fault_injection": "no"},
    ]
    return reqs, elems, tcs


def test_clean_set_passes_all():
    data = t.analyze(*_clean_set())
    assert data["findings"]["hwe2"] == []
    assert data["findings"]["hwe3"] == []
    assert data["findings"]["hwe4"] == []
    assert data["overall"] == "PASS"
    assert data["design_asil"] == "D"


def test_orphan_element_and_requirement_detected():
    reqs = [{"ID": "HW-REQ-1", "ASIL": "D"}, {"ID": "HW-REQ-2", "ASIL": "D"}]
    elems = [
        {"ID": "HW-ELEM-1", "Name": "E1", "ASIL": "D",
         "allocated_req_ids": "HW-REQ-1", "allocation_type": "Full"},
        {"ID": "HW-ELEM-2", "Name": "Housing", "ASIL": "D",
         "allocated_req_ids": "", "allocation_type": "Full"},  # orphan element
    ]
    tcs = []
    data = t.analyze(reqs, elems, tcs)
    joined = " ".join(data["findings"]["hwe2"])
    assert "Orphan element HW-ELEM-2" in joined
    assert "Orphan requirement HW-REQ-2" in joined


def test_asil_d_element_without_fault_injection_flagged():
    reqs, elems, tcs = _clean_set()
    tcs[0]["fault_injection"] = "no"  # remove FI from the only TC-D
    data = t.analyze(reqs, elems, tcs)
    assert any("fault-injection" in f for f in data["findings"]["hwe3"])


def test_coverage_below_asil_d_target_flagged():
    # Regression for the dead-config-key review finding: thresholds must bite.
    reqs = [{"ID": "HW-REQ-1", "ASIL": "D"}, {"ID": "HW-REQ-2", "ASIL": "D"}]
    elems = [{"ID": "HW-ELEM-1", "Name": "E1", "ASIL": "D",
              "allocated_req_ids": "HW-REQ-1;HW-REQ-2", "allocation_type": "Full"}]
    tcs = [
        {"ID": "TC-D-1", "type": "D", "verifies_id": "HW-ELEM-1",
         "ASIL": "D", "fault_injection": "yes"},
        {"ID": "TC-R-1", "type": "R", "verifies_id": "HW-REQ-1",
         "ASIL": "D", "fault_injection": "no"},  # HW-REQ-2 has no TC-R
    ]
    data = t.analyze(reqs, elems, tcs)
    assert data["req_coverage"] == 50.0
    assert any("target 100%" in f for f in data["findings"]["hwe4"])


def test_unknown_id_reference_flagged():
    reqs = [{"ID": "HW-REQ-1", "ASIL": "D"}]
    elems = [{"ID": "HW-ELEM-1", "Name": "E1", "ASIL": "D",
              "allocated_req_ids": "HW-REQ-1", "allocation_type": "Full"}]
    tcs = [{"ID": "TC-R-9", "type": "R", "verifies_id": "HW-REQ-NOPE",
            "ASIL": "D", "fault_injection": "no"}]
    data = t.analyze(reqs, elems, tcs)
    assert any("unknown requirement HW-REQ-NOPE" in f for f in data["findings"]["hwe4"])
