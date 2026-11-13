"""Verify both integer customer vectors against the published 259-node policy."""
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import re

ARCHIVE = Path(__file__).resolve().parents[3]
POLICY_BODY = ARCHIVE / 'state/反例/实际前缀的剩余利润与新增覆盖--反例.md'
LABELS = range(6)  # A, B, T, Q, R, S
ORIGINAL = {1: 10, 2: 12, 4: 5, 8: 5, 20: 2, 24: 2, 36: 2, 40: 2, 49: 6, 50: 6}
EQUALITY = {4: 1, 8: 1, 51: 4}


def verify(weights, policy):
    def finish(history):
        while len(history) < 4:
            history += (policy[history],)
        return history

    def utility(terminal, player):
        return sum(
            (Fraction(weight, sum(bool(mask & (1 << action)) for action in terminal))
             for mask, weight in weights.items() if mask & (1 << terminal[player])),
            Fraction(0),
        )

    gaps = Counter()
    for history in policy:
        player = len(history)
        actual = utility(finish(history), player)
        for action in LABELS:
            gaps[actual - utility(finish(history + (action,)), player)] += 1

    terminal = finish(())
    assert terminal == (0, 1, 0, 1)
    assert sum(gaps.values()) == 1554 and min(gaps) == 0
    return {
        'customer_count': sum(weights.values()),
        'terminal': list(terminal),
        'terminal_payoffs': [str(utility(terminal, player)) for player in range(4)],
        'old_floor': str(sum((Fraction(weight, 2 + bool(mask & 1) + bool(mask & 2))
                             for mask, weight in weights.items() if mask & 3), Fraction(0))),
        'new_customers': sum(weight for mask, weight in weights.items() if not mask & 3),
        'deviation_slack_counts': {str(gap): gaps[gap] for gap in sorted(gaps)},
    }


def main():
    data = POLICY_BODY.read_text()
    literal = data.split('POLICY = (', 1)[1].split(')', 1)[0]
    actions = ''.join(re.findall(r'"([0-5]+)"', literal))
    histories = [h for depth in range(4) for h in product(LABELS, repeat=depth)]
    assert len(actions) == len(histories) == 259
    policy = dict(zip(histories, map(int, actions)))
    original = verify(ORIGINAL, policy)
    equality = verify(EQUALITY, policy)
    assert original['terminal_payoffs'] == ['8', '9', '8', '9']
    assert equality['terminal_payoffs'] == ['1'] * 4
    assert original['new_customers'] == 18 and equality['new_customers'] == 2
    assert original['old_floor'] == '34/3' and equality['old_floor'] == '1'
    assert all(mask & 12 for mask in (ORIGINAL | EQUALITY) if not mask & 3)
    print(json.dumps({'original': original, 'equality': equality}, indent=2))


if __name__ == '__main__':
    main()
