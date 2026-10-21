"""Complete 13-client CCE counterexample policy cone, fixed saddle separation."""
from pathlib import Path
from itertools import combinations_with_replacement
import json,random
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[6]
k=5;n=3;masks=np.arange(1,1<<k);inc=(masks[:,None]>>np.arange(k))&1
policy={tuple(z['history']):z['action'] for z in json.load(open(ROOT/'evidence/certificates/customer_attraction/worst_cce_welfare_failure.json'))['actions']}
def finish(h):
    while len(h)<n:h+=(policy[h],)
    return h
def row(a,z):
    den=inc[:,list(z)].sum(axis=1)
    return np.divide(inc[:,a],den,out=np.zeros(len(masks)),where=den!=0)
G=[]
for h,a in policy.items():
    u=row(a,finish(h));G.extend(u-row(t,finish(h+(t,))) for t in range(k) if t!=a)
G=np.array(G);term=finish(());load=inc[:,list(term)].sum(axis=1);W=(load>0).astype(float)
D=np.where(load>0,(n+1)/(load+1),n)[:,None]*inc
backgrounds=list(combinations_with_replacement(range(k),n-1))
static=np.array([inc/(1+inc[:,list(B)].sum(axis=1))[:,None] for B in backgrounds])

def saddle(w):
    f=np.einsum('bta,t->ba',static,w)
    res=linprog(np.r_[np.zeros(k),-1],A_ub=np.c_[-f,np.ones(len(f))],b_ub=np.zeros(len(f)),A_eq=[np.r_[np.ones(k),0]],b_eq=[1],bounds=[(0,None)]*k+[(None,None)],method='highs')
    return res.x[:-1],-res.ineqlin.marginals

if __name__=='__main__':
    rng=np.random.default_rng(762917);best=None
    inp=json.load(open(ROOT/'examples/customer_attraction/worst_cce_welfare_failure.json'))
    w=np.zeros(len(masks))
    for t in inp['customers']:w[sum(1<<a for a in t['topics'])-1]=t['multiplicity']
    p=np.array([0,.2,.2,.2,.4]);Q=np.zeros(len(backgrounds));Q[backgrounds.index((0,4))]=1
    for i in range(10000):
        if i%4==0 and i:
            ext=linprog(rng.normal(size=len(masks)),A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[np.ones(len(masks))],b_eq=[1],bounds=(0,None),method='highs')
            if not ext.success:raise RuntimeError(ext.message)
            p,Q=saddle(ext.x)
        root=np.einsum('bta,a->bt',static,p)
        upper=np.einsum('bta,b->at',static,Q)
        A=np.r_[np.c_[-G,np.zeros(len(G))],np.c_[-root,np.ones(len(root))],np.c_[upper,-np.ones(k)]]
        lp=linprog(np.r_[W-D@p,0],A_ub=A,b_ub=np.zeros(len(A)),A_eq=[np.r_[np.ones(len(masks)),0]],b_eq=[1],bounds=[(0,None)]*len(masks)+[(None,None)],method='highs')
        if not lp.success:raise RuntimeError(lp.message)
        if best is None or lp.fun<best['gap']-1e-9:
            best=dict(status='floating complete SPE policy cone saddle screen',gap=lp.fun,weights=lp.x[:-1].tolist(),value=lp.x[-1],query=p.tolist(),opponent=Q.tolist(),backgrounds=backgrounds,iteration=i);print(json.dumps(dict(gap=lp.fun,iteration=i)),flush=True)
        if lp.fun< -1e-8:break
        p,Q=saddle(lp.x[:-1])
    Path(__file__).with_name('cce_policy_deletion_results.json').write_text(json.dumps(best,indent=2))
