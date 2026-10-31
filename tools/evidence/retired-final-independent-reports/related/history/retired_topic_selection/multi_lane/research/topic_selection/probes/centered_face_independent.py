#!/usr/bin/env python3
"""Exact independent check using affine spans of permutation vertices.

No QP optimizer, no floating-point tolerance, no novelty assertion.
Default output goes to stdout; redirect to a NEW path to preserve frozen data.
"""
from fractions import Fraction as F
from itertools import permutations
import json


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def independent(vectors):
    basis, pivots, original = [], [], []
    for vector in vectors:
        work = list(map(F, vector))
        for row, pivot in zip(basis, pivots):
            q = work[pivot]
            work = [a-q*b for a, b in zip(work, row)]
        pivot = next((i for i, x in enumerate(work) if x), None)
        if pivot is not None:
            q = work[pivot]
            basis.append([x/q for x in work])
            pivots.append(pivot)
            original.append(list(map(F, vector)))
    return original


def solve(a, b):
    n = len(b)
    mat = [list(map(F, row))+[F(rhs)] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if mat[i][col])
        mat[col], mat[pivot] = mat[pivot], mat[col]
        q = mat[col][col]
        mat[col] = [x/q for x in mat[col]]
        for i in range(n):
            if i != col:
                q = mat[i][col]
                mat[i] = [x-q*y for x, y in zip(mat[i], mat[col])]
    return [row[-1] for row in mat]


def audit(n, edges):
    edges = sorted(set(edges))
    if n < 1 or any(not (0 <= i < n and 0 <= j < n) for i, j in edges):
        raise ValueError("invalid support graph")
    allowed = set(edges)
    perms = [p for p in permutations(range(n)) if all((i, p[i]) in allowed for i in range(n))]
    if not perms:
        raise ValueError("no perfect matching")
    require_covered = {(i, p[i]) for p in perms for i in range(n)} == allowed
    assert require_covered, "unused edges do not define the stated relative-interior support"
    vertices = [[F(int(p[i] == j)) for i, j in edges] for p in perms]
    v0 = vertices[0]
    directions = independent([[x-y for x, y in zip(v, v0)] for v in vertices[1:]])
    gram = [[dot(a, b) for b in directions] for a in directions]
    coeffs = solve(gram, [-dot(a, v0) for a in directions]) if directions else []
    p = [v0[k]+sum((c*d[k] for c, d in zip(coeffs, directions)), F(0)) for k in range(len(edges))]
    assert all(dot(p, d) == 0 for d in directions)
    assert all(sum((p[k] for k, (i, j) in enumerate(edges) if i == row), F(0)) == 1 for row in range(n))
    assert all(sum((p[k] for k, (i, j) in enumerate(edges) if j == col), F(0)) == 1 for col in range(n))
    # Affine feasibility + nonnegative entries is exactly membership in this face.
    return {"n": n, "edges": edges, "permutations": perms, "face_dimension": len(directions),
            "projection": [str(x) for x in p], "minimum": str(min(p)),
            "centered": min(p) >= 0, "squared_norm": str(dot(p, p))}


def main():
    star4 = [(0, j) for j in range(4)] + [(i, 0) for i in range(1, 4)] + [(i, i) for i in range(1, 4)]
    subdivided = [(0, 0), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1),
                  (2, 0), (2, 2), (3, 0), (3, 3), (4, 1), (4, 4)]
    rows = {"singleton": audit(1, [(0, 0)]), "star4": audit(4, star4),
            "odd_subdivision": audit(5, subdivided)}
    assert rows["singleton"]["centered"]
    assert rows["star4"]["minimum"] == "0"
    assert rows["odd_subdivision"]["minimum"] == "-1/28"
    assert rows["star4"]["face_dimension"] == rows["odd_subdivision"]["face_dimension"]
    for n, edges in [(1, []), (1, [(1, 0)])]:
        try:
            audit(n, edges)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid boundary case accepted")
    print(json.dumps({"method": "Fraction affine projection from all permutation vertices",
                      "examples": rows, "limits": "finite exact checks; no general classification or novelty claim"}, indent=2))


if __name__ == "__main__":
    main()
