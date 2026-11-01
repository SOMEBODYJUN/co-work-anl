"""Discovery: cap mixtures over true first-deviation backgrounds along actual path.
No positive float is a certificate; preserves all ordered-history incentive rows.
"""
from pathlib import Path
from itertools import product
from functools import lru_cache
import json, argparse
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent

def make_policy(n,k,w,rng,mode):
    bits=np.array([[(t>>a)&1 for a in range(k)] for t in range(1,1<<k)],float)
    acts={};outs={}
    for d in range(n,-1,-1):
        for h in product(range(k),repeat=d):
            if d==n:outs[h]=np.bincount(h,minlength=k);continue
            vals=np.array([np.sum(w*bits[:,a]/np.maximum(bits@outs[h+(a,)],1)) for a in range(k)])
            best=np.flatnonzero(vals>=np.max(vals)-1e-8)
            if mode==0:a=int(rng.choice(best))
            elif mode==1:a=int(best[0])
            else:
                # Break only actual payoff ties by harm to prefix incumbents.
                scores=[]
                for a0 in best:
                    z=outs[h+(int(a0),)]
                    scores.append(sum(np.sum(w*bits[:,b]/np.maximum(bits@z,1)) for b in h))
                a=int(best[int(np.argmin(scores))])
            acts[h]=a;outs[h]=outs[h+(a,)]
    return bits,acts,outs

def build(n,k,bits,acts,outs,full=False):
    def row(a,z):return bits[:,a]/np.maximum(bits@z,1)
    gamma=np.array([row(a0,outs[h])-row(a,outs[h+(a,)]) for h,a0 in acts.items() for a in range(k) if a!=a0])
    gamma=gamma[np.any(abs(gamma)>1e-10,axis=1)]
    bg=[];h=()
    while len(h)<n:
        for a in range(k):bg.append(outs[h+(a,)] if full else outs[h+(a,)]-np.eye(k,dtype=int)[a])
        h=h+(acts[h],)
    bg=np.unique(bg,axis=0)
    coeff=bits[None,:,:]/(1+bg@bits.T)[:,:,None]
    c=(bits@outs[()]>0).astype(float)
    return gamma,bg,coeff,c

def cap_lp(w,coeff):
    mat=np.einsum('bta,t->ba',coeff,w)
    r=linprog(np.r_[np.zeros(mat.shape[1]),-1],A_ub=np.c_[-mat,np.ones(len(mat))],b_ub=np.zeros(len(mat)),A_eq=[np.r_[np.ones(mat.shape[1]),0]],b_eq=[1],bounds=[(0,None)]*mat.shape[1]+[(None,None)],method='highs')
    if not r.success:raise RuntimeError(r.message)
    return r.x[:-1],r.x[-1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');ap.add_argument('--n',type=int,default=3);ap.add_argument('--k',type=int,default=6);ap.add_argument('--policies',type=int,default=100);ap.add_argument('--starts',type=int,default=5);a=ap.parse_args()
    n,k=a.n,a.k;rng=np.random.default_rng(48691);best=None;trace=[]
    for policy in range(a.policies):
        # Sparse integral inputs create substantial exact ties and varied policies.
        w=rng.integers(0,7,size=(1<<k)-1).astype(float)
        w[rng.random(len(w))<.7]=0
        bits,acts,outs=make_policy(n,k,w,rng,policy%3)
        gamma,bg,coeff,c=build(n,k,bits,acts,outs,a.full)
        starts=[np.ones(k)/k]+[rng.dirichlet(np.ones(k)*.4) for _ in range(a.starts)]
        for p in starts:
            last=None
            for it in range(12):
                beta=coeff@p
                r=linprog(np.r_[c,-n],A_ub=np.r_[np.c_[-gamma,np.zeros(len(gamma))],np.c_[-beta,np.ones(len(beta))]],b_ub=np.zeros(len(gamma)+len(beta)),A_eq=[np.r_[np.ones(len(c)),0]],b_eq=[1],bounds=[(0,None)]*len(c)+[(None,None)],method='highs')
                if not r.success:raise RuntimeError(r.message)
                w=r.x[:-1];p,v=cap_lp(w,coeff);gap=n*v-c@w
                if best is None or gap>best['gap']+1e-8:
                    best=dict(policy=policy,iteration=it,gap=float(gap),W=float(c@w),cap=float(v),p=p.tolist(),weights={str(t):float(x) for t,x in enumerate(w,1) if x>1e-9},backgrounds=bg.tolist(),actions=[dict(history=list(h),action=int(x)) for h,x in acts.items()])
                    print(json.dumps({key:best[key] for key in ['policy','iteration','gap','W','cap','weights','p']}),flush=True)
                    (HERE/f'path_menu_discovery_full{a.full}_n{n}_k{k}.json').write_text(json.dumps(best,indent=2))
                if last is not None and abs(gap-last)<1e-9:break
                last=gap
        if policy%20==0:print('policy',policy,flush=True)
    print('done',json.dumps({k:v for k,v in best.items() if k not in ['actions','backgrounds']}),flush=True)

if __name__=='__main__':main()
