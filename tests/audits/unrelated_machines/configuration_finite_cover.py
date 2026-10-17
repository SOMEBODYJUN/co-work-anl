#!/usr/bin/env python3
"""配置证书到真实有限覆盖调度：精确、输出敏感构造及有限核验。

None 表示不可用；仅接收 int/Fraction，拒绝 bool/float。
没有配置 LP 求解器，没有困难性归约或相对原输入的多项式阶数承诺。
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from math import lcm
import hashlib
import json
from pathlib import Path
import random
import sys


def rational(x):
    if type(x) is int or type(x) is F:
        if x >= 0:
            return F(x)
    raise ValueError('expected nonnegative exact rational')


def matrix(p):
    if not p or any(len(row) != len(p[0]) for row in p):
        raise ValueError('nonempty rectangular machine matrix required')
    p = [[None if v is None else rational(v) for v in row] for row in p]
    if any(all(row[j] is None for row in p) for j in range(len(p[0]))):
        raise ValueError('job has no finite machine')
    return p


def realize(p, y, target):
    """y[i] is [(tuple_of_original_job_indices, exact_weight), ...].

    Return incidence permutations job-copy -> machine-copy and an actual
    assignment (flattened indices i*q+b). Runtime is polynomial in explicit
    output size and supplied certificate length; q may be exponentially large.
    """
    p = matrix(p)
    T = rational(target)
    m, n = len(p), len(p[0])
    if len(y) != m:
        raise ValueError('one configuration distribution per machine')
    clean, coverage, q = [], [F(0)] * n, 1
    for i, distribution in enumerate(y):
        row, mass = [], F(0)
        for config, weight in distribution:
            w = rational(weight)
            C = tuple(config)
            if any(type(j) is not int or not 0 <= j < n for j in C):
                raise ValueError('invalid job index')
            if len(C) != len(set(C)) or any(p[i][j] is None for j in C):
                raise ValueError('configuration is not a finite-edge subset')
            if sum((p[i][j] for j in C), F(0)) > T:
                raise ValueError('configuration exceeds target')
            mass += w
            for j in C:
                coverage[j] += w
            if w:
                row.append((tuple(sorted(C)), w))
                q = lcm(q, w.denominator)
        if mass != 1:
            raise ValueError('machine distribution mass is not one')
        clean.append(row)
    if any(v != 1 for v in coverage):
        raise ValueError('job coverage is not exactly one')
    configs, sockets = [], [[] for _ in range(n)]
    for i, row in enumerate(clean):
        copies = [C for C, w in row for _ in range(int(q*w))]
        assert len(copies) == q
        configs.append(copies)
        for b, C in enumerate(copies):
            for j in C:
                sockets[j].append((i, b))
    permutations = {(i, j): [-1]*q for i in range(m)
                    for j in range(n) if p[i][j] is not None}
    sigma = [-1] * (n*q)
    for j, positions in enumerate(sockets):
        assert len(positions) == q
        for a, (i, b) in enumerate(positions):
            permutations[i, j][a] = b
            sigma[j*q+a] = i*q+b
        for i in range(m):
            if (i, j) not in permutations:
                continue
            perm = permutations[i, j]
            missing = iter(sorted(set(range(q))-set(perm)))
            for a in range(q):
                if perm[a] < 0:
                    perm[a] = next(missing)
            assert sorted(perm) == list(range(q))
    loads = [F(0)] * (m*q)
    for ja, ib in enumerate(sigma):
        j, a = divmod(ja, q)
        i, b = divmod(ib, q)
        assert permutations[i, j][a] == b
        loads[ib] += p[i][j]
    assert max(loads, default=F(0)) <= T
    return {'q': q, 'permutations': permutations, 'sigma': sigma,
            'loads': loads, 'configs': configs}


def fixture():
    p = [[None]*7 for _ in range(4)]
    p[0][0] = p[1][0] = F(1)
    y = [None]*4
    for root, terminal, jobs in [(0, 2, (1, 2, 3)), (1, 3, (4, 5, 6))]:
        for j in jobs:
            p[root][j], p[terminal][j] = F(1, 3), F(1)
        y[root] = [(jobs, F(1, 2))] + [((0, j), F(1, 6)) for j in jobs]
        y[terminal] = [((j,), F(1, 3)) for j in jobs]
    return p, y, F(4, 3)


def serial_fixture():
    p, y, T = fixture()
    return {'machines': ['A', 'B', 'a', 'b'],
            'jobs': ['c', 'A0', 'A1', 'A2', 'B0', 'B1', 'B2'],
            'p': [[None if v is None else str(v) for v in row] for row in p],
            'T': str(T), 'configuration':
            [[{'jobs': list(C), 'weight': str(w)} for C, w in row] for row in y]}


def serial_witness():
    p, y, T = fixture()
    out = realize(p, y, T)
    return {'q': out['q'], 'target': str(T), 'sigma': out['sigma'],
            'loads': [str(v) for v in out['loads']],
            'permutations': [{'machine': i, 'job': j, 'job_to_machine_copy': perm}
                             for (i, j), perm in sorted(out['permutations'].items())]}


def audit():
    p, y, T = fixture()
    out = realize(p, y, T)
    choices = [[i for i in range(4) if p[i][j] is not None] for j in range(7)]
    best, count = None, 0
    for assignment in product(*choices):
        loads = [sum((p[i][j] for j in range(7) if assignment[j] == i), F(0))
                 for i in range(4)]
        value = max(loads)
        best = value if best is None else min(best, value)
        lifted = [F(0)]*24
        for j, i in enumerate(assignment):
            for a in range(6):
                lifted[6*i+out['permutations'][i, j][a]] += p[i][j]
        assert all(lifted[6*i+b] == loads[i] for i in range(4) for b in range(6))
        count += 1
    assert best == F(5, 3) and max(out['loads']) == F(4, 3)
    # Independent projection from returned actual assignments, not stored configs.
    projected = [{ } for _ in range(4)]
    for ib in range(24):
        i = ib//6
        C = tuple(sorted(ja//6 for ja, dest in enumerate(out['sigma']) if dest == ib))
        assert len(set(C)) == len(C)
        projected[i][C] = projected[i].get(C, F(0)) + F(1, 6)
    for i in range(4):
        assert projected[i] == dict(y[i])
    rng, random_cases = random.Random(20261017), 0
    for _ in range(160):
        m, n, states = rng.randrange(1, 5), rng.randrange(0, 6), rng.randrange(1, 6)
        pp = [[F(rng.randrange(7), rng.randrange(1, 8)) for _ in range(n)]
              for _ in range(m)]
        schedules = [[rng.randrange(m) for _ in range(n)] for _ in range(states)]
        yy = [[] for _ in range(m)]
        TT = F(0)
        for i in range(m):
            for s in schedules:
                C = tuple(j for j in range(n) if s[j] == i)
                yy[i].append((C, F(1, states)))
                TT = max(TT, sum((pp[i][j] for j in C), F(0)))
        rr = realize(pp, yy, TT)
        assert len(rr['sigma']) == n*rr['q']
        random_cases += 1
    boundaries = [([[]], [[((), F(1))]], 0),
                  ([[0]], [[((0,), F(1))]], 0),
                  ([[None], [F(7, 5)]], [[((), F(1))], [((0,), F(1))]], F(7, 5))]
    for args in boundaries:
        realize(*args)
    invalid = [([[1.0]], [[((0,), 1)]], 1),
               ([[True]], [[((0,), 1)]], 1),
               ([[None]], [[((0,), 1)]], 1),
               ([[1]], [[((0, 0), 1)]], 2),
               ([[1]], [[((0,), F(1, 2))]], 1),
               ([[1]], [[((0,), 1)]], 0),
               ([[0]], [[((False,), 1)]], 0)]
    for args in invalid:
        try:
            realize(*args)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid input accepted')
    return {'schema_version': 1, 'seed': 20261017,
            'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'base_schedules': count, 'base_OPT': str(best),
            'configuration_threshold_proved_in_account': str(T),
            'cover_q': out['q'], 'cover_actual_makespan': str(max(out['loads'])),
            'random_true_mixtures': random_cases, 'boundary_cases': len(boundaries),
            'invalid_cases': len(invalid), 'python_version': sys.version,
            'limitations': ['Finite implementation checks, not a universal proof.',
                            'No general configuration solver or polynomial-size hardness reduction.',
                            'High-girth existence is proved in the account, not generated here.']}


if __name__ == '__main__':
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
