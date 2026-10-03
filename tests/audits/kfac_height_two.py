#!/usr/bin/env python3
"""Independent exact finite audit of the height-two, unequal-edge witness.

This script uses only Fraction, product, and the model definitions. It does
not import a solver and does not prove the universal height-two theorem.
"""
from fractions import Fraction as F
from itertools import product
import json

SITES = ('H1', 'H2', 'M', 'L')
K = 10
# Preserve individual atoms, including the two different weights on H1--M.
CLIENTS = (
    (183, (0,)), (140, (1,)), (89, (2,)), (41, (3,)),
    (15, (0, 2)), (1, (0, 2)), (13, (1, 2)), (6, (2, 3)),
)


def greedy():
    q = [0] * len(SITES)
    totals = [F(0)] * len(SITES)
    assigned = [-1] * len(CLIENTS)
    opened = {}
    history = []
    for step in range(K):
        scores = []
        for t in range(len(SITES)):
            if q[t]:
                score = totals[t] / (q[t] + 1)
            else:
                score = sum((F(w) for i, (w, opts) in enumerate(CLIENTS)
                             if assigned[i] < 0 and t in opts), F(0))
            scores.append(score)
        maximum = max(scores)
        winners = [t for t, score in enumerate(scores) if score == maximum]
        assert len(winners) == 1, ('unexpected greedy tie', step, scores)
        t = winners[0]
        if not q[t]:
            opened[t] = step
            for i, (w, opts) in enumerate(CLIENTS):
                if assigned[i] < 0 and t in opts:
                    assigned[i] = t
                    totals[t] += w
        q[t] += 1
        history.append((t, maximum))
    return tuple(q), tuple(totals), tuple(assigned), opened, history


def totals_for(assigned):
    totals = [F(0)] * len(SITES)
    for (w, opts), t in zip(CLIENTS, assigned):
        assert t in opts
        totals[t] += w
    return tuple(totals)


def is_ne(assigned, q):
    totals = totals_for(assigned)
    return all((totals[t] - w) / q[t] <= totals[v] / q[v]
               for (w, opts), t in zip(CLIENTS, assigned)
               for v in opts if v != t)


def potential(assigned, q):
    totals = totals_for(assigned)
    squares = [F(0)] * len(SITES)
    for (w, opts), t in zip(CLIENTS, assigned):
        squares[t] += w * w
    return sum(((totals[t] ** 2 - squares[t]) / (2 * q[t])
                for t in range(len(SITES))), F(0))


def lpt(weights, bins):
    loads = [F(0)] * bins
    for w in sorted(weights, reverse=True):
        t = min(range(bins), key=lambda b: (loads[b], b))
        loads[t] += w
    return tuple(loads)


