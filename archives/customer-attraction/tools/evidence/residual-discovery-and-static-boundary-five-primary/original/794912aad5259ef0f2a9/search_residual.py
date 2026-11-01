"""Explore stronger residual-cover inequality; floats screen, exact oracle confirms."""
import sys,random,itertools,json,time
from functools import lru_cache
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
OUT=Path(__file__).resolve().parent

def screen(m,k,weights):
    @lru_cache(None)
    def payoff(q):
        p=[0.0]*k
        for bits,w in weights:
            c=sum(q[a] for a in range(k) if bits>>a&1)
            if c:
                for a in range(k):
                    if bits>>a&1:p[a]+=w/c
        return p
    @lru_cache(None)
    def rec(q):
        if sum(q)==m:return (q,)
        ch=[]
        for a in range(k):
            c=list(q);c[a]+=1;ch.append(rec(tuple(c)))
        floor=max(min(payoff(t)[a] for t in cs) for a,cs in enumerate(ch))
        return tuple(set(t for a,cs in enumerate(ch) for t in cs if payoff(t)[a]>=floor-1e-8))
    for q in rec((0,)*k):
        occupied=sum((1<<a) for a in range(k) if q[a])
        w=sum(v for b,v in weights if b&occupied)
        remaining=[(b,v) for b,v in weights if not b&occupied]
        # Residual clients cannot like occupied actions, so consider only remaining actions.
        avail=[a for a in range(k) if not q[a]]
        r=max((sum(v for b,v in remaining if b&sum(1<<a for a in acts)) for acts in itertools.combinations(avail,min(m,len(avail)))),default=0)
        if r>w:
            ins=Instance(tuple(map(str,range(k))),tuple(CustomerType(frozenset(a for a in range(k) if b>>a&1),v) for b,v in weights),m)
            ex=ExactSPESolver(ins)
            if q in ex.outcomes():return q,w,r,ins.to_dict()
    return None

def main():
    rng=random.Random(993421);start=time.time();best=0
    trials=int(sys.argv[1]) if len(sys.argv)>1 else 1000
    for n in range(trials):
        m=rng.choice([2,3,4,5]);k=rng.choice([5,6,7,8])
        density=rng.choice([.2,.3,.45,.6])
        weights=[]
        for b in range(1,1<<k):
            if rng.random()<density:weights.append((b,rng.choice([1,1,2,3,5,8,13])))
        res=screen(m,k,weights)
        if res:
            data={'trial':n,'m':m,'k':k,'outcome':res[0],'welfare':res[1],'residual_opt':res[2],'instance':res[3]}
            (OUT/'residual_counterexample.json').write_text(json.dumps(data,indent=2))
            print(json.dumps(data));return
        if n%25==0:print('checked',n,'seconds',round(time.time()-start,1),flush=True)
    print('no witness',trials,'seconds',time.time()-start)
if __name__=='__main__':main()
