"""Fixed complete-policy cone screen for the safety-optimal regret bridge.

Floating saddle distributions p,Q are held fixed in each linear mass-cone
optimization. A separation is a numerical candidate only, never a proof.
"""
from itertools import product, combinations_with_replacement
from pathlib import Path
import argparse, json, random, time
import numpy as np
from scipy.optimize import linprog


def run(iterations, seconds, seed):
    k=6;n=3;masks=np.arange(1,1<<k);inc=(masks[:,None]>>np.arange(k))&1
    histories=[h for d in range(n) for h in product(range(k),repeat=d)]
    def action(h):
        if not h:return 0
        if len(h)==1:return 3 if h[0]<3 else 0
        return next(a for a in (range(3) if h[-1]<3 else range(3,6)) if a not in h)
    sigma={h:action(h) for h in histories}
    def terminal(h):
        while len(h)<n:h=h+(sigma[h],)
        return h
    def row(a,z):
        load=inc[:,list(z)].sum(axis=1)
        return np.divide(inc[:,a],load,out=np.zeros(len(masks)),where=load>0)
    gamma=np.asarray([row(sigma[h],terminal(h))-row(a,terminal(h+(a,))) for h in histories for a in range(k)])
    Bs=list(combinations_with_replacement(range(k),n-1))
    beta=np.asarray([inc.T/(1+inc[:,list(B)].sum(axis=1)) for B in Bs])
    z=terminal(());load=inc[:,list(z)].sum(axis=1);covered=(load>0).astype(float)
    static=inc.T*np.where(load>0,(n+1)/(load+1),n)
    def saddle(w):
        f=beta@w
        p=linprog(np.r_[np.zeros(k),-1],A_ub=np.c_[-f,np.ones(len(Bs))],b_ub=np.zeros(len(Bs)),
                  A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
        q=linprog(np.r_[np.zeros(len(Bs)),1],A_ub=np.c_[f.T,-np.ones(k)],b_ub=np.zeros(k),
                  A_eq=[np.r_[np.ones(len(Bs)),0]],b_eq=[1],bounds=[(0,None)]*len(Bs)+[(None,None)],method='highs')
        assert p.success and q.success
        return p.x[:-1],q.x[:-1],p.x[-1]
    rng=np.random.default_rng(seed);best=None;start=time.monotonic();lastw=None
    for it in range(iterations):
        if lastw is None or it%5==0:
            ext=linprog(rng.standard_normal(len(masks)),A_ub=-gamma,b_ub=np.zeros(len(gamma)),
                        A_eq=[np.ones(len(masks))],b_eq=[1],bounds=[(0,None)]*len(masks),method='highs')
            assert ext.success
            w=ext.x
        else:w=lastw
        p,Q,v=saddle(w);root=np.einsum('baj,a->bj',beta,p);dual=np.einsum('baj,b->aj',beta,Q)
        objective=covered-p@static
        r=linprog(np.r_[objective,0],A_ub=np.r_[np.c_[-gamma,np.zeros(len(gamma))],
                    np.c_[-root,np.ones(len(Bs))],np.c_[dual,-np.ones(k)]],
                    b_ub=np.zeros(len(gamma)+len(Bs)+k),A_eq=[np.r_[np.ones(len(masks)),0]],b_eq=[1],
                    bounds=[(0,None)]*len(masks)+[(None,None)],method='highs')
        assert r.success
        lastw=r.x[:-1];p2,Q2,v2=saddle(lastw);f=beta@lastw;R=static@lastw
        minreg=linprog(R,A_ub=-f,b_ub=np.full(len(Bs),-v2+1e-9),A_eq=[np.ones(k)],b_eq=[1],bounds=[(0,None)]*k,method='highs')
        assert minreg.success
        gap=minreg.fun-covered@lastw
        if best is None or gap>best['gap']+1e-8:
            best=dict(iteration=it,gap=gap,w=lastw.tolist(),p=minreg.x.tolist(),Q=Q2.tolist(),security=v2,
                      welfare=float(covered@lastw),minimum_static_aggregate=minreg.fun,
                      fixed_saddle_objective=float(-r.fun),masks=masks.tolist(),terminal=z)
            print(json.dumps(dict(iteration=it,gap=gap,fixed_saddle=-r.fun)),flush=True)
        if gap>1e-7 or time.monotonic()-start>seconds:break
    return dict(status='floating fixed full-policy mass-cone screening; not proof',seed=seed,
                iterations=it+1,elapsed=time.monotonic()-start,best=best)


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--iterations',type=int,default=1000)
    ap.add_argument('--seconds',type=float,default=45);ap.add_argument('--seed',type=int,default=301021)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    result=run(args.iterations,args.seconds,args.seed)
    with args.output.open('x') as out:json.dump(result,out,indent=2)
