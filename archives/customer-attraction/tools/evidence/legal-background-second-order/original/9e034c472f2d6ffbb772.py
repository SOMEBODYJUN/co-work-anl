"""Discovery: legal uniform high backgrounds, equal theme sizes, fixed-rank types.
A strict pairwise witness can be lifted to exact CAG at sufficiently large legal prefix.
"""
from itertools import combinations,product
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
import random,json,sys
OUT=Path(__file__).resolve().parent

def make_basis(K,k):
 masks=[sum(1<<a for a in B) for B in combinations(range(K),k)]
 M=np.array([[(mask>>a)&1 for mask in masks] for a in range(K)],dtype=float)
 return masks,M

def actual_policy(K,r,M,w,rng):
 C=(M*w)@M.T;actions={}
 def rec(h):
  if len(h)==r:return h
  zs=[rec(h+(a,)) for a in range(K)]
  vals=[sum(C[a,b] for b in zs[a][len(h)+1:])+sum(C[a,b] for b in h) for a in range(K)]
  low=min(vals);A=rng.choice([a for a in range(K) if vals[a]<=low+1e-9])
  actions[h]=A;return zs[A]
 z=rec(());return actions,z

def policy_lp(K,r,M,actions):
 rows=[]
 def cost(a,z):return M[a]*(np.array([z.count(b) for b in range(K)])@M-1)
 def rec(h):
  if len(h)==r:return h
  zs=[rec(h+(a,)) for a in range(K)];A=actions[h]
  for a in range(K):
   if a!=A:rows.append(cost(a,zs[a])-cost(A,zs[A]))
  return zs[A]
 z=rec(());obj=cost(z[0],z)-(r-1)*M[0]*k/K
 G=np.unique(np.round(rows,8),axis=0)
 ans=linprog(-obj,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=M,b_eq=np.ones(K),bounds=(0,None),method='highs')
 return ans,G,z,obj

def gen_weights(K,k,masks,rng):
 # cyclic-orbit random weights keep all theme sizes identical.
 d={a:j for j,a in enumerate(masks)};w=np.zeros(len(masks));seen=set()
 for mask in masks:
  if mask in seen:continue
  orbit=set();mm=mask
  for _ in range(K):orbit.add(mm);mm=((mm<<1)&((1<<K)-1))|(mm>>(K-1))
  val=rng.expovariate(1)
  for mm in orbit:w[d[mm]]=val
  seen.update(orbit)
 return w
if __name__=='__main__':
 rng=random.Random(731107);best=-1e9;records=[]
 cases=[(3,6,2),(3,6,3),(3,7,2),(3,7,3),(4,6,2),(4,6,3),(5,6,2),(5,7,3)]
 for r,K,k in cases:
  masks,M=make_basis(K,k)
  for it in range(60):
   w=gen_weights(K,k,masks,rng);actions,z=actual_policy(K,r,M,w,rng)
   ans,G,z,obj=policy_lp(K,r,M,actions)
   if not ans.success:continue
   loss=-ans.fun
   if loss>best+1e-9:
    best=loss;record={'r':r,'K':K,'k':k,'iteration':it,'excess_overlap_tax':loss,'masks':masks,'weights':ans.x.tolist(),'z':z,'actions':[{'history':h,'action':a} for h,a in actions.items()]};records.append(record)
    print(json.dumps({key:record[key] for key in ['r','K','k','iteration','excess_overlap_tax','z']}),flush=True)
    (OUT/'high_background_numerical.json').write_text(json.dumps(records,indent=2))
   if loss>1e-7:
    (OUT/'high_background_candidate.json').write_text(json.dumps(record,indent=2));sys.exit(0)
 print('No strict witness; completed',len(cases)*60,'policies',flush=True)
