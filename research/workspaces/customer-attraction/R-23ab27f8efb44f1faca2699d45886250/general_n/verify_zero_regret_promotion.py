"""A fixed all-history witness, checked on distinct unit customers.

No solver, optimizer, random search, or anonymous strategy restriction.
The failed statement concerns promotion of the ACTUAL LAST topic.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

LAST = ((2, 2, 2, 2), (2, 2, 0, 2), (1, 0, 0, 2), (2, 2, 2, 2))
ACTIONS = {(): 0, (0,): 1, (1,): 2, (2,): 3, (3,): 1}
ACTIONS.update({(a, b): LAST[a][b] for a, b in product(range(4), repeat=2)})


def verify(name: str, weights: dict[int, int], t: int) -> dict:
    units = [tuple(a for a in range(4) if mask >> a & 1)
             for mask, w in weights.items() for _ in range(w*t)]

    def finish(h=()):
        while len(h) < 3:
            h += (ACTIONS[h],)
        return h

    def payoff(z, i):
        return sum((F(1, sum(a in likes for a in z))
                    for likes in units if z[i] in likes), F(0))

    def potential(z):
        return sum((sum((F(1, j) for j in range(1, sum(a in likes for a in z)+1)), F(0))
                    for likes in units), F(0))

    def welfare(z):
        return sum(any(a in likes for a in z) for likes in units)

    rows = []
    for length in range(3):
        for h in product(range(4), repeat=length):
            vals = [payoff(finish(h+(a,)), length) for a in range(4)]
            assert vals[ACTIONS[h]] == max(vals)
            rows.append({'history': h, 'action': ACTIONS[h],
                         'true_deviation_payoffs': list(map(str, vals))})

    z = finish()
    zc = finish((z[-1],))
    assert z == (0, 1, 2) and zc == (2, 3, 2)
    regret = payoff(z, 0)-payoff(zc, 0)
    gap = potential(z)-potential(zc)
    assert regret == 0 and gap == t
    optimum = max(welfare(x) for x in product(range(4), repeat=3))
    assert welfare(z) == optimum == len(units)
    result = {'name': name, 'weights_by_mask_before_scaling': weights, 't': t,
              'unit_customers': len(units), 'players': 3, 'topics': 4,
              'ordered_histories': len(rows), 'IC_comparisons_including_self': 4*len(rows),
              'strategy_and_exact_payoffs': rows, 'actual_path': z, 'promoted_true_path': zc,
              'actual_payoffs': [str(payoff(z, i)) for i in range(3)],
              'promoted_payoffs': [str(payoff(zc, i)) for i in range(3)],
              'source_regret': str(regret), 'actual_potential': str(potential(z)),
              'promoted_potential': str(potential(zc)), 'potential_drop': str(gap),
              'W_actual': welfare(z), 'W_promoted': welfare(zc), 'OPT_3': optimum}
    if name == 'seven_customer_sharp_reset':
        assert potential(z) == 9*t and potential(zc) == 8*t
        assert tuple(payoff(z, i) for i in range(3)) == (2*t, 2*t, 3*t)
        assert tuple(payoff(zc, i) for i in range(3)) == (2*t, 2*t, 2*t)
        replay = finish((zc[0], z[0]))
        assert replay == (2, 0, 1)
        replay_slack = payoff(zc, 1)-payoff(replay, 1)
        assert replay_slack == 0
        deleted_old, deleted_new = (zc[0], zc[2]), (replay[0], replay[2])
        assert potential(deleted_old) == 6*t and potential(deleted_new) == 7*t
        reset = sum((F(1, (int(zc[0] in likes)+1)*(int(zc[0] in likes)+2))
                     for likes in units if zc[1] in likes and zc[2] not in likes), F(0))
        assert reset == gap == t
        result['sharp_reset'] = {'new_branch_exclusive_tax': str(reset),
                                'replay_path': replay, 'replay_middle_IC_slack': str(replay_slack),
                                'deleted_promoted_potential': str(potential(deleted_old)),
                                'deleted_replay_potential': str(potential(deleted_new))}
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--t', type=int, default=1)
    parser.add_argument('--output')
    args = parser.parse_args()
    assert args.t > 0
    result = {'status': 'exact_fixed_witness_passed',
              'scope': 'No finite multiple of source regret pays actual-last promotion reset; not HALF counterexample',
              'case': verify('seven_customer_sharp_reset', {1: 1, 4: 2, 6: 2, 11: 2}, args.t)}
    out = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.output:
        with Path(args.output).open('x') as handle:
            handle.write(out)
    print(out)
