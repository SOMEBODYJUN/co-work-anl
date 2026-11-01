"""Exact type-level audit of RF relaxation; never calls a SPE oracle.

The family is not a SPE counterexample. Run from anywhere; output is fresh stdout.
"""
from fractions import Fraction
from math import lcm
import json


def instance(m):
    d = lcm(*range(1, m + 1))
    scale = m * d
    h = sum((Fraction(1, r) for r in range(1, m + 1)), Fraction())
    rows = []
    for i in range(m):
        for j in range(m):
            rows.append((frozenset((i, m + j)), d // (m - i)))
    private = scale - int(d * h)
    assert private > 0 and d * h == int(d * h)
    for j in range(m):
        rows.append((frozenset((m + j,)), private))
    return rows, scale, h


def payoff(rows, path, player):
    action = path[player]
    return sum((Fraction(count, sum(a in support for a in path))
                for support, count in rows if action in support), Fraction())


def coverage(rows, actions):
    return sum(count for support, count in rows if any(a in support for a in actions))


def audit(m):
    rows, scale, h = instance(m)
    path = tuple(range(m))
    welfare = coverage(rows, path)
    total = sum(count for _, count in rows)
    optimum = coverage(rows, range(m, 2 * m))
    assert optimum == total == m * scale
    assert welfare == scale * h
    actual = [payoff(rows, path, i) for i in range(m)]
    assert sum(actual) == welfare
    checks = 0
    for i in range(m):
        remaining = m - i
        assert actual[i] == Fraction(scale, remaining)
        for action in range(2 * m):
            floor = sum((Fraction(count, sum(a in support for a in path[:i]) + remaining)
                         for support, count in rows if action in support), Fraction())
            assert actual[i] >= floor
            checks += 1
    at_actual_last = [payoff(rows, path[:-1] + (a,), m - 1) for a in range(2 * m)]
    assert at_actual_last[m - 1] == scale
    assert all(v < scale for a, v in enumerate(at_actual_last) if a != m - 1)
    deviating_prefix = path[:-2] + (m - 1,)
    reply_values = [payoff(rows, deviating_prefix + (a,), m - 1) for a in range(2 * m)]
    best = max(reply_values)
    replies = [a for a, v in enumerate(reply_values) if v == best]
    assert replies == list(range(m, 2 * m))
    assert best == scale * (1 - (h - Fraction(1, 2)) / (2 * m))
    for reply in replies:
        dev = payoff(rows, deviating_prefix + (reply,), m - 2)
        assert dev == scale * (1 - Fraction(1, 2 * m)) > actual[m - 2]
    if m >= 5:
        assert optimum > 2 * welfare
    return {"m": m, "L": scale, "customers": total, "W": welfare,
            "OPT": optimum, "ratio": str(Fraction(optimum, welfare)),
            "robust_rows": checks, "last_unique_best_reply": m - 1,
            "penultimate_deviation_profitable_against_every_best_reply": True,
            "is_SPE_counterexample": False}


if __name__ == "__main__":
    print(json.dumps({"claim": "B7-ROBUST-PREFIX-FLOOR-UNBOUNDED-v1",
                      "status": "finite implementation audit, universal proof in note",
                      "results": [audit(m) for m in range(2, 21)]}, indent=2))
