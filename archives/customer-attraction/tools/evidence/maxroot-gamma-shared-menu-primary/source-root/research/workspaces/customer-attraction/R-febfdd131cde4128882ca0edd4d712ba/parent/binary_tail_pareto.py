"""Discovery only: a binary-background four-tail certificate tradeoff.

Every column is one complete membership assignment, not a sampled game.
Any floating answer still needs exact multipliers and independent auditing.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog


def quotient(n, d):
    return F(n, d) if n else F(0)


NAMES = []


def coefficients(p, eta, e):
    a, b, c, d, q, r, s = eta
    actual = (a, b, c, d)
    off = (d, q, r, s)
    labels = dict(zip("abcdqrs", eta))
    rows = []
    names = []
    for path_name, path, indices in (("actual", actual, range(4)), ("off", off, range(1, 4))):
        for i in indices:
            own = quotient(path[i], p + sum(path))
            denom = p + sum(path[:i]) + 4 - i
            for label, bit in labels.items():
                names.append(f"{path_name}:{i}:K:{label}")
                rows.append(own - quotient(bit, denom))
            names.append(f"{path_name}:{i}:sum-opt")
            rows.append(4 * own - quotient(e, denom))
        pref = p + sum(path[:2])
        H = quotient(path[2] + path[3], p + sum(path)) + quotient(path[2], (pref + 1) * (pref + 2))
        names.append(path_name + ":pair-opt")
        rows.append(6 * H - quotient(e * (4 - e), pref + 1) - quotient(e * (e - 1), pref + 2))
    names.append("root-copy-d")
    rows.append(quotient(a, p + sum(actual)) - quotient(d, p + sum(off)))
    # The original aggregate corrections are independently valid too.
    D = (p + 1) * (p + 2) * (p + 3) * (p + 4)
    v2 = a + b
    delta2 = F(1, p + 1) - F(1, p + v2 + 1) + (F(2 * p * p, 3 * D) if v2 == 2 else 0)
    v3 = a + b + c
    delta3 = F(1, p + 1) - F(1, p + v3 + 1) + (F(p * p + p, D) if v3 == 3 else 0)
    pref = p + a + b
    H = quotient(c + d, p + sum(actual)) + quotient(c, (pref + 1) * (pref + 2))
    target = quotient(e, p + e)
    names.extend(("old-P", "old-E"))
    rows.extend((2 * H + delta2 - target, 4 * quotient(d, p + sum(actual)) + delta3 - target))
    return names, rows, target, quotient(sum(actual), p + sum(actual))


def solve(beta0):
    columns = []
    rhs = []
    for p, eta, e in product(range(2), product(range(2), repeat=7), range(5)):
        names, rows, target, V = coefficients(p, eta, e)
        columns.append([float(x) for x in rows] + [-float(V) if p else 0.0])
        rhs.append(float((beta0 * V if not p else 0) - target))
    objective = [0.0] * len(names) + [1.0]
    result = linprog(objective, A_ub=np.array(columns), b_ub=np.array(rhs), bounds=[(0, None)] * len(objective), method="highs")
    report = {"status": "floating discovery only", "beta0": str(beta0), "success": bool(result.success), "message": result.message}
    if result.success:
        report.update(beta1=float(result.fun), multipliers={n: float(v) for n, v in zip(names, result.x[:-1]) if abs(v) > 1e-9}, min_slack=float(np.min(np.array(rhs)-np.array(columns) @ result.x)))
    return report


def exact_fixed(beta0=F(2), beta1=F(5, 3), filename="binary_tail_exact.json"):
    exact_A, exact_b, states = [], [], []
    for p, eta, e in product(range(2), product(range(2), repeat=7), range(5)):
        names, rows, target, V = coefficients(p, eta, e)
        exact_A.append(rows)
        exact_b.append((beta1 if p else beta0) * V - target)
        states.append((p, eta, e))
    A = np.array(exact_A, dtype=float)
    b = np.array(exact_b, dtype=float)
    result = linprog(np.ones(len(names)), A_ub=A, b_ub=b, bounds=(0, None), method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    support = np.flatnonzero(result.x > 1e-8)
    active = np.flatnonzero(b-A @ result.x < 1e-8)
    _, R, pivots = qr(A[active][:, support].T, pivoting=True)
    selected = active[pivots[:len(support)]]
    matrix = [[exact_A[i][j] for j in support] + [exact_b[i]] for i in selected]
    for j in range(len(support)):
        pivot = next(i for i in range(j, len(support)) if matrix[i][j])
        matrix[j], matrix[pivot] = matrix[pivot], matrix[j]
        factor = matrix[j][j]
        matrix[j] = [x / factor for x in matrix[j]]
        for i in range(len(support)):
            if i == j or not matrix[i][j]:
                continue
            factor = matrix[i][j]
            matrix[i] = [x-factor*y for x,y in zip(matrix[i],matrix[j])]
    solution = [row[-1] for row in matrix]
    weights = {names[j]: F(v) for j, v in zip(support, solution)}
    assert all(v >= 0 for v in weights.values())
    residuals = [bb - sum(weights.get(n, 0) * a for n, a in zip(names, row)) for row, bb in zip(exact_A, exact_b)]
    assert min(residuals) >= 0
    report = {"status": "exact all-type author certificate; independent audit pending", "beta0": str(beta0), "beta1": str(beta1), "multipliers": {n: str(v) for n,v in weights.items()}, "states": len(states), "min_residual": str(min(residuals)), "zero_residuals": sum(x == 0 for x in residuals)}
    Path(__file__).with_name(filename).write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact", action="store_true")
    parser.add_argument("--beta0", type=F, default=F(2))
    parser.add_argument("--beta1", type=F, default=F(5, 3))
    parser.add_argument("--output", default="binary_tail_exact.json")
    args = parser.parse_args()
    if args.exact:
        print(json.dumps(exact_fixed(args.beta0, args.beta1, args.output), indent=2))
        raise SystemExit(0)
    output = [solve(x) for x in (F(2), F(1499,750), F(21,10), F(5,2))]
    path = Path(__file__).with_suffix(".json")
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))
