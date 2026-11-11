"""Finite full-history policy audit, exact affine payoffs a*R+b*C.
All writes are outside the review clone. No scientific search or new SPE solver.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

LABELS = tuple(product(range(3), range(2)))

def counts(history, axis, size):
    return tuple(sum(a[axis] == k for a in history) for k in range(size))

def minima(values):
    return tuple(i for i, v in enumerate(values) if v == min(values))

def balanced(history):
    n = len(history)
    if n == 0:
        return (0, 0)
    rmin = minima(counts(history, 0, 3))
    row = history[0][0] if n == 3 and len(rmin) == 3 else rmin[0]
    col = minima(counts(history, 1, 2))[0]
    return (row, col)

def same_column(history):
    n = len(history)
    if n == 0:
        return (0, 0)
    if n == 1:
        return (min(r for r in range(3) if r != history[0][0]), history[0][1])
    a, b = history[:2]
    if n == 2:
        empty_row = minima(counts(history, 0, 3))[0]
        if a[0] != b[0] and a[1] == b[1]:
            return (empty_row, a[1])
        return (empty_row, minima(counts(history, 1, 2))[0])
    rmin = minima(counts(history, 0, 3))
    row = rmin[0]
    if len(rmin) == 3:
        if a[0] != b[0] and a[1] == b[1]:
            row = a[0] if history[2][1] == a[1] else history[2][0]
        elif a[0] != b[0] and a[1] != b[1]:
            row = b[0]
    return (row, minima(counts(history, 1, 2))[0])

def complete(history, policy):
    while len(history) < 4:
        history += (policy(history),)
    return history

def payoff(leaf, player):
    action = leaf[player]
    return tuple(F(1, sum(a[axis] == action[axis] for a in leaf)) for axis in range(2))

def frac(value):
    return str(value)

def audit(policy, domain):
    # For all R,C>0, aR+bC>=0 iff both coefficients are nonnegative.
    # On R>=C/3>0, equivalent to a>=0 and a/3+b>=0.
    failures = []
    by_depth = []
    distinct_diffs = set()
    for depth in range(4):
        nodes, comparisons = 0, 0
        for history in product(LABELS, repeat=depth):
            nodes += 1
            actual = payoff(complete(history, policy), depth)
            for action in LABELS:
                alt = payoff(complete(history + (action,), policy), depth)
                diff = tuple(a - b for a, b in zip(actual, alt))
                distinct_diffs.add(diff)
                comparisons += 1
                a, b = diff
                valid = (a >= 0 and b >= 0) if domain == 'positive quadrant' else (a >= 0 and a / 3 + b >= 0)
                if not valid:
                    failures.append({'history': history, 'action': action, 'diff': [frac(x) for x in diff]})
        by_depth.append({'depth': depth, 'nodes': nodes, 'comparisons': comparisons})
    roots = []
    for action in LABELS:
        leaf = complete((action,), policy)
        roots.append({'root': action, 'leaf': leaf, 'payoffs': [[frac(x) for x in payoff(leaf, i)] for i in range(4)]})
    return {'parameter_domain': domain, 'criterion': 'a>=0 and b>=0' if domain == 'positive quadrant' else 'a>=0 and a/3+b>=0', 'by_depth': by_depth, 'nodes': sum(x['nodes'] for x in by_depth), 'comparisons': sum(x['comparisons'] for x in by_depth), 'distinct_affine_differences': [[frac(x) for x in diff] for diff in sorted(distinct_diffs)], 'failures': failures, 'forced_root_outcomes': roots}

if __name__ == '__main__':
    result = {'method': 'Enumerate every ordered history, compare prescribed action with each of six actions using the same actual suffix strategy; preserve exact coefficients aR+bC; discharge a cone inequality rather than sample numerical ratios.', 'balanced': audit(balanced, 'positive quadrant'), 'three_same_column': audit(same_column, 'R>=C/3>0')}
    path = Path(__file__).with_name('symbolic_strategy_audit.json')
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: {'nodes': value['nodes'], 'comparisons': value['comparisons'], 'failure_count': len(value['failures']), 'distinct_affine_differences': value['distinct_affine_differences']} for key, value in result.items() if key != 'method'}, ensure_ascii=False, indent=2))
