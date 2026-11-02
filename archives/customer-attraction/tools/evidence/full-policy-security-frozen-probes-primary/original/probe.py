"""Aggregate static security: exact SPE-policy cones, numerical search only."""
import json, math, random, sys, time
from itertools import combinations_with_replacement
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance, CustomerType, ExactSPESolver

OUT=Path(__file__).resolve().parent
rng=random.Random(2070121887)

def policy_matrix(actions,n,k):
    member=np.array([[(mask>>a)&1 for mask in range(1,1<<k)] for a in range(k)], dtype=np.int16)
    scale=math.lcm(*range(1,n+1)); rows=[]
    def util(a,q):
        return member[a]*(scale//np.maximum(np.array(q)@member,1))
    def walk(h):
        if len(h)==n:return tuple(h.count(a) for a in range(k))
        children=[walk(h+(a,)) for a in range(k)]
        a=actions[h];q=children[a]
        for b in range(k):
            if b!=a:rows.append(util(a,q)-util(b,children[b]))
        return q
    q=walk(())
    G=np.unique(np.array(rows),axis=0).astype(float)/scale
    c=(np.array(q)@member>0).astype(float)
    bg=np.array([tuple(b.count(a) for a in range(k)) for b in combinations_with_replacement(range(k),n-1)])
    reciprocal=1/(1+bg@member)
    return G,c,member,reciprocal,q

def security(w,member,R):
    pay=(R*w)@member.T
    # maximize z under z <= payoff(row,p)
    res=linprog(np.r_[np.zeros(len(member)),-1.],A_ub=np.column_stack([-pay,np.ones(len(pay))]),b_ub=np.zeros(len(pay)),A_eq=np.array([np.r_[np.ones(len(member)),0.]]),b_eq=[1.],bounds=[(0,None)]*len(member)+[(None,None)],method='highs')
    if not res.success:raise ValueError(res.message)
    return res.x[:-1],res.x[-1]

def cone_step(G,c,member,R,p):
    beta=R*(p@member)
    A=np.vstack([np.column_stack([-G,np.zeros(len(G))]),np.column_stack([-beta,np.ones(len(beta))])])
    res=linprog(np.r_[np.zeros(len(c)),-1.],A_ub=A,b_ub=np.zeros(len(A)),A_eq=np.array([np.r_[c,0.]]),b_eq=[1.],bounds=[(0,None)]*len(c)+[(None,None)],method='highs')
    if not res.success:raise ValueError(res.message)
    return res.x[:-1],res.x[-1]

def explore(ins,trial,best):
    n=ins.players;k=ins.topic_count
    solver=ExactSPESolver(ins)
    z=min(solver.outcomes(),key=ins.welfare)
    cert=solver.certificate(z,action_selector=lambda h,c:rng.choice(c),continuation_selector=lambda h,c:rng.choice(c))
    G,c,member,R,q=policy_matrix(cert.actions,n,k)
    ws=np.zeros((1<<k)-1)
    for x in ins.customers:
        mask=sum(1<<a for a in x.topics)
        if mask:ws[mask-1]+=x.multiplicity
    starts=[security(ws,member,R)[0],np.ones(k)/k]
    starts.extend(rng.dirichlet(np.ones(k)) if False else np.random.default_rng(sum(map(ord,str(trial)))+991).dirichlet(np.ones(k)) for j in range(1))
    for si,p in enumerate(starts):
        old=-1
        for iteration in range(8):
            w,v=cone_step(G,c,member,R,p)
            p,v=security(w,member,R)
            ratio=n*v
            if ratio>best+1e-8:
                best=ratio
                record=dict(n=n,k=k,trial=trial,start=si,iteration=iteration,ratio=ratio,weights=w.tolist(),p=p.tolist(),on_path=q,actions={','.join(map(str,h)):int(a) for h,a in cert.actions.items()},rows=len(G),status='numerical_only')
                (OUT/'best.json').write_text(json.dumps(record,indent=2)+'\n')
                print(json.dumps({x:record[x] for x in ['n','k','trial','start','iteration','ratio','rows']}),flush=True)
            if ratio>1+1e-6:
                print('POSITIVE_CANDIDATE',flush=True)
                return best,True
            if ratio<old+1e-9:break
            old=ratio
    return best,False

def main():
    best=0.
    named=['aggregate_theta_failure','individual_security_failure','local_security_increment','dynamic_iid_local','root_tax_failure','worst_pne_welfare_failure']
    for name in named:
        p=Path('examples/customer_attraction')/(name+'.json')
        if not p.exists():continue
        try:
            ins=Instance.from_dict(json.loads(p.read_text()))
            best,found=explore(ins,name,best)
            if found:return
        except Exception as e:print('SKIP',name,str(e),flush=True)
    for n,k,runs in [(3,6,40),(4,6,50),(5,7,30),(6,7,15)]:
        for trial in range(runs):
            density=rng.choice([.1,.3,.5,1.])
            customers=[CustomerType(frozenset(a for a in range(k) if mask>>a&1),rng.randrange(1,15)) for mask in range(1,1<<k) if rng.random()<density]
            ins=Instance(tuple(map(str,range(k))),tuple(customers),n)
            best,found=explore(ins,1000*n+trial,best)
            if found:return
    print('FINISHED',best,flush=True)

if __name__=='__main__':main()
