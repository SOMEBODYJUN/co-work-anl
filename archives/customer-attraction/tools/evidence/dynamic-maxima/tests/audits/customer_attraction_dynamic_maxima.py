"""Independent exact finite attack on the dynamic maximal-routing proof.
No imports from the repository model, solver, or earlier audits.
The full-menu recursion permits independent child choices at ordered histories.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import lcm
import json
import random
from pathlib import Path
import argparse
import hashlib


def wt(mask, weights):
    return sum(w for x, w in enumerate(weights) if mask >> x & 1)


def structure(catalog, weights):
    distinct = set(catalog)
    maxima = tuple(sorted(a for a in distinct if not any(a != b and a & b == a for b in distinct)))
    union = 0
    core = maxima[0]
    for b in maxima:
        union |= b
        core &= b
    route = tuple(next(j for j, b in enumerate(maxima) if a & b == a) for a in catalog)
    incidences = tuple(sum(1 << j for j, b in enumerate(maxima) if b >> x & 1)
                       for x in range(len(weights)))
    blocks = {i: sum(w for x, w in enumerate(weights) if incidences[x] == i)
              for i in range(1, 1 << len(maxima))}
    return maxima, wt(union, weights), wt(core, weights), route, blocks


def compositions(total, m):
    if m == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, m - 1):
                yield (first,) + rest


class Audit:
    def __init__(self, catalog, weights, n, stats):
        self.catalog, self.weights, self.n = tuple(catalog), tuple(weights), n
        self.m, self.stats = len(catalog), stats
        self.maxima, self.U, self.c, self.route, self.blocks = structure(catalog, weights)
        self.s = len(self.maxima)
        self.scale = lcm(*range(1, n + 1))
        self.chosen = {}
        self.threshold = {}
        self.D = tuple(max(F(t) + F(self.s * (n - t), 2), F(n + self.s - 1)) for t in range(n))
        self.ell = tuple(F(self.c, n) + F(self.U - self.c, 1) / d for d in self.D)
        self.gamma = sum((1 / d for d in self.D), F(0))
        self.P = sum(w for incidence, w in self.blocks.items() if incidence.bit_count() == 1 and self.s >= 2)
        self.V = self.U - self.c - self.P
        rawA = [F(n+t, 2*(t+1)) / (F(t) + F(self.s*(n-t),2)) for t in range(n-1)] + [F(1,n+self.s-1)]
        rawB = [1 / (F(t) + F(self.s*(n-t),2)) for t in range(n-1)] + [F(n+1,n*(n+self.s-1))]
        self.alpha = tuple(min(rawA[t:]) for t in range(n))
        self.beta = tuple(min(rawB[t:]) for t in range(n))
        self.mixed_ell = tuple(F(self.c,n) + self.P * a + self.V * b for a,b in zip(self.alpha,self.beta))

    def add(self, q, a):
        return q[:a] + (q[a] + 1,) + q[a + 1:]

    @lru_cache(None)
    def payoff(self, q, a):
        value = 0
        for x, w in enumerate(self.weights):
            if w and self.catalog[a] >> x & 1:
                d = sum(q[b] for b, mask in enumerate(self.catalog) if mask >> x & 1)
                assert d > 0 and self.scale % d == 0
                value += w * (self.scale // d)
        return value

    def welfare(self, q):
        union = 0
        for a, count in enumerate(q):
            if count:
                union |= self.catalog[a]
        return wt(union, self.weights)

    def coefficients(self, q):
        if self.s == 1:
            return
        p = tuple(sum(q[a] for a in range(self.m) if self.route[a] == j)
                  for j in range(self.s))
        t, r = sum(q), self.n - sum(q)
        f = []
        for j in range(self.s):
            val = F(0)
            for incidence, w in self.blocks.items():
                if incidence == (1 << self.s) - 1 or not (incidence >> j & 1):
                    continue
                pI = sum(p[k] for k in range(self.s) if incidence >> k & 1)
                d = p[j] + 1 if incidence.bit_count() == 1 else pI + r
                val += F(w, d)
            f.append(val)
        y = tuple(F(pj) + (F(r, 2) if r >= 2 else 1) for pj in p)
        for incidence, w in self.blocks.items():
            if incidence == (1 << self.s) - 1 or not w:
                continue
            pI = sum(p[k] for k in range(self.s) if incidence >> k & 1)
            d = pI + 1 if incidence.bit_count() == 1 else pI + r
            coefficient = sum(y[k] for k in range(self.s) if incidence >> k & 1) / d
            assert coefficient >= 1, (p, incidence, coefficient)
            self.stats['positive_type_coefficients'] += 1
        assert self.U - self.c <= sum(yj * fj for yj, fj in zip(y, f))
        assert max(f) >= F(self.U - self.c) / self.D[t]
        self.stats['dynamic_budget_states'] += 1

    @lru_cache(None)
    def solve(self, q):
        self.stats['count_states'] += 1
        if sum(q) == self.n:
            return frozenset((q,))
        self.coefficients(q)
        replies = tuple(self.solve(self.add(q, a)) for a in range(self.m))
        floor = max(min(self.payoff(terminal, a) for terminal in replies[a]) for a in range(self.m))
        self.threshold[q] = floor
        options = tuple(frozenset(terminal for terminal in replies[a] if self.payoff(terminal, a) >= floor)
                        for a in range(self.m))
        self.chosen[q] = options
        for a, menu in enumerate(options):
            for terminal in menu:
                if self.s >= 2:
                    assert F(self.payoff(terminal, a), self.scale) >= self.ell[sum(q)], (
                        self.catalog, self.weights, self.n, q, a, terminal,
                        F(self.payoff(terminal, a), self.scale), self.ell[sum(q)])
                if self.s >= 2:
                    assert F(self.payoff(terminal,a),self.scale) >= self.mixed_ell[sum(q)]
                    self.stats['mixed_mass_payoff_comparisons'] += 1
                self.stats['position_payoff_comparisons'] += 1
        retained = frozenset(terminal for menu in options for terminal in menu)
        assert retained
        return retained

    def audit(self, materialize=False):
        root = self.solve((0,) * self.m)
        self.stats['root_outcomes'] += len(root)
        optimum = max(self.welfare(tuple(int(a in chosen) for a in range(self.m)))
                      for count in range(min(self.m,self.n)+1)
                      for chosen in combinations(range(self.m),count))
        for terminal in root:
            W = self.welfare(terminal)
            if self.s >= 2:
                assert W >= self.c + self.gamma * (self.U - self.c)
                assert W >= self.c + self.P * sum(self.alpha) + self.V * sum(self.beta)
            else:
                assert W == self.U
            if self.s <= 4 and self.n >= 3:
                assert self.U <= 2 * W - self.c
            if self.s <= 5:
                assert optimum <= 2 * W
                if self.n >= 5:
                    assert self.U <= 2 * W - self.c
            if self.n == 1:
                assert W == max(wt(a, self.weights) for a in self.catalog)
        if materialize:
            for terminal in sorted(root)[:3]:
                self.materialize(terminal)
        if any(a == 0 for a in self.catalog):
            self.stats['empty_action_cases'] += 1
        if len(set(self.catalog)) < self.m:
            self.stats['duplicate_label_cases'] += 1
        fullcore = self.maxima[0]
        for b in self.maxima[1:]:
            fullcore &= b
        if fullcore and any(a & fullcore != fullcore for a in self.catalog):
            self.stats['core_omission_cases'] += 1
        nonemptyI = [i for i, w in self.blocks.items() if w]
        if any(i & j and i & ~j and j & ~i for i, j in combinations(nonemptyI, 2)):
            self.stats['crossed_incidence_cases'] += 1
        self.stats['cases'] += 1

    def materialize(self, target):
        strategy = {}
        def expand(h, q, desired):
            if len(h) == self.n:
                assert q == desired
                return
            candidates = [a for a in range(self.m) if desired in self.chosen[q][a]]
            assert candidates
            picked = candidates[0]
            strategy[h] = picked
            for a in range(self.m):
                child = self.add(q, a)
                desired_child = desired if a == picked else min(self.solve(child), key=lambda z: (self.payoff(z, a), z))
                expand(h + (a,), child, desired_child)
        expand((), (0,) * self.m, target)
        @lru_cache(None)
        def follow(h):
            if len(h) == self.n:
                return h
            return follow(h + (strategy[h],))
        histories = {h for t in range(self.n) for h in product(range(self.m), repeat=t)}
        assert set(strategy) == histories
        for h in histories:
            chosen_terminal = follow(h)
            q = tuple(chosen_terminal.count(a) for a in range(self.m))
            a = strategy[h]
            for deviation in range(self.m):
                deviating_terminal = follow(h + (deviation,))
                qdev = tuple(deviating_terminal.count(b) for b in range(self.m))
                assert self.payoff(q, a) >= self.payoff(qdev, deviation)
                self.stats['full_ordered_history_deviations'] += 1
            if self.s >= 2:
                assert F(self.payoff(q, a), self.scale) >= self.ell[len(h)]
                assert F(self.payoff(q, a), self.scale) >= self.mixed_ell[len(h)]
        self.stats['materialized_strategies'] += 1
        self.stats['materialized_histories'] += len(histories)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--random-cases', type=int, default=100)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error('refusing to overwrite existing output')
    stats = {key: 0 for key in [
        'cases','count_states','dynamic_budget_states','positive_type_coefficients',
        'position_payoff_comparisons','mixed_mass_payoff_comparisons','root_outcomes','empty_action_cases',
        'duplicate_label_cases','core_omission_cases','crossed_incidence_cases',
        'materialized_strategies','materialized_histories','full_ordered_history_deviations']}
    def run(catalog, weights, n, materialize=False):
        Audit(catalog, weights, n, stats).audit(materialize)

    # Zero customers, empty actions, duplicate labels, and one maximal action.
    for n in range(1, 8):
        run([0, 0], [0], n, n <= 4)
        run([3, 1, 0, 3], [2, 3], n, n <= 3)

    # Exhaust all graph-only four-index incidence patterns and all n=3,5.
    types = [1 << j for j in range(4)] + [sum(1 << j for j in pair) for pair in combinations(range(4),2)]
    maxima = [sum(1 << x for x, incidence in enumerate(types) if incidence >> j & 1) for j in range(4)]
    for graph in range(64):
        weights = [1] * 4 + [(graph >> k) & 1 for k in range(6)]
        catalog = [a & sum(1 << x for x, w in enumerate(weights) if w) for a in maxima]
        for n in (3, 5):
            run(catalog, weights, n, graph in (0, 63) and n == 3)

    # Exact previous static-seat obstruction: private 2n, triangle pair blocks n.
    for n in (3,4,5,7,9):
        run([1, 6, 10, 12], [2*n, n, n, n], n, n == 5)

    # Five maxima, five providers, full crossed incidence and an omitted core.
    types5 = list(range(1,32))
    weights5 = [7 if incidence == 31 else incidence.bit_count() for incidence in types5]
    maxima5 = [sum(1 << x for x, incidence in enumerate(types5) if incidence >> j & 1)
               for j in range(5)]
    run(maxima5 + [maxima5[0] & ~(1 << 30), 0], weights5, 5, True)

    # All maximal incidence types, arbitrary subset actions including omitted core.
    rng = random.Random(20261010)
    for index in range(args.random_cases):
        s = 2 + index % 5
        types = list(range(1, 1 << s))
        # Always positive singleton witnesses preserve the intended distinct maxima.
        weights = [rng.randrange(1, 6) if incidence.bit_count() == 1 else rng.randrange(0, 7) for incidence in types]
        maxima = [sum(1 << x for x, incidence in enumerate(types) if incidence >> j & 1 and weights[x]) for j in range(s)]
        catalog = list(maxima)
        for _ in range(index % 3):
            b = rng.choice(maxima)
            catalog.append(sum(1 << x for x in range(len(types)) if b >> x & 1 and rng.randrange(2)))
        if index % 7 == 0:
            catalog += [0]
        if index % 11 == 0:
            catalog += [catalog[-1]]
        n = (1,2,3,4,5,6,7)[index % 7]
        # Keep large action catalogs computationally compact without dropping ties.
        if len(catalog) >= 8:
            n = min(n, 4)
        run(catalog, weights, n, index < 5 and n <= 4)

    # Symbolic denominator / harmonic identity exact regressions.
    for n in range(3, 101):
        D = [max(F(2*n-t), F(n+3)) for t in range(n)]
        assert all(d <= 2*n for d in D)
        assert sum((1/d for d in D), F(0)) == sum((F(1,d) for d in range(n+4,2*n+1)),F(0)) + F(3,n+3)
    # Five-maxima five-provider fixed coefficient table and mixed sum.
    raw_private = [F(1,5),F(3,22),F(7,57),F(1,8),F(1,9)]
    shared = [F(2,25),F(1,11),F(2,19),F(1,8),F(2,15)]
    assert all(a >= F(1,9) for a in raw_private)
    assert shared == sorted(shared)
    assert sum(shared) == F(67027,125400) > F(1,2)
    assert F(5,9) > F(67027,125400)
    for n in range(6,101):
        for s in range(2,6):
            D = [max(F(t)+F(s*(n-t),2),F(n+s-1)) for t in range(n)]
            assert sum(D) <= F(7*n*n+3*n+14,4)
            gamma = sum((1/d for d in D),F(0))
            assert gamma >= F(4*n*n,7*n*n+3*n+14) >= F(1,2)

    stats['status'] = 'passed; finite exact verification, not a universal proof'
    stats['random_seed'] = 20261010
    stats['random_cases'] = args.random_cases
    root = Path(__file__).resolve().parents[2]
    paths = ['tests/audits/customer_attraction_dynamic_maxima.py',
             'research/current/customer_attraction/dynamic_maxima_bound.md',
             'research/current/customer_attraction/model.md']
    stats['source_sha256'] = {path: hashlib.sha256((root/path).read_bytes()).hexdigest() for path in paths}
    report = json.dumps(stats, indent=2)
    print(report)
    if args.output:
        args.output.write_text(report+'\n')

if __name__ == '__main__':
    main()
