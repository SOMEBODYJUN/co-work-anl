"""Attack individual fractional floor and one inductive sufficient lemma."""
from fractional_explore import benchmark
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
from pathlib import Path
import random,json,itertools
rng=random.Random(77128912)
for n in [3,4,5,6]:
 for trial in range(200):
  k=6
  ts=[]
  for mask in range(1,1<<k):
   if rng.random()<.22:ts.append(CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randrange(1,10)))
  ins=Instance(tuple(map(str,range(k))),tuple(ts),n)
  m,_=benchmark(ins,(0,)*k)
  solver=ExactSPESolver(ins); floor=solver.threshold((0,)*k)
  if float(floor)<m-1e-6:
   out={'kind':'individual_floor','instance':ins.to_dict(),'M':m,'floor':str(floor)}
   Path(__file__).with_name('fractional_floor_obstruction.json').write_text(json.dumps(out,indent=2))
   print('FLOOR COUNTER',n,trial,float(floor),m,flush=True);raise SystemExit
  witness={}
  for bs in itertools.combinations_with_replacement(range(k),n-1):
   for a in range(k):
    q=ins.counts(bs+(a,)); pay=ins.topic_payoffs(q)
    if float(pay[a])<m-1e-6 and min(float(pay[b]) for b in bs)>=m+1e-6:
     witness[a]=list(bs)
  if len(witness)==k:
   out={'kind':'threshold_safe_action','instance':ins.to_dict(),'M':m,'witness':witness,'floor':str(floor)}
   Path(__file__).with_name('fractional_induction_obstruction.json').write_text(json.dumps(out,indent=2))
   print('INDUCTION COUNTER',n,trial,float(floor),m,flush=True);raise SystemExit
 print('finished',n,flush=True)
