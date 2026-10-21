"""Small matched benchmark of valid old-provider prefix payoff envelopes.

No mathematical inference is made from solver bounds or a time limit. SciPy's
MILP API has no incumbent-start argument; a known feasible threshold is an
acceptance control, not a true MIP warm start.
"""
from pathlib import Path
from itertools import product
import argparse,hashlib,json,time,warnings
import numpy as np
import scipy
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_array,vstack
import full_tree_baseline as old

def augment(model):
    m,p=model['m'],model['p'];ri=[];ci=[];data=[];lb=[];ub=[]
    def add(items,lo=-np.inf,hi=np.inf):
        row=len(lb)
        for j,v in items:
            if v:ri.append(row);ci.append(j);data.append(v)
        lb.append(lo);ub.append(hi)
    for t in range(1,m):
        for h in product(range(p),repeat=t):
            bg=[sum(bool(B>>a&1) for a in h) for B in model['masks']]
            for i,a in enumerate(h):
                # lower envelope <= real final old-player payoff <= upper.
                low=[(model['utilities'][h,i],1)]
                high=list(low)
                for j,B in enumerate(model['masks']):
                    if B>>a&1:
                        assert bg[j]>=1
                        low.append((j,-1/(bg[j]+m-t)))
                        high.append((j,-1/bg[j]))
                add(low,lo=0);add(high,hi=0)
    extra=coo_array((data,(ri,ci)),shape=(len(lb),model['n'])).tocsc()
    base=model['constraint']
    model=dict(model)
    model['constraint']=LinearConstraint(vstack([base.A,extra],format='csc'),np.r_[base.lb,lb],np.r_[base.ub,ub])
    model['rows']+=len(lb);model['prefix_rows']=len(lb)
    return model

def run(m,p,cut,fixed,seconds,seed):
    started=time.monotonic();model=old.build(m,p,0,'gap')
    portfolio=tuple(range(min(m,p)))
    c=np.zeros(model['n'])
    for j,B in enumerate(model['masks']):c[j]=-int(any(B>>a&1 for a in portfolio))
    for i in range(m):c[model['utilities'][(),i]]=1
    if fixed:
        for t in range(m):
            h=(0,)*t;model['lower'][model['choices'][h,0]]=1;model['upper'][model['choices'][h,0]]=1
        # Feasibility at the exact known all-big ratio: u1=1,W=m,OPT=2m-1.
        row=coo_array(c.reshape(1,-1)).tocsc();base=model['constraint']
        model['constraint']=LinearConstraint(vstack([base.A,row],format='csc'),np.r_[base.lb,-np.inf],np.r_[base.ub,-(m-1)])
        model['rows']+=1
    if cut:model=augment(model)
    build_seconds=time.monotonic()-started;started=time.monotonic()
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore',message='Unrecognized options detected')
        sol=milp(np.zeros_like(c) if fixed else c,integrality=model['integrality'],bounds=Bounds(model['lower'],model['upper']),constraints=model['constraint'],options={'time_limit':seconds,'mip_rel_gap':0.,'random_seed':seed,'threads':1})
    report={'m':m,'p':p,'individual_normalization':'u1=1','prefix_cuts':cut,'fixed_all_big_path_and_known_feasible_threshold':fixed,'true_mip_warm_start':False,'seed':seed,'threads':1,'time_limit':seconds,'build_seconds':build_seconds,'solver_seconds':time.monotonic()-started,'variables':model['n'],'rows':model['rows'],'nonzeros':model['constraint'].A.nnz,'status':int(sol.status),'message':sol.message,'candidate_found':sol.x is not None,'gap_objective':None if sol.x is None else float(-c@sol.x),'universal_result':False}
    for key in ('mip_node_count','mip_gap','mip_dual_bound'):
        value=getattr(sol,key,None);report[key]=None if value is None else float(value)
    return report

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=20);ap.add_argument('--seed',type=int,default=216741);ap.add_argument('--m',type=int,default=5);ap.add_argument('--p',type=int,default=7);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    baseline=Path(old.__file__)
    report={'scope':'finite matched full-tree MILP performance control, not a theorem','scipy_version':scipy.__version__,'baseline_sha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),'runs':[]}
    for fixed in (True,False):
        for cut in (False,True):
            row=run(a.m,a.p,cut,fixed,a.seconds,a.seed);report['runs'].append(row);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(row),flush=True)
