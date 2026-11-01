#!/usr/bin/env python3
"""Definition-level finite audit; the adjacent markdown proves arbitrary q."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json


def policy(h, q, variant):
    a, b = h.count(0), h.count(1)
    if a >= q:
        return 1
    if b >= q:
        return 0
    if variant == 0:
        return 0 if not h else 1
    # Deliberately order-sensitive: 01 and 10 have distinct weighted sums.
    modulus = variant + 2
    residue = (variant + sum((i + 1) * (v + 1) for i, v in enumerate(h))) % modulus
    return int(residue >= modulus // 2)


def audit_tree(q, variant):
    m = 2 * q

    @lru_cache(None)
    def terminal(h):
        if len(h) == m:
            return h
        return terminal(h + (policy(h, q, variant),))

    comparisons = 0
    for d in range(m):
        for h in product(range(2), repeat=d):
            chosen = policy(h, q, variant)
            followed = terminal(h)
            current = F(1, followed.count(chosen))
            for dev in range(2):
                other = terminal(h + (dev,))
                deviation = F(1, other.count(dev))
                assert current >= deviation, (q, variant, h, chosen, dev)
                comparisons += 1
            a, b = h.count(0), h.count(1)
            if a < q and b < q:
                assert followed.count(0) == followed.count(1) == q
            elif a >= q:
                assert followed[d:] == (1,) * (m - d)
            else:
                assert followed[d:] == (0,) * (m - d)
    path = terminal(())
    assert path.count(0) == path.count(1) == q
    if variant == 0:
        assert path == (0,) + (1,) * q + (0,) * (q - 1)
    return comparisons


def audit_budget(q, rho):
    m = 2 * q
    path = (0,) + (1,) * q + (0,) * (q - 1)
    congestion = [F(0)] * m
    total = F(0)
    for j in range(1, q):
        slot = q + 1 + j  # 1-indexed
        theta = F(1, j)
        congestion[slot - 1] += j * theta
        error = F(0)
        for client in (0, 1):
            background = path[:j].count(client)
            inserted = int(path[slot - 1] == client)
            error += background * (
                1 / (background + rho) - 1 / (background + rho + inserted)
            )
        assert error == 1 / ((rho + 1) * (rho + 2))
        total += theta * error
    harmonic = sum((F(1, j) for j in range(1, q)), F(0))
    assert total == harmonic / ((rho + 1) * (rho + 2))
    assert max(congestion, default=F(0)) == (1 if q >= 2 else 0)
    return total


def main():
    comparisons = sum(audit_tree(q, variant) for q in range(1, 7) for variant in range(4))
    budget_cases = 0
    for q in range(1, 80):
        for rho in (F(1, 3), F(1), F(5, 2), F(7)):
            audit_budget(q, rho)
            budget_cases += 1
    print(json.dumps({
        "scope": "finite definition audit; arbitrary-q proof is in adjacent markdown",
        "unit_customers": 2,
        "catalog": [["x"], ["y"]],
        "all_ordered_history_q": [1, 6],
        "history_dependent_policy_variants": 4,
        "spe_comparisons": comparisons,
        "fraction_budget_cases": budget_cases,
        "root_welfare": 2,
        "slot_congestion": 1,
        "rent_rho_1": "H_(q-1)/6",
        "rent_over_W_rho_1": "H_(q-1)/12 -> infinity",
        "general_target": "OPEN; the SPE family has OPT=W=2"
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
