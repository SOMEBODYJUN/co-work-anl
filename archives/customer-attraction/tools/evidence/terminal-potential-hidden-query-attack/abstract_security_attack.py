"""Finite discovery in a larger anonymous exact-potential class, NOT CAG.

Utilities have u(a,h)=F(h+a)-G(h), are nonnegative, and are smallest
when the added opponent clones a. All ordered-history SPE rows are kept.
Alternate game coefficients and the hidden query distribution; output only
an exact rational separation, or a bounded observation with no truth claim.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import itertools as it
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def attack(m, p, seeds, starts, rounds):
    ts = list(it.combinations_with_replacement(range(p), m))
    hs = list(it.combinations_with_replacement(range(p), m - 1))
    fi = {h: k for k, h in enumerate(ts)}
    gi = {h: len(ts) + k for k, h in enumerate(hs)}
    dim = len(ts) + len(hs)

    def u(a, h):
        r = np.zeros(dim)
        r[fi[tuple(sorted((*h, a)))]] = 1
        r[gi[tuple(sorted(h))]] = -1
        return r

    values = np.array([[u(a, h) for a in range(p)] for h in hs])
    positive = [v for block in values for v in block]
    clone = [u(a, (*h, b)) - u(a, (*h, a))
             for h in it.combinations_with_replacement(range(p), m - 2)
             for a, b in it.product(range(p), repeat=2) if a != b]
    best = 0.
    programs = 0
    for seed in range(seeds):
        rng = np.random.default_rng(640000 + seed)
        initial = rng.normal(size=dim)
        actions = {}

        def end(h):
            while len(h) < m:
                h = (*h, actions[h])
            return h

        for depth in reversed(range(m)):
            for h in it.product(range(p), repeat=depth):
                score = []
                for a in range(p):
                    q = end((*h, a))
                    score.append(u(a, q[:depth] + q[depth + 1:]) @ initial)
                top = max(score)
                actions[h] = int(rng.choice([a for a in range(p)
                                           if score[a] >= top - 1e-10]))
        path = end(())
        spe = []
        for h, a in actions.items():
            depth = len(h)
            chosen = end(h)
            row = u(a, chosen[:depth] + chosen[depth + 1:])
            for b in range(p):
                if b == a:
                    continue
                deviation = end((*h, b))
                spe.append(row - u(b, deviation[:depth] + deviation[depth + 1:]))
        base = np.array(positive + clone + spe)
        welfare = sum((u(a, path[:i] + path[i + 1:])
                       for i, a in enumerate(path)), np.zeros(dim))
        for trial in range(starts):
            query = np.ones(p) / p if trial == 0 else rng.dirichlet(np.ones(p))
            for iteration in range(rounds):
                caps = np.einsum('hap,a->hp', values, query)
                aub = np.vstack((np.column_stack((-base, np.zeros(len(base)))),
                                 np.column_stack((-caps, np.ones(len(caps))))))
                result = linprog(np.r_[np.zeros(dim), -1.], A_ub=aub,
                                 b_ub=np.zeros(len(aub)),
                                 A_eq=np.r_[welfare, 0.][None, :], b_eq=[1.],
                                 bounds=[(-20., 20.)] * dim + [(0., None)],
                                 method='highs')
                programs += 1
                if not result.success:
                    break
                game = result.x[:-1]
                matrix = np.einsum('hap,p->ha', values, game)
                primal = linprog(np.r_[np.zeros(p), -1.],
                                 A_ub=np.column_stack((-matrix, np.ones(len(hs)))),
                                 b_ub=np.zeros(len(hs)),
                                 A_eq=np.r_[np.ones(p), 0.][None, :], b_eq=[1.],
                                 bounds=[(0., None)] * (p + 1), method='highs')
                programs += 1
                if not primal.success:
                    break
                query = primal.x[:-1]
                best = max(best, float(primal.x[-1]))
                if primal.x[-1] <= 1. / m + 1e-7:
                    continue
                coeffs = [Q(float(x)).limit_denominator(100000) for x in game]
                probs = [Q(float(x)).limit_denominator(100000) for x in query]

                def dot(row):
                    return sum((int(x) * v for x, v in zip(row, coeffs)), Q())

                if any(dot(row) < 0 for row in base) or dot(welfare) != 1:
                    continue
                if min(probs) < 0 or sum(probs) != 1:
                    continue
                security = min(sum((probs[a] * dot(u(a, h))
                                    for a in range(p)), Q()) for h in hs)
                if security <= Q(1, m):
                    continue
                return dict(status='exact_abstract_separation', m=m, p=p,
                            seed=640000 + seed, start=trial, iteration=iteration,
                            query=list(map(str, probs)), security=str(security),
                            W='1', weak_bridge_also_fails=security > Q(2, 2*m-1),
                            F=list(map(str, coeffs[:len(ts)])),
                            G=list(map(str, coeffs[len(ts):])),
                            terminals=ts, backgrounds=hs, path=path,
                            actions=[dict(history=h, action=a)
                                     for h, a in sorted(actions.items())],
                            checked_rows=len(base), programs=programs,
                            scope='NOT a customer-attraction instance')
    return dict(status='finite_no_separation', m=m, p=p, seeds=seeds,
                starts=starts, rounds=rounds, programs=programs,
                best_numerical_security=best,
                scope='No universal truth conclusion, not original CAG')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--m', type=int, default=4)
    ap.add_argument('--p', type=int, default=4)
    ap.add_argument('--seeds', type=int, default=20)
    ap.add_argument('--starts', type=int, default=4)
    ap.add_argument('--rounds', type=int, default=3)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    report = attack(args.m, args.p, args.seeds, args.starts, args.rounds)
    with args.output.open('x') as f:
        json.dump(report, f, indent=2)
        f.write('\n')
    print(json.dumps({k: v for k, v in report.items()
                      if k not in {'F', 'G', 'actions', 'terminals', 'backgrounds'}}, indent=2))
