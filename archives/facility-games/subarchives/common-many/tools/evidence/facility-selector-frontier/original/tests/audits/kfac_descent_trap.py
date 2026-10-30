"""Exact audit of the forced three-site downward-only repair trap.

Run: python3 tests/audits/kfac_descent_trap.py
The finite obstruction and its limits are proved in polytime_frontier.md.
"""

import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / 'examples/multi_facility/greedy_descent_trap.json').read_text())
SITES = DATA['sites']
WEIGHT = [F(c['weight']) for c in DATA['clients']]
ACCESS = [set(c['sites']) for c in DATA['clients']]


def totals(a):
    return {s: sum((WEIGHT[i] for i, t in enumerate(a) if t == s), F(0))
            for s in SITES}


def greedy():
    q = {s: 0 for s in SITES}
    a = [None] * len(WEIGHT)
    trace = []
    for _ in range(DATA['k']):
        w = totals(a)
        scores = {s: w[s] / (q[s] + 1) if q[s] else
                  sum((WEIGHT[i] for i in range(len(a))
                       if a[i] is None and s in ACCESS[i]), F(0))
                  for s in SITES}
        selected = max(SITES, key=lambda s: scores[s])
        assert sum(value == scores[selected] for value in scores.values()) == 1
        trace.append((selected, scores[selected]))
        if not q[selected]:
            for i in range(len(a)):
                if a[i] is None and selected in ACCESS[i]:
                    a[i] = selected
        q[selected] += 1
    return q, a, trace


def improvements(a, q, downward_only):
    w = totals(a)
    return [(i, old, new, (w[old] - WEIGHT[i]) / q[old], w[new] / q[new])
            for i, old in enumerate(a) if old is not None
            for new in SITES if new != old and q[new] and new in ACCESS[i]
            and (not downward_only or q[new] <= q[old])
            and (w[old] - WEIGHT[i]) / q[old] > w[new] / q[new]]


def audit():
    q, a, trace = greedy()
    assert trace == [('H', F(73)), ('M', F(44)), ('H', F(73, 2)),
                     ('H', F(73, 3)), ('M', F(22)), ('L', F(20))]
    assert [q[s] for s in SITES] == [3, 2, 1]
    assert [totals(a)[s] for s in SITES] == [73, 44, 20]
    expected = [(4, 'M', 'L', [73, 42, 22]),
                (1, 'H', 'M', [64, 51, 22]),
                (3, 'M', 'L', [64, 46, 27])]
    for i, old, new, loads in expected:
        moves = improvements(a, q, True)
        assert len(moves) == 1 and moves[0][:3] == (i, old, new)
        a[i] = new
        assert [totals(a)[s] for s in SITES] == loads
        assert all(q[s] * 20 <= totals(a)[s] <= (q[s] + 1) * 20
                   for s in SITES)
    assert improvements(a, q, True) == []
    assert improvements(a, q, False) == [(4, 'L', 'M', F(25), F(23))]
    a[4] = 'M'
    assert [totals(a)[s] for s in SITES] == [64, 48, 25]
    assert improvements(a, q, False) == []
    print('PASS: tie-free greedy, unique downhill path, forced uphill return, exact NE')


if __name__ == '__main__':
    audit()
