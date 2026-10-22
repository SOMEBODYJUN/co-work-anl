"""Floating discovery attack on the stronger B(u_i)<=W bridge.

All nonempty customer masks are allowed in each supplied complete-policy cone.
The candidate query is fixed while weights are optimized; no finite run proves
the price bridge or the original half conjecture.
"""
import argparse
from functools import lru_cache
from itertools import combinations
from math import lcm
from pathlib import Path
import json
import time
import numpy as np
from scipy.optimize import linprog


def cone(path):
    data = json.loads(Path(path).read_text())
    strategy = data.get('strategy', data)
    if 'policy' in data and 'weights' in data:
        lookup = {tuple(item['history']): item['action'] for item in data['policy']}
        history = ()
        while len(history) < data['n']:
            history += (lookup[history],)
        strategy = {'actions': data['policy'],
                    'terminal_counts': [history.count(a) for a in range(data['m'])]}
    if 'actions' not in strategy or 'terminal_counts' not in strategy:
        raise ValueError('not a complete policy format')
    k = len(strategy['terminal_counts'])
    m = sum(strategy['terminal_counts'])
    policy = {tuple(item['history']): item['action'] for item in strategy['actions']}
    masks = np.arange(1, 1 << k, dtype=np.int64)
    incidence = np.array([((masks >> a) & 1) for a in range(k)], dtype=np.int64)
    scale = lcm(*range(1, m + 1))

    @lru_cache(None)
    def counts(history):
        if len(history) == m:
            return tuple(history.count(a) for a in range(k))
        return counts(history + (policy[history],))

    @lru_cache(None)
    def utilities(q):
        load = np.asarray(q) @ incidence
        inverse = np.zeros(len(masks), dtype=np.int64)
        positive = load > 0
        inverse[positive] = scale // load[positive]
        return incidence * inverse

    rows = set()
    for history, a in policy.items():
        actual = utilities(counts(history))[a]
        for b in range(k):
            row = actual - utilities(counts(history + (b,)))[b]
            if np.any(row): rows.add(row.astype(np.int32).tobytes())
    matrix = np.asarray([np.frombuffer(row, dtype=np.int32) for row in rows], dtype=float)
    q = counts(())
    pay = utilities(q) / scale
    welfare = (np.asarray(q) @ incidence > 0).astype(float)
    return k, m, incidence, matrix, pay, welfare, q


def run(path):
    start = time.time()
    k, m, incidence, matrix, pay, welfare, q = cone(path)
    best = {'value': -1e10}
    solved = 0
    print(json.dumps({'phase': 'cone_ready', 'topics': k, 'rows': len(matrix),
                      'variables': len(welfare), 'seconds': time.time() - start}), flush=True)
    if k <= 7:
        supports = [s for size in range(1, k + 1) for s in combinations(range(k), size)]
    else:
        supports = [(4, 9)]
    for support in supports:
            size = len(support)
            degree = incidence[list(support)].sum(axis=0)
            for denominator in (range(1, size + 1) if k <= 7 else [1]):
                coverage = np.minimum(1., degree / denominator)
                tau = size / denominator
                for a in range(k):
                    if not q[a]: continue
                    if k > 7 and a != 8: continue
                    objective = coverage - tau * pay[a] - welfare
                    result = linprog(-objective, A_ub=-matrix, b_ub=np.zeros(len(matrix)),
                                     A_eq=np.ones((1, len(welfare))), b_eq=[1.],
                                     bounds=(0, None), method='highs', options={'time_limit': 45})
                    if not result.success:
                        return {'policy': path, 'players': m, 'topics': k, 'cone_unique_rows': len(matrix),
                                'solved_fixed_query_LPs': solved, 'incomplete': result.message,
                                'seconds': time.time() - start}
                    solved += 1
                    if -result.fun > best['value'] + 1e-10:
                        best = {'value': float(-result.fun), 'actual_theme': a,
                                'query_support': support, 'query_denominator': denominator,
                                'weights': {str(j + 1): float(x) for j, x in enumerate(result.x) if x > 1e-8},
                                'welfare': float(welfare @ result.x),
                                'price_value': float((coverage - tau * pay[a]) @ result.x)}
    return {'policy': path, 'players': m, 'topics': k, 'cone_unique_rows': len(matrix),
            'solved_fixed_query_LPs': solved, 'best': best, 'seconds': time.time() - start}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('policies', nargs='+')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    records = []
    for path in args.policies:
        record = run(path)
        records.append(record)
        print(json.dumps({k: v for k, v in record.items() if k != 'best'} | {'best_value': record['best']['value']}), flush=True)
        Path(args.output).write_text(json.dumps({'scope': 'finite floating fixed-query cone attacks; no general conclusion', 'records': records}, indent=2) + '\n')
