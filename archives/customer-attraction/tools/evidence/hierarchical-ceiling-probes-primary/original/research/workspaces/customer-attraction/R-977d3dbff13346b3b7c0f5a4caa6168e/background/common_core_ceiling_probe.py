"""Exact symmetry DP for the common core plus equal private-customer catalog.
Exploratory attack on another work area's myopic-ceiling relaxation, not SPE BI.
"""
from fractions import Fraction as F
from functools import lru_cache

def solve(m,K):
 @lru_cache(None)
 def dp(b):
  t=sum(b)
  if t==m:return b,F(0),None
  children={}
  for a in range(m):
   if a and b[a]==b[a-1]:continue
   c=list(b);c[a]+=1
   order=sorted(range(m),key=lambda z:c[z]);cs=tuple(c[z] for z in order)
   cm,cost,_=dp(cs);un=[0]*m
   for j,z in enumerate(order):un[z]=cm[j]
   children[a]=(un,cost)
  floor=F(K,m)+max(F(1,children[a][0][a]) for a in children)
  allowed=[a for a in children if F(K,t+1)+F(1,b[a]+1)>=floor]
  # For every equivalent action in an equal-count class, account for a possible
  # boost of its own count rather than only the chosen representative.
  maxima=[0]*m
  for a in allowed:
   un,_=children[a]
   group=[j for j in range(m) if b[j]==b[a]]
   for j in range(m):
    maxima[j]=max(maxima[j],un[j])
    if j in group:maxima[j]=max(maxima[j],un[a])
  # Restore exact symmetry of indistinguishable labels, including untouched groups.
  for val in set(b):
   group=[j for j in range(m) if b[j]==val]
   mx=max(maxima[j] for j in group)
   for j in group:maxima[j]=mx
  return tuple(maxima),floor+min(children[a][1] for a in allowed),floor
 maxs,cost,floor=dp((0,)*m)
 return cost,floor,dp.cache_info().currsize

if __name__=='__main__':
 for m in [3,4,5,6,8,10,15,20,25]:
  best=None
  for K in sorted(set([0,1,2,3,5,10,m//2,m,2*m,4*m,m*m])):
   G,L,n=solve(m,K);ratio=G/F(K+m)
   if best is None or ratio<best[0]:best=(ratio,K,G,L,n)
  print(m,*map(str,best),flush=True)
