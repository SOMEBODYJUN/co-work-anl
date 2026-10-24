"""Exploratory LP boundary for the frozen worst-denominator Farkas template.

This is not a theorem or a counterexample to Q-CAG-HALF.  It checks the
deterministic singleton family described in notes/direct_farkas_and_static_lp_boundary.md.
"""
import numpy as np
from scipy.optimize import linprog


def feasible(m: int) -> bool:
    # Actual S_i={y_i}; comparison T_j={x_j}; all 2m customers are distinct.
    n = 2 * m
    p = m * m
    rows, rhs = [], []
    actual = [{m + i} for i in range(m)]
    target = [{j} for j in range(m)]
    for x in range(n):
        row = np.zeros(p)
        c = sum(x in actual[i] for i in range(m))
        d = sum(x in target[j] for j in range(m))
        for i in range(m):
            b = sum(x in actual[k] for k in range(i))
            remaining = m - i
            for j in range(m):
                row[i * m + j] = (
                    (1 / c if c and x in actual[i] else 0)
                    - (1 / (b + remaining) if x in target[j] else 0)
                )
        rows.append(row)
        rhs.append(2 * int(c > 0) - int(d > 0))
    result = linprog(
        np.zeros(p),
        A_ub=np.asarray(rows),
        b_ub=np.asarray(rhs),
        bounds=[(0, None)] * p,
        method="highs",
    )
    return bool(result.success)


if __name__ == "__main__":
    for m in range(2, 15):
        print(m, feasible(m))

