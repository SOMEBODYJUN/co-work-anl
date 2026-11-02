from pathlib import Path
import sys,json,random,gzip
from fractions import Fraction as F
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction_strategy_lp import StrategyCone,coverage_row,payoff_row,dot,integer_clones,instance_from_clones,independently_verify
from cone_attack_credible_variants import credible_cone,builtin_sources
from customer_attraction import ExactSPESolver,StrategyCertificate,verify_certificate
rng=random.Random(1728)
summary=[]
for seedlabel,instance,target in builtin_sources():
    solver=ExactSPESolver(instance)
    for mode in ['max_credible_payoff','uniform_credible','min_credible_welfare','max_credible_welfare']:
      cone,stats=credible_cone(solver,target,rng,mode)
      p,m=cone.topics,cone.players
      for a in range(p):
       if not cone.root[a]:continue
       for T in combinations(range(p),min(p,m)):
        obj=tuple(o-w-m*u for o,w,u in zip(coverage_row(p,T),cone.welfare,payoff_row(p,cone.root,a)))
        res=linprog(-np.array(obj,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],float),b_eq=[1],bounds=(0,None),method='highs')
        if not res.success:raise RuntimeError(res.message)
        val=-res.fun
        print(seedlabel,mode,a,val,flush=True)
        summary.append(dict(seed=seedlabel,mode=mode,topic=a,objective=val))
        if val>1e-7:
          vals=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
          if not cone.verify(vals) or dot(cone.welfare,vals)!=1:vals=cone.recover_vertex(res.x)
          if vals is None or not cone.verify(vals):raise RuntimeError('recover')
          clones=integer_clones(vals)
          assert independently_verify(cone,clones)
          candidate=instance_from_clones(p,m,clones)
          cert=StrategyCertificate(cone.actions,cone.root)
          verify_certificate(candidate,cert).assert_valid()
          result=dict(instance=candidate.to_dict(),certificate=cert.to_dict(),portfolio=T,topic=a,objective=str(dot(obj,clones)),normalized_objective=str(dot(obj,vals)))
          (Path(__file__).parent/'minimum_payoff_bridge_counterexample.json').write_text(json.dumps(result,indent=2))
          raise SystemExit('COUNTEREXAMPLE')
(Path(__file__).parent/'minimum_payoff_bridge_search.json').write_text(json.dumps(summary,indent=2))
