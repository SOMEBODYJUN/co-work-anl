"""Independent exact arithmetic checks supporting the repeated-last review.

The written review supplies the all-m argument; these checks audit formulas.
No repository model, solver, or proof script is imported.
"""
import json
from fractions import Fraction as F
from math import isqrt

cases=0
for m in range(1,101):
    for c in range(m+1):
        for b in (0,1):
            if b>c:continue
            share=F(b,c) if c else F(0)
            for d in range(m+1):
                q=F(d,c+1-b)
                slack=F(c>0)-share+q-F(d>0)
                assert slack>=0, (m,c,b,d,slack)
                cases+=1
    for k in range(1,m+1):
        coefficient=F(k*(2*m-k),m)
        assert coefficient==F(m)-F((m-k)**2,m)
        assert (coefficient>=m-1)==((m-k)**2<=m)
        assert ((m-k)**2<=m)==(k>=m-isqrt(m))
        factor=1+F(m*(m-1),k*(2*m-k))
        if k==m:assert factor==2-F(1,m)
        assert (factor<=2)==((m-k)**2<=m)

print(json.dumps({'status':'passed','pointwise_cases':cases,'player_counts':100,'scope':'formula audit; universal proof is in the independent written review'},indent=2))
