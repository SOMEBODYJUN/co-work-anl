"""Independent exact check; no canonical model or equilibrium solver imports."""
from fractions import Fraction as F
from itertools import product
import json


def check_identity(b, samples):
    # samples are probability, membership, total remaining load.
    t = sum(p*i for p, i, c in samples)
    load = sum(p*c for p, i, c in samples)
    center = b+1+load
    direct = sum(p*F(i, b+c) for p, i, c in samples if i)
    pushed = t/center
    cov = sum(p*i*c for p, i, c in samples)-t*load
    jensen = sum(p*i*(b+c-center)**2/F(b+c)
                 for p, i, c in samples if i)
    assert direct-pushed == (t-cov+jensen)/center**2
    return direct, pushed


def utility(action, other):
    return sum((F(1, 1+(x in other)) for x in action), F(0))


def run():
    checks = 0
    for b, c0, c1, i0, i1, numerator in product(
            range(4), range(6), range(6), range(2), range(2), range(1, 8)):
        if (i0 and not c0) or (i1 and not c1):
            continue
        p = F(numerator, 8)
        direct, pushed = check_identity(
            b, [(p, i0, c0), (1-p, i1, c1)])
        if max(c0, c1)-min(c0, c1) <= 1:
            assert direct >= pushed
        checks += 1

    topics = [set('x') | {'z1', 'z2'}, {'y1', 'y2', 'y3'},
              {'x', 'y1', 'y2', 'y3'}, {'z1', 'z2', 'w1', 'w2'}]
    replies = [2, 3, 3, 2]
    last_table = [[utility(topic, first) for topic in topics]
                  for first in topics]
    for a, reply in enumerate(replies):
        assert last_table[a][reply] == max(last_table[a])
        assert sum(v == max(last_table[a]) for v in last_table[a]) == 1
    root_values = [utility(topics[a], topics[reply])
                   for a, reply in enumerate(replies)]
    assert root_values[2] == max(root_values)
    welfare = len(topics[2] | topics[3])
    optimum = max(len(a | b) for a in topics for b in topics)
    assert welfare == optimum == 8
    customers = set().union(*topics)
    direct = pushed = F(0)
    for x in customers:
        samples = []
        for probability, query in [(F(1, 4), 0), (F(3, 4), 1)]:
            total = int(x in topics[query]) + int(x in topics[replies[query]])
            samples.append((probability, int(x in topics[query]), total))
        dx, fx = check_identity(0, samples)
        direct += dx
        pushed += fx
        if x == 'x':
            assert dx == F(1, 8) and fx == F(1, 6)
    assert direct == F(23, 8)
    assert pushed == F(37, 24)
    return {'identity_checks': checks,
            'last_payoffs': [[str(v) for v in row] for row in last_table],
            'root_payoffs': list(map(str, root_values)),
            'welfare': welfare, 'optimum': optimum,
            'D': str(direct), 'F': str(pushed),
            'D_minus_F': str(direct-pushed)}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
