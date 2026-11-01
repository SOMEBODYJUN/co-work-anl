"""Exploratory alternating whole-SPE-cone / static-CCE-dual attack.

Correct minimization dual: d_z=(1-sum(lambda))*W_z+sum(lambda_a)*D_a,z,
where D_a,z=sum_i u_i(a,z_-i). Numerical candidates require exact replay.
"""
from __future__ import annotations
import argparse,json,random,time
from itertools import combinations_with_replacement
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from cone_security_search import make_policy,geometry

def cce_geometry(n,k,incidence):
    counts=np.array([np.bincount(z,minlength=k) for z in combinations_with_replacement(range(k),n)])
    loads=counts@incidence.T
    W=(loads>0).astype(float)
    H=np.where(loads>0,(n+1)/(1+loads),n)
    return W,H,counts

def cce_dual(W,H,incidence,w):
    welfare=W@w
    replacement=(H*w)@incidence
    A=(replacement-welfare[:,None]).T
    lp=linprog(welfare,A_ub=A,b_ub=np.zeros(incidence.shape[1]),A_eq=np.ones((1,len(W))),b_eq=[1],bounds=(0,None),method='highs')
    if not lp.success:raise RuntimeError(lp.message)
    lam=-lp.ineqlin.marginals
    lower=(1-lam.sum())*welfare+replacement@lam
    assert abs(min(lower)-lp.fun)<1e-5*max(1,abs(lp.fun))
    return lam,lp

def cone_step(gamma,c,W,H,incidence,lam):
    D=(1-lam.sum())*W+H*(incidence@lam)[None,:]
    A=np.vstack((np.c_[-gamma,np.zeros(len(gamma))],np.c_[-D,np.ones(len(D))]))
    b=np.zeros(len(A))
    # A universal-interest customer adds exactly the same constant to both
    # sides of the proposed bridge. It can be stripped without loss for a
    # strict counterexample and would otherwise create a trivial tie t=1.
    bounds=[(0,None)]*len(c)+[(None,None)]
    bounds[len(c)-1]=(0,0)
    lp=linprog(np.r_[np.zeros(len(c)),-1],A_ub=A,b_ub=b,A_eq=np.array([np.r_[c,0]]),b_eq=[1],bounds=bounds,method='highs')
    return lp,D

def run(args):
    rng=random.Random(args.seed);cases=[];start=time.time();lpcount=0
    for j in range(args.cases):
        n,k=args.players,args.topics
        w=np.zeros((1<<k)-1,dtype=int)
        for t in rng.sample(range(len(w)-1),min(len(w)-1,args.types)):
            w[t]=rng.randint(1,20)
        policy,instance=make_policy(n,k,w,args.seed+j)
        gamma,recip,incidence,c,z=geometry(n,k,policy)
        W,H,counts=cce_geometry(n,k,incidence)
        lam0,primal=cce_dual(W,H,incidence,w)
        starts=[lam0]
        starts += [np.array([rng.expovariate(1) for a in range(k)])*rng.uniform(.1,3)/k for s in range(args.starts-1)]
        best=-float('inf'); bestrec=None; attempts=[]
        for s,lam in enumerate(starts):
            for it in range(args.iterations):
                lp,D=cone_step(gamma,c,W,H,incidence,lam);lpcount+=1
                att=dict(start=s,iteration=it,status=int(lp.status),message=lp.message)
                if not lp.success:
                    attempts.append(att);break
                v=-lp.fun
                att.update(objective=float(v),gamma_min=float(np.min(gamma@lp.x[:-1])) if len(gamma) else 0,normalization=float(c@lp.x[:-1]),dual_slack_min=float(np.min(D@lp.x[:-1]-lp.x[-1])))
                attempts.append(att)
                lamnew,ccelp=cce_dual(W,H,incidence,lp.x[:-1])
                if ccelp.fun>best:
                    best=ccelp.fun
                    bestrec=dict(start=s,iteration=it,weights=lp.x[:-1].tolist(),lambda_values=lamnew.tolist(),cce_lower_bound=float(v),cce_value=float(ccelp.fun))
                lam=lamnew
                if ccelp.fun>1+1e-6:break
            if best>1+1e-6:break
        rec=dict(case=j,players=n,topics=k,ordered_histories=len(policy),unique_gamma_rows=len(gamma),static_profiles=len(W),root_counts=z,seed_actual_W=instance.welfare(z),seed_CCE_value=float(primal.fun),best_CCE_ratio=float(best),attempts=attempts)
        if best>1+1e-6:
            rec['witness']=bestrec
            rec['policy']=[dict(history=h,action=a) for h,a in policy.items()]
        cases.append(rec)
        print(json.dumps({q:rec[q] for q in ['case','players','topics','unique_gamma_rows','seed_actual_W','seed_CCE_value','best_CCE_ratio']}),flush=True)
        if best>1+1e-6:break
    return dict(scope='Finite numerical alternating full-policy cone / CCE-dual attack. No universal claim; all ordered histories retained.',correct_dual='(1-sum(lambda))*W+sum(lambda_a)*D_a',seed=args.seed,elapsed=time.time()-start,cone_LPs=lpcount,cases=cases)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--players',type=int,default=3);ap.add_argument('--topics',type=int,default=4);ap.add_argument('--cases',type=int,default=10);ap.add_argument('--types',type=int,default=10);ap.add_argument('--starts',type=int,default=4);ap.add_argument('--iterations',type=int,default=5);ap.add_argument('--seed',type=int,default=20261021);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();result=run(args);args.output.write_text(json.dumps(result,indent=2)+'\n')
