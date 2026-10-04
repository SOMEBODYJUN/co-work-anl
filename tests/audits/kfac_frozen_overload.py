"""Exact independent audit of MF-FROZEN-OVERLOAD-POLY's strict fixture.

This enumerates one small residual game. It does not implement the
published polynomial Nashification algorithm or infer a universal result
from finite tests. No facility_spe solver is imported.
"""
from __future__ import annotations

import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def loads(weights, assignment, k):
    result = [F(0)] * k
    for i, g in enumerate(assignment):
        if g >= 0:
            result[g] += weights[i]
    return result


def is_pure_ne(weights, options, assignment, actual):
    for i, allowed in enumerate(options):
        g = assignment[i]
        if not allowed:
            if g != -1:
                return False
        elif g not in allowed or any(
            actual[g] > weights[i] + actual[h]
            for h in allowed if h != g
        ):
            return False
    return True


def residual_floors(weights, options, layout, ordinary, residual):
    """Use only residual clients and ordinary facility multiplicities."""
    result = {}
    for s in set(layout[g] for g in ordinary):
        q = sum(layout[g] == s for g in ordinary)
        forced = sorted(
            (weights[i] for i in residual
             if {layout[g] for g in options[i]} == {s}),
            reverse=True,
        )
        forced += [F(0)] * q
        remaining = sum(forced, F(0)) - sum(forced[:q - 1], F(0))
        result[s] = min(max(forced[h], remaining / (q - h))
                        for h in range(q))
    return result


def run(root):
    data = json.loads((root / "examples/multi_facility/greedy_cap_obstruction.json").read_text())
    weights = [F(client["weight"]) for client in data["clients"]]
    covers = [set(client["sites"]) for client in data["clients"]]
    assert weights == list(map(F, [20, 8, 24, 20, 10, 30, 13, 67, 20, 20]))
    assert covers == [{0}, {0, 2}, {1, 2, 5}, {2}, {0, 3},
                      {3}, {2, 4}, {4}, {1}, {5}]

    # Verify the exact independent-mixed on-path NE directly from costs.
    q = [1, 1, 2, 1, 3, 0]
    site_assignment = [0, 2, 1, 2, 0, 3, 2, 4, 1, -1]
    site_loads = loads(weights, site_assignment, 6)
    assert site_loads == list(map(F, [30, 44, 41, 30, 67, 0]))
    for i, s in enumerate(site_assignment):
        occupied_options = [t for t in covers[i] if q[t]]
        if not occupied_options:
            assert s == -1
            continue
        assert s in occupied_options
        cost = weights[i] + (site_loads[s] - weights[i]) / q[s]
        assert all(cost <= weights[i] + site_loads[t] / q[t]
                   for t in occupied_options if t != s)
    source_payoff = site_loads[2] / q[2]
    cap = 2 * source_payoff
    assert cap == 41

    onpath_layout = [0, 1, 2, 2, 3, 4, 4, 4]
    mover = 3
    layout = list(onpath_layout)
    layout[mover] = 5
    k = len(layout)
    options = [[g for g, s in enumerate(layout) if s in covers[i]]
               for i in range(len(weights))]
    seed = [0, 0, 1, 2, 0, 4, 6, 5, 1, 3]
    actual = loads(weights, seed, k)
    assert actual == list(map(F, [38, 44, 20, 20, 30, 67, 13, 0]))
    assert all(g in options[i] for i, g in enumerate(seed))
    assert not is_pure_ne(weights, options, seed, actual)

    frozen = {1, 5}
    ordinary = set(range(k)) - frozen
    assert mover in ordinary
    frozen_clients = {i for i, g in enumerate(seed) if g in frozen}
    residual = set(range(len(weights))) - frozen_clients
    assert frozen_clients == {2, 7, 8}
    assert all(actual[g] <= cap for g in ordinary)
    assert all(actual[g] > cap for g in frozen)
    residual_options = [[g for g in options[i] if g in ordinary]
                        if i in residual else []
                        for i in range(len(weights))]
    assert all(seed[i] in residual_options[i] for i in residual)
    floors = residual_floors(weights, residual_options, layout, ordinary, residual)
    assert floors == {0: F(20), 2: F(20), 5: F(20), 3: F(30), 4: F(0)}
    assert sum(layout[g] == 4 for g in ordinary) == 2
    for i in frozen_clients:
        external = actual[seed[i]] - weights[i]
        assert all(external <= actual[g]
                   for g in options[i] if g in frozen and g != seed[i])
        assert all(external <= floors[layout[g]]
                   for g in options[i] if g in ordinary)

    # One strict ordinary move repairs the deliberately non-NE seed.
    repaired = list(seed)
    assert actual[seed[1]] == 38 > weights[1] + actual[2] == 28
    repaired[1] = 2
    final_loads = loads(weights, repaired, k)
    assert final_loads == list(map(F, [30, 44, 28, 20, 30, 67, 13, 0]))
    assert is_pure_ne(weights, options, repaired, final_loads)
    assert final_loads[mover] == 20 <= cap

    # Every pure assignment has a nonmacro cap violation at B, E or G.
    shared = 2
    private = {1: 8, 2: 3, 3: 9}  # facility -> forced client
    assert set(options[shared]) == set(private)
    for g, i in private.items():
        assert options[i] == [g]
        assert weights[i] == 20 and weights[shared] == 24
        assert max(weights[i], weights[shared]) <= cap
        assert weights[i] + weights[shared] == 44 > cap

    # Exhaust all 12 residual assignments; every capped residual NE lifts.
    remaining = sorted(residual)
    feasible_count = ne_count = capped_ne_count = 0
    for choices in product(*(residual_options[i] for i in remaining)):
        feasible_count += 1
        assignment = [-1] * len(weights)
        for i, g in zip(remaining, choices):
            assignment[i] = g
        residual_loads = loads(weights, assignment, k)
        if not is_pure_ne(weights, residual_options, assignment, residual_loads):
            continue
        ne_count += 1
        assert all(residual_loads[g] >= floors[layout[g]] for g in ordinary)
        if any(residual_loads[g] > cap for g in ordinary):
            continue
        capped_ne_count += 1
        full_assignment = list(assignment)
        for i in frozen_clients:
            full_assignment[i] = seed[i]
        full_loads = loads(weights, full_assignment, k)
        assert is_pure_ne(weights, options, full_assignment, full_loads)
        assert full_loads[mover] <= cap
    assert feasible_count == 12
    assert ne_count > 0 and capped_ne_count > 0
    print(f"Verified frozen-overload certificate, strict ordinary repair, full NE, "
          f"global cap impossibility, and {capped_ne_count} lifted capped NEs "
          f"among {ne_count} residual NEs / {feasible_count} assignments")


if __name__ == "__main__":
    run(Path(__file__).resolve().parents[2])
