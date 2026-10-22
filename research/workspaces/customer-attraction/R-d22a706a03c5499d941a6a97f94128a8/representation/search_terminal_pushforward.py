"""Exploratory finite-cone attack on D >= C for a full terminal pushforward."""
import argparse
import json
from functools import lru_cache
from itertools import product
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, minimize


def run(p, m, seeds, probes, background=0, weak=False):
    rng = np.random.default_rng(933612)
    masks = np.arange(1, 1 << p)
    I = ((masks[:, None] >> np.arange(p)) & 1).astype(float)
    # Uniform scalar background is an explicit nonnegative integer vector;
    # no promise is made that it comes from a legal prefix of a larger game.
    b = np.full(len(masks), background)
    best = 1
    carry = None
    for seed in range(seeds):
        w = carry if carry is not None and seed % 2 else rng.integers(0, 10, len(masks)).astype(float)

        def payoff(q, a, plus=0):
            d = I @ np.array(q) + b + plus
            return np.divide(I[:, a], d, out=np.zeros(len(masks)), where=d > 0)

        actions = {}

        @lru_cache(None)
        def solve(q):
            if sum(q) == m:
                return q
            children = []
            for a in range(p):
                qnext = list(q)
                qnext[a] += 1
                children.append(solve(tuple(qnext)))
            vals = [payoff(z, a) @ w for a, z in enumerate(children)]
            mx = max(vals)
            a = int(rng.choice([a for a in range(p) if vals[a] >= mx - 1e-9]))
            actions[q] = a
            return children[a]

        solve((0,) * p)

        def leaf(h):
            q = [h.count(a) for a in range(p)]
            while sum(q) < m:
                a = actions[tuple(q)]
                q[a] += 1
            return tuple(q)

        G = []
        for k in range(1, m):
            for h in product(range(p), repeat=k):
                q = tuple(h.count(a) for a in range(p))
                a = actions[q]
                r = payoff(leaf(h), a)
                G += [r - payoff(leaf(h + (a2,)), a2) for a2 in range(p) if a2 != a]
        G = np.array(G)
        Z = [leaf((a,)) for a in range(p)]
        L = np.array([payoff(Z[a], a) for a in range(p)])
        C = np.array([[payoff(Z[a2], a, 1) for a2 in range(p)] for a in range(p)])
        q_next = np.ones(p) / p
        for j in range(probes):
            q = q_next if j % 3 == 0 else rng.dirichlet(np.full(p, .35 if j % 2 else 2))
            cross = np.einsum('a,b,abt->t', q, q, C)
            D = q @ L - cross
            if weak:
                A = np.concatenate([np.column_stack([-G, np.zeros(len(G))]),
                                    np.column_stack([L, -np.ones(p)])])
                r = linprog(np.r_[-cross, 1], A_ub=A, b_ub=np.zeros(len(G) + p),
                            A_eq=[np.r_[np.ones(len(masks)), 0]], b_eq=[1],
                            bounds=(0, None), method='highs')
            else:
                r = linprog(D, A_ub=-G, b_ub=np.zeros(len(G)), A_eq=[np.ones(len(masks))],
                            b_eq=[1], bounds=(0, None), method='highs')
            if not r.success:
                continue
            rw = r.x[:-1] if weak else r.x
            carry = rw
            # Minimize the exact quadratic in p at this LP extremum.
            Lin = L @ rw
            Cq = C @ rw
            f = (lambda v: max(Lin) - v @ Cq @ v) if weak else (lambda v: v @ Lin - v @ Cq @ v)
            sol = minimize(f, q, method='SLSQP', bounds=[(0, 1)] * p,
                           constraints=[{'type': 'eq', 'fun': lambda v: v.sum() - 1}],
                           options={'ftol': 1e-12, 'maxiter': 300})
            q_next = sol.x / sol.x.sum() if sol.success else q
            value = r.fun
            if value < best - 1e-9:
                best = value
                print(json.dumps({'p': p, 'm': m, 'b': background, 'seed': seed, 'probe': j,
                                  'objective': 'u-C' if weak else 'D-C',
                                  'D_minus_C': float(D @ rw), 'u_minus_C': float(max(L @ rw) -
                                  np.einsum('a,b,abt,t->', q, q, C, rw)),
                                  'probability': q.tolist()}), flush=True)
                Path(__file__).with_name(f'pushforward_candidate_{p}_{m}_{background}_{"weak" if weak else "strong"}.json').write_text(
                    json.dumps({'p': p, 'm': m, 'background': background,
                                'weights': rw.tolist(), 'probability': q.tolist(),
                                'actions': [[list(v), a] for v, a in actions.items()],
                                'D_minus_C': value}))
            if best < -1e-8:
                return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topics', type=int, default=6)
    parser.add_argument('--players', type=int, default=3)
    parser.add_argument('--background', type=int, default=0)
    parser.add_argument('--seeds', type=int, default=100)
    parser.add_argument('--probes', type=int, default=30)
    parser.add_argument('--weak', action='store_true')
    args = parser.parse_args()
    run(args.topics, args.players, args.seeds, args.probes, args.background, args.weak)
