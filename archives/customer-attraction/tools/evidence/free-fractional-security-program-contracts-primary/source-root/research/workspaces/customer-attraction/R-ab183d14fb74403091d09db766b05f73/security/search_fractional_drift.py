"""Numeric exploratory search for local free-fractional-security drift failure."""
from pathlib import Path
import sys,json,random,time,argparse
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'R-acd97406d8c4409d962eab2adcdc520c'/'round3_security'))
from search_security import Search
from fractional_minmax_probe import value

def trial(s,w):
    info,outcomes,u=s.evaluate(w,need_outcomes=True)
    q0=(0,)*s.k
    ch=[outcomes[c] for c in s.children[q0]]
    floor=max(np.min(u[child,a]) for a,child in enumerate(ch))
    v,q,p=value(s.masks,w,s.n)
    best=None
    for a,child in enumerate(ch):
        use=child[u[child,a]>=floor]
        if not len(use):continue
        z=min(use,key=lambda j:u[j,a]);ui=u[z,a]/s.scale
        vn,qn,pn=value(s.masks,w,s.n-1,s.masks[:,a])
        d=ui+(s.n-1)*vn-s.n*v
        rec=dict(debt=d,relative_debt=d/info['min_welfare'],root_value=v,next_value=vn,
                 action=a,terminal=s.final[z],utility=ui,query_load=q.tolist(),next_query_load=qn.tolist())
        if best is None or d<best['debt']:best=rec
    return dict(n=s.n,k=s.k,weights=list(map(int,w)),**best)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=3);ap.add_argument('--k',type=int,default=5)
    ap.add_argument('--seconds',type=int,default=55);ap.add_argument('--seed',type=int,default=73679)
    ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();rng=random.Random(a.seed);s=Search(a.n,a.k)
    bank=[];best=None;start=time.monotonic();i=0;err=0
    while time.monotonic()-start<a.seconds:
        if bank and rng.random()<.8:
            w=rng.choice(bank)['weights'].copy()
            for _ in range(rng.randrange(1,5)):
                j=rng.randrange(len(w));w[j]=max(0,w[j]+rng.randint(-9,9))
        else:w=[rng.randrange(15) if rng.random()<.5 else 0 for _ in range(2**a.k-1)]
        w[-1]=0
        if not any(w):continue
        try:z=trial(s,np.array(w,dtype=np.int64))
        except RuntimeError:err+=1;continue
        i+=1;bank.append(z);bank.sort(key=lambda z:z['relative_debt']);bank=bank[:20]
        if best is None or z['relative_debt']<best['relative_debt']-1e-10:
            best=z;print(json.dumps({k:v for k,v in z.items() if k not in ('weights','query_load','next_query_load')}),flush=True)
        a.output.write_text(json.dumps(dict(status='NUMERIC_EXPLORATION_ONLY',seed=a.seed,trials=i,errors=err,elapsed=time.monotonic()-start,best=best,bank=bank),indent=2)+'\n')
        if z['debt']< -1e-6:break
if __name__=='__main__':main()
