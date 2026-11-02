"""Probe one-deviation leaf deletion support (a candidate restriction only)."""
import json, math, random
from pathlib import Path
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance,CustomerType,ExactSPESolver
from probe import policy_matrix,security,cone_step
OUT=Path(__file__).resolve().parent
rng=random.Random(517082193)

def bg_support(cert,n,k,depth=1):
    leaves=[]
    def walk(h,d):
        if len(h)==n:
            leaves.append(h);return
        s=cert.actions[h]
        walk(h+(s,),d)
        if d<depth:
            for a in range(k):
                if a!=s:walk(h+(a,),d+1)
    walk((),0)
    bgs=set()
    for h in leaves:
        for i in range(n):
            b=h[:i]+h[i+1:]
            bgs.add(tuple(b.count(a) for a in range(k)))
    return sorted(bgs),leaves

def run(ins,name,best):
    n=ins.players;k=ins.topic_count
    solver=ExactSPESolver(ins)
    cert=solver.certificate(min(solver.outcomes(),key=ins.welfare),action_selector=lambda h,c:rng.choice(c),continuation_selector=lambda h,c:rng.choice(c))
    G,c,member,R,actual=policy_matrix(cert.actions,n,k)
    bgs,leaves=bg_support(cert,n,k)
    RR=1/(1+np.array(bgs)@member)
    w=np.zeros((1<<k)-1)
    for cc in ins.customers:
        mask=sum(1<<a for a in cc.topics)
        if mask:w[mask-1]=cc.multiplicity
    p,v=security(w,member,RR)
    observed=n*v/(c@w) if c@w else 1
    if observed>1+1e-7:
        print('INPUT_FAIL',name,observed,flush=True)
    for iteration in range(8):
        w,v=cone_step(G,c,member,RR,p)
        p,v=security(w,member,RR)
        ratio=n*v
        if ratio>best+1e-8:
            best=ratio
            record=dict(n=n,k=k,name=name,iteration=iteration,ratio=ratio,weights=w.tolist(),p=p.tolist(),on_path=actual,actions={','.join(map(str,h)):int(a) for h,a in cert.actions.items()},rows=len(G),backgrounds=bgs,status='numerical_only')
            (OUT/'leaf_support_best.json').write_text(json.dumps(record,indent=2)+'\n')
            print(json.dumps({x:record[x] for x in ['n','k','name','iteration','ratio','rows']}),flush=True)
        if ratio>1+1e-6:
            pfull,vfull=security(w,member,R)
            print('CANDIDATE',ratio,'true_ratio',n*vfull,flush=True)
            return best,True
    return best,False

def main():
    best=0.
    for name in ['aggregate_theta_failure','individual_security_failure','local_security_increment','dynamic_iid_local','root_tax_failure','worst_pne_welfare_failure']:
        path=Path('examples/customer_attraction')/(name+'.json')
        if path.exists():
            best,done=run(Instance.from_dict(json.loads(path.read_text())),name,best)
            if done:return
    for n,k,runs in [(3,5,50),(4,6,50),(5,7,30)]:
        for trial in range(runs):
            cs=[CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randrange(1,15)) for mask in range(1,1<<k) if rng.random()<rng.choice([.1,.3,.5,1.])]
            ins=Instance(tuple(map(str,range(k))),tuple(cs),n)
            best,done=run(ins,f'{n}_{k}_{trial}',best)
            if done:return
    print('FINISHED',best,flush=True)
if __name__=='__main__':main()
