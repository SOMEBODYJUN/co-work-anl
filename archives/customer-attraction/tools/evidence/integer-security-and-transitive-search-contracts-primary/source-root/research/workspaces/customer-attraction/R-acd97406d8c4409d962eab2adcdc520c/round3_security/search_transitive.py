"""Exact symmetry-reduced search; finite evidence, not a universal theorem.

Two equal groups of topics, independent within-group permutations and swapping
the two groups.  Customer multiplicities are constant on the resulting orbits.
This topic action is transitive, so uniform query is safety-optimal by averaging.
The static minimum is an exact integer calculation with denominator k*lcm(1..n).
"""
import argparse,json,random,time
from pathlib import Path
import numpy as np
from search_security import Search


def evaluate(s,w):
    u=s.utility_coeff@w
    outcomes={q:np.array([j],dtype=int) for q,j in s.fi.items()}
    for d in reversed(range(s.n)):
        for q in s.cts[d]:
            children=[outcomes[c] for c in s.children[q]]
            floor=max(np.min(u[child,a]) for a,child in enumerate(children))
            outcomes[q]=np.unique(np.concatenate([child[u[child,a]>=floor]
                                                 for a,child in enumerate(children)]))
    roots=outcomes[(0,)*s.k];wc=s.coverage_coeff@w;W=int(np.min(wc[roots]))
    cols=(s.security_coeff@w).sum(axis=1);vm=int(np.min(cols));den=s.scale*s.k
    return dict(n=s.n,k=s.k,weights=w.tolist(),min_welfare=W,
                value_numerator=vm,value_denominator=den,
                gap_numerator=W*den-s.n*vm,
                relative_gap=(W*den-s.n*vm)/(s.n*vm) if vm else 0,
                worst_counts=[s.final[j] for j in roots if wc[j]==W],
                minimizing_backgrounds=[s.cts[s.n-1][j] for j,v in enumerate(cols) if v==vm],
                query=[1/s.k]*s.k)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=5);ap.add_argument('--group',type=int,default=3)
    ap.add_argument('--cyclic',action='store_true')
    ap.add_argument('--trials',type=int,default=30000);ap.add_argument('--seconds',type=int,default=240)
    ap.add_argument('--seed',type=int,default=76347);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();rng=random.Random(a.seed);s=Search(a.n,2*a.group)
    if a.cyclic:
        def label(mask):
            return min(tuple(np.roll(mask,r).tolist()) for r in range(s.k))
        classes=sorted({label(mask) for mask in s.masks});classes.remove((1,)*s.k)
    else:
        def label(mask):return tuple(sorted((int(mask[:a.group].sum()),int(mask[a.group:].sum()))))
        classes=sorted({label(mask) for mask in s.masks});classes.remove((a.group,a.group))
    ci={p:j for j,p in enumerate(classes)}
    orbits=[ci.get(label(mask),-1) for mask in s.masks]
    best=None;bank=[];start=time.monotonic();i=0
    while i<a.trials and time.monotonic()-start<a.seconds:
        if bank and rng.random()<.8:
            x=list(rng.choice(bank)['orbit_weights'])
            for _ in range(rng.randint(1,3)):
                j=rng.randrange(len(x));x[j]=max(0,x[j]+rng.randint(-5,5))
        else:x=[rng.randrange(16) if rng.random()<.6 else 0 for _ in classes]
        if not any(x):continue
        w=np.array([x[j] if j>=0 else 0 for j in orbits],dtype=np.int64)
        z=evaluate(s,w);z['orbit_weights']=x;i+=1
        bank.append(z);bank.sort(key=lambda b:b['relative_gap'])
        distinct=[];seen=set()
        for b in bank:
            key=tuple(b['orbit_weights'])
            if key in seen:continue
            distinct.append(b);seen.add(key)
            if len(distinct)==30:break
        bank=distinct
        if best is None or z['relative_gap']<best['relative_gap']-1e-12:
            best=z
            print(json.dumps({k:v for k,v in z.items() if k not in ('weights','query','minimizing_backgrounds','worst_counts')}),flush=True)
            a.output.write_text(json.dumps(dict(status='EXACT_FINITE_SEARCH_ONLY',trials=i,
                elapsed=time.monotonic()-start,seed=a.seed,classes=classes,best=best,bank=bank),indent=2)+'\n')
        if z['gap_numerator']<0:break
    a.output.write_text(json.dumps(dict(status='EXACT_FINITE_SEARCH_ONLY',trials=i,
        elapsed=time.monotonic()-start,seed=a.seed,classes=classes,best=best,bank=bank),indent=2)+'\n')

if __name__=='__main__':main()
