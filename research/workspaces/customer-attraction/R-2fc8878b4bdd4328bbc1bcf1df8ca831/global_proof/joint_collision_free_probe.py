"""Low-budget full-history MILP proposals with actual client load at most one.
No floating MIP bound is a theorem. Each extracted policy is reoptimized by a
restricted strategy-cone LP and exactly verified before a witness is emitted.
"""
import sys,json,argparse
from pathlib import Path
from fractions import Fraction
from math import lcm
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5];sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
import cone_attack_joint_milp as joint
from customer_attraction_strategy_lp import independently_verify,integer_clones,instance_from_clones,serializable
from customer_attraction import StrategyCertificate,verify_certificate
OUT=Path(__file__).parent

def run(p,m,seconds,start_k):
 path=tuple(range(m));forbidden=[sum((mask>>a)&1 for a in path)>1 for mask in range(1,1<<p)]
 original=joint.Bounds
 def collision_bounds(lo,hi):
  hi=hi.copy();hi[:len(forbidden)][np.array(forbidden)]=0
  return original(lo,hi)
 joint.Bounds=collision_bounds
 original_milp=joint.milp
 def safe_milp(*args,**kwargs):
  res=original_milp(*args,**kwargs)
  if getattr(res,'mip_gap',None)is None:res.mip_gap=float('nan')
  return res
 joint.milp=safe_milp
 report=[]
 for k in range(max(start_k,0,2*m-p),m):
  portfolio=tuple(range(k))+tuple(range(m,m+(m-k)))
  cone,meta=joint.joint_candidate(p,path,portfolio,seconds);record={'m':m,'p':p,'path':path,'portfolio':portfolio,'floating_MILP':meta};print('milp',m,p,k,meta,flush=True)
  if cone is not None:
   objective=joint.coverage_row(p,portfolio)
   res=linprog(-np.array(objective,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=[np.array(cone.welfare,float)],b_eq=[1.],bounds=[(0,0)if no else (0,None)for no in forbidden],method='highs')
   if res.success:
    values=tuple(Fraction(float(v)).limit_denominator(10**7)for v in res.x)
    if not cone.verify(values)or sum(a*b for a,b in zip(cone.welfare,values))!=1:values=cone.recover_vertex(res.x)
    if values is not None and cone.verify(values)and all(not v for v,no in zip(values,forbidden)if no):
     clones=integer_clones(values);assert independently_verify(cone,clones);inst=instance_from_clones(p,m,clones);cert=StrategyCertificate(cone.actions,cone.root);ver=verify_certificate(inst,cert);ver.assert_valid();actual=ver.terminal_history
     cover_sets=[frozenset(i for i,t in enumerate(inst.customer_types)if a in t.topics)for a in range(p)] if hasattr(inst,'customer_types')else []
     record['exact_witness']={'ratio':Fraction(inst.optimal_welfare(),inst.welfare(cone.root)),'instance':inst.to_dict(),'strategy':cert.to_dict(),'actual':actual,'W':inst.welfare(cone.root),'OPT':inst.optimal_welfare()};print('exact',serializable(record['exact_witness']['ratio']),flush=True)
  report.append(record);(OUT/f'joint_collision_free_m{m}p{p}_k{start_k}.json').write_text(json.dumps(serializable(report),indent=2)+'\n')
 joint.Bounds=original; joint.milp=original_milp
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--p',type=int,default=6);a.add_argument('--m',type=int,default=3);a.add_argument('--seconds',type=float,default=20);a.add_argument('--start-k',type=int,default=0);x=a.parse_args();run(x.p,x.m,x.seconds,x.start_k)
