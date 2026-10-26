#!/usr/bin/env python3
"""Exact finite audit for CA-HALF-RESTART-PRICE-CONTROL-v1.

The analytic proof is in candidates/half_restart_absorption.md.  This script
only checks arithmetic, nonunique maximizers, self loops, and a tight case.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def stationary_restart(kernel, restart):
    """Solve 2p-pT=r over Fractions by Gaussian elimination."""
    n = len(kernel)
    mat = []
    for j in range(n):
        row = [(F(2) if j == k else F(0)) - kernel[k][j] for k in range(n)]
        mat.append(row + [restart[j]])
    for col in range(n):
        pivot = next(i for i in range(col, n) if mat[i][col])
        mat[col], mat[pivot] = mat[pivot], mat[col]
        q = mat[col][col]
        mat[col] = [x / q for x in mat[col]]
        for i in range(n):
            if i == col or not mat[i][col]:
                continue
            q = mat[i][col]
            mat[i] = [x - q * y for x, y in zip(mat[i], mat[col])]
    return [mat[i][-1] for i in range(n)]


def check(kernel, P, g, gamma, restart, sign=1):
    n = len(kernel)
    p = stationary_restart(kernel, restart)
    pt = [sum(p[i] * kernel[i][j] for i in range(n)) for j in range(n)]
    boundary = sum(p[i] * kernel[i][j] * (P[j] - P[i])
                   for i in range(n) for j in range(n))
    query_gap = gamma - sum(p[i] * g[i] for i in range(n))
    H = [P[i] / 2 + sign * g[i] for i in range(n)]
    assert sum(p) == 1 and all(x >= 0 for x in p)
    assert all(pt[j] <= 2 * p[j] for j in range(n))
    assert all(restart[i] == 0 or H[i] == max(H) for i in range(n))
    if sign == 1:
        assert boundary / 2 <= query_gap
        decomposition = (sum(restart[i] * H[i] for i in range(n))
                         - sum(p[i] * H[i] for i in range(n))
                         + gamma - sum(restart[i] * g[i] for i in range(n)))
        assert query_gap - boundary / 2 == decomposition
        return p, query_gap - boundary / 2
    joint = boundary / 2 + query_gap
    restart_gap = gamma - sum(restart[i] * g[i] for i in range(n))
    assert joint <= restart_gap
    return p, restart_gap - joint


def main():
    cases = 0
    min_slack = None
    min_reverse_slack = None
    tight = None
    # All 2-state deterministic kernels, small integral prices.
    for image in product(range(2), repeat=2):
        kernel = [[F(int(image[i] == j)) for j in range(2)] for i in range(2)]
        for P in product(range(-2, 3), repeat=2):
            P = list(map(F, P))
            for g0 in product(range(-2, 3), repeat=2):
                g = list(map(F, g0))
                gamma = max(g)
                H = [P[i] / 2 + g[i] for i in range(2)]
                maxima = [i for i, x in enumerate(H) if x == max(H)]
                restarts = []
                for i in maxima:
                    r = [F(0), F(0)]; r[i] = 1; restarts.append(r)
                if len(maxima) == 2:
                    restarts.append([F(1, 3), F(2, 3)])
                for restart in restarts:
                    p, slack = check(kernel, P, g, gamma, restart, sign=1)
                    cases += 1
                    if min_slack is None or slack < min_slack:
                        min_slack = slack
                        tight = dict(image=image, P=P, g=g, restart=restart, p=p)
                J = [P[i] / 2 - g[i] for i in range(2)]
                for i in [j for j, x in enumerate(J) if x == max(J)]:
                    restart = [F(0), F(0)]; restart[i] = 1
                    _, reverse_slack = check(kernel, P, g, gamma, restart, sign=-1)
                    if min_reverse_slack is None or reverse_slack < min_reverse_slack:
                        min_reverse_slack = reverse_slack
    out = {
        "claim": "CA-HALF-RESTART-PRICE-CONTROL-v1",
        "status": "PASS",
        "exact_cases": cases,
        "minimum_slack": str(min_slack),
        "minimum_reverse_slack": str(min_reverse_slack),
        "tight_case": {k: [str(x) for x in v] if isinstance(v, (list, tuple)) else v
                       for k, v in tight.items()},
        "scope": "finite arithmetic audit only; reverse sign cancels Qinput only when restart is full-price",
    }
    target = Path(__file__).with_name("half_restart_audit.json")
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
