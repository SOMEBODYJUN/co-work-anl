#!/usr/bin/env python3
"""Independent exact combinatorial check; no author helpers imported."""
from math import comb
from fractions import Fraction as F
import json

def C(n,k):return comb(n,k) if n>=0 and 0<=k<=n else 0

def H(n):return sum((F(1,j) for j in range(1,n+1)),F(0))
count=0
for m in range(1,21):
 for c in range(m+1):
  Q=lambda r:F(C(m-r,c),C(m,c))
  if c:
   assert sum(((1-Q(r))/r for r in range(1,m+1)),F(0))==H(c)
   assert sum(((1-Q(r))/(m-r) for r in range(m)),F(0))==H(m)-F(1,c)
  for d in range(1,m+1):
   P=lambda r:F(C(r,d),C(m,d))
   K=lambda a,b:F(C(m,a+b),b*C(m,a)*C(m,b))
   assert sum((P(r)*Q(r)/r for r in range(1,m+1)),F(0))==K(c,d)
   if c:
    assert sum((P(r)*Q(r)/(m-r) for r in range(m)),F(0))==K(d,c)
   else:
    assert sum((P(r)/(m-r) for r in range(m)),F(0))==H(m)-H(d)
   count+=1
print(json.dumps({'status':'PASS','exact_parameter_triples':count,'players_range':[1,20],'checks':'harmonic coefficients and both Vandermonde kernels; Fraction only'}))
