"""Exact audit of the continuous-security/log-potential separation family.

This script verifies an algebraic representation boundary, not a SPE or welfare
counterexample. It reads no credentials and imports no equilibrium optimizer.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def query_values(weights, q, k):
    return tuple(sum((F(w, 1) / (1 + k * sum(q[i] for i in range(4)
                                               if mask >> i & 1))
                      for mask, w in weights.items() if mask >> j & 1), F(0))
                 for j in range(4))


def check(m):
    k = m - 1
    a, d = k + 3, 2 * k + 3
    weights = {2: a, 4: a, 8: a, 13: d, 3: a}
    s = F(3*d + 2*a, 4*(d + 2*a))
    eps = F(1, 4*k)
    D, G = F(a, 3), F(d, 3)
    q = (F(0), F(1, 3), F(1, 3), F(1, 3))
    qp = (eps, F(1, 3)-s*eps,
          F(1, 3)-(1-s)*eps/2, F(1, 3)-(1-s)*eps/2)
    assert sum(qp) == 1 and min(qp) >= 0
    at_log = query_values(weights, q, k)
    alternate = query_values(weights, qp, k)
    assert at_log == (F(6),)*4
    assert max(alternate) < 6
    assert sum(weights.values()) == 6*m+9
    # Independently expand each unit client, rather than reuse type sums.
    customers = [mask for mask, w in weights.items() for _ in range(w)]
    expanded = tuple(sum((1 / (1 + k * sum(qp[i] for i in range(4)
                                          if mask >> i & 1))
                         for mask in customers if mask >> j & 1), F(0))
                     for j in range(4))
    assert expanded == alternate
    # The two exact threshold reductions used in the universal argument.
    threshold1 = D*(1-2*s)/(2*k*s*(1-s))
    threshold2 = (s*D-(1-s)*G/2)/(k*s*(1-s))
    assert threshold1 == F(a, 4*k*(d+2*a))*1/(s*(1-s))
    assert threshold2 == 1/(8*k*s*(1-s))
    assert eps < threshold1 and eps < threshold2
    assert s*D-(1-s)*G/2 == F(1, 8)
    return {"m": m, "unit_customers": len(customers),
            "q_prime": list(map(str, qp)), "queries": list(map(str, alternate)),
            "gap_below_log_KKT_value": str(6-max(alternate))}


def main():
    rows = [check(m) for m in list(range(2, 31)) + [50, 100, 1000]]
    # Zero-client and single-topic boundaries of the continuous objective.
    assert query_values({}, (F(1), F(0), F(0), F(0)), 7) == (F(0),)*4
    # m=1 has constant g and no claim of strict log/minimax separation.
    assert query_values({1: 3}, (F(1), F(0), F(0), F(0)), 0)[0] == 3
    report = {"status": "exact algebra audit passed; no SPE claim",
              "checked_players": [r["m"] for r in rows],
              "examples": [rows[0], rows[1], rows[-1]]}
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
