"""Exact arithmetic on the strict star-edge separation example.

Run: python3 tests/audits/kfac_star_edges.py
The finite check is not a proof of the general algorithm.
"""

import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / "examples/multi_facility/greedy_star_edges.json").read_text())
SITES = DATA["sites"]
WEIGHT = [F(row["weight"]) for row in DATA["clients"]]
OPTIONS = [set(row["sites"]) for row in DATA["clients"]]


def totals(a):
    return {t: sum((WEIGHT[i] for i, v in enumerate(a) if v == t), F(0))
            for t in SITES}


def audit():
    q = {t: 0 for t in SITES}
    a = [None] * len(WEIGHT)
    trace = []
    for _ in range(DATA["k"]):
        w = totals(a)
        score = {t: w[t] / (q[t] + 1) if q[t] else
                 sum((WEIGHT[i] for i, v in enumerate(a)
                      if v is None and t in OPTIONS[i]), F(0)) for t in SITES}
        t = max(SITES, key=lambda s: score[s])
        assert list(score.values()).count(score[t]) == 1
        trace.append((t, score[t]))
        if q[t] == 0:
            for i in range(len(a)):
                if a[i] is None and t in OPTIONS[i]:
                    a[i] = t
        q[t] += 1
    assert trace == [("H", 180), ("M", 95), ("H", 90),
                     ("H", 60), ("M", F(95, 2)), ("L", 47)]
    assert a == ["H", "M", "L", "H", "H"]
    assert [q[t] for t in SITES] == [3, 2, 1]
    assert totals(a) == {"H": 180, "M": 95, "L": 47}
    assert F(180 - 36, 3) > F(95, 2)
    assert F(180 - 44, 3) <= F(47)
    a[3] = "M"
    assert totals(a) == {"H": 144, "M": 131, "L": 47}
    w = totals(a)
    assert all(q[t] * 47 <= w[t] <= (q[t] + 1) * 47 for t in SITES)
    assert all((w[a[i]] - WEIGHT[i]) / q[a[i]] <= w[t] / q[t]
               for i in range(len(a)) for t in OPTIONS[i] if t != a[i])
    assert F(180 - 36, 3) > F(95, 2)  # Initial RANGE check fails.
    print("PASS: strict star greedy trace, unequal light weights, box and exact NE")


if __name__ == "__main__":
    audit()
