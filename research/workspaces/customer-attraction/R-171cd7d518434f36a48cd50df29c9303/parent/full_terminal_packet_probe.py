"""Finite discovery in one pre-existing complete SPE automaton, not a proof.

Preserve every ordered-history comparison via the complete acyclic automaton.
Attack only FTA: W >= sum_i E_(a,b iid p) f_(z_i(b))(a).
Positive output requires separate rational reconstruction and full verification.
"""
from pathlib import Path
from itertools import combinations
import gzip
import json
import sys

import numpy as np
from scipy.optimize import linprog, minimize

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent


def load_packet(source):
    with (gzip.open(source, 'rt') if str(source).endswith('.gz') else open(source)) as f:
        data = json.load(f)
    nodes = data['nodes']
    k = len(data['instance']['topics'])
    n = data['instance']['players']
    targets = [None] * len(nodes)
    for j in sorted(range(len(nodes)), key=lambda j: -sum(nodes[j]['counts'])):
        node = nodes[j]
        targets[j] = (targets[node['children'][node['action']]]
                      if 'action' in node else np.array(node['counts']))
    bits = np.array([[(mask >> a) & 1 for a in range(k)]
                     for mask in range(1, 1 << k)], float)
    rows = []
    for j, node in enumerate(nodes):
        if 'action' not in node:
            continue
        own = bits[:, node['action']] / np.maximum(bits @ targets[j], 1)
        for a, child in enumerate(node['children']):
            if a != node['action']:
                rows.append(own - bits[:, a] / np.maximum(bits @ targets[child], 1))
    gamma = np.unique(rows, axis=0)
    branches = []
    j = data['root']
    while 'action' in nodes[j]:
        branches.append([targets[child] for child in nodes[j]['children']])
        j = nodes[j]['children'][nodes[j]['action']]
    tensor = np.einsum('ibt,ta->abt',
                       1 / (1 + np.einsum('ibk,tk->ibt', np.array(branches), bits)), bits)
    welfare = (bits @ targets[data['root']] > 0).astype(float)
    weights = np.zeros((1 << k) - 1)
    for customer in data['instance']['customers']:
        mask = sum(1 << a for a in customer['topics'])
        if mask:
            weights[mask - 1] += customer['multiplicity']
    assert np.min(gamma @ weights) > -1e-8
    return data, gamma, tensor, welfare, weights


def maximize_query(matrix, start):
    k = len(start)
    matrix = (matrix + matrix.T) / 2
    candidates = [start, *np.eye(k)]
    for a, b in combinations(range(k), 2):
        quadratic = matrix[a, a] - 2 * matrix[a, b] + matrix[b, b]
        linear = 2 * (matrix[a, b] - matrix[b, b])
        if quadratic < 0:
            t = -linear / (2 * quadratic)
            if 0 < t < 1:
                p = np.zeros(k)
                p[a], p[b] = t, 1 - t
                candidates.append(p)
    fit = minimize(lambda p: -p @ matrix @ p, start,
                   jac=lambda p: -2 * matrix @ p, bounds=[(0, 1)] * k,
                   constraints=[{'type': 'eq', 'fun': lambda p: sum(p) - 1,
                                 'jac': lambda p: np.ones(k)}],
                   method='SLSQP', options={'maxiter': 100, 'ftol': 1e-11})
    if fit.success:
        candidates.append(fit.x)
    return max(candidates, key=lambda p: p @ matrix @ p)


def main():
    source = ROOT / sys.argv[1]
    data, gamma, tensor, welfare, seed = load_packet(source)
    k = tensor.shape[0]
    rng = np.random.default_rng(1712026)
    starts = [np.ones(k) / k, *np.eye(k)]
    starts += [rng.dirichlet(np.ones(k) / 3) for _ in range(10)]
    best = None
    for s, start in enumerate(starts):
        p = maximize_query(tensor @ seed, start)
        for iteration in range(8):
            objective = np.einsum('a,b,abt->t', p, p, tensor) - welfare
            lp = linprog(-objective, A_ub=-gamma, b_ub=np.zeros(len(gamma)),
                         A_eq=[np.ones(len(welfare))], b_eq=[1],
                         bounds=[(0, None)] * len(welfare), method='highs')
            assert lp.success, lp.message
            p = maximize_query(tensor @ lp.x, p)
            gap = float((np.einsum('a,b,abt->t', p, p, tensor) - welfare) @ lp.x)
            if best is None or gap > best['gap'] + 1e-9:
                best = {'status': 'finite floating discovery only',
                        'source': str(source.relative_to(ROOT)),
                        'gamma_rows': len(gamma), 'seed': 1712026,
                        'start': s, 'iteration': iteration,
                        'gap': gap, 'W': float(welfare @ lp.x), 'p': p.tolist(),
                        'weights': {str(i + 1): float(w) for i, w in enumerate(lp.x) if w > 1e-9}}
                print(json.dumps(best), flush=True)
                (HERE / 'full_terminal_packet_probe.json').write_text(json.dumps(best, indent=2))
            if gap > 1e-7:
                return
    print('done; finite negative results have no general truth implication', flush=True)


if __name__ == '__main__':
    main()
