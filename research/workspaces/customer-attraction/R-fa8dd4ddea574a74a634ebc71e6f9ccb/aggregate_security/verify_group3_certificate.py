"""Exact reconstruction and independent coefficient verification of a fixed-policy pair bound.
The Fraction check, not the floating LP, establishes the finite coefficient identity.
"""
from fractions import Fraction as F
from pathlib import Path
import json
P=Path(__file__).resolve().parent
source=json.loads((P/'group3_within_Q.json').read_text())
k=6;m=3
# Rebuild all histories without importing the discovery program.
def action(h):
 if len(h)==0:return 0
 if len(h)==1:return 3 if h[0]<3 else 0
 return next(a for a in (range(3) if h[1]<3 else range(3,6)) if a not in h)
def terminal(h):
 while len(h)<3:h=h+(action(h),)
 return h
def coefficient(a,z,mask):
 if not mask&(1<<a):return F(0)
 return F(1,sum(bool(mask&(1<<b)) for b in z))
def row(h,b,mask):return coefficient(action(h),terminal(h),mask)-coefficient(b,terminal(h+(b,)),mask)
q=[(tuple(x['B']),F(x['p']).limit_denominator(120)) for x in source['Q']]
lam=[(x['a'],tuple(x['h']),x['b'],F(x['value']).limit_denominator(120)) for x in source['lambda']]
assert sum(p for B,p in q)==1 and all(p>=0 for B,p in q)
assert all(v>=0 for a,h,b,v in lam)
z=terminal(())
remainders=[]
for a in range(k):
 for mask in range(1,1<<k):
  budget=coefficient(z[0],z,mask)+coefficient(z[1],z,mask)
  beta=sum((p*F(bool(mask&(1<<a)),1+sum(bool(mask&(1<<b)) for b in B)) for B,p in q),F(0))
  rhs=sum((v*row(h,b,mask) for aa,h,b,v in lam if aa==a),F(0))
  rest=budget-2*beta-rhs
  assert rest>=0,(a,mask,rest)
  remainders.append(rest)
cert={'identity':'pair_budget - 2 E_Q payoff(query) = sum lambda Gamma + nonnegative_remainder','scope':'three players; exactly six labeled actions; fixed opposite-group complete formal strategy; arbitrary nonnegative type masses satisfying all its SPE rows','Q':[{'B':list(B),'p':str(p)} for B,p in q],'lambda':[{'a':a,'h':list(h),'b':b,'value':str(v)} for a,h,b,v in lam],'root':z,'checked_coefficients':len(remainders),'min_remainder':str(min(remainders)),'nonzero_remainders':sum(x!=0 for x in remainders),'verified':True}
(P/'group3_pair_exact_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
print(json.dumps({k:v for k,v in cert.items() if k not in ('lambda',)},indent=2))
