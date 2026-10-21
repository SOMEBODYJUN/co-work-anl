"""Exploratory full-strategy cone attacks on aggregate static security.

Numerical discovery only. Each candidate policy is complete and its full
one-deviation matrix is retained, including ordered histories independently.
"""
import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, minimize


class Model:
    def __init__(self, m, n):
        self.m, self.n = m, n
        self.masks = np.arange(1, 2**m)
        self.member = ((self.masks[:, None] >> np.arange(m)) & 1).astype(float)
        self.cache = {}
        self.backgrounds = list(itertools.combinations_with_replacement(range(m), n-1))
        self.static = np.array([self.member.T / (1+self.member[:, b].sum(axis=1))
                                for b in self.backgrounds])

    def utility(self, z):
        k = tuple(sorted(z))
        if k not in self.cache:
            loads = self.member[:, k].sum(axis=1)
            inv = np.divide(1., loads, out=np.zeros_like(loads), where=loads > 0)
            self.cache[k] = self.member.T * inv
        return self.cache[k]

    def policy(self, w, rng):
        actions, leaves = {}, {}
        def rec(h):
            if len(h) == self.n:
                return h
            branches = [rec(h+(a,)) for a in range(self.m)]
            vals = np.array([self.utility(branches[a])[a] @ w for a in range(self.m)])
            good = np.flatnonzero(vals >= max(vals)-1e-8)
            a = int(rng.choice(good))
            actions[h] = a
            leaves[h] = branches[a]
            return branches[a]
        rec(())
        return actions, leaves

    def matrix(self, actions, leaves):
        rows = []
        for h, a0 in actions.items():
            z = leaves[h]
            for a in range(self.m):
                child = h+(a,)
                za = child if len(child) == self.n else leaves[child]
                row = self.utility(z)[a0] - self.utility(za)[a]
                if np.any(row):
                    rows.append(row)
        c = (self.member[:, leaves[()]].sum(axis=1) > 0).astype(float)
        return np.array(rows), c

    def security(self, w):
        mat = np.einsum('bad,d->ba', self.static, w)
        # p variables followed by value t.
        ans = linprog(np.r_[np.zeros(self.m), -1.],
                      A_ub=np.c_[-mat, np.ones(len(mat))], b_ub=np.zeros(len(mat)),
                      A_eq=[np.r_[np.ones(self.m), 0]], b_eq=[1],
                      bounds=[(0, None)]*self.m+[(None, None)], method='highs')
        return ans.x[:self.m], ans.x[-1]

    def iid(self, w):
        n = self.n
        def value(q):
            t = self.member @ q
            # f_n derivative n*g_n, integrate explicitly by binomial expectation.
            f = np.zeros_like(t)
            H = 0.
            for j in range(1, n+1):
                H += 1/j
                f += H*math.comb(n,j)*t**j*(1-t)**(n-j)
            return -(w@f)
        def jac(q):
            t = self.member @ q
            g = sum((1-t)**j for j in range(n))/n
            return -n * self.member.T @ (w*g)
        ans = minimize(value,np.ones(self.m)/self.m,jac=jac,method='SLSQP',
                       bounds=[(0,1)]*self.m,
                       constraints=[{'type':'eq','fun':lambda q:q.sum()-1,
                                     'jac':lambda q:np.ones(self.m)}],
                       options={'ftol':1e-12,'maxiter':300})
        q=np.maximum(ans.x,0);q/=q.sum()
        t=self.member@q
        return q,w@(1-(1-t)**n)

    def attack_security(self, gamma, c, p):
        beta=np.einsum('bad,a->bd', self.static,p)
        ans=linprog(np.r_[c,-self.n],
                    A_ub=np.vstack([np.c_[-gamma,np.zeros(len(gamma))],
                                    np.c_[-beta,np.ones(len(beta))]]),
                    b_ub=np.zeros(len(gamma)+len(beta)),
                    A_eq=[np.r_[np.ones(len(c)),0]],b_eq=[1],
                    bounds=[(0,None)]*len(c)+[(None,None)],method='highs')
        return ans

    def attack_iid(self, gamma, c, q):
        t=self.member@q
        psi=1-(1-t)**self.n
        g=sum((1-t)**j for j in range(self.n))/self.n
        E=psi[None,:]-self.n*self.member.T*g
        ans=linprog(c-psi,A_ub=-np.vstack([gamma,E]),
                    b_ub=np.zeros(len(gamma)+self.m),
                    A_eq=[np.ones(len(c))],b_eq=[1],
                    bounds=[(0,None)]*len(c),method='highs')
        return ans

    def ratio_iid(self, gamma, c, q):
        t=self.member@q
        psi=1-(1-t)**self.n
        g=sum((1-t)**j for j in range(self.n))/self.n
        E=psi[None,:]-self.n*self.member.T*g
        return linprog(c,A_ub=-np.vstack([gamma,E]),
                       b_ub=np.zeros(len(gamma)+self.m),
                       A_eq=[psi],b_eq=[1],bounds=[(0,None)]*len(c),method='highs')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--topics',type=int,default=6)
    parser.add_argument('--players',type=int,default=3)
    parser.add_argument('--trials',type=int,default=100)
    parser.add_argument('--seed',type=int,default=789)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    rng=np.random.default_rng(args.seed)
    model=Model(args.topics,args.players)
    best_s=0;best_i=0
    records=[]
    for trial in range(args.trials):
        w=rng.exponential(1,len(model.masks))
        w*=rng.random(len(w)) < .3
        if trial%3==0:
            # Equal weights across all cardinality classes give many exact ties.
            card=rng.integers(0,10,args.topics+1)
            w=np.array([card[int(t).bit_count()] for t in model.masks],float)
        policy,leaves=model.policy(w,rng)
        gamma,c=model.matrix(policy,leaves)
        p,v=model.security(w)
        security=model.attack_security(gamma,c,p)
        q,z=model.iid(w)
        iid=model.ratio_iid(gamma,c,q)
        sv=security.fun if security.success else None
        iv=iid.fun-1 if iid.success else None
        records.append({'trial':trial,'security_gap':sv,'iid_gap':iv})
        if (sv is not None and sv < best_s-1e-9) or (iv is not None and iv < best_i-1e-9):
            best_s=min(best_s,sv or 0);best_i=min(best_i,iv or 0)
            print(json.dumps({'trial':trial,'security_gap':sv,'iid_gap':iv}),flush=True)
            payload={'args':vars(args)|{'output':str(args.output)},'records':records,
                     'actions':[[list(h),a] for h,a in policy.items()],
                     'p':p.tolist(),'q':q.tolist(),
                     'security_w':security.x.tolist() if security.success else None,
                     'iid_w':iid.x.tolist() if iid.success else None}
            if args.output:
                args.output.write_text(json.dumps(payload,indent=2))
        if trial%10==0:
            print(json.dumps({'progress':trial,'best_security_gap':best_s,'best_iid_gap':best_i}),flush=True)
    if args.output and not args.output.exists():
        args.output.write_text(json.dumps({'args':vars(args)|{'output':str(args.output)},'records':records},indent=2))

if __name__=='__main__':
    main()
