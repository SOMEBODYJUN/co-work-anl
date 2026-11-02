"""Counterexample-only LP attack on independently reconstructed H4.
LP answers are proposals only. A positive proposal must be rationalized and all
ordered histories checked exactly. No negative run proves a universal claim.
"""
from fractions import Fraction as F
from itertools import product, combinations, permutations
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]

def attack(certfile):
    obj=json.loads((ROOT/certfile).read_text()); st=obj.get('strategy',obj)
    actions={tuple(a['history']):a['action'] for a in st['actions']}
    m=max(map(len,actions))+1; K=max(max(h,default=0) for h in actions)+1
    K=max(K,max(actions.values())+1)
    masks=range(1,1<<K); B=np.array([[(b>>a)&1 for a in range(K)] for b in masks],dtype=int)
    D=len(B)
    def leaf(h):
        while len(h)<m: h=h+(actions[h],)
        return h
    def payoff(h,a):
        c=B[:,h].sum(axis=1)
        return np.divide(B[:,a],c,out=np.zeros(D),where=c>0)
    q=leaf(()); load=B[:,q].sum(axis=1)
    cov=(load>0).astype(float); G=np.divide(cov,load+1)
    e=B/(load[:,None]+1)
    ds=np.column_stack([payoff(leaf(q[:i]+(a,)),a) for i in range(m) for a in range(K)]).reshape(D,m,K)
    rows=[]
    for h,a in actions.items():
        chosen=payoff(leaf(h),a)
        for b in range(K):
            if a!=b: rows.append(payoff(leaf(h+(b,)),b)-chosen)
    subsets=list(combinations(range(K),m))
    print(certfile,'K,m,vars,IC=',K,m,D,len(rows),flush=True)
    results=[]
    for T in subsets:
        o=(B[:,T].sum(axis=1)>0).astype(float)
        Aub=[np.r_[r,0.] for r in rows]; bub=[0.]*len(rows)
        # Unique optimum: every distinct m-support loses by at least t.
        for U in subsets:
            if U==T: continue
            oc=(B[:,U].sum(axis=1)>0).astype(float)
            Aub.append(np.r_[oc-o,1.]);bub.append(0.)
        for p in permutations(T):
            debt=sum(e[:,a]-ds[:,i,a] for i,a in enumerate(p))-G
            Aub.append(np.r_[-debt,1.]);bub.append(0.)
        res=linprog(np.r_[np.zeros(D),-1.],A_ub=Aub,b_ub=bub,A_eq=[np.r_[cov,0.]],b_eq=[1.],bounds=[(0,None)]*(D+1),method='highs')
        if res.success and res.x[-1]>1e-8:
            print('POSITIVE',T,res.x[-1],flush=True)
            results.append({'topics':K,'players':m,'target':T,'margin':float(res.x[-1]),'weights':{str(b):float(w) for b,w in zip(masks,res.x[:-1]) if w>1e-9},'actions':st['actions'],'terminal':q})
    return results
if __name__=='__main__':
    certs=['evidence/certificates/customer_attraction/aggregate_theta_failure.json','evidence/certificates/customer_attraction/individual_security_failure.json','evidence/certificates/customer_attraction/root_tax_failure.json']
    results=[]
    for c in certs:results+=attack(c)
    print(json.dumps(results,indent=2))
