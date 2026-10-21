"""Numerical fixed complete Markov-policy cone search. No formal positive claim."""
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy import sparse
import json,time,argparse
from search import Oracle
P=Path(__file__).resolve().parent

def policy(o,w,rng):
    U=o.utility_basis@w
    out=np.arange(len(o.tq))
    gam=[];pol=[]
    for lev in range(o.m-1,-1,-1):
        nxt=[]; acts=[]
        for cs,children in enumerate(o.children[lev]):
            scores=np.array([U[out[c],a] for a,c in enumerate(children)])
            choices=np.flatnonzero(scores>=scores.max()-1e-8)
            a=int(rng.choice(choices)); z=int(out[children[a]])
            nxt.append(z);acts.append(a)
            for b,c in enumerate(children):
                if a!=b:
                    row=o.utility_basis[z,a]-o.utility_basis[out[c],b]
                    if np.any(abs(row)>1e-10):gam.append(row)
        pol.append(acts);out=np.array(nxt)
    gamma=np.unique(np.array(gam),axis=0)
    root=int(out[0]);return sparse.csr_matrix(gamma), o.cover[root].astype(float),pol,root

def optimize(o,gamma,c,p):
    beta=(o.payoff_basis*p[None,:,None]).sum(axis=1)
    lpobj=np.r_[c,-o.m]
    A=sparse.vstack([sparse.hstack([-gamma,sparse.csr_matrix((gamma.shape[0],1))]),sparse.csr_matrix(np.c_[-beta,np.ones(len(beta))]),sparse.csr_matrix(np.r_[c,0][None,:])],format='csr')
    res=linprog(lpobj,A_ub=A,b_ub=np.r_[np.zeros(A.shape[0]-1),.99],A_eq=np.array([np.r_[np.ones(len(c)),0]]),b_eq=[1],bounds=[(0,None)]*(len(c)-1)+[(0,0),(None,None)],method='highs')
    if not res.success:return None,None,None
    return -res.fun,res.x[:-1],res.x[-1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=7);ap.add_argument('--m',type=int,default=5);ap.add_argument('--iterations',type=int,default=100);ap.add_argument('--seed',type=int,default=0);a=ap.parse_args();rng=np.random.default_rng(a.seed);o=Oracle(a.k,a.m);best=-1;start=time.time()
    for j in range(a.iterations):
        seed=np.zeros(len(o.types));seed[0]=a.m
        for i in range(1,a.k):seed[(1<<i)-1]=1
        if j%4==1:
            seed[-1]=1
        elif j%4==2:
            # cross-group complement seed with equal weights
            seed=np.zeros_like(seed)
            for x in range(a.k//2):
                for y in range(a.k//2,a.k):seed[(((1<<a.k)-1)^(1<<x)^(1<<y))-1]=1
        elif j%4==3:
            seed=np.round(rng.integers(0,5,len(seed))*(o.types.sum(axis=1)<=2))
        g,c,pol,z=policy(o,seed,rng)
        p=np.ones(a.k)/a.k
        for step in range(5):
            if step==1:p=rng.dirichlet(np.ones(a.k))
            margin,w,t=optimize(o,g,c,p)
            if margin is None:break
            if margin>best+1e-9:
                best=margin;print('best',j,step,round(best,12),'rows',g.shape[0],'time',round(time.time()-start,1),flush=True)
                d={'k':a.k,'m':a.m,'j':j,'step':step,'margin':margin,'root':o.tq[z].tolist(),'p':p.tolist(),'w':w.tolist(),'policy_by_reversed_layer':pol,'seed':seed.tolist()}
                (P/f'cone-best-k{a.k}-m{a.m}-s{a.seed}.json').write_text(json.dumps(d,indent=2))
            if margin>1e-7:
                print('POSITIVE CANDIDATE',flush=True);return
            # use exact static best query for current cone-optimal customer vector
            ratio,term,p,v,W=o.solve(w)
    print('DONE',a.k,a.m,a.iterations,best,time.time()-start,flush=True)
if __name__=='__main__':main()
