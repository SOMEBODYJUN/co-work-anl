"""Exact finite audit of the three-maximal-coverage half theorem.

Independent literal customer shares and all-continuation menus: no imports
from customer_attraction or the separate coefficient audit. Menus cache
counts but allow independent ordered-history child choices. Selected outcomes
are expanded into complete ordered strategies and checked directly.
Finite success does not prove the theorem outside the tested families.
"""

import argparse
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path
import random
import hashlib


def weight(mask, weights):
    return sum(w for x, w in enumerate(weights) if mask & (1 << x))


def structure(catalog, weights):
    distinct = set(catalog)
    maxima = tuple(sorted(a for a in distinct if not any(
        a != b and a & b == a for b in distinct)))
    assert 1 <= len(maxima) <= 3
    union = 0
    core = maxima[0]
    for maximum in maxima:
        union |= maximum
        core &= maximum
    private = []
    for j, maximum in enumerate(maxima):
        others = 0
        for k, other in enumerate(maxima):
            if k != j:
                others |= other
        private.append(weight(maximum & ~others, weights))
    shared = [weight(maximum, weights) - private[j] - weight(core, weights)
              for j, maximum in enumerate(maxima)]
    if len(maxima) == 1:
        private = [0]
        shared = [0]
    assignment = tuple(next(j for j, b in enumerate(maxima) if a & b == a)
                       for a in catalog)
    return maxima, weight(union, weights), weight(core, weights), tuple(private), tuple(shared), assignment


def seats(catalog, weights, n):
    maxima, union, core, private, shared, assignment = structure(catalog, weights)
    table = tuple(tuple(F(w, k) + F(v, n) for k in range(1, n + 1))
                  for w, v in zip(private, shared))
    nu = sorted((z for row in table for z in row), reverse=True)[n - 1]
    above = tuple(sum(z > nu for z in row) for row in table)
    a = tuple(e + 1 for e in above)
    assert sum(above) <= n - 1 and all(1 <= z <= n for z in a)
    assert all(row[k - 1] <= nu for row, k in zip(table, a))
    s = len(maxima)
    certificate = None
    if n >= 2 and s == 3:
        bound = max(F(sum(a)), F(n + max(a)), F(3 * n, 2))
        upper = bound - n
        y = [F(k) for k in a]
        remainder = bound - sum(y)
        for j in range(3):
            increase = min(remainder, upper - y[j])
            assert increase >= 0
            y[j] += increase
            remainder -= increase
        assert remainder == 0 and sum(y) == bound <= 2 * n
        assert all(y[j] >= a[j] for j in range(3))
        assert all(y[j] + y[k] >= n for j, k in combinations(range(3), 2))
        assert union - core <= sum(y[j] * table[j][a[j] - 1] for j in range(3)) <= bound * nu
        certificate = bound
    if n >= 2 and s == 2:
        assert union - core == sum(private)
        assert union - core <= sum(n * row[k - 1] for row, k in zip(table, a)) <= 2 * n * nu
        certificate = F(2 * n)
    return core, union, private, shared, assignment, table, nu, certificate


