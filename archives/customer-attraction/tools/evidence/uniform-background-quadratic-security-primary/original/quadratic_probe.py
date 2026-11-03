"""Finite discovery test for the equal-norm quadratic limiting mechanism.

This is not a CAG proof. The auxiliary n-player game has utility
 -sum_{j!=i}<a_i,a_j>; incidence vectors all have the same norm.
All full-history SPE terminal count vectors are retained by set-valued BI.
The symmetric static Nash value is -(n-1) min_q q'Gq, whereas the genuine
static zero-sum value is -(n-1)H, H=min_p max_b (Gp)_b.
We report both targets and search for a violation of the genuine H target.
Positive gaps would be numerical candidates requiring exact recovery.
"""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import minimize, linprog


def outcomes(G, n):
    k = len(G)

    @lru_cache(None)
    def solve(h):
        if sum(h) == n:
            return frozenset((h,))
        branches = []
        worst = []
        for a in range(k):
            child = list(h)
            child[a] += 1
            z = solve(tuple(child))
            def u(c):
                return int(G[a, a] - sum(c[b]*G[a, b] for b in range(k)))
            branches.append([(c, u(c)) for c in z])
            worst.append(min(v for _, v in branches[-1]))
        cutoff = max(worst)
        return frozenset(c for branch in branches for c, v in branch if v >= cutoff)
    zs = solve((0,)*k)
    root_pairs = []
    floors = []
    for a in range(k):
        h = [0]*k
        h[a] = 1
        branch = [(c, int(G[a,a]-sum(c[b]*G[a,b] for b in range(k)))) for c in solve(tuple(h))]
        root_pairs.extend((a, c, u) for c, u in branch)
        floors.append(min(u for c, u in branch))
    cutoff = max(floors)
    root_cost = max(-u for a, c, u in root_pairs if u >= cutoff)
    return zs, solve.cache_info().currsize, root_cost


def norm_min(G):
    k = len(G)
    res = minimize(lambda q: q@G@q, np.ones(k)/k,
                   jac=lambda q: 2*G@q, bounds=[(0, 1)]*k,
                   constraints=[dict(type='eq', fun=lambda q: sum(q)-1,
                                     jac=lambda q: np.ones(k))],
                   method='SLSQP', options=dict(ftol=1e-12, maxiter=500))
    if not res.success:
        raise RuntimeError(res.message)
    return res.x, res.fun


def safety_overlap(G):
    k = len(G)
    res = linprog(np.r_[np.zeros(k), 1.],
                  A_ub=np.c_[G, -np.ones(k)], b_ub=np.zeros(k),
                  A_eq=[np.r_[np.ones(k), 0.]], b_eq=[1.],
                  bounds=[(0, None)]*k+[(None, None)], method='highs')
    if not res.success:
        raise RuntimeError(res.message)
    return res.x[:-1], res.fun


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trials', type=int, default=200)
    ap.add_argument('--seed', type=int, default=103)
    ap.add_argument('--arbitrary-matrix', action='store_true')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    rows = []
    best = None
    for n in range(3, 8):
        max_gap = -float('inf')
        max_example = None
        root_max_gap = -float('inf')
        for t in range(args.trials):
            ambient, size, k = 10, 4, 6
            atoms = np.array([rng.choice(ambient, size=size, replace=False) for _ in range(k)])
            A = np.zeros((k, ambient), dtype=np.int64)
            for a, s in enumerate(atoms):
                A[a, s] = 1
            G = A@A.T
            if args.arbitrary_matrix:
                size = 10
                G = rng.integers(0, 10, size=(k, k))
                G = np.tril(G, -1)+np.tril(G, -1).T+size*np.eye(k, dtype=np.int64)
                q, v = np.zeros(k), None
            else:
                q, v = norm_min(G)
            p, H = safety_overlap(G)
            zs, states, root_cost = outcomes(G, n)
            root_max_gap = max(root_max_gap, root_cost-(n-1)*H)
            gap_z = [(float(np.asarray(z)@G@np.asarray(z)-n*size-n*(n-1)*H), z) for z in zs]
            gap, z = max(gap_z)
            if gap > max_gap:
                max_gap = gap
                max_example = dict(n=n, trial=t, atoms=atoms.tolist(), gram=G.tolist(),
                                   q=q.tolist(), minimum_norm=v, security_query=p.tolist(),
                                   security_overlap=H, terminal=list(z), gap=gap,
                                   stronger_nash_gap=None if v is None else float(np.asarray(z)@G@np.asarray(z)-n*size-n*(n-1)*v),
                                   terminal_count=len(zs), count_states=states)
            if gap > 1e-7:
                best = max_example
                break
        rows.append(dict(n=n, trials=t+1, maximum_gap=max_gap,
                         maximum_root_individual_gap=root_max_gap, witness=max_example))
        if best:
            break
    report = dict(scope='finite numerical discovery only; auxiliary quadratic game, not CAG',
                  seed=args.seed, arbitrary_matrix=args.arbitrary_matrix,
                  results=rows, positive_candidate=best)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
