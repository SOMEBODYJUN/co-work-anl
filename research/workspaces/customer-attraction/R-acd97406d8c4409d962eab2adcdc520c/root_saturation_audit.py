"""Finite exact stress test of the root/last-node branch inequality.

The theorem is analytic. This independently enumerates small branches having
only the hypotheses used by the proof, including empty topics and repeated
choices. Run from repository root, optionally --output new.json.
"""
import argparse
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def payoff(sets, i):
    return sum((F(1, sum(x in s for s in sets)) for x in sets[i]), F(0))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    checked = 0
    feasible = 0
    # Ground-set relabelling lets C be the first K customers.
    for n in range(4):
        subsets = [frozenset(x for x in range(n) if mask >> x & 1)
                   for mask in range(1 << n)]
        for m in range(2, 6):
            for K in range(n + 1):
                C = frozenset(range(K))
                legal = [s for s in subsets if len(s) <= K]
                for tail in product(legal, repeat=m - 1):
                    branch = (C,) + tail
                    v, t = payoff(branch, 0), payoff(branch, m - 1)
                    E = m * v - K
                    assert E >= 0
                    d = sum(m - sum(x in s for s in branch) for x in C)
                    dL = len(C - branch[-1])
                    assert F(d, m * (m - 1)) <= v - F(K, m)
                    assert t <= v + F(m - 2, m - 1) * dL
                    for D in legal:
                        checked += 1
                        deviation = payoff(branch[:-1] + (D,), m - 1)
                        if t < deviation:
                            continue
                        feasible += 1
                        lhs = m * len(D - C) + len(D & C)
                        rhs = K + (m - 1) ** 2 * E
                        assert lhs <= rhs, (n, m, branch, D, lhs, rhs)
    for k in range(101):
        assert F(k, k + 1) <= F(k, 2)
    result = {"scope": "ground set 0..3, players 2..5, all branches and D of size <= K",
              "branch_D_pairs": checked, "last_reply_feasible_pairs": feasible,
              "status": "passed", "arithmetic": "fractions.Fraction",
              "meaning": "finite implementation check, not a general proof"}
    if args.output:
        with args.output.open("x") as f:
            json.dump(result, f, indent=2)
            f.write("\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
