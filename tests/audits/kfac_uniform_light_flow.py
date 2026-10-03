"""Exact finite audit of the uniform-light chain and its flow objective.

Run: python3 tests/audits/kfac_uniform_light_flow.py
Finite enumeration of two clients checks only this instance, not the theorem.
"""

import itertools
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / 'examples/multi_facility/greedy_uniform_light_flow.json').read_text())
SITES = DATA['sites']
WEIGHT = [F(row['weight']) for row in DATA['clients']]
ACCESS = [set(row['sites']) for row in DATA['clients']]


def totals(assignment):
    return {s: sum((WEIGHT[i] for i, v in enumerate(assignment) if v == s), F(0))
            for s in SITES}


def greedy():
    q = {s: 0 for s in SITES}
    a = [None] * len(WEIGHT)
    trace = []
    for _ in range(DATA['k']):
        w = totals(a)
        scores = {s: w[s] / (q[s] + 1) if q[s] else
                  sum((WEIGHT[i] for i, v in enumerate(a)
                       if v is None and s in ACCESS[i]), F(0))
                  for s in SITES}
        s = max(SITES, key=lambda v: scores[v])
        assert list(scores.values()).count(scores[s]) == 1
        trace.append((s, scores[s]))
        if not q[s]:
            for i, v in enumerate(a):
                if v is None and s in ACCESS[i]:
                    a[i] = s
        q[s] += 1
    return q, a, trace


def flow_objective(assignment, q):
    base = {'H': F(140), 'M': F(80), 'L': F(41)}
    count = {s: sum(assignment[i] == s for i in (3, 4)) for s in SITES}
    delta = F(10)
    return sum((base[s] * count[s] / q[s] +
                delta * count[s] * (count[s] - 1) / (2 * q[s]) for s in SITES), F(0))


def ne(assignment, q):
    w = totals(assignment)
    return all((w[assignment[i]] - WEIGHT[i]) / q[assignment[i]] <= w[t] / q[t]
               for i in range(len(WEIGHT)) for t in ACCESS[i] if t != assignment[i])


def audit():
    q, initial, trace = greedy()
    assert trace == [('H', F(150)), ('M', F(90)), ('H', F(75)),
                     ('H', F(50)), ('M', F(45)), ('L', F(41))]
    assert [q[s] for s in SITES] == [3, 2, 1]
    assert initial == ['H', 'M', 'L', 'H', 'M']
    gamma = trace[-1][1]
    feasible = []
    for h, m in itertools.product(sorted(ACCESS[3]), sorted(ACCESS[4])):
        a = ['H', 'M', 'L', h, m]
        w = totals(a)
        if all(w[s] >= q[s] * gamma for s in SITES):
            feasible.append((flow_objective(a, q), a))
    minimum = min(value for value, _ in feasible)
    optima = [a for value, a in feasible if value == minimum]
    assert optima == [['H', 'M', 'L', 'M', 'L']]
    assert [totals(optima[0])[s] for s in SITES] == [140, 90, 51]
    assert ne(optima[0], q)
    assert all(q[s] * gamma <= totals(optima[0])[s] <= (q[s] + 1) * gamma
               for s in SITES)
    assert F(140, 3) > F(45)  # Old RANGE condition fails on HM weight 10.
    print('PASS: strict greedy, lower-constrained potential minimum, box, exact NE')


if __name__ == '__main__':
    audit()