def main():
    q, initial, origins, opened, history = greedy()
    gamma = history[-1][1]
    assert q == (4, 3, 2, 1)
    assert gamma == 41
    assert initial == (199, 153, 95, 41)
    assert [t for t, score in history] == [0, 1, 0, 2, 1, 0, 1, 0, 2, 3]
    assert [score for t, score in history] == list(map(F, (
        199, 153, F(199, 2), 95, F(153, 2), F(199, 3),
        51, F(199, 4), F(95, 2), 41)))
    assert all(q[t] * gamma <= initial[t] <= (q[t] + 1) * gamma
               for t in range(len(SITES)))
    assert all(q[origins[i]] >= q[t]
               for i, (w, opts) in enumerate(CLIENTS) for t in opts)

    variable = [i for i, (w, opts) in enumerate(CLIENTS)
                if len(opts) > 1 and w < gamma]
    assert variable == [4, 5, 6, 7]
    edges = {}
    for i in variable:
        w, opts = CLIENTS[i]
        assert len(opts) == 2
        u, v = sorted(opts, key=lambda t: opened[t])
        assert origins[i] == u
        edges.setdefault((u, v), []).append(w)
    assert set(edges) == {(0, 2), (1, 2), (2, 3)}
    incoming = {t: [] for t in range(len(SITES))}
    outgoing = {t: [] for t in range(len(SITES))}
    for u, v in edges:
        incoming[v].append(u)
        outgoing[u].append(v)
    depth = {}
    for t in sorted(range(len(SITES)), key=lambda t: opened[t]):
        depth[t] = max((depth[u] + 1 for u in incoming[t]), default=0)
    assert max(depth.values()) == 2
    assert all(not incoming[h]
               for u in outgoing if outgoing[u] for h in incoming[u])

    # Exclude older sufficient classes and the new polynomial path rule.
    assert len(set(q)) > 1             # not constant multiplicity
    assert len(SITES) > 2              # not a two-site component
    assert all(len(CLIENTS[i][1]) != len(SITES) for i in variable)
    assert not all(0 in CLIENTS[i][1] for i in variable)  # no first anchor
    assert len({CLIENTS[i][0] for i in variable}) > 1    # not uniform light
    assert len(incoming[2]) == 2                        # not directed path
    assert len(set(edges[(0, 2)])) == 2                 # not edge uniform
    undirected_degree = {t: len(incoming[t]) + len(outgoing[t]) for t in incoming}
    center = next(t for t, degree in undirected_degree.items() if degree == 3)
    assert center == 2
    assert not all(opened[center] < opened[t] for t in opened if t != center)
    # RANGE is violated by both the weight-one H1--M and weight-six M--L.
    assert (initial[0] - 1) / q[0] > initial[2] / q[2]
    assert (initial[2] - 6) / q[2] > initial[3] / q[3]
    pools = [[w for i, (w, opts) in enumerate(CLIENTS) if origins[i] == t]
             for t in range(len(SITES))]
    first_lpt = [lpt(pools[t], q[t]) for t in range(len(SITES))]
    assert min(first_lpt[0]) == 0 < gamma  # not DOUBLE-LPT recognized

    rows = []
    for choices in product(*(CLIENTS[i][1] for i in variable)):
        assigned = list(origins)
        for i, t in zip(variable, choices):
            assigned[i] = t
        totals = totals_for(assigned)
        box = all(q[t] * gamma <= totals[t] <= (q[t] + 1) * gamma
                  for t in range(len(SITES)))
        rows.append((potential(assigned, q), tuple(assigned), totals,
                     box, is_ne(assigned, q)))
    assert len(rows) == 16
    boxed = [row for row in rows if row[3]]
    assert len(boxed) == 15
    minimum = min(row[0] for row in boxed)
    minimizers = [row for row in boxed if row[0] == minimum]
    assert len(minimizers) == 1
    winner = minimizers[0]
    assert minimum == F(6241, 4)
    assert winner[1] == (0, 1, 2, 3, 0, 0, 2, 3)
    assert winner[2] == (199, 140, 102, 47)
    assert winner[4]
    assert all(row[4] for row in minimizers)
    assert sum(row[4] for row in boxed) == 2

    print(json.dumps({
        'status': 'exact finite audit passed',
        'greedy': [(SITES[t], str(score)) for t, score in history],
        'multiplicities': q, 'gamma': str(gamma),
        'assignments': len(rows), 'boxed_assignments': len(boxed),
        'boxed_nes': sum(row[4] for row in boxed),
        'unique_box_potential_minimum': str(minimum),
        'minimum_site_totals': [str(x) for x in winner[2]],
        'excluded': ['RANGE', 'constant-multiplicity', 'two-site',
                     'ALL-OR-ONE', 'NESTED-ANCHOR', 'UNIFORM-LIGHT',
                     'STAR-LIGHT', 'PATH-EDGE-LIGHT', 'DOUBLE-LPT'],
        'scope': 'one finite witness; not the universal height-two proof',
    }, indent=2))


if __name__ == '__main__':
    main()
