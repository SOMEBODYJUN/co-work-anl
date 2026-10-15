#!/usr/bin/env python3
"""Finite exact attacks on the independently reconstructed rigidity claim."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
from math import comb
import hashlib
import json

REVIEWED_FREEZE = '7a2ee0b7ed466d426b3ee6d9142c30be95392cb454bbfb860d7045a21cff1299'


def direct_cost(sig, degree, weights, state, player):
    if not ((sig[player] >> state[player]) & 1):
        return F(0)
    return sum(w for j, w in enumerate(weights) if (sig[j] >> state[j]) & 1) ** degree


def audit_pair_signs():
    values = tuple(map(F, ('1/3', '2/3', '1', '3/2', '7/3')))
    checks = positive = negative = zero = 0
    for a, b in product(values, repeat=2):
        for k in range(9):
            lhs = a * ((a + b) ** k - a ** k) - b * ((a + b) ** k - b ** k)
            rhs = (a - b) * ((a + b) ** k - sum(a ** (k-r) * b ** r for r in range(k+1)))
            assert lhs == rhs
            if k <= 1 or a == b:
                assert lhs == 0
                zero += 1
            elif a > b:
                assert lhs > 0
                positive += 1
            else:
                assert lhs < 0
                negative += 1
            checks += 1
    return dict(weights=list(map(str, values)), degree_range=[0, 8], checks=checks,
                positive=positive, negative=negative, zero=zero)


def audit_signature_faces(weights, max_degree=6):
    """Every finite test column is evaluated from genuine state loads.

    Successive linear zero faces remove all columns except full action-1 x.
    The sign audit on each *current* face is essential: no claim is made that
    the later functionals are nonnegative before the earlier face reductions.
    """
    n = len(weights)
    a, b, p, q = next((weights[p], weights[q], p, q)
                     for p in range(n) for q in range(n) if weights[p] > weights[q])
    ss = tuple(product((0, 1), repeat=n))
    zero = (0,) * n
    solo = tuple(tuple(int(j == i) for j in range(n)) for i in range(n))

    def pair(i, j):
        return tuple(int(k == i or k == j) for k in range(n))

    def functionals(table):
        def delta(i, j):
            return table[i, pair(i, j)] - table[i, solo[i]]
        slope = delta(p, q) / b
        return (
            sum(table[i, zero] for i in range(n)),
            a * delta(p, q) - b * delta(q, p),
            table[p, solo[p]] - a * slope,
            sum(slope - delta(p, j) / weights[j] for j in range(n) if j != p),
            sum(table[i, solo[i]] - weights[i] * slope for i in range(n)),
        )

    target = {(i, s): s[i] * sum(w * x for w, x in zip(weights, s))
              for i in range(n) for s in ss}
    assert functionals(target) == (0, 0, 0, 0, 0)
    columns = []
    for sig in product(range(4), repeat=n):
        if not any(sig):
            continue
        for k in range(max_degree + 1):
            table = {(i, s): direct_cost(sig, k, weights, s, i) for i in range(n) for s in ss}
            columns.append((sig, k, functionals(table)))
    counts = [len(columns)]
    stage_names = ('zero-action costs', 'unequal pair high degrees', 'p solo budget',
                   'all p resources contain every player', 'all remaining solo budgets')
    eliminated = []
    for stage in range(5):
        assert all(col[2][stage] >= 0 for col in columns)
        kept = [col for col in columns if col[2][stage] == 0]
        eliminated.append(len(columns) - len(kept))
        columns = kept
        counts.append(len(columns))
    assert [(sig, k) for sig, k, _ in columns] == [((2,) * n, 1)]
    return dict(weights=list(map(str, weights)), max_degree=max_degree,
                full_signatures=4 ** n - 1, columns=counts[0], chosen_pair=[p, q],
                stage_names=stage_names, surviving_column_counts=counts,
                eliminated_columns=eliminated, final_only_column='all players action 1, fee x')


def audit_equal_weight_family(n, q):
    denom = 2 ** q - 1
    private = 1 - F(n - 1, denom)
    assert 2 ** q >= n and private >= 0
    # Resources are represented as (potential user set, coefficient, degree).
    resources = [(frozenset(pair), F(1, denom), q) for pair in combinations(range(n), 2)]
    if private:
        resources += [(frozenset((i,)), private, 0) for i in range(n)]
    checks = 0
    for s in product((0, 1), repeat=n):
        for i in range(n):
            actual = sum(coef * sum(s[j] for j in users) ** degree
                         for users, coef, degree in resources if i in users and s[i])
            expected = s[i] * sum(s)
            assert actual == expected
            checks += 1
    # Add two distinct private action markers per player and check actual sets.
    incidences = [(users, 1) for users, _, _ in resources]
    for i in range(n):
        for action in (0, 1):
            incidences.append((frozenset((i,)), action))
    for i in range(n):
        acts = [set(r for r, (users, a) in enumerate(incidences) if i in users and a == action)
                for action in (0, 1)]
        assert all(acts) and not acts[0].intersection(acts[1])
        assert not acts[0] <= acts[1] and not acts[1] <= acts[0]
    assert max(map(lambda r: len(r[0]), resources)) == 2 < n
    return dict(n=n, q=q, private_constant=str(private), positive_resources=len(resources),
                maximum_positive_potential_users=2, state_player_entries=checks,
                all_real_costs_match=True, zero_marker_core=True)


def audit_two_equal_players():
    w = F(3, 2)
    const, quadratic = 2 * w / 3, 1 / (3 * w)
    entries = 0
    for s in product((0, 1), repeat=2):
        load = w * sum(s)
        for i in range(2):
            actual = s[i] * (const + quadratic * load ** 2)
            assert actual == s[i] * load
            entries += 1
    return dict(n=2, equal_weight=str(w), full_resource_constant=str(const),
                full_resource_quadratic=str(quadratic), state_player_entries=entries)


def main():
    equal = []
    for n in range(3, 9):
        q = next(q for q in range(1, 10) if 2 ** q >= n)
        equal.extend(audit_equal_weight_family(n, power) for power in (q, q + 1))
    print(json.dumps(dict(
        scope='Finite exact algebra and representation audit; no substitute for arbitrary-degree real proof.',
        arithmetic='fractions.Fraction and integers; no tolerance, solver, or randomness',
        reviewed_freeze_sha256=REVIEWED_FREEZE,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        pair_signs=audit_pair_signs(),
        signature_faces=[audit_signature_faces(tuple(map(F, x)))
                         for x in [('1/2', '3/2'), ('1', '1', '2'), ('1/3', '1/3', '7/5', '7/5')]],
        equal_weight_families=equal,
        equal_two_player_nonaffine=audit_two_equal_players(),
    ), indent=2))


if __name__ == '__main__':
    main()
