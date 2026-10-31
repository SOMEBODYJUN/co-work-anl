#!/usr/bin/env python3
"""本轮补充有限核对；不属于Potechin原文，不代替一般PSD证明。"""
from fractions import Fraction
from itertools import combinations
from math import comb
import json

def falling(x, a):
    out = Fraction(1)
    for j in range(a):
        out *= x-j
    return out

def mu(n, k, a):
    return falling(k, a)/falling(n, a)

def exact_psd(matrix):
    a = [row[:] for row in matrix]
    positive = 0
    zero = 0
    while a:
        assert all(a[i][i] >= 0 for i in range(len(a)))
        chosen = next((i for i in range(len(a)) if a[i][i] > 0), None)
        if chosen is None:
            assert all(x == 0 for row in a for x in row)
            zero += len(a)
            break
        if chosen:
            a[0], a[chosen] = a[chosen], a[0]
            for row in a:
                row[0], row[chosen] = row[chosen], row[0]
        pivot = a[0][0]
        a = [[a[i][j]-a[i][0]*a[0][j]/pivot
              for j in range(1, len(a))] for i in range(1, len(a))]
        positive += 1
    return {'positive_pivots': positive, 'zero_pivots': zero}

def audit(n, k, square_order):
    subsets = [frozenset(c) for a in range(square_order+1)
               for c in combinations(range(n), a)]
    matrix = [[mu(n,k,len(a|b)) for b in subsets] for a in subsets]
    result = exact_psd(matrix)
    recursion_count = 0
    for a in range(n):
        assert a*mu(n,k,a)+(n-a)*mu(n,k,a+1) == k*mu(n,k,a)
        recursion_count += 1
    cylinder_count = 0
    for a in range(n+1):
        for b in range(n-a+1):
            direct = sum(((-1)**j*comb(b,j)
                          *mu(n,k,a+j) for j in range(b+1)), Fraction(0))
            assert direct == falling(k,a)*falling(n-k,b)/falling(n,a+b)
            cylinder_count += 1
    mean = n*mu(n,k,1)
    second = mean+n*(n-1)*mu(n,k,2)
    assert mean == k and second == k*k
    d = min(2*int(min(k,n-k))+3, n)
    assert square_order == d//2
    return dict(n=n,k=str(k),source_index_degree_bound=d,
                square_order=square_order,matrix_dimension=len(subsets),
                **result,recursion_count=recursion_count,
                cylinder_identity_count=cylinder_count,
                mean=str(mean),formal_variance=str(second-mean*mean))

if __name__ == '__main__':
    cases = [audit(8,Fraction(3,2),2), audit(7,Fraction(7,2),3)]
    negative = mu(8,Fraction(3,2),3)
    assert negative == Fraction(-1,896)
    print(json.dumps({'kind':'finite-exact-check-only', 'cases':cases,
                      'negative_length_3_cylinder':str(negative),
                      'all_checks_passed':True},indent=2))
