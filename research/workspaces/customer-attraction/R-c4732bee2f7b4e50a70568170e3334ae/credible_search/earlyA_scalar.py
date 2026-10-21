"""Exact candidate search in early-A / late-reply complete strategy cones.
Search objective: (m-1)u_last-W-D, not an efficiency counterexample.
"""
import sys,json,argparse,time
from pathlib import Path
from itertools import product,combinations
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import StrategyCone,payoff_row,coverage_row,serializable,dot,integer_clones,independently_verify,instance_from_clones

def search(p,m,threshold):
    E,F=p-2,p-1
    actions={h:(0 if len(h)<m-1 or h.count(0)<threshold else E if F in h else F) for d in range(m) for h in product(range(p),repeat=d)}
    cone=StrategyCone(p,m,actions);last=actions[(0,)*(m-1)];root=cone.root
    D=tuple(Fraction(1,sum(root[a] for a in range(p) if mask&(1<<a))+1) if not mask&(1<<last) and any(root[a] and mask&(1<<a) for a in range(p)) else Fraction(0) for mask in range(1,1<<p))
    objective=tuple((m-1)*u-w-d for u,w,d in zip(payoff_row(p,root,last),cone.welfare,D))
    out=linprog(-np.array(objective,dtype=float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
    report={'m':m,'p':p,'threshold':threshold,'rows':len(cone.rows),'root':root,'floating_max_scalar':float(-out.fun) if out.fun is not None else None,'status':out.message,'scope':'fixed complete policy cone only','scalar_exact':None}
    if out.success:
        values=tuple(Fraction(float(x)).limit_denominator(10**7) for x in out.x)
        if not cone.verify(values) or dot(cone.welfare,values)!=1:values=cone.recover_vertex(out.x)
        if values is not None and cone.verify(values) and dot(cone.welfare,values)==1:
            clones=integer_clones(values);instance=instance_from_clones(p,m,clones)
            if not independently_verify(cone,clones):raise AssertionError('complete history direct')
            verify_certificate(instance,StrategyCertificate(cone.actions,cone.root)).assert_valid()
            report.update({'scalar_exact':dot(objective,values),'integer_clones':clones,'strategy':StrategyCertificate(cone.actions,cone.root).to_dict(),'W':instance.welfare(root),'OPT':instance.optimal_welfare(),'normalization':'W=1'})
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--topics',type=int,default=7);ap.add_argument('--players',type=int,default=5);ap.add_argument('--threshold',type=int);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    r=search(args.topics,args.players,args.threshold if args.threshold is not None else args.players-2)
    args.output.write_text(json.dumps(serializable(r),indent=2)+'\n');print(json.dumps(serializable({k:v for k,v in r.items() if k not in ('strategy','integer_clones')})),flush=True)
