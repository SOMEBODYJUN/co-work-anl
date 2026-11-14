"""Exact audit of the frozen five-person, seven-label ordered Shapley policies."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
import json
from math import factorial
from pathlib import Path
import sys


LABELS = tuple(range(7))
PLAYERS = 5
OUTSIDE = (2, 3, 4, 5, 6)
EVIDENCE = Path('archives/customer-attraction/tools/evidence')
R275 = EVIDENCE / 'R275-credible-search-20261031/original'
CURRENT = EVIDENCE / 'truncated-shapley-positive-root-uniform-payment/positive-tenth-witness.json'
SOURCES = {
    'new': CURRENT,
    'old_floor': R275 / 'eb29376c023b5cd9726a__submodular_joint_m5p7_q32_genuine.json',
    'old_no_floor': R275 / '633b64cbcf0233d0f667__submodular_joint_m5p7_q32.json',
}
TRUNCATED_SUPPORTS = tuple(frozenset(s) for k in range(PLAYERS + 1) for s in combinations(LABELS, k))
SLOT_MULTISET = tuple(combinations_with_replacement(LABELS, PLAYERS))
HISTORIES = tuple(h for depth in range(PLAYERS) for h in product(LABELS, repeat=depth))


def audit(path):
    raw = path.read_bytes()
    source = json.loads(raw)
    old = source.get('exact_candidate')
    if old:
        data = old['complete_strategy']['actions']
        values = old['values']
    else:
        data = source['complete_strategy']
        values = source['moment_values']
    coordinates = tuple(map(tuple, source['moment_orbits']))
    moments = dict(zip(coordinates, map(Fraction, values), strict=True))
    expected_coordinates = {(b, k) for b in range(4) for k in range(6 - b.bit_count())}
    assert set(moments) | {(0, 0)} == expected_coordinates
    assert len(coordinates) == len(moments) == 19
    moments[0, 0] = Fraction(0)

    @lru_cache(None)
    def c(labels):
        return moments[sum(1 << a for a in labels if a < 2), sum(a > 1 for a in labels)]

    actions = {tuple(row['history']): row['action'] for row in data}
    assert len(actions) == len(data) == len(HISTORIES) and set(actions) == set(HISTORIES)
    assert set(actions.values()) <= set(LABELS)

    @lru_cache(None)
    def follow(history):
        if len(history) == PLAYERS:
            return history
        return follow(history + (actions[history],))

    @lru_cache(None)
    def payoff(others, label):
        result = Fraction(0)
        for size in range(PLAYERS):
            weight = factorial(size) * factorial(PLAYERS - 1 - size)
            for predecessors in combinations(others, size):
                support = frozenset(predecessors)
                result += weight * (c(support | {label}) - c(support))
        return result / factorial(PLAYERS)

    def utility(leaf, index):
        others = tuple(sorted(leaf[:index] + leaf[index + 1:]))
        return payoff(others, leaf[index])

    monotonicity = dr = 0
    for s in TRUNCATED_SUPPORTS:
        absent = set(LABELS) - s
        if len(s) < PLAYERS:
            for a in absent:
                assert c(s | {a}) >= c(s), (s, a)
                monotonicity += 1
        if len(s) < PLAYERS - 1:
            for a, b in combinations(absent, 2):
                assert c(s | {a}) + c(s | {b}) >= c(s) + c(s | {a, b}), (s, a, b)
                dr += 1

    for multiset in SLOT_MULTISET:
        assert sum(utility(multiset, i) for i in range(PLAYERS)) == c(frozenset(multiset))

    ic_slacks = Counter()
    for h in HISTORIES:
        i = len(h)
        v = utility(follow(h), i)
        for a in LABELS:
            if a != actions[h]:
                slack = v - utility(follow(h + (a,)), i)
                assert slack >= 0, (h, a, slack)
                ic_slacks[slack] += 1

    actual = follow(())
    support = frozenset(actual)
    welfare = c(support)
    optimum = max(c(s) for s in TRUNCATED_SUPPORTS)
    optimal_multisets = tuple(s for s in SLOT_MULTISET if c(frozenset(s)) == optimum)
    assert optimal_multisets == (OUTSIDE,)
    payoffs = tuple(utility(actual, i) for i in range(PLAYERS))
    assert sum(payoffs) == welfare
    root = tuple(welfare - c(support - {a}) for a in sorted(support))
    query_leaves = tuple(tuple(follow(actual[:i] + (a,)) for a in LABELS) for i in range(PLAYERS))
    matrix = tuple(tuple(utility(z, i) for z in row) for i, row in enumerate(query_leaves))
    columns = tuple(sum(row[a] for row in matrix) for a in LABELS)
    query_sum = sum(columns[a] for a in OUTSIDE)

    def up_margin(slot_multiset):
        return (PLAYERS - 1) * welfare + sum(columns[a] for a in slot_multiset) - PLAYERS * c(frozenset(slot_multiset))

    gap = up_margin(OUTSIDE)
    lower_bound = PLAYERS * optimum - (PLAYERS - 1) * welfare
    assert gap + lower_bound == query_sum
    all_up = {slots: up_margin(slots) for slots in SLOT_MULTISET}
    outer = frozenset(OUTSIDE)
    left, right = outer - {2} | {0}, outer - {3} | {0}
    bound = c(left) + c(right) - c(left & right)
    triple = frozenset({1, 2, 3})
    triple_values = [c(frozenset(s)) for size in (1, 2, 3) for s in combinations(sorted(triple), size)]
    boolean_moment = sum(triple_values[:3]) - sum(triple_values[3:6]) + triple_values[6]
    def intersection(a, b):
        return c(frozenset({a})) + c(frozenset({b})) - c(frozenset({a, b}))

    for z0, z1, z2, z3 in product((0, 1), repeat=4):
        k = z1 + z2 + z3
        assert z0 * (1 - k) + k * (k - 1) // 2 >= 0
    boolean_pairs = c(frozenset({0})) - sum(intersection(0, a) for a in (1, 2, 3))
    boolean_pairs += sum(intersection(a, b) for a, b in combinations((1, 2, 3), 2))
    assert bound < optimum
    key_histories = ((0, 0, 1, 2), (0, 0, 2, 1))
    result = {
        'source_sha256': sha256(raw).hexdigest(),
        'histories': len(actions),
        'deviations': sum(ic_slacks.values()),
        'ic_ties': ic_slacks[Fraction(0)],
        'minimum_strict_ic_slack': min(s for s in ic_slacks if s > 0),
        'monotonicity_checks': monotonicity,
        'adjacent_diminishing_marginal_checks': dr,
        'actual': actual,
        'welfare': welfare,
        'actual_payoffs': payoffs,
        'root_marginals': root,
        'unique_optimal_comparison_multiset': optimal_multisets[0],
        'optimum': optimum,
        'count_equal_ordered_prefix_actions': [actions[h] for h in key_histories],
        'ordered_query_leaves': query_leaves,
        'query_matrix': matrix,
        'comparison_query_sum': query_sum,
        'comparison_up_margin': gap,
        'minimum_comparison_up_margin': min(all_up.values()),
        'negative_comparison_multisets': [slots for slots, d in all_up.items() if d < 0],
        'weak_uniform_payment_margin': welfare + query_sum / PLAYERS - optimum,
        'full_extension_lower': optimum,
        'full_extension_upper': bound,
        'boolean_triple_values': triple_values,
        'boolean_triple_123_moment': boolean_moment,
        'boolean_quadratic_0123_moment': boolean_pairs,
    }
    if old:
        assert tuple(source['milp']['path']) == actual
        assert Fraction(old['value']) == Fraction(old['dual_bound']) == optimum
        declared = old['independent_uniform_order_audit']
        assert result['histories'] == declared['histories']
        assert result['deviations'] == declared['nonself_deviations']
        assert result['ic_ties'] == declared['ties']
        assert result['welfare'] == Fraction(declared['W'])
        assert result['optimum'] == Fraction(declared['OPT'])
        if not source.get('root_marginal_floor'):
            pair = {(1, 0): (1, 0), (0, 0, 0, 0): (0, 1)}
            assert [actions[h] for h in pair] == [moves[0] for moves in pair.values()]
            leaves = [follow(h + (a,)) for h, moves in pair.items() for a in moves]
            assert tuple(map(lambda z: tuple(sorted(z)), leaves)) == (
                (0, 0, 0, 1, 1), (0, 0, 1, 1, 1), (0, 0, 0, 0, 0), (0, 0, 0, 0, 1))
            result['root_floor_obstructing_ic_leaves'] = leaves
    else:
        assert actual == tuple(source['actual_path']) == (0, 0, 0, 0, 1)
        assert payoffs == tuple(map(Fraction, source['actual_payoffs']))
        assert matrix == tuple(tuple(map(Fraction, row)) for row in source['query_matrix'])
        assert root == tuple(map(Fraction, source['root_marginals'])) == (Fraction(1, 5), Fraction(1, 10))
        assert (welfare, optimum, query_sum, gap) == (1, Fraction(9, 8), Fraction(53, 40), Fraction(-3, 10))
        assert gap == min(all_up.values()) and result['negative_comparison_multisets'] == [OUTSIDE]
        assert (len(actions), sum(ic_slacks.values()), ic_slacks[Fraction(0)], monotonicity, dr) == (2801, 16806, 1193, 399, 546)
        assert result['count_equal_ordered_prefix_actions'] == [0, 1]
        assert boolean_moment == boolean_pairs == Fraction(-1, 5)
        assert bound == c(frozenset({0})) == Fraction(9, 10)
        assert all(c(frozenset({0, a})) == c(frozenset({0})) for a in OUTSIDE)
        assert all(len({row[a] for a in OUTSIDE}) == 1 for row in matrix)
    return result


if __name__ == '__main__':
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    results = {kind: audit(root / path) for kind, path in SOURCES.items()}
    print(json.dumps(results, default=str, indent=2))
