"""Exploratory LP attack on the virtual entrant aggregate cap; no general claim."""
from itertools import product
from fractions import Fraction
from random import Random
import json
import numpy as np
from scipy.optimize import linprog
from customer_attraction import CustomerType, Instance, ExactSPESolver, verify_certificate


def rollout(actions,h,m):
 h=tuple(h)
 while len(h)<m:h=h+(actions[h],)
 return h

def coeff(z,i,mask):
 return Fraction(1,sum((mask>>a)&1 for a in z)) if mask>>z[i]&1 else Fraction()

def build(actions,k,m):
 masks=list(range(1,1<<k));rows=[];labels=[]
 for i in range(m):
  for h in product(range(k),repeat=i):
   z=rollout(actions,h,m)
   for a in range(k):
    if a==actions[h]:continue
    y=rollout(actions,h+(a,),m)
    rows.append([coeff(z,i,t)-coeff(y,i,t) for t in masks]);labels.append((h,a))
 return masks,rows,labels

def scan(seed=67,trials=300):
 rng=Random(seed)
 for it in range(trials):
  k=rng.choice([3,4,5,6]);m=rng.choice([2,3,4,5]);
  # Favor private and sparse customer types.
  cs=[]
  for mask in range(1,1<<k):
   if rng.random() < (0.7 if mask.bit_count()<=2 else 0.15):
    cs.append(CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randrange(1,20)))
  ins=Instance(tuple(map(str,range(k))),tuple(cs),m);sol=ExactSPESolver(ins)
  outs=sorted(sol.outcomes());q=rng.choice(outs)
  cert=sol.certificate(q,action_selector=lambda h,aa:rng.choice(aa),continuation_selector=lambda h,aa:rng.choice(aa))
  masks,rows,labels=build(cert.actions,k,m);A=np.array(rows,dtype=float)
  root=rollout(cert.actions,(),m)
  c=np.array([int(any(t>>a&1 for a in root)) for t in masks])
  for T in range(k):
   g=np.array([float((Fraction(m,1+sum(t>>a&1 for a in root)) if t>>T&1 else Fraction()) - (Fraction(1,1+sum(t>>a&1 for a in root)) if c[j] else Fraction()))-c[j] for j,t in enumerate(masks)])
   res=linprog(-g,A_ub=-A,b_ub=np.zeros(len(A)),A_eq=np.ones((1,len(masks))),b_eq=[1],bounds=(0,None),method='highs')
   if res.success and -res.fun>1e-8:
    out={'trial':it,'k':k,'m':m,'root':root,'T':T,'objective':-res.fun,'seed_instance':ins.to_dict(),'weights':[float(v) for v in res.x], 'actions':[{ 'history':h, 'action':a} for h,a in cert.actions.items()]}
    print(json.dumps(out));return out
  if it%20==0:print('progress',it,flush=True)
 print('NO_COUNTEREXAMPLE')
if __name__=='__main__': scan()
