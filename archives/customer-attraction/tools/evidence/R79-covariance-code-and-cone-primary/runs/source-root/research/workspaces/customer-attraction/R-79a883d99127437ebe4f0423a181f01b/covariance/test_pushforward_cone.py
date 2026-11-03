"""Targeted test of the all-p full-query pushforward inequality.

This is an auxiliary candidate test, not an algorithm for Q-CAG-HALF.
The fixed full ordered-history policies are existing certified SPE policies;
LP changes customer type multiplicities while preserving every policy IC.
Only a positive exactly certified witness would refute the candidate.
"""
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, minimize

ROOT = Path(__file__).resolve().parents[5]


def run(name, players, topics, p0):
    obj = json.loads((ROOT / 'evidence/certificates/customer_attraction' / (name+'.json')).read_text())
    policy = {tuple(r['history']):r['action'] for r in obj['strategy']['actions']}
    masks = np.arange(1, 1 << topics)
    incidence = ((masks[:,None] >> np.arange(topics)) & 1).astype(float)

    def terminal(h):
        while len(h) < players:
            h = h+(policy[h],)
        return h

    def payoff(h, a, pos):
        z = terminal(h+(a,))
        loads = incidence[:,z].sum(axis=1)
        return np.divide(incidence[:,z[pos]], loads, out=np.zeros(len(masks)), where=loads>0)

    rows=[]
    for h, a in policy.items():
        own=payoff(h,a,len(h))
        for b in range(topics):
            if b != a:
                rows.append(own-payoff(h,b,len(h)))
    actual=terminal(())
    covered=(incidence[:,actual].sum(axis=1)>0).astype(float)
    tensor=np.zeros((len(masks),topics,topics))
    for pos in range(players):
        h=actual[:pos]
        for a in range(topics):
            loads=incidence[:,terminal(h+(a,))].sum(axis=1)
            tensor[:,a,:]+=incidence/(1+loads[:,None])

    def solve(p):
        gain=np.einsum('a,xab,b->x',p,tensor,p)-covered
        result=linprog(-gain,A_ub=-np.array(rows),b_ub=np.zeros(len(rows)),A_eq=covered[None,:],b_eq=[1.],bounds=(0,None),method='highs')
        if not result.success:
            raise RuntimeError(result.message)
        return -result.fun,result.x

    p=np.array(p0,dtype=float)
    records=[]
    for iteration in range(8):
        value,w=solve(p)
        records.append({'iteration':iteration,'gain':value,'p':p.tolist()})
        mat=np.einsum('x,xab->ab',w,tensor)
        fit=minimize(lambda q: -q@mat@q,p,jac=lambda q:-(mat+mat.T)@q,bounds=[(0,1)]*topics,constraints={'type':'eq','fun':lambda q:q.sum()-1,'jac':lambda q:np.ones(topics)},method='SLSQP',options={'ftol':1e-12,'maxiter':300})
        if np.linalg.norm(fit.x-p)<1e-9:
            break
        p=fit.x
    print(json.dumps({'policy':name,'candidate':'sum_i C_i(p)<=W','records':records},indent=2))


if __name__ == '__main__':
    run('aggregate_theta_failure',3,6,[0,0,.5,0,0,.5])
    run('global_decorrelation_failure',4,6,[0,.5,.5,0,0,0])
