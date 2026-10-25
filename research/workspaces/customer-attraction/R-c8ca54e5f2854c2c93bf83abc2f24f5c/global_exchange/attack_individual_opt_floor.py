"""Attack the candidate 2m*u_i >= OPT_m on one existing fixed full policy.
A negative result is not evidence of a universal theorem.
"""
import json,itertools
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
p=6;m=3
cert=json.load(open(ROOT/'evidence/certificates/customer_attraction/individual_security_failure.json'))
pol={tuple(r['history']):r['action'] for r in cert['strategy']['actions']}
types=list(range(1,1<<p))
def end(h):
 h=tuple(h)
 while len(h)<m:h+=pol[h],
 return h
def row(a,z):
 return [Fraction(1,sum(bool(B>>t&1) for t in z)) if B>>a&1 else Fraction(0) for B in types]
z=end(())
G=[]
for h,a in pol.items():
 base=row(a,end(h))
 for t in range(p):
  other=row(t,end(h+(t,)))
  G.append([u-v for u,v in zip(base,other)])
f=row(z[0],z)
best=(-1,None,None)
for J in itertools.combinations(range(p),m):
 v=[int(any(B>>a&1 for a in J)) for B in types]
 ans=linprog(-np.array(v),A_ub=-np.array(G,dtype=float),b_ub=np.zeros(len(G)),A_eq=np.array([f],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
 if ans.success and -ans.fun>best[0]:best=(-ans.fun,J,ans)
val,J,ans=best
x=[Fraction(float(t)).limit_denominator(1000000) for t in ans.x]
v=[int(any(B>>a&1 for a in J)) for B in types]
print('fixed policy p,m,actual',p,m,z,'best O/u1',val,'comparison',J)
print('exact O',sum(t*xx for t,xx in zip(v,x)),'u1',sum(t*xx for t,xx in zip(f,x)),'min IC',min(sum(g*xx for g,xx in zip(r,x)) for r in G))
print('nonzero types',[(tuple(i for i in range(p) if B>>i&1),str(xx)) for B,xx in zip(types,x) if xx])
