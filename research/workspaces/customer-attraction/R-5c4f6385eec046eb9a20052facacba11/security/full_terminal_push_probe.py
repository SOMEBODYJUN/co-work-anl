"""Finite numerical attack on the explicit extra-one pushforward construction."""
from background_pair_probe import make_policy, matrices, OUT
import argparse,itertools,json,random
import numpy as np
from scipy.optimize import linprog

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--runs',type=int,default=300)
    ap.add_argument('--queries',type=int,default=30);ap.add_argument('--seed',type=int,default=7819288)
    args=ap.parse_args();rng=random.Random(args.seed);nr=np.random.default_rng(args.seed)
    best=-1e6
    for trial in range(args.runs):
        r=rng.choice([3,4,5]);k=rng.choice([4,5,6])
        member=np.array([[(mask>>a)&1 for mask in range(1,1<<k)]for a in range(k)])
        bg=[0]*k
        for j in range(rng.randrange(0,9)):bg[rng.randrange(k)]+=1
        w=np.array([rng.randrange(1,20)if rng.random()<.4 else 0 for mask in range(1,1<<k)],dtype=float)
        acts=make_policy(w,member,r,bg,rng);G,pair,wel,beta,z=matrices(acts,member,r,bg)
        def terminal(h):
            while len(h)<r:h=h+(acts[h],)
            return np.bincount(h,minlength=k)
        T=np.array([terminal((a,))for a in range(k)]);base=np.array(bg)@member
        c=member[z[0]]/np.maximum(base+np.sum(member[list(z)],axis=0),1)
        for query in range(args.queries):
            p=nr.dirichlet(np.ones(k)*nr.choice([.1,.3,1.,3.]))
            f=(p@member)/(1+base+p@T@member)
            ans=linprog(c-f,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=c[None,:],b_eq=[1.],bounds=(0,None),method='highs')
            if not ans.success:continue
            gap=-ans.fun
            if gap>best+1e-8:
                best=gap;print(json.dumps(dict(trial=trial,query=query,r=r,k=k,bg=bg,gap=gap)),flush=True)
            if gap>1e-7:
                packet=dict(status='numerical_only',trial=trial,r=r,k=k,background=bg,
                    weights=ans.x.tolist(),p=p.tolist(),path=z,gap=gap,
                    actions=[dict(h=h,a=a)for h,a in sorted(acts.items())])
                (OUT/'full_terminal_push_failure.json').write_text(json.dumps(packet,indent=2)+'\n')
                return
        if trial%20==0:print(json.dumps(dict(done=trial,best=best)),flush=True)
    (OUT/'full_terminal_push_numerical.json').write_text(json.dumps(dict(status='finite_no_separation',runs=args.runs,queries=args.queries,seed=args.seed,best=best),indent=2)+'\n')
    print(json.dumps(dict(status='finite_no_separation',runs=args.runs,queries=args.queries,best=best)),flush=True)

if __name__=='__main__':main()
