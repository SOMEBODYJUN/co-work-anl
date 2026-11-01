"""Finite random perturbations of sharp star / all-big instances; no theorem."""
import json,random,time
from fractions import Fraction
from customer_attraction import Instance,CustomerType,ExactSPESolver
r=random.Random(70921)
root='research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/coverage_exchange/'
best=Fraction(2)
for m,k,trial in [(3,5,500),(4,6,500),(5,7,400),(6,8,100)]:
 for z in range(trial):
  # 0 is big hub. k-1 leaves, each has shared with hub plus private.
  weights={1:r.randint(0,20)}
  for j in range(1,k):
   weights[1<<j]=r.randint(0,8)
   weights[(1<<j)|1]=r.randint(0,10)
  # A few crossing blocks permit non-sunflower retaliation.
  for _ in range(r.randint(0,8)):
   mask=0
   for j in range(k):
    if r.random()<.35:mask|=1<<j
   if mask:weights[mask]=weights.get(mask,0)+r.randint(1,6)
  cs=tuple(CustomerType(frozenset(j for j in range(k) if mask>>j&1),w) for mask,w in weights.items() if w)
  inst=Instance(tuple(map(str,range(k))),cs,m)
  opt=inst.optimal_welfare()
  if not opt:continue
  sol=ExactSPESolver(inst)
  low=[]
  for c in sol.outcomes():
   ps=inst.topic_payoffs(c)
   low.append((min(ps[j] for j in range(k) if c[j]),c))
  v,c=min(low);ratio=2*m*v/opt
  if ratio<best:
   best=ratio
   print(json.dumps({'m':m,'k':k,'trial':z,'scaled_ratio':str(ratio),'counts':c,'instance':inst.to_dict()}),flush=True)
  if ratio<1:
   print('FATAL_WEAK_INDIVIDUAL',flush=True);raise SystemExit
print('DONE',best)
