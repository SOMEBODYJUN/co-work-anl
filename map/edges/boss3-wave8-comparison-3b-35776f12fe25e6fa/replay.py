"""Compare the three frozen full ordered strategies using only the Python standard library."""
import json
import sys
from collections import Counter
from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path

LABELS = tuple(range(7))
PLAYERS = 5
J = (2, 3, 4, 5, 6)
HISTORIES = tuple(h for n in range(PLAYERS) for h in product(LABELS, repeat=n))
SUPPORTS = tuple(frozenset(s) for n in range(PLAYERS + 1) for s in combinations(LABELS, n))
ORDERS = tuple(permutations(range(PLAYERS)))
FROZEN = {
    'old_no_floor': ('R275-credible-search-20261031/original/633b64cbcf0233d0f667__submodular_joint_m5p7_q32.json', 'dbf83fe8561340f29505cb33e37c83cf79e521ab2c1bcb4f5dd959d2b0968d6d'),
    'old_floor': ('R275-credible-search-20261031/original/eb29376c023b5cd9726a__submodular_joint_m5p7_q32_genuine.json', '48dd63e02d6623f34967db6bf8e22a55f303f6fe72b1f06a7847e36e139110a0'),
    'new_floor_up': ('truncated-shapley-positive-root-uniform-payment/positive-tenth-witness.json', 'ea7e0c350f3d617b6522e07652b0b5c22b2acda9940d5176d9bb023d3b7ff7f6'),
}
EXPECTED = {
    'old_no_floor': ((0, 0, 0, 1, 1), F(2), (F(0), F(0)), F(5), F(-1), 2956),
    'old_floor': ((0, 0, 0, 1, 1), F(88, 57), (F(6, 19), F(3, 19)), F(5), F(73, 57), 1213),
    'new_floor_up': ((0, 0, 0, 0, 1), F(9, 8), (F(1, 5), F(1, 10)), F(53, 40), F(-3, 10), 1193),
}


@cache
def value_coordinate(support):
    return sum(1 << a for a in support if a < 2), len(support - {0, 1})


@cache
def permutation_row(action, other_copies):
    chosen = (action,) + other_copies
    row = Counter()
    for order in ORDERS:
        before = frozenset(chosen[i] for i in order[:order.index(0)])
        row[value_coordinate(before | {action})] += 1
        row[value_coordinate(before)] -= 1
    return {coordinate: count for coordinate, count in row.items() if count}


def sh_row(terminal, position):
    action = terminal[position]
    others = tuple(sorted(terminal[:position] + terminal[position + 1:]))
    return permutation_row(action, others)


class Frozen:
    def __init__(self, path, sha):
        raw = path.read_bytes()
        assert sha256(raw).hexdigest() == sha
        report = json.loads(raw)
        if 'exact_candidate' in report:
            candidate = report['exact_candidate']
            decisions = candidate['complete_strategy']['actions']
            values = candidate['values']
        else:
            decisions = report['complete_strategy']
            values = report['moment_values']
        self.actions = {tuple(row['history']): row['action'] for row in decisions}
        assert len(decisions) == len(self.actions) == len(HISTORIES)
        assert set(self.actions) == set(HISTORIES)
        assert set(self.actions.values()) <= set(LABELS)
        keys = tuple(map(tuple, report['moment_orbits']))
        assert set(keys) == {value_coordinate(s) for s in SUPPORTS if s}
        self.moments = {(0, 0): F(0), **dict(zip(keys, map(F, values), strict=True))}
        self.sha = sha

    def c(self, support):
        return self.moments[value_coordinate(frozenset(support))]

    def u(self, terminal, position):
        return sum(self.moments[key] * n for key, n in sh_row(terminal, position).items()) / len(ORDERS)

    @cache
    def terminal(self, h):
        return h if len(h) == PLAYERS else self.terminal(h + (self.actions[h],))


def dif(row, other):
    result = Counter(row)
    result.subtract(other)
    return {str(k): F(v, len(ORDERS)) for k, v in sorted(result.items()) if v}


def checks(strategy, values):
    slacks = Counter()
    failed = []
    for h in HISTORIES:
        chosen = strategy.actions[h]
        own = strategy.terminal(h)
        payoff = values.u(own, len(h))
        for a in LABELS:
            if a == chosen:
                continue
            alternate = strategy.terminal(h + (a,))
            slack = payoff - values.u(alternate, len(h))
            slacks[slack] += 1
            if slack < 0:
                failed.append((slack, h, chosen, a, own, alternate))
    return {
        'comparisons': sum(slacks.values()), 'negative': sum(n for s, n in slacks.items() if s < 0),
        'ties': slacks[0], 'min_strict_slack': min(s for s in slacks if s > 0),
        'lowest_slack': min(slacks), 'earliest_failure': failed[0] if failed else None,
        'worst_failure': min(failed) if failed else None,
    }


