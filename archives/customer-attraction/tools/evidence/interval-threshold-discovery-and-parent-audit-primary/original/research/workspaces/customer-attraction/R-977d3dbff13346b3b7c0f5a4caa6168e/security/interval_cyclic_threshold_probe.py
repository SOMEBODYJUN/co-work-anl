"""Discovery: interval floor versus exact cyclic fractional extra-one threshold.

The static threshold has an analytic group-averaging formula; interval DP here
is floating only. Any positive result is rerun by the Fraction implementation.
No output is an SPE counterexample: the tested floor belongs to a relaxation.
"""
from functools import lru_cache
from pathlib import Path
import argparse,json,random,sys,time
import numpy as np

OUT=Path(__file__).resolve().parent
BG=OUT.parent/'background'
sys.path.insert(0,str(BG))
sys.path.insert(0,str(OUT.parents[4]))
from interval_ceiling_dp import IntervalCeilingFloor
from customer_attraction import Instance,CustomerType
from fractions import Fraction as F


def orbits(q):
    remaining=set(range(1,(1<<q)-1));ans=[];full=(1<<q)-1
    while remaining:
        x=min(remaining);orbit=set()
        for _ in range(q):
            orbit.add(x);x=((x<<1)&full)|(x>>(q-1))
        remaining-=orbit;ans.append(tuple(sorted(orbit)))
    return ans


def screen(q,r,B,rows):
    member=np.array([[(mask>>a)&1 for mask,w in rows]for a in range(q)],dtype=float)
    wt=np.array([w for mask,w in rows],dtype=float)
    past=np.full(q,B);base=past@member
    @lru_cache(None)
    def dp(b):
        if sum(b)==r:
            den=base+np.array(b)@member
            u=member@np.divide(wt,den,out=np.zeros(len(rows)),where=den>0)
            u=np.where(np.array(b)+past>0,u,0.)
            return u,u,0.
        children=[dp(b[:a]+(b[a]+1,)+b[a+1:])for a in range(q)]
        floor=max(children[a][0][a]for a in range(q))
        E=[a for a in range(q)if children[a][1][a]>=floor-1e-11]
        return np.min([children[a][0]for a in E],axis=0),np.max([children[a][1]for a in E],axis=0),floor
    li=dp((0,)*q)[2]
    threshold=sum(F(w,1)/(1+B*mask.bit_count()+F(r*mask.bit_count(),q))for mask,w in rows if mask&1)
    return li,threshold,dp.cache_info().currsize


def exact(q,r,B,rows):
    ins=Instance(tuple(map(str,range(q))),tuple(CustomerType(frozenset(a for a in range(q)if mask>>a&1),w)for mask,w in rows),q*B+r)
    dp=IntervalCeilingFloor(ins);li=dp.floor((B,)*q)
    threshold=sum(F(w,1)/(1+B*mask.bit_count()+F(r*mask.bit_count(),q))for mask,w in rows if mask&1)
    return li,threshold


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--games',type=int,default=600);ap.add_argument('--seed',type=int,default=977410)
    a=ap.parse_args();rng=random.Random(a.seed);best=None;start=time.time();runs=[]
    for game in range(a.games):
        q=rng.choice([4,5,6,7,8]);r=rng.choice([3,4,5,6,7]);B=rng.choice([0,0,1,2,5,20,100])
        oo=orbits(q);rows=[]
        for orbit in rng.sample(oo,rng.randrange(1,min(len(oo),8)+1)):
            w=rng.choice([1,1,2,3,5,10,30]);rows.extend((mask,w)for mask in orbit)
        rows.sort();li,t,states=screen(q,r,B,rows);ratio=float(t)/li
        rec=dict(game=game,topics=q,remaining=r,uniform_past=B,LI_float=li,threshold=str(t),ratio=ratio,states=states)
        runs.append(rec)
        if best is None or ratio>best['ratio']+1e-10:
            best={**rec,'rows':rows};print(json.dumps({**rec,'elapsed':time.time()-start}),flush=True)
        if ratio>1+1e-8:
            eli,et=exact(q,r,B,rows)
            rec.update(status='exact interval threshold counterexample'if eli<et else 'float false positive',LI=str(eli),threshold=str(et),rows=rows)
            print(json.dumps(rec),flush=True)
            if eli<et:
                (OUT/'interval_threshold_candidate.json').write_text(json.dumps(rec,indent=2)+'\n');return
    result=dict(status='finite floating no separation',seed=a.seed,games=a.games,best=best,elapsed=time.time()-start,runs=runs)
    (OUT/'interval_cyclic_threshold_numerical.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='runs'}),flush=True)


if __name__=='__main__':main()
