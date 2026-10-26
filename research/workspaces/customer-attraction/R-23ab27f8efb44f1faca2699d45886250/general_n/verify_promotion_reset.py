"""Fixed exact full-history witness; no solver, LP, or random scan.

This verifies a failed promotion-potential bridge, not a HALF counterexample.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def verify(t: int) -> dict:
    assert t > 0
    # P likes A,C; Q likes B; O likes A,B. Each entry is one distinct unit.
    units = [(0, 2)] * (2*t) + [(1,)] * (2*t) + [(0, 1)] * (3*t)
    actions = {(): 0, (0,): 1, (1,): 2, (2,): 1}
    last = ((1, 1, 1), (0, 0, 1), (1, 0, 1))
    actions.update({(a, b): last[a][b] for a, b in product(range(3), repeat=2)})

    def finish(h=()):
        while len(h) < 3:
            h += (actions[h],)
        return h

    def payoff(z, i):
        return sum((F(1, sum(a in likes for a in z))
                    for likes in units if z[i] in likes), F(0))

    def potential(z):
        return sum((sum((F(1, j) for j in range(1, sum(a in likes for a in z)+1)), F(0))
                    for likes in units), F(0))

    def welfare(z):
        return sum(any(a in likes for a in z) for likes in units)

    table = []
    for length in range(3):
        for h in product(range(3), repeat=length):
            z = finish(h)
            payoffs = tuple(payoff(finish(h+(a,)), length) for a in range(3))
            chosen = payoff(z, length)
            assert chosen == payoffs[actions[h]] and chosen == max(payoffs)
            table.append({'history': h, 'action': actions[h],
                          'true_deviation_payoffs': list(map(str, payoffs))})

    old = finish()
    promoted = finish((old[-1],))
    assert old == (0, 1, 1) and promoted == (1, 2, 1)
    gap = potential(old)-potential(promoted)
    # General reset expression: new prefix old[-1], D=new[1], E=new[2].
    reset = sum((F(1, (int(promoted[0] in likes)+1)*(int(promoted[0] in likes)+2))
                 for likes in units if promoted[1] in likes and promoted[2] not in likes), F(0))
    assert potential(old) == F(21*t, 2)
    assert potential(promoted) == F(19*t, 2)
    assert gap == reset == t
    assert tuple(payoff(old, i) for i in range(3)) == (3*t, 2*t, 2*t)
    assert tuple(payoff(promoted, i) for i in range(3)) == (F(5*t, 2), 2*t, F(5*t, 2))
    optimum = max(welfare(z) for z in product(range(3), repeat=3))
    assert welfare(old) == optimum == 7*t
    return {'status': 'exact_fixed_family_witness_passed',
            'scope': 'Promotion-potential bridge false; sharp existing strong-PAIR reset; not HALF counterexample',
            't': t, 'unit_customers': len(units), 'players': 3, 'topic_count': 3,
            'ordered_histories': len(table), 'IC_comparisons_including_self': 3*len(table),
            'strategy_and_exact_payoffs': table,
            'actual_path': old, 'promoted_true_path': promoted,
            'actual_potential': str(potential(old)), 'promoted_potential': str(potential(promoted)),
            'potential_drop': str(gap), 'new_branch_exclusive_reset_tax': str(reset),
            'W': welfare(old), 'OPT_3': optimum}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--t', type=int, default=1)
    parser.add_argument('--output')
    args = parser.parse_args()
    result = json.dumps(verify(args.t), ensure_ascii=False, indent=2)+'\n'
    if args.output:
        with Path(args.output).open('x') as handle:
            handle.write(result)
    print(result)
