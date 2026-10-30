"""Exact fixed 26-unit-customer witness; no optimizer and no SPE claim.

Source: frozen quadratic_meta_nash_gap.md, source ID e2807d4a6bc0b716313c.
This reconstructs the three matrices from individual customers, then checks
the explicit matching minimax certificates and the positive leading minors.
The all-distributions conclusion uses the accompanying algebraic proof.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import argparse
import json


def determinant(matrix):
    n = len(matrix)
    total = F(0)
    for perm in permutations(range(n)):
        inversions = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = F((-1) ** inversions)
        for i, j in enumerate(perm):
            term *= matrix[i][j]
        total += term
    return total


def audit():
    customers = [frozenset(s) for s, count in [((0,), 6), ((0, 1), 6), ((1, 2), 8), ((2,), 6)] for _ in range(count)]
    assert len(customers) == 26
    f = [sum(F(1) for c in customers if t in c) for t in range(3)]
    h = [[sum((F(1, 2) for c in customers if t in c and a in c), F(0)) for a in range(3)] for t in range(3)]
    k = [[sum((F(1, 1 + (a in c)) for c in customers if t in c), F(0)) for a in range(3)] for t in range(3)]
    assert f == [12, 14, 14]
    assert all(k[t][a] == f[t] - h[t][a] for t in range(3) for a in range(3))
    minors = [determinant([row[:i] for row in h[:i]]) for i in (1, 2, 3)]
    assert minors == [6, 33, 135]
    p = [F(4, 14), F(3, 14), F(7, 14)]
    q = [F(0), F(5, 6), F(1, 6)]
    lam = [F(1, 2), F(0), F(1, 2)]
    assert all(sum(v) == 1 and min(v) >= 0 for v in (p, q, lam))
    kp = [sum(k[t][a] * p[a] for a in range(3)) for t in range(3)]
    kq = [sum(k[t][a] * q[a] for a in range(3)) for t in range(3)]
    lk = [sum(lam[t] * k[t][a] for t in range(3)) for a in range(3)]
    assert kp == [F(135, 14)] * 3
    assert kq == [F(19, 2), F(15, 2), F(19, 2)]
    assert lk == [F(10), F(19, 2), F(19, 2)]
    assert max(kq) == min(lk) == F(19, 2)
    assert kp[0] - max(kq) == F(1, 7)
    return {"unit_customers": 26, "background": "zero", "f": list(map(str, f)),
            "H": [list(map(str, row)) for row in h], "K": [list(map(str, row)) for row in k],
            "leading_principal_minors": list(map(str, minors)), "p": list(map(str, p)),
            "q": list(map(str, q)), "row_certificate": list(map(str, lam)),
            "Kp": list(map(str, kp)), "Kq": list(map(str, kq)), "lambdaK": list(map(str, lk)),
            "minimax": "19/2", "self_response": "135/14", "gap": "1/7",
            "scope": "fixed static matrix certificates; no complete SPE counterexample"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit("Assertions must remain enabled.")
    result = audit()
    encoded = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x") as stream:
            stream.write(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
