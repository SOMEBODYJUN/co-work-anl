"""Alternating numerical discovery in a complete SPE strategy cone.

The static competitor tuple never observes the query draw. No output proves
anything until recovered as a rational full-strategy certificate.
"""
import argparse
import itertools as it
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from search_cce import data, solve_spe


def security_data(k, m):
    masks = list(range(1, 1 << k))
    covered = np.array([[(mask >> a) & 1 for mask in masks] for a in range(k)])
    bs = list(it.combinations_with_replacement(range(k), m - 1))
    beta = np.array([covered / (1 + np.array([b.count(a) for a in range(k)]) @ covered) for b in bs])
    return bs, beta


def security(r, beta):
    b, k, t = beta.shape
    A = beta @ r
    lp = linprog(np.r_[np.zeros(k), -1], A_ub=np.c_[-A, np.ones(b)], b_ub=np.zeros(b),
                 A_eq=[np.r_[np.ones(k), 0]], b_eq=[1], bounds=[(0, None)] * k + [(None, None)], method="highs")
    assert lp.success
    return lp.x[:-1], lp.x[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--m", type=int, default=3)
    ap.add_argument("--trials", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    k, m = args.k, args.m
    d = data(k, m)
    masks, profiles, counts, ix, uc, wc, g = d
    bs, beta = security_data(k, m)
    rng = np.random.default_rng(args.seed)
    best = -1e10
    for trial in range(args.trials):
        r = rng.integers(0, 8, len(masks)).astype(float)
        r *= rng.random(len(masks)) < .35
        if not r.sum():
            continue
        r /= r.sum()
        target, constraints, sigma = solve_spe(r, d, k, m)
        for step in range(15):
            p, val = security(r, beta)
            gap = m * val - wc[target] @ r
            if gap > best + 1e-9:
                best = gap
                print(json.dumps({"trial": trial, "step": step, "gap": gap, "W": float(wc[target] @ r), "v": val}), flush=True)
                args.out.write_text(json.dumps({"k": k, "m": m, "gap": gap, "masks": masks, "r": r.tolist(), "target": profiles[target], "query_p": p.tolist(), "sigma": {",".join(map(str, h)): a for h, a in sigma.items()}}, indent=2))
            if gap > 1e-7:
                return
            coefficients = np.einsum("a,bat->bt", p, beta)
            lp = linprog(np.r_[wc[target], -m],
                         A_ub=np.concatenate([np.c_[-constraints, np.zeros(len(constraints))], np.c_[-coefficients, np.ones(len(bs))]]),
                         b_ub=np.zeros(len(constraints) + len(bs)),
                         A_eq=[np.r_[np.ones(len(masks)), 0]], b_eq=[1],
                         bounds=[(0, None)] * len(masks) + [(None, None)], method="highs")
            if not lp.success or np.linalg.norm(r - lp.x[:-1]) < 1e-8:
                break
            r = lp.x[:-1]


if __name__ == "__main__":
    main()
