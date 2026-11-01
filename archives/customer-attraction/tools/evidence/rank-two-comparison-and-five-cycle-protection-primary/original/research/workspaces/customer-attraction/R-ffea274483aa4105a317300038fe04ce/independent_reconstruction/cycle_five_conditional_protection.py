"""Definition-level rational audit of a false rank-two protection lemma.

This script does not assert that the exhibited future sequence is an SPE.
It explicitly verifies the last player's profitable deviation.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys


TOPICS = tuple(frozenset((a, (a-1) % 5)) for a in range(5))


def utilities(path):
    loads = {edge: sum(edge in TOPICS[a] for a in path) for edge in range(5)}
    return tuple(sum((Fraction(1, loads[edge]) for edge in TOPICS[a]), Fraction())
                 for a in path)


def main():
    floors = {}
    for prefix in product(range(5), repeat=2):
        values = [utilities(prefix + (action,))[-1] for action in range(5)]
        floors[prefix] = max(values)
        if prefix[0] == prefix[1] or (prefix[0]-prefix[1]) % 5 in (1, 4):
            assert max(values) == 2
        else:
            assert max(values) == Fraction(3, 2)
    theta = min(floors.values())
    assert theta == Fraction(3, 2)
    victims = []
    for action in range(5):
        path = (action, (action-1) % 5, (action+1) % 5)
        values = utilities(path)
        assert values == (1, theta, theta)
        last_values = [utilities(path[:2] + (reply,))[-1] for reply in range(5)]
        best = max(last_values)
        assert best == 2 > values[-1]
        victims.append({'path': path, 'utilities': list(map(str, values)),
                        'last_best_response': str(best),
                        'profitable_last_actions': [reply for reply, value in enumerate(last_values)
                                                    if value == best]})
    report = {'theta': str(theta), 'ordered_prefixes': len(floors),
              'victim_sequences': victims,
              'claim_refuted': 'rank-two conditional protection using only follower floors',
              'is_spe_counterexample': False}
    Path(sys.argv[1]).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
