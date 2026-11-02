"""Independent exact checks of terminal kernels, not an all-input proof/SPE solver."""
from fractions import Fraction as F
from itertools import combinations
from math import comb
import json
from pathlib import Path

def c(n,k):
    return comb(n,k) if 0 <= k <= n else 0

def resource(b,t):
    return F(t,b+t) if t else F(0)

def D(r,n,values):
    return tuple(F(r,n)*sum((F(c(t,k)*c(r-t,n-k),c(r,n))*values[k] for k in range(n+1)),F(0)) for t in range(r+1))

counts={'conditional_subsets':0,'kernel_cases':0,'nested_cases':0,'concavity_cases':0,'potential_endpoints':0}
for r in range(1,10):
 for n in range(1,r+1):
  for b in range(4):
   vals=tuple(resource(b,t) for t in range(r+1))
   df=D(r,n,vals)
   diffs=[df[t+1]-df[t] for t in range(r)]
   assert all(v>=0 for v in diffs)
   assert all(diffs[j]>=diffs[j+1] for j in range(r-1))
   counts['concavity_cases']+=1
   for t in range(1,r+1):
    # Current player=0, covering identities={0,...,t-1}.
    subs=list(combinations(range(1,r),n-1))
    a=sum((F(1,b+1+sum(j<t for j in s)) for s in subs),F(0))/len(subs)
    ah=sum((F(c(t-1,k)*c(r-t,n-1-k),c(r-1,n-1))*F(1,b+1+k) for k in range(n)),F(0))
    assert a==ah==df[t]/t
    u=F(1,b+t); q=F(r,n)*u-a
    assert 0<=q<=F(r-n,n)*u
    assert t*q==F(r,n)*vals[t]-df[t]
    assert F(n,r)*(df[t]+t*q)==vals[t] # inverse reconstruction
    if b==0:
     assert q==F(r,n*t)*F(c(r-t,n),c(r,n))
    if n==r-1:
     assert q==(resource(b,t)-resource(b,t-1))/n
    if n==1:
     assert a==F(1,b+1)
    counts['conditional_subsets']+=len(subs)
    counts['kernel_cases']+=1
   sum_a=sum((df[t]/t for t in range(1,r+1)),F(0))
   potential=sum((F(1,b+t)-F(n,r)*df[t]/t for t in range(1,r+1)),F(0))
   tail=sum((F(1,b+t) for t in range(n+1,r+1)),F(0))
   assert potential==tail
   assert F(n,r)*sum_a==sum((F(1,b+j) for j in range(1,n+1)),F(0))
   counts['potential_endpoints']+=1
   for k in range(1,n+1):
    inner=D(n,k,vals)
    composed=D(r,n,inner)
    direct=D(r,k,vals)
    assert composed==direct
    qrn=tuple(F(r,n)*vals[t]-df[t] for t in range(r+1))
    qnk=tuple(F(n,k)*vals[t]-inner[t] for t in range(n+1))
    d_qnk=D(r,n,qnk)
    for t in range(r+1):
     assert F(r,k)*vals[t]-direct[t]==F(n,k)*qrn[t]+d_qnk[t]
    counts['nested_cases']+=1

coeff={str(n):[str(F(5,n)*F(c(5-t,n),c(5,n))) for t in range(1,6)] for n in range(1,6)}
report={'status':'PASS','scope':'Finite exact regression of general formulas, no SPE or half certification','checks':counts,'m5_empty_background_Q_coefficients_E1_to_E5':coeff}
out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
