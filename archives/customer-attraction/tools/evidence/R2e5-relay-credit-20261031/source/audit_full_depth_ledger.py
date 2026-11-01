#!/usr/bin/env python3
"""Definition-level exact checks for the full-depth ledger and sharp-family stop.

Run from anywhere. Writes only when --output PATH is explicitly supplied.
No imports from the existing SPE solver or other audit implementations.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from itertools import permutations, product
import json
import random
from pathlib import Path


def payoffs(catalog, outcome):
    clients = set().union(*catalog) if catalog else set()
    loads = {x: sum(x in catalog[a] for a in outcome) for x in clients}
    us = [sum((Q(1, loads[x]) for x in catalog[a]), Q(0)) for a in outcome]
    welfare = sum(v > 0 for v in loads.values())
    assert sum(us, Q(0)) == welfare
    return us, welfare, loads


def continuation(h, m, policy):
    out = tuple(h)
    while len(out) < m:
        out += (policy(out),)
    return out


def ledger(catalog, h, a, m, policy):
    i = len(h)
    before = continuation(h, m, policy)
    after = continuation(tuple(h) + (a,), m, policy)
    u, w, loads = payoffs(catalog, before)
    v, ww, loads2 = payoffs(catalog, after)
    gamma = u[i] - v[i]
    tail = sum(v[i + 1 :], Q(0)) - sum(u[i + 1 :], Q(0))
    old = sum(v[:i], Q(0)) - sum(u[:i], Q(0))
    assert ww - w == tail + old - gamma
    old_by_clients = Q(0)
    clients = set().union(*catalog)
    for x in clients:
        b = sum(x in catalog[t] for t in h)
        if b:
            old_by_clients += b * (Q(1, loads2[x]) - Q(1, loads[x]))
    assert old == old_by_clients
    return gamma, tail, old, ww - w


def sharp_catalog(m):
    # label 0: m distinct B clients; labels 1..m-1: distinct private clients.
    return [frozenset(range(m))] + [frozenset([m + j]) for j in range(m - 1)]


def harmonic(m):
    return sum((Q(1, q) for q in range(1, m + 1)), Q(0))


def tuple_ledger(catalog, t, policy):
    m = len(t)
    gamma_sum = tail_sum = old_sum = Q(0)
    h = ()
    for a in t:
        gamma, tail, old, _ = ledger(catalog, h, a, m, policy)
        assert gamma >= 0
        gamma_sum += gamma
        tail_sum += tail
        old_sum += old
        if a:
            r = m - len(h)
            b = h.count(0)
            assert b + r - 1 > 0
            assert gamma == Q(m, b + r) - 1
            assert tail == Q((r - 1) * m, (b + r - 1) * (b + r))
            assert old == Q(b * m, (b + r - 1) * (b + r))
        else:
            assert gamma == tail == old == 0
        h += (a,)
    actual_w = payoffs(catalog, continuation((), m, policy))[1]
    compare_w = payoffs(catalog, t)[1]
    assert tail_sum + old_sum - gamma_sum == compare_w - actual_w
    assert tail_sum + old_sum == m * (harmonic(m) - 1)
    assert gamma_sum == m * harmonic(m) - 2 * m + 1
    return gamma_sum, tail_sum, old_sum


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    spe_nodes = spe_comparisons = tuple_count = algebra_edges = 0
    policy = lambda h: 0

    # All complete ordered histories for each of these entire games.
    for m in range(2, 7):
        catalog = sharp_catalog(m)
        for depth in range(m):
            for h in product(range(m), repeat=depth):
                spe_nodes += 1
                own = payoffs(catalog, continuation(h, m, policy))[0][depth]
                assert own >= 1
                for a in range(m):
                    gamma, _, _, _ = ledger(catalog, h, a, m, policy)
                    assert gamma >= 0
                    spe_comparisons += 1

    # Every optimal ordering, not just one representative per B position.
    for m in range(2, 8):
        catalog = sharp_catalog(m)
        for t in permutations(range(m)):
            tuple_ledger(catalog, t, policy)
            tuple_count += 1

    # Larger variable-player formula checks, each possible B position.
    examples = []
    for m in range(2, 81):
        harmonic_fee = m * (harmonic(m) - 1)
        for pos in range(m):
            seq = list(range(1, m))
            seq.insert(pos, 0)
            denominators = [m - depth + int(depth > pos)
                            for depth, a in enumerate(seq) if a]
            assert sorted(denominators) == list(range(2, m + 1))
        fee = harmonic_fee
        assert (fee > m) == (m >= 4)
        # Disjoint sources at the actual prefixes: source i pays singleton i+1.
        for i in range(m - 1):
            tail = Q(m - i - 1, m - 1)
            old = Q(i, m - 1)
            assert tail + old == 1
            if m <= 10:
                gamma, actual_tail, actual_old, delta_w = ledger(
                    sharp_catalog(m), (0,) * i, i + 1, m, policy)
                assert gamma == 0 and delta_w == 1
                assert (actual_tail, actual_old) == (tail, old)
        if m in (2, 3, 4, 5, 10, 20, 40, 80):
            examples.append({"m": m, "W": m, "OPT": 2 * m - 1,
                             "relay_fee": str(fee),
                             "regret_sum": str(m * harmonic(m) - 2 * m + 1),
                             "relay_fee_over_W": str(fee / m)})

    # Arbitrary prescribed strategies: check only the identities, not SPE.
    # Empty theme and zero-client cases are included explicitly.
    rng = random.Random(20261023)
    zero_cases = 0
    for trial in range(60):
        m = rng.randrange(1, 6)
        n = rng.randrange(0, 8)
        k = rng.randrange(1, 5)
        catalog = [frozenset(x for x in range(n) if rng.randrange(2)) for _ in range(k)]
        catalog[0] = frozenset()
        zero_cases += n == 0
        # Genuinely ordered-history-dependent complete policy, unrelated to counts.
        def arbitrary_policy(h, trial=trial, k=k):
            return (trial + sum((j + 3) * (a + 1) ** 2 for j, a in enumerate(h))) % k
        for depth in range(m):
            for h in product(range(k), repeat=depth):
                for a in range(k):
                    ledger(catalog, h, a, m, arbitrary_policy)
                    algebra_edges += 1

    report = {
        "status": "all_exact_checks_passed",
        "scope": "Finite regression; general statements rely on the written proof.",
        "sharp_family_complete_SPE": {"m_min": 2, "m_max": 6,
                                      "all_ordered_histories": spe_nodes,
                                      "all_action_comparisons": spe_comparisons},
        "all_optimal_permutations": {"m_min": 2, "m_max": 7, "count": tuple_count},
        "variable_m_formulas": {"m_min": 2, "m_max": 80,
                                "each_B_position_denominator_multiset_checked": True,
                                "actual_prefix_fan_definition_check_m_max": 10},
        "arbitrary_strategy_algebra": {"instances": 60, "edges": algebra_edges,
                                        "zero_client_instances": zero_cases,
                                        "empty_theme_in_every_instance": True,
                                        "SPE_claim": False},
        "examples": examples,
    }
    result = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(result + "\n", encoding="utf-8")
    print(result)


if __name__ == "__main__":
    main()
