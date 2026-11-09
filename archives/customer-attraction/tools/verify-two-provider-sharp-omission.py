"""Audit all reachable two-provider outcomes and the exact 27-client equality case."""
from fractions import Fraction as F
from itertools import product
from random import Random

def profits(a, b):
    overlap = F(len(a & b), 2)
    return len(a) - overlap, len(b) - overlap

def examine(catalogue):
    k = len(catalogue)
    pay = {(i,j): profits(a,b) for i,a in enumerate(catalogue) for j,b in enumerate(catalogue)}
    tail = {i: [j for j in range(k) if pay[i,j][1] == max(pay[i,l][1] for l in range(k))]
            for i in range(k)}
    threshold = max(min(pay[i,j][0] for j in tail[i]) for i in range(k))
    comparisons = [c|d for c,d in product(catalogue, repeat=2)]
    outcomes = 0
    for i, js in tail.items():
        for j in js:
            if pay[i,j][0] < threshold:
                continue
            a,b = catalogue[i],catalogue[j]
            u,v = pay[i,j]
            L = max(map(len,catalogue))
            for union in comparisons:
                residual = len(union - (a|b))
                assert residual <= 2*v
                assert residual <= 3*u-F(L,2)
                assert F(13)*residual <= F(14)*(u+v)
            outcomes += 1
    return outcomes, len(comparisons)

A=set(range(6))
B=set(range(6,13))
C=set(range(13,20))
D=set(range(20,27))
P={0,1,6,7,13,14,20,21}
Q={0,1,6,7,15,16,22,23}
sharp=[A,B,C,D,P,Q]
policy=(1,4,4,4,5,4)
for i,j in enumerate(policy):
    p=profits(sharp[i],sharp[j])
    assert p[0]==6 and p[1]==max(profits(sharp[i],s)[1] for s in sharp)
assert len(A|B)==13 and len((C|D)-(A|B))==14
assert max(len(x|y) for x,y in product(sharp,repeat=2))==14

rng=Random(142613)
counts={"catalogues":0,"equilibrium_paths":0,"comparisons":0}
for catalogue in [sharp]+[
    [{x for x in range(n) if rng.randrange(4)<2} for _ in range(k)]
    for n,k in ((rng.randrange(28),rng.randrange(2,7)) for _ in range(480))
]:
    paths, pairs=examine(catalogue)
    counts["catalogues"]+=1
    counts["equilibrium_paths"]+=paths
    counts["comparisons"]+=paths*pairs
print(counts)
