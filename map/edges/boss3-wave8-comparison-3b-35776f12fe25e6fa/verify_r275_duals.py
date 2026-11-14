"""Replay the two frozen R275 fixed-strategy certificates using rational arithmetic."""
import argparse
import json
from fractions import Fraction as F
from functools import cache
from itertools import combinations, product
from math import comb
from pathlib import Path


LABELS = range(7)
DEPTH = 5
PORTFOLIO = (2, 3, 4, 5, 6)


def moment_key(mask):
    return (mask & 3, (mask >> 2).bit_count())


KEYS = sorted({moment_key(mask) for mask in range(1, 128) if mask.bit_count() <= DEPTH})
ZERO = (F(0),) * len(KEYS)


@cache
def value_row(mask):
    if mask == 0:
        return ZERO
    return tuple(F(moment_key(mask) == key) for key in KEYS)


def combine(*terms):
    return tuple(sum(factor * row[i] for factor, row in terms) for i in range(len(KEYS)))


def difference(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(row, values):
    return sum(a * b for a, b in zip(row, values))


def count_labels(h):
    return tuple(h.count(label) for label in LABELS)


@cache
def payoff_row(counts, label):
    other_copies = tuple(a for a in LABELS for _ in range(counts[a] - (a == label)))
    row = [F(0)] * len(KEYS)
    for size in range(DEPTH):
        for subset in combinations(other_copies, size):
            mask = sum(1 << a for a in set(subset))
            marginal = difference(value_row(mask | (1 << label)), value_row(mask))
            weight = F(1, DEPTH * comb(DEPTH - 1, size))
            for i, coefficient in enumerate(marginal):
                row[i] += weight * coefficient
    return tuple(row)


def axioms():
    mono = []
    dr = []
    for mask in range(128):
        if mask.bit_count() >= DEPTH:
            continue
        missing = [1 << a for a in LABELS if not mask & (1 << a)]
        for a in missing:
            mono.append(difference(value_row(mask | a), value_row(mask)))
        if mask.bit_count() <= DEPTH - 2:
            for a, b in combinations(missing, 2):
                dr.append(combine((1, value_row(mask | a)), (1, value_row(mask | b)),
                                  (-1, value_row(mask)), (-1, value_row(mask | a | b))))
    return mono, dr


def replay(actions):
    assert len(actions) == sum(len(LABELS) ** depth for depth in range(DEPTH))
    terminals = {}
    for depth in range(DEPTH, -1, -1):
        for h in product(LABELS, repeat=depth):
            if depth == DEPTH:
                terminals[h] = h
            else:
                terminals[h] = terminals[h + (actions[h],)]
    return terminals


def path_cuts(actual):
    rows = set()
    counts = count_labels(actual)
    for i, action in enumerate(actual):
        actual_payoff = payoff_row(counts, action)
        for alt in LABELS:
            all_copy = count_labels(actual[:i] + (alt,) * (DEPTH - i))
            row = difference(actual_payoff, payoff_row(all_copy, alt))
            if any(row):
                rows.add(row)
    return rows


def verify(path):
    data = json.loads(path.read_text())
    assert data['moment_orbits'] == [list(key) for key in KEYS]
    assert data['coefficient_rows_checked'] == sum(
        sum(n > 0 for n in counts) for counts in {count_labels(h) for h in product(LABELS, repeat=DEPTH)}
    )
    exact = data['exact_candidate']
    values = tuple(map(F, exact['values']))
    assert all(v > 0 for v in values)
    actions = {tuple(record['history']): record['action'] for record in exact['complete_strategy']['actions']}
    terminals = replay(actions)
    actual = terminals[()]
    counts = count_labels(actual)
    assert list(counts) == exact['complete_strategy']['terminal_counts']
    assert list(actual) == data['milp']['path']
    assert list(PORTFOLIO) == data['milp']['portfolio']
    actual_support = sum(1 << a for a in set(actual))
    w = value_row(actual_support)
    objective = value_row(sum(1 << a for a in PORTFOLIO))
    mono, dr = axioms()
    mono_dr = set(mono + dr) - {ZERO}
    pcuts = path_cuts(actual)
    eps = F(str(data.get('root_marginal_floor', 0)))
    floors = {combine((1 - eps, w), (-1, value_row(actual_support ^ (1 << a))))
              for a in set(actual)} if eps else set()
    actual_ics = []
    for h, chosen in actions.items():
        u = payoff_row(count_labels(terminals[h]), chosen)
        for alt in LABELS:
            if alt != chosen:
                v = payoff_row(count_labels(terminals[h + (alt,)]), alt)
                actual_ics.append(difference(u, v))
    # Non-self actions give a nonzero row in the original customer coordinates
    # by the singleton customer types, even if reduction identifies a zero row.
    rows = sorted(mono_dr | pcuts | floors | set(actual_ics))
    assert len(rows) > 0 and dot(w, values) == 1
    assert all(dot(row, values) >= 0 for row in rows)
    beta = F(exact['dual_bound'])
    dual = {i: F(value) for i, value in exact['dual_support']}
    assert all(0 <= i < len(rows) and mu > 0 for i, mu in dual.items())
    residual = tuple(beta * w[j] - sum(mu * rows[i][j] for i, mu in dual.items()) - objective[j]
                     for j in range(len(KEYS)))
    assert residual == ZERO
    assert dot(objective, values) == beta == F(exact['value'])
    assert all(dot(rows[i], values) == 0 for i in dual)
    supports = [(mask, dot(value_row(mask), values)) for mask in range(128) if mask.bit_count() <= DEPTH]
    optimum = max(v for _, v in supports)
    optimal = [mask for mask, v in supports if v == optimum]
    assert optimal == [sum(1 << a for a in PORTFOLIO)]
    payments = [dot(payoff_row(counts, a), values) for a in actual]
    assert sum(payments) == 1
    margins = [dot(difference(w, value_row(actual_support ^ (1 << a))), values)
               for a in sorted(set(actual))]
    query = [[dot(payoff_row(count_labels(terminals[actual[:i] + (a,)]), a), values)
              for a in LABELS] for i in range(DEPTH)]
    qsum = sum(row[a] for row in query for a in PORTFOLIO)
    ic_slacks = [dot(row, values) for row in actual_ics]
    assert len(ic_slacks) == exact['independent_uniform_order_audit']['nonself_deviations']
    assert ic_slacks.count(0) == exact['independent_uniform_order_audit']['ties']
    print(path.name)
    print('path', actual, 'histories', len(actions), 'deviations', len(actual_ics),
          'ties', ic_slacks.count(0), 'min slack', min(ic_slacks))
    print('unquotiented monotonicity/DR', len(mono), len(dr), 'unique nonzero axiom rows', len(mono_dr),
          'unique nonzero path rows', len(pcuts), 'floors', len(floors),
          'unique reduced genuine ICs', len(set(actual_ics)), 'unique union', len(rows),
          'dual positive terms', len(dual), 'of which path-only',
          sum(rows[i] in pcuts - mono_dr - floors - set(actual_ics) for i in dual))
    print('exact objective and dual bound', beta, 'root marginals', list(map(str, margins)))
    print('payments', list(map(str, payments)), 'queries', [list(map(str, row)) for row in query],
          'Q', qsum, 'D', 4 + qsum - 5 * optimum)
    print('all primal rows, all dual coordinates, and unique optimal support verified')
    return actions


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('frozen_reports', nargs='+', type=Path)
    arguments = parser.parse_args()
    strategies = [verify(path) for path in arguments.frozen_reports]
    if len(strategies) == 2:
        print('old-table differing ordered histories', sum(strategies[0][h] != strategies[1][h] for h in strategies[0]))
