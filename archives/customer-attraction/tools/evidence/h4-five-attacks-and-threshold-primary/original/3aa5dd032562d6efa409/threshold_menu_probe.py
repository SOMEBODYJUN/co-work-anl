"""Attack a precisely stated all-input threshold extension candidate.

For r terminal players and a root menu A -> B(A), root payoff < t, every
tail payoff >= t. Test whether this can coexist with a fixed query p whose
extra-slot payoff is > t in every menu column. No SPE assertion is made.
Finite runs are only attacks on this generic terminal-combination lemma.
"""
import itertools
import json
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def run(k, r, trials, seed):
    rng = np.random.default_rng(seed)
    types = np.arange(1, 1 << k)
    inc = np.array([[(int(b) >> a) & 1 for b in types]
                    for a in range(k)], dtype=float)
    tails = list(itertools.combinations_with_replacement(range(k), r - 1))
    for i in range(trials):
        p = rng.dirichlet(np.ones(k)) if i % 3 else np.ones(k) / k
        # A label can be given zero query mass without being removed.
        if i % 5 == 4:
            p[rng.integers(k)] = 0
            p /= sum(p)
        opt = tuple(rng.integers(len(tails), size=k))
        rows, bounds = [], []
        for a, bi in enumerate(opt):
            z = (a,) + tails[bi]
            load = inc[list(z)].sum(axis=0)
            root = np.divide(inc[a], load, out=np.zeros(len(types)), where=load > 0)
            rows.append(np.r_[root, 1]); bounds.append(1)
            for b in tails[bi]:
                rows.append(np.r_[-np.divide(inc[b], load, out=np.zeros(len(types)), where=load > 0), 0]); bounds.append(-1)
            query = p @ inc / (1 + load)
            rows.append(np.r_[-query, 1]); bounds.append(-1)
        result = linprog(np.r_[np.zeros(len(types)), -1], A_ub=rows,
                         b_ub=bounds,
                         bounds=[(0, None)] * len(types) + [(0, 1)],
                         method="highs")
        if result.success and result.x[-1] > 1e-7:
            return {"candidate": "root<t, all tails>=t => Mfull<=t",
                    "k": k, "r": r, "trial": i, "seed": seed,
                    "p": p.tolist(), "epsilon": float(result.x[-1]),
                    "menu": [list(tails[bi]) for bi in opt],
                    "weights": {str(t): float(w) for t, w in zip(types, result.x[:-1]) if w > 1e-8},
                    "status": "floating discovery only; requires exact audit"}
    return {"k": k, "r": r, "trials": trials, "seed": seed,
            "status": "no numerical witness; no general conclusion"}


if __name__ == "__main__":
    reports = []
    for args in [(4, 3, 5000, 41), (5, 3, 10000, 51),
                 (6, 3, 10000, 61), (5, 4, 10000, 54)]:
        report = run(*args)
        reports.append(report)
        print(json.dumps(report), flush=True)
        if "weights" in report:
            break
    Path(__file__).with_name("threshold_menu_probe.json").write_text(
        json.dumps(reports, indent=2) + "\n")
