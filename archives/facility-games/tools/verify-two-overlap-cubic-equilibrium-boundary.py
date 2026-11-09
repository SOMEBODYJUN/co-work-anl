"""Exhaust two-action support cells and correlated-polytope vertices exactly."""
from fractions import Fraction as F
from itertools import combinations, product

PROFILES = tuple(product((0, 1), repeat=2))

def cost_differences(a, b, weights, degree):
    result = []
    for i, w in enumerate(weights):
        other = weights[1-i]
        result.append(((a+w)**degree-(b+w+other)**degree,
                       (a+w+other)**degree-(b+w)**degree))
    return result

def ne(differences, point):
    for i, own in enumerate(point):
        low, high = differences[i]
        delta = low + (high-low)*point[1-i]
        if (own > 0 and delta > 0) or (own < 1 and delta < 0):
            return False
    return True

def test_axis(*rows):
    breakpoints = {F(0), F(1)}
    for low, high in rows:
        t = -low/(high-low)
        if 0 <= t <= 1:
            breakpoints.add(t)
    ordered = sorted(breakpoints)
    return ordered + [(a+b)/2 for a,b in zip(ordered, ordered[1:])]

def correlated_rows(differences):
    rows = [tuple(F(-int(i==j)) for j in range(4)) for i in range(4)]
    for i, rec in product(range(2), (0,1)):
        rows.append(tuple((2*rec-1)*differences[i][p[1-i]] if p[i]==rec else F(0) for p in PROFILES))
    return rows

def solve(matrix):
    matrix = [list(row)+[F(i==0)] for i, row in enumerate(matrix)]
    for j in range(4):
        k = next((i for i in range(j, 4) if matrix[i][j]), None)
        if k is None:
            return None
        matrix[j], matrix[k] = matrix[k], matrix[j]
        pivot = matrix[j][j]
        matrix[j] = [x/pivot for x in matrix[j]]
        for i in range(4):
            if i != j and matrix[i][j]:
                k = matrix[i][j]
                matrix[i] = [x-k*y for x,y in zip(matrix[i],matrix[j])]
    return tuple(row[-1] for row in matrix)

def satisfies(point, rows):
    return all(sum(x*y for x,y in zip(row,point)) <= 0 for row in rows)

def vertices(rows):
    for tight in combinations(rows, 3):
        point = solve([(F(1),)*4, *tight])
        if point is not None and satisfies(point, rows):
            yield point

def same_correlated(left, right):
    return all(satisfies(x, right) for x in vertices(left)) and all(satisfies(x, left) for x in vertices(right))

counts={"instances":0,"different_independent_and_correlated":0,"boundary_differences":0}
for u in map(F, range(1,5)):
    for v in map(F, range(int(u),6)):
        for b in (F(0),F(1,3),F(3)):
            for d in {F(0),F(1,2),u/2,u,(u+v)/2,v,v+1}:
                linear=cost_differences(b+d,b,(u,v),1)
                cubic=cost_differences(b+d,b,(u,v),3)
                expected = 0 < d < u or d == u < v
                axis0=test_axis(linear[1],cubic[1])
                axis1=test_axis(linear[0],cubic[0])
                assert any(ne(linear,p)!=ne(cubic,p) for p in product(axis0,axis1)) == expected
                assert all(ne(linear,p)==ne(cubic,p) for p in PROFILES)
                assert (not same_correlated(correlated_rows(linear),correlated_rows(cubic))) == expected
                counts["instances"]+=1
                counts["different_independent_and_correlated"]+=expected
                counts["boundary_differences"]+=d==u<v
print(counts)
