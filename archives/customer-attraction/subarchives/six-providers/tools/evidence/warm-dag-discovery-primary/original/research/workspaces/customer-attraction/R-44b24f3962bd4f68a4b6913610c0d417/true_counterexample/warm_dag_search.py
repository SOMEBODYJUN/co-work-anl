"""Warm-start the unrestricted outcome-witness DAG with a complete feasible seed.
Private SciPy/HiGHS API is an optional implementation dependency. Float MIP
bounds have no exact mathematical status; exported policies are independently
verified over Fraction by the prior DAG implementation.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import importlib.util
import hashlib
import math
import platform
import scipy
import json
from pathlib import Path
import sys
import time
from types import SimpleNamespace
import numpy as np
from scipy.optimize._highspy import _core as hc
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import ExactSPESolver
from customer_attraction_strategy_lp import instance_from_clones,coverage_row,dot,serializable
OLD=ROOT/'research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/true_spe_search/outcome_dag_milp.py'
spec=importlib.util.spec_from_file_location('old_dag',OLD);dag=importlib.util.module_from_spec(spec);spec.loader.exec_module(dag)


def initial_vector(p,q,clones):
    m=sum(q);n=(1<<p)-1
    if p<1 or m<1 or len(q)!=p or len(clones)!=n:raise ValueError('positive players/topics and correctly sized vectors required')
    inst=instance_from_clones(p,m,clones);solver=ExactSPESolver(inst)
    outcomes=solver.outcomes()
    if q not in outcomes:raise ValueError('seed root is not SPE-realizable')
    scale=dot(coverage_row(p,[a for a,v in enumerate(q) if v]),clones)
    if not scale:raise ValueError('seed root welfare is zero')
    states=tuple(k for depth in range(m+1) for k in dag.counts(p,depth))
    leaves=tuple(dag.counts(p,m));below={k:tuple(c for c in leaves if all(x<=y for x,y in zip(k,c))) for k in states}
    y,z,x,t={},{},{},{};idx=n
    for k in states:
        for c in below[k]:y[k,c]=idx;idx+=1
        if sum(k)<m:t[k]=idx;idx+=1
    for k in t:
        for a in range(p):
            for c in below[dag.inc(k,a)]:
                z[k,c,a]=idx;idx+=1;x[k,a,c]=idx;idx+=1
    seed=np.zeros(idx);seed[:n]=np.array(clones,dtype=float)/float(scale)
    root=(0,)*p
    for k in states:
        R=solver.outcomes(k)
        for c in R:
            if k!=root or c==q:seed[y[k,c]]=1
        if k not in t:continue
        floor=solver.threshold(k);seed[t[k]]=float(floor/scale)
        for c in R:
            if k==root and c!=q:continue
            a=next(a for a in range(p) if c in solver.outcomes(dag.inc(k,a)) and inst.topic_payoff(a,c)>=floor)
            seed[z[k,c,a]]=1
        for a in range(p):
            d=min(solver.outcomes(dag.inc(k,a)),key=lambda c:(inst.topic_payoff(a,c),c))
            seed[x[k,a,d]]=1
    return seed,{'seed_root_outcomes':len(outcomes),'seed_exact_optimum':inst.optimal_welfare(),'seed_welfare':str(scale),'seed_stats':solver.stats.__dict__}


class WarmSolver:
    def __init__(self,seed,seconds,random_seed=20261021,freeze_radius=None,use_seed=True,restrict_outcomes=None):
        self.seed=seed;self.seconds=seconds;self.random_seed=random_seed;self.freeze_radius=freeze_radius;self.use_seed=use_seed;self.restrict_outcomes=restrict_outcomes;self.info={}
    def __call__(self,c,*,integrality,bounds,constraints,options):
        from scipy.sparse import csc_matrix,vstack
        A=csc_matrix(constraints.A);lb=np.asarray(constraints.lb);ub=np.asarray(constraints.ub)
        low=np.asarray(bounds.lb).copy();high=np.asarray(bounds.ub).copy()
        if self.restrict_outcomes is not None:
            for j in self.restrict_outcomes:
                if self.seed[j]<.5:high[j]=0
        if len(c)!=len(self.seed):raise AssertionError('seed ordering mismatch')
        activity=A@self.seed
        violation=float(max(np.max(np.maximum(lb-activity,0)),np.max(np.maximum(activity-ub,0)),np.max(np.maximum(low-self.seed,0)),np.max(np.maximum(self.seed-high,0))))
        if violation>1e-8:raise AssertionError(f'initial solution violates model by {violation}')
        if self.freeze_radius is not None:
            # Local branching limits binary changes but never changes SPE validity.
            binary=np.flatnonzero(integrality);values=np.where(self.seed[binary]>.5,-1.0,1.0)
            row=csc_matrix((values,(np.zeros(len(binary)),binary)),shape=(1,len(c)))
            A=vstack([A,row],format='csc');lb=np.r_[lb,-np.inf];ub=np.r_[ub,self.freeze_radius+sum(values<0)*-1]
        lp=hc.HighsLp();lp.num_col_=len(c);lp.num_row_=A.shape[0]
        lp.col_cost_=c;lp.col_lower_=low;lp.col_upper_=high
        lp.row_lower_=lb;lp.row_upper_=ub
        lp.integrality_=[hc.HighsVarType.kInteger if z else hc.HighsVarType.kContinuous for z in integrality]
        lp.a_matrix_.num_col_=len(c);lp.a_matrix_.num_row_=A.shape[0]
        lp.a_matrix_.start_=A.indptr.astype(np.int32);lp.a_matrix_.index_=A.indices.astype(np.int32);lp.a_matrix_.value_=A.data
        h=hc._Highs();h.setOptionValue('output_flag',False);h.setOptionValue('time_limit',self.seconds)
        h.setOptionValue('random_seed',self.random_seed);h.setOptionValue('mip_rel_gap',0.0)
        h.setOptionValue('threads',1)
        passed=h.passModel(lp)
        if passed!=hc.HighsStatus.kOk:raise RuntimeError(f'model pass status {passed}')
        if self.use_seed:
            supplied=h.setSolution(len(c),np.arange(len(c),dtype=np.int32),self.seed)
            if supplied!=hc.HighsStatus.kOk:raise RuntimeError(f'seed pass status {supplied}')
        started=time.monotonic();h.run();elapsed=time.monotonic()-started
        sol=h.getSolution();info=h.getInfo();status=h.getModelStatus()
        self.info={'warm_start_supplied':self.use_seed,'warm_start_max_constraint_violation':violation,'seed_objective_float':float(-c@self.seed),'solver_status':str(status),'solver_seconds':elapsed,'mip_nodes':info.mip_node_count,'mip_gap_float':info.mip_gap if math.isfinite(info.mip_gap) else None,'dual_bound_float_not_certificate':-info.mip_dual_bound if math.isfinite(info.mip_dual_bound) else None,'local_branching_radius':self.freeze_radius,'restricted_outcome_candidates':self.restrict_outcomes is not None}
        valid=sol.value_valid
        return SimpleNamespace(x=np.array(sol.col_value) if valid else None,fun=info.objective_function_value if valid else None,status=0 if status==hc.HighsModelStatus.kOptimal else 1,message=str(status))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=5);ap.add_argument('--topics',type=int,default=7);ap.add_argument('--seed-file',type=Path);ap.add_argument('--root');ap.add_argument('--portfolio');ap.add_argument('--floor',type=float);ap.add_argument('--seconds',type=float,default=30);ap.add_argument('--seed',type=int,default=20261021);ap.add_argument('--radius',type=int);ap.add_argument('--cold',action='store_true');ap.add_argument('--restrict-outcomes',action='store_true');ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    m,p=args.players,args.topics
    if m<1 or p<1:raise ValueError('players and topics must be positive')
    q=tuple(map(int,args.root.split(','))) if args.root else (m,)+(0,)*(p-1)
    if len(q)!=p or sum(q)!=m:raise ValueError('root size mismatch')
    clones=[0]*((1<<p)-1)
    for a in range(p):clones[(1<<a)-1]=max(q[a],1)
    if args.seed_file:clones=json.loads(args.seed_file.read_text())['exact_candidate']['integer_clones']
    portfolio=tuple(map(int,args.portfolio.split(','))) if args.portfolio else tuple(sorted(range(p),key=lambda a:(-clones[(1<<a)-1],a))[:min(m,p)])
    objective=coverage_row(p,portfolio)
    start=time.monotonic();seed,meta=initial_vector(p,q,clones);meta['construction_seconds']=time.monotonic()-start
    restricted=[] if args.restrict_outcomes else None
    if restricted is not None:
        idx=(1<<p)-1
        for depth in range(m+1):
            for k in dag.counts(p,depth):
                for leaf in dag.counts(p,m):
                    if all(x<=y for x,y in zip(k,leaf)):restricted.append(idx);idx+=1
                if depth<m:idx+=1
    warm=WarmSolver(seed,args.seconds,args.seed,args.radius,use_seed=not args.cold,restrict_outcomes=restricted);dag.milp=warm
    cone,report=dag.build(p,q,objective,args.seconds,objective_floor=args.floor if args.floor is not None else float(dot(objective,clones)/dot(coverage_row(p,[a for a,v in enumerate(q) if v]),clones)))
    print(json.dumps({'stage':'mip_finished_before_exact_policy_reoptimization','output':str(args.output),'solver':warm.info}),flush=True)
    result={'scope':'warm-start full-history outcome DAG search; optional explicit subset restrictions; floating search plus exact full-policy verification','universal_bound_proved':False,'seed':args.seed,'environment':{'python':platform.python_version(),'scipy':scipy.__version__,'numpy':np.__version__,'warm_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'original_dag_sha256':hashlib.sha256(OLD.read_bytes()).hexdigest()},'parameters':{'players':m,'topics':p,'root':q,'portfolio':portfolio,'requested_solver_seconds':args.seconds,'seed_file':str(args.seed_file) if args.seed_file else None,'objective_floor':args.floor,'cold':args.cold,'local_branching_radius':args.radius,'restrict_outcomes':args.restrict_outcomes},'warm_seed':meta,'solver':warm.info,'milp':report,'exact_candidate':dag.exact_optimize(cone,objective) if cone else None}
    args.output.write_text(json.dumps(serializable(result),indent=2)+'\n')
    brief={k:v for k,v in result.items() if k!='exact_candidate'}
    if result['exact_candidate']:brief['exact_candidate']={k:v for k,v in result['exact_candidate'].items() if k not in ('strategy','integer_clones','dual_support')}
    print(json.dumps(serializable(brief)),flush=True)

if __name__=='__main__':main()
