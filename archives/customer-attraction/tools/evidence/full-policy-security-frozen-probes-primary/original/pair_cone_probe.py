"""Full policy cone numerical separation of u1+u2 >= 2*v_n."""
import json,random
from pathlib import Path
import numpy as np
from customer_attraction import Instance,CustomerType,ExactSPESolver
from probe import policy_matrix,security,cone_step
OUT=Path(__file__).resolve().parent
rng=random.Random(810734)
best=0
for n,k,runs in [(3,6,100),(4,6,100),(5,7,80),(6,7,40)]:
 for trial in range(runs):
    cs=[CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randrange(1,15)) for mask in range(1,1<<k) if rng.random()<rng.choice([.1,.3,.5,1.])]
    ins=Instance(tuple(map(str,range(k))),tuple(cs),n)
    sol=ExactSPESolver(ins)
    out=min(sol.outcomes(),key=ins.welfare)
    cert=sol.certificate(out,action_selector=lambda h,c:rng.choice(c),continuation_selector=lambda h,c:rng.choice(c))
    h=();actual=[]
    for i in range(n):a=cert.actions[h];actual.append(a);h+=(a,)
    G,c,member,R,q=policy_matrix(cert.actions,n,k)
    pair=(member[actual[0]]+member[actual[1]])/np.maximum(np.array(q)@member,1)
    w0=np.zeros((1<<k)-1)
    for cc in cs:w0[sum(1<<a for a in cc.topics)-1]=cc.multiplicity
    p,_=security(w0,member,R)
    old=-1
    for iteration in range(8):
        w,v=cone_step(G,pair,member,R,p)
        p,v=security(w,member,R)
        ratio=2*v
        if ratio>best+1e-8:
            best=ratio;print(json.dumps(dict(n=n,k=k,trial=trial,it=iteration,ratio=ratio)),flush=True)
        if ratio>1+1e-7:
            record=dict(n=n,k=k,trial=trial,ratio=ratio,weights=w.tolist(),p=p.tolist(),on_path=actual,actions={','.join(map(str,h)):int(a) for h,a in cert.actions.items()},status='numerical_only')
            (OUT/'pair_cone_failure.json').write_text(json.dumps(record,indent=2)+'\n')
            raise SystemExit
        if ratio<old+1e-9:break
        old=ratio
print('FINISHED',best,flush=True)
