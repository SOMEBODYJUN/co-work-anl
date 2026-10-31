"""Enumerate the two original destinations of every original job; no formula oracle."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def construct(p, a, b, c):
    # Machine identities H_r=r, A_r=p+r, R=2p, S=2p+1.
    jobs = []
    for r in range(p):
        jobs.append([(r, a[r]), (p + r, F(1))])
    for r in range(p):
        jobs.append([(p + r, F(1)), (2 * p, b[r])])
    jobs.append([(2 * p, c), (2 * p + 1, F(1))])
    return jobs


def actual(jobs, mask, machine_count):
    load = [F(0) for _ in range(machine_count)]
    destinations = []
    for j, options in enumerate(jobs):
        machine, cost = options[(mask >> j) & 1]
        destinations.append(machine)
        load[machine] += cost
    return max(load), destinations, load


def formula_fee(total, c, beta):
    if total > beta:
        return None
    return int(c + total > beta)


def audit_case(p, a, b, c, name):
    assert p >= 1 and len(a) == len(b) == p
    assert all(0 < t <= 1 for t in a + b) and 0 < c <= 1
    assert c + sum(b, F(0)) >= 1
    jobs = construct(p, a, b, c)
    by_pattern = [[None, None] for _ in range(1 << p)]
    witnesses = [[None, None] for _ in range(1 << p)]
    assignments = 1 << len(jobs)
    for mask in range(assignments):
        peak, _, _ = actual(jobs, mask, 2 * p + 2)
        pattern = mask & ((1 << p) - 1)
        fee = (mask >> (2 * p)) & 1
        old = by_pattern[pattern][fee]
        if old is None or peak < old:
            by_pattern[pattern][fee] = peak
            witnesses[pattern][fee] = mask

    assert min(min(v) for v in by_pattern) == 1
    assert actual(jobs, 0, 2 * p + 2)[0] == 1
    for r in range(p):
        mask = (1 << r) | (1 << (p + r)) | (1 << (2 * p))
        assert actual(jobs, mask, 2 * p + 2)[0] == 1

    fee_checks = 0
    nonempty_tradeoff_checks = 0
    rows = []
    for pattern, by_fee in enumerate(by_pattern):
        total = sum((b[r] for r in range(p) if (pattern >> r) & 1), F(0))
        expected_opt = min(F(2), max(F(1), total))
        assert min(by_fee) == expected_opt, (name, pattern, by_fee, total)
        assert (min(by_fee) <= 1) == (total <= 1)

        beta_set = {F(1), F(5, 4), F(3, 2), F(7, 4), F(199, 100)}
        for endpoint in {total, total + c} | set(by_fee):
            if 1 <= endpoint < 2:
                beta_set.add(endpoint)
                beta_set.add((1 + endpoint) / 2)
                beta_set.add((2 + endpoint) / 2)
        for beta in sorted(beta_set):
            feasible_fees = [fee for fee in (0, 1) if by_fee[fee] <= beta]
            actual_fee = min(feasible_fees) if feasible_fees else None
            expected_fee = formula_fee(total, c, beta)
            assert actual_fee == expected_fee, (
                name, pattern, str(beta), actual_fee, expected_fee, by_fee
            )
            fee_checks += 1
            if pattern and total <= 1:
                indices = [r for r in range(p) if (pattern >> r) & 1]
                if all(formula_fee(b[r], c, beta) == 1 for r in indices):
                    assert len(indices) * (beta - c) < total <= 1
                    if beta >= F(3, 2):
                        assert len(indices) <= 1
                    nonempty_tradeoff_checks += 1

        # At beta=2 all query patterns have a complete fee-zero witness.
        assert by_fee[0] <= 2
        if p <= 2:
            rows.append({
                "pattern": pattern,
                "B_K": str(total),
                "opt": str(min(by_fee)),
                "best_peak_fee0": str(by_fee[0]),
                "best_peak_fee1": str(by_fee[1]),
                "original_assignment_masks": witnesses[pattern],
            })
    return {
        "name": name,
        "p": p,
        "a": list(map(str, a)),
        "b": list(map(str, b)),
        "c": str(c),
        "original_assignments_enumerated": assignments,
        "patterns_checked": 1 << p,
        "closed_threshold_fee_checks": fee_checks,
        "nonempty_tradeoff_checks": nonempty_tradeoff_checks,
        "small_pattern_certificates": rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New JSON output path; an existing file is never replaced.')
    parser.add_argument('--source-file', type=Path, action='append', default=[], help='Optional proof or statement files whose hashes should be retained.')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output already exists; choose a new path')
    cases = []
    for p in range(1, 7):
        a = [F(1, 100 + p + r) for r in range(p)]
        for s in range(1, p + 1):
            for c in (F(1), F(2, 3), F(1, 10)):
                cases.append(audit_case(p, a, [F(1, s)] * p, c, f"uniform_p{p}_s{s}_c{c}"))

    rng = random.Random(2026101811)
    choices = [F(1), F(1, 2), F(1, 3), F(1, 4), F(2, 3), F(3, 4), F(1, 100)]
    for k in range(48):
        p = rng.randrange(1, 7)
        a = [F(1, rng.randrange(1, 10000)) for _ in range(p)]
        b = [rng.choice(choices) for _ in range(p)]
        c = rng.choice([F(1), F(1, 2), F(9, 10), F(1, 100)])
        if sum(b, F(0)) + c < 1:
            c = F(1)
        cases.append(audit_case(p, a, b, c, f"heterogeneous_{k}"))

    # Exact equality c+sum(b)=1 is permitted, including p=1 and an empty pattern.
    cases.append(audit_case(1, [F(1, 1000)], [F(1, 3)], F(2, 3), "domain_equality"))
    # The initial fixed source is not tiny; the query initial times are tiny.
    cases.append(audit_case(4, [F(1, 1000000)] * 4, [F(1)] * 4, F(99, 100), "nearunit_old_fee"))

    # Preserve an executable test that v1 item 7 fails at K=empty; v2 excludes it.
    empty_sum = F(0)
    v1_empty_strict_inequality = 0 * (F(3, 2) - F(1)) < empty_sum
    assert not v1_empty_strict_inequality

    files = [Path(__file__).resolve()] + [path.resolve() for path in args.source_file]
    output = {
        "status": "all_exact_finite_checks_passed",
        "scope": "raw original two-destination assignments only; not a general proof or source decoder",
        "case_count": len(cases),
        "assignment_count": sum(v["original_assignments_enumerated"] for v in cases),
        "pattern_count": sum(v["patterns_checked"] for v in cases),
        "closed_threshold_fee_checks": sum(v["closed_threshold_fee_checks"] for v in cases),
        "v1_empty_set_counterexample_reproduced": True,
        "source_sha256": {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in files},
        "cases": cases,
    }
    path = args.output.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as stream:
        stream.write(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: output[key] for key in ("status", "case_count", "assignment_count", "pattern_count", "closed_threshold_fee_checks", "v1_empty_set_counterexample_reproduced")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
