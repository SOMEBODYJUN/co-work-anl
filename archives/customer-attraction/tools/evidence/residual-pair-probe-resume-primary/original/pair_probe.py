"""Screen two-step security-chain balances.  LP is numerical only."""
import argparse
import json
from pathlib import Path
import random
import numpy as np
from scipy.optimize import linprog
from probe import probe, multisets


def security(k,r,w,prefix):
    masks=np.arange(1,1<<k,dtype=np.int64)
    inc=((masks[:,None]>>np.arange(k))&1)
    bg=inc@np.bincount(prefix,minlength=k)
    f=np.array([(np.array(w)/(bg+inc@np.array(q)+1))@inc for q in multisets(k,r-1)])
    z=linprog(np.r_[np.zeros(k),-1.],A_ub=np.c_[-f,np.ones(len(f))],b_ub=np.zeros(len(f)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
    if not z.success: raise RuntimeError(z.message)
    return z.x[-1]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--samples',type=int,default=500)
    ap.add_argument('--k',type=int,default=7)
    ap.add_argument('--r',type=int,default=5)
    ap.add_argument('--background',type=int,default=0)
    ap.add_argument('--seed',type=int,default=717290)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    rng=random.Random(args.seed)
    best=None
    for i in range(args.samples):
        density=rng.choice((.1,.3,1.))
        w=[rng.randint(1,10) if rng.random()<density else 0 for _ in range((1<<args.k)-1)]
        prefix=tuple(rng.randrange(args.k) for _ in range(args.background))
        z=probe(args.k,args.r,w,prefix)
        path=z['ordered_path']
        v=[security(args.k,args.r-j,w,prefix+tuple(path[:j])) for j in range(args.r)]
        for j in range(args.r-2):
            r=args.r-j
            pair=sum(z['path_payoffs'][j:j+2])+(r-2)*v[j+2]-r*v[j]
            if best is None or pair<best['pair']-1e-9:
                best={'pair':pair,'step':j,'values':v,'instance':z}
                print(json.dumps({'sample':i,'pair':pair,'step':j,'values':v,'path':path,'payoffs':z['path_payoffs']}),flush=True)
            if pair < -1e-7:
                print('CANDIDATE FAILURE',json.dumps(best),flush=True)
                break
        if best['pair'] < -1e-7:
            break
    if args.output:
        with args.output.open('x') as f:
            json.dump({'status':'floating LP screening; not proof','samples_requested':args.samples,'seed':args.seed,'best':best},f,indent=2)


if __name__=='__main__':main()
