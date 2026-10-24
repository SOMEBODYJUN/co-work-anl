"""Discovery-only attack on universal C26, retaining every ordered SPE row.

Run from repository root. Floating optima are observations, never certificates.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import json
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]


def experiment(position, rounds, seed):
    obj = json.loads((ROOT / 'evidence/certificates/customer_attraction/individual_security_failure.json').read_text())
    policy = {tuple(v['history']): v['action'] for v in obj['strategy']['actions']}
    m, p = 3, 6
    types = list(range(1, 1 << p))

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == m else terminal(h + (policy[h],))

    @lru_cache(None)
    def own(profile, i):
        return tuple(F(1, sum(bool(B >> a & 1) for a in profile))
                     if B >> profile[i] & 1 else F(0) for B in types)

    def query(profile, t):
        return [F(1, 1 + sum(bool(B >> a & 1) for a in profile))
                if B >> t & 1 else F(0) for B in types]

    rows = []
    for depth in range(m):
        for h in product(range(p), repeat=depth):
            chosen = own(terminal(h), depth)
            for a in range(p):
                dev = own(terminal(h + (a,)), depth)
                rows.append([float(x-y) for x, y in zip(chosen, dev)])
    G = np.array(rows)
    z = terminal(())
    wc = np.array([float(any(B >> a & 1 for a in z)) for B in types])
    uc = np.array(own(z, position), dtype=float)
    K = np.array([[query(terminal(z[:position] + (a,)), t) for a in range(p)]
                  for t in range(p)], dtype=float)
    eq = np.append(wc, 0)[None, :]
    rng = np.random.default_rng(seed)
    initial = [np.ones(p)/p, np.array([10,10,21,10,10,21])/82]
    initial += [np.eye(p)[i] for i in range(p)]
    initial += list(rng.dirichlet(np.ones(p), 12))
    results = []
    for start, prob in enumerate(initial):
        trace = []
        for r in range(rounds):
            # min_A (p K_A - u) w >= epsilon, normalized actual W=1.
            delta = np.einsum('t,tab->ab', prob, K) - uc
            aub = np.concatenate([np.c_[-G, np.zeros(len(G))],
                                  np.c_[-delta, np.ones(p)]])
            sol = linprog(np.r_[np.zeros(len(types)), -1.], A_ub=aub,
                          b_ub=np.zeros(len(aub)), A_eq=eq, b_eq=[1.],
                          bounds=[(0, None)]*len(types)+[(None, None)], method='highs')
            if not sol.success:
                trace.append({'weight_lp_status': sol.message})
                break
            weights, gap = sol.x[:-1], sol.x[-1]
            # Best query distribution for the same complete SPE and weights.
            value = np.einsum('tab,b->ta', K, weights)
            ps = linprog(np.r_[np.zeros(p), -1.],
                         A_ub=np.c_[-value.T, np.ones(p)], b_ub=np.zeros(p),
                         A_eq=np.r_[np.ones(p), 0][None,:], b_eq=[1.],
                         bounds=[(0,None)]*p+[(None,None)], method='highs')
            assert ps.success
            prob = ps.x[:-1]
            excess = ps.x[-1] - uc @ weights
            trace.append({'gap_fixed_p': float(gap), 'best_p_gap': float(excess)})
            if r and abs(trace[-1]['best_p_gap']-trace[-2]['best_p_gap']) < 1e-11:
                break
        results.append({'start': start, 'trace': trace,
                        'p': prob.tolist(), 'weights': weights.tolist()})
    best = max(results, key=lambda x: x['trace'][-1].get('best_p_gap', -1e9))
    return {'claim': 'C26 universal full-root extra-slot menu <= own utility',
            'status': 'discovery-only; no exact certificate, no general conclusion',
            'policy_source': 'individual_security_failure.json',
            'players': m, 'topics': p, 'position_zero_based': position,
            'ordered_histories': len(policy), 'rows_including_self': len(rows),
            'seed': seed, 'best': best,
            'gaps': [v['trace'][-1].get('best_p_gap') for v in results]}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--position', type=int, default=0)
    ap.add_argument('--rounds', type=int, default=10)
    ap.add_argument('--seed', type=int, default=20261024)
    ap.add_argument('--output')
    args = ap.parse_args()
    result = experiment(args.position, args.rounds, args.seed)
    data = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(data+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'best'}))
    print('best_gap', max(v for v in result['gaps'] if v is not None))
