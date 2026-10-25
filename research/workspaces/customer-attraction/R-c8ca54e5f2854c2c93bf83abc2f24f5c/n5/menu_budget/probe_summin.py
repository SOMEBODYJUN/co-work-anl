"""Targeted n=5 true CAG/full-history SPE attack on SUMmin-full.

Each fixed-policy LP retains every ordered-history IC, unit-client type
nonnegative representation, and the actual-prefix true continuation menus.
Float discovery only; any positive output needs a fresh Fraction audit.
"""
import argparse, itertools, json, math, time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix


class Experiment:
    def __init__(self, k, n=5, seed=0, roles=None):
        self.k, self.n = k, n
        self.roles = list(range(n)) if roles is None else roles
        self.rng = np.random.default_rng(seed)
        self.types = np.arange(1, 1 << k)
        self.inc = ((self.types[None, :] >> np.arange(k)[:, None]) & 1).astype(float)
        self.histories = [list(itertools.product(range(k), repeat=d)) for d in range(n+1)]
        self.leaves = self.histories[n]
        self.counts = list(itertools.combinations_with_replacement(range(k), n))
        self.term = {}
        self.ext = {}
        for q in self.counts:
            count = np.bincount(q, minlength=k)
            load = count @ self.inc
            self.term[q] = self.inc / np.maximum(load, 1)[None, :]
            self.ext[q] = self.inc / (1 + load)[None, :]

    def key(self, z):
        return tuple(sorted(z))

    def build(self, w):
        complete = {h:h for h in self.leaves}
        sigma = {}
        for d in range(self.n-1, -1, -1):
            for h in self.histories[d]:
                vals = np.array([self.term[self.key(complete[h+(a,)])][a] @ w for a in range(self.k)])
                best = np.flatnonzero(vals >= vals.max() - 1e-8)
                a = int(self.rng.choice(best))
                sigma[h] = a
                complete[h] = complete[h+(a,)]
        return sigma, complete

    def data(self, sigma, complete):
        z = complete[()]
        W = np.sum([self.term[self.key(z)][z[i]] for i in self.roles],axis=0)
        menus = [[self.ext[self.key(complete[z[:i]+(a,)])] for a in range(self.k)] for i in self.roles]
        rows = []
        for d in range(self.n):
            for h in self.histories[d]:
                chosen = self.term[self.key(complete[h])][sigma[h]]
                for a in range(self.k):
                    if a != sigma[h]:
                        rows.append(self.term[self.key(complete[h+(a,)])][a]-chosen)
        return z, W, np.array(menus), np.array(rows)

    def p_lp(self, w, menus, W):
        k,n=self.k,len(self.roles)
        mat=np.zeros((n*k,k+n))
        for i in range(n):
            for a in range(k):
                mat[i*k+a,:k]=-(menus[i,a] @ w)
                mat[i*k+a,k+i]=1
        res=linprog(np.r_[np.zeros(k),-np.ones(n)], A_ub=mat,b_ub=np.zeros(n*k),A_eq=[np.r_[np.ones(k),np.zeros(n)]],b_eq=[1],bounds=[(0,None)]*(k+n),method='highs')
        if not res.success: raise RuntimeError(res.message)
        return res.x[:k], float(-res.fun-W@w)

    def w_lp(self, p, menus, W, rows):
        d=len(self.types);k,n=self.k,len(self.roles)
        mat=np.zeros((len(rows)+n*k,d+n))
        mat[:len(rows),:d]=rows
        for i in range(n):
            for a in range(k):
                j=len(rows)+i*k+a
                mat[j,:d]=-(p @ menus[i,a])
                mat[j,d+i]=1
        res=linprog(np.r_[W,-np.ones(n)], A_ub=csr_matrix(mat),b_ub=np.zeros(len(mat)), A_eq=[np.r_[np.ones(d),np.zeros(n)]],b_eq=[1],bounds=[(0,None)]*(d+n),method='highs')
        if not res.success: raise RuntimeError(res.message)
        return res.x[:d],float(-res.fun)

    def average_w_lp(self, p, menus, W, rows):
        # Stronger same-p pushforward candidate; no free column minimum.
        Q=np.einsum('a,t,iatd->d',p,p,menus)
        res=linprog(W-Q,A_ub=csr_matrix(rows),b_ub=np.zeros(len(rows)),A_eq=[np.ones(len(W))],b_eq=[1],bounds=[(0,None)]*len(W),method='highs')
        if not res.success:raise RuntimeError(res.message)
        return res.x,float(-res.fun)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,default=5);ap.add_argument('--n',type=int,default=5);ap.add_argument('--roles',type=str);ap.add_argument('--average',action='store_true');ap.add_argument('--rounds',type=int,default=20);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    roles=None if args.roles is None else [int(a)-1 for a in args.roles.split(',')]
    e=Experiment(args.k,args.n,args.seed,roles);best=-1e99;record={};start=time.time();logs=[]
    w=np.ones(len(e.types))/len(e.types)
    for r in range(args.rounds):
        if r%5==0:
            w=e.rng.exponential(1,len(e.types));w*=e.rng.random(len(w))<.4;w/=w.sum()
        sig,comp=e.build(w);z,W,menus,rows=e.data(sig,comp)
        if args.average:
            p=e.rng.dirichlet(np.ones(e.k))
            w,gap=e.average_w_lp(p,menus,W,rows)
        else:
            p,gap=e.p_lp(w,menus,W)
            for j in range(3):
                w,gap=e.w_lp(p,menus,W,rows)
                p,gap=e.p_lp(w,menus,W)
        if gap>best+1e-10:
            best=gap
            record={'k':e.k,'n':e.n,'roles':e.roles,'seed':args.seed,'round':r,'gap':gap,'w':w.tolist(),'p':p.tolist(),'actual':z,'sigma':[[list(h),a] for h,a in sig.items()]}
            args.out.write_text(json.dumps(record,indent=2)+'\n')
            print(json.dumps({'round':r,'gap':gap,'best':best,'actual':z,'seconds':time.time()-start}),flush=True)
        logs.append({'round':r,'gap':gap,'best':best})
        if gap>1e-7:break
    args.out.with_suffix('.log.json').write_text(json.dumps(logs,indent=2)+'\n')
    print(json.dumps({'done':True,'rounds':len(logs),'best':best,'seconds':time.time()-start}),flush=True)

if __name__=='__main__':main()
