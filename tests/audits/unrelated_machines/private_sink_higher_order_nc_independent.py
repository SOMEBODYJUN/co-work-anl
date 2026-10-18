#!/usr/bin/env python3
"""Independent exact expansion of private-sink upper-cylinder NC laws.

This script imports no repository implementation.  It expands actual labelled
schedules, then computes every job marginal and every same-sink subset event
directly from atom weights.  Finite checks do not replace the general proof.
Run with Python 3; JSON is written to stdout without changing frozen evidence.
"""

from collections import defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import comb
import hashlib
import json
from pathlib import Path
import platform


def rational(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def claimed_tail(k, r, d, q):
    assert 2 <= k <= r and 1 <= d <= k and 1 <= q <= k
    orders = range(2, min(d, q) + 1)
    bounds = [Fraction(comb(k, s), r ** (s - 1) * comb(q, s))
              for s in orders]
    return min([Fraction(1)] + bounds)


def enumerate_law(k, r, d, q):
    """Return (h, per-group sink bit masks) -> exact probability.

    Conditional on B's home h, the distinguished group has a tasks going to its
    sink and k-a other groups each have one.  All labelled choices are listed.
    """
    success_weight = claimed_tail(k, r, d, q)
    branches = [(q, success_weight), (1, 1 - success_weight)]
    atoms = defaultdict(Fraction)
    for distinguished_count, branch_weight in branches:
        if branch_weight == 0:
            continue
        other_count = k - distinguished_count
        denominator = (r * comb(k, distinguished_count)
                       * comb(r - 1, other_count) * k ** other_count)
        weight = branch_weight / denominator
        for h in range(r):
            outside = tuple(i for i in range(r) if i != h)
            for distinguished in combinations(range(k), distinguished_count):
                main_mask = sum(1 << j for j in distinguished)
                for other_groups in combinations(outside, other_count):
                    for other_tasks in product(range(k), repeat=other_count):
                        masks = [0] * r
                        masks[h] = main_mask
                        for group, task in zip(other_groups, other_tasks):
                            masks[group] = 1 << task
                        atoms[(h, tuple(masks))] += weight
    return dict(atoms)


def audit_case(k, r, d, q, check_expectation=False):
    atoms = enumerate_law(k, r, d, q)
    total = sum(atoms.values(), Fraction(0))
    assert total == 1
    b_marginals = [Fraction(0) for _ in range(r)]
    sink_marginals = [[Fraction(0) for _ in range(k)] for _ in range(r)]
    subsets = {
        s: tuple(sum(1 << j for j in js) for js in combinations(range(k), s))
        for s in range(2, k + 1)
    }
    joints = {
        (group, mask): Fraction(0)
        for masks in subsets.values() for group in range(r) for mask in masks
    }
    threshold = 2 - Fraction(q, k)
    success = Fraction(0)
    expected = Fraction(0)
    for (h, masks), weight in atoms.items():
        assert weight > 0 and len(masks) == r and 0 <= h < r
        assert all(0 <= mask < (1 << k) for mask in masks)
        # A mask assigns each original small job to exactly one of its two
        # original finite endpoints; B is assigned to its original home h.
        counts = [mask.bit_count() for mask in masks]
        assert sum(counts) == k
        home_loads = [1 - Fraction(count, k) + int(i == h)
                      for i, count in enumerate(counts)]
        sink_loads = [Fraction(count, k) for count in counts]
        makespan = max(home_loads + sink_loads)
        assert makespan == 2 - Fraction(counts[h], k)
        expected += weight * makespan
        if makespan <= threshold:
            success += weight
        b_marginals[h] += weight
        for group, mask in enumerate(masks):
            for task in range(k):
                if mask & (1 << task):
                    sink_marginals[group][task] += weight
            for s, event_masks in subsets.items():
                for event in event_masks:
                    if (mask & event) == event:
                        joints[(group, event)] += weight
    assert all(value == Fraction(1, r) for value in b_marginals)
    assert all(value == Fraction(1, r)
               for row in sink_marginals for value in row)
    # The complementary home endpoint marginal is 1 - the audited sink marginal.
    assert all(1 - value == Fraction(r - 1, r)
               for row in sink_marginals for value in row)
    order_results = []
    for s in range(2, k + 1):
        values = [joints[(group, event)]
                  for group in range(r) for event in subsets[s]]
        assert min(values) == max(values)  # Checked exchangeability, not assumed.
        upper = Fraction(1, r ** s)
        if s <= d:
            assert all(value <= upper for value in values)
        order_results.append({
            "order": s,
            "labelled_events_checked": len(values),
            "every_event_probability": rational(values[0]),
            "required_upper_bound": rational(upper),
            "is_required": s <= d,
            "satisfies_bound": max(values) <= upper,
        })
    target = claimed_tail(k, r, d, q)
    assert success == target
    if check_expectation:
        assert d == k and q == 2 and r >= max(k, comb(k, 2))
        expected_minimum = 2 - Fraction(1, k) - Fraction(k - 1, 2 * r)
        assert expected == expected_minimum
    return {
        "k": k, "r": r, "d": d, "q": q,
        "actual_labelled_atoms": len(atoms),
        "total_probability": rational(total),
        "B_marginals": [rational(value) for value in b_marginals],
        "every_small_sink_marginal": rational(sink_marginals[0][0]),
        "every_small_home_marginal": rational(1 - sink_marginals[0][0]),
        "actual_success_probability": rational(success),
        "claimed_sharp_success_probability": rational(target),
        "expected_makespan": rational(expected),
        "all_required_subset_events_checked": True,
        "orders": order_results,
        "also_checks_all_order_sharp_expectation": check_expectation,
    }


def main():
    parameters = [
        (2, 2, 1, 2),  # No NC constraint; q-type, rather than 1-type, is needed.
        (2, 2, 2, 1),
        (2, 2, 2, 2),
        (3, 3, 1, 3),
        (3, 3, 2, 2),
        (3, 3, 3, 3),
        (3, 3, 2, 3),
        (3, 4, 3, 2),
        (4, 4, 2, 2),
        (4, 4, 2, 3),
        (4, 4, 3, 3),
        (4, 4, 4, 3),
        (4, 4, 3, 4),
        (4, 6, 4, 4),
        (4, 6, 4, 1),
    ]
    cases = [audit_case(*parameter) for parameter in parameters]
    expectation_cases = [audit_case(k, r, k, 2, check_expectation=True)
                         for k, r in [(2, 2), (2, 4), (3, 3), (3, 9), (4, 6)]]
    this_file = Path(__file__)
    output = {
        "purpose": "independent fully expanded Fraction check; no author imports",
        "python": platform.python_version(),
        "arithmetic": "Fraction and integers only",
        "seed": None,
        "script_sha256": hashlib.sha256(this_file.read_bytes()).hexdigest(),
        "tail_cases": cases,
        "all_order_expectation_cases": expectation_cases,
        "tail_case_count": len(cases),
        "expectation_case_count": len(expectation_cases),
        "total_atoms_checked_with_multiplicity": sum(
            case["actual_labelled_atoms"] for case in cases + expectation_cases),
        "limitations": [
            "Finite labelled cases verify the construction, not the universal upper bound.",
            "Only positive-cylinder upper NC is asserted; no all-zero NC is assumed.",
            "Conditional-history sampling bound is proved separately, not simulated.",
            "No general scheduling or certificate-generation algorithm is implemented.",
        ],
        "passed": True,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
