"""Replay the complete strategies and unique static optima for 61 sizes."""
from fractions import Fraction as F
from itertools import combinations_with_replacement

def shares(a, b):
    overlap = F(len(a & b), 2)
    return len(a) - overlap, len(b) - overlap

def instance(k):
    a = [('a', i) for i in range(6*k-4)]
    b = [('b', i) for i in range(7*k-1)]
    c = [('c', i) for i in range(7*k-2)]
    d = [('d', i) for i in range(7*k-2)]
    ac = {('ac', 0), ('ac', 1)}
    ad = {('ad', 0), ('ad', 1)}
    A, B, C, D = set(a)|ac|ad, set(b), set(c)|ac, set(d)|ad
    shared = set(c[:2*k]) | set(d[:2*k])
    P = shared | set(a[:2*k+2]) | set(b[:2*k-2])
    Q = shared | set(a[2*k+2:4*k+4]) | set(b[2*k-2:4*k-4])
    assert len(P) == len(Q) == 8*k and len(P & Q) == 4*k
    return A, B, C, D, P, Q

for k in range(4, 65):
    X = instance(k)
    response = (1, 4, 4, 4, 5, 4)
    for i, j in enumerate(response):
        u, v = shares(X[i], X[j])
        assert u == 6*k and v == max(shares(X[i], S)[1] for S in X)
    unions = {(i,j): len(X[i]|X[j]) for i,j in combinations_with_replacement(range(6), 2)}
    assert max(unions.values()) == 14*k
    assert [pair for pair, value in unions.items() if value == 14*k] == [(2,3)]
    assert len(X[0]|X[1]) == 13*k-1
    assert len((X[2]|X[3])-(X[0]|X[1])) == 14*k-4
print("61 exact instances, 2562 complete incentive rows and 1281 comparison pairs.")
