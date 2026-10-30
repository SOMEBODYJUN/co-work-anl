"""Independent exact audit of six maximal coverages without private blocks.

No imports from the repository model, solver, or other audits. Rational
coefficient identities are part of the proof; finite game testing is separate.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import lcm
from pathlib import Path
import argparse
import hashlib
import json
import random


ROOT = Path(__file__).resolve().parents[2]
CERT_PATH = ROOT / 'evidence/runs/2026-10-10/customer_attraction_six_maxima_no_private_certificates.json'


def canonical_paths(length):
    def visit(prefix):
        if len(prefix) == length:
            yield prefix
            return
        for label in range(max(prefix, default=-1) + 2):
            yield from visit(prefix + (label,))
    yield from visit(())


def check_coefficients(stats):
    package = json.loads(CERT_PATH.read_text())
    assert package['maximal_indices'] == 6
    assert package['denominator'] == 12
    assert set(package['certificates']) == {'5', '6'}
    types = [I for I in range(1, 63) if I.bit_count() >= 2]
    assert len(types) == 56
    for n in (5, 6):
        rows = package['certificates'][str(n)]
        paths = [tuple(row['path']) for row in rows]
        expected = set(canonical_paths(n - 1))
        assert len(paths) == len(set(paths))
        assert set(paths) == expected
        assert len(paths) == (15 if n == 5 else 52)
        minimum = F(1)
        for entry in rows:
            path, d = tuple(entry['path']), entry['weights']
            assert entry['denominator'] == 12
            assert len(d) == n
            assert all(len(row) == 6 for row in d)
            assert all(type(x) is int and 0 <= x <= 12 for row in d for x in row)
            assert all(sum(row) == 12 for row in d)
            p = [0] * 6
            coefficient = {I: F(0) for I in types}
            for t in range(n):
                for I in types:
                    pI = sum(p[j] for j in range(6) if I >> j & 1)
                    numerator = sum(d[t][j] for j in range(6) if I >> j & 1)
                    coefficient[I] += F(numerator, 12 * (pI + n - t))
                if t < n - 1:
                    p[path[t]] += 1
            assert min(coefficient.values()) >= F(1, 2)
            assert F(entry['minimum']) == min(coefficient.values())
            minimum = min(minimum, min(coefficient.values()))
            stats['coefficient_certificates'] += 1
            stats['exact_type_inequalities'] += len(types)
        assert minimum == F(1, 2)
    assert stats['exact_type_inequalities'] == 3752
    return package


def check_analytic_and_obstruction(stats):
    assert sum((F(1, 15 - 2*t) for t in range(5)), F(0)) == F(22003, 45045)
    assert sum((F(1, 18 - 2*t) for t in range(6)), F(0)) == F(2509, 5040)
    lower_log = F(1) + F(1, 12) + F(1, 80) + F(1, 448)
    assert lower_log == F(7379, 6720) > F(23, 21)
    assert lower_log / 2 - F(1, 21) == F(6739, 13440) > F(1, 2)
    shared9 = sum((F(1, 9+2*r) for r in range(2, 10)), F(0)) + F(10, 9*14)
    assert shared9 == F(229324183, 456326325) > F(1, 2)
    lower9 = lower_log/2 - F(1, 27) - F(16, 9*11*14)
    assert lower9 == F(665881, 1330560) > F(1, 2)
    for n in range(5, 301):
        raw = [F(n+t, 2*(t+1)*(3*n-2*t)) for t in range(n-1)] + [F(1, n+5)]
        assert all(a >= F(1, 2*n) for a in raw)
        last_minimum, private_sum = raw[-1], F(0)
        for a in reversed(raw):
            last_minimum = min(last_minimum, a)
            private_sum += last_minimum
        assert private_sum >= F(1, 2)
        stats['six_maxima_private_envelope_checks'] += 1
    for n in range(7, 301):
        H = sum((F(1, 3*n - 2*t) for t in range(n)), F(0))
        assert H >= lower_log/2 - F(1, 3*n) > F(1, 2)
        stats['analytic_sum_checks'] += 1
        delta = F(2*(n-1), n*(n+2)*(n+5))
        next_delta = F(2*n, (n+1)*(n+3)*(n+6))
        denominator = n*(n+2)*(n+5)*(n+1)*(n+3)*(n+6)
        assert (delta-next_delta)*denominator == 2*(n-2)*(2*n*n+11*n+13)+16 > 0
        if n >= 9:
            shared_sum = sum((F(1, n+2*r) for r in range(2, n+1)), F(0)) + F(n+1, n*(n+5))
            assert shared_sum == H-delta
            assert shared_sum >= lower_log/2-F(1, 3*n)-delta >= lower9 > F(1, 2)
            stats['six_maxima_large_n_shared_checks'] += 1

    # Nine literal customer types from NP19; indices in masks are zero based.
    weights = {4: 27, 16: 1, 32: 1, 9: 9, 10: 9, 17: 21, 24: 4, 34: 21, 40: 4}
    assert sum(weights.values()) == 97
    full = tuple(sum(1 << k for k, I in enumerate(weights) if I >> j & 1) for j in range(6))
    assert all(not (a != b and a & b == a) for a in full for b in full)
    assert len(set(full)) == 6
    optimal_mask = 0
    for j in (0, 1, 2, 4, 5):
        optimal_mask |= full[j]
    assert optimal_mask == (1 << len(weights)) - 1
    p, floors = [0] * 6, []
    for t in range(5):
        r = 5 - t
        seats = []
        for j in range(6):
            shared = sum((F(w, sum(p[k] for k in range(6) if I >> k & 1) + r)
                          for I, w in weights.items() if I.bit_count() >= 2 and I >> j & 1), F(0))
            seats.extend(F(weights.get(1 << j, 0), p[j] + k) + shared for k in range(1, r+1))
        floors.append(sorted(seats, reverse=True)[r-1])
        if t < 4:
            p[t] += 1
    assert floors == [F(6), F(15, 2), F(9), F(10), F(27, 2)]
    assert sum(floors) == 46 < F(97, 2)
    stats['seat_obstruction'] = {'OPT_5': 97, 'floors': [str(x) for x in floors],
                                 'sum': 46, 'scope': 'proof-budget obstruction, not SPE counterexample'}


def mask_weight(mask, weights):
    return sum(w for x, w in enumerate(weights) if mask >> x & 1)


class IndependentMenu:
    def __init__(self, catalog, weights, n, stats):
        active = sum(1 << x for x, w in enumerate(weights) if w)
        self.catalog = tuple(a & active for a in catalog)
        self.weights, self.n, self.stats = tuple(weights), n, stats
        self.m = len(self.catalog)
        distinct = set(self.catalog)
        self.maxima = tuple(sorted(a for a in distinct if not any(a != b and a & b == a for b in distinct)))
        self.s = len(self.maxima)
        assert 1 <= self.s <= 6
        self.route = tuple(next(j for j, b in enumerate(self.maxima) if a & b == a) for a in self.catalog)
        self.core = self.maxima[0]
        self.union = 0
        for b in self.maxima:
            self.core &= b
            self.union |= b
        self.c, self.U = mask_weight(self.core, weights), mask_weight(self.union, weights)
        self.blocks = {}
        self.no_private = True
        for x, w in enumerate(weights):
            if not w:
                continue
            I = sum(1 << j for j, b in enumerate(self.maxima) if b >> x & 1)
            if not I:
                continue
            if self.s >= 2:
                self.no_private = self.no_private and I.bit_count() >= 2
            self.blocks[I] = self.blocks.get(I, 0) + w
        assert self.no_private or n >= 9
        self.P = sum(w for I, w in self.blocks.items() if self.s >= 2 and I.bit_count() == 1)
        self.V = self.U-self.c-self.P
        self.scale = lcm(*range(1, n+1))
        self.options = {}

    def add(self, q, a):
        return q[:a] + (q[a]+1,) + q[a+1:]

    @lru_cache(None)
    def payoff(self, q, a):
        value = 0
        for x, w in enumerate(self.weights):
            if w and self.catalog[a] >> x & 1:
                load = sum(q[b] for b in range(self.m) if self.catalog[b] >> x & 1)
                assert load > 0 and self.scale % load == 0
                value += w * (self.scale // load)
        return value

    def welfare(self, q):
        covered = 0
        for a, count in enumerate(q):
            if count:
                covered |= self.catalog[a]
        return mask_weight(covered, self.weights)

    def routing(self, q):
        return tuple(sum(q[a] for a in range(self.m) if self.route[a] == j) for j in range(self.s))

    def residual_values(self, p, r):
        core_incidence = (1 << self.s) - 1
        return tuple(sum((F(w, sum(p[k] for k in range(self.s) if I >> k & 1) + r)
                          for I, w in self.blocks.items() if I != core_incidence and I >> j & 1), F(0))
                     for j in range(self.s))

    def floor(self, q):
        p = self.routing(q)
        return F(self.c, self.n) + max(self.residual_values(p, self.n - sum(q)))

    def large_n_mixed_floor(self, q):
        t = sum(q)
        shared_coefficient = F(1, 3*self.n-2*t) if t < self.n-1 else F(self.n+1, self.n*(self.n+5))
        return F(self.c, self.n) + F(self.P, 2*self.n) + self.V*shared_coefficient

    @lru_cache(None)
    def solve(self, q):
        self.stats['count_states'] += 1
        if sum(q) == self.n:
            return frozenset((q,))
        r = self.n - sum(q)
        p = self.routing(q)
        old_values = self.residual_values(p, r)
        if r >= 2:
            for a in range(self.m):
                newer = self.residual_values(self.routing(self.add(q, a)), r-1)
                assert all(y >= x for x, y in zip(old_values, newer))
                self.stats['routing_monotonicity_checks'] += 1
        children = tuple(self.solve(self.add(q, a)) for a in range(self.m))
        # Each off-action child can independently select its least profitable
        # equilibrium continuation at that ordered history; all ties are retained.
        threshold = max(min(self.payoff(z, a) for z in children[a]) for a in range(self.m))
        choices = tuple(frozenset(z for z in children[a] if self.payoff(z, a) >= threshold)
                        for a in range(self.m))
        self.options[q] = choices
        for a, menu in enumerate(choices):
            for terminal in menu:
                assert F(self.payoff(terminal, a), self.scale) >= self.floor(q)
                self.stats['history_floor_payoff_checks'] += 1
                if self.n >= 9:
                    assert F(self.payoff(terminal, a), self.scale) >= self.large_n_mixed_floor(q)
                    self.stats['large_n_mixed_payoff_checks'] += 1
        result = frozenset(z for menu in choices for z in menu)
        assert result
        return result

    def audit(self, materialize=False):
        root = self.solve((0,) * self.m)
        optimum = max(self.welfare(tuple(int(a in chosen) for a in range(self.m)))
                      for count in range(min(self.m, self.n)+1)
                      for chosen in combinations(range(self.m), count))
        if self.n >= 5:
            assert optimum == self.U
        for terminal in root:
            W = self.welfare(terminal)
            assert optimum <= 2 * W
            if self.n >= 5:
                assert self.U <= 2 * W - self.c
            if self.n >= 7 and self.no_private:
                H = sum((F(1, 3*self.n - 2*t) for t in range(self.n)), F(0))
                assert W >= self.c + H*(self.U-self.c)
        if materialize:
            for terminal in sorted(root)[:2]:
                self.materialize(terminal)
        self.stats['cases'] += 1
        if not self.no_private:
            self.stats['private_large_n_cases'] += 1
        self.stats['root_outcomes'] += len(root)
        if self.s == 6:
            self.stats['six_maxima_cases'] += 1
        if self.core and any(a & self.core != self.core for a in self.catalog):
            self.stats['core_omission_cases'] += 1
        if 0 in self.catalog:
            self.stats['empty_action_cases'] += 1
        if len(set(self.catalog)) < self.m:
            self.stats['duplicate_label_cases'] += 1

    def materialize(self, target):
        strategy = {}
        def expand(history, q, desired):
            if len(history) == self.n:
                assert q == desired
                return
            picked = next(a for a in range(self.m) if desired in self.options[q][a])
            strategy[history] = picked
            for a in range(self.m):
                child = self.add(q, a)
                destination = desired if a == picked else min(self.solve(child), key=lambda z: (self.payoff(z, a), z))
                expand(history + (a,), child, destination)
        expand((), (0,) * self.m, target)
        @lru_cache(None)
        def follow(history):
            if len(history) == self.n:
                return history
            return follow(history + (strategy[history],))
        histories = {h for t in range(self.n) for h in product(range(self.m), repeat=t)}
        assert set(strategy) == histories
        for h in histories:
            terminal = follow(h)
            q = tuple(terminal.count(a) for a in range(self.m))
            current = strategy[h]
            prefix_q = tuple(h.count(a) for a in range(self.m))
            assert F(self.payoff(q, current), self.scale) >= self.floor(prefix_q)
            for deviation in range(self.m):
                reply = follow(h + (deviation,))
                q_reply = tuple(reply.count(a) for a in range(self.m))
                assert self.payoff(q, current) >= self.payoff(q_reply, deviation)
                self.stats['full_ordered_history_deviations'] += 1
        terminal = follow(())
        floor_sum = F(self.c)
        for t in range(self.n):
            prefix_q = tuple(terminal[:t].count(a) for a in range(self.m))
            floor_sum += max(self.residual_values(self.routing(prefix_q), self.n-t))
        q = tuple(terminal.count(a) for a in range(self.m))
        assert self.welfare(q) >= floor_sum
        if self.n >= 5 and self.no_private:
            assert floor_sum >= F(self.U+self.c, 2)
        self.stats['materialized_strategies'] += 1
        self.stats['materialized_histories'] += len(histories)


def make_maxima(types, weights, s):
    return [sum(1 << x for x, I in enumerate(types) if I >> j & 1 and weights[x]) for j in range(s)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--random-cases', type=int, default=40)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error('refusing to overwrite existing output')
    keys = ['coefficient_certificates', 'exact_type_inequalities', 'analytic_sum_checks',
            'six_maxima_private_envelope_checks', 'six_maxima_large_n_shared_checks', 'cases',
            'count_states', 'routing_monotonicity_checks', 'history_floor_payoff_checks', 'root_outcomes',
            'six_maxima_cases', 'core_omission_cases', 'empty_action_cases', 'duplicate_label_cases',
            'materialized_strategies', 'materialized_histories', 'full_ordered_history_deviations']
    keys.extend(['large_n_mixed_payoff_checks', 'private_large_n_cases'])
    stats = {key: 0 for key in keys}
    check_coefficients(stats)
    check_analytic_and_obstruction(stats)
    def run(catalog, weights, n, materialize=False):
        IndependentMenu(catalog, weights, n, stats).audit(materialize)
    for n in range(1, 9):
        run([0, 0], [0], n, n <= 4)
        run([3, 1, 0, 3], [2, 3], n, n <= 3)

    # All crossed pair incidences among six maxima, including omitted cores.
    pair_types = [sum(1 << j for j in pair) for pair in combinations(range(6), 2)]
    types = pair_types + [63]
    weights = [2 + (k % 3) for k in range(15)] + [7]
    maxima = make_maxima(types, weights, 6)
    for n in (1, 2, 3, 4, 5, 6, 7, 8):
        run(maxima, weights, n, n in (5, 6))
    omitted_core = maxima[0] & ~(1 << 15)
    for n in (3, 5, 6):
        run(maxima + [omitted_core, 0], weights, n, n == 5)
    run(maxima + [maxima[0]], weights, 5, True)

    # Unrestricted six maxima with genuine private mass, n=9 corollary.
    general_types = [1 << j for j in range(6)] + pair_types + [63]
    for index in range(3):
        general_weights = [19 + index + 3*j for j in range(6)] + [2 + (k+index)%5 for k in range(15)] + [7]
        general_maxima = make_maxima(general_types, general_weights, 6)
        run(general_maxima, general_weights, 9)

    # Three crossed maxima, residual pair incidences, duplicate and subset actions.
    types3, weights3 = [3, 5, 6, 7], [2, 3, 5, 4]
    maxima3 = make_maxima(types3, weights3, 3)
    for subset in range(8):
        catalog = maxima3 + [subset, 0, maxima3[0]]
        if not any(subset & b == subset for b in maxima3):
            continue
        for n in (3, 5, 7):
            run(catalog, weights3, n, subset == 0 and n == 3)

    rng = random.Random(202610106)
    for index in range(args.random_cases):
        s = 3 + index % 4
        types = [I for I in range(1, 1 << s) if I.bit_count() >= 2]
        weights = [rng.randrange(1, 5) if I.bit_count() == 2 else rng.randrange(0, 5) for I in types]
        maxima = make_maxima(types, weights, s)
        catalog = list(maxima)
        if index % 3 == 0:
            b = rng.choice(maxima)
            catalog.append(sum(1 << x for x in range(len(types)) if b >> x & 1 and rng.randrange(2)))
        if index % 7 == 0:
            catalog.append(0)
        if index % 11 == 0:
            catalog.append(catalog[-1])
        n = (3, 4, 5, 6, 7)[index % 5]
        run(catalog, weights, n, index < 4 and n <= 4)

    stats['status'] = 'passed; coefficient identities close finite proof branches; SPE tests are finite only'
    stats['random_seed'] = 202610106
    stats['random_cases'] = args.random_cases
    paths = ['research/current/customer_attraction/model.md',
             'research/current/customer_attraction/six_maxima_no_private.md',
             'tests/audits/customer_attraction_six_maxima_no_private.py',
             str(CERT_PATH.relative_to(ROOT))]
    stats['source_sha256'] = {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in paths}
    report = json.dumps(stats, indent=2)
    print(report)
    if args.output:
        args.output.write_text(report + '\n')


if __name__ == '__main__':
    main()
