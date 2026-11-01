"""Exploration: full SPE tree, local cylinders, and global low-degree lift.

All floating outputs are candidates only.  The moment vector need not have a
common nonnegative customer realization.  A degree-two lift is strictly more
than each terminal support having an independent nonnegative realization.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[5]
SOURCE = ROOT / "research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/round3_moments/probe_local_cone.py"
spec = importlib.util.spec_from_file_location("local_moment_probe", SOURCE)
local = importlib.util.module_from_spec(spec)
spec.loader.exec_module(local)


class LiftProblem(local.Problem):
    def __init__(self, m, p, degree):
        super().__init__(m, p)
        self.degree = degree
        self.types = list(range(1, 1 << p))
        self.n = self.d + len(self.types)
        self.lift_masks = [s for s in self.ms if s.bit_count() <= degree]
        self.lift = np.zeros((len(self.lift_masks), self.n))
        for j, s in enumerate(self.lift_masks):
            self.lift[j, self.ix[s]] = 1
            for k, b in enumerate(self.types):
                if s & b == s:
                    self.lift[j, self.d + k] = -1
        self.bounds = [(None, None)] * self.d + [(0, None)] * len(self.types)
        self.local_ext = np.pad(self.local_np, ((0, 0), (0, len(self.types))))
        self.single_ext = np.r_[self.single, np.zeros(len(self.types))]

    def random_t(self, rng):
        obj = np.r_[[rng.uniform(-1, 1) for _ in range(self.d)], np.zeros(len(self.types))]
        lp = linprog(obj, A_ub=-self.local_ext, b_ub=np.zeros(len(self.local)),
                     A_eq=np.vstack([self.lift, self.single_ext]),
                     b_eq=np.r_[np.zeros(len(self.lift)), 1], bounds=self.bounds,
                     method="highs")
        if not lp.success:
            raise RuntimeError(lp.message)
        return lp.x[:self.d]

    def optimize(self, sigma):
        rows, ids, root = self.rows(sigma)
        c = np.r_[np.array(self.cover(sum(1 << a for a in set(root))), dtype=float),
                  np.zeros(len(self.types))]
        incentives = np.pad(np.array(rows, dtype=float), ((0, 0), (0, len(self.types))))
        A = np.vstack([-self.local_ext, -incentives])
        best = None
        for J in itertools.combinations(range(self.p), min(self.m, self.p)):
            o = np.r_[np.array(self.cover(sum(1 << a for a in J)), dtype=float),
                      np.zeros(len(self.types))]
            lp = linprog(-o, A_ub=A, b_ub=np.zeros(len(A)),
                         A_eq=np.vstack([self.lift, c]),
                         b_eq=np.r_[np.zeros(len(self.lift)), 1], bounds=self.bounds,
                         method="highs")
            if lp.status == 3:
                return {"unbounded": True, "root": root, "J": J, "sigma": sigma}
            if lp.success and (best is None or -lp.fun > best["ratio"] + 1e-8):
                best = {"ratio": -lp.fun, "t": lp.x[:self.d],
                        "lift": lp.x[self.d:], "root": root, "J": J, "sigma": sigma}
        return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, default=3)
    ap.add_argument("--p", type=int, default=5)
    ap.add_argument("--degree", type=int, default=2)
    ap.add_argument("--trials", type=int, default=50)
    ap.add_argument("--seed", type=int, default=741227)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    pr = LiftProblem(args.m, args.p, args.degree)
    rng = random.Random(args.seed)
    best_ratio = 0
    best = None
    seen = set()
    for trial in range(args.trials):
        t = pr.random_t(rng)
        sigma, _ = pr.policy(t, rng.randrange(2**32))
        fingerprint = tuple(sorted(sigma.items()))
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        result = pr.optimize(sigma)
        if result is not None and (result.get("unbounded") or result["ratio"] > best_ratio + 1e-8):
            best = result
            best_ratio = result.get("ratio", float("inf"))
            data = local.serial(pr, result)
            data.update({"identity": "floating exploration only; not an SPE customer instance",
                         "degree": args.degree, "seed": args.seed, "trial": trial,
                         "seen": len(seen), "lift": {
                             str(b): str(F(float(x)).limit_denominator(1000000))
                             for b, x in zip(pr.types, result.get("lift", [])) if x > 1e-10}})
            args.output.write_text(json.dumps(data, indent=2) + "\n")
            print(json.dumps({"trial": trial, "seen": len(seen), "ratio": best_ratio,
                              "root": result["root"]}), flush=True)
        if best_ratio > 2.000001:
            break
    print(json.dumps({"finished": True, "m": args.m, "p": args.p, "degree": args.degree,
                      "trials": args.trials, "seen": len(seen), "best": best_ratio}), flush=True)


if __name__ == "__main__":
    main()
