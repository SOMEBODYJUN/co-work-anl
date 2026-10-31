from __future__ import annotations
import sys, json, random, time
from fractions import Fraction
from pathlib import Path
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import *
from customer_attraction_strategy_lp import *
from cone_attack_credible_variants import credible_cone
D=Path(__file__).parent
seed=37381021;rng=random.Random(seed);started=time.time()
best=Fraction(-100);records=[]
def run(p,m,weights,label):
 global best
 clones=tuple(weights.get(mask,0) for mask in range(1,1<<p))
 ins=instance_from_clones(p,m,clones);solver=ExactSPESolver(ins)
 targetsets=sorted(solver.outcomes(),key=lambda q:ins.welfare(q))[:8]
 for target in targetsets:
  for mode in ('uniform_credible','max_credible_payoff'):
   cone,stats=credible_cone(solver,target,rng,mode)
   rootact=cone.actions[()]
   # Explicit optimal portfolios, canonical p=m means one objective.
   for support in combinations(range(p),min(m,p)):
    obj=tuple(v-w-(m-1)*u for v,w,u in zip(coverage_row(p,support),cone.welfare,payoff_row(p,cone.root,rootact)))
    res=linprog(-np.array(obj,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],float),b_eq=[1],bounds=(0,None),method='highs')
    if not res.success:continue
    fval=-res.fun
    if fval<float(best)+1e-7:continue
    vals=tuple(Fraction(float(x)).limit_denominator(10**6) for x in res.x)
    if not cone.verify(vals) or dot(cone.welfare,vals)!=1: vals=cone.recover_vertex(res.x)
    if vals is None or not cone.verify(vals) or dot(cone.welfare,vals)!=1:continue
    val=dot(obj,vals)
    if val<=best:continue
    best=val;new=integer_clones(vals);ii=instance_from_clones(p,m,new)
    cert=StrategyCertificate(cone.actions,cone.root);vr=verify_certificate(ii,cert);vr.assert_valid()
    rec={'seed':seed,'label':label,'p':p,'m':m,'mode':mode,'source_weights':weights,'weights':new,'target':target,'objective':str(val),'path':vr.terminal_history,'utilities':list(map(str,ii.player_payoffs(vr.terminal_history))),'welfare':ii.welfare(cone.root),'optimum':ii.optimal_welfare(),'strategy':cert.to_dict(),'elapsed':time.time()-started}
    records.append(rec);(D/'strong_scan_best.json').write_text(json.dumps(rec));print(json.dumps({k:v for k,v in rec.items() if k not in ('strategy','weights','source_weights')}),flush=True)
    if val>0: return True
 return False
for p,m in [(5,4),(6,4),(5,5),(6,5)]:
 # Start generic sparse asymmetric sources and classic near-2 sources with sparse overlap perturbations.
 for it in range(160):
  weights={}
  if it%2==0:
   weights={1:m*rng.randint(1,4)}
   for a in range(1,p):weights[1<<a]=rng.randint(1,4)
   for j in range(rng.randrange(2*p)):
    mask=rng.randrange(1,1<<p);weights[mask]=weights.get(mask,0)+rng.randint(1,3)
  else:
   for j in range(rng.randint(p,3*p)):
    mask=rng.randrange(1,1<<p);weights[mask]=weights.get(mask,0)+rng.randint(1,10)
  if run(p,m,weights,f'random-{it}'):sys.exit(0)
  payoff_row.cache_clear()
  if it%10==0:print(json.dumps({'progress':[p,m,it],'best':str(best),'elapsed':time.time()-started}),flush=True)
print(json.dumps({'final_best':str(best),'elapsed':time.time()-started}))
