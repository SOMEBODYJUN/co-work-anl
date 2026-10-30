"""Discovery only: free fractional-opponent leader floor on a full SPE cone.

All policy inequalities use every ordered history. Continuous opponent
separation is convex; floating optimization is not a proof or a certificate.
"""
import json, sys, math, random
from pathlib import Path
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog, minimize
from customer_attraction import Instance, ExactSPESolver

ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/aggregate_security'))
from probe import policy_matrix, security, cone_step

def continuous_best(w,p,member,n,start=None):
    """Minimize the p-query value over every fractional (n-1)-topic load."""
    k=len(member); l=n-1; alpha=p@member
    def f(q):return np.dot(w*alpha,1/(1+l*(q@member)))
    def j(q):return -l*member@(w*alpha/(1+l*(q@member))**2)
    q0=np.ones(k)/k if start is None else start
    ans=minimize(f,q0,jac=j,bounds=[(0,1)]*k,
        constraints=[{'type':'eq','fun':lambda q:q.sum()-1,'jac':lambda q:np.ones(k)}],
        method='SLSQP',options={'ftol':1e-11,'maxiter':500})
    if not ans.success:raise RuntimeError(ans.message)
    return ans.x,ans.fun

def fractional_security(w,member,n):
    k=len(member);l=n-1
    def g(q):return member@(w/(1+l*(q@member)))
    def dg(q):return -l*(member*(w/(1+l*(q@member))**2))@member.T
    q0=np.ones(k)/k
    ans=minimize(lambda z:z[-1],np.r_[q0,max(g(q0))],jac=lambda z:np.r_[np.zeros(k),1],
        bounds=[(0,1)]*k+[(0,None)],constraints=[
            {'type':'eq','fun':lambda z:z[:-1].sum()-1,'jac':lambda z:np.r_[np.ones(k),0]},
            {'type':'ineq','fun':lambda z:z[-1]-g(z[:-1]),'jac':lambda z:np.c_[-dg(z[:-1]),np.ones(k)]}],
        method='SLSQP',options={'ftol':1e-11,'maxiter':1000})
    if not ans.success:raise RuntimeError(ans.message)
    p=np.maximum(ans.multipliers[1:],0);p/=p.sum()
    qq,lower=continuous_best(w,p,member,n,ans.x[:-1])
    if ans.x[-1]-lower>1e-6:raise RuntimeError(('fractional KKT gap',ans.x[-1]-lower))
    return p,lower,np.vstack([np.eye(k),q0,ans.x[:-1]])

def cone_fixed_p(G,c,member,n,p,qs):
    qs=list(qs)
    for it in range(250):
        R=1/(1+(n-1)*np.array(qs)@member)
        w,upper=cone_step(G,c,member,R,p)
        q,lower=continuous_best(w,p,member,n)
        if upper-lower<2e-6:return w,lower,np.array(qs)
        qs.append(q)
    raise RuntimeError('cone cut budget')

def load_named(name):
    ins=Instance.from_dict(json.loads((ROOT/'examples/customer_attraction'/f'{name}.json').read_text()))
    raw=json.loads((ROOT/'evidence/certificates/customer_attraction'/f'{name}.json').read_text())
    if 'strategy' in raw:raw=raw['strategy']
    acts={tuple(r['history']):r['action'] for r in raw['actions']}
    return ins,acts

def restricted_policy_matrix(actions,n,k,masks):
    member=np.array([[(mask>>a)&1 for mask in masks] for a in range(k)],dtype=float)
    scale=math.lcm(*range(1,n+1));rows=[]
    def util(a,q):return member[a]*(scale//np.maximum(np.array(q)@member,1))
    def walk(h):
        if len(h)==n:return tuple(h.count(a) for a in range(k))
        children=[walk(h+(a,)) for a in range(k)]
        a=actions[h];q=children[a]
        for b in range(k):
            if b!=a:rows.append(util(a,q)-util(b,children[b]))
        return q
    q=walk(())
    G=np.unique(np.array(rows),axis=0)/scale
    return G,None,member,None,q

def challenge(ins,actions,name):
    n=ins.players;k=ins.topic_count
    masks=sorted({sum(1<<a for a in c.topics) for c in ins.customers if c.topics})
    if k>7:G,W,member,R,counts=restricted_policy_matrix(actions,n,k,masks)
    else:
        G,W,member,R,counts=policy_matrix(actions,n,k)
        masks=list(range(1,1<<k))
    a=actions[()];c=member[a]/np.maximum(np.array(counts)@member,1)
    w0=np.zeros(len(masks));index={m:j for j,m in enumerate(masks)}
    for cc in ins.customers:
        mask=sum(1<<a for a in cc.topics)
        if mask:w0[index[mask]]+=cc.multiplicity
    p,v,qs=fractional_security(w0,member,n)
    original=v/(c@w0)
    print(json.dumps({'name':name,'original_t/root':original}),flush=True)
    best=0;record=None
    for it in range(10):
        w,v,qs=cone_fixed_p(G,c,member,n,p,qs)
        p,v,newqs=fractional_security(w,member,n)
        qs=np.vstack([qs,newqs]);ratio=v
        if ratio>best+1e-8:
            best=ratio;record={'status':'floating discovery only','name':name,'n':n,'k':k,'iteration':it,'ratio_t/root':ratio,'masks':masks,'weights':w.tolist(),'query':p.tolist(),'actions':[{'history':list(h),'action':int(a)} for h,a in actions.items()]}
            print(json.dumps({s:record[s] for s in ['name','n','k','iteration','ratio_t/root']}),flush=True)
        if ratio>1+1e-6:
            (OUT/'fractional_leader_candidate.json').write_text(json.dumps(record,indent=2)+'\n')
            return True
    return False

if __name__=='__main__':
    names=sys.argv[1:] or ['individual_security_failure','aggregate_theta_failure','local_security_increment']
    for name in names:
        ins,actions=load_named(name)
        if challenge(ins,actions,name):break
