"""Rational fixed-table root-floor frontier; no optimizer is required."""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
import json
from math import comb
from pathlib import Path
import sys

WITNESS = Path('archives/customer-attraction/tools/evidence/truncated-shapley-positive-root-uniform-payment/positive-tenth-witness.json')
WITNESS_SHA = 'ea7e0c350f3d617b6522e07652b0b5c22b2acda9940d5176d9bb023d3b7ff7f6'


def verify(path, comparison_duals):
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == WITNESS_SHA
    witness = json.loads(raw)
    labels = tuple(witness['topic_labels'])
    m = witness['players']
    keys = tuple(map(tuple, witness['moment_orbits']))
    actions = {tuple(row['history']): row['action'] for row in witness['complete_strategy']}
    assert len(actions) == 2801 and set(actions) == {h for k in range(m) for h in product(labels, repeat=k)}
    zero = (F(0),) * len(keys)

    def combine(*terms):
        return tuple(sum((a * row[j] for a, row in terms), F(0)) for j in range(len(keys)))

    def dot(row, values):
        return sum(a * b for a, b in zip(row, values))

    def key(labels_in_support):
        support = set(labels_in_support)
        return sum(1 << a for a in support & {0, 1}), len(support - {0, 1})

    def cov(support):
        b, k = key(support)
        return tuple(F((b, k) == idx) for idx in keys)

    @lru_cache(None)
    def leaf(h):
        return h if len(h) == m else leaf(h + (actions[h],))

    @lru_cache(None)
    def payoff(counts, a):
        rest = [b for b, n in enumerate(counts) for _ in range(n - int(a == b))]
        factors = []
        for size in range(m):
            w = F(1, m * comb(m - 1, size))
            for predecessors in combinations(rest, size):
                factors.extend([(w, cov((*predecessors, a))), (-w, cov(predecessors))])
        return combine(*factors)

    def count(h):
        return tuple(h.count(a) for a in labels)

    def query(h, a):
        return payoff(count(leaf(h + (a,))), a)

    path = leaf(())
    J = tuple(witness['optimal_comparison'])
    assert path == (0, 0, 0, 0, 1) and J == (2, 3, 4, 5, 6)
    for i in range(m):
        for a in J:
            expected = (0, 0, 0, 1, a) if i < m - 1 else (0, 0, 0, 0, a)
            assert count(leaf(path[:i] + (a,))) == count(expected)
    assert leaf((1,)) == (1, 0, 0, 0, 1)
    welfare = cov(path)
    portfolio_value = cov(J)
    score = combine((5, portfolio_value), (-4, welfare),
                    *((-1, query(path[:i], a)) for i in range(m) for a in J))
    rows = set()

    for size in range(m):
        for support in combinations(labels, size):
            absent = tuple(a for a in labels if a not in support)
            for a in absent:
                rows.add(combine((1, cov((*support, a))), (-1, cov(support))))
            if size <= m - 2:
                for a, b in combinations(absent, 2):
                    rows.add(combine((1, cov((*support, a))), (1, cov((*support, b))),
                                     (-1, cov((*support, a, b))), (-1, cov(support))))
    for h, own in sorted(actions.items()):
        for a in labels:
            if a != own:
                rows.add(combine((1, query(h, own)), (-1, query(h, a))))

    def floors(d):
        return [combine((1 - d, welfare), (-1, cov((b,)))) for b in (0, 1)]

    def recover(desc, d):
        kind, *args = desc
        if kind == 'floor':
            return floors(d)[args[0]]
        if kind == 'monotone':
            s, a = args
            return combine((1, cov((*s, a))), (-1, cov(s)))
        if kind == 'submodular':
            s, a, b = args
            return combine((1, cov((*s, a))), (1, cov((*s, b))), (-1, cov((*s, a, b))), (-1, cov(s)))
        assert kind == 'real_IC'
        h, a, b = args
        assert actions[tuple(h)] == a and a != b
        return combine((1, query(tuple(h), a)), (-1, query(tuple(h), b)))

    DUALS = {
        "linear1": (1, -7, [
            (('submodular', [2], 3, 4), F('5')),
            (('submodular', [2, 3], 4, 5), F('5')),
            (('submodular', [2, 3, 4], 5, 6), F('5')),
            (('monotone', [2, 3, 4, 5], 0), F('5')),
            (('floor', 0), F('7')),
            (('submodular', [0], 2, 3), F('15')),
            (('real_IC', [0, 0, 2, 1], 1, 0), F('72')),
            (('submodular', [0, 2], 3, 4), F('10')),
            (('submodular', [0, 2, 3], 4, 5), F('5')),
            (('real_IC', [1, 2, 2, 2], 0, 1), F('20/3')),
            (('real_IC', [], 0, 1), F('208/3')),
            (('submodular', [], 2, 3), F('5')),
        ]),
        "linear2": (F(8, 3), -22, [
            (('submodular', [2], 3, 4), F('5/3')),
            (('submodular', [2, 3], 4, 5), F('10/3')),
            (('submodular', [2, 3, 4], 5, 6), F('5')),
            (('monotone', [2, 3, 4, 5], 0), F('20/3')),
            (('floor', 0), F('22')),
            (('submodular', [0], 2, 3), F('20')),
            (('real_IC', [0, 0, 2, 1], 1, 0), F('102')),
            (('submodular', [0, 2], 3, 4), F('40/3')),
            (('submodular', [0, 2, 3], 4, 5), F('20/3')),
            (('real_IC', [1, 2, 2, 2], 0, 1), F('10/9')),
            (('real_IC', [], 0, 1), F('1184/9')),
            (('submodular', [], 1, 2), F('20/3')),
        ]),
    }
    for spec, (const, slope, dual) in DUALS.items():
        assert all(mu >= 0 for _, mu in dual)
        for d in (F(0), F(1)):
            residual = combine((const + d * slope, welfare), (-1, score),
                               *((-mu, recover(desc, d)) for desc, mu in dual))
            assert residual == zero

    def family(d, segment):
        if segment == 'linear1':
            outside = [(1 - d) * j / 4 for j in range(1, 6)]
        else:
            outside = [2 * d, F(1, 3) + d, F(2, 3), 1 - d, F(4, 3) - 2 * d]
        return tuple(outside + [1 - d] * 5 + [1 - 2 * d] + [F(1)] * 8)

    all_comparisons = json.loads(comparison_duals.read_bytes())
    threshold = F(4, 33)
    assert F(all_comparisons['floor']) == threshold
    floor_rows = tuple(sorted(rows | set(floors(threshold))))
    assert len(floor_rows) == all_comparisons['row_count'] == 175

    columns = {a: combine(*((1, query(path[:i], a)) for i in range(m))) for a in labels}
    assert all(columns[a] == columns[J[0]] for a in J)
    groups = {}
    for slots in combinations_with_replacement(labels, m):
        _, k = key(slots)
        groups[(slots.count(0), slots.count(1), k)] = slots
    assert len(groups) == 41
    assert len(all_comparisons['certificates']) == len(groups)
    certified_groups = set()
    max_other_bound = None
    for certificate in all_comparisons['certificates']:
        group = tuple(certificate['group'])
        assert group in groups and group not in certified_groups
        certified_groups.add(group)
        slots = tuple(certificate['slots'])
        assert slots == groups[group]
        value = cov(slots)
        objective = combine((5, value), (-4, welfare), *((-1, columns[a]) for a in slots))
        bound = F(certificate['bound'])
        dual = [(index, F(multiplier)) for index, multiplier in certificate['dual_support']]
        assert all(0 <= i < len(floor_rows) and mu > 0 for i, mu in dual)
        residual = combine((bound, welfare), (-1, objective),
                            *((-mu, floor_rows[i]) for i, mu in dual))
        assert residual == zero
        if slots == J:
            assert bound == 0
        else:
            assert bound < 0
            max_other_bound = bound if max_other_bound is None else max(max_other_bound, bound)
    assert certified_groups == set(groups)

    records = []
    for spec, endpoints in [('linear1', (F(0), F(1, 9))),
                            ('linear2', (F(1, 9), threshold, F(1, 6), F(1, 3)))]:
        const, slope, _ = DUALS[spec]
        for d in endpoints:
            v = family(d, spec)
            assert len(v) == len(keys) and all(x >= 0 for x in v)
            assert all(dot(row, v) >= 0 for row in rows)
            assert all(dot(row, v) >= 0 for row in floors(d))
            assert dot(welfare, v) == 1
            assert dot(score, v) == const + slope * d
            j_value = dot(portfolio_value, v)
            other_maximum = max(x for key_, x in zip(keys, v) if key_ != (0, 5))
            expected_sign = (d < F(1, 6)) - (d > F(1, 6))
            actual_sign = (j_value > other_maximum) - (j_value < other_maximum)
            assert actual_sign == expected_sign
            records.append({'segment': spec, 'delta': d, 'score': dot(score, v), 'J': j_value, 'max_other_support': other_maximum,
                            'min_slack_all_rows': min(dot(row, v) for row in rows), 'values': v})
    print(json.dumps({'witness_sha256': WITNESS_SHA, 'distinct_non_floor_rows': len(rows),
                      'dual_nonnegative_rows': [len(dual) for _, _, dual in DUALS.values()],
                      'checked_dual_coordinates_at_each_affine_endpoint': len(keys),
                      'all_comparison_classes_at_threshold': len(certified_groups),
                      'largest_bound_other_than_J_at_threshold': max_other_bound,
                      'ordered_histories': len(actions),
                      'ordered_nonself_deviations': 6 * len(actions), 'records': records}, default=str, indent=2))


if __name__ == '__main__':
    verify(Path(sys.argv[1]) if len(sys.argv) > 1 else WITNESS,
           Path(__file__).with_name('all-comparison-duals.json'))
