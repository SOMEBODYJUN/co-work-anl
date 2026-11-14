from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import sys

source = Path(sys.argv[1])
raw = source.read_bytes()
report = json.loads(raw)
candidate = report['exact_candidate']
policy = {tuple(record['history']): record['action'] for record in candidate['strategy']['actions']}
players, topics = report['milp']['players'], report['milp']['topics']
labels = tuple(range(topics))
masks = tuple(range(1, 1 << topics))
clone = tuple(candidate['integer_clones'])
assert (players, topics) == (5, 7)
assert len(policy) == len(candidate['strategy']['actions']) == 2801
assert set(policy) == {h for depth in range(players) for h in product(labels, repeat=depth)}
assert all(type(a) is int and a in labels for a in policy.values())
assert len(clone) == len(masks) and all(type(w) is int and w >= 0 for w in clone)
assert {sum(1 << a for a in entry['topics']): entry['multiplicity']
        for entry in candidate['instance']['customers']} == {m: w for m, w in zip(masks, clone) if w}


@lru_cache(None)
def finish(history):
    while len(history) < players:
        history += (policy[history],)
    return history


@lru_cache(None)
def payoff_row(action, counts):
    return tuple(Fraction(1, sum(c for j, c in enumerate(counts) if m & (1 << j)))
                 if m & (1 << action) else Fraction(0) for m in masks)


def counts(history):
    return tuple(history.count(a) for a in labels)


def cover_row(support):
    support_mask = sum(1 << j for j in set(support))
    return tuple(int(bool(m & support_mask)) for m in masks)


def dot(row, mass):
    return sum(x * y for x, y in zip(row, mass, strict=True))


def diff(first, second):
    return tuple(x - y for x, y in zip(first, second, strict=True))


def ic_row(history, action):
    actual = payoff_row(policy[history], counts(finish(history)))
    deviation = payoff_row(action, counts(finish(history + (action,))))
    return diff(actual, deviation)


rows_and_witnesses = {}
minimum_slack = None
checks = 0
for history in sorted(policy, key=lambda h: (len(h), h)):
    for action in labels:
        if action == policy[history]:
            continue
        row = ic_row(history, action)
        slack = dot(row, clone)
        assert slack >= 0, (history, action, slack)
        minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
        checks += 1
        if any(row):
            rows_and_witnesses.setdefault(row, (history, action))
assert checks == candidate['deviation_checks'] == 16806
rows = sorted(rows_and_witnesses)
actual_leaf = finish(())
actual_cover = cover_row(actual_leaf)
comparison_support = tuple(report['milp']['portfolio'])
comparison = cover_row(comparison_support)
W = dot(actual_cover, clone)
assert list(counts(actual_leaf)) == candidate['strategy']['terminal_counts']
assert W == candidate['welfare'] == 20
support_values = {support: dot(cover_row(support), clone) for support in combinations(labels, players)}
assert max(support_values.values()) == candidate['optimal_welfare'] == 33
assert dot(comparison, clone) == sum(clone) == 33

beta = Fraction(candidate['exact_dual_bound'])
weights = tuple((index, Fraction(value)) for index, value in candidate['dual_support'])
assert len(weights) == 13 and len(set(index for index, _ in weights)) == len(weights)
assert all(0 <= index < len(rows) and weight > 0 for index, weight in weights)
assert all(dot(rows[index], clone) == 0 for index, _ in weights)
residual = tuple(beta * cover - objective - sum(weight * rows[index][j] for index, weight in weights)
                 for j, (cover, objective) in enumerate(zip(actual_cover, comparison, strict=True)))
assert min(residual) == 0 and dot(residual, clone) == 0
assert beta == Fraction(dot(comparison, clone), W) == Fraction(33, 20)

x = tuple(int(m & 3 == 1) for m in masks)
y = tuple(int(m & 3 == 2) for m in masks)
z = tuple(int(m & 3 == 3) for m in masks)
root_ic = ic_row((), 1)
assert actual_leaf == (0, 0, 0, 1, 1) and finish((1,)) == (1, 0, 0, 0, 0)
assert root_ic == tuple(Fraction(a, 3) - b for a, b in zip(x, y, strict=True))
last_prefix = actual_leaf[:-1]
last_ic = ic_row(last_prefix, 0)
assert finish(last_prefix + (0,)) == (0, 0, 0, 1, 0)
assert last_ic == tuple(Fraction(b, 2) - Fraction(a, 4) for a, b in zip(x, y, strict=True))
assert tuple(-12*a - 24*b for a,b in zip(root_ic,last_ic,strict=True)) == tuple(2*a for a in x)
assert tuple(-6*a - 8*b for a,b in zip(root_ic,last_ic,strict=True)) == tuple(2*a for a in y)
assert all(payoff_row(a, counts(actual_leaf))[j] == Fraction(1, 5)
           for j, indicator in enumerate(z) if indicator for a in (0, 1))
