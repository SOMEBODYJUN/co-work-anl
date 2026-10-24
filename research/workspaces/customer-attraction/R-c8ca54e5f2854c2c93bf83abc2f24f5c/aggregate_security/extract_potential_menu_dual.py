"""One fixed-policy diagnostic for the general aggregate free-column candidate.

Potential values at all m and m-1 multisets are free signed variables.
This extracts and exactly audits a dual, rather than treating LP zero as proof.
No claim for other policies or query laws is made by this script.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

M, K = 3, 6
P = [F(0), F(0), F(1, 2), F(0), F(0), F(1, 2)]
STATES = list(combinations_with_replacement(range(K), M))
STATES += list(combinations_with_replacement(range(K), M - 1))
INDEX = {z: i for i, z in enumerate(STATES)}
D = len(STATES)


def policy(h):
    if not h:
        return 0
    if len(h) == 1:
        return 3 if h[0] < 3 else 0
    group = range(3) if h[1] < 3 else range(3, 6)
    return min(x for x in group if x not in h)


def leaf(h):
    h = list(h)
    while len(h) < M:
        h.append(policy(h))
    return tuple(h)


def utility(z, i):
    r = [F(0)] * D
    r[INDEX[tuple(sorted(z))]] += 1
    r[INDEX[tuple(sorted(z[:i] + z[i + 1:]))]] -= 1
    return r


def subtract(a, b):
    return [x - y for x, y in zip(a, b)]


def exact_solve(matrix, rhs):
    a = [list(row) + [b] for row, b in zip(matrix, rhs)]
    n = len(matrix[0])
    pivot_row = 0
    pivots = []
    for col in range(n):
        selected = next((r for r in range(pivot_row, len(a)) if a[r][col]), None)
        if selected is None:
            continue
        a[pivot_row], a[selected] = a[selected], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [x / scale for x in a[pivot_row]]
        for r in range(len(a)):
            if r != pivot_row and a[r][col]:
                scale = a[r][col]
                a[r] = [x - scale * y for x, y in zip(a[r], a[pivot_row])]
        pivots.append(col)
        pivot_row += 1
    assert all(any(row[:n]) or row[n] == 0 for row in a)
    result = [F(0)] * n
    for r, col in enumerate(pivots):
        result[col] = a[r][n]
    return result


def run():
    z = leaf(())
    rows, labels = [], []
    for i in range(M):
        for h in product(range(K), repeat=i):
            for a in range(K):
                rows.append(subtract(utility(leaf(h), i),
                                     utility(leaf(h + (a,)), i)) + [F(0)] * M)
                labels.append({"kind": "IC", "history": list(h), "action": a})
    for i in range(M):
        for b in range(K):
            q = leaf(z[:i] + (b,))
            v = q[:i] + q[i + 1:]
            r = [sum(P[a] * utility((a,) + v, 0)[j] for a in range(K))
                 for j in range(D)]
            rows.append(r + [-F(j == i) for j in range(M)])
            labels.append({"kind": "MENU", "position": i, "column": b,
                           "opponents": list(v)})
    target = [sum(utility(z, i)[j] for i in range(M)) for j in range(D)]
    target += [-F(1)] * M
    array = np.array(rows, dtype=float).T
    out = linprog(np.zeros(len(rows)), A_eq=array,
                  b_eq=np.array(target, dtype=float), bounds=(0, None),
                  method="highs")
    if not out.success:
        raise RuntimeError(out.message)
    support = [i for i, x in enumerate(out.x) if x > 1e-8]
    basis = [[rows[i][j] for i in support] for j in range(D + M)]
    coeff = exact_solve(basis, target)
    assert all(x >= 0 for x in coeff)
    assert all(sum(x * rows[i][j] for x, i in zip(coeff, support)) == target[j]
               for j in range(D + M))
    cert = [{**labels[i], "coefficient": str(x)}
            for x, i in zip(coeff, support) if x]
    report = {"scope": "fixed six-topic group policy, m=3, p=(e2+e5)/2 only",
              "potential_coordinates": [list(x) for x in STATES],
              "actual_path": list(z), "query": [str(x) for x in P],
              "identity": "W-sum_i H_i = sum lambda IC + sum q MENU",
              "zero_remainder": True, "terms": cert}
    dest = Path(__file__).with_name("potential_menu_dual.json")
    dest.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"audited_coordinates": D + M,
                      "terms": cert}, indent=2))


if __name__ == "__main__":
    run()
