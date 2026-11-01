"""Exploration only: local truncated cylinders, full history SPE, moment LP.

No generated pseudo-moment is asserted to be a customer instance.
"""
from __future__ import annotations
import argparse, itertools, json, math, random, time
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def masks(p, max_size):
    return [s for s in range(1, 1 << p) if s.bit_count() <= max_size]


class Problem:
    def __init__(self, m, p):
        self.m, self.p = m, p
        self.ms = masks(p, m)
        self.ix = {s:i for i,s in enumerate(self.ms)}
        self.d = len(self.ms)
        self.local = []
        self.local_ids = []
        for a in self.ms:
            for c in range(1 << p):
                if a & c or (a | c).bit_count() > m:
                    continue
                row = [F(0)] * self.d
                e = c
                while True:
                    row[self.ix[a|e]] = F((-1) ** e.bit_count())
                    if not e: break
                    e = (e - 1) & c
                self.local.append(row)
                self.local_ids.append((a,c))
        self.local_np = np.array(self.local, dtype=float)
        self.single = np.array([int(s.bit_count()==1) for s in self.ms])

    @lru_cache(None)
    def payoff(self, q, a):
        row = [F(0)] * self.d
        support = [b for b,x in enumerate(q) if x and b != a]
        for bits in range(1 << len(support)):
            subset = [support[j] for j in range(len(support)) if bits >> j & 1]
            gamma = F(0)
            for eb in range(1 << len(subset)):
                den = q[a] + sum(q[b] for j,b in enumerate(subset) if eb >> j & 1)
                gamma += F((-1) ** (len(subset) - eb.bit_count()), den)
            mask = (1 << a) | sum(1 << b for b in subset)
            row[self.ix[mask]] += gamma
        return tuple(row)

    @lru_cache(None)
    def cover(self, mask):
        return tuple(F((-1)**(s.bit_count()+1)) if s & mask == s else F(0) for s in self.ms)

    def counts(self, h):
        return tuple(h.count(a) for a in range(self.p))

    def policy(self, t, seed):
        rng = random.Random(seed)
        sigma = {}
        def rec(h):
            if len(h) == self.m:
                return h
            outs = [rec(h+(a,)) for a in range(self.p)]
            vals = [float(np.dot(self.payoff(self.counts(s), a), t)) for a,s in enumerate(outs)]
            best = max(vals)
            a = rng.choice([a for a,x in enumerate(vals) if x >= best-1e-8])
            sigma[h] = a
            return outs[a]
        out = rec(())
        return sigma, out

    def rows(self, sigma):
        outcomes = {}
        def continuation(h):
            if h in outcomes: return outcomes[h]
            if len(h)==self.m: ans=h
            else: ans=continuation(h+(sigma[h],))
            outcomes[h]=ans
            return ans
        rows=[]; ids=[]
        for h,a in sigma.items():
            pos = self.payoff(self.counts(continuation(h)), a)
            for b in range(self.p):
                if b==a: continue
                neg=self.payoff(self.counts(continuation(h+(b,))), b)
                rows.append(tuple(x-y for x,y in zip(pos,neg)))
                ids.append((h,b))
        root=continuation(())
        return rows, ids, root

    def random_t(self, rng):
        obj=np.array([rng.uniform(-1,1) for _ in range(self.d)])
        lp=linprog(obj, A_ub=-self.local_np, b_ub=np.zeros(len(self.local)),
                   A_eq=[self.single], b_eq=[1], bounds=[(None,None)]*self.d,
                   method='highs')
        return lp.x

    def optimize(self, sigma):
        rows,ids,root=self.rows(sigma)
        c=np.array(self.cover(sum(1<<a for a in set(root))), dtype=float)
        A=np.vstack([-self.local_np, -np.array(rows, dtype=float)])
        best=None
        for J in itertools.combinations(range(self.p),min(self.m,self.p)):
            o=np.array(self.cover(sum(1<<a for a in J)),dtype=float)
            lp=linprog(-o,A_ub=A,b_ub=np.zeros(len(A)),A_eq=[c],b_eq=[1],
                       bounds=[(None,None)]*self.d,method='highs')
            if lp.status==3:
                return {'unbounded':True,'root':root,'J':J,'sigma':sigma}
            if lp.success and (best is None or -lp.fun>best['ratio']):
                best={'ratio':-lp.fun,'t':lp.x,'root':root,'J':J,'sigma':sigma}
        return best


def serial(problem, best):
    return {'m':problem.m,'p':problem.p,'ratio':best.get('ratio'),
            'unbounded':best.get('unbounded',False),'root':best['root'],'J':best['J'],
            'moments':{str(s):str(F(float(x)).limit_denominator(100000)) for s,x in zip(problem.ms,best.get('t',[]))},
            'policy':{','.join(map(str,h)):a for h,a in best['sigma'].items()}}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--m',type=int,default=3);ap.add_argument('--p',type=int,default=4)
    ap.add_argument('--trials',type=int,default=100);ap.add_argument('--seed',type=int,default=62421)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    pr=Problem(args.m,args.p);rng=random.Random(args.seed);best_ratio=0;best=None;seen=set()
    for k in range(args.trials):
        t=pr.random_t(rng)
        sigma,root=pr.policy(t,rng.randrange(2**32))
        sig=tuple(sorted(sigma.items()))
        if sig in seen:continue
        seen.add(sig);r=pr.optimize(sigma)
        if r and (r.get('unbounded') or r['ratio']>best_ratio+1e-9):
            best=r;best_ratio=r.get('ratio',float('inf'))
            args.output.write_text(json.dumps(serial(pr,r),indent=2)+'\n')
            print(json.dumps({'trial':k,'seen':len(seen),'ratio':best_ratio,'root':r['root']}),flush=True)
        if best_ratio>2.000001:break
    print(json.dumps({'finished':True,'trials':args.trials,'seen':len(seen),'best':best_ratio}),flush=True)


if __name__=='__main__': main()
