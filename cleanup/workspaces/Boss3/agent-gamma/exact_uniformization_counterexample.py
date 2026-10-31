"""Exact rational obstruction to fixed-x within-size-class uniformization."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

x=list(map(Q,['.60','.26','.17','.34','.46']))
a,b=Q(7,10),Q(2,5)
w=[2,2,1,1,2]
assert a*sum(x[:2])+b*sum(x[2:])<=1 and a+b>1

def ratio(w):
    den=sum(p*v for p,v in zip(x,w))
    if not den:return None
    num=Q(0)
    for r in product([0,1],repeat=5):
        p=Q(1)
        for pi,ri in zip(x,r):p*=pi if ri else 1-pi
        aa=max([w[j] for j in range(2) if r[j]]+[0])
        bb=sum(sorted([w[j] for j in range(2,5) if r[j]],reverse=True)[:2])
        num+=p*max(aa,bb)
    return num/den

best=(Q(2),None)
for mask in product([0,1],repeat=5):
    for u,v in [(1,0),(0,1),(1,1),(2,1)]:
        ww=[mask[j]*(u if j<2 else v) for j in range(5)]
        z=ratio(ww)
        if z is not None and z<best[0]:best=(z,ww)
candidate=ratio(w)
assert candidate<best[0]
out={'sizes':[str(a),str(b)],'natural_lp_cost':str(a*sum(x[:2])+b*sum(x[2:])),
     'x':[str(p) for p in x],'counterexample_weights':w,
     'ratio':str(candidate),'ratio_float':float(candidate),
     'best_class_uniform_subsupport_ratio':str(best[0]),
     'best_class_uniform_subsupport_weights':best[1],
     'gap':str(best[0]-candidate),
     'scope':'Refutes fixed-x within-class uniformization, even allowing zero-weight sub-supports. Does not refute global symmetrization that changes x.'}
path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
