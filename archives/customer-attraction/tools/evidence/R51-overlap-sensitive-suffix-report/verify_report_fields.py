"""Independent formulas for every field of the frozen overlap audit report.

This does not import or execute the original auditor and does not re-enumerate
its membership identities or strategy comparisons.  The report's finite
cardinalities and endpoint values are checked against the established formulas.
"""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent


def endpoint_fields(p, q):
    label_count = (4 if p else 1) * (2 if q else 1)
    row = {"p": p, "q": q, "W": 4*p + 2*q, "I": 2*q,
           "OPT": 5*p + 3*q,
           "comparisons": label_count + label_count**2}
    assert 8 * row["OPT"] == 10 * row["W"] + 2 * row["I"]
    return row


def main():
    raw = (HERE / "original/overlap_sensitive_suffix_audit.json").read_bytes()
    assert len(raw) == 2899
    assert sha256(raw).hexdigest() == (
        "dcd0adf87428f0aa77e671ca8d47e0d52dddeb79c6958d9acf6d86881d81af06"
    )
    actual = json.loads(raw)
    background_tests = (Fraction(0), Fraction(1), Fraction(2), Fraction(3),
                        Fraction(17), Fraction(10**6),
                        Fraction(1, 2), Fraction(11, 7))
    records = [endpoint_fields(p, q) for p in range(5) for q in range(5)]
    expected = {
        "status": "exact independent audit passed",
        "membership_cases": (2**6) * len(background_tests),
        "endpoint_records": records,
        "rational_ratio_denominator_max": 10,
    }
    assert actual == expected
    integer_loads = sum(b.denominator == 1 for b in background_tests)
    assert integer_loads == 6
    ratio_calls = 0
    ratio_comparisons = 0
    ratios = set()
    for denominator in range(1, 11):
        for numerator in range(denominator + 1):
            row = endpoint_fields(denominator - numerator, 2*numerator)
            assert row["W"] == 4 * denominator > 0
            assert Fraction(row["I"], row["W"]) == Fraction(numerator, denominator)
            ratio_calls += 1
            ratio_comparisons += row["comparisons"]
            ratios.add(Fraction(numerator, denominator))
    assert ratio_calls == 65 and len(ratios) == 33
    assert sum(row["comparisons"] for row in records) == 1258
    assert ratio_comparisons == 3500
    print(json.dumps({
        "status": "PASS",
        "source_bytes": len(raw), "source_sha256": sha256(raw).hexdigest(),
        "all_original_keys_and_values_match": True,
        "membership_bit_patterns": 64,
        "background_test_values": list(map(str, background_tests)),
        "membership_cases": 512,
        "integer_background_bound_checks_in_original": 64*integer_loads,
        "noninteger_background_identity_checks_in_original": 64*(8-integer_loads),
        "saved_endpoint_records": 25,
        "saved_endpoint_action_comparisons": 1258,
        "additional_unsaved_ratio_endpoint_calls": ratio_calls,
        "additional_unsaved_ratio_action_comparisons": ratio_comparisons,
        "ratio_arguments_distinct_values": len(ratios),
        "zero_endpoint_has_one_empty_theme_two_comparisons": records[0],
        "original_auditor_executed_by_this_checker": False,
        "membership_identities_reenumerated_by_this_checker": False,
        "strategy_ICs_reenumerated_by_this_checker": False,
    }, indent=2))


if __name__ == "__main__":
    main()
