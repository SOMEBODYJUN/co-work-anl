"""Numerical discovery only; outputs require exact independent verification."""
import argparse
import itertools as it
import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def data(k, m):
    masks = list(range(1, 1 << k))
    covered = np.array([[(mask >> a) & 1 for mask in masks] for a in range(k)])
    profiles = list(it.combinations_with_replacement(range(k), m))
    counts = [tuple(s.count(a) for a in range(k)) for s in profiles]
    ix = {q: i for i, q in enumerate(counts)}
    u = np.empty((len(profiles), k, len(masks)))
    w = np.empty((len(profiles), len(masks)))
    g = np.empty((len(profiles), k, len(masks)))
    for j, q in enumerate(counts):
        load = np.array(q) @ covered
        w[j] = load > 0
        u[j] = covered / np.maximum(load, 1)
        for a in range(k):
            dev = np.zeros(len(masks))
            for b, qb in enumerate(q):
                if qb:
                    dev += qb * covered[a] / np.maximum(load - covered[b] + covered[a], 1)
            g[j, a] = w[j] - dev
    return masks, profiles, counts, ix, u, w, g


def solve_spe(r, d, k, m):
    masks, profiles, counts, ix, uc, wc, g = d
    u, w = uc @ r, wc @ r

    @lru_cache(None)
    def outcomes(q):
        if sum(q) == m:
            return (ix[q],)
        child = [outcomes(tuple(q[b] + (a == b) for b in range(k))) for a in range(k)]
        floor = max(min(u[j, a] for j in ch) for a, ch in enumerate(child))
        return tuple(sorted({j for a, ch in enumerate(child) for j in ch if u[j, a] >= floor - 1e-9}))

    root = outcomes((0,) * k)
    target = min(root, key=lambda j: (w[j], j))
    sigma, constraints = {}, []

    def expand(h, q, desired):
        if len(h) == m:
            return desired
        childq = [tuple(q[b] + (a == b) for b in range(k)) for a in range(k)]
        children = [outcomes(qa) for qa in childq]
        floor = max(min(u[j, a] for j in ch) for a, ch in enumerate(children))
        a = next(a for a, ch in enumerate(children) if desired in ch and u[desired, a] >= floor - 1e-9)
        sigma[h] = a
        for b, ch in enumerate(children):
            jd = desired if b == a else min(ch, key=lambda j: (u[j, b], j))
            expand(h + (b,), childq[b], jd)
            constraints.append(uc[desired, a] - uc[jd, b])
        return desired

    expand((), (0,) * k, target)
    return target, np.array(constraints), sigma


def cce(r, d):
    *_, uc, wc, g = d
    lp = linprog(wc @ r, A_ub=-(g @ r).T, b_ub=np.zeros(g.shape[1]),
                 A_eq=np.ones((1, len(wc))), b_eq=[1], bounds=(0, None), method="highs")
    assert lp.success
    return lp.fun, -lp.ineqlin.marginals, lp.x


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
    rng = np.random.default_rng(args.seed)
    best = -1e10
    for trial in range(args.trials):
        r = rng.integers(0, 8, len(masks)).astype(float)
        r *= rng.random(len(masks)) < .5
        if not r.sum():
            continue
        r /= r.sum()
        target, constraints, sigma = solve_spe(r, d, k, m)
        for step in range(12):
            val, y, lam = cce(r, d)
            gap = val - wc[target] @ r
            if gap > best + 1e-9:
                best = gap
                print(json.dumps({"trial": trial, "step": step, "gap": gap, "w": float(wc[target] @ r), "cce": val}), flush=True)
                args.out.write_text(json.dumps({"k": k, "m": m, "gap": gap, "masks": masks, "r": r.tolist(), "target": profiles[target], "dual_y": y.tolist(), "sigma": {",".join(map(str, h)): a for h, a in sigma.items()}}, indent=2))
            if gap > 1e-7:
                return
            coefficients = wc - np.einsum("a,jat->jt", y, g) - wc[target]
            # Maximize t with static CCE dual lower bound minus the SPE welfare.
            lp = linprog(np.r_[np.zeros(len(masks)), -1.],
                         A_ub=np.concatenate([np.c_[-constraints, np.zeros(len(constraints))], np.c_[-coefficients, np.ones(len(wc))]]),
                         b_ub=np.zeros(len(constraints) + len(wc)),
                         A_eq=[np.r_[np.ones(len(masks)), 0]], b_eq=[1],
                         bounds=[(0, None)] * len(masks) + [(None, None)], method="highs")
            if not lp.success or np.linalg.norm(r - lp.x[:-1]) < 1e-8:
                break
            r = lp.x[:-1]


if __name__ == "__main__":
    main()
