"""Independent rational saddle certificates for the published insurance menu.

Build each terminal count directly from BASE at the root.  The general
proof is algebraic; these finite checks only audit that exact matrix.
"""
from fractions import Fraction as F
from itertools import product
import json


def check(m):
    labels = tuple(product(range(m), range(m - 1)))

    def entry(query, anchor):
        a, b = anchor
        qa, qb = query
        economic = [0] * m
        banks = [1] * (m - 1)
        economic[a] = m - 1
        economic[1 if a == 0 else 0] += 1
        banks[b] += 1
        return F(1, 1 + economic[qa]) + F(2, 1 + banks[qb])

    # Independent primal columns and dual query weights have the same support.
    support = tuple((a, b) for a, b in labels if a != 0)
    primal_rows = [sum((entry(q, a) for a in support), F(0)) / len(support)
                   for q in labels]
    dual_columns = [sum((entry(q, a) for q in support), F(0)) / len(support)
                    for a in labels]
    value = F(2) - F(1, m) - F(1, 3 * (m - 1))
    assert max(primal_rows) == min(dual_columns) == value
    root = F(1) + F(1, m - 1)
    assert value > root
    assert value < F(2)  # This family does not obstruct Mpath <= W/m.
    return {"m": m, "topics": len(labels), "value": str(value),
            "root_payoff": str(root), "gap": str(value - root),
            "primal_max": str(max(primal_rows)),
            "dual_min": str(min(dual_columns))}


if __name__ == "__main__":
    print(json.dumps({"scope": "finite saddle-certificate audit; not a general proof",
                      "cases": [check(m) for m in (4, 5, 7)]}, indent=2))
