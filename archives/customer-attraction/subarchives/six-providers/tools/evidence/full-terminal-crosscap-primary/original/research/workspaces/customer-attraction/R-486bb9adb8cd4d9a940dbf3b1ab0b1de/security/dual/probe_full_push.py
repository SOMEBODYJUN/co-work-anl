"""Floating discovery of the all-p full-terminal push budget.
Keeps every true ordered-history SPE row. No finite negative run proves a bridge.
"""
from pathlib import Path
from itertools import combinations
import argparse,json
import numpy as np
from scipy.optimize import linprog,minimize
from probe_path_menu import make_policy,build
HERE=Path(__file__).resolve().parent

def tensor(n,k,bits,acts,outs):
    zs=[];h=()
    for i in range(n):
        zs.append([outs[h+(b,)] for b in range(k)])
        h=h+(acts[h],)
    zs=np.array(zs)
    # query a, observed b, customer type t
    return np.einsum('ibt,ta->abt',1/(1+np.einsum('ibk,tk->ibt',zs,bits)),bits)

def query_opt(mat,p0):
    k=len(p0);S=(mat+mat.T)/2;candidates=[p0]+list(np.eye(k))
    for a,b in combinations(range(k),2):
        A=S[a,a]-2*S[a,b]+S[b,b];B=2*(S[a,b]-S[b,b])
        if A<0:
            t=-B/(2*A)
            if 0<t<1:
                p=np.zeros(k);p[a]=t;p[b]=1-t;candidates.append(p)
    r=minimize(lambda p:-p@S@p,p0,jac=lambda p:-2*S@p,bounds=[(0,1)]*k,constraints=[{'type':'eq','fun':lambda p:sum(p)-1,'jac':lambda p:np.ones(k)}],method='SLSQP',options={'maxiter':300,'ftol':1e-12})
    if r.success:candidates.append(r.x)
    return max(candidates,key=lambda p:p@S@p)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=3);ap.add_argument('--k',type=int,default=6);ap.add_argument('--policies',type=int,default=100);ap.add_argument('--starts',type=int,default=5);a=ap.parse_args()
    n,k=a.n,a.k;rng=np.random.default_rng(48693);best=None
    for policy in range(a.policies):
        w=rng.integers(0,7,size=(1<<k)-1).astype(float);w[rng.random(len(w))<.6]=0
        bits,acts,outs=make_policy(n,k,w,rng,policy%3);gamma,bg,coeff,c=build(n,k,bits,acts,outs,True);T=tensor(n,k,bits,acts,outs)
        starts=[np.ones(k)/k]+[rng.dirichlet(np.ones(k)*.3)for _ in range(a.starts)]
        for p in starts:
            last=None
            for it in range(15):
                debt=np.einsum('a,b,abt->t',p,p,T)-c
                r=linprog(-debt,A_ub=-gamma,b_ub=np.zeros(len(gamma)),A_eq=[np.ones(len(c))],b_eq=[1],bounds=[(0,None)]*len(c),method='highs');assert r.success,r.message
                w=r.x;p=query_opt(T@w,p);debt=np.einsum('a,b,abt->t',p,p,T)-c;gap=float(debt@w)
                if best is None or gap>best['gap']+1e-8:
                    best=dict(status='floating discovery only, all-p full-terminal push budget',n=n,k=k,policy=policy,it=it,gap=gap,W=float(c@w),p=p.tolist(),weights={str(t):float(v)for t,v in enumerate(w,1)if v>1e-9},actions=[dict(history=list(h),action=int(v))for h,v in acts.items()])
                    print(json.dumps({key:v for key,v in best.items()if key!='actions'}),flush=True);(HERE/f'full_push_n{n}_k{k}.json').write_text(json.dumps(best,indent=2))
                if last is not None and abs(gap-last)<1e-9:break
                last=gap
        if policy%20==0:print('policy',policy,flush=True)
    print('done',a.policies,flush=True)
if __name__=='__main__':main()
