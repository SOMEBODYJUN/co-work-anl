"""Finite necessary-condition experiment; this does NOT produce an SPE.

Only actual paths and m comparison topics are represented.  AP is the old
arbitrary-theme background near-saturation row, imposed at each actual node.
"""
from pathlib import Path
import argparse
import json

import numpy as np
from scipy.optimize import linprog


def build(m, maxima=None):
    labels = 2 * m
    masks = np.arange(1, 1 << labels, dtype=np.int64)
    bit = ((masks[None, :] >> np.arange(labels)[:, None]) & 1).astype(float)
    actual_count = bit[:m].sum(axis=0)
    covered = (actual_count > 0).astype(float)
    opt = (bit[m:].sum(axis=0) > 0).astype(float)
    rows, names = [], []
    for i in range(m):
        k = m - i
        b = bit[:i].sum(axis=0)
        u = np.divide(bit[i], actual_count, out=np.zeros_like(covered), where=actual_count > 0)
        sizes = bit / (b + k)
        for c in range(labels):
            rows.append(sizes[c] - u)
            names.append(f"floor:{i}:{c}")
        if k == 1:
            continue
        if maxima is not None:
            assigned = maxima[i] if isinstance(maxima[i], list) else [maxima[i]]
            cs = sorted(set(c for a in assigned for c in ([a] if a < m else list(range(m, labels)))))
            for c in cs:
                for t in range(labels):
                    rows.append(sizes[t] - sizes[c])
                    names.append(f"maximum:{i}:{c}:{t}")
                coefficient = (k - 1) * (m - 1)
                for d in range(labels):
                    f = bit[d] * (bit[c] / (b + k) + (1 - bit[c]) / (b + 1))
                    rows.append(f + (coefficient - 1) * sizes[c] - coefficient * u)
                    names.append(f"BNS:{i}:{c}:{d}")
        p = (k - 1) * (m - 1) + k * k / 2
        for c in range(labels):
            for d in range(labels):
                f = bit[d] * (bit[c] / (b + k) + (1 - bit[c]) / (b + 1))
                rows.append(f + (p - 1) * sizes[c] - p * u)
                names.append(f"AP:{i}:{c}:{d}")
    return masks, covered, opt, np.asarray(rows), names


def run(m, output, symmetric=False, maxima=None):
    masks, covered, opt, rows, names = build(m, maxima)
    if symmetric:
        groups = np.array([[a + (1 << (m + t)) - 1 for t in range(m)]
                           for a in range(1 << m)])
        rows = rows[:, groups].mean(axis=2)
        covered = covered[groups].mean(axis=1)
        opt = opt[groups].mean(axis=1)
        masks = np.arange(1 << m)
    result = linprog(-opt, A_ub=rows, b_ub=np.zeros(len(rows)), A_eq=covered[None, :],
                     b_eq=[1], bounds=(0, None), method="highs")
    report = {"m": m, "status": result.status, "message": result.message,
              "variables": len(masks), "rows": len(rows), "symmetric_opt_singletons": symmetric,
              "designated_maxima": maxima,
              "scope": "Necessary projection only; no SPE construction."}
    if result.success:
        report.update({"optimum_float": -result.fun,
                       "atoms_float": [{"mask": int(masks[j]), "mass": float(x)}
                                       for j, x in enumerate(result.x) if x > 1e-9],
                       "positive_dual_rows": [{"row": names[j], "weight": float(-v)}
                                              for j, v in enumerate(result.ineqlin.marginals) if v < -1e-9],
                       "min_slack_float": float(np.min(-rows @ result.x))})
    if output:
        Path(output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k:v for k,v in report.items() if k not in {"atoms_float", "positive_dual_rows"}}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("m", type=int)
    parser.add_argument("--output")
    parser.add_argument("--symmetric", action="store_true")
    parser.add_argument("--maxima", nargs="*")
    args = parser.parse_args()
    maxima = [[int(v) for v in word.split(",")] for word in args.maxima] if args.maxima else None
    run(args.m, args.output, args.symmetric, maxima)
