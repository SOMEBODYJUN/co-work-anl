"""All fixed query pairs, full ordered SPE cones; floating discovery only."""
from pathlib import Path
from itertools import combinations
import numpy as np,json,argparse
from scipy.optimize import linprog
from probe_path_menu import make_policy,build
from probe_full_push import tensor
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=3);ap.add_argument('--k',type=int,default=6);ap.add_argument('--policies',type=int,default=300);a=ap.parse_args();n,k=a.n,a.k
rng=np.random.default_rng(48694);best=None
for policy in range(a.policies):
    w=rng.integers(0,7,size=(1<<k)-1).astype(float);w[rng.random(len(w))<.65]=0
    bits,acts,outs=make_policy(n,k,w,rng,policy%3);g,_,_,c=build(n,k,bits,acts,outs,True);T=tensor(n,k,bits,acts,outs)
    for x,y in combinations(range(k),2):
        d=T[x,y]+T[y,x]-2*c
        r=linprog(-d,A_ub=-g,b_ub=np.zeros(len(g)),A_eq=[np.ones(len(c))],b_eq=[1],bounds=[(0,None)]*len(c),method='highs');assert r.success
        gap=float(-r.fun)
        if best is None or gap>best['gap']+1e-9:
            best=dict(status='floating discovery only, crosscap full-terminal pair',n=n,k=k,policy=policy,gap=gap,pair=[x,y],W=float(c@r.x),weights={str(t):float(v)for t,v in enumerate(r.x,1)if v>1e-9},actions=[dict(history=list(h),action=int(v))for h,v in acts.items()])
            print(json.dumps({key:v for key,v in best.items()if key!='actions'}),flush=True);(HERE/f'crosscap_n{n}_k{k}.json').write_text(json.dumps(best,indent=2))
        if gap>1e-7:raise SystemExit('POSITIVE CANDIDATE')
    if policy%20==0:print('policy',policy,flush=True)
print('done',a.policies,flush=True)
