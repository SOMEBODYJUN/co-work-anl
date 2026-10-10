"""Exact two-level obstruction to the bare two-plus-three proposed path.

This is a necessary credible-tail rejection, not a counterexample to coverage.
"""
from fractions import Fraction as F
from itertools import product
import json


def run():
    types = [(frozenset(set(range(10)) - {a, b}), 3)
             for a, b in product(range(5), range(5, 10))]

    def utility(action, z):
        return sum((F(count, sum(b in likes for b in z))
                    for likes, count in types if action in likes), F(0))

    h = (3, 4, 5)
    actual = (3, 4, 5, 6, 7)
    actual_payoff = utility(6, actual)
    last_values = [utility(a, h + (0, a)) for a in range(10)]
    last_best = max(last_values)
    best_replies = [a for a in range(10) if last_values[a] == last_best]
    deviation_values = [utility(0, h + (0, a)) for a in best_replies]
    assert actual_payoff == F(151, 10)
    assert min(deviation_values) == F(303, 20)
    assert min(deviation_values) - actual_payoff == F(1, 20)
    assert utility(7, actual) == max(utility(a, h + (6, a)) for a in range(10))
    return {'status': 'PASS', 'unit_customers': 75, 'players': 5, 'topics': 10,
            'target_path': actual, 'fourth_history': h, 'actual_fourth_payoff': str(actual_payoff),
            'deviation_action': 0, 'last_payoffs_after_deviation': list(map(str, last_values)),
            'last_best_replies_after_deviation': best_replies,
            'fourth_payoffs_at_all_last_best_replies': list(map(str, deviation_values)),
            'credible_deviation_floor': str(min(deviation_values)), 'strict_gain': '1/20',
            'scope': 'Bare 25 omitted-pair populations only; rejects this target path in every complete SPE.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
