"""Exact full ordered-tree completion for the I2/I3 six-player family.

Every decision node independently compares 8 real children. We cache only
terminal payoffs by counts. No count-based assumption is made on a strategy.
"""
from functools import cache
from itertools import combinations_with_replacement
from math import lcm

ACTIONS = ('H', 'P', 'Q', 'R', 'D1', 'D2', 'D3', 'D4')
NUM = len(ACTIONS)
PLAYERS = 6
SCALE = lcm(*range(1, PLAYERS + 1))
PATH = (4, 5, 6, 7, 0, 2)


def verify(mass):
    groups = [
        ((2,), mass - 3),
        ((1, 2), 6),
        ((3,), 2),
        ((0, 1, 3), 2 * mass),
        ((2, 3), 4),
    ]
    groups += [((a,), 2 * mass + 7) for a in range(4, 8)]

    @cache
    def terminal(counts):
        values = [0] * NUM
        coverage = 0
        for labels, customers in groups:
            load = sum(counts[a] for a in labels)
            if not load:
                continue
            coverage += customers
            for a in labels:
                if counts[a]:
                    values[a] += customers * (SCALE // load)
        return tuple(values), coverage

    nodes = [0] * (PLAYERS + 1)
    def induce(prefix):
        depth = len(prefix)
        nodes[depth] += 1
        if depth == PLAYERS:
            counts = tuple(prefix.count(a) for a in range(NUM))
            return terminal(counts)
        children = [induce(prefix+(a,)) for a in range(NUM)]
        rates = [pays[a] for a, (pays, _) in enumerate(children)]
        best = max(rates)
        action = PATH[depth] if prefix == PATH[:depth] else rates.index(best)
        assert rates[action] == best, (prefix, action, rates)
        if depth == 4 and prefix == PATH[:4]:
            expected = [2 * mass, mass + 6, mass + 5, mass + 6]
            assert rates[:4] == [x*SCALE for x in expected] and rates.count(best) == 1
        if prefix[:4] == PATH[:4] and depth == 5 and prefix[4] < 4:
            assert rates.index(best) == (2, 3, 3, 1)[prefix[4]] and rates.count(best) == 1
        return children[action]

    _, achieved = induce(())
    all_counts = (tuple(seq.count(a) for a in range(NUM))
                  for seq in combinations_with_replacement(range(NUM), PLAYERS))
    optimum = max(terminal(counts)[1] for counts in all_counts)
    assert achieved == 4*(2*mass+7) + 3*mass + 7
    assert optimum == 4*(2*mass+7) + 3*mass + 9
    assert nodes == [NUM**depth for depth in range(PLAYERS+1)]
    print(f'M={mass} nodes={nodes} W={achieved} OPT6={optimum} '
          f'penultimate_H={2*mass} deviation_P={mass+6} '
          f'pair_HQ={3*mass+7} pair_PR={2*mass+12}')


if __name__ == '__main__':
    for mass in (7, 101):
        verify(mass)