assert all(payoff_row(0, counts(rivals + (0,)))[j] >= Fraction(1, 5)
           for rivals in product(labels, repeat=4) for j, indicator in enumerate(z) if indicator)
assert all(diff(payoff_row(1, counts(actual_leaf)), payoff_row(a, counts(last_prefix + (a,))))
           == ic_row(last_prefix, a) for a in labels)
assert all(dot(payoff_row(a, counts(last_prefix + (a,))), clone) == 4 for a in labels)
assert all(dot(payoff_row(a, counts(actual_leaf)), clone) == 4 for a in actual_leaf)

# At an actual prefix, filling the unused rival slots with 0 gives the same
# load as the common Q on every type consistent with the forced aliases.
for position in range(players):
    background = actual_leaf[:position] + (0,) * (players - position - 1)
    for action in labels:
        prefix_cap = payoff_row(action, counts(background + (action,)))
        common_cap = payoff_row(action, counts(last_prefix + (action,)))
        assert all(left == right for m, left, right in zip(masks, prefix_cap, common_cap, strict=True)
                   if m & 3 in (0, 3))


# Check the two nonnegative Farkas combinations that imply the alias constraints.
assert tuple(6*a + 12*b for a, b in zip(root_ic, last_ic, strict=True)) == tuple(-a for a in x)
assert tuple(3*a + 4*b for a, b in zip(root_ic, last_ic, strict=True)) == tuple(-b for b in y)

# Same pure Q pays all queries against each player's row and the average row.
last_payoff = payoff_row(1, counts(actual_leaf))
for query in labels:
    query_payoff = payoff_row(query, counts(last_prefix + (query,)))
    query_ic = ic_row(last_prefix, query)
    assert diff(last_payoff, query_payoff) == query_ic
    assert diff(payoff_row(0, counts(actual_leaf)), query_payoff) == tuple(
        delta + Fraction(3, 2)*a + 2*b + Fraction(c, 3)
        for delta, a, b, c in zip(query_ic, root_ic, last_ic, x, strict=True))
    assert diff(tuple(Fraction(c, 5) for c in actual_cover), query_payoff) == tuple(
        delta + Fraction(9, 10)*a + Fraction(6, 5)*b + Fraction(c, 5)
        for delta, a, b, c in zip(query_ic, root_ic, last_ic, x, strict=True))

# For the fixed-query real-menu budget, force 0 at each actual position.
query_zero_rivals = []
for position in range(players):
    forced_leaf = finish(actual_leaf[:position] + (0,))
    rivals = forced_leaf[:position] + forced_leaf[position + 1:]
    assert set(rivals) <= {0, 1}
    assert diff(payoff_row(0, counts(rivals + (0,))), tuple(Fraction(c, 5) for c in actual_cover)) == tuple(
        Fraction(int(m & 3 == 1), 1 + rivals.count(0)) - Fraction(int(m & 3 in (1, 2)), 5)
        for m in masks)
    query_zero_rivals.append(rivals)

signatures = {frozenset(m for m, w in zip(masks, clone, strict=True) if w and m & (1 << a)) for a in labels}
maxima = {s for s in signatures if not any(s < other for other in signatures)}
assert len(signatures) == len(maxima) == 6

print(json.dumps({
    'source_sha256': hashlib.sha256(raw).hexdigest(),
    'histories': len(policy), 'deviation_checks': checks, 'minimum_IC_slack': str(minimum_slack),
    'nonzero_distinct_IC_rows': len(rows), 'actual_leaf': actual_leaf,
    'root_deviation_1': finish((1,)), 'last_prefix': last_prefix,
    'last_deviation_0': finish(last_prefix + (0,)), 'all_static_backgrounds': topics ** 4,
    'weight': sum(clone), 'W': W, 'OPT5': max(support_values.values()), 'v5': '4',
    'maxima_count_at_frozen_point': len(maxima), 'common_Q_background': last_prefix,
    'common_Q_coordinate_identities': 3 * topics * len(masks),
    'actual_prefix_security_values_at_frozen_point': ['4'] * players,
    'actual_prefix_security_debts_at_frozen_point': ['0'] * players,
    'force_zero_backgrounds_on_real_path': query_zero_rivals,
    'supports_of_size_five': [{'support': key, 'coverage': value} for key, value in support_values.items()],
    'comparison_support': comparison_support, 'bound': str(beta),
    'dual_weights': [{'index': index, 'weight': str(weight), 'history': rows_and_witnesses[rows[index]][0],
                      'deviation': rows_and_witnesses[rows[index]][1]} for index, weight in weights],
    'dual_minimum_residual': str(min(residual)), 'dual_maximum_residual': str(max(residual)),
    'dual_zero_coordinates': sum(value == 0 for value in residual), 'dual_positive_coordinates': sum(value > 0 for value in residual),
}, ensure_ascii=False, indent=2))
