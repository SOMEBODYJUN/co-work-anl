"""Exploratory full-policy cone LP attack; numerical optima are not proofs.

Every retained numerical candidate must be rationalized and checked against all
ordered-history inequalities before it is called a counterexample.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import random
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import CustomerType, Instance
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate


def all_types(k):
    return tuple(frozenset(a for a in range(k) if mask >> a & 1)
                 for mask in range(1, 1 << k))


def payoff_row(counts, action, types):
    return tuple(Fraction(int(action in t), sum(counts[a] for a in t))
                 if action in t else Fraction(0) for t in types)


def cone(instance, cert, types):
    rows = set()
    def walk(h):
        if len(h) == instance.players:
            return instance.counts(h, terminal=True)
        branches = [walk(h + (a,)) for a in range(instance.topic_count)]
        a = cert.actions[h]
        own = payoff_row(branches[a], a, types)
        for b, terminal in enumerate(branches):
            if b == a:
                continue
            alt = payoff_row(terminal, b, types)
            row = tuple(y - x for x, y in zip(own, alt))
            if any(row):
                rows.add(row)
        return branches[a]
    walk(())
    return tuple(rows)


def attack(seed, k, m, rounds, output, strong=False):
    rng = random.Random(seed)
    types = all_types(k)
    best = 0.0
    for iteration in range(rounds):
        # Mix dense and sparse integral games, retaining all customer types as
        # variables in the subsequent full-strategy cone.
        support = rng.sample(types, rng.randint(k, min(len(types), 3*k)))
        game = Instance(tuple(f'T{a}' for a in range(k)), tuple(
            CustomerType(t, rng.randint(1, 20)) for t in support), m)
        solver = ExactSPESolver(game)
        candidates = sorted(solver.outcomes(), key=game.welfare)[:3]
        for target in candidates:
            cert = solver.certificate(target)
            verified = verify_certificate(game, cert)
            verified.assert_valid()
            history = verified.terminal_history
            rows = cone(game, cert, types)
            A = np.array(rows, dtype=float)
            w = np.array([int(any(target[a] for a in t)) for t in types], dtype=float)
            if not np.any(w):
                continue
            # Include all distinct m-theme portfolios. Repeats cannot improve
            # coverage, so smaller portfolios extend to one of these.
            portfolios = combinations(range(k), min(k, m))
            for portfolio in portfolios:
                o = np.array([int(bool(t.intersection(portfolio))) for t in types], dtype=float)
                for a in set(history):
                    p = np.array(payoff_row(target, a, types), dtype=float)
                    coefficient = m - 1 if strong else m
                    obj = w + coefficient*p - o
                    lp = linprog(obj, A_ub=A, b_ub=np.zeros(len(A)),
                                 A_eq=w.reshape(1,-1), b_eq=[1.0],
                                 bounds=(0, None), method='highs')
                    if lp.status == 3 or (lp.success and lp.fun < best - 1e-7):
                        best = -1e99 if lp.status == 3 else float(lp.fun)
                        report = {'status': 'NUMERICAL CANDIDATE, NOT EXACTLY VERIFIED',
                                  'seed': seed, 'iteration': iteration, 'k': k, 'm': m,
                                  'objective': best, 'topic': a,
                                  'payoff_coefficient': coefficient,
                                  'portfolio': list(portfolio),
                                  'initial_instance': game.to_dict(),
                                  'certificate': cert.to_dict(),
                                  'type_masks': [sum(1 << a for a in t) for t in types],
                                  'weights': None if lp.x is None else list(lp.x),
                                  'cone_rows': len(rows)}
                        output.write_text(json.dumps(report, indent=2) + '\n')
                        print(json.dumps({key: report[key] for key in
                              ('iteration','k','m','objective','topic','portfolio','cone_rows')}), flush=True)
                        return
        if iteration % 10 == 0:
            print(json.dumps({'iteration': iteration, 'k': k, 'm': m,
                              'best_negative_objective': best}), flush=True)
    output.write_text(json.dumps({'status': 'finite numerical search only', 'seed': seed,
                                  'k': k, 'm': m, 'rounds': rounds,
                                  'payoff_coefficient': m-1 if strong else m,
                                  'best_negative_objective': best}, indent=2) + '\n')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=61)
    ap.add_argument('--k', type=int, default=5)
    ap.add_argument('--m', type=int, default=4)
    ap.add_argument('--rounds', type=int, default=100)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--strong', action='store_true',
                    help='Attack the stronger W+(m-1)u_i>=OPT bridge.')
    args = ap.parse_args()
    attack(args.seed, args.k, args.m, args.rounds, args.output, args.strong)
