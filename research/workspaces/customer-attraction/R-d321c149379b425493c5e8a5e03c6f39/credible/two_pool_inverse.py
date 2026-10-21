"""Full-history MILP inverse probe of one-fresh-group two-pool catalog.
Floating search proposes a policy only; exact rational cone extraction follows.
"""
from pathlib import Path
import sys,json,time
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
import cone_attack_joint_milp as joint
from customer_attraction_strategy_lp import integer_clones,instance_from_clones,independently_verify,serializable
from customer_attraction import StrategyCertificate,verify_certificate


def run(seconds=60,old=0):
 k=old+1;p=4*k+2;m=3
 # Each old group is C once in fixed background. The joint tool cannot insert
 # background, so this initial probe takes only k=1.
 assert old==0
 allowed=[15,1,18,16,36,32]
 raw_bounds=joint.Bounds
 def bounds(lo,hi):
  hi=hi.copy()
  for mask in range(1,1<<p):
   if mask not in allowed:hi[mask-1]=0
  return raw_bounds(lo,hi)
 joint.Bounds=bounds
 rawcover=joint.coverage_row
 def objective_or_cover(p,J):
  J=tuple(J)
  if J==(-1,):return tuple(F(mask==1)-F(mask==15,2) for mask in range(1,1<<p))
  return rawcover(p,J)
 joint.coverage_row=objective_or_cover
 rawmilp=joint.milp
 def safemilp(*args,**kwargs):
  res=rawmilp(*args,**kwargs)
  if getattr(res,'mip_gap',None)is None:res.mip_gap=float('nan')
  return res
 joint.milp=safemilp
 cone,meta=joint.joint_candidate(p,(3,4,5),(-1,),seconds)
 report={'identity':'one-fresh-group full three-mover two-pool inverse search','floating_only':meta}
 if cone:
  objective=np.array(objective_or_cover(p,(-1,)),float)
  result=linprog(-objective,A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=[np.array(cone.welfare,float)],b_eq=[1],bounds=[(0,None)if mask in allowed else(0,0)for mask in range(1,1<<p)],method='highs')
  if result.success:
   values=tuple(F(float(v)).limit_denominator(10**7)for v in result.x)
   if not cone.verify(values)or sum(a*b for a,b in zip(cone.welfare,values))!=1: values=cone.recover_vertex(result.x)
   if values is not None and cone.verify(values)and all(not v for mask,v in enumerate(values,1)if mask not in allowed):
    clones=integer_clones(values);assert independently_verify(cone,clones)
    inst=instance_from_clones(p,m,clones);cert=StrategyCertificate(cone.actions,cone.root);verify_certificate(inst,cert).assert_valid()
    report['exact_witness']={'parameters':dict(zip(('x','a','b1','d1','b2','d2'),(clones[mask-1]for mask in allowed))),'a_minus_half_x':str(sum(a*b for a,b in zip(objective_or_cover(p,(-1,)),clones))),'instance':inst.to_dict(),'strategy':cert.to_dict()}
 out=Path(__file__).with_name('two_pool_inverse.json');out.write_text(json.dumps(serializable(report),indent=2)+'\n');print(json.dumps(serializable(report),indent=2))

if __name__=='__main__':run()
