"""Discovery only: arbitrary mixtures of true root continuation backgrounds.
A positive float output must be reconstructed and audited before any claim.
"""
from pathlib import Path
from itertools import product
from functools import lru_cache
import argparse,json,math
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent

def group_policy():
    n,k=3,6
    def act(h):
        if not h:return 0
        if len(h)==1:return 3 if h[0]<3 else 0
        g=range(3) if h[1]<3 else range(3,6)
        return next(a for a in g if a not in h)
    histories=[h for d in range(n) for h in product(range(k),repeat=d)]
    @lru_cache(None)
    def out(h):
        if len(h)==n:return np.bincount(h,minlength=k)
        return out(h+(act(h),))
    return n,k,histories,act,out

def cap_lp(w,coeff):
    mat=np.einsum('bta,t->ba',coeff,w)
    r=linprog(np.r_[np.zeros(mat.shape[1]),-1],A_ub=np.c_[-mat,np.ones(len(mat))],
      b_ub=np.zeros(len(mat)),A_eq=[np.r_[np.ones(mat.shape[1]),0]],b_eq=[1],
      bounds=[(0,None)]*mat.shape[1]+[(None,None)],method='highs')
    if not r.success:raise RuntimeError(r.message)
    return r.x[:-1],r.x[-1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--starts',type=int,default=64);ap.add_argument('--factor',type=float,default=3);args=ap.parse_args()
    n,k,hs,act,out=group_policy();masks=np.arange(1,1<<k)
    bits=np.array([[(t>>a)&1 for a in range(k)] for t in masks],float)
    def row(a,z):return bits[:,a]/np.maximum(bits@z,1)
    gamma=np.array([row(act(h),out(h))-row(a,out(h+(a,))) for h in hs for a in range(k) if a!=act(h)])
    gamma=gamma[np.any(gamma!=0,axis=1)]
    bg=np.array([out((a,))-np.eye(k,dtype=int)[a] for a in range(k)])
    bg=np.unique(bg,axis=0)
    coeff=bits[None,:,:]/(1+bg@bits.T)[:,:,None]
    c=(bits@out(())>0).astype(float)
    rng=np.random.default_rng(3738);trace=[];best=None
    starts=[np.eye(k)[a] for a in range(k)]+[np.ones(k)/k]+[rng.dirichlet(np.ones(k)*.3) for _ in range(args.starts)]
    for s,p in enumerate(starts):
        last=None
        for it in range(30):
            beta=coeff@p
            r=linprog(np.r_[c,-args.factor],A_ub=np.r_[np.c_[-gamma,np.zeros(len(gamma))],np.c_[-beta,np.ones(len(beta))]],b_ub=np.zeros(len(gamma)+len(beta)),A_eq=[np.r_[np.ones(len(c)),0]],b_eq=[1],bounds=[(0,None)]*len(c)+[(None,None)],method='highs')
            if not r.success:raise RuntimeError(r.message)
            w=r.x[:-1];p,v=cap_lp(w,coeff);gap=args.factor*v-c@w
            item=dict(start=s,iteration=it,W=float(c@w),cap=float(v),gap=float(gap),p=p.tolist(),weights={int(t):float(x)for t,x in zip(masks,w)if x>1e-9})
            trace.append(item)
            if best is None or gap>best['gap']+1e-9:best=item;print(json.dumps(item),flush=True)
            if last is not None and abs(last-gap)<1e-10:break
            last=gap
    target=HERE/f'root_cap_group_factor{args.factor}.json'
    target.write_text(json.dumps(dict(status='floating discovery; no universal assertion',factor=args.factor,full_histories=len(hs),true_rows=len(gamma),root_backgrounds=bg.tolist(),seed=3738,best=best,trace=trace),indent=2))
if __name__=='__main__':main()
