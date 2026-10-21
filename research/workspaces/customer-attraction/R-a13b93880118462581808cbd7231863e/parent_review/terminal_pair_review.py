"""Independent definition-level replay of the finite load-dominance witness.

No import from its discovery code, SPE solver, or payoff implementation.
This checks a finite witness, not the general conditional theorem.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def main():
    base = Path(__file__).resolve().parents[1]
    raw = json.loads((base / 'credible_attack/load_dominance_witness.json').read_text())
    topics = ({0, 1}, {2, 3}, {0, 2}, {1, 3})
    actions = {tuple(row['history']): row['action']
               for row in raw['certificate']['actions']}
    histories = {h for depth in range(4) for h in product(range(4), repeat=depth)}
    assert set(actions) == histories

    def finish(prefix):
        while len(prefix) < 4:
            prefix += (actions[prefix],)
        return prefix

    def payoff(terminal, player):
        return sum((Fraction(1, sum(x in topics[a] for a in terminal))
                    for x in topics[terminal[player]]), Fraction())

    checks = 0
    for h in sorted(histories, key=lambda h: (len(h), h)):
        actual = payoff(finish(h), len(h))
        for alternative in range(4):
            if alternative != actions[h]:
                assert actual >= payoff(finish(h + (alternative,)), len(h))
                checks += 1
    terminal = finish(())
    assert terminal == (2, 3, 0, 1)
    p = [sum(x in topics[a] for a in terminal[:2]) for x in range(4)]
    assert p == [1, 1, 1, 1]
    assert all(p[x] >= int(x in topics[0]) + int(x in topics[1]) for x in range(4))
    assert all(not (topics[a] >= topics[b]) for a in terminal[:2] for b in terminal[2:])

    def last_value(first, last):
        return sum((Fraction(1, p[x] + 1 + int(x in topics[first]))
                    for x in topics[last]), Fraction())

    theta = min(max(last_value(first, last) for last in range(4)) for first in range(4))
    gains = [payoff(terminal, player) for player in range(4)]
    welfare = len(set().union(*(topics[a] for a in terminal)))
    optimum = max(len(set().union(*(topics[a] for a in candidate)))
                  for candidate in product(range(4), repeat=4))
    assert sum(gains) == welfare == optimum == 4
    assert theta == 1 and welfare == 4 * theta
    print(json.dumps({'histories': len(histories), 'genuine_deviations': checks,
                      'terminal': terminal, 'payoffs': [str(v) for v in gains],
                      'theta_at_actual_prefix': str(theta), 'W': welfare,
                      'OPT': optimum, 'load_dominance': True,
                      'no_early_action_contains_either_tail_action': True}, indent=2))


if __name__ == '__main__':
    main()