def own_summary(frozen, expected):
    actual, opt, root_deletions, query, gap, ties = expected
    assert frozen.terminal(()) == actual
    axioms = Counter()
    for s in SUPPORTS:
        missing = set(LABELS) - s
        if len(s) < PLAYERS:
            for a in missing:
                assert frozen.c(s | {a}) >= frozen.c(s)
                axioms['monotonicity'] += 1
        if len(s) + 2 <= PLAYERS:
            for a, b in combinations(sorted(missing), 2):
                assert frozen.c(s | {a}) + frozen.c(s | {b}) >= frozen.c(s | {a, b}) + frozen.c(s)
                axioms['diminishing_returns'] += 1
    assert axioms == {'monotonicity': 399, 'diminishing_returns': 546}
    w = frozen.c(actual)
    payments = [frozen.u(actual, i) for i in range(PLAYERS)]
    assert sum(payments) == w == 1
    assert [sorted(s) for s in SUPPORTS if frozen.c(s) == max(map(frozen.c, SUPPORTS))] == [list(J)]
    assert opt == frozen.c(J)
    assert root_deletions == tuple(w - frozen.c(set(actual) - {a}) for a in sorted(set(actual)))
    q = [[frozen.u(frozen.terminal(actual[:i] + (a,)), i) for a in LABELS] for i in range(PLAYERS)]
    assert query == sum(row[a] for row in q for a in J)
    assert gap == 4 * w + query - 5 * opt
    assert 5 * opt - 4 * w == query - gap
    bound = {}
    for a in (0, 1):
        x = {a} | (set(J) - {2})
        y = {a} | (set(J) - {3})
        bound[a] = frozen.c(x) + frozen.c(y) - frozen.c(x & y)
    k = max(frozen.c({a}) for a in LABELS)
    assert all(u >= k / PLAYERS for u in payments)
    return {
        'sha256': frozen.sha, 'axioms': axioms, 'actual': actual, 'W': w,
        'root_deletions': root_deletions, 'unique_optimal_support': J, 'OPT': opt,
        'K': k, 'static_floor': k / PLAYERS, 'payoffs': payments,
        'payoff_minus_static_floor': [u - k / PLAYERS for u in payments],
        'query_matrix': q, 'Q_J': query, 'D_J': gap,
        'full_extension_upper_bounds_by_anchor': bound, 'full_extension_lower_bound': opt,
        'archived_IC_ties': ties,
    }


def cross_point_summary(strategy, values):
    actual = strategy.terminal(())
    w = values.c(actual)
    deletions = [w - values.c(set(actual) - {a}) for a in sorted(set(actual))]
    q = [[values.u(strategy.terminal(actual[:i] + (a,)), i) for a in LABELS]
         for i in range(PLAYERS)]
    query = sum(row[a] for row in q for a in J)
    optimum = max(map(values.c, SUPPORTS))
    assert optimum == values.c(J)
    return {'actual': actual, 'W': w, 'root_deletions': deletions,
            'positive_tenth_floor': all(delta >= w / 10 for delta in deletions),
            'OPT': optimum, 'Q_J': query, 'D_J': 4 * w + query - 5 * optimum,
            'query_matrix': q}


def two_original_ics(frozen):
    cases = [((1, 0), 1, 0), ((0, 0, 0, 0), 0, 1)]
    result = []
    for h, chosen, alt in cases:
        assert frozen.actions[h] == chosen
        own = frozen.terminal(h)
        alternate = frozen.terminal(h + (alt,))
        coeffs = dif(sh_row(own, len(h)), sh_row(alternate, len(h)))
        result.append({'history': h, 'actual_action': chosen, 'deviation': alt, 'actual_terminal': own,
                       'deviation_terminal': alternate, 'coefficient': coeffs})
    assert result[0]['coefficient'] == {'(1, 0)': F(-1, 2), '(2, 0)': F(1, 2)}
    assert result[1]['coefficient'] == {'(1, 0)': F(1), '(2, 0)': F(-1, 5), '(3, 0)': F(-4, 5)}
    return result


def cross_check(repo):
    sources = repo / 'archives/customer-attraction/tools/evidence'
    models = {name: Frozen(sources / filename, sha) for name, (filename, sha) in FROZEN.items()}
    old = models['old_no_floor']
    fresh = models['new_floor_up']
    for a in J:
        assert fresh.c({0, a}) == fresh.c({0}) == F(9, 10)
    assert fresh.c(J) > fresh.c({0})
    assert fresh.actions[(0, 0, 1, 2)] == 0 and fresh.actions[(0, 0, 2, 1)] == 1
    assert fresh.actions[(0, 0, 0, 0)] == 1
    assert old.actions[(0, 0, 0, 0)] == 0
    changed = {'/'.join((a, b)): sum(models[a].actions[h] != models[b].actions[h] for h in HISTORIES)
               for a, b in combinations(models, 2)}
    models_results = {name: own_summary(data, EXPECTED[name]) for name, data in models.items()}
    comparisons = {}
    for strategy_name, strategy in models.items():
        comparisons[strategy_name] = {}
        for values_name, values in models.items():
            check = checks(strategy, values)
            assert check['comparisons'] == 16806
            if strategy_name == values_name:
                assert check['negative'] == 0
                assert check['ties'] == EXPECTED[values_name][-1]
            check['point_summary'] = cross_point_summary(strategy, values)
            comparisons[strategy_name][values_name] = check
    return {'histories': len(HISTORIES), 'old_no_floor_true_ICs': two_original_ics(old),
            'policies_pairwise_action_differences': changed,
            'frozen_points': models_results, 'cross_strategy_comparison': comparisons}


if __name__ == '__main__':
    print(json.dumps(cross_check(Path(sys.argv[1])), ensure_ascii=False, indent=2, default=str))
