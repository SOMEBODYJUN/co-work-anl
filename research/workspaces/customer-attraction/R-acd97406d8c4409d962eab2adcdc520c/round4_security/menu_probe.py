"""Exploratory restriction of static backgrounds to actual-node reply menus.

The set-valued DP supplies genuine ordered-history SPE realizations.  Floats
are used only for the zero-sum LP score, never the sequential comparisons.
"""
from pathlib import Path
import argparse, json, random, sys, time
import numpy as np
from scipy.optimize import linprog
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'round3_security'))
from search_security import Search


def probe(s,w,restricted_path=False):
    info,O,u=s.evaluate(w,need_outcomes=True)
    welfare=s.coverage_coeff@w
    root=min(O[(0,)*s.k],key=lambda j:welfare[j])
    q=(0,)*s.k;menus=[];actions=[]
    while sum(q)<s.n:
        children=[O[c] for c in s.children[q]]
        floor=max(np.min(u[child,a]) for a,child in enumerate(children))
        a=next(a for a,child in enumerate(children)
               if root in child and u[root,a]>=floor)
        actions.append(a)
        for b,child in enumerate(children):
            dev=root if b==a else min(child,key=lambda j:u[j,b])
            counts=tuple(c-int(j==b) for j,c in enumerate(s.final[dev]))
            menus.append(counts)
        q=s.children[q][a]
    allowed=set(actions)
    if restricted_path:
        counts=[q for q in s.cts[s.n-1]
                if all(not c or j in allowed for j,c in enumerate(q))]
    else:
        counts=sorted(set(menus))
    B=np.array([s.security_coeff[s.cts[s.n-1].index(q)]@w/s.scale
                for q in counts])
    lp=linprog(np.r_[np.zeros(len(B)),1],
               A_ub=np.c_[B.T,-np.ones(s.k)],b_ub=np.zeros(s.k),
               A_eq=[np.r_[np.ones(len(B)),0]],b_eq=[1],
               bounds=[(0,None)]*len(B)+[(None,None)],method='highs')
    if not lp.success:raise RuntimeError(lp.message)
    return dict(**info,actual_path=actions,restricted_value=float(lp.x[-1]),
                restricted_gap=float(welfare[root]-s.n*lp.x[-1]),
                restricted_weak_gap=float(welfare[root]-(s.n-.5)*lp.x[-1]),
                menu_counts=[list(q) for q in counts],
                restricted_Q=[dict(counts=list(q),probability=float(p))
                              for q,p in zip(counts,lp.x[:-1]) if p>1e-9],
                restricted_query=list(map(float,-lp.ineqlin.marginals)))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=4)
    ap.add_argument('--k',type=int,default=6);ap.add_argument('--seconds',type=int,default=60)
    ap.add_argument('--trials',type=int,default=20000);ap.add_argument('--seed',type=int,default=6841)
    ap.add_argument('--path-only',action='store_true');ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();rng=random.Random(a.seed);s=Search(a.n,a.k)
    start=time.monotonic();bank=[];best=None;i=0
    while i<a.trials and time.monotonic()-start<a.seconds:
        if bank and rng.random()<.8:
            w=list(rng.choice(bank)['weights'])
            for _ in range(rng.randrange(1,5)):
                j=rng.randrange(len(w));w[j]=max(0,w[j]+rng.randint(-8,8))
        else:
            w=[rng.randrange(20) if rng.random()<rng.uniform(.1,.7) else 0
               for _ in range((1<<a.k)-1)]
        w[-1]=0
        if not any(w):continue
        z=probe(s,np.array(w,dtype=np.int64),a.path_only);i+=1
        score=z['restricted_gap']/z['min_welfare']
        z['restricted_relative_gap']=score
        if z['has_nonPNE_worst_outcome']:
            bank.append(z);bank.sort(key=lambda d:d['restricted_relative_gap']);bank=bank[:20]
        if best is None or score<best['restricted_relative_gap']-1e-10:
            best=z
            print(json.dumps(dict(trial=i,gap=z['restricted_gap'],weak=z['restricted_weak_gap'],score=score)),flush=True)
            a.output.write_text(json.dumps(dict(status='EXPLORATORY',trials=i,best=best,bank=bank),indent=2)+'\n')
        if z['restricted_weak_gap']< -1e-7:break
    a.output.write_text(json.dumps(dict(status='EXPLORATORY',seed=a.seed,trials=i,
                    elapsed=time.monotonic()-start,best=best,bank=bank),indent=2)+'\n')

if __name__=='__main__':main()