class Menu:
    def __init__(self, catalog, weights, n, counters):
        self.catalog = catalog
        self.weights = weights
        self.n = n
        self.m = len(catalog)
        self.counters = counters
        self.core, self.union, self.private, self.shared, self.assignment, self.table, self.nu, self.bound = seats(catalog, weights, n)
        self.levels = sorted({z for row in self.table for z in row if z > 0})
        self.floor = {}

    def add(self, q, a):
        return q[:a] + (q[a] + 1,) + q[a + 1:]

    @lru_cache(None)
    def payoff(self, q, a):
        return sum((F(w, sum(q[b] for b, mask in enumerate(self.catalog)
                             if mask & (1 << x)))
                    for x, w in enumerate(self.weights)
                    if w and self.catalog[a] & (1 << x)), F(0))

    def welfare(self, q):
        union = 0
        for a, k in enumerate(q):
            if k:
                union |= self.catalog[a]
        return weight(union, self.weights)

    @lru_cache(None)
    def solve(self, q):
        self.counters['count_states'] += 1
        if sum(q) == self.n:
            return frozenset((q,))
        replies = [self.solve(self.add(q, a)) for a in range(self.m)]
        floor = max(min(self.payoff(t, a) for t in menu)
                    for a, menu in enumerate(replies))
        self.floor[q] = floor
        retained = frozenset(t for a, menu in enumerate(replies)
                             for t in menu if self.payoff(t, a) >= floor)
        assert retained
        p = tuple(sum(q[a] for a in range(self.m) if self.assignment[a] == j)
                  for j in range(len(self.table)))
        for level in [F(0)] + self.levels:
            capacities = tuple(sum(z >= level for z in row) for row in self.table)
            if sum(max(d - k, 0) for d, k in zip(capacities, p)) >= self.n - sum(q):
                for terminal in retained:
                    for a in range(self.m):
                        if terminal[a] > q[a]:
                            assert self.payoff(terminal, a) >= level + F(self.core, self.n)
                            self.counters['seat_floor_checks'] += 1
        return retained

    def audit(self, materialize=False):
        root = self.solve((0,) * self.m)
        optimum = max(self.welfare(tuple(int(a in chosen) for a in range(self.m)))
                      for k in range(min(self.m, self.n) + 1)
                      for chosen in combinations(range(self.m), k))
        self.counters['root_outcomes'] += len(root)
        for q in root:
            welfare = self.welfare(q)
            assert all(self.payoff(q, a) >= self.nu + F(self.core, self.n)
                       for a, k in enumerate(q) if k)
            assert welfare >= self.core + self.n * self.nu
            if self.n == 1:
                assert welfare == optimum
            else:
                assert optimum <= self.union <= self.core + 2 * (welfare - self.core)
                if self.bound is not None:
                    assert self.union <= self.core + F(self.bound, self.n) * (welfare - self.core)
            if len(self.table) == 1:
                assert welfare == optimum == self.union
        if materialize:
            for q in sorted(root):
                self.certificate(q)

    def certificate(self, desired):
        actions = {}

        def expand(h, q, target):
            if len(h) == self.n:
                assert q == target
                return
            available = [a for a in range(self.m)
                         if target in self.solve(self.add(q, a))
                         and self.payoff(target, a) >= self.floor[q]]
            chosen = available[0]
            actions[h] = chosen
            for a in range(self.m):
                child = self.add(q, a)
                target_child = target if a == chosen else min(
                    self.solve(child), key=lambda t: (self.payoff(t, a), t))
                expand(h + (a,), child, target_child)

        expand((), (0,) * self.m, desired)

        @lru_cache(None)
        def follow(h):
            if len(h) == self.n:
                return h
            return follow(h + (actions[h],))

        def counts(h):
            return tuple(h.count(a) for a in range(self.m))

        expected = {h for k in range(self.n) for h in product(range(self.m), repeat=k)}
        assert set(actions) == expected and counts(follow(())) == desired
        for h in expected:
            terminal = counts(follow(h))
            for a in range(self.m):
                deviation = counts(follow(h + (a,)))
                assert self.payoff(terminal, actions[h]) >= self.payoff(deviation, a)
                self.counters['ordered_deviation_checks'] += 1
        self.counters['complete_strategies'] += 1
        self.counters['ordered_histories'] += len(expected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--random-cases', type=int, default=120)
    args = parser.parse_args()
    counters = {k: 0 for k in ['cases', 'count_states', 'root_outcomes', 'seat_floor_checks',
                             'complete_strategies', 'ordered_histories', 'ordered_deviation_checks',
                             'crossed_incidence_cases', 'core_omission_cases']}

    def run(catalog, weights, n, materialize=False):
        menu = Menu(tuple(catalog), tuple(weights), n, counters)
        maxima = structure(catalog, weights)[0]
        incidences = [frozenset(j for j, b in enumerate(maxima) if b & (1 << x))
                      for x, w in enumerate(weights) if w]
        if any(a & b and a - b and b - a for a, b in combinations(incidences, 2)):
            counters['crossed_incidence_cases'] += 1
        common = maxima[0]
        for b in maxima[1:]:
            common &= b
        if common and any(a & common != common for a in catalog):
            counters['core_omission_cases'] += 1
        menu.audit(materialize)
        counters['cases'] += 1

    # Exhaust every nonempty catalog of <=4 sets on three literal customers.
    for size in range(1, 5):
        for catalog in combinations(range(8), size):
            for n in (1, 2, 3, 5):
                run(catalog, (1, 1, 1), n, materialize=n <= 2)

    targeted = [((3, 5, 10, 1, 0), (4, 4, 3, 3)),
                ((11, 13, 14, 3, 0), (2, 3, 5, 7)),
                ((7, 11, 13, 1, 2), (5, 3, 2, 4)),
                ((0, 0), ()),
                ((3, 3, 5, 1, 0), (3, 2, 1))]
    for catalog, weights in targeted:
        for n in (1, 2, 3, 4, 5, 7):
            run(catalog, weights, n, materialize=n <= 4)

    rng = random.Random(310102026)
    incidence = ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2))
    for i in range(args.random_cases):
        weights = tuple(rng.randrange(0, 15) for _ in incidence)
        maxima = tuple(sum(1 << x for x, included in enumerate(incidence)
                           if weights[x] and j in included) for j in range(3))
        catalog = list(maxima)
        for _ in range(rng.randrange(0, 3)):
            maximum = rng.choice(maxima)
            catalog.append(maximum & rng.randrange(1 << len(weights)))
        run(tuple(catalog), weights, rng.choice((2, 3, 4, 5, 7)), materialize=i < 6)

    proof_path = Path(__file__).resolve().parents[2] / 'research/current/customer_attraction/three_maxima_bound.md'
    if not proof_path.exists():
        proof_path = Path(__file__).with_name('three_maxima_bound.md')
    report = {'status': 'passed', 'arithmetic': 'Fraction', 'seed': 310102026,
              'counts': counters, 'scope': 'finite menus and ordered-strategy checks; universal proof is separate',
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if proof_path.exists():
        report['proof_sha256'] = hashlib.sha256(proof_path.read_bytes()).hexdigest()
    if args.output:
        if args.output.exists():
            raise FileExistsError(f'Refusing to overwrite {args.output}')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as stream:
            stream.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
