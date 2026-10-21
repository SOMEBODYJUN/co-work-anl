"""Exploratory integer DP and LP search, not a general proof.

Terminal sets preserve arbitrary history-dependent tie selections, using the
same set-valued recurrence as the normative solver; integer common-denominator
payoffs make all DP decisions exact.  SciPy LP numbers are only search scores.
"""
from itertools import combinations_with_replacement
from math import lcm
import argparse, json, random, time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def count_vectors(length, topics):
    for labels in combinations_with_replacement(range(topics), length):
        yield tuple(labels.count(a) for a in range(topics))


class Search:
    def __init__(self, n, k):
        self.n, self.k = n, k
        self.scale = lcm(*range(1, n+1))
        self.masks = np.array([[bool(mask & (1 << a)) for a in range(k)]
                               for mask in range(1, 1 << k)], dtype=np.int64)
        self.cts = [list(count_vectors(d, k)) for d in range(n+1)]
        self.final = self.cts[-1]
        self.fi = {q:j for j,q in enumerate(self.final)}
        coeff = []
        for q in self.final:
            loads = self.masks @ np.array(q)
            denom = np.maximum(1, loads)
            coeff.append(self.masks.T * (self.scale // denom))
        self.utility_coeff = np.array(coeff)
        self.coverage_coeff = np.array([(self.masks @ np.array(q)) > 0
                                       for q in self.final], dtype=np.int64)
        self.security_coeff = np.array([
            self.masks.T * (self.scale // (1 + self.masks @ np.array(q)))
            for q in self.cts[n-1]])
        self.children = {}
        for d in range(n):
            for q in self.cts[d]:
                self.children[q] = [tuple(x + int(b == a) for b,x in enumerate(q))
                                    for a in range(k)]

    def evaluate(self, w, need_outcomes=False):
        utilities = self.utility_coeff @ w
        outcomes = {q:np.array([j], dtype=int) for q,j in self.fi.items()}
        for d in reversed(range(self.n)):
            for q in self.cts[d]:
                children = [outcomes[c] for c in self.children[q]]
                floor = max(np.min(utilities[child,a])
                            for a, child in enumerate(children))
                outcomes[q] = np.unique(np.concatenate([
                    child[utilities[child,a] >= floor]
                    for a,child in enumerate(children)]))
        roots = outcomes[(0,) * self.k]
        welfare = self.coverage_coeff @ w
        minw = np.min(welfare[roots])
        pay = (self.security_coeff @ w) / self.scale
        # query player maximizes v under every static rival multiset
        lp = linprog(np.r_[np.zeros(self.k),-1],
                     A_ub=np.c_[-pay,np.ones(len(pay))],
                     b_ub=np.zeros(len(pay)),
                     A_eq=[np.r_[np.ones(self.k),0]],b_eq=[1],
                     bounds=[(0,None)] * self.k + [(None,None)],
                     method='highs')
        if not lp.success: raise RuntimeError(lp.message)
        value = lp.x[-1]
        result = dict(n=self.n,k=self.k,weights=list(map(int,w)),
                      min_welfare=int(minw),value=float(value),
                      gap=float(minw-self.n*value),
                      relative_gap=float(minw/(self.n*value)-1) if value else 0.,
                      query=list(map(float,lp.x[:-1])),
                      rivals=[dict(counts=list(self.cts[self.n-1][j]),
                                   probability=float(-v))
                              for j,v in enumerate(lp.ineqlin.marginals) if v < -1e-9],
                      worst_counts=[list(self.final[j]) for j in roots if welfare[j]==minw],
                      max_welfare=int(np.max(welfare)))
        excess=0
        for j in roots:
            if welfare[j]!=minw:continue
            q=self.final[j]
            for a in range(self.k):
                if not q[a]:continue
                for b in range(self.k):
                    dev=tuple(q[c]-int(c==a)+int(c==b) for c in range(self.k))
                    excess=max(excess,int(utilities[self.fi[dev],b]-utilities[j,a]))
        result['static_deviation_excess']=excess/self.scale
        result['has_nonPNE_worst_outcome']=excess>0
        if need_outcomes: return result, outcomes, utilities
        return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,default=4)
    ap.add_argument('--k',type=int,default=5);ap.add_argument('--trials',type=int,default=3000)
    ap.add_argument('--seed',type=int,default=763031);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--seconds',type=int,default=120)
    a=ap.parse_args();rng=random.Random(a.seed);s=Search(a.n,a.k)
    best=None;start=time.monotonic();bank=[];i=0
    while i<a.trials and time.monotonic()-start<a.seconds:
        if bank and rng.random()<0.8:
            w=list(rng.choice(bank)['weights'])
            for _ in range(rng.randrange(1,5)):
                j=rng.randrange(len(w));w[j]=max(0,w[j]+rng.randint(-10,10))
        else:
            w=[rng.randrange(20) if rng.random()<rng.uniform(0.1,0.7) else 0
               for _ in range((1<<a.k)-1)]
        # Universal customers add exactly the same constant to every payoff
        # and can make a relative score look arbitrarily good without closing
        # the absolute aggregate deficit.  Remove this search-only nuisance.
        w[-1]=0
        if not any(w):continue
        z=s.evaluate(np.array(w,dtype=np.int64));i+=1
        if z['has_nonPNE_worst_outcome']:
            bank.append(z);bank.sort(key=lambda q:q['relative_gap']);bank=bank[:30]
        if z['has_nonPNE_worst_outcome'] and (best is None or z['relative_gap']<best['relative_gap']-1e-10):
            best=z
            a.output.write_text(json.dumps(dict(status='EXPLORATORY',seed=a.seed,
                 trials=i,elapsed=time.monotonic()-start,best=best),indent=2)+'\n')
            print(json.dumps(dict(trial=i,gap=z['gap'],rel=z['relative_gap'],W=z['min_welfare'],v=z['value'])),flush=True)
        if z['gap'] < -1e-7:
            print('CANDIDATE FOUND',flush=True);break
    a.output.write_text(json.dumps(dict(status='EXPLORATORY',seed=a.seed,
        trials=i,elapsed=time.monotonic()-start,best=best,bank=bank),indent=2)+'\n')

if __name__=='__main__':main()
