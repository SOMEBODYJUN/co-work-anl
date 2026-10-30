"""Floating full-policy-cone attack on the sufficient first-step condition.

The epigraph variable exactly optimizes OPT_(r-1) outside the first topic.
A negative LP is only a candidate until rational reconstruction and replay.
"""
import importlib.util
from pathlib import Path
from itertools import combinations
import random
import argparse
import json
import time
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).parent
source = HERE.parent / "global_proof/background_regret_probe.py"
spec = importlib.util.spec_from_file_location("regret_probe", source)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def probe(q, r, trials, seed):
    rng = random.Random(seed)
    masks = np.arange(1, 1 << q)
    member = np.array([[(mask >> a) & 1 for a in range(q)] for mask in masks])
    states = [c for n in range(r) for c in base.comps(n, q)]
    terminals = list(base.comps(r, q))
    ti = {t: i for i, t in enumerate(terminals)}
    best = 0.0
    start = time.time()
    for trial in range(trials):
        prefix = [0] * q
        for _ in range(rng.randrange(5)):
            prefix[rng.randrange(q)] += 1
        bg = member @ np.array(prefix)
        fresh = (bg == 0).astype(float)
        loads = np.array([member @ np.array(t) for t in terminals])
        tot = loads + bg
        coeff = np.divide(member[None, :, :], tot[:, :, None],
                          out=np.zeros((len(terminals), len(masks), q)),
                          where=tot[:, :, None] != 0)
        w = np.array([rng.randrange(50) if rng.random() < .3 else 0 for _ in masks])
        pay = np.einsum('tka,k->ta', coeff, w)
        policy = {}
        out = {t: t for t in terminals}
        for c in reversed(states):
            child = []
            for a in range(q):
                d = list(c)
                d[a] += 1
                child.append(out[tuple(d)])
            vals = [pay[ti[child[a]], a] for a in range(q)]
            v = max(vals)
            a = rng.choice([a for a in range(q) if abs(vals[a] - v) < 1e-8])
            policy[c] = a
            out[c] = child[a]
        zero = (0,) * q
        first = policy[zero]
        actual = out[zero]
        at = ti[actual]
        rows = []
        for c in states:
            a = policy[c]
            on = coeff[ti[out[c]], :, a]
            for b in range(q):
                if b == a:
                    continue
                d = list(c)
                d[b] += 1
                off = coeff[ti[out[tuple(d)]], :, b]
                rows.append(np.r_[on - off, 0.0])
        for comp in combinations(range(q), min(r - 1, q)):
            covered = fresh * (1 - member[:, first]) * (member[:, comp].sum(axis=1) > 0)
            rows.append(np.r_[-covered, 1.0])
        rows = np.array(rows)
        comparisons = list(combinations(range(q), min(r, q)))
        rng.shuffle(comparisons)
        for comp in comparisons:
            covered = fresh * (member[:, comp].sum(axis=1) > 0)
            obj = np.r_[coeff[at, :, first] + fresh * member[:, first] - covered, 1.0]
            res = linprog(obj, A_ub=-rows, b_ub=np.zeros(len(rows)),
                          A_eq=[np.r_[np.ones(len(masks)), 0.0]], b_eq=[1.0],
                          bounds=[(0, None)] * len(masks) + [(0, None)], method='highs')
            if res.success and res.fun < best - 1e-8:
                best = float(res.fun)
                data = dict(q=q, r=r, prefix=prefix, first=first, actual=actual,
                            comparison=comp, policy=[[c, a] for c, a in policy.items()],
                            weights={int(mask): float(v) for mask, v in zip(masks, res.x) if v > 1e-9},
                            objective=best, z=float(res.x[-1]), seed=seed, trial=trial,
                            scope="Candidate failure of first-step sufficient condition only")
                (HERE / "coverage_step_lp_candidate.json").write_text(json.dumps(data, indent=2) + "\n")
                print("FOUND", trial, best, data, flush=True)
                return
        if trial % 25 == 0:
            print('trial', trial, 'seconds', round(time.time() - start, 1), 'best', best, flush=True)
    print('completed', trials, 'best', best, 'seconds', round(time.time() - start, 1), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--q', type=int, default=6)
    p.add_argument('--r', type=int, default=3)
    p.add_argument('--trials', type=int, default=200)
    p.add_argument('--seed', type=int, default=193770)
    args = p.parse_args()
    probe(args.q, args.r, args.trials, args.seed)
