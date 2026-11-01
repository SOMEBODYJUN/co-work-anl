"""Numerical attack on all two-step subpath budgets in saved full policy cones.

A negative LP objective is an upper bound on the true PAIR gap at its mass
point, so it is a candidate, requiring a rational full-tree check. Nonnegative
outputs are finite exploratory evidence only.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import argparse, gzip, json, time, importlib.util
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT/'history/source/notes/customer_attraction/transport_round'))
spec = importlib.util.spec_from_file_location('q_generator', ROOT/'history/source/notes/customer_attraction/transport_round/common_q_generator.py')
old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)

def matrix(space, r, prefix):
    bg = space.inc[:,prefix].sum(axis=1) if prefix else np.zeros(space.k)
    rivals = list(combinations_with_replacement(range(space.m),r-1))
    return np.array([space.inc.T/(1+bg+space.inc[:,B].sum(axis=1))[None,:] for B in rivals]), rivals

def primal_dual(f):
    k=f.shape[1]
    z=linprog(np.r_[np.zeros(k),-1.], A_ub=np.c_[-f,np.ones(len(f))], b_ub=np.zeros(len(f)), A_eq=[np.r_[np.ones(k),0]], b_eq=[1], bounds=[(0,None)]*k+[(None,None)], method='highs')
    if not z.success: raise RuntimeError(z.message)
    return z.x[:-1],-z.ineqlin.marginals

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--iterations',type=int,default=12);ap.add_argument('--seconds',type=float,default=180);ap.add_argument('--seed',type=int,default=824177);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();rng=np.random.default_rng(args.seed);start=time.perf_counter();best=None;solves=0;events=[]
    cases=[]
    for file in ('root_tax_failure.json','global_decorrelation_failure.json'):
        z=json.loads((ROOT/'evidence/certificates/customer_attraction'/file).read_text());cases.append(dict(name=file,players=4,topics=6,policy=z['strategy']['actions']))
    cases += json.load(gzip.open(ROOT/'evidence/certificates/customer_attraction/new_policy_security_cones.json.gz','rt'))['cases']
    spaces={};done=False
    for case in cases:
        n,k=case['players'],case['topics']
        if n>5 or k>7:continue
        if (n,k) not in spaces:spaces[n,k]=old.Space(n,k)
        space=spaces[n,k];policy={tuple(z['history']):z['action'] for z in case['policy']};cone=space.full_policy(policy);G=cone['gamma']/space.L
        path=[]
        while len(path)<n:path.append(policy[tuple(path)])
        terminal=cone['realized'][0]
        for step in range(n-2):
            r=n-step;d=(space.pay[terminal,path[step]]+space.pay[terminal,path[step+1]])/space.L
            root,rootBs=matrix(space,r,path[:step]);tail,tailBs=matrix(space,r-2,path[:step+2])
            w=np.ones(space.k)/space.k
            for iteration in range(args.iterations):
                if iteration%3==0:
                    z=linprog(rng.normal(size=space.k),A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[np.ones(space.k)],b_eq=[1],bounds=(0,None),method='highs')
                    if not z.success:raise RuntimeError(z.message)
                    w=z.x
                p,_=primal_dual(root@w);_,q=primal_dual(tail@w)
                beta=np.einsum('bak,a->bk',root,p);upper=np.einsum('bak,b->ak',tail,q)
                A=np.r_[np.c_[-G,np.zeros((len(G),2))],np.c_[-beta,np.ones(len(beta)),np.zeros(len(beta))],np.c_[upper,np.zeros(k),-np.ones(k)]]
                z=linprog(np.r_[d,-r,r-2],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[np.ones(space.k),0,0]],b_eq=[1],bounds=[(0,None)]*(space.k+2),method='highs')
                if not z.success:raise RuntimeError(z.message)
                solves+=1;w=z.x[:space.k]
                if best is None or z.fun<best['gap']-1e-9:
                    best=dict(gap=float(z.fun),name=case['name'],players=n,topics=k,path=path,step=step,p=p.tolist(),q=q.tolist(),root_rivals=rootBs,tail_rivals=tailBs,weights=w.tolist())
                    event=dict(solve=solves,name=case['name'],step=step,iteration=iteration,gap=float(z.fun),elapsed=time.perf_counter()-start);events.append(event);print(json.dumps(event),flush=True)
                packet=dict(status='floating LP screening; not proof',seed=args.seed,iterations=args.iterations,seconds_requested=args.seconds,solves=solves,elapsed=time.perf_counter()-start,events=events,best=best)
                args.output.write_text(json.dumps(packet,indent=2)+'\n')
                if z.fun < -1e-7 or time.perf_counter()-start>args.seconds:done=True;break
            if done:break
        if done:break
    print(json.dumps(dict(done=True,solves=solves,elapsed=time.perf_counter()-start,best=best['gap'] if best else None)),flush=True)

if __name__=='__main__':main()
