"""Finite collision-free complete-history SPE cone attack; MILP proposes only.
All claims on endpoints use exact Fraction comparison at every ordered history.
No mathematical conclusion follows from a MILP upper bound or lack of endpoints.
"""
from pathlib import Path
import sys,inspect,json,argparse,time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
import cone_attack_joint_milp as joint
from customer_attraction_strategy_lp import integer_clones,instance_from_clones,independently_verify,serializable,coverage_row,dot
from customer_attraction import StrategyCertificate,verify_certificate
src=inspect.getsource(joint.joint_candidate)
src=src.replace('hi[:n]=m','hi[:n]=m\n    rootmask=sum(1<<a for a in set(path))\n    for j in range(n):\n        if ((j+1)&rootmask).bit_count()>1:hi[j]=0')
src=src.replace("float(result.mip_gap) if hasattr(result,'mip_gap') else None","float(result.mip_gap) if getattr(result,'mip_gap',None) is not None else None")
exec(src,joint.__dict__)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=3);ap.add_argument('--topics',type=int,default=6);ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--out',required=True);a=ap.parse_args()
    p,m=a.topics,a.players;path=tuple(range(m));J=tuple(range(p-m,p))
    cone,meta=joint.joint_candidate(p,path,J,a.seconds)
    report={'scope':'finite collision-free complete-history SPE cone attack','parameters':vars(a),'milp_proposal':meta,'exact_endpoint':None}
    if cone is not None:
        rootmask=sum(1<<b for b in path);bounds=[(0,0) if (mask&rootmask).bit_count()>1 else (0,None) for mask in range(1,1<<p)]
        v=coverage_row(p,J)
        res=linprog(-np.array(v,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=[np.array(cone.welfare,dtype=float)],b_eq=[1.],bounds=bounds,method='highs')
        if res.success:
            x=tuple(F(float(z)).limit_denominator(10**7) for z in res.x)
            if not(cone.verify(x) and dot(cone.welfare,x)==1):x=cone.recover_vertex(res.x)
            if x is not None and cone.verify(x) and all(x[j]==0 for j,(lo,hi) in enumerate(bounds) if hi==0):
                clones=integer_clones(x);assert independently_verify(cone,clones)
                inst=instance_from_clones(p,m,clones);cert=StrategyCertificate(cone.actions,cone.root);verify_certificate(inst,cert).assert_valid()
                report['exact_endpoint']={'W':inst.welfare(cone.root),'OPT':inst.optimal_welfare(),'ratio':str(F(inst.optimal_welfare(),inst.welfare(cone.root))),'instance':inst.to_dict(),'strategy':cert.to_dict(),'all_history_verified':True,'objective':str(dot(v,x))}
    Path(a.out).write_text(json.dumps(serializable(report),indent=2)+'\n')
    print(json.dumps({'milp':meta,'endpoint':None if report['exact_endpoint'] is None else {k:report['exact_endpoint'][k] for k in ['W','OPT','ratio','objective']}}),flush=True)
if __name__=='__main__':main()
