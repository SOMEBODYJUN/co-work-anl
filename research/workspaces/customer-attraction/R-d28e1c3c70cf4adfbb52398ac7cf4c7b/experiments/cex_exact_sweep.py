"""Integer-scaled set-valued backward induction for finite candidate searches.

This is an exploratory accelerator, not a general welfare proof. Payoffs are
scaled by lcm(1,...,m), and integer inputs keep every tie exactly. Counts cache
sets of achievable terminal counts, never a single common continuation policy.
Any potential target counterexample must additionally receive a complete
ordered-history canonical certificate and independent definition-level check.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement
import json
from math import lcm
from pathlib import Path
import random
import sys
import time

import numpy as np

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "customer_attraction" / "__init__.py").is_file())
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance


def counts(p, m):
    for z in combinations_with_replacement(range(p), m):
        yield tuple(z.count(a) for a in range(p))


class IntegerSetSolver:
    def __init__(self, p, m):
        self.p, self.m = p, m
        self.scale = lcm(*range(1, m + 1))
        self.types = tuple(range(1, 1 << p))
        self.terminals = tuple(counts(p, m))
        self.tindex = {q: j for j, q in enumerate(self.terminals)}
        self.layers = [tuple(counts(p, d)) for d in range(m + 1)]
        self.states = tuple(q for layer in self.layers for q in layer)
        self.sindex = {q: j for j, q in enumerate(self.states)}
        self.children = {}
        for q in self.states:
            if sum(q) == m:
                continue
            self.children[self.sindex[q]] = tuple(self.sindex[q[:a] + (q[a] + 1,) + q[a+1:]] for a in range(p))
        self.coverage = np.zeros((len(self.terminals), len(self.types)), dtype=np.int64)
        self.rows = np.zeros((len(self.terminals), p, len(self.types)), dtype=np.int64)
        for j, q in enumerate(self.terminals):
            for k, mask in enumerate(self.types):
                den = sum(q[a] for a in range(p) if mask & (1 << a))
                if not den:
                    continue
                self.coverage[j, k] = 1
                for a in range(p):
                    if mask & (1 << a):
                        self.rows[j, a, k] = self.scale // den

    def solve(self, weights):
        w = np.asarray(weights, dtype=np.int64)
        assert w.shape == (len(self.types),) and np.all(w >= 0)
        # Enforce an explicit conservative bound before using int64 arithmetic.
        assert int(sum(map(int, w))) * self.scale < 2**62
        utility = self.rows @ w
        welfare = self.coverage @ w
        outcomes = [None] * len(self.states)
        for q, j in self.tindex.items():
            outcomes[self.sindex[q]] = np.asarray([j], dtype=np.int64)
        for d in range(self.m - 1, -1, -1):
            for q in self.layers[d]:
                idx = self.sindex[q]
                child = tuple(outcomes[j] for j in self.children[idx])
                threshold = max(int(np.min(utility[c, a])) for a, c in enumerate(child))
                keep = tuple(c[utility[c, a] >= threshold] for a, c in enumerate(child))
                outcomes[idx] = np.unique(np.concatenate(keep))
                assert len(outcomes[idx]) > 0
        roots = outcomes[0]
        self.last_utility, self.last_welfare, self.last_outcomes = utility, welfare, outcomes
        worst = int(roots[np.argmin(welfare[roots])])
        return dict(minimum=int(welfare[worst]), optimum=int(np.max(welfare)),
                    worst_counts=self.terminals[worst], root_outcomes=tuple(self.terminals[int(j)] for j in roots))


class BackgroundIntegerSolver(IntegerSetSolver):
    """Same outcome-set recursion with a fixed legal prefix and tail-profit objective.

    `m` is the number of remaining providers. Returned objective integers are
    scaled by `scale`; the efficiency ratio is unchanged. The returned counts
    count only remaining providers, so add `background` before canonical checks.
    """
    def __init__(self, p, m, background):
        super().__init__(p, m)
        assert len(background) == p and min(background) >= 0
        self.background = tuple(background)
        self.scale = lcm(*range(1, m + sum(background) + 1))
        for j, delta in enumerate(self.terminals):
            for k, mask in enumerate(self.types):
                d = sum(delta[a] for a in range(p) if mask & (1 << a))
                b = sum(background[a] for a in range(p) if mask & (1 << a))
                den = b + d
                self.coverage[j, k] = d * self.scale // den if den else 0
                for a in range(p):
                    self.rows[j, a, k] = self.scale // den if den and mask & (1 << a) else 0


def background_search(p, m, trials, seed, background):
    solver = BackgroundIntegerSolver(p, m, background)
    rng = random.Random(seed); best = Fraction(0); records = []
    weights = [0] * ((1 << p)-1)
    weights[0] = m + sum(background)
    for a in range(1,p): weights[(1 << a)-1] = 1
    champion = weights.copy(); started = time.monotonic()
    for trial in range(trials):
        if trial and trial % 50 == 0:
            weights = [rng.randrange(1, 21) if rng.random() < .12 else 0 for _ in weights]
        elif trial:
            weights = champion.copy()
            for _ in range(rng.randrange(1,5)):
                j = rng.randrange(len(weights))
                weights[j] = max(0, weights[j] + rng.choice((-3,-2,-1,1,2,3)))
        out = solver.solve(weights)
        ratio = Fraction(out['optimum'], out['minimum']) if out['minimum'] else Fraction(1)
        if ratio >= best:
            if ratio > best or rng.random() < .15: champion = weights.copy()
            if ratio > best:
                best = ratio
                row = dict(trial=trial, ratio=str(ratio), weights=weights,
                           minimum_scaled=out['minimum'], optimum_scaled=out['optimum'], worst_counts=out['worst_counts'])
                records.append(row); print(json.dumps(row), flush=True)
    return dict(scope='finite exact background tail-profit search only; no universal proof',
                remaining_players=m,topics=p,background=background,scale=solver.scale,trials=trials,
                seed=seed,elapsed_seconds=time.monotonic()-started,best_ratio=str(best),records=records)


def instance(p, m, w):
    return Instance(tuple(map(str, range(p))), tuple(CustomerType(frozenset(a for a in range(p) if mask & (1 << a)), int(v)) for mask, v in enumerate(w, 1) if v), m)


def self_test():
    rng = random.Random(22102026)
    checked = 0
    for p, m in ((1, 1), (2, 3), (3, 4), (4, 3), (3, 5)):
        accelerated = IntegerSetSolver(p, m)
        inputs = [[0] * ((1 << p) - 1), [1] * ((1 << p) - 1)]
        inputs += [[rng.randrange(4) for _ in range((1 << p) - 1)] for j in range(8)]
        for weights in inputs:
            out = accelerated.solve(weights)
            canonical = ExactSPESolver(instance(p, m, weights))
            assert set(out['root_outcomes']) == set(canonical.outcomes())
            assert out['minimum'] == canonical.minimum_welfare()
            assert out['optimum'] == canonical.instance.optimal_welfare()
            checked += 1
    background_checked = 0
    for p,m,background in ((2,2,(1,0)), (3,3,(0,2,1)), (4,2,(0,2,0,1))):
        accelerated = BackgroundIntegerSolver(p,m,background)
        for trial in range(10):
            weights = [rng.randrange(4) for _ in range((1 << p)-1)]
            out = accelerated.solve(weights)
            canonical = ExactSPESolver(instance(p,m+sum(background),weights))
            full_outcomes = {tuple(q[a]+background[a] for a in range(p)) for q in out['root_outcomes']}
            assert full_outcomes == canonical.outcomes(background)
            def profit(q):
                return sum(weights[k] * Fraction(sum((q[a]-background[a]) for a in range(p) if mask&(1<<a)),
                                                sum(q[a] for a in range(p) if mask&(1<<a)))
                           for k,mask in enumerate(accelerated.types)
                           if sum(q[a] for a in range(p) if mask&(1<<a)))
            assert Fraction(out['minimum'],accelerated.scale) == min(map(profit,full_outcomes))
            all_counts = (tuple(q[a]+background[a] for a in range(p)) for q in accelerated.terminals)
            assert Fraction(out['optimum'],accelerated.scale) == max(map(profit,all_counts))
            background_checked += 1
    return dict(status='PASS', exact_canonical_comparisons=checked,
                background_exact_canonical_comparisons=background_checked)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--self-test', action='store_true')
    ap.add_argument('--topics', type=int, default=7)
    ap.add_argument('--players', type=int, default=5)
    ap.add_argument('--trials', type=int, default=1000)
    ap.add_argument('--seed', type=int, default=20261021)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--background', help='comma-separated fixed-prefix topic counts; then --players counts tail players')
    args = ap.parse_args()
    if args.self_test:
        print(json.dumps(self_test())); return
    if args.output and args.output.exists(): raise FileExistsError(args.output)
    p, m = args.topics, args.players
    if args.background:
        background = tuple(map(int,args.background.split(',')))
        report = background_search(p,m,args.trials,args.seed,background)
        if args.output: args.output.write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k!='records'}),flush=True)
        return
    solver = IntegerSetSolver(p, m); rng = random.Random(args.seed)
    started = time.monotonic(); best = Fraction(0); records=[]
    base = [0] * ((1 << p) - 1)
    base[0] = m
    for a in range(1, min(p,m)): base[(1 << a)-1] = 1
    champion = base.copy()
    for trial in range(args.trials):
        if trial == 0: weights = base.copy()
        elif trial % 50 == 0:
            # Sparse arbitrary overlaps; diverse random restarts.
            weights = [rng.randrange(1, 21) if rng.random() < .12 else 0 for _ in base]
        elif trial % 17 == 0:
            weights = [0] * len(base)
            for a in range(p): weights[(1 << a)-1] = rng.randrange(1, m+2)
            for _ in range(rng.randrange(1, p+1)): weights[rng.randrange(len(base))] += rng.randrange(1, m+2)
        else:
            weights = champion.copy()
            for _ in range(rng.randrange(1, 5)):
                j = rng.randrange(len(base))
                weights[j] = max(0, weights[j] + rng.choice((-3,-2,-1,1,2,3)))
        out = solver.solve(weights)
        ratio = Fraction(out['optimum'], out['minimum']) if out['minimum'] else Fraction(1)
        if ratio >= best:
            if ratio > best or rng.random() < .15: champion = weights.copy()
            if ratio > best:
                best = ratio
                row = dict(trial=trial, ratio=str(ratio), weights=weights,
                           minimum=out['minimum'], optimum=out['optimum'], worst_counts=out['worst_counts'])
                records.append(row); print(json.dumps(row), flush=True)
    report = dict(scope='finite exact integer set-valued search only; no universal proof',
                  players=m,topics=p,trials=args.trials,seed=args.seed,
                  elapsed_seconds=time.monotonic()-started,best_ratio=str(best),records=records)
    if args.output: args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='records'}),flush=True)


if __name__=='__main__': main()
