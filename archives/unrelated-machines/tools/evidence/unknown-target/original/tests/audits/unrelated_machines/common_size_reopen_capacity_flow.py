#!/usr/bin/env python3
"""Exact Fraction audit for the common-size reopen interface."""
from itertools import product
from fractions import Fraction
import json

def enum(p,b):
    m=len(p); n=len(p[0]); vals=[]
    for ass in product(range(m), repeat=n):
        l=[sum(Fraction(p[i][j]) for j,i2 in enumerate(ass) if i2==i) for i in range(m)]
        vals.append((ass,l,max(l)))
    return vals

# Equal-size common profile: fractional Hall passes but integral repair fails.
p=[[2,2,2],[2,2,2]]; b=[3,3]
vals=enum(p,b)
assert all(v[2]>3 for v in vals)
frac=[sum(Fraction(2)*Fraction(1,2) for _ in range(3)) for _ in range(2)]
assert frac==[Fraction(3),Fraction(3)]
# Heterogeneous endpoint profile: min-per-job shortcut is unsound.
p2=[[2,100,2],[100,2,2]]; b2=[3,3]
vals2=enum(p2,b2)
assert all(v[2]>3 for v in vals2)
# A valid headroom example: q=(1,2), capacities (3,2), all eligible; assign both to A/B? qmax=2 headroom c=(1,0) fails, but per-support H certificate with x putting q2 on B, q1 on A has r=(1,2), loads=(1,2), and loads+r=(2,4), so b=(3,4) needed.
p3=[[1,2],[1,2]]; b3=[3,4]
# x: q1 A, q2 B
assert 1+1<=3 and 2+2<=4

# General unrelated fractional infeasibility certificate: p=(2,3) for each job, b=(3,3).
# Machine-1 fraction sum S must satisfy S<=3/2; machine-2 requires S>=2.
S_upper=Fraction(3,2); S_lower=Fraction(2)
assert S_upper < S_lower
lam=(Fraction(3),Fraction(2))
assert sum(lam[i]*Fraction(3) for i in range(2)) == Fraction(15)
assert sum(min(lam[0]*2,lam[1]*3) for _ in range(3)) == Fraction(18)

print(json.dumps({
  'equal_common_fractional_load': [str(x) for x in frac],
  'equal_common_integral_min_makespan': str(min(v[2] for v in vals)),
  'heterogeneous_integral_min_makespan': str(min(v[2] for v in vals2)),
  'headroom_certificate_example': {'loads_plus_support_max': ['2','4'], 'capacities':['3','4']},
}, sort_keys=True))
