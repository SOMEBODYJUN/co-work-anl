"""Attack only the general occupancy candidate along known credible family cones."""
import json
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
import numpy as np
from scipy.optimize import linprog
OUT=Path(__file__).parent

def comps(n,k):
 if k==1:yield (n,);return
 for i in range(n+1):
  for tail in comps(n-i,k-1):yield (i,)+tail

def run(m):
 P=m+2; original=np.array([m-2,1,m-2,m-2,m-2,m-1,0,0],float)
 # orbit coefficients: ordinary-private, ordinary-A, ordinary-B,
 # special-private, special-B, special-AB, A-only, B-only.
 types=[]
 for j in range(2,m+1):
  types.extend([((j,),0),((0,j),1),((1,j),2)])
 types.extend([((m+1,),3),((1,m+1),4),((0,1,m+1),5),((0,),6),((1,),7)])
 @lru_cache(None)
 def util(counts,a):
  out=np.zeros(8)
  for S,j in types:
   if a in S:out[j]+=1/sum(counts[t] for t in S)
  return out
 @lru_cache(None)
 def act(counts):
  if sum(counts)<m-1:return 0 if counts[1]==sum(counts) else 1
  vals=[]
  for a in range(P):
   c=list(counts);c[a]+=1;vals.append(util(tuple(c),a)@original)
  order=[1,0]+list(range(2,P));return max(order,key=lambda a:round(vals[a],12))
 @lru_cache(None)
 def leaf(counts):
  if sum(counts)==m:return counts
  c=list(counts);c[act(counts)]+=1;return leaf(tuple(c))
 rows=[]
 for t in range(m):
  for c in comps(t,P):
   a=act(c);base=util(leaf(c),a)
   for b in range(P):
    if b==a:continue
    d=list(c);d[b]+=1;rows.append(util(leaf(tuple(d)),b)-base)
 norm=np.array([0,m-1,m-1,0,1,1,1,1],float)
 E=np.array([0,(m-1)/2,(m-1)**2/m,0,(m-1)/m,m/(m+1),1/2,(m-1)/m],float)
 best=None
 for af in (0,1):
  for bf in (0,1):
   for sf in (0,1):
    k=m-af-bf-sf
    if not 0<=k<=m-1:continue
    optimum=np.array([k,m-1 if af else k,m-1 if bf else k,sf,int(bf or sf),int(af or bf or sf),af,bf],float)
    obj=optimum-norm-E
    res=linprog(-obj,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),A_eq=norm[None,:],b_eq=[1],bounds=(0,None),method='highs')
    if res.success and (best is None or -res.fun>best[0]):best=(-res.fun,af,bf,sf,k,res.x)
 print('m',m,'rows',len(rows),'max conjecture gap',best[0],'support',best[1:5],'weights',[str(Fraction(float(v)).limit_denominator()) for v in best[5]],flush=True)
 if best[0]>1e-8:
  (OUT/'prefix_occupancy_candidate_failure.json').write_text(json.dumps({'m':m,'value':best[0],'support':best[1:5],'weights':best[5].tolist()},indent=2));return True
 return False
for m in range(4,9):
 if run(m):break
