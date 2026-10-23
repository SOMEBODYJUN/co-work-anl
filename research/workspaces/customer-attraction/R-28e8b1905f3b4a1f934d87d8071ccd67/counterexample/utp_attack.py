"""Directed finite separation oracle for the explicit forest UTP candidate.

Positive discovery is independently reconstructed with Fractions.  A negative
run is only a diagnostic of UTP, not evidence for the main half conjecture.
"""
import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import random
import numpy as np


def compositions(n, p):
    if p == 1:
        yield (n,)
    else:
        for v in range(n + 1):
            for rest in compositions(n-v, p-1):
                yield (v,) + rest


class UTP:
    def __init__(self, p, m, support):
        self.p, self.m, self.support = p, m, support
        self.terminal = np.array(list(compositions(m, p)), dtype=int)
        self.bg = np.array(list(compositions(m-1, p)), dtype=int)
        self.prefix = np.array([b for t in range(m-1) for b in compositions(t,p)], dtype=int)
        member = np.zeros((len(support), p), dtype=int)
        for i, s in enumerate(support):
            member[i,list(s)] = 1
        den = self.terminal @ member.T
        self.coef = np.array([member.T / np.maximum(d,1) for d in den])
        self.menus = np.array([member.T / (1 + b @ member.T) for b in self.bg])
        self.children = [[np.flatnonzero(np.all(self.terminal >= b + np.eye(p,dtype=int)[a],axis=1)) for a in range(p)] for b in self.prefix]

    def test(self, w):
        u = self.coef @ w
        menu = self.menus @ w
        theta = menu.max(axis=1).min()
        high = u >= theta - 1e-9
        low = u < theta - 1e-9
        for b, ca in zip(self.prefix,self.children):
            witnesses=[]
            for a, choices in enumerate(ca):
                q=self.terminal[choices]
                valid = low[choices,a] & np.all((q <= b) | high[choices] | (np.arange(self.p)==a),axis=1) & (q[:,a] == b[a]+1)
                good=np.flatnonzero(valid)
                if not len(good):
                    break
                witnesses.append(tuple(map(int,q[good[0]])))
            if len(witnesses)==self.p:
                return self.exact(w, b, witnesses)
        return None

    def exact(self,w,b,qs):
        def payoff(q,a):
            return sum((Fraction(int(wi),sum(q[j] for j in s)) for s,wi in zip(self.support,w) if a in s),Fraction(0))
        def menu(k,a):
            return sum((Fraction(int(wi),1+sum(k[j] for j in s)) for s,wi in zip(self.support,w) if a in s),Fraction(0))
        theta=min(max(menu(k,a) for a in range(self.p)) for k in self.bg)
        detail=[]
        for a,q in enumerate(qs):
            ua=payoff(q,a)
            others={j:payoff(q,j) for j in range(self.p) if q[j]>b[j]+int(a==j)}
            assert ua<theta and all(v>=theta for v in others.values())
            detail.append({'action':a,'q':q,'u_action':str(ua),'followers':{j:str(v) for j,v in others.items()}})
        return {'p':self.p,'m':self.m,'support':self.support,'weights':list(map(int,w)),'prefix':list(map(int,b)),'theta':str(theta),'witnesses':detail}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--seed',type=int,default=2026102321)
    ap.add_argument('--trials',type=int,default=500)
    ap.add_argument('--p',type=int,default=5)
    ap.add_argument('--m',type=int,default=5)
    ap.add_argument('--out',default='utp_diagnostic.json')
    args=ap.parse_args(); rng=random.Random(args.seed)
    seen=0
    # Two topology families: action trees, and hyperedge trees made by attaching
    # a fresh action to an existing resource. Every generated incidence is forest.
    for topology in range(20):
        support=[(a,) for a in range(args.p)]
        for a in range(1,args.p):
            if topology%2 or a==1 or rng.random()<.6:
                support.append(tuple(sorted((a,rng.randrange(a)))))
            else:
                at=rng.randrange(args.p,len(support))
                support[at]=tuple(sorted(support[at]+(a,)))
        oracle=UTP(args.p,args.m,support)
        for _ in range(max(1,args.trials//20)):
            w=np.array([rng.randrange(0,21) for s in support])
            seen+=1
            res=oracle.test(w)
            if res:
                Path(args.out).write_text(json.dumps({'scope':'exact counterexample to forest UTP only','seed':args.seed,'checked':seen,'witness':res},indent=2))
                print(json.dumps(res)); return
    Path(args.out).write_text(json.dumps({'scope':'finite directed UTP diagnostic only','seed':args.seed,'checked':seen,'positive':False,'p':args.p,'m':args.m},indent=2))
    print(json.dumps({'checked':seen,'positive':False}))

if __name__=='__main__': main()
