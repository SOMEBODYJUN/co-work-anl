"""Exact arithmetic corroboration of proved all-N marginal inequalities.
The infinite statement is proved in UNIVERSAL_SCALING_ATTACK.md.
"""
from fractions import Fraction as Q
import json
from pathlib import Path

def S2(t): return Q(t*(t+1)*(2*t+1),6)
def F(k,l):return 8*S2(l)+S2(k)+2*l*k*(k+1)+4*l*l*k+Q(3,4)*k*l
def H1(k,l):return Q((k+2*l)**2+k+4*l,2)
alpha=Q(64,59); h=Q(59,32)
tests=0; extrema={}
for name,p,degree in [('quadratic',F,2),('affine',H1,1),('constant',lambda k,l:k+2*l,0)]:
    for dk,dl,weight,scale in [(1,0,1,Q(1)),(0,1,2,h)]:
        vals=[]
        for k in range(101):
            for l in range(101):
                ratio=(p(k+dk,l+dl)-p(k,l))/Q((k+2*l+weight)**degree)
                assert scale<=ratio<=alpha*scale,(name,k,l,weight,ratio)
                vals.append(ratio);tests+=1
        extrema[f'{name}_w{weight}']=[str(min(vals)),str(max(vals))]
out=dict(alpha=str(alpha),heavy_scaling=str(h),theta='3/8',finite_checks=tests,extrema=extrema,infinite_proof='UNIVERSAL_SCALING_ATTACK.md; finite checks do not replace proof')
print(json.dumps(out,indent=2))
Path(__file__).with_name('verify_universal.json').write_text(json.dumps(out,indent=2))
