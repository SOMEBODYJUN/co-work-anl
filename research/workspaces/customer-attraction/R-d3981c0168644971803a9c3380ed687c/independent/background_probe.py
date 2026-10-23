"""Attack the arbitrary-background aggregate-security candidate; discovery only."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import json, random, sys
import numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance, CustomerType, ExactSPESolver

def comps(k,n):
 for a in combinations_with_replacement(range(k),n):
  yield tuple(a.count(i) for i in range(k))

def security(inst,prefix):
 k=inst.topic_count;r=inst.players-sum(prefix)
 backgrounds=list(comps(k,r-1))
 M=[[sum((F(c.multiplicity,1+sum((prefix[j]+q[j]) for j in c.topics)) for c in inst.customers if a in c.topics),F(0)) for q in backgrounds] for a in range(k)]
 # minimizer Q, with v final coordinate
 A=np.array([[float(v) for v in row]+[-1] for row in M]); cost=[0]*len(backgrounds)+[1]
 res=linprog(cost,A_ub=A,b_ub=[0]*k,A_eq=[[1]*len(backgrounds)+[0]],b_eq=[1],bounds=[(0,None)]*len(backgrounds)+[(None,None)],method='highs')
 return res.fun, M, backgrounds, res

def profits(inst,prefix,q):
 return sum((q[a]-prefix[a])*u for a,u in enumerate(inst.topic_payoffs(q)))

def main():
 rng=random.Random(4924879);tested=0;best=(1.,None)
 for k,r,prefnum,iters in [(4,3,1,200),(5,3,2,200),(5,4,1,200),(6,3,2,100),(6,4,1,100)]:
  for it in range(iters):
   cs=[]
   for mask in range(1,1<<k):
    mult=rng.randrange(0,9) if rng.random()<.7 else 0
    if mult:cs.append(CustomerType(frozenset(j for j in range(k) if mask>>j&1),mult))
   inst=Instance(tuple(map(str,range(k))),tuple(cs),r+prefnum)
   pref=[0]*k
   for j in range(prefnum):pref[rng.randrange(k)]+=1
   pref=tuple(pref)
   sol=ExactSPESolver(inst);outs=sol.outcomes(pref)
   q=min(outs,key=lambda z:profits(inst,pref,z));P=profits(inst,pref,q)
   v,M,B,res=security(inst,pref);tested+=1
   gap=float(P)-r*v
   if v and float(P)/(r*v)<best[0]:
    best=(float(P)/(r*v),(k,r,prefnum,it,str(P),v)); print('best',tested,best,flush=True)
   if gap < -1e-7:
    data={'instance':inst.to_dict(),'prefix_counts':pref,'terminal':q,'profit':str(P),'v_float':v,'Q_float':[(B[i],x) for i,x in enumerate(res.x[:-1]) if x>1e-8]}
    Path(__file__).with_name('background_candidate_failure.json').write_text(json.dumps(data,indent=2)); print('FOUND',data,flush=True);return
  print('batch',k,r,prefnum,'tested',tested,'best',best,flush=True)
 print('DONE',tested,best)
if __name__=='__main__':main()
