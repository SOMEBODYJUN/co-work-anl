"""A finite whole-SPE-cone attack on B2 using fixed safety witnesses."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json, random
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack
from background_probe import security, comps
from customer_attraction import Instance, CustomerType, ExactSPESolver

OUT=Path(__file__).parent

def add(q,a):return q[:a]+(q[a]+1,)+q[a+1:]
def masks(k):return [tuple(i for i in range(k) if m>>i&1) for m in range(1,1<<k)]
def frow(q,a,types):return [F(int(a in T),1+sum(q[j] for j in T)) for T in types]
def gamma(inst,cert,types):
 actions=cert.actions;k=inst.topic_count;n=inst.players
 z={}
 def term(h):
  if h in z:return z[h]
  if len(h)==n:q=tuple(h.count(i) for i in range(k))
  else:q=term(h+(actions[h],))
  z[h]=q;return q
 rows=[]
 for h,a0 in actions.items():
  q0=term(h)
  for a in range(k):
   if a==a0:continue
   q1=term(h+(a,))
   rows.append([float((F(int(a0 in T),sum(q0[j] for j in T)) if a0 in T else F(0))-(F(int(a in T),sum(q1[j] for j in T)) if a in T else F(0))) for T in types])
 return np.array(rows)

def probe(k,r,seed):
 rng=random.Random(seed);types=masks(k)
 cs=tuple(CustomerType(frozenset(T),rng.randrange(1,10)) for T in types)
 inst=Instance(tuple(map(str,range(k))),cs,r)
 sol=ExactSPESolver(inst)
 # Lowest total first-two payout path among all realizable ordered prefixes and outcomes.
 floor=sol.threshold((0,)*k);best=None
 for a in range(k):
  p1=add((0,)*k,a);f1=sol.threshold(p1)
  for b in range(k):
   p2=add(p1,b)
   for q in sol.outcomes(p2):
    U=inst.topic_payoffs(q)
    if U[a]>=floor and U[b]>=f1:
     val=U[a]+U[b]
     if best is None or val<best[0]:best=(val,a,b,q)
 _,a,b,q=best
 path=next(h for h in sol.ordered_outcomes(q) if h[:2]==(a,b))
 cert=sol.certificate(q,on_path=path)
 print('policy',k,r,seed,path,'nodes',len(cert.actions),flush=True)
 G=gamma(inst,cert,types);dim=len(types)
 pref2=add(add((0,)*k,a),b)
 v0,M0,B0,res0=security(inst,(0,)*k)
 v2,M2,B2,res2=security(inst,pref2)
 p=-res0.ineqlin.marginals
 Q=res2.x[:-1]
 low=[]
 for bg in B0:
  low.append([sum(float(p[t])*float(frow(bg,t,types)[j]) for t in range(k)) for j in range(dim)])
 high=[]
 for t in range(k):
  high.append([sum(float(Q[l])*float(frow(tuple(pref2[j]+bg[j] for j in range(k)),t,types)[h]) for l,bg in enumerate(B2)) for h in range(dim)])
 # variables w, vL, vU. Full policy SPE G*w>=0; lower safety >=vL; upper safety<=vU.
 A=np.vstack([np.column_stack([-G,np.zeros((len(G),2))]),np.column_stack([-np.array(low),np.ones(len(low)),np.zeros(len(low))]),np.column_stack([np.array(high),np.zeros(k),-np.ones(k)])])
 c=np.array([float((F(int(a in T),sum(q[j] for j in T)) if a in T else F(0))+(F(int(b in T),sum(q[j] for j in T)) if b in T else F(0))) for T in types]+[-r,r-2])
 res=linprog(c,A_ub=A,b_ub=np.zeros(len(A)),A_eq=[[1]*dim+[0,0]],b_eq=[1],bounds=[(0,None)]*dim+[(None,None),(None,None)],method='highs')
 print('RESULT',k,r,seed,'fun',res.fun,'success',res.success,flush=True)
 data={'k':k,'r':r,'seed':seed,'policy_path':path,'node_count':len(cert.actions),'cone_rows':len(G),'fun':res.fun,'status':res.message,'p':[float(x) for x in p],'Q':[(B2[i],float(x)) for i,x in enumerate(Q) if x>1e-8]}
 if res.success and res.fun < -1e-8:
  data['w_float']=res.x[:dim].tolist();data['types']=types;data['certificate']=cert.to_dict()
 OUT.joinpath(f'block_cone_{k}_{r}_{seed}.json').write_text(json.dumps(data,indent=2))
 return data

if __name__=='__main__':
 for k,r,seed in [(5,4,928797),(6,5,129487),(7,5,932739)]:
  d=probe(k,r,seed)
  if d['fun'] is not None and d['fun']< -1e-8:break
