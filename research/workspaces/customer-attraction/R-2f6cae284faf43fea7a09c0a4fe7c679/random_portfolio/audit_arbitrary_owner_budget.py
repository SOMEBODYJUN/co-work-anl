#!/usr/bin/env python3
"""Exact single-customer regression for ANY-OWNER-REPEAT and fixed endpoints.

This does not search for SPE, prove a finite-player target, or import a solver.
The arbitrary-m proof is in the accompanying manuscript.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json


def harmonic(a):
    return sum((Q(1, k) for k in range(1, a + 1)), Q(0))


def owner_potential(covered, owner):
    return Q(1) - (Q(1, len(covered) + 1) if owner not in covered else Q(0))


def error(covered, current, owner):
    return Q(1, len(covered)) - (
        owner_potential(covered, owner)
        - owner_potential(covered - {current}, owner)
    )


def subsets(items):
    items = list(items)
    for bits in range(1 << len(items)):
        yield frozenset(x for j, x in enumerate(items) if bits >> j & 1)


def audit(max_m=8):
    n_states = n_budgets = n_symmetric = 0
    for m in range(1, max_m + 1):
        universe = frozenset(range(m))
        for comparison_cover in subsets(universe):
            if not comparison_cover:
                continue
            a = len(comparison_cover)
            for owner in comparison_cover:
                sum_max = Q(0)
                owner_rank = sorted(comparison_cover).index(owner) + 1
                for ordinal, current in enumerate(sorted(comparison_cover), 1):
                    forced = frozenset(i for i in comparison_cover if i <= current)
                    worst = Q(0)
                    for future in subsets(range(current + 1, m)):
                        covered = forced | future
                        actual = error(covered, current, owner)
                        if ordinal < owner_rank:
                            bound = Q(1, ordinal + 1)
                        elif ordinal == owner_rank:
                            bound = Q(0)
                        else:
                            bound = Q(1, ordinal)
                        assert Q(0) <= actual <= bound
                        # The shorter reviewer proof: all earlier nonowners
                        # and the current nonowner are in the fixed prefix.
                        if current != owner:
                            nonowner_rank = len([i for i in comparison_cover
                                                 if i <= current and i != owner])
                            assert actual <= Q(1, nonowner_rank + 1)
                        worst = max(worst, actual)
                        n_states += 1
                    sum_max += worst
                assert sum_max <= harmonic(a) - 1
                # Every term's maximum is attained by some independently
                # chosen suffix. This exact identity checks sharpness of
                # the prefix-only relaxation, not simultaneous SPE play.
                assert sum_max == harmonic(a) - 1
                n_budgets += 1
        for covered in subsets(universe):
            c = len(covered)
            average_f = sum((owner_potential(covered, o) for o in universe), Q(0)) / m
            assert average_f == Q((m + 1) * c, m * (c + 1))
            total_e = sum((sum((error(covered, i, o) for i in covered), Q(0))
                           for o in universe), Q(0)) / m
            assert total_e == (Q(m * c - 1, m * (c + 1)) if c else Q(0))
            if c:
                for i in covered:
                    average_e = sum((error(covered, i, o) for o in universe), Q(0)) / m
                    assert average_e == Q(m * c - 1, m * c * (c + 1))
            n_symmetric += 1
        if m >= 2:
            for c in range(1, m):
                e0 = Q(m * c - 1, m * c * (c + 1))
                e1 = Q(m * (c + 1) - 1, m * (c + 1) * (c + 2))
                assert e0 - e1 == Q(m * c - 2, m * c * (c + 1) * (c + 2)) >= 0
    return {
        "status": "PASS",
        "scope": "single-customer algebra regression; no SPE or half claim",
        "max_m_regression_only": max_m,
        "prefix_states": n_states,
        "arbitrary_owner_prefix_budgets": n_budgets,
        "uniform_owner_fixed_endpoint_states": n_symmetric,
        "claims": ["rank bound", "arbitrary fixed owner H_a-1 bound",
                   "prefix-only algebraic sharpness", "uniform owner endpoint F",
                   "uniform owner endpoint error", "symmetric error monotonicity"]
    }


if __name__ == "__main__":
    result = audit()
    encoded = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    Path(__file__).with_name("arbitrary_owner_budget_audit.json").write_text(encoded)
    print(encoded, end="")
