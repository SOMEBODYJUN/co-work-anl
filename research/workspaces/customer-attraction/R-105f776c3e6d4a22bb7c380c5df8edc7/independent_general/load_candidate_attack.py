"""Finite adversarial checks for the named full-input load certificate candidate.
Candidate: OPT_m <= sum_{covered x}(2 - 1/(c_x+1)).
This is a falsification tool; no finite success proves the candidate.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType,ExactSPESolver,verify_certificate
from fractions import Fraction
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
import random,json,time

def coefficients(k,q,a):
 return tuple(Fraction(int(mask>>a&1),sum(q[t] for t in range(k) if mask>>t&1)) if mask>>a&1 else Fraction() for mask in range(1,1<<k))

def policy_matrix(k,m,cert):
 actions=cert.actions
 def rollout(h):
  while len(h)<m:h=h+(actions[h],)
  return tuple(h.count(t) for t in range(k))
 rows=[]
 for h,a in actions.items():
  qa=rollout(h+(a,));va=coefficients(k,qa,a)
  for b in range(k):
   if b==a:continue
   vb=coefficients(k,rollout(h+(b,)),b)
   rows.append(tuple(x-y for x,y in zip(va,vb)))
 # Duplicate IC rows do not change cone.
 return tuple(set(rows))

def attack(I,S,q):
 k=I.topic_count;m=I.players
 cert=S.certificate(target_counts=q)
 rows=policy_matrix(k,m,cert)
 loads=[sum(q[t] for t in range(k) if mask>>t&1) for mask in range(1,1<<k)]
 welfare=[int(c>0) for c in loads]
 f=[Fraction(2)-Fraction(1,c+1) if c else Fraction() for c in loads]
 A=-np.array(rows,dtype=float)
 best=None
 for sz in [min(m,k)]:
  for support in combinations(range(k),sz):
   om=sum(1<<t for t in support)
   objective=[v-int(mask&om!=0) for mask,v in enumerate(f,1)]
   res=linprog(np.array(objective,dtype=float),A_ub=A,b_ub=np.zeros(len(rows)),A_eq=[welfare],b_eq=[1],bounds=(0,None),method='highs')
   if not res.success:continue
   if best is None or res.fun<best:best=res.fun
   if res.fun < -1e-8:
    weights=[Fraction(float(x)).limit_denominator(10**7) for x in res.x]
    if any(sum(a*w for a,w in zip(row,weights))<0 for row in rows):continue
    from math import lcm
    scale=lcm(*(w.denominator for w in weights))
    multiplicities=[int(w*scale) for w in weights]
    J=Instance(I.topics,tuple(CustomerType(frozenset(t for t in range(k) if mask>>t&1),v) for mask,v in enumerate(multiplicities,1) if v),m)
    report=verify_certificate(J,cert);report.assert_valid()
    F=sum((Fraction(2)-Fraction(1,c+1))*v for c,v in zip(loads,multiplicities) if c)
    if F<J.optimal_welfare():
     return {'instance':J.to_dict(),'certificate':cert.to_dict(),'terminal':q,'F':str(F),'OPT':J.optimal_welfare(),'W':J.welfare(q),'comparator':support}
 return {'lp_best':best,'rows':len(rows)}

def main():
 R=random.Random(105776);start=time.time();policies=0;best=0
 for k,m,cases in [(4,4,40),(5,5,40),(5,4,30)]:
  for z in range(cases):
   # Sparse incidence is deliberate: dense random inputs put OPT near W.
   cs=[]
   for mask in range(1,1<<k):
    if R.random() < .24:
     cs.append(CustomerType(frozenset(t for t in range(k) if mask>>t&1),R.randrange(1,10)))
   if not cs:continue
   I=Instance(tuple(map(str,range(k))),tuple(cs),m);S=ExactSPESolver(I)
   qs=sorted(S.outcomes(),key=I.welfare)[:4]
   for q in qs:
    result=attack(I,S,q);policies+=1
    if 'instance' in result:
     out=Path(__file__).with_name('load_candidate_counterexample.json');out.write_text(json.dumps(result,indent=2)+'\n')
     print('COUNTEREXAMPLE',out,result['F'],result['OPT'],flush=True);return
    best=min(best,result['lp_best'] or 0)
   if z%10==0:print('progress',k,m,z,'policies',policies,'minimum objective',best,'elapsed',round(time.time()-start,2),flush=True)
 print('NO COUNTEREXAMPLE','policies',policies,'minimum objective',best,'elapsed',round(time.time()-start,2))
if __name__=='__main__':main()
