"""Experimental finite background-aggregate security search; floats only, not certificates."""
import argparse,json,time
from functools import lru_cache
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog

def counts(k,r):
    if k==1:return [(r,)]
    return [(j,)+t for j in range(r+1) for t in counts(k-1,r-j)]

def solve(k,r,w,b):
    masks=np.arange(1,2**k); X=((masks[:,None]>>np.arange(k))&1).astype(float)
    ts=counts(k,r); T=np.array(ts); loads=X@T.T; base=X@np.array(b)
    a=(w[:,None]/np.maximum(base[:,None]+loads,1))
    U=(X.T@a).T
    P=np.sum(U*T,axis=1)
    tind={t:i for i,t in enumerate(ts)}
    @lru_cache(None)
    def rec(c):
        if sum(c)==r:return frozenset([tind[c]])
        ch=[]; lows=[]
        for j in range(k):
            cc=list(c);cc[j]+=1
            o=rec(tuple(cc));ch.append(o);lows.append(min(U[t,j] for t in o))
        threshold=max(lows)
        return frozenset(t for j,o in enumerate(ch) for t in o if U[t,j]>=threshold-1e-9)
    roots=rec((0,)*k); worst=min(roots,key=lambda t:P[t])
    hs=np.array(counts(k,r-1)); D=base[:,None]+1+X@hs.T
    mat=(X.T@(w[:,None]/D))
    lp=linprog(np.r_[np.zeros(k),-1.],A_ub=np.c_[-mat.T,np.ones(len(hs))],b_ub=np.zeros(len(hs)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
    v=lp.x[-1]
    return P[worst]/(r*v) if v>1e-9 else 1., {'P':P[worst], 'v':v, 'outcome':ts[worst], 'security_p':lp.x[:-1].tolist(), 'all_root_outcomes':len(roots)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seed',type=int,default=201);ap.add_argument('--iterations',type=int,default=1000);ap.add_argument('--topics',type=int,default=5);ap.add_argument('--remaining',type=int,default=3);ap.add_argument('--background',type=int,default=2);ap.add_argument('--output',required=True);args=ap.parse_args()
    rng=np.random.default_rng(args.seed);best=1e100;start=time.time();rec=None
    for it in range(args.iterations):
        w=rng.geometric(.15,size=2**args.topics-1).astype(float);w[rng.random(len(w))<.55]=0
        b=rng.multinomial(args.background,np.ones(args.topics)/args.topics)
        if w.sum()==0:continue
        val,data=solve(args.topics,args.remaining,w,b)
        if val<best:
            best=val;rec={'ratio':val,'iteration':it,'weights':w.astype(int).tolist(),'background':b.tolist(), 'topics':args.topics,'remaining':args.remaining,**data}
            with open(args.output,'w') as f:json.dump(rec,f,indent=2)
            print(json.dumps({'it':it,'best':best,'P':data['P'],'rv':data['v']*args.remaining}),flush=True)
        if val<1-1e-8:break
    print(json.dumps({'done':it+1,'seconds':time.time()-start,'best':best}),flush=True)
if __name__=='__main__':main()
