"""Targeted attack on the general child-SPE query-row inequality.

This is a floating-point discovery tool. Any hit must be independently checked
with exact rational full-history SPE certificates before it is a conclusion.
"""
import argparse
import itertools
import json
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for a in range(n + 1):
            for tail in compositions(n - a, k - 1):
                yield (a,) + tail


class Topology:
    def __init__(self, m, k):
        self.m, self.k = m, k
        self.counts = np.array(list(compositions(m, k)), dtype=int)
        self.index = {tuple(c): i for i, c in enumerate(self.counts)}
        self.masks = np.arange(1, 2**k)
        self.inc = ((self.masks[:, None] >> np.arange(k)) & 1).astype(float)
        self.loads = self.counts @ self.inc.T
        self.cover = (self.loads > 0).astype(float)
        self.kernels = np.divide(
            self.inc.T[None, :, :], self.loads[:, None, :],
            out=np.zeros((len(self.counts), k, len(self.masks))),
            where=self.loads[:, None, :] > 0,
        )
        self.zero = (0,) * k
        self.child_states = []
        for a in range(k):
            c = list(self.zero)
            c[a] = 1
            self.child_states.append(tuple(c))

    def attack(self, weights):
        payoffs = self.kernels @ weights
        welfare = self.cover @ weights

        @lru_cache(None)
        def solve(c):
            if sum(c) == self.m:
                return frozenset([self.index[c]])
            children = []
            for a in range(self.k):
                d = list(c)
                d[a] += 1
                children.append(solve(tuple(d)))
            floor = max(min(payoffs[t, a] for t in child)
                        for a, child in enumerate(children))
            return frozenset(t for a, child in enumerate(children)
                             for t in child if payoffs[t, a] >= floor - 1e-8)

        children = [solve(c) for c in self.child_states]
        floors = np.array([min(payoffs[t, a] for t in child)
                           for a, child in enumerate(children)])
        base = self.counts @ floors - welfare
        best = None
        for a, child in enumerate(children):
            for t in child:
                gaps = base + welfare[t] + self.counts[:, a] * (payoffs[t, a] - floors[a])
                q = int(gaps.argmin())
                value = gaps[q]
                if best is None or value < best[0]:
                    best = (value, a, t, q)
        gap, a, t, q = best
        query_outcomes = [min(child, key=lambda z: payoffs[z, b])
                          for b, child in enumerate(children)]
        query_outcomes[a] = t
        return dict(
            gap=float(gap), actual_action=int(a),
            actual_counts=self.counts[t].tolist(),
            comparator_counts=self.counts[q].tolist(),
            query_counts=[self.counts[x].tolist() for x in query_outcomes],
            parent_is_optimal=bool(payoffs[t, a] >= max(floors) - 1e-8),
            welfare=int(welfare[t]), comparison_coverage=int(welfare[q]),
            weights=[int(x) for x in weights], m=self.m, k=self.k,
        )

    def policy_cone_attack(self, weights, actual_action, actual_counts, comparator_counts, empty_topic=False):
        """Optimize the exact proposed row over one full child-policy cone."""
        payoffs = self.kernels @ weights

        @lru_cache(None)
        def solve(c):
            if sum(c) == self.m:
                return frozenset([self.index[c]])
            children = []
            for a in range(self.k):
                d = list(c)
                d[a] += 1
                children.append(solve(tuple(d)))
            floor = max(min(payoffs[t, a] for t in child)
                        for a, child in enumerate(children))
            return frozenset(t for a, child in enumerate(children)
                             for t in child if payoffs[t, a] >= floor - 1e-8)

        actions, leaves, constraints = {}, {}, []

        def inc(c, a):
            d = list(c)
            d[a] += 1
            return tuple(d)

        def expand(h, c, desired):
            if len(h) == self.m:
                return desired
            children = [solve(inc(c, a)) for a in range(self.k)]
            floors = [min(payoffs[t, a] for t in child)
                      for a, child in enumerate(children)]
            admissible = [a for a, child in enumerate(children)
                          if desired in child and payoffs[desired, a] >= max(floors) - 1e-8]
            chosen = admissible[0]
            actions[h] = chosen
            child_leaves = []
            for a, child in enumerate(children):
                t = desired if a == chosen else min(child, key=lambda t: payoffs[t, a])
                child_leaves.append(expand(h + (a,), inc(c, a), t))
            for a, t in enumerate(child_leaves):
                if a != chosen:
                    constraints.append(self.kernels[desired, chosen] - self.kernels[t, a])
            leaves[h] = desired
            return desired

        query_leaves = []
        for a, c in enumerate(self.child_states):
            child = solve(c)
            t = self.index[tuple(actual_counts)] if a == actual_action else min(child, key=lambda t: payoffs[t, a])
            query_leaves.append(expand((a,), c, t))
        d = np.array(comparator_counts)
        actual = query_leaves[actual_action]
        comparator = self.index[tuple(comparator_counts)]
        objective = self.cover[actual] - self.cover[comparator]
        for a, times in enumerate(d):
            objective = objective + times * self.kernels[query_leaves[a], a]
        bounds = [(0, 0) if empty_topic and mask & 1 else (0, None) for mask in self.masks]
        result = linprog(objective, A_ub=-np.array(constraints), b_ub=np.zeros(len(constraints)),
                         A_eq=np.ones((1, len(weights))), b_eq=[1.0], bounds=bounds, method='highs')
        if not result.success:
            raise RuntimeError(result.message)
        return result, actions


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--m', type=int, default=4)
    p.add_argument('--k', type=int, default=6)
    p.add_argument('--trials', type=int, default=500)
    p.add_argument('--seed', type=int, default=719)
    p.add_argument('--output', type=Path)
    p.add_argument('--cones', action='store_true')
    p.add_argument('--empty', action='store_true')
    p.add_argument('--optimal_comparator', action='store_true')
    args = p.parse_args()
    rng = np.random.default_rng(args.seed)
    top = Topology(args.m, args.k)
    best = None
    for z in range(args.trials):
        weights = rng.integers(0, 12, size=2**args.k - 1)
        weights[rng.random(len(weights)) < 0.75] = 0
        if args.empty:
            weights[top.masks & 1 == 1] = 0
        result = top.attack(weights)
        if best is None or result['gap'] < best['gap']:
            best = result
            print(z, json.dumps(best), flush=True)
        if best['gap'] < -1e-6:
            break
        if args.cones:
            comparator = result['comparator_counts']
            if args.optimal_comparator:
                comparator = top.counts[int((top.cover @ weights).argmax())].tolist()
            lp, actions = top.policy_cone_attack(weights, result['actual_action'], result['actual_counts'], comparator, args.empty)
            if lp.fun < -1e-7:
                best = dict(result, comparator_counts=comparator, lp_gap=float(lp.fun), lp_weights=lp.x.tolist(),
                            actions={','.join(map(str, h)): a for h, a in actions.items()})
                print('CONE_HIT', json.dumps(best), flush=True)
                break
    if args.output:
        args.output.write_text(json.dumps(best, indent=2) + '\n')


if __name__ == '__main__':
    main()
