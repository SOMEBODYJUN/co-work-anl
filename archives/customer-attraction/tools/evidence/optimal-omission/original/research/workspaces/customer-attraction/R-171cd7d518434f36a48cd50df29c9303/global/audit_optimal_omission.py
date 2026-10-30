"""Definition-level unit-customer audit. No solver or discovery code is imported."""
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
NAMES = ('A', 'B', 'T', 'Q', 'R', 'S')
GROUPS = (
    ('A', 10), ('ARS', 6), ('B', 13), ('BRS', 4),
    ('BTRS', 1), ('BQRS', 1),
    ('T', 8), ('TR', 5), ('TS', 5),
    ('Q', 8), ('QR', 5), ('QS', 5),
)
# The following list explicitly contains 71 distinct unit clients.
CLIENTS = tuple(frozenset(letters) for letters, number in GROUPS for _ in range(number))
REPLY = dict(zip(NAMES, ('B', 'S', 'R', 'S', 'S', 'R')))

def utility(action, profile):
    return sum((Fraction(1, sum(a in client for a in profile))
                for client in CLIENTS if action in client), Fraction(0))

def covered(profile):
    return frozenset(i for i, client in enumerate(CLIENTS) if any(a in client for a in profile))

def main():
    assert len(CLIENTS) == 71
    rows = {}
    comparison_count = 0
    for first in NAMES:
        values = {a: utility(a, (first, a)) for a in NAMES}
        selected = values[REPLY[first]]
        assert all(selected >= value for value in values.values())
        comparison_count += len(values)
        rows[first] = {a: str(value) for a, value in values.items()}
    root = {a: utility(a, (a, REPLY[a])) for a in NAMES}
    assert root['A'] == 16 and all(root['A'] >= value for value in root.values())
    comparison_count += len(root)
    assert comparison_count == 42
    pairs = {''.join(pair): len(covered(pair)) for pair in combinations_with_replacement(NAMES, 2)}
    opt = max(pairs.values())
    maximizers = [pair for pair, value in pairs.items() if value == opt]
    assert opt == 38 and maximizers == ['TQ']
    actual = covered(('A', 'B'))
    optimum = covered(('T', 'Q'))
    W, missed, excess = len(actual), len(optimum - actual), len(actual - optimum)
    assert (W, missed, excess, len(actual & optimum)) == (35, 36, 33, 2)
    assert missed > W and opt - W == missed - excess == 3
    assert 2 * W - opt == 32
    report = {
        'status': 'exact unit-customer audit passed',
        'unit_customers': len(CLIENTS), 'decision_histories': 7,
        'including_self_comparisons': comparison_count,
        'root': 'A', 'reply': REPLY, 'follower_utility_table': rows,
        'leader_deviation_utility': {a: str(v) for a, v in root.items()},
        'all_unordered_pair_coverages': pairs,
        'optimal_welfare': opt, 'unique_optimal_unordered_pair': maximizers[0],
        'actual_profile': ['A', 'B'], 'actual_payoffs': ['16', '19'],
        'actual_welfare': W, 'optimal_missed': missed,
        'actual_outside_optimum_G': excess, 'intersection': 2,
        'OPT_minus_W_equals_U_minus_G': 3, 'half_slack': 32,
    }
    print(json.dumps(report, indent=2))
    return report

if __name__ == '__main__':
    main()
