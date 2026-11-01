#!/usr/bin/env python3
"""Numerical fixed-full-policy cone probe for m*u_last <= 2W; no theorem."""
from pathlib import Path
import sys,random,json,time
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
import numpy as np
from scipy.optimize import linprog
from customer_attraction import ExactSPESolver
from customer_attraction_strategy_lp import StrategyCone,payoff_row,instance_from_clones,integer_clones,dot,serializable,independently_verify
from cone_attack_credible_variants import credible_cone

rng=random.Random(431903)
start=time.time();best=Fraction(0);records=[];trials=0
for players,topics,count in [(3,5,300),(4,5,300),(5,5,300),(6,5,300)]:
 for it in range(count):
  weights=[0]*((1<<topics)-1)
  for mask in rng.sample(range(1,1<<topics),rng.randrange(5,16)):
   weights[mask-1]=rng.randrange(1,15)
  instance=instance_from_clones(topics,players,weights)
  solver=ExactSPESolver(instance)
  targets=sorted(solver.outcomes())
  target=rng.choice(targets)
  cone,_=credible_cone(solver,target,rng,rng.choice(['uniform_credible','max_credible_payoff','min_credible_welfare']))
  path=()
  while len(path)<players:path+=(cone.actions[path],)
  last=path[-1]
  objective=tuple(players*v for v in payoff_row(topics,cone.root,last))
  res=linprog(-np.array(objective,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
  trials+=1
  if not res.success:continue
  value=-res.fun
  if value>float(best)+1e-8:
   vals=tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
   if not cone.verify(vals) or dot(cone.welfare,vals)!=1: vals=cone.recover_vertex(res.x)
   if vals is None or not cone.verify(vals) or dot(cone.welfare,vals)!=1:continue
   exact=dot(objective,vals)
   if exact<=best:continue
   best=exact;clones=integer_clones(vals)
   assert independently_verify(cone,clones)
   record={'players':players,'topics':topics,'iteration':it,'trials':trials,'value':str(best),'path':path,'clones':clones,'actions':[{'history':h,'action':a} for h,a in sorted(cone.actions.items())]}
   records.append(record)
   print(json.dumps({'players':players,'iteration':it,'value':str(best),'seconds':time.time()-start}),flush=True)
   Path(__file__).with_name('terminal_cap_probe.json').write_text(json.dumps(serializable({'seed':431903,'trials':trials,'records':records}),indent=2)+'\n')
   if best>2:raise SystemExit('Exact candidate refutes cap')
print('FINAL',trials,best,time.time()-start)
