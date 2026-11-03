"""Discovery only: two-term CAG expansion under a large legal background.
Every policy has all ordered histories. Not a finite-B SPE certificate.
"""
from pathlib import Path
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
import random,json,sys
OUT=Path(__file__).resolve().parent

def coefficients(K,P):
 masks=np.arange(1,1<<K)
 M=np.array([[(int(mask)>>a)&1 for mask in masks] for a in range(K)],dtype=float)
 base=np.array(P)@M
 L=M/base;D=M/(base*base)
 return masks,M,L,D

def pair_policy(K,r,M,D,w,rng):
 C=(D*w)@M.T;diag=np.diag(C);actions={}
 def rec(h):
  if len(h)==r:return h
  zs=[rec(h+(a,)) for a in range(K)]
  vals=[diag[a]+sum(C[a,b] for b in zs[a] if False) for a in range(K)]
  vals=[sum(C[a,b] for b in zs[a]) for a in range(K)]
  low=min(vals);A=rng.choice([a for a in range(K) if vals[a]<=low+1e-9]);actions[h]=A;return zs[A]
 return actions,rec(())

def gamma(K,r,M,D,actions):
 rows=[]
 def cost(a,z):return D[a]*(np.array([z.count(b) for b in range(K)])@M)
 def rec(h):
  if len(h)==r:return h
  zs=[rec(h+(a,)) for a in range(K)];A=actions[h]
  for a in range(K):
   if a!=A:rows.append(cost(a,zs[a])-cost(A,zs[A]))
  return zs[A]
 z=rec(());return np.unique(np.round(rows,10),axis=0),cost(z[0],z),z

def securitytax(M,D,w,r):
 C=(D*w)@M.T;A=np.diag(C)[:,None]+(r-1)*C
 # min_p max_b p A_b, gives upper bound on max_q min_a A q.
 K=len(M);ans=linprog(np.r_[np.zeros(K),1],A_ub=np.c_[A.T,-np.ones(K)],b_ub=np.zeros(K),A_eq=[np.r_[np.ones(K),0]],b_eq=[1],bounds=[(0,None)]*K+[(None,None)],method='highs')
 return ans.x[:-1],ans.fun

def lp(G,cost,L,M,D,r,p):
 k,d=M.shape;B=np.array([p@D+(r-1)*((p@D)*M[b]) for b in range(k)])
 A=np.vstack([np.c_[-G,np.zeros(len(G))],np.c_[B,-np.ones(k)]])
 ans=linprog(np.r_[-cost,1],A_ub=A,b_ub=np.zeros(len(A)),A_eq=np.c_[L,np.zeros(k)],b_eq=np.ones(k),bounds=[(0,None)]*d+[(None,None)],method='highs')
 return ans
if __name__=='__main__':
 rng=random.Random(91037);best=-1e6;count=0
 for r,K in [(3,5),(3,6),(4,5),(4,6),(5,5)]:
  for it in range(100):
   P=[rng.randrange(1,5) for _ in range(K)];masks,M,L,D=coefficients(K,P)
   # Sparse feasible equally-large leading-order catalog; generic random objective.
   w0=linprog(np.array([rng.uniform(-1,1) for _ in masks]),A_eq=L,b_eq=np.ones(K),bounds=(0,None),method='highs').x
   actions,z=pair_policy(K,r,M,D,w0,rng);G,cost,z=gamma(K,r,M,D,actions)
   p,v=securitytax(M,D,w0,r)
   for alt in range(4):
    ans=lp(G,cost,L,M,D,r,p)
    if not ans.success:break
    w=ans.x[:-1];p,v=securitytax(M,D,w,r);loss=cost@w-v
    count+=1
    if loss>best+1e-8:
     best=loss;record={'status':'asymptotic floating only','r':r,'K':K,'P':P,'iteration':it,'alt':alt,'excess_tax':float(loss),'masks':masks.tolist(),'weights':w.tolist(),'query':p.tolist(),'z':z,'actions':[{'history':h,'action':a} for h,a in actions.items()]}
     (OUT/'nonuniform_background_best.json').write_text(json.dumps(record,indent=2));print(json.dumps({s:record[s] for s in ['r','K','P','iteration','alt','excess_tax','z']}),flush=True)
    if loss>1e-7:
     (OUT/'nonuniform_background_candidate.json').write_text(json.dumps(record,indent=2));sys.exit()
 print('Completed LPs',count,'best',best,flush=True)
