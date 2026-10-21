"""Minimize first-player share in sampled credible strategy cones, exact primal acceptance."""
from pathlib import Path
from fractions import Fraction
import sys,json,random,time
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5];sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction import ExactSPESolver,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import instance_from_clones,integer_clones,payoff_row,dot,serializable,independently_verify
from cone_attack_credible_variants import credible_cone

def run():
 rng=random.Random(128420);p=7;m=5;weights={16|32:12,16|64:12}
 for j,a in enumerate((4,5,6,7)):weights[1<<j]=a;weights[(1<<j)|32|64]=4
 source=tuple(weights.get(mask,0) for mask in range(1,1<<p));target=(0,0,0,1,1,1,2)
 best=Fraction(8,47);bestrecord=None;log=[];start=time.monotonic()
 for step in range(12):
  ins=instance_from_clones(p,m,source);solver=ExactSPESolver(ins)
  class Choice:
   first=True
   def choice(self,c):
    if self.first:self.first=False;return min(c,key=lambda a:solver._utility(target,a))
    return rng.choice(c)
  cone,stats=credible_cone(solver,target,Choice(),rng.choice(('uniform_credible','max_credible_payoff','min_credible_welfare','max_credible_welfare')))
  first=cone.actions[()];row=payoff_row(p,cone.root,first)
  res=linprog(np.array(row,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
  if not res.success:continue
  vals=tuple(Fraction(float(v)).limit_denominator(10**7) for v in res.x)
  if not cone.verify(vals) or dot(cone.welfare,vals)!=1:vals=cone.recover_vertex(res.x)
  if vals is None or not cone.verify(vals) or dot(cone.welfare,vals)!=1:continue
  point=integer_clones(vals);candidate=instance_from_clones(p,m,point);cert=StrategyCertificate(cone.actions,cone.root);verify_certificate(candidate,cert).assert_valid()
  share=dot(row,vals);record={'step':step,'root_share':share,'root_counts':cone.root,'W':candidate.welfare(cone.root),'OPT':candidate.optimal_welfare(),'stats':stats,'seconds':time.monotonic()-start};log.append(record);print(json.dumps(serializable(record)),flush=True)
  if share<=best:
   if not independently_verify(cone,point):raise AssertionError('full independent exact')
   best=share;bestrecord={'clones':point,'strategy':cert.to_dict(),'root_share':share,'W':candidate.welfare(cone.root),'OPT':candidate.optimal_welfare(),'source_clones':source,'target':target,'seed':128420,'step':step};source=point
  # The source policy target stays fixed; every endpoint was verified in this cone.
 out=Path(__file__).parent
 (out/'minimum_root_summary.json').write_text(json.dumps(serializable(log),indent=2)+'\n')
 if bestrecord:(out/'minimum_root_best.json').write_text(json.dumps(serializable(bestrecord),indent=2)+'\n')
if __name__=='__main__':run()
