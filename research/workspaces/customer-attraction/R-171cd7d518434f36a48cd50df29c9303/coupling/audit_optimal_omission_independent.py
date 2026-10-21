#!/usr/bin/env python3
"""Independent all-history/unit-client audit and linear-family certificate.

Inputs transcribed only from the proposed interest table and full strategy.
No author audit, optimization package, or repository equilibrium engine is
imported. A linear polynomial is represented by (constant, slope).
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import argparse
import json


LABELS = tuple('ABTQRS')
REPLY = dict(zip(LABELS, 'BSRSSR'))
# The order above gives A->B, B->S, T->R, Q->S, R->S, S->R.
assert REPLY == {'A': 'B', 'B': 'S', 'T': 'R', 'Q': 'S', 'R': 'S', 'S': 'R'}
TYPES = [
    ('A', (-2, 4)), ('ARS', (0, 2)),
    ('B', (-2, 5)), ('BRS', (-2, 2)),
    ('BTRS', (1, 0)), ('BQRS', (1, 0)),
    ('T', (-1, 3)), ('TR', (-1, 2)), ('TS', (-1, 2)),
    ('Q', (-1, 3)), ('QR', (-1, 2)), ('QS', (-1, 2)),
]


def plus(*polys):
    return tuple(sum((F(p[i]) for p in polys), F(0)) for i in (0, 1))


def scale(a, p):
    return tuple(F(a) * v for v in p)


def minus(a, b):
    return plus(a, scale(-1, b))


def at(p, k):
    return p[0] + k * p[1]


def payoff_poly(first, second, player):
    selected = (first, second)[player]
    terms = []
    for interest, multiplicity in TYPES:
        if selected in interest:
            load = (first in interest) + (second in interest)
            terms.append(scale(F(1, load), multiplicity))
    return plus(*terms)


def coverage_poly(pair):
    return plus(*(mult for interest, mult in TYPES
                  if any(label in interest for label in pair)))


def serialize(p):
    return {'constant': str(p[0]), 'slope': str(p[1]),
            'value_at_3': str(at(p, 3))}


def run():
    # Actual unit expansion at k=3; no compressed payoff formulas used here.
    clients = []
    for interest, multiplicity in TYPES:
        count = at(multiplicity, 3)
        assert count.denominator == 1 and count >= 0
        clients.extend(frozenset(interest) for _ in range(int(count)))
    topics = {label: {x for x, interest in enumerate(clients) if label in interest}
              for label in LABELS}
    assert len(clients) == 71
    assert len({frozenset(topic) for topic in topics.values()}) == 6

    def unit_payoff(pair, player):
        action = pair[player]
        return sum((F(1, sum(label in clients[x] for label in pair))
                    for x in topics[action]), F(0))

    leaf_matrix = [[unit_payoff((first, second), 1) for second in LABELS]
                   for first in LABELS]
    unit_inequalities = []
    for first in LABELS:
        prescribed = unit_payoff((first, REPLY[first]), 1)
        for other in LABELS:
            gap = prescribed - unit_payoff((first, other), 1)
            assert gap >= 0
            unit_inequalities.append((first, other, gap))
    actual = ('A', REPLY['A'])
    root = unit_payoff(actual, 0)
    root_returns = []
    for first in LABELS:
        deviation = unit_payoff((first, REPLY[first]), 0)
        assert root >= deviation
        unit_inequalities.append(('', first, root - deviation))
        root_returns.append(deviation)
    assert len(unit_inequalities) == 42

    unions = []
    for pair in combinations_with_replacement(LABELS, 2):
        union = topics[pair[0]] | topics[pair[1]]
        unions.append((pair, len(union)))
    assert len(unions) == 21
    optimum = max(size for _, size in unions)
    maximizers = [pair for pair, size in unions if size == optimum]
    assert maximizers == [('T', 'Q')]
    C = topics['A'] | topics['B']
    O = topics['T'] | topics['Q']
    values = {'W': len(C), 'OPT': len(O), 'U': len(O - C),
              'G': len(C - O), 'intersection': len(O & C),
              'half_slack': 2 * len(C) - len(O)}
    assert values == {'W': 35, 'OPT': 38, 'U': 36, 'G': 33,
                      'intersection': 2, 'half_slack': 32}
    assert values['U'] > values['W']

    # Complete symbolic comparison certificate for every integer k>=3.
    # For a linear polynomial f(k)=alpha*k+beta, alpha>=0 and f(3)>=0
    # prove f(k)>=0 on this entire range. Strict f(3)>0 proves strictness.
    symbolic_gaps = []
    for first in LABELS:
        best = payoff_poly(first, REPLY[first], 1)
        for other in LABELS:
            gap = minus(best, payoff_poly(first, other, 1))
            assert gap[1] >= 0 and at(gap, 3) >= 0
            symbolic_gaps.append({'history': first, 'query': other,
                                  **serialize(gap)})
    symbolic_root = payoff_poly('A', 'B', 0)
    for other in LABELS:
        gap = minus(symbolic_root, payoff_poly(other, REPLY[other], 0))
        assert gap == (0, 0)
        symbolic_gaps.append({'history': '', 'query': other, **serialize(gap)})
    # Positivity of every customer multiplicity is also certified on k>=3.
    for interest, mult in TYPES:
        assert mult[1] >= 0 and at(mult, 3) > 0
    symbolic_pairs = []
    opt_poly = coverage_poly(('T', 'Q'))
    for pair in combinations_with_replacement(LABELS, 2):
        poly = coverage_poly(pair)
        assert at(poly, 3) == dict(unions)[pair]
        gap = minus(opt_poly, poly)
        if pair != ('T', 'Q'):
            assert gap[1] >= 0 and at(gap, 3) > 0
        else:
            assert gap == (0, 0)
        symbolic_pairs.append({'pair': ''.join(pair), 'coverage': serialize(poly),
                                'optimality_gap': serialize(gap)})
    # Rebuild intersection, omitted, and exclusive customers from types.
    named_poly = {}
    named_poly['total_clients'] = plus(*(mult for _, mult in TYPES))
    named_poly['W'] = coverage_poly(('A', 'B'))
    named_poly['OPT'] = opt_poly
    named_poly['U'] = plus(*(mult for interest, mult in TYPES
                            if ('T' in interest or 'Q' in interest)
                            and not ('A' in interest or 'B' in interest)))
    named_poly['G'] = plus(*(mult for interest, mult in TYPES
                            if ('A' in interest or 'B' in interest)
                            and not ('T' in interest or 'Q' in interest)))
    named_poly['intersection'] = plus(*(mult for interest, mult in TYPES
                            if ('A' in interest or 'B' in interest)
                            and ('T' in interest or 'Q' in interest)))
    assert named_poly == {'total_clients': (-10, 27), 'W': (-4, 13),
                          'OPT': (-4, 14), 'U': (-6, 14), 'G': (-6, 13),
                          'intersection': (2, 0)}
    assert minus(named_poly['U'], named_poly['W']) == (-2, 1)
    assert minus(scale(2, named_poly['W']), named_poly['OPT']) == (-4, 12)
    # Compare all 72 unit-terminal payoff entries to the independent family map.
    for first in LABELS:
        for second in LABELS:
            for player in (0, 1):
                assert unit_payoff((first, second), player) == at(
                    payoff_poly(first, second, player), 3)

    return {
        'status': 'independent unit-client and all-k linear checks passed',
        'scope': 'counterexample to optimal omission existence bridge only; not Q-CAG-HALF',
        'labels': LABELS, 'strategy': {'root': 'A', 'reply': REPLY},
        'unit_client_count': len(clients), 'decision_histories': 7,
        'all_history_comparisons': len(unit_inequalities),
        'terminal_payoff_entries_crosschecked': 72,
        'reply_payoff_matrix': [[str(v) for v in row] for row in leaf_matrix],
        'root_deviation_returns': [str(v) for v in root_returns],
        'pair_coverage': {''.join(pair): size for pair, size in unions},
        'unique_optimal_unordered_pairs': [''.join(pair) for pair in maximizers],
        'values_at_k3': values,
        'family_polynomials': {name: serialize(poly) for name, poly in named_poly.items()},
        'family_all_history_gap_certificates': symbolic_gaps,
        'family_all_pair_certificates': symbolic_pairs,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), ensure_ascii=False, indent=2)
    if args.output:
        with args.output.open('x', encoding='utf-8') as out:
            out.write(result + '\n')
    print(result)
