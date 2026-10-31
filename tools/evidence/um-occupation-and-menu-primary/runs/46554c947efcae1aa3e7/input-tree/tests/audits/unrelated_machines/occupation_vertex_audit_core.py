#!/usr/bin/env python3
"""Fraction vertex, matroid-face and matching oracles for finite audits.

Exponential enumeration is intentional; this is not a production LP backend.
"""
from fractions import Fraction as F
from itertools import product, combinations, permutations


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def rank(matrix):
    if not matrix:
        return 0
    a = [list(map(F, row)) for row in matrix]
    rows, cols, k = len(a), len(a[0]), 0
    for j in range(cols):
        pivot = next((i for i in range(k, rows) if a[i][j]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        c = a[k][j]
        a[k] = [x/c for x in a[k]]
        for i in range(rows):
            if i != k and a[i][j]:
                c = a[i][j]
                a[i] = [x-c*y for x, y in zip(a[i], a[k])]
        k += 1
        if k == rows:
            break
    return k


def solve_square(matrix, rhs):
    n = len(rhs)
    a = [list(map(F, row)) + [F(b)] for row, b in zip(matrix, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return None
        a[j], a[pivot] = a[pivot], a[j]
        c = a[j][j]
        a[j] = [x/c for x in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                c = a[i][j]
                a[i] = [x-c*y for x, y in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


def affine_rank(points):
    if not points:
        raise AssertionError('empty affine hull')
    p = points[0]
    return rank([[x-y for x, y in zip(q, p)] for q in points[1:]])


def max_matching(graph, homes):
    """Independent recursive integer oracle; can leave macros unmatched."""
    homes = set(homes)
    def rec(b, used):
        if b == len(graph):
            return ()
        best = rec(b+1, used)
        for h in sorted(graph[b] & homes - used):
            candidate = ((b, h),) + rec(b+1, used | {h})
            if len(candidate) > len(best):
                best = candidate
        return best
    return rec(0, set())


def prepare(groups, graph):
    hcount = len(groups)
    offsets = []
    labels = []
    columns = []
    for group in groups:
        offsets.append(len(columns))
        for o, a in group:
            labels.append(o)
            columns.append(tuple(map(F, a)))
    kcount = len(columns[0]) if columns else 0
    rows = tuple(tuple(col[z] for col in columns) for z in range(kcount))
    selections, points = [], []
    for selection in product(*(range(len(qs)) for qs in groups)):
        occupied = {h for h, q in enumerate(selection) if groups[h][q][0]}
        if len(occupied) != len(graph):
            continue
        if len(max_matching(graph, occupied)) != len(graph):
            continue
        point = [F(0)] * len(columns)
        for h, q in enumerate(selection):
            point[offsets[h]+q] = F(1)
        selections.append(selection)
        points.append(tuple(point))
    if not hcount:
        assert not graph
        selections, points = [()], [()]
    return offsets, rows, selections, points


def projected_vertex(points, rows, budgets, active):
    """Enumerate vertices of the lambda extension, then lex-minimize y exactly.

    An extension vertex has <= |active|+1 positive convex coefficients.
    Lex-minimization in all y coordinates chooses a projected vertex, even
    when an arbitrary extension vertex need not project to one.
    """
    loads = [[dot(row, p) for row in rows] for p in points]
    best = None
    candidate_count = 0
    for s in range(1, min(len(points), len(active)+1)+1):
        for inds in combinations(range(len(points)), s):
            for eqrows in combinations(active, s-1):
                matrix = [[F(1)]*s]
                rhs = [F(1)]
                for z in eqrows:
                    matrix.append([loads[i][z] for i in inds])
                    rhs.append(budgets[z])
                lam = solve_square(matrix, rhs)
                if lam is None or any(t < 0 for t in lam):
                    continue
                if any(sum((lam[j]*loads[i][z] for j, i in enumerate(inds)), F(0)) > budgets[z] for z in active):
                    continue
                point = tuple(sum((lam[j]*points[i][t] for j, i in enumerate(inds)), F(0)) for t in range(len(points[0])))
                candidate_count += 1
                if best is None or point < best:
                    best = point
    assert best is not None, 'feasible extension must have an enumerated vertex'
    return best, candidate_count


def face_dimensions(y, groups, graph, offsets, integer_points):
    hcount = len(groups)
    x = [sum((F(o)*y[offsets[h]+q] for q, (o, _) in enumerate(group)), F(0)) for h, group in enumerate(groups)]
    support = [{q for q in range(len(group)) if y[offsets[h]+q]} for h, group in enumerate(groups)]
    tight = []
    for mask in range(1 << hcount):
        sub = {h for h in range(hcount) if mask & (1 << h)}
        matroid_rank = len(max_matching(graph, sub))
        val = sum((x[h] for h in sub), F(0))
        assert val <= matroid_rank
        if val == matroid_rank:
            tight.append((sub, matroid_rank))
    face, occupations = [], []
    for point in integer_points:
        if any(point[offsets[h]+q] and q not in support[h] for h, group in enumerate(groups) for q in range(len(group))):
            continue
        occupation = [sum((F(o)*point[offsets[h]+q] for q, (o, _) in enumerate(group)), F(0)) for h, group in enumerate(groups)]
        if any(sum((occupation[h] for h in sub), F(0)) != rhs for sub, rhs in tight):
            continue
        face.append(point)
        occupations.append(occupation)
    return affine_rank(face), affine_rank(occupations), support, sum(0 < t < 1 for t in x)
