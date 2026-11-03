"""Targeted search for an SPE whose every full root column has M_1 > u.

Canonical BI proposes full ordered-history strategies.  A fixed strategy cone
then varies all customer-type multiplicities, and a MILP selects one offending
query for every root column.  Numerical optima are exploration only; a positive
candidate must be recovered and checked exactly before it becomes a claim.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import importlib.util
from itertools import product
import json
from pathlib import Path
import random
import sys

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'customer_attraction/__init__.py').is_file())
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance

spec = importlib.util.spec_from_file_location('ca_strategy_cone', ROOT / 'tests/audits/customer_attraction_strategy_lp.py')
cone_module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cone_module
spec.loader.exec_module(cone_module)
StrategyCone = cone_module.StrategyCone
payoff_row = cone_module.payoff_row


def insertion_row(topics, counts, query):
    return tuple(Fraction(int(bool(mask & (1 << query))),
                          1 + sum(counts[t] for t in range(topics) if mask & (1 << t)))
                 for mask in range(1, 1 << topics))


def optimize(cone, seconds):
    p, m = cone.topics, cone.players
    n = (1 << p) - 1
    delta = n
    binary_start = n + 1
    size = n + 1 + p * p
    root_u = payoff_row(p, cone.root, cone.actions[()])
    rows, lower, upper = [], [], []
    for row in cone.rows:
        rows.append([float(x) for x in row] + [0.] * (1 + p * p))
        lower.append(0.)
        upper.append(np.inf)
    big_m = m + 1
    for b in range(p):
        q = cone.terminals[(b,)]
        for a in range(p):
            f = insertion_row(p, q, a)
            row = [float(u - v) for u, v in zip(root_u, f)] + [0.] * (1 + p * p)
            row[delta] = 1.
            row[binary_start + b * p + a] = big_m
            rows.append(row)
            lower.append(-np.inf)
            upper.append(big_m)
        row = [0.] * size
        for a in range(p):
            row[binary_start + b * p + a] = 1.
        rows.append(row)
        lower.append(1.)
        upper.append(1.)
    rows.append([float(x) for x in cone.welfare] + [0.] * (1 + p * p))
    lower.append(1.)
    upper.append(1.)
    objective = np.zeros(size)
    objective[delta] = -1.
    lo = np.zeros(size)
    hi = np.full(size, m * p, dtype=float)
    lo[delta], hi[delta] = -1., m
    hi[binary_start:] = 1.
    integrality = np.zeros(size)
    integrality[binary_start:] = 1.
    result = milp(objective, integrality=integrality,
                  bounds=Bounds(lo, hi),
                  constraints=LinearConstraint(np.array(rows), lower, upper),
                  options={'time_limit': seconds, 'mip_rel_gap': 1e-9})
    if result.x is None:
        return {'status': str(result.message), 'positive_candidate': False}
    out = {'status': str(result.message), 'margin': float(result.x[delta]),
           'dual_upper_bound': -float(result.mip_dual_bound),
           'positive_candidate': bool(result.x[delta] > 1e-7),
           'bad_queries': [int(np.argmax(result.x[binary_start + b * p:binary_start + (b + 1) * p]))
                           for b in range(p)]}
    if out['positive_candidate']:
        out['floating_multiplicities'] = result.x[:n].tolist()
        out['actions'] = [{'history': list(h), 'action': a} for h, a in sorted(cone.actions.items())]
        out['root_counts'] = list(cone.root)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--topics', type=int, default=4)
    ap.add_argument('--players', type=int, default=4)
    ap.add_argument('--cones', type=int, default=20)
    ap.add_argument('--seconds-per-cone', type=float, default=5.)
    ap.add_argument('--seed', type=int, default=2210227)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    seen = set()
    records = []
    for attempt in range(args.cones * 5):
        weights = [rng.randrange(1, 9) if rng.random() < .32 else 0
                   for _ in range((1 << args.topics) - 1)]
        if not any(weights):
            continue
        inst = Instance(tuple(f'T{a}' for a in range(args.topics)),
                        tuple(CustomerType(frozenset(a for a in range(args.topics) if mask & (1 << a)), w)
                              for mask, w in enumerate(weights, 1) if w), args.players)
        solver = ExactSPESolver(inst)
        outcomes = tuple(solver.outcomes())
        target = rng.choice(outcomes)
        certificate = solver.certificate(target,
            action_selector=lambda h, candidates: rng.choice(candidates),
            continuation_selector=lambda h, candidates: rng.choice(candidates))
        key = tuple(sorted(certificate.actions.items()))
        if key in seen:
            continue
        seen.add(key)
        cone = StrategyCone(args.topics, args.players, dict(certificate.actions))
        result = optimize(cone, args.seconds_per_cone)
        result['source_weights'] = weights
        records.append(result)
        print(json.dumps({'cone': len(records), **{k: v for k, v in result.items()
              if k not in ('source_weights', 'floating_multiplicities', 'actions', 'root_counts')}}), flush=True)
        if result['positive_candidate'] or len(records) >= args.cones:
            break
    report = {'scope': 'sampled fixed complete SPE cones; pure full-root-menu blocker only',
              'universal_claim_proved': False, 'parameters': vars(args) | {'output': str(args.output)},
              'records': records}
    if args.output:
        with args.output.open('x') as stream:
            json.dump(report, stream, indent=2)
            stream.write('\n')


if __name__ == '__main__':
    main()
