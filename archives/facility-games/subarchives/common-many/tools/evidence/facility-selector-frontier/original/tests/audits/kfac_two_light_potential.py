"""Exact fixed-instance audit of the two-unequal-light potential obstruction.

Run: python3 tests/audits/kfac_two_light_potential.py
This checks one input and the stated parameter family at selected values;
the family proof is algebraic in polytime_frontier.md.
"""

import itertools
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / "examples/multi_facility/greedy_two_light_potential.json").read_text())
SITES = DATA["sites"]
WEIGHTS = [F(x["weight"]) for x in DATA["clients"]]
ACCESS = [set(x["sites"]) for x in DATA["clients"]]


def totals(assignment, weights=WEIGHTS):
    return {s: sum((weights[i] for i, t in enumerate(assignment) if t == s), F(0))
            for s in SITES}


def greedy(weights=WEIGHTS):
    q = {s: 0 for s in SITES}
    a = [None] * len(weights)
    trace = []
    for _ in range(7):
        w = totals(a, weights)
        scores = {s: w[s] / (q[s] + 1) if q[s] else
                  sum((weights[i] for i, v in enumerate(a)
                       if v is None and s in ACCESS[i]), F(0)) for s in SITES}
        t = max(SITES, key=lambda s: scores[s])
        assert list(scores.values()).count(scores[t]) == 1
        trace.append((t, scores[t]))
        if q[t] == 0:
            for i in range(len(a)):
                if a[i] is None and t in ACCESS[i]:
                    a[i] = t
        q[t] += 1
    return q, a, trace


def potential(a, q, weights=WEIGHTS):
    return sum((sum((weights[i] * weights[j] for i in range(len(a))
                     for j in range(i + 1, len(a)) if a[i] == a[j] == t), F(0))
                / q[t] for t in SITES), F(0))


def ne(a, q, weights=WEIGHTS):
    w = totals(a, weights)
    return all((w[a[i]] - weights[i]) / q[a[i]] <= w[t] / q[t]
               for i in range(len(a)) for t in ACCESS[i] if t != a[i])


def audit(n):
    assert n >= 45 and n % 5 == 0
    weights = [F(16 * n, 5) - 1, F(2 * n), F(n + 2), F(n),
               F(4 * n, 5), F(n - 1)]
    q, initial, trace = greedy(weights)
    assert trace == [("H", 4*n-1), ("M", 3*n-1),
                     ("H", F(4*n-1, 2)), ("M", F(3*n-1, 2)),
                     ("H", F(4*n-1, 3)), ("L", n+2), ("R", n)]
    assert [q[t] for t in SITES] == [1, 3, 2, 1]
    assert initial == ["H", "M", "L", "R", "H", "M"]
    states = {}
    for x, y in itertools.product(["H", "M"], ["M", "L"]):
        a = initial[:4] + [x, y]
        w = totals(a, weights)
        assert all(w[t] >= q[t] * n for t in SITES)
        states[(x, y)] = (potential(a, q, weights), w, ne(a, q, weights))
    assert states[("M", "L")][0] < min(v[0] for key, v in states.items()
                                       if key != ("M", "L"))
    assert states[("H", "M")][2] and states[("M", "L")][2]
    assert all(q[t]*n <= states[("H", "M")][1][t] <= (q[t]+1)*n for t in SITES)
    assert states[("M", "L")][1]["L"] == 2*n+1
    if n == 45:
        assert {key: v[0] for key, v in states.items()} == {
            ("H", "M"): 3696, ("H", "L"): 3784,
            ("M", "M"): 4392, ("M", "L"): 3688}
    return trace


if __name__ == "__main__":
    assert [F(x["weight"]) for x in DATA["clients"]] == [143, 90, 47, 45, 36, 44]
    for n in (45, 50, 100, 1000):
        audit(n)
    print("PASS: strict greedy; four feasible states; unique overflowing potential minimum and box NE")
