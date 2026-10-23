"""Diagnostic LP for a general VA(r) mechanism; not an SPE oracle.

Customer multiplicities are normalized by actual leader utility = 1.
The LP retains true all-B terminal BRs, root comparison to one true
off-path branch T,Y, and prefix-specific unconditional action guarantees
on that branch. A negative objective only refutes this necessary-condition
proof template, never VA or the half-coverage conjecture.
"""

import argparse
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def solve(r, background):
    patterns = list(itertools.product((0, 1), repeat=r + 3))[1:]
    # Membership coordinates: A, B, T, Y_1, ..., Y_r.
    p = np.array(patterns, dtype=float)
    a, b, t = p[:, 0], p[:, 1], p[:, 2]
    ys = p[:, 3:]
    leader = a / (background + 1 + r * b)
    tax = a * (1 - b) / ((background + 1) * (background + 2))
    query = t / (background + 1 + r * b)
    offloads = t + ys.sum(axis=1)
    true_t = t / np.maximum(1, background + offloads)
    rows = []
    names = []

    def add(name, slack):
        names.append(name)
        rows.append(-slack)

    # On-path last player is B; hence B^r is static PNE in b+A.
    b_pay = b / (background + a + r)
    for j in range(r + 3):
        s = p[:, j]
        add(f"actual_last_vs_{j}", b_pay - s / (background + a + 1 + (r - 1) * b))
    add("root_true_T", leader - true_t)

    for j in range(r + 3):
        s = p[:, j]
        add(f"root_safe_{j}", leader - s / (background + r + 1))

    # At each actual off-path prefix, deviation to any S guarantees this
    # payoff even if all still-unmoved followers cover every S customer.
    for i in range(r):
        true_i = ys[:, i] / np.maximum(1, background + offloads)
        prev = ys[:, :i].sum(axis=1)
        for j in range(r + 3):
            s = p[:, j]
            safe = s / (background + t + prev + 1 + (r - i - 1))
            add(f"off_{i}_safe_{j}", true_i - safe)

    obj = leader + tax - query
    result = linprog(obj, A_ub=np.array(rows), b_ub=np.zeros(len(rows)),
                     A_eq=leader[None, :], b_eq=[1], bounds=(0, None), method="highs")
    out = {"r": r, "background": background, "success": bool(result.success),
           "message": result.message, "scope": "necessary-condition relaxation only"}
    if result.success:
        out["objective"] = float(result.fun)
        out["customers"] = [{"membership": list(map(int, patterns[j])), "weight": float(x)}
                            for j, x in enumerate(result.x) if x > 1e-8]
        out["dual_rows"] = {name: float(-v) for name, v in zip(names, result.ineqlin.marginals)
                            if abs(v) > 1e-8}
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("r", type=int)
    parser.add_argument("--background", type=int, default=0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    out = solve(args.r, args.background)
    text = json.dumps(out, indent=2)
    if args.output:
        args.output.write_text(text + "\n")
    print(text)
