#!/usr/bin/env python3
"""Exact finite checks of the resource-minimum flat-menu bridge.

This does not implement the imported restricted Santa Claus algorithm.  It
independently enumerates ordinary schedules and item ownership on small inputs.
Run from the repository root; JSON is written to stdout, never to frozen runs.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import random


def normalize(groups):
    """Preserve zero incidences; add a distinct bonus resource to each short row."""
    u = max((len(row) for group in groups for row in group), default=0)
    out = [[list(row) + [F(0)] * (u-len(row)) for row in group]
           for group in groups]
    for g, group in enumerate(groups):
        for s, row in enumerate(group):
            w = sum(row, F(0))
            assert 0 <= w <= 1
            if w < 1:
                for gg in out:
                    for rr in gg:
                        rr.append(F(0))
                out[g][s][-1] = 1-w
    return out


def envelope(groups):
    u = len(groups[0][0])
    low, kappa = [], F(1)
    for j in range(u):
        positive = [row[j] for group in groups for row in group if row[j] > 0]
        low.append(min(positive) if positive else F(0))
        if positive:
            kappa = max(kappa, max(positive)/min(positive))
    restricted = [[[low[j] if v > 0 else F(0) for j, v in enumerate(row)]
                   for row in group] for group in groups]
    return restricted, kappa


def menu_value(groups):
    """Enumerate a single owner per resource and choose one state per group."""
    u = len(groups[0][0])
    value = F(0)
    for owners in product(range(-1, len(groups)), repeat=u):
        utilities = [max(sum((v for j, v in enumerate(row) if owners[j] == g), F(0))
                         for row in group) for g, group in enumerate(groups)]
        value = max(value, min(utilities))
    return value


def sc_value(groups):
    """Enumerate state-agent item allocations, including all unit dummies."""
    agents = [(g, s) for g, group in enumerate(groups) for s in range(len(group))]
    u = len(groups[0][0])
    items = [[groups[g][s][j] for g, s in agents] for j in range(u)]
    for g, group in enumerate(groups):
        for _ in range(len(group)-1):
            items.append([F(gg == g) for gg, _ in agents])
    best = F(0)
    for owners in product(range(len(agents)), repeat=len(items)):
        utilities = [F(0)] * len(agents)
        for vals, owner in zip(items, owners):
            utilities[owner] += vals[owner]
        best = max(best, min(utilities))
    return best


def ordinary_opt(groups):
    """Build all original jobs and enumerate their actual machine choices."""
    states = [(g, s) for g, group in enumerate(groups) for s in range(len(group))]
    private = {gs: i for i, gs in enumerate(states)}
    u = len(groups[0][0])
    jobs = [[(private[g, s], F(1)) for s in range(len(group))]
            for g, group in enumerate(groups)]
    for g, s in states:
        for j, v in enumerate(groups[g][s]):
            jobs.append([(private[g, s], v), (len(states)+j, F(1))])
    optimum = None
    for assignment in product(*jobs):
        loads = [F(0)] * (len(states)+u)
        for machine, p in assignment:
            loads[machine] += p
        value = max(loads)
        if optimum is None or value < optimum:
            optimum = value
    return optimum


def check(groups, direct):
    assert groups and all(group for group in groups)
    norm = normalize(groups)
    original_u = len(groups[0][0])
    reduced, k = envelope(norm)
    v, vlow = menu_value(norm), menu_value(reduced)
    assert v/k <= vlow <= v <= 1
    assert sc_value(reduced) == vlow
    if direct:
        old = ordinary_opt(groups)
        # Explicitly materializing bonus zero incidences multiplies enumeration.
        # Cases with few states use an independent original-matrix oracle.
        assert old == 2-v
        if len(norm[0][0]) == original_u:
            assert ordinary_opt(norm) == old
    for alpha in (F(7), F(13, 2), F(601, 100)):
        c = 2-v/(alpha*k)
        ratio = 2-1/(alpha*k)
        o = 2-v
        assert ratio*o-c == 2*(1-1/(alpha*k))*(1-v) >= 0
    return k


def main():
    rows = [(F(1), F(0)), (F(0), F(1)), (F(1, 2), F(1, 2)),
            (F(1, 4), F(3, 4)), (F(3, 4), F(1, 4))]
    cases = direct = 0
    kappas = set()
    for k0, k1 in ((1, 1), (1, 2), (2, 1), (2, 2)):
        for selected in product(rows, repeat=k0+k1):
            q = [list(selected[:k0]), list(selected[k0:])]
            kappas.add(check(q, True))
            cases += 1
            direct += 1
    # Non-normalized rows, empty positive supports, rational distortion,
    # duplicate states and an unused all-zero resource.
    boundary = [
        [[(F(0), F(0))]],
        [[(F(0), F(0)), (F(0), F(0))]],
        [[(F(1, 2), F(0))], [(F(0), F(1, 3))]],
        [[(F(1, 2), F(1, 4)), (F(1, 2), F(1, 4))]],
        [[(F(1, 10**30), F(1)-F(1, 10**30))], [(F(1), F(0))]],
    ]
    for q in boundary:
        kappas.add(check(q, True))
        cases += 1
        direct += 1
    rng = random.Random(210721)
    for _ in range(40):
        q = []
        for _ in range(2):
            a = rng.randrange(5)
            b = rng.randrange(5-a)
            q.append([((F(a, 4)), F(b, 4))])
        kappas.add(check(q, True))
        cases += 1
        direct += 1
    print(json.dumps({
        'status': 'passed', 'arithmetic': 'fractions.Fraction; exhaustive ownership',
        'seed': 210721, 'cases': cases, 'ordinary_matrix_cases': direct,
        'kappa_values': sorted(map(str, kappas)),
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'not_checked': ['restricted Santa backend implementation',
                        'all rational matrices', 'general unrelated machines',
                        'NP hardness or the negation of UM-TARGET-v1'],
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
