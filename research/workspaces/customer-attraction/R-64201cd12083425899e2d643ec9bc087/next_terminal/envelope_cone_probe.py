"""Exploratory floating LP: can a fixed full SPE cone refute E_* <= 2W?

Every original ordered-history SPE row is retained. The last-node envelope
is minimized over all count prefixes. A positive optimum needs separate
rational reconstruction and definition-level verification before being used.
"""

import argparse
import itertools
import json
import random
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver


def optimize(instance, cert):
    m, p = instance.players, instance.topic_count
    masks = np.arange(1, 1 << p)
    incidence = np.array([((masks >> a) & 1) for a in range(p)], dtype=float)

    @lru_cache(None)
    def terminal(h):
        if len(h) == m:
            return h
        return terminal(h + (cert.actions[h],))

    @lru_cache(None)
    def coefficients(counts):
        load = np.array(counts) @ incidence
        reciprocal = np.divide(1., load, out=np.zeros_like(load), where=load > 0)
        return incidence * reciprocal

    def counts(h):
        return tuple(h.count(a) for a in range(p))

    z = terminal(())
    w = ((np.array(counts(z)) @ incidence) > 0).astype(float)
    rows = []
    for depth in range(m):
        for h in itertools.product(range(p), repeat=depth):
            a = cert.actions[h]
            own = coefficients(counts(terminal(h)))[a]
            for b in range(p):
                if b != a:
                    dev = coefficients(counts(terminal(h+(b,))))[b]
                    rows.append(np.r_[dev-own, 0.])
    for h in itertools.combinations_with_replacement(range(p), m-1):
        load = np.array(counts(h)) @ incidence
        a = cert.actions[h]
        br = incidence[a] / (load+1)
        tax = load / (load+1)
        rows.append(np.r_[2*w-m*br-tax, 1.])
    matrix = csr_matrix(np.vstack(rows))
    result = linprog(np.r_[np.zeros(len(masks)), -1.],
                     A_ub=matrix, b_ub=np.zeros(matrix.shape[0]),
                     A_eq=csr_matrix(np.array([np.r_[w, 0.]])), b_eq=[1.],
                     bounds=[(0., None)]*len(masks)+[(None, None)], method='highs')
    out = {'success': result.success, 'actual_path': z,
           'ordered_spe_rows': sum(p**d*(p-1) for d in range(m)),
           'all_rows': matrix.shape[0]}
    if result.success:
        out['max_Estar_minus_2W_normalized_W'] = result.x[-1]
        out['numerical_weights'] = {str(mask): float(v)
                                    for mask, v in zip(masks, result.x[:-1]) if v > 1e-9}
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--players', type=int, default=5)
    parser.add_argument('--topics', type=int, default=7)
    parser.add_argument('--trials', type=int, default=10)
    parser.add_argument('--seed', type=int, default=620261021)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    records = []
    for trial in range(args.trials):
        p, m = args.topics, args.players
        instance = Instance(tuple(map(str, range(p))),
                            tuple(CustomerType(frozenset(a for a in range(p) if mask >> a & 1),
                                               rng.randint(1, 12))
                                  for mask in range(1, 1 << p) if rng.random() < .4), m)
        solver = ExactSPESolver(instance)
        cert = solver.worst_certificate()
        record = optimize(instance, cert)
        record['trial'] = trial
        print(json.dumps({k:v for k,v in record.items() if k != 'numerical_weights'}), flush=True)
        records.append(record)
    report = {'status': 'floating_exploration_only', 'parameters': vars(args) | {'output': str(args.output)},
              'records': records}
    if args.output:
        with args.output.open('x') as f:
            json.dump(report, f, indent=2)
            f.write('\n')


if __name__ == '__main__':
    main()
