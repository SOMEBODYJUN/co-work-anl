"""Explore the insertion-credit bridge in wider completely monotone kernels.

Not CAG: resource utility is t**(load-1). Full count policies correspond to
complete ordered policies; LP serves only to find exact-auditable candidates.
"""
import argparse, json
from functools import lru_cache
from itertools import product
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

ap=argparse.ArgumentParser()
ap.add_argument('--players',type=int,default=3)
ap.add_argument('--topics',type=int,default=6)
ap.add_argument('--iterations',type=int,default=300)
ap.add_argument('--seed',type=int,default=791)
ap.add_argument('--resource-specific',action='store_true')
ap.add_argument('--random-policy',action='store_true')
ap.add_argument('--mixture',action='store_true')
args=ap.parse_args()
m,p=args.players,args.topics
rng=np.random.default_rng(args.seed)
masks=np.arange(1,1<<p)
mix_rates=[0.0,.125,.25,.5,.75,.9,1.0]
if args.mixture:
    masks=np.repeat(masks,len(mix_rates))
    fixed_rates=np.tile(mix_rates,(1<<p)-1)
inc=np.array([[int(b>>a&1) for a in range(p)]for b in masks])

def states(total,left=p):
    if left==1:
        yield (total,)
    else:
        for x in range(total+1):
            for tail in states(total-x,left-1):yield (x,)+tail
layers=[list(states(k))for k in range(m+1)]
eye=np.eye(p,dtype=int)
best=-1e9
for it in range(args.iterations):
    trials=[0.0,.01,.125,.25,.5,.75,.9]
    tv=(fixed_rates if args.mixture else
        rng.choice(trials+[1.0],size=len(masks))if args.resource_specific else
        trials[it%len(trials)])
    # Optional unstructured weight vector, still common geometric kernel.
    weights=rng.exponential(size=len(masks))*(rng.random(len(masks))<.35)
    F={}
    WF={}
    for q in layers[m]:
        c=inc@q
        factors=np.where(c>0,tv**np.maximum(c-1,0),0)
        for a in range(p):
            if q[a]:F[q,a]=inc[:,a]*factors
        WF[q]=c*factors
    final={q:q for q in layers[m]}
    sigma={}
    for depth in reversed(range(m)):
        for q in layers[depth]:
            children=[final[tuple(np.array(q)+eye[a])]for a in range(p)]
            vals=np.array([F[z,a]@weights for a,z in enumerate(children)])
            action=(int(rng.integers(p))if args.random_policy else
                    int(rng.choice(np.flatnonzero(vals>=vals.max()-1e-9))))
            sigma[q]=action
            final[q]=children[action]
    root=(0,)*p
    actual=final[root]
    rows=[]
    for depth in range(m):
        for q in layers[depth]:
            a=sigma[q]
            for b in range(p):
                other=final[tuple(np.array(q)+eye[b])]
                rows.append(F[final[q],a]-F[other,b])
    A=-np.array(rows)
    c_actual=inc@actual
    credit=c_actual*(tv**np.maximum(c_actual,0))
    for query in range(p):
        coeff=m*inc[:,query]*(tv**c_actual)+credit-2*WF[actual]
        res=linprog(-coeff,A_ub=A,b_ub=np.zeros(len(A)),
                    A_eq=WF[actual][None,:],b_eq=[1],bounds=(0,None),method='highs')
        if res.success:
            value=float(coeff@res.x)
            if value>best+1e-8:
                best=value
                print('best',it,'mixture'if args.mixture else'resource-specific'if args.resource_specific else tv,value,actual,query,flush=True)
            if value>1e-6:
                out=dict(scope='wider completely monotone geometric kernel, NOT CAG',
                         players=m,topics=p,t=(list(map(float,tv))if args.resource_specific or args.mixture else str(tv)),seed=args.seed,iteration=it,
                         query=query,actual=actual,value=value,
                         weights=[dict(mask=int(b),value=float(w),t=float(tt))for b,w,tt in zip(masks,res.x,np.broadcast_to(tv,len(masks)))if w>1e-9],
                         sigma=[dict(counts=q,action=a)for q,a in sigma.items()])
                path=Path(__file__).with_name('geometric_kernel_candidate.json')
                path.write_text(json.dumps(out,indent=2)+'\n')
                print('CANDIDATE',path,flush=True)
                raise SystemExit
print('finished',args.iterations,'best',best,flush=True)
