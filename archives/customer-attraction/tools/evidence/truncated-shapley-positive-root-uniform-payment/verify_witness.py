"""Verify the exact published 1/10-floor UP witness with no solver dependencies."""
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys


def verify(path):
    original = path.read_bytes()
    source = json.loads(original)
    labels = tuple(source['topic_labels'])
    players = source['players']
    assert labels == tuple(range(7)) and players == 5
    actions = {tuple(row['history']): row['action'] for row in source['complete_strategy']}
    histories = {h for size in range(players) for h in product(labels, repeat=size)}
    assert len(actions) == len(source['complete_strategy']) == len(histories)
    assert set(actions) == histories and all(a in labels for a in actions.values())
    supports = tuple(set(s) for size in range(players + 1) for s in combinations(labels, size))
    keys = tuple(map(tuple, source['moment_orbits']))
    assert len(keys) == len(set(keys)) == len(source['moment_values']) == 19
    moments = dict(zip(keys, map(Fraction, source['moment_values'])))

    def coverage(support):
        support = set(support)
        if not support:
            return Fraction(0)
        distinguished = sum(1 << a for a in support & {0, 1})
        return moments[distinguished, len(support - {0, 1})]

    monotonicity, diminishing_returns = 0, 0
    for s in supports:
        absent = set(labels) - s
        if len(s) < players:
            for a in absent:
                assert coverage(s | {a}) >= coverage(s)
                monotonicity += 1
        if len(s) + 2 <= players:
            for a, b in combinations(absent, 2):
                assert coverage(s | {a}) + coverage(s | {b}) >= coverage(s) + coverage(s | {a, b})
                diminishing_returns += 1

    @lru_cache(None)
    def leaf(h):
        return h if len(h) == players else leaf(h + (actions[h],))

    orders = tuple(permutations(range(players)))

    @lru_cache(None)
    def payoff(h, i):
        total = Fraction(0)
        for order in orders:
            previous = {h[j] for j in order[:order.index(i)]}
            total += coverage(previous | {h[i]}) - coverage(previous)
        return total / len(orders)

    comparisons, ties, positive = 0, 0, []
    for h in histories:
        i = len(h)
        own = payoff(leaf(h), i)
        for a in labels:
            if a != actions[h]:
                slack = own - payoff(leaf(h + (a,)), i)
                assert slack >= 0, (h, actions[h], a, slack)
                comparisons += 1
                ties += int(slack == 0)
                if slack:
                    positive.append(slack)

    actual = leaf(())
    assert actual == tuple(source['actual_path']) == (0, 0, 0, 0, 1)
    portfolio = tuple(source['optimal_comparison'])
    assert portfolio == (2, 3, 4, 5, 6)
    w = coverage(actual)
    actual_payoffs = tuple(payoff(actual, i) for i in range(players))
    assert actual_payoffs == tuple(map(Fraction, source['actual_payoffs']))
    assert sum(actual_payoffs) == w == 1
    optimum = max(coverage(s) for s in supports)
    assert optimum == coverage(portfolio) == Fraction(9, 8)
    assert [s for s in supports if coverage(s) == optimum] == [set(portfolio)]
    marginals = tuple(w - coverage(set(actual) - {a}) for a in sorted(set(actual)))
    assert marginals == (Fraction(1, 5), Fraction(1, 10))
    matrix = tuple(tuple(payoff(leaf(actual[:i] + (a,)), i) for a in labels) for i in range(players))
    assert matrix == tuple(tuple(map(Fraction, row)) for row in source['query_matrix'])
    assert all(matrix[i][a] == Fraction(11 if i < 4 else 9, 200)
               for i in range(players) for a in portfolio)
    query = sum(matrix[i][a] for i in range(players) for a in portfolio)
    gap = (players - 1) * w + query - players * optimum
    assert query == Fraction(53, 40) and gap == Fraction(-3, 10)
    assert players * optimum - (players - 1) * w == query - gap
    assert all(coverage({0, a}) == coverage({0}) for a in portfolio)
    outside = set(portfolio)
    left = {0} | (outside - {2})
    right = {0} | (outside - {3})
    bound = coverage(left) + coverage(right) - coverage(left & right)
    assert bound == coverage({0}) == Fraction(9, 10) < optimum
    assert (len(histories), comparisons, ties, monotonicity, diminishing_returns) == (2801, 16806, 1193, 399, 546)
    return {'input_sha256': sha256(original).hexdigest(), 'histories': len(histories),
            'nonself_deviations': comparisons, 'ties': ties, 'minimum_strict_slack': min(positive),
            'truncated_monotonicity_rows': monotonicity, 'truncated_submodularity_rows': diminishing_returns,
            'welfare': w, 'optimum': optimum, 'root_marginals': marginals, 'query_sum': query,
            'UP_margin': gap, 'full_extension_upper_bound': bound}


if __name__ == '__main__':
    witness = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name('positive-tenth-witness.json')
    print(json.dumps(verify(witness), indent=2, default=str))
