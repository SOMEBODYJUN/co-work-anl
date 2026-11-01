"""Numerical discovery only. Complete count-cached SPE outcome sets + static minimax."""
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy import sparse
from itertools import product
import json,time,argparse

P=Path(__file__).resolve().parent

def comps(n,k):
    if k==1:
        yield (n,); return
    for j in range(n+1):
        for c in comps(n-j,k-1):yield (j,)+c

class Oracle:
    def __init__(self,k,m):
        self.k,self.m=k,m
        self.types=np.array([[bool(t&(1<<a)) for a in range(k)] for t in range(1,1<<k)],float)
        self.layers=[list(comps(j,k)) for j in range(m+1)]
        self.tq=np.array(self.layers[m]); self.bq=np.array(self.layers[m-1])
        self.cover=self.tq@self.types.T>0
        load=self.tq@self.types.T
        inv=np.divide(1.,load,out=np.zeros_like(load),where=load>0)
        self.utility_basis=np.stack([inv*self.types[:,a] for a in range(k)],axis=1)
        self.payoff_basis=np.stack([self.types[:,a]/(1+self.bq@self.types.T) for a in range(k)],axis=1)
        self.children={}
        index={q:i for i,q in enumerate(self.layers[m])}
        for lev in range(m-1,-1,-1):
            child_index={q:i for i,q in enumerate(self.layers[lev+1])}
            self.children[lev]=np.array([[child_index[tuple(x+(a==b) for b,x in enumerate(q))] for a in range(k)] for q in self.layers[lev]])
    def solve(self,w):
        U=self.utility_basis@w
        W=self.cover@w
        out=[np.array([j]) for j in range(len(W))]
        for lev in range(self.m-1,-1,-1):
            nxt=[]
            for children in self.children[lev]:
                floor=max(U[out[c],a].min() for a,c in enumerate(children))
                ids=np.unique(np.concatenate([out[c][U[out[c],a]>=floor-1e-8] for a,c in enumerate(children)]))
                nxt.append(ids)
            out=nxt
        minid=min(out[0],key=lambda z:W[z])
        A=self.payoff_basis@w
        c=np.r_[np.zeros(self.k),-1.]
        res=linprog(c,A_ub=np.c_[-A,np.ones(len(A))],b_ub=np.zeros(len(A)),A_eq=np.array([np.r_[np.ones(self.k),0.]]),b_eq=[1.],bounds=[(0,None)]*self.k+[(None,None)],method='highs')
        assert res.success
        return self.m*res.x[-1]/W[minid], int(minid),res.x[:-1],res.x[-1],W[minid]

def main():
    p=argparse.ArgumentParser();p.add_argument('--k',type=int,default=7);p.add_argument('--m',type=int,default=5);p.add_argument('--iterations',type=int,default=1000);p.add_argument('--seed',type=int,default=0);p.add_argument('--resume',type=Path);a=p.parse_args()
    rng=np.random.default_rng(a.seed); o=Oracle(a.k,a.m); best=0.; start=time.time(); cache=[]
    if a.resume:
        init=json.loads(a.resume.read_text())['w'];cache=[np.array(init)]
    for i in range(a.iterations):
        if cache and rng.random()<.9:
            w=cache[rng.integers(len(cache))].copy(); typ=rng.integers(4)
            if typ==0:
                pos=rng.choice(len(w),rng.integers(1,8),replace=False);w[pos]=np.maximum(0,w[pos]+rng.integers(-8,9,len(pos)))
            elif typ==1:
                pos=rng.choice(len(w),rng.integers(1,8),replace=False);w[pos]=rng.integers(0,20,len(pos))
            elif typ==2:
                w=np.round(w*rng.uniform(.7,1.3,size=len(w)))
            else:
                pos=rng.choice(len(w),rng.integers(1,6),replace=False);w[pos]=0
        else:
            density=rng.uniform(.1,.7); sizes=o.types.sum(axis=1); w=rng.integers(1,30,len(o.types))*(rng.random(len(o.types))<density)*(sizes<=rng.integers(1,4))
        w[-1]=0
        if not w.sum():continue
        ratio,term,p,v,W=o.solve(w)
        if W>=w.sum()-.5:continue
        if ratio>best+1e-9:
            best=ratio; d={'k':a.k,'m':a.m,'iteration':i,'ratio':float(ratio),'W':float(W),'v':float(v),'terminal':o.tq[term].tolist(),'p':p.tolist(),'w':[int(x) for x in w],'masks':[j+1 for j,x in enumerate(w) if x]}
            (P/f'best-k{a.k}-m{a.m}-s{a.seed}.json').write_text(json.dumps(d,indent=2)); print(i,round(best,9),round(W,5),round(v,6),round(time.time()-start,1),flush=True)
            cache.append(w.copy());cache=cache[-8:]
        elif ratio>=best*.995 and rng.random()<.2:
            cache.append(w.copy());cache=cache[-8:]
        if best>1+1e-7: print('COUNTEREXAMPLE CANDIDATE',flush=True);break
    print('DONE',a.k,a.m,a.iterations,best,time.time()-start,flush=True)
if __name__=='__main__':main()
