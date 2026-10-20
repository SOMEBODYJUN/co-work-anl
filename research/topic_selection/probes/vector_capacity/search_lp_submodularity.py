"""Find a small failure of the GAP fractional value's submodularity.

Enabled-item value phi(S) maximizes sum p_ij*x_ij, with item sums <= 1
and bin loads sum s_ij*x_ij <= 1. This uses a fixed seed and reports all
eight values. Numerical search is followed by exact certificates separately.
"""
import itertools
import json
import random
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parent
N, M = 3, 2

def values(size, profit):
    rows = []
    for i in range(N):
        row = np.zeros(N * M)
        row[i*M:(i+1)*M] = 1
        rows.append(row)
    for j in range(M):
        row = np.zeros(N * M)
        for i in range(N):
            row[i*M+j] = size[i][j]
        rows.append(row)
    ans = []
    sols = []
    for mask in range(1 << N):
        bounds = [(0, None if mask & (1 << i) else 0)
                  for i in range(N) for j in range(M)]
        r = linprog(-np.array(profit).reshape(-1), A_ub=rows,
                    b_ub=np.ones(N+M), bounds=bounds, method='highs')
        assert r.success
        ans.append(float(-r.fun))
        sols.append(r.x.reshape(N, M).tolist())
    return ans, sols

def failure(vals):
    for a in range(1 << N):
        for b in range(a, 1 << N):
            gap = vals[a | b] + vals[a & b] - vals[a] - vals[b]
            if gap > 1e-8:
                return a, b, gap

def main():
    rng = random.Random(20261020)
    # Simple two-scale sizes. All profit entries are nonnegative.
    for trial in range(10000):
        size = [[rng.choice([0.5, 1.0]) for _ in range(M)] for _ in range(N)]
        profit = [[rng.choice([0, 1, 2]) for _ in range(M)] for _ in range(N)]
        vals, sols = values(size, profit)
        bad = failure(vals)
        if bad:
            out = dict(trial=trial, size=size, profit=profit, values=vals,
                       optimal_fractional_assignments=sols,
                       violating_masks=list(bad[:2]), violation=bad[2])
            target = ROOT / 'lp_submodularity_counterexample.json'
            target.write_text(json.dumps(out, indent=2))
            print(json.dumps(out, indent=2))
            return
    raise RuntimeError('No witness in search window')

if __name__ == '__main__':
    main()
