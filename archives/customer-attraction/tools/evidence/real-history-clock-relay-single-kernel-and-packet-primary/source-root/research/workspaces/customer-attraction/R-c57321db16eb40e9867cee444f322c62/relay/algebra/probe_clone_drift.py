"""Exact complete-history witness for a zero-slack positive clone drift.

Two disjoint unit customers A,B and five providers.  This is an auxiliary
obstruction, not a half-coverage counterexample.
"""
from fractions import Fraction as F
from functools import cache
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
M = 5
FORCED_ACTION = {(): 0, (0,): 1}
FORCED_TARGET = {(0, 0): (2, 3)}


@cache
def possibilities(h):
    if len(h) == M:
        q = (h.count(0), h.count(1))
        return {q: None}
    children = [possibilities(h + (a,)) for a in range(2)]
    witnesses = {}
    for qa, qb in product(children[0], children[1]):
        targets = (qa, qb)
        values = (F(1, qa[0]), F(1, qb[1]))
        actions = [FORCED_ACTION[h]] if h in FORCED_ACTION else range(2)
        for a in actions:
            if values[a] < max(values):
                continue
            q = targets[a]
            if h in FORCED_TARGET and q != FORCED_TARGET[h]:
                continue
            witnesses.setdefault(q, (a, targets))
    return witnesses


def main():
    strategy = {}
    def materialize(h, target):
        if len(h) == M:
            assert target == (h.count(0), h.count(1))
            return
        action, children = possibilities(h)[target]
        strategy[h] = action
        for a in range(2):
            materialize(h + (a,), children[a])
    materialize((), (3, 2))
    def finish(h):
        while len(h) < M:
            h += (strategy[h],)
        return h
    def payoff(a, s):
        return F(1, s.count(a))
    rows = []
    for length in range(M):
        for h in product(range(2), repeat=length):
            a = strategy[h]
            leaf = finish(h)
            own = payoff(a, leaf)
            margins = []
            for b in range(2):
                alt = finish(h + (b,))
                margin = own - payoff(b, alt)
                assert margin >= 0
                margins.append(str(margin))
            rows.append(dict(history=''.join('AB'[a] for a in h),
                             action='AB'[a],
                             terminal=''.join('AB'[a] for a in leaf),
                             own=str(own), margins=margins))
    before, after = finish((0,)), finish((0, 0))
    old_share = payoff(0, before)
    new_share = payoff(0, after)
    mover_value = payoff(strategy[(0,)], before)
    slack = mover_value - new_share
    assert old_share == F(1, 3)
    assert new_share == mover_value == F(1, 2)
    assert slack == 0 and new_share - old_share == F(1, 6)
    result = dict(status='Auxiliary exact complete SPE, not a half counterexample',
                  customers=[dict(topics=['A'], multiplicity=1),
                             dict(topics=['B'], multiplicity=1)],
                  players=M, nodes=len(rows), comparisons=2*len(rows),
                  terminal=''.join('AB'[a] for a in finish(())),
                  W=2, OPT=2,
                  clone_history='A', before=''.join('AB'[a] for a in before),
                  clone_terminal=''.join('AB'[a] for a in after),
                  old_share=str(old_share), new_share=str(new_share),
                  mover_value=str(mover_value), clone_slack=str(slack),
                  drift=str(new_share-old_share), strategy=rows)
    (HERE/'clone_drift_witness.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'strategy'}, indent=2))


if __name__ == '__main__':
    main()
