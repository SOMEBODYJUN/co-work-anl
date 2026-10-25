#!/usr/bin/env python3
"""Definition-level Fraction check of the crossed-reply tax identity.

This checks the finite per-client algebra and the old 34-unit complete-SPE
fixture's weighted menu. It does not assert ROW3 or half coverage.
"""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path

def u(x, others, b):
    return Q(x, b + 1 + sum(others))

def phi(x,y,b):
    return sum((Q(1,b+k) for k in range(1,x+y+1)),Q(0))

def g(x,y,t,b):
    return Q(x*y,(b+t+1)*(b+t+2))

checks=0
for b in [0,1,2,3,4,10,100]:
  for t,r,s,v,w,k in product(range(2),repeat=6):
    l1=u(r,[t,s],b)-u(v,[t,k],b)
    l2=u(k,[t,v],b)-u(w,[t,v],b)
    l3=u(s,[t,r],b)-u(k,[t,r],b)
    lhs=u(t,[r,s],b)-u(t,[v,w],b)
    rhs=l1+l2+u(s,[t],b)-u(k,[t],b)+phi(v,w,b)-phi(r,s,b)
    assert lhs==rhs,(b,t,r,s,v,w,k,lhs,rhs)
    tau=g(r,r,t,b)-g(s,r,t,b)
    assert tau>=0
    exact=l1+l2+l3+g(r,r,t,b)-g(k,r,t,b)+phi(v,w,b)-phi(r,s,b)
    assert lhs+tau==exact
    assert g(r,r,t,b)-g(k,r,t,b)>=0
    checks+=1

weights={4:1,27:4,29:3,30:3,31:2,32:1,43:3,45:3,46:3,51:3,53:3,54:3,59:2}
p=[Q(v,82) for v in (10,10,21,10,10,21)]
def B(a): return 3 if a<3 else 0
def C(a,b):
    group=range(3) if b<3 else range(3,6)
    return next(c for c in group if c not in (a,b))
def U(a,others):
    return sum((w*u((mask>>a)&1,[(mask>>z)&1 for z in others],0) for mask,w in weights.items()),Q(0))
def G(a,c,t):
    return sum((w*g((mask>>a)&1,(mask>>c)&1,(mask>>t)&1,0) for mask,w in weights.items()),Q(0))
D=Tax=Slacks=Remainder=Q(0)
for i in range(6):
    ri,si=B(i),C(i,B(i))
    Tax+=p[i]*(G(ri,ri,i)-G(si,ri,i))
    for j in range(6):
        rj,sj=B(j),C(j,B(j))
        kij=C(i,rj)
        mass=p[i]*p[j]
        D+=mass*(U(i,[ri,si])-U(i,[rj,sj]))
        l1=U(ri,[i,si])-U(rj,[i,kij])
        l2=U(kij,[i,rj])-U(sj,[i,rj])
        l3=U(si,[i,ri])-U(kij,[i,ri])
        assert min(l1,l2,l3)>=0
        Slacks+=mass*(l1+l2+l3)
        Remainder+=mass*(G(ri,ri,i)-G(kij,ri,i))
assert D==Q(-11,82)
assert D+Tax==Slacks+Remainder>=0
result={'status':'passed','pointwise_identity_cases':checks,'old_34_unit_weighted_fixture':{'decorrelation_delta':str(D),'private_first_follower_tax':str(Tax),'delta_plus_tax':str(D+Tax),'three_slacks':str(Slacks),'nonnegative_remainder':str(Remainder)},'scope':'Algebra/known complete-SPE fixture; no proof of ROW3 or half coverage.'}
out=Path(__file__).with_name('crossed_reply_tax_audit.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
