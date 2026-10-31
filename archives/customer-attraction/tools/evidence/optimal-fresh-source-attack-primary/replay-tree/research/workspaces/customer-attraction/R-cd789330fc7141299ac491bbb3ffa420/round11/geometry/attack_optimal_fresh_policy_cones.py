"""Bounded falsification of (S), preserving full policy IC and unique OPT.

Existing complete policies are varied over nonnegative customer-type weights.
This is not an enlarged-catalog proof or a HALF counterexample search. Any
floating separation is only a candidate pending independent exact recovery.
"""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).parent


def cone(name):
    source = ROOT / 'evidence/certificates/customer_attraction' / (name+'.json')
    example = ROOT / 'examples/customer_attraction' / (name+'.json')
    cert = json.loads(source.read_text())
    instance = json.loads(example.read_text())
    cert = cert.get('strategy', cert)
    policy = {tuple(z['history']): z['action'] for z in cert['actions']}
    m, p = instance['players'], len(instance['topics'])
    masks = list(range(1, 1 << p))

    @lru_cache(None)
    def finish(h):
        return h if len(h) == m else finish(h+(policy[h],))

    @lru_cache(None)
    def payoff(z, a):
        return np.array([1/sum(bool(mask >> b & 1) for b in z)
                         if mask >> a & 1 else 0 for mask in masks])

    gamma = []
    for h in policy:
        a = policy[h]
        actual_row = payoff(finish(h), a)
        for b in range(p):
            gamma.append(actual_row-payoff(finish(h+(b,)), b))
    gamma = np.array(gamma)
    z = finish(())
    coverage = np.array([int(any(mask >> a & 1 for a in z)) for mask in masks])
    reserve = np.array([1/(1+sum(bool(mask >> a & 1) for a in z))
                        if any(mask >> a & 1 for a in z) else 0 for mask in masks])
    fresh = [np.array([int(bool(mask >> a & 1))/
                        (1+sum(bool(mask >> b & 1) for b in z)) for mask in masks])
             for a in range(p)]
    supports = [support for k in range(min(m, p)+1)
                for support in combinations(range(p), k)]
    cover_rows = {s: np.array([int(any(mask >> a & 1 for a in s))
                              for mask in masks]) for s in supports}
    best = None
    feasible = 0
    # A strict positive coverage gap rules out lower-fresh-cost OPT ties. A
    # target with exactly m distinct labels needs no padding convention.
    eps = 1e-6
    for target in combinations(range(p), m):
        other = [s for s in supports if s != target]
        opt_rows = np.array([cover_rows[target]-cover_rows[s] for s in other])
        objective = coverage+reserve-sum((fresh[a] for a in target), np.zeros(len(masks)))
        sol = linprog(objective, A_ub=np.vstack([-gamma, -opt_rows]),
                      b_ub=np.concatenate([np.zeros(len(gamma)), -eps*np.ones(len(other))]),
                      A_eq=np.ones((1, len(masks))), b_eq=[1], bounds=(0, None),
                      method='highs')
        if sol.success:
            feasible += 1
            if best is None or sol.fun < best['objective']:
                best = {'target': target, 'objective': float(sol.fun),
                        'IC_min_float': float((gamma@sol.x).min()),
                        'strict_OPT_gap_float': float((opt_rows@sol.x).min())}
            if sol.fun < -1e-7:
                return {'name': name, 'm': m, 'p': p, 'status': 'UNVERIFIED_FLOAT_SEPARATION',
                        'actual': z, 'target': target, 'best': best,
                        'weights': {str(mask): float(w) for mask, w in zip(masks, sol.x) if w>0},
                        'full_policy_source': str(source.relative_to(ROOT))}
    return {'name': name, 'm': m, 'p': p, 'status': 'NO_FLOAT_SEPARATION_IN_THIS_POLICY_CONE',
            'targets': len(list(combinations(range(p), m))), 'feasible_targets': feasible,
            'IC_rows': len(gamma), 'best': best}


def main():
    names = ['worst_cce_welfare_failure', 'aggregate_theta_failure',
             'individual_security_failure', 'prefix_balance_failure']
    rows = []
    for name in names:
        row = cone(name)
        rows.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != 'weights'}), flush=True)
        if row['status'] == 'UNVERIFIED_FLOAT_SEPARATION':
            break
    report = {'candidate': 'min_OPT_m Kfresh <= W+Rself',
              'status': 'bounded candidate falsification; not a universal proof',
              'rows': rows}
    (HERE/'attack_optimal_fresh_policy_cones.json').write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
