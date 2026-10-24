"""Review-only exact recheck of the fixed module certificate. Writes nothing.

The finite checks below only verify the certificate's exceptional layers;
the displayed quadratic proves the remaining integer layers analytically.
This is not an SPE assembly or an EO counterexample.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json

types = [(4,1),(27,4),(29,3),(30,3),(31,2),(32,1),(43,3),
         (45,3),(46,3),(51,3),(53,3),(54,3),(59,2)]
p = [F(z,82) for z in (10,10,21,10,10,21)]
weights = [w*sum(p[j] for j in range(6) if mask >> j & 1)
           for mask,w in types]
A = sum(weights)
S = [sum(v for (mask,_),v in zip(types,weights) if mask >> j & 1)
     for j in range(6)]
assert sum(w for _,w in types) == 34
assert A == F(901,41) and max(S) == F(1235,82)

minima = []
count = 0
for t in range(7):
    vals = []
    for B in combinations_with_replacement(range(6),t):
        value = sum(v/(1+sum(mask >> j & 1 for j in B))
                    for (mask,_),v in zip(types,weights))
        assert value >= F(2411-587*(t-2),246)
        vals.append(value)
        count += 1
    minima.append(str(min(vals)))

# Cauchy lower bound A^2/(A+max(S)*t) minus the affine line has
# numerator 724945*t^2 - 3369701*t + 3281442 after multiplication
# by the positive denominator 246*(1802+1235*t).
# At t=0,1 this numerator is positive.  At t=s+4, s>=0, it is
# 724945*s^2 + 2429859*s + 1401758 > 0.
# The exact finite minima above separately establish t=2,3.
print(json.dumps(dict(
    A=str(A), S=list(map(str,S)), count=count, minima=minima,
    n17_gap=str(F(2411,246)-F(587,246*17)-F(29,3)),
    n18_gap=str(F(2411,246)-F(587,246*18)-F(29,3))),indent=2))
