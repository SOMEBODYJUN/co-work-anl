"""Independent exact arithmetic check of SC-K-GREEDY-CAP-INFEASIBLE.

No constructor import, random sampling, or search-based universal inference.
The general cap impossibility is the forced private-20 plus shared-24 proof
in the mathematical account; the loop below checks its three possible homes.
"""
from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "examples/multi_facility/greedy_cap_obstruction.json"


def loads(weights, assignment, number_of_bins):
    out = [F(0)] * number_of_bins
    for i, f in enumerate(assignment):
        if f >= 0:
            out[f] += weights[i]
    return out


def check_ne(weights, covers, layout, assignment):
    actual = loads(weights, assignment, len(layout))
    for i, f in enumerate(assignment):
        available = [g for g, site in enumerate(layout) if site in covers[i]]
        assert (f in available) if available else (f == -1)
        if f >= 0:
            assert all(actual[f] <= actual[g] + weights[i] for g in available)
    return actual


def run():
    data = json.loads(DATA.read_text())
    weights = [F(c["weight"]) for c in data["clients"]]
    covers = [set(c["sites"]) for c in data["clients"]]
    assert len(weights) == 10 and data["k"] == 8 and data["m"] == 6
    q, W, site_assignment = [0] * 6, [F(0)] * 6, [-1] * 10
    chosen = []
    for _ in range(data["k"]):
        scores = [W[s] / (q[s] + 1) if q[s] else
                  sum((weights[i] for i in range(10)
                       if site_assignment[i] < 0 and s in covers[i]), F(0))
                  for s in range(6)]
        s = max(range(6), key=lambda j: (scores[j], -j))
        chosen.append((s, scores[s]))
        if q[s] == 0:
            for i in range(10):
                if site_assignment[i] < 0 and s in covers[i]:
                    site_assignment[i] = s
                    W[s] += weights[i]
        q[s] += 1
    assert chosen == [(4, 80), (2, 52), (3, 40), (4, 40),
                      (4, F(80, 3)), (2, 26), (0, 20), (1, 20)]
    assert q == [1, 1, 2, 1, 3, 0]
    costs = []
    for i, target in [(1, 0), (4, 0), (6, 2), (1, 2), (2, 1)]:
        source = site_assignment[i]
        old = weights[i] + (W[source] - weights[i]) / q[source]
        new = weights[i] + W[target] / q[target]
        assert new < old
        costs.append((old, new))
        W[source] -= weights[i]
        W[target] += weights[i]
        site_assignment[i] = target
    assert costs == [(30, 28), (40, 38), (F(106, 3), 35),
                     (38, F(73, 2)), (F(89, 2), 44)]
    assert W == [30, 44, 41, 30, 67, 0]

    # Site-uniform independent mixing: check actual conditional costs.
    layout = tuple(s for s in range(6) for _ in range(q[s]))
    for i, site in enumerate(site_assignment):
        available_sites = [s for s in range(6) if q[s] and s in covers[i]]
        if not available_sites:
            assert site == -1
            continue
        own_cost = weights[i] + (W[site] - weights[i]) / q[site]
        assert all(own_cost <= weights[i] + W[t] / q[t]
                   for t in available_sites if t != site)
    assert W[2] / q[2] == F(41, 2)

    deviation = list(layout)
    b_labels = [f for f, s in enumerate(layout) if s == 2]
    deviator = b_labels[1]
    deviation[deviator] = 5
    # Private weight-20 clients at B/E/G force 20+24 on one of them.
    private = {2: 3, 1: 8, 5: 9}
    assert all(covers[i] == {s} and weights[i] == 20
               for s, i in private.items())
    assert covers[2] == set(private) and weights[2] == 24
    assert all(weights[private[s]] + weights[2] == 44 > 41
               for s in covers[2])
    assert all(weights[i] <= 41 for i in [2, *private.values()])

    # Independent explicit pure NE of the actual deviation layout.
    # The three D labels are 5,6,7; the deviator G is label 3.
    offpath = [0, 2, 1, 2, 0, 4, 6, 5, 1, deviator]
    actual = check_ne(weights, covers, deviation, offpath)
    assert actual == [30, 44, 28, 20, 30, 67, 13, 0]
    assert actual[deviator] == 20 <= 2 * F(41, 2)
    print("Exact greedy scores, five strict moves, on-path NE, forced cap 44,"
          " and off-path low-deviator NE verified")


if __name__ == "__main__":
    run()
