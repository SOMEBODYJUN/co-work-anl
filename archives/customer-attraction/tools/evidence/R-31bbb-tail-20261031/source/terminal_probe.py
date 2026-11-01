"""Finite full-policy cone attack on OPT <= W + sum_x c_x/(c_x+1).

LP results only generate candidates. No finite negative run proves the bridge.
Each positive result must be reconstructed and checked exactly before use.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations
import json
from math import lcm
from pathlib import Path
import random
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').is_file())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests/audits'))
from customer_attraction import CustomerType, ExactSPESolver, Instance
from customer_attraction_strategy_lp import (StrategyCone, dot, integer_clones,
                                             independently_verify, serializable)


def matrix(actions, m, p):
    member = np.array([[(t >> a) & 1 for t in range(1, 1 << p)]
                       for a in range(p)], dtype=np.int16)
    scale = lcm(*range(1, m + 1))
    rows = []
    def payoff(a, z):
        return member[a] * (scale // np.maximum(np.array(z) @ member, 1))
    def walk(h):
        if len(h) == m:
            return tuple(h.count(a) for a in range(p))
        children = [walk(h + (a,)) for a in range(p)]
        a = actions[h]
        for b in range(p):
            if b != a:
                rows.append(payoff(a, children[a]) - payoff(b, children[b]))
        return children[a]
    z = walk(())
    G = np.unique(np.array(rows, dtype=np.int32), axis=0) / scale
    loads = np.array(z) @ member
    c = (loads > 0).astype(float)
    tax = loads / (loads + 1)
    return G, c, tax, member, z


def attack(actions, m, p, label):
    G, c, tax, member, z = matrix(actions, m, p)
    best = None
    targets = list(combinations(range(p), min(m, p)))
    for target in targets:
        o = (member[list(target)].sum(axis=0) > 0).astype(float)
        objective = o - c - tax
        res = linprog(-objective, A_ub=-G, b_ub=np.zeros(len(G)),
                      A_eq=[c], b_eq=[1], bounds=(0, None), method='highs')
        if not res.success:
            continue
        gap = float(-res.fun)
        if best is None or gap > best['gap']:
            best = dict(label=label, players=m, topics=p, target=target,
                        root=z, gap=gap, distinct_rows=len(G),
                        ordered_nodes=len(actions),
                        floating_weights=res.x.tolist())
        if gap > 1e-7:
            cone = StrategyCone(p, m, actions)
            weights = tuple(Fraction(float(x)).limit_denominator(10**7)
                            for x in res.x)
            if not cone.verify(weights) or dot(cone.welfare, weights) != 1:
                weights = cone.recover_vertex(res.x)
            if weights is None or not cone.verify(weights):
                best['positive_failed_exact_recovery'] = True
                continue
            exact_o = tuple(Fraction(int(any(t >> a & 1 for a in target)))
                            for t in range(1, 1 << p))
            exact_tax = tuple(Fraction(sum(z[a] for a in range(p) if t >> a & 1),
                                      1 + sum(z[a] for a in range(p) if t >> a & 1))
                              for t in range(1, 1 << p))
            exact_gap = dot(tuple(a-b-d for a,b,d in
                                  zip(exact_o, cone.welfare, exact_tax)), weights)
            if exact_gap <= 0:
                continue
            clones = integer_clones(weights)
            assert independently_verify(cone, clones)
            best.update(status='exact_full_policy_auxiliary_bridge_counterexample',
                        exact_gap=exact_gap,
                        weights=weights,
                        clones=clones,
                        actions=[dict(history=h, action=a)
                                 for h, a in sorted(actions.items())])
            return best
    if best:
        best.pop('floating_weights', None)
        best['status'] = 'finite_floating_cone_result_only'
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--games', type=int, default=40)
    ap.add_argument('--players', type=int, default=5)
    ap.add_argument('--topics', type=int, default=7)
    ap.add_argument('--seed', type=int, default=102110)
    ap.add_argument('--named', action='store_true')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if min(args.players, args.topics) < 1 or args.games < 0:
        ap.error('positive players/topics and nonnegative games required')
    if args.output.exists():
        ap.error('output already exists; keep frozen runs unchanged')
    rng = random.Random(args.seed)
    rows = []
    def accept(row):
        if row:
            rows.append(row)
            print(json.dumps(serializable({k:v for k,v in row.items()
                                            if k not in {'weights','clones','actions'}})),
                  flush=True)
        return row and 'counterexample' in row['status']
    if args.named:
        for path in sorted((ROOT/'evidence/certificates/customer_attraction').glob('*.json')):
            data = json.loads(path.read_text())
            if not isinstance(data, dict):
                continue
            policy = data.get('strategy', data.get('certificate', data))
            if not isinstance(policy, dict) or 'actions' not in policy:
                continue
            if not isinstance(policy['actions'], list) or any(
                    not isinstance(r, dict) or not {'history','action'} <= r.keys()
                    for r in policy['actions']):
                print(json.dumps(dict(skipped=str(path.relative_to(ROOT)),
                                      reason='unsupported alternate certificate schema')),
                      flush=True)
                continue
            actions = {tuple(r['history']): r['action'] for r in policy['actions']}
            if not actions:
                continue
            m = max(map(len, actions)) + 1
            p = max(max(actions.values()), max((max(h) for h in actions if h), default=0)) + 1
            if m > 6 or p > 8:
                continue
            if accept(attack(actions, m, p, str(path.relative_to(ROOT)))):
                break
    if not any('counterexample' in r['status'] for r in rows):
        for j in range(args.games):
            p,m = args.topics,args.players
            masks = rng.sample(range(1,1<<p),min(12,(1<<p)-1))
            ins = Instance(tuple(map(str,range(p))),tuple(
                CustomerType(frozenset(a for a in range(p) if t>>a&1),
                             rng.randrange(1,20)) for t in masks),m)
            sol = ExactSPESolver(ins)
            cert = sol.certificate(min(sol.worst_outcomes()),
                action_selector=lambda h,c:rng.choice(c),
                continuation_selector=lambda h,c:rng.choice(c))
            if accept(attack(cert.actions,m,p,f'random-{j}')):
                break
    report = dict(scope='finite complete-policy cone attack; not a universal proof',
                  parameters=vars(args)|{'output':str(args.output)}, results=rows)
    with args.output.open('x') as stream:
        json.dump(serializable(report), stream, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    main()
