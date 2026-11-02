"""Unrestricted random full formal policies; all-interest makes every cone nonempty."""
import json, random
from pathlib import Path
import numpy as np
from customer_attraction.certificate import StrategyCertificate
from probe import policy_matrix,security,cone_step
from leaf_support_probe import bg_support
OUT=Path(__file__).resolve().parent
rng=random.Random(1772102)
best=0
for n,k,runs in [(3,4,300),(3,5,300),(4,4,300),(4,5,200),(5,5,100)]:
 for trial in range(runs):
    actions={}
    def choose(h):
        if len(h)==n:return h
        a=rng.randrange(k);actions[h]=a
        chosen=None
        for b in range(k):
            r=choose(h+(b,))
            if b==a:chosen=r
        return chosen
    actual=choose(())
    cert=StrategyCertificate(actions,tuple(actual.count(a) for a in range(k)))
    G,c,member,R,q=policy_matrix(actions,n,k)
    bgs,_=bg_support(cert,n,k)
    RR=1/(1+np.array(bgs)@member)
    for st in range(2):
        p=np.ones(k)/k if st==0 else np.random.default_rng(100000*n+1000*k+trial).dirichlet(np.ones(k))
        old=-1
        for iteration in range(4):
            w,v=cone_step(G,c,member,RR,p)
            p,v=security(w,member,RR)
            ratio=n*v
            if ratio>best+1e-8:
                best=ratio
                print(json.dumps(dict(n=n,k=k,trial=trial,st=st,iteration=iteration,ratio=ratio)),flush=True)
            if ratio>1+1e-7:
                rec=dict(n=n,k=k,trial=trial,st=st,iteration=iteration,ratio=ratio,weights=w.tolist(),p=p.tolist(),on_path=q,backgrounds=bgs,actions={','.join(map(str,h)):a for h,a in actions.items()})
                (OUT/'random_policy_failure.json').write_text(json.dumps(rec,indent=2)+'\n')
                _,vf=security(w,member,R)
                print('RESTRICTION_FAIL',ratio,'TRUE_RATIO',n*vf,flush=True)
                raise SystemExit
            if ratio<old+1e-9:break
            old=ratio
print('FINISHED',best,flush=True)
