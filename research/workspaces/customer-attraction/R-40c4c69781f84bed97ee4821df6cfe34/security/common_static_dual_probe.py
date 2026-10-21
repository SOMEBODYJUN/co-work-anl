"""Numerical diagnostic: one static Q for a whole fixed complete-strategy cone.

This is stronger than the desired instance-dependent security bound. A failed LP
is not a CAG counterexample. Retains every ordered history and individual action.
"""
from itertools import product, combinations_with_replacement
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import bmat, csr_matrix, eye, hstack, vstack


def matrices(n, k, policy):
    masks=np.arange(1,1<<k)
    member=((masks[None,:]>>np.arange(k)[:,None])&1).astype(float)
    histories=[h for d in range(n) for h in product(range(k),repeat=d)]
    terminal={h:h for h in product(range(k),repeat=n)}
    for h in reversed(histories): terminal[h]=terminal[h+(policy[h],)]
    def utility(a,z):
        loads=member[list(z)].sum(axis=0)
        return np.divide(member[a],loads,out=np.zeros(len(masks)),where=loads>0)
    gamma=np.array([utility(policy[h],terminal[h])-utility(a,terminal[h+(a,)])
                    for h in histories for a in range(k) if a!=policy[h]])
    backgrounds=list(combinations_with_replacement(range(k),n-1))
    static=np.array([[member[a]/(1+member[list(b)].sum(axis=0))
                      for b in backgrounds] for a in range(k)])
    coverage=(member[list(terminal[()])].sum(axis=0)>0).astype(float)
    return gamma,static,coverage,backgrounds,terminal[()]


def run(n,k,policy,out):
    gamma,static,c,backgrounds,root=matrices(n,k,policy)
    nr,nt=gamma.shape;nb=len(backgrounds)
    # For each query a: c/n-static_a^T Q = gamma^T lambda_a + slack_a.
    blocks=[]
    for a in range(k):
        blocks.append([csr_matrix(static[a].T)]+[
            csr_matrix(gamma.T) if a==b else csr_matrix((nt,nr))
            for b in range(k)]+[
            eye(nt,format='csr') if a==b else csr_matrix((nt,nt))
            for b in range(k)])
    aeq=bmat(blocks,format='csr')
    aeq=vstack([aeq,csr_matrix(([1.]*nb,(np.zeros(nb,dtype=int),np.arange(nb))),shape=(1,nb+k*nr+k*nt))])
    beq=np.r_[np.tile(c/n,k),1.]
    res=linprog(np.zeros(nb+k*nr+k*nt),A_eq=aeq,b_eq=beq,bounds=(0,None),method='highs')
    report={'scope':'floating diagnostic only; fixed full-history strategy cone; common Q is stronger than security bridge',
            'n':n,'k':k,'root':root,'histories':sum(k**d for d in range(n)),
            'gamma_rows':nr,'types':nt,'status':res.message,'success':res.success}
    if res.success:
        q=res.x[:nb]; report['Q']=[{'background':b,'probability':float(v)} for b,v in zip(backgrounds,q) if v>1e-8]
        report['max_equation_residual']=float(np.max(np.abs(aeq@res.x-beq)))
    Path(out).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    n,k=3,6
    policy={():0}
    for a in range(k):
        policy[(a,)]=3 if a<3 else 0
        for b in range(k): policy[(a,b)]=next(c for c in (range(3) if b<3 else range(3,6)) if c not in (a,b))
    run(n,k,policy,Path(__file__).with_name('common_static_dual_groups.json'))
