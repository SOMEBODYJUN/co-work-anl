from pathlib import Path
import sys,json,random,time
from fractions import Fraction as F
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction_strategy_lp import StrategyCone,coverage_row,payoff_row,dot,integer_clones,instance_from_clones,independently_verify,structural_seeds,cone_from_solver,serializable
from customer_attraction import ExactSPESolver,StrategyCertificate,verify_certificate
rng=random.Random(6428); out=[]
for si,clones in enumerate(structural_seeds(7,5)):
 if si>3:break
 inst=instance_from_clones(7,5,clones); solver=ExactSPESolver(inst)
 targets=sorted(solver.worst_outcomes())[:2]
 for target in targets:
  cone=cone_from_solver(solver,target,rng,True)
  for a in range(7):
   if not cone.root[a]:continue
   best=-100
   for T in combinations(range(7),5):
    obj=tuple(o-w-5*u for o,w,u in zip(coverage_row(7,T),cone.welfare,payoff_row(7,cone.root,a)))
    res=linprog(-np.array(obj,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],float),b_eq=[1],bounds=(0,None),method='highs')
    if not res.success:raise RuntimeError(res.message)
    val=-res.fun;best=max(best,val)
    if val>1e-7:
     vals=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
     if not cone.verify(vals) or dot(cone.welfare,vals)!=1:vals=cone.recover_vertex(res.x)
     if vals is None or not cone.verify(vals):raise RuntimeError('recover')
     c=integer_clones(vals);assert independently_verify(cone,c)
     candidate=instance_from_clones(7,5,c);cert=StrategyCertificate(cone.actions,cone.root);verify_certificate(candidate,cert).assert_valid()
     result=dict(instance=candidate.to_dict(),certificate=cert.to_dict(),portfolio=T,topic=a,objective=str(dot(obj,c)),normalized_objective=str(dot(obj,vals)),optimum=candidate.optimal_welfare(),welfare=candidate.welfare(cone.root))
     (Path(__file__).parent/'minimum_payoff_bridge_counterexample.json').write_text(json.dumps(result,indent=2));raise SystemExit('COUNTEREXAMPLE')
   print(si,target,a,best,flush=True);out.append(dict(seed_index=si,target=target,topic=a,max_objective=best))
(Path(__file__).parent/'sampled_bridge_extend.json').write_text(json.dumps(out,indent=2))
