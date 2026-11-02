"""Finite screening only; exact verification required for any reported witness."""
import sys,random,json,itertools,time
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

def screen(weights,p,m):
    types=[(tuple(a for a in range(p) if mask>>a&1),w) for mask,w in weights.items() if w]
    @lru_cache(None)
    def pay(c):
        u=[0.0]*p
        for a,w in types:
            load=sum(c[i] for i in a)
            if load:
                for i in a:
                    if c[i]:u[i]+=w/load
        return tuple(u)
    @lru_cache(None)
    def solve(c):
        if sum(c)==m:return frozenset([c])
        children=[]
        for i in range(p):
            cc=list(c);cc[i]+=1;children.append(solve(tuple(cc)))
        floor=max(min(pay(z)[i] for z in child) for i,child in enumerate(children))
        return frozenset(z for i,child in enumerate(children) for z in child if pay(z)[i]>=floor-1e-8)
    best=(float('inf'),None,None)
    for c in solve((0,)*p):
        W=0.;G=0.;madd=[0.]*p;malpha=[0.]*p
        for a,w in types:
            load=sum(c[i] for i in a)
            if load:W+=w;G+=w/(1+load)
            for i in a:madd[i]+=w/(1+load)
        gap=W+G-m*max(madd)
        if gap<best[0]:best=(gap,c,(W,G,madd))
    return best

def exact(weights,p,m,c):
    inst=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(i for i in range(p) if mask>>i&1),w) for mask,w in weights.items() if w),m)
    solver=ExactSPESolver(inst)
    if c not in solver.outcomes():return None
    W=inst.welfare(c);G=Fraction(0);v=[Fraction(0) for _ in range(p)]
    for t in inst.customers:
        load=sum(c[a] for a in t.topics)
        if load:G+=Fraction(t.multiplicity,1+load)
        for a in t.topics:v[a]+=Fraction(t.multiplicity,1+load)
    return inst,solver,W,G,v

if __name__=='__main__':
    seed=int(sys.argv[1]) if len(sys.argv)>1 else 87901
    trials=int(sys.argv[2]) if len(sys.argv)>2 else 1000
    rng=random.Random(seed);best=1e20;t=time.time()
    for it in range(trials):
        p=rng.choice([5,6,7]);m=rng.choice([3,4,5])
        weights={k:(rng.randint(1,15) if rng.random()<0.25 else 0) for k in range(1,1<<p)}
        gap,c,data=screen(weights,p,m)
        if gap<best:
            best=gap; print('BEST',it,p,m,gap,c,data,flush=True)
        if gap<-1e-7:
            out=exact(weights,p,m,c)
            if out is None: continue
            inst,solver,W,G,v=out
            egap=W+G-m*max(v)
            if egap<0:
                report={'seed':seed,'iteration':it,'instance':inst.to_dict(),'counts':c,'W':W,'G':str(G),'entrant_payoffs':list(map(str,v)),'gap':str(egap)}
                path=Path(__file__).with_name('entrant_witness.json');path.write_text(json.dumps(report,indent=2));print('WITNESS',path,flush=True);break
    print('DONE',it+1,'seconds',time.time()-t,'best',best)
