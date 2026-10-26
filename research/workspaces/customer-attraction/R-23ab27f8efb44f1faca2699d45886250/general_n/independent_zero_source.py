"""Independent ordered-tree construction for the seven-unit reset witness.

Does not import the author's strategy, checker, optimization, or game solver.
Different ordered histories keep independently selectable continuations.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import json


def run():
    units = []
    for mask, number in ((1, 1), (4, 2), (6, 2), (11, 2)):
        units.extend([frozenset(a for a in range(4) if mask >> a & 1)] * number)

    def payoff(z, i):
        return sum((F(1, sum(a in interests for a in z))
                    for interests in units if z[i] in interests), F())

    def potential(z):
        return sum((sum((F(1, j) for j in range(1, sum(a in interests for a in z) + 1)), F())
                    for interests in units), F())

    def welfare(z):
        return sum(any(a in interests for a in z) for interests in units)

    @lru_cache(None)
    def outcomes(h):
        if len(h) == 3:
            return (h,)
        children = [outcomes(h + (a,)) for a in range(4)]
        threshold = max(min(payoff(z, len(h)) for z in child) for child in children)
        return tuple(z for child in children for z in child if payoff(z, len(h)) >= threshold)

    assert (0, 1, 2) in outcomes(()) and (2, 3, 2) in outcomes((2,))
    actions = {}

    def construct(h, desired):
        if len(h) == 3:
            return
        i = len(h)
        chosen = desired[i]
        actions[h] = chosen
        for a in range(4):
            child = h + (a,)
            target = desired if a == chosen else min(outcomes(child), key=lambda z: (payoff(z, i), z))
            if not h and a == 2:
                target = (2, 3, 2)
            construct(child, target)

    construct((), (0, 1, 2))

    def finish(h):
        while len(h) < 3:
            h += (actions[h],)
        return h

    comparisons = []
    for h, chosen in sorted(actions.items()):
        values = [payoff(finish(h + (a,)), len(h)) for a in range(4)]
        assert values[chosen] == max(values)
        comparisons.append({'history': h, 'action': chosen, 'payoffs': list(map(str, values))})
    old = finish(())
    new = finish((old[-1],))
    source_gap = payoff(old, 0) - payoff(new, 0)
    drop = potential(old) - potential(new)
    assert old == (0, 1, 2) and new == (2, 3, 2)
    assert source_gap == 0 and drop == 1
    chain = [new, finish((2, 0)), (2, 0, 1)]
    gaps, resets = [], []
    for i in (1, 2):
        z, zz = chain[i - 1:i + 1]
        gamma = payoff(z, i) - payoff(zz, i)
        reset = potential(zz[:i] + zz[i + 1:]) - potential(z[:i] + z[i + 1:])
        assert potential(zz) - potential(z) == reset - gamma
        gaps.append(gamma)
        resets.append(reset)
    assert gaps == [0, 0] and resets == [1, 0]
    assert welfare(old) == 7 and welfare(new) == 6
    assert max(welfare(z) for z in product(range(4), repeat=3)) == 7
    return {'scope': 'independent complete ordered-tree construction; auxiliary payment bridge counterexample',
            'unit_customer_masks': {'1': 1, '4': 2, '6': 2, '11': 2},
            'ordered_tree_states': outcomes.cache_info().currsize,
            'ordered_decision_histories': len(actions), 'all_IC_comparisons': 4 * len(actions),
            'actual': old, 'promoted': new, 'actual_potential': str(potential(old)),
            'promoted_potential': str(potential(new)), 'potential_drop': str(drop),
            'source_IC_slack': str(source_gap), 'replay_IC_slacks': list(map(str, gaps)),
            'signed_deletion_potential_resets': list(map(str, resets)),
            'W': 7, 'promoted_W': 6, 'OPT_3': 7, 'strategy_and_payoffs': comparisons,
            'main_half_status': 'OPEN; this is not a HALF counterexample'}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    text = json.dumps(run(), indent=2) + '\n'
    if args.output:
        with args.output.open('x') as stream:
            stream.write(text)
    print(text, end='')
