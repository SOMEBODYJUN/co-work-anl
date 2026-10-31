"""Joint credible completion in a BROADER common-submodular Shapley class.

The outcome-witness DAG retains full ordered-history pure SPE possibilities.
Only its input variables are changed from nonnegative customer masses to
common monotone-submodular truncated moments. A counterexample here would
not by itself refute customer-attraction half coverage.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from math import comb
from math import ceil
from pathlib import Path
import sys
import types

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from submodular_path import Moments, dot, serializable, solve

source = HERE.parent / 'symmetric_dag.py'
raw = source.read_text()
replacements = {
    'lo, hi = np.zeros(idx), np.ones(idx)':
        'lo, hi = np.zeros(idx), np.ones(idx)\n        hi[:len(self.rkeys)] = self.m',
    'for k in t:\n            actions_per_pair':
        'self.add_moment_rows(add)\n        for k in t:\n            actions_per_pair',
    "clones = [0] * ((1 << p) - 1)\n            clones[(1 << self.d) - 2] = m\n            for a in range(self.d, p):\n                clones[(1 << a) - 1] = 1":
        'clones = self.seed_clones()',
    'seed[j] = clones[self.orbits[key][0] - 1] / scale':
        'seed[j] = sum(n for mask, n in enumerate(clones, 1) if mask & self.orbits[key][0]) / scale',
    'floats = [result.x[self.mask_to_r[mask]] for mask in range(1, 1 << p)]':
        'floats = [result.x[j] for j in range(len(self.rkeys))]',
}
for old, new in replacements.items():
    assert old in raw, old
    raw = raw.replace(old, new)
old = types.ModuleType('submodular_witness_base')
old.__file__ = str(source)
exec(compile(raw, str(source), 'exec'), old.__dict__)


class SubmodularDAG(old.SymmetricDAG):
    def __init__(self, p, d, m, path, root_marginal_floor=None):
        super().__init__(p, d, m)
        self.moments = Moments(p, d, m)
        self.path = path
        self.root_marginal_floor = root_marginal_floor
        self.rkeys = self.moments.keys
        self.orbits = {key: [mask for mask in range(1, 1 << p)
                            if mask.bit_count() <= m and self.moments.key(mask) == key]
                       for key in self.rkeys}
        self.mask_to_r = {mask: j for j, key in enumerate(self.rkeys)
                          for mask in self.orbits[key]}
        extra_rows = set(self.moments.rows + self.moments.path_rows(path))
        if root_marginal_floor is not None:
            eps = F(str(root_marginal_floor))
            inside = (1 << d) - 1
            for a in range(d):
                extra_rows.add(self.moments.combine((1 - eps, self.moments.C(inside)),
                    (-1, self.moments.C(inside ^ (1 << a)))))
        self.extra_rows = tuple(sorted(extra_rows))

    @lru_cache(None)
    def reduce(self, full_customer_row):
        # Boolean superset Mobius transform, independently checked below against
        # the positive Shapley-marginal formula on every terminal payoff row.
        values = [F(0)] + list(full_customer_row)
        for bit in range(self.p):
            for mask in range(1 << self.p):
                if not mask & (1 << bit):
                    values[mask] -= values[mask | (1 << bit)]
        full = (1 << self.p) - 1
        row = [F(0)] * len(self.rkeys)
        for S in range(1, 1 << self.p):
            coefficient = -values[full ^ S]
            if S.bit_count() > self.m:
                assert coefficient == 0
            else:
                row[self.mask_to_r[S]] += coefficient
        return tuple(row)

    def add_moment_rows(self, add):
        for row in self.extra_rows:
            add({j: a for j, a in enumerate(row) if a}, lower=0)

    def seed_clones(self):
        # Full input symmetry and a valid 9/5 all-big SPE when m=s=5.
        # Every outside theme gets one disjoint piece of the common big cover
        # and its own private clients; actual distinguished themes are aliases.
        clones = [0] * ((1 << self.p) - 1)
        inside = (1 << self.d) - 1
        s = self.p - self.d
        for b in range(self.d, self.p):
            clones[(inside | (1 << b)) - 1] = self.m
            clones[(1 << b) - 1] = s - 1
        if self.root_marginal_floor is not None:
            eps = F(str(self.root_marginal_floor))
            assert self.d * eps < 1
            exclusive = ceil(eps * s * self.m / (1 - self.d * eps))
            for a in range(self.d):
                clones[(1 << a) - 1] += exclusive
        return clones

    def coefficient_check(self):
        checked = 0
        for c in self.leaves:
            for a, n in enumerate(c):
                if n:
                    assert self.reduce(old.payoff_row(self.p, c, a)) == self.moments.payoff(c, a)
                    checked += 1
        return checked


def independent_uniform_order_audit(dag, values, certificate):
    """No generating payoff row: sum over subsets of the other providers."""
    p, m = dag.p, dag.m
    actions = dict(certificate.actions)
    expected = {h for depth in range(m) for h in product(range(p), repeat=depth)}
    assert set(actions) == expected

    def C(mask):
        return F(0) if not mask else values[dag.moments.index[dag.moments.key(mask)]]

    @lru_cache(None)
    def utility(q, a):
        others = [b for b, n in enumerate(q) for _ in range(n - int(b == a))]
        assert len(others) == m - 1
        answer = F(0)
        for subset in range(1 << (m - 1)):
            support = 0
            for j, b in enumerate(others):
                if subset & (1 << j):
                    support |= 1 << b
            contribution = C(support | (1 << a)) - C(support)
            answer += contribution / (m * comb(m - 1, subset.bit_count()))
        assert answer == dot(dag.moments.payoff(q, a), values)
        return answer

    terminal = {}
    checked = ties = 0
    for depth in range(m, -1, -1):
        for h in product(range(p), repeat=depth):
            if depth == m:
                terminal[h] = tuple(h.count(a) for a in range(p))
                continue
            chosen = actions[h]
            q = terminal[h + (chosen,)]
            terminal[h] = q
            own = utility(q, chosen)
            for b in range(p):
                if b == chosen:
                    continue
                alt = utility(terminal[h + (b,)], b)
                assert own >= alt, (h, chosen, b, own, alt)
                checked += 1
                ties += int(own == alt)
    q = terminal[()]
    assert q == certificate.terminal_counts
    support = sum(1 << a for a, n in enumerate(q) if n)
    W = C(support)
    assert sum(n * utility(q, a) for a, n in enumerate(q) if n) == W
    optimum = max(C(S) for S in range(1 << p) if S.bit_count() <= m)
    assert all(dot(row, values) >= 0 for row in dag.moments.rows)
    return {'definition_verified': True, 'histories': len(expected),
            'nonself_deviations': checked, 'ties': ties, 'W': W,
            'OPT': optimum, 'OPT_over_W': optimum / W,
            'payoff_method': 'uniform-permutation predecessor subsets of individual provider copies'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topics', type=int, default=7)
    ap.add_argument('--path', default='0,0,0,1,1')
    ap.add_argument('--portfolio', default='2,3,4,5,6')
    ap.add_argument('--seconds', type=float, default=45)
    ap.add_argument('--floor', type=float)
    ap.add_argument('--root-marginal-floor', type=float)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    path = tuple(map(int, args.path.split(',')))
    p, m, d = args.topics, len(path), max(path) + 1
    J = tuple(map(int, args.portfolio.split(',')))
    q = tuple(path.count(a) for a in range(p))
    dag = SubmodularDAG(p, d, m, path, args.root_marginal_floor)
    checked = dag.coefficient_check()
    found, meta = dag.build(q, J, args.seconds, path=path, floor=args.floor, warm_start=True)
    point = None
    if found:
        certificate, _ = found
        cone = old.StrategyCone(p, m, dict(certificate.actions))
        rows = tuple(sorted(set(dag.extra_rows + tuple(dag.reduce(row) for row in cone.rows))))
        w = dag.moments.C(sum(1 << a for a, n in enumerate(q) if n))
        objective = dag.moments.C(sum(1 << a for a in J))
        point = solve(rows, w, objective)
        if point.get('certified'):
            point['complete_strategy'] = certificate.to_dict()
            point['independent_uniform_order_audit'] = independent_uniform_order_audit(dag, point['values'], certificate)
    report = {'scope': 'BROADER common monotone-submodular Shapley input class; full ordered-history pure SPE; not a customer-attraction counterexample',
              'customer_attraction_half_status': 'OPEN', 'coefficient_rows_checked': checked,
              'root_marginal_floor': args.root_marginal_floor,
              'moment_orbits': dag.rkeys, 'milp': meta, 'exact_candidate': point}
    args.output.write_text(json.dumps(serializable(report), indent=2) + '\n')
    summary = dict(report)
    summary.pop('moment_orbits')
    if point:
        summary['exact_candidate'] = {k: v for k, v in point.items()
            if k not in ('values', 'dual_support', 'complete_strategy')}
    print(json.dumps(serializable(summary), indent=2))


if __name__ == '__main__':
    main()
