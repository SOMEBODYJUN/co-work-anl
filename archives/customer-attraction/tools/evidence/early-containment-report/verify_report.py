"""New exact reconstruction from six pairs of Boolean topic memberships.

No import of audit_containment.py, LP, game solver, or third-party package.
The old program is replayed separately by the companion program task.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from math import factorial, prod
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def share(bit, denominator):
    return F(bit, denominator) if bit else F(0)


def signature(atoms):
    t = [atom & 1 for atom in atoms]
    r = [(atom >> 1) & 1 for atom in atoms]
    return sum(t), sum(r), sum(x * y for x, y in zip(t, r))


def main():
    if not __debug__:
        raise RuntimeError("Exact audit requires assertions enabled; do not use -O")
    raw = (HERE / "original.json").read_bytes()
    assert len(raw) == 405
    assert hashlib.sha256(raw).hexdigest() == "9f23473ad97b4d4127c19f9643c3621ca1add12df42b61c662b5c9c0ea985a36"
    old = json.loads(raw)
    # 4^6 ordered pair patterns; this establishes the compressed domain rather
    # than assuming independence of d, ell, and their same-index overlap.
    signature_counts = Counter(signature(atoms) for atoms in product(range(4), repeat=6))
    representatives = {signature(atoms): atoms
                       for atoms in combinations_with_replacement(range(4), 6)}
    assert len(signature_counts) == len(representatives) == 84
    assert sum(signature_counts.values()) == 4096
    for (d, ell, h), multiplicity in signature_counts.items():
        assert max(0, d + ell - 6) <= h <= min(d, ell)
        buckets = (6 - d - ell + h, d - h, ell - h, h)
        assert multiplicity == factorial(6) // prod(factorial(v) for v in buckets)
    expected = {(d, ell, h) for d in range(7) for ell in range(7)
                for h in range(max(0, d + ell - 6), min(d, ell) + 1)}
    assert set(representatives) == expected

    actual_patterns = []
    for bits in product((0, 1), repeat=6):
        e1, e2, e3, e4, a, b = bits
        if a and not (e3 and e4):
            continue
        actual_patterns.append(bits)
    assert len(actual_patterns) == 40

    reduced, all_slacks, nonzero_slacks = {}, [], []
    minima_by_actual = []
    overlap_invariance_checks = 0
    raw_pattern_count = 0
    zero_types = []
    for bits in actual_patterns:
        early, a, b = bits[:4], bits[4], bits[5]
        p = sum(early)
        total = sum(bits)
        actual = [share(bit, total) for bit in bits]
        assert sum(actual) == int(total > 0)
        local_values = []
        for (d, ell, h), atoms in sorted(representatives.items()):
            t = [atom & 1 for atom in atoms]
            r = [(atom >> 1) & 1 for atom in atoms]
            # Direct original query / reply comparisons on a named customer.
            s = 6 * actual[4] - sum(share(ti, p + 1 + ri) for ti, ri in zip(t, r))
            z = 6 * actual[5] - sum(share(ri, p + a + 1) for ri in r)
            v = sum(share(r[i], p + 1 + t[i]) - share(r[j], p + 1 + t[i])
                    for i in range(6) for j in range(6) if i != j)
            both_den = (p + 1) * (p + 2)
            assert s == 6 * actual[4] - F(d, p + 1) + F(h, both_den)
            assert z == 6 * actual[5] - F(ell, p + a + 1)
            assert v == F(d * ell - 6 * h, both_den)
            g = s + z / 12 + v / 6
            assert g == (6 * actual[4] + actual[5] / 2 - F(d, p + 1)
                         - F(ell, 12 * (p + a + 1)) + F(d * ell, 6 * both_den))
            h1 = actual[0] - F(a, 6)
            h2 = actual[1] - F(a, 6)
            last = actual[5] - share(a, p + a + 1)
            slack = 2 * int(total > 0) - int(d > 0) - g - F(5, 4) * (h1 + h2) - last
            assert slack >= 0
            key = (bits, d, ell)
            if key in reduced:
                assert reduced[key] == slack
                overlap_invariance_checks += 1
            reduced[key] = slack
            local_values.append(slack)
            all_slacks.append(slack)
            raw_pattern_count += signature_counts[d, ell, h]
            if total or d or ell:
                nonzero_slacks.append(slack)
            if slack == 0:
                zero_types.append([list(bits), d, ell, h])
        minima_by_actual.append([list(bits), str(min(local_values))])
    assert len(reduced) == 1960 and len(all_slacks) == 3360
    assert raw_pattern_count == 163840

    # Compute F from the path recurrence, independently of the source product.
    current = F(0)
    recurrence = []
    for remaining in range(6, 0, -1):
        current += (1 - current) / (6 * remaining)
        recurrence.append([remaining, str(current)])
    factor = 1 - prod(1 - F(1, 6 * r) for r in range(1, 7))
    assert current == factor
    beta = 1 / current
    assert (1 + beta) / 2 < 2 and 3 - beta > 0
    reconstructed = {
        "status": "passed",
        "scope": "existing conditional coefficient theorem; no unrestricted HALF-6 claim",
        "reduced_states": len(reduced),
        "states_with_feasible_overlap": len(all_slacks),
        "minimum_residual": str(min(all_slacks)),
        "nonzero_state_minimum_residual": str(min(nonzero_slacks)),
        "F6": str(factor),
        "beta": str(beta),
        "multiplicity_two_bound": str((1 + beta) / 2),
        "necessary_single_omission_fraction": str(3 - beta),
    }
    assert reconstructed == old
    report = {
        "status": "all ten frozen fields reproduced by new direct-membership audit",
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "old_report_fields": reconstructed,
        "actual_six_bit_patterns": 40,
        "raw_six_pair_membership_patterns_enumerated": 4096,
        "same_index_pair_count_signatures": 84,
        "complete_raw_bit_domain_represented": raw_pattern_count,
        "raw_domain_note": "163840 is represented by exact signature multiplicities, not separately sampled games or explicit full game trees",
        "direct_S_Z_V_coefficient_cases_checked": len(all_slacks),
        "overlap_invariance_additional_checks": overlap_invariance_checks,
        "nonzero_expanded_types": len(nonzero_slacks),
        "zero_residual_expanded_types": len(zero_types),
        "positive_residual_expanded_types": sum(q > 0 for q in all_slacks),
        "zero_residual_witnesses": zero_types,
        "all_40_actual_pattern_minima": minima_by_actual,
        "all_84_pair_signatures_and_raw_multiplicities": [[*key, value] for key, value in sorted(signature_counts.items())],
        "path_recurrence_unit_demand": recurrence,
        "limits": "Global nonnegative SPE rows require the proved true-history semantics; no game/SPE enumeration, no LP, no unconditional HALF-6 proof.",
    }
    companion = HERE.parent / "early-containment-auditor/rerun/original_stdout.json"
    if companion.exists():
        assert companion.read_bytes() == raw
        report["companion_original_entry_stdout_byte_identical"] = True
        report["companion_original_entry_stdout"] = "../early-containment-auditor/rerun/original_stdout.json"
    (HERE / "independent-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "old_fields_equal": True,
                      "expanded_types": len(all_slacks), "raw_domain_represented": raw_pattern_count,
                      "zero_residual_expanded_types": len(zero_types)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
