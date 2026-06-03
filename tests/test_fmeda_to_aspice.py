"""Unit tests for parser/fmeda_to_aspice.py (ISO 26262-5 metrics)."""
import math

import fmeda_to_aspice as f

TARGETS = {
    "spfm_min_percent": {"A": None, "B": 90, "C": 97, "D": 99},
    "lfm_min_percent": {"A": None, "B": 60, "C": 80, "D": 90},
    "pmhf_max_fit": {"A": None, "B": 100, "C": 100, "D": 10},
}


def _rows(spf, rf, mpf, total=100.0):
    return [{"id": "E1", "total": total, "spf": spf, "rf": rf, "mpf": mpf}]


def test_compute_formulas():
    m = f.compute(_rows(spf=0.5, rf=0.5, mpf=9.0))
    assert math.isclose(m["spfm"], 99.0, rel_tol=1e-9)        # 1 - 1/100
    assert math.isclose(m["lfm"], (1 - 9.0 / 99.0) * 100, rel_tol=1e-9)
    assert math.isclose(m["pmhf_proxy_fit"], 1.0, rel_tol=1e-9)


def test_asil_d_pass():
    m = f.compute(_rows(0.5, 0.5, 9.0))
    ev = f.evaluate(m, "D", TARGETS)
    assert ev["verdict"] == "PASS"


def test_asil_d_fail_on_low_spfm_and_lfm():
    m = f.compute(_rows(spf=3.0, rf=2.0, mpf=20.0))  # SPFM 95%, LFM ~78.9%
    ev = f.evaluate(m, "D", TARGETS)
    assert ev["verdict"] == "FAIL"
    results = {name.split(" ")[0]: res for name, res, _ in ev["checks"]}
    assert results["SPFM"] == "FAIL"
    assert results["LFM"] == "FAIL"


def test_asil_a_has_no_targets():
    m = f.compute(_rows(0.5, 0.5, 9.0))
    ev = f.evaluate(m, "A", TARGETS)
    assert ev["verdict"] == "N/A"


def test_zero_total_does_not_crash():
    m = f.compute([{"id": "E0", "total": 0.0, "spf": 0.0, "rf": 0.0, "mpf": 0.0}])
    assert m["spfm"] is None
    ev = f.evaluate(m, "D", TARGETS)
    assert ev["verdict"] == "FAIL"  # not computable -> cannot claim PASS
