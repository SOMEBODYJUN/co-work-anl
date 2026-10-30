"""Parent reconstruction using expanded distinct unit customers.

Does not import the author's audit. The finite cases audit a general analytic
template obstruction; they are not SPE counterexamples to Q-CAG-HALF.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json


def instance(k, m):
    blocks = [set(range(m-k))]
    cursor = m-k
    for _ in range(m):
        blocks.append(set(range(cursor, cursor+k+1)))
        cursor += k+1
    assert sum(map(len, blocks)) == len(set.union(*blocks))
    return blocks


def payoff(blocks, history, player):
    return sum((F(1, sum(x in blocks[a] for a in history))
                for x in blocks[history[player]]), F())


def policy(blocks, history):
    return next(a for a in range(1, len(blocks)) if a not in history)


def finish(blocks, m, history):
    history = list(history)
    while len(history) < m:
        history.append(policy(blocks, history))
    return tuple(history)


def check(k, m, full_tail):
    blocks = instance(k, m)
    n = m-k
    actual = (0,)*n+tuple(range(1, k+1))
    welfare = len(set.union(*(blocks[a] for a in actual)))
    optimum = max(len(set.union(*(blocks[a] for a in subset)))
                  for subset in combinations(range(m+1), m))
    assert welfare == m+k*k
    assert optimum == (k+2)*m-2*k-1
    assert optimum-2*welfare == k*(m-2*k-2)-1
    early_rows = 0
    for player in range(n):
        value = payoff(blocks, actual, player)
        assert value == 1
        for topic in range(m+1):
            bound = sum((F(1, sum(x in blocks[a] for a in actual[:player])+m-player)
                         for x in blocks[topic]), F())
            assert value >= bound
            early_rows += 1
    tail_rows = 0
    if full_tail:
        for depth in range(k):
            for suffix in product(range(m+1), repeat=depth):
                history = (0,)*n+suffix
                chosen = policy(blocks, history)
                terminal = finish(blocks, m, history+(chosen,))
                value = payoff(blocks, terminal, len(history))
                assert value == k+1
                for topic in range(m+1):
                    changed = finish(blocks, m, history+(topic,))
                    assert value >= payoff(blocks, changed, len(history))
                    tail_rows += 1
    # A genuine early deviation, deliberately absent from the weak template.
    changed = finish(blocks, m, (0,)*(n-1)+(1,))
    assert payoff(blocks, changed, n-1) == k+1 > payoff(blocks, actual, n-1)
    return dict(k=k, m=m, customers=len(set.union(*blocks)), W=welfare,
                OPT=optimum, early_rows=early_rows, tail_rows=tail_rows)


def main():
    cases = [check(k, m, k <= 3 and m <= 10)
             for k in range(1, 6) for m in range(2*k+1, 2*k+8)]
    # A growing tail can also fail; no fixed-k asymptotic is needed here.
    for k in range(1, 101):
        m=2*k+4
        assert ((k+2)*m-2*k-1)-2*(m+k*k) == 2*k-1 > 0
    report = dict(status='independent finite audit passed',
                  general_proof='analytic in bounded_suffix_security_obstruction.md',
                  main_target='OPEN; these paths fail early SPE optimality',
                  cases=cases, tail_rows=sum(c['tail_rows'] for c in cases),
                  early_rows=sum(c['early_rows'] for c in cases))
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='cases'}))


if __name__ == '__main__':
    main()
