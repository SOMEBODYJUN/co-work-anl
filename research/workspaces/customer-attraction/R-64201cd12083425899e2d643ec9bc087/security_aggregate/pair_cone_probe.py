"""Attack two-step chain using saved full policy cones, numerical LP only.

The old cones were exhausted for AGGREGATE security; that does not exhaust
the strictly stronger two-step chain inequality being tested here.
"""
import sys
sys.dont_write_bytecode=True
import importlib.util
from pathlib import Path
import argparse,gzip,json,random
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
spec=importlib.util.spec_from_file_location('old_cone_generator',ROOT/'history/source/notes/customer_attraction/transport_round/common_q_generator.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)


def distributions(f):
    k=f.shape[1]
    res=linprog(np.r_[np.zeros(k),-1.],A_ub=np.c_[-f,np.ones(len(f))],b_ub=np.zeros(len(f)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
    if not res.success:raise RuntimeError(res.message)
    return res.x[:-1],-res.ineqlin.marginals


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--iterations',type=int,default=10);ap.add_argument('--output',type=Path)
    args=ap.parse_args();rng=np.random.default_rng(615039)
    cases=json.load(gzip.open(ROOT/'evidence/certificates/customer_attraction/new_policy_security_cones.json.gz','rt'))['cases']
    space=None;best=None;solves=0
    for case in cases:
        n,k=case['players'],case['topics']
        if n!=5 or k!=7:continue
        if space is None:space=old.Space(n,k)
        policy={tuple(z['history']):z['action'] for z in case['policy']}
        cone=space.full_policy(policy)
        path=[]
        while len(path)<n:path.append(policy[tuple(path)])
        terminal=cone['realized'][0]
        d=(space.pay[terminal,path[0]]+space.pay[terminal,path[1]])/space.L
        background=space.inc[:,path[:2]].sum(axis=1)
        rivals=list(combinations_with_replacement(range(k),n-3))
        tail=np.array([space.inc.T/(1+background+space.inc[:,B].sum(axis=1))[None,:] for B in rivals])
        G=cone['gamma']/space.L
        p=np.ones(k)/k;q=np.ones(len(rivals))/len(rivals)
        for j in range(args.iterations):
            # Every third step starts at a fresh random cone extreme point;
            # this avoids remaining at the all-interest zero-gap point.
            if j%3==0:
                start=linprog(rng.normal(size=space.k),A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[np.ones(space.k)],b_eq=[1],bounds=(0,None),method='highs')
                if not start.success:raise RuntimeError(start.message)
                w=start.x
                p,_=distributions(space.static@w)
                _,q=distributions(tail@w)
            beta=np.einsum('bak,a->bk',space.static,p)
            upper=np.einsum('bak,b->ak',tail,q)
            A=np.r_[np.c_[-G,np.zeros((len(G),2))],np.c_[-beta,np.ones(len(beta)),np.zeros(len(beta))],np.c_[upper,np.zeros(k),-np.ones(k)]]
            res=linprog(np.r_[d,-n,n-2],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[np.ones(space.k),0,0]],b_eq=[1],bounds=[(0,None)]*(space.k+2),method='highs')
            solves+=1
            if not res.success:raise RuntimeError(res.message)
            if best is None or res.fun<best['gap']-1e-9:
                best={'gap':res.fun,'name':case['name'],'path':path,'p':p.tolist(),'q':q.tolist(),'rivals':rivals,'weights':res.x[:space.k].tolist()}
                print(json.dumps({'name':case['name'],'iteration':j,'gap':res.fun,'path':path}),flush=True)
            if res.fun < -1e-7:
                print('CANDIDATE FAILURE',json.dumps(best),flush=True)
                break
            p,_=distributions(space.static@res.x[:space.k]);_,q=distributions(tail@res.x[:space.k])
        if best['gap'] < -1e-7:break
    if args.output:
        with args.output.open('x') as f:json.dump({'status':'floating LP screening; not proof','solves':solves,'best':best},f,indent=2)


if __name__=='__main__':main()
