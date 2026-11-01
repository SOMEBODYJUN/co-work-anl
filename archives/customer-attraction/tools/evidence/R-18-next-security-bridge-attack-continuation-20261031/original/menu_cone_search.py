"""Attack only enlarged on-path first-deviation menu; any positive is NOT BR failure."""
from pathlib import Path
import json,time,argparse
import numpy as np
from scipy.optimize import linprog
from scipy import sparse
from search import Oracle
from cone_search import policy
P=Path(__file__).resolve().parent

def support(o,pol):
    layer_index=[{q:i for i,q in enumerate(layer)} for layer in o.layers]
    def term(h):
        q=np.bincount(h,minlength=o.k)
        while len(h)<o.m:
            lev=len(h);a=pol[o.m-1-lev][layer_index[lev][tuple(q)]];q[a]+=1;h=h+(a,)
        return h
    actual=term(());menu=set()
    for i in range(o.m):
        for a in range(o.k):
            z=term(actual[:i]+(a,));menu.add(tuple(np.bincount(z[:i]+z[i+1:],minlength=o.k)))
    index={tuple(q):i for i,q in enumerate(o.bq)}
    return actual,[index[q] for q in sorted(menu)]

def wopt(o,g,c,p,menu):
    beta=(o.payoff_basis[menu]*p[None,:,None]).sum(axis=1)
    obj=np.r_[c,-o.m]
    A=sparse.vstack([sparse.hstack([-g,sparse.csr_matrix((g.shape[0],1))]),sparse.csr_matrix(np.c_[-beta,np.ones(len(beta))])],format='csr')
    res=linprog(obj,A_ub=A,b_ub=np.zeros(A.shape[0]),A_eq=np.array([np.r_[np.ones(len(c)),0]]),b_eq=[1],bounds=[(0,None)]*(len(c)-1)+[(0,0),(None,None)],method='highs');assert res.success
    return -res.fun,res.x[:-1]

def popt(o,w,menu):
    A=o.payoff_basis[menu]@w;k=o.k
    res=linprog(np.r_[np.zeros(k),-1],A_ub=np.c_[-A,np.ones(len(A))],b_ub=np.zeros(len(A)),A_eq=np.array([np.r_[np.ones(k),0]]),b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs');assert res.success
    return res.x[:-1],res.x[-1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=7);ap.add_argument('--m',type=int,default=5);ap.add_argument('--iterations',type=int,default=100);ap.add_argument('--seed',type=int,default=185);a=ap.parse_args();rng=np.random.default_rng(a.seed);o=Oracle(a.k,a.m);best=-1;start=time.time()
    for j in range(a.iterations):
        seed=np.zeros(len(o.types));seed[0]=a.m
        for i in range(1,a.k):seed[(1<<i)-1]=1
        if j%3==1:
            seed=np.zeros_like(seed)
            for x in range(a.k//2):
                for y in range(a.k//2,a.k):seed[(((1<<a.k)-1)^(1<<x)^(1<<y))-1]=1
        elif j%3==2:seed=np.round(rng.integers(0,5,len(seed))*(o.types.sum(axis=1)<=2))
        g,c,pol,z=policy(o,seed,rng);actual,menu=support(o,pol)
        p=np.ones(o.k)/o.k
        for step in range(7):
            if step in (1,4):p=rng.dirichlet(np.ones(o.k))
            gap,w=wopt(o,g,c,p,menu)
            if gap>best+1e-9:
                best=gap;print('BEST',j,step,gap,'menus',len(menu),'sec',round(time.time()-start,1),flush=True)
                d={'scope':'only on-path first-deviation menu, not full BR','k':o.k,'m':o.m,'gap':gap,'root':list(actual),'menu':[o.bq[b].tolist() for b in menu],'query':p.tolist(),'w':w.tolist(),'policy_reversed_layers':pol,'seed':seed.tolist()};(P/f'menu-cone-best-{a.seed}.json').write_text(json.dumps(d,indent=2))
            if gap>1e-7:print('POSITIVE MENU CANDIDATE',flush=True);return
            p,v=popt(o,w,menu)
    print('DONE',a.iterations,best,time.time()-start,flush=True)
if __name__=='__main__':main()
