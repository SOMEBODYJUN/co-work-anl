"""Exact finite audit of the greedy fixed-layout potential-selection obstruction.

Run: python3 tests/audits/kfac_greedy_potential.py
The universal mixed-off-path forcing and the two-NE classification are proved
in research/current/multi_facility/polytime_frontier.md.
"""

import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads(
    (ROOT / "examples/multi_facility/greedy_potential_escape.json").read_text()
)
SITES = DATA["sites"]
W = [F(c["weight"]) for c in DATA["clients"]]
ACCESS = [set(c["sites"]) for c in DATA["clients"]]


def totals(assignment):
    return {s: sum((W[i] for i, t in enumerate(assignment) if t == s), F(0))
            for s in SITES}


def greedy():
    q = {s: 0 for s in SITES}
    assignment = [None] * len(W)
    trace = []
    for _ in range(DATA["k"]):
        t = totals(assignment)
        scores = {
            s: t[s] / (q[s] + 1) if q[s] else
            sum((W[i] for i in range(len(W))
                 if assignment[i] is None and s in ACCESS[i]), F(0))
            for s in SITES
        }
        site = max(SITES, key=lambda s: scores[s])
        trace.append((site, scores[site]))
        if q[site] == 0:
            for i in range(len(W)):
                if assignment[i] is None and site in ACCESS[i]:
                    assignment[i] = site
        q[site] += 1
    return q, assignment, trace


def potential(assignment, q):
    t = totals(assignment)
    return sum(((t[s] ** 2 - sum((W[i] ** 2 for i, home in enumerate(assignment)
                                   if home == s), F(0))) / (2 * q[s])
                for s in SITES if q[s]), F(0))


def is_ne(assignment, q):
    t = totals(assignment)
    for i, home in enumerate(assignment):
        choices = [s for s in SITES if q[s] and s in ACCESS[i]]
        if not choices:
            if home is not None:
                return False
            continue
        if home not in choices or any(
                (t[home] - W[i]) / q[home] > t[s] / q[s]
                for s in choices if s != home):
            return False
    return True


def audit():
    q, initial, trace = greedy()
    assert trace == [("D", F(800)), ("B", F(599)), ("D", F(400)),
                     ("C", F(398)), ("B", F(599, 2)), ("D", F(800, 3)),
                     ("A", F(200)), ("E", F(200))]
    assert [q[s] for s in SITES] == [1, 1, 2, 1, 3, 0]
    assert [totals(initial)[s] for s in SITES] == [200, 200, 599, 398, 800, 0]
    shared = [1, 2, 4, 6]
    feasible = []
    for choices in product(*[[s for s in SITES if q[s] and s in ACCESS[i]]
                             for i in shared]):
        assignment = initial.copy()
        for i, site in zip(shared, choices):
            assignment[i] = site
        t = totals(assignment)
        minimum = min(t[s] / q[s] for s in SITES if q[s])
        feasible.append((choices, assignment, potential(assignment, q),
                         minimum, is_ne(assignment, q)))
    assert len(feasible) == 16
    equilibria = [(choice, p) for choice, _, p, _, ne in feasible if ne]
    assert set(equilibria) == {(('B', 'B', 'A', 'D'), F(86264)),
                               (('B', 'E', 'A', 'B'), F(86200))}
    assert [row[0] for row in feasible if row[2] == min(x[2] for x in feasible)] == [
        ('B', 'E', 'A', 'B')]
    assert [row[0] for row in feasible if row[3] == max(x[3] for x in feasible)] == [
        ('B', 'E', 'A', 'B')]
    good = next(a for choice, a, _, _, _ in feasible if choice == ('B', 'B', 'A', 'D'))
    t = totals(good)
    assert all(q[s] * 200 <= t[s] <= (q[s] + 1) * 200
               for s in SITES if q[s])
    assert t['C'] + W[4] <= 2 * t['A']
    assert W[9] <= 200
    bad = next(a for choice, a, _, _, _ in feasible if choice == ('B', 'E', 'A', 'B'))
    assert totals(bad)['B'] / 2 == 214
    assert ACCESS[2] == {'B', 'E', 'G'}
    assert {i for i, acc in enumerate(ACCESS) if 'G' in acc} == {2, 9}
    assert W[9] == 199 < W[8] == 200 < W[3] == 240
    assert (W[2] + W[9]) / (totals(bad)['B'] / 2) == F(215, 107) > 2
    print('PASS: greedy trace, all 16 assignments, unique potential and lexmax bad NE')


if __name__ == '__main__':
    audit()
