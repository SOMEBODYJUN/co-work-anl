"""Exploration, not a general theorem: exact full-history fresh quadratic games.

All-outcome BI is set-valued and cached by occupied-label set. Distinct ordered
histories remain independent when reconstructing a complete policy. The game
forces no repeated labels; it is auxiliary to, not identical with, CAG.
"""
from __future__ import annotations
import argparse
from functools import lru_cache
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import random
import time
import numpy as np
from scipy.optimize import linprog

class Fresh:
    def __init__(self,p,m,x):
        self.p,self.m,self.x=p,m,tuple(x)
        self.edges=list(combinations(range(p),2))
        self.edge_index={e:p+i for i,e in enumerate(self.edges)}
        self.full=(1<<p)-1
        self._pay={}
        self._out={}
        self._threshold={}
    def labels(self,H):
        return [a for a in range(self.p) if H>>a&1]
    def coeff(self,a,S):
        v=np.zeros(len(self.x));v[a]=1
        for b in self.labels(S^(1<<a)):
            v[self.edge_index[tuple(sorted((a,b)))]]=1
        return v
    def pay(self,a,S):
        key=(a,S)
        if key not in self._pay:
            self._pay[key]=self.x[a]+sum(self.x[self.edge_index[tuple(sorted((a,b)))]]
                                         for b in self.labels(S^(1<<a)))
        return self._pay[key]
    def outcomes(self,H=0):
        if H in self._out:return self._out[H]
        if H.bit_count()==self.m:
            ans=frozenset((H,));self._out[H]=ans;return ans
        menu={a:self.outcomes(H|1<<a) for a in self.labels(self.full^H)}
        threshold=max(min(self.pay(a,S) for S in ss) for a,ss in menu.items())
        self._threshold[H]=threshold
        ans=frozenset(S for a,ss in menu.items() for S in ss
                      if self.pay(a,S)>=threshold-1e-9)
        self._out[H]=ans
        return ans
    def theta(self):
        return min(max(self.pay(a,H|1<<a) for a in self.labels(self.full^H))
                   for ss in combinations(range(self.p),self.m-1)
                   for H in [sum(1<<a for a in ss)])
    def policy(self,target,root_action=None):
        """Reconstruct a full ordered-history policy witnessing target."""
        policy={}
        def fill(h,H,S,force=None):
            if len(h)==self.m:return
            threshold=self._threshold[H]
            choices=[a for a in self.labels(self.full^H)
                     if S in self.outcomes(H|1<<a) and self.pay(a,S)>=threshold-1e-9]
            a=force if force is not None else choices[0]
            assert a in choices
            policy[h]=a
            for b in self.labels(self.full^H):
                T=S if b==a else min(self.outcomes(H|1<<b),key=lambda R:self.pay(b,R))
                fill(h+(b,),H|1<<b,T)
        self.outcomes();fill((),0,target,root_action)
        return policy
    def optimize_policy(self,policy,low_action,target):
        """LP varies all signed quadratic coefficients and the theta witness menu."""
        d=len(self.x)
        @lru_cache(None)
        def end(h):
            if len(h)==self.m:return sum(1<<a for a in h)
            return end(h+(policy[h],))
        rows=[]
        for h,a in policy.items():
            S=end(h);H=sum(1<<b for b in h)
            for b in self.labels(self.full^H):
                if a==b:continue
                T=end(h+(b,))
                rows.append(np.r_[self.coeff(b,T)-self.coeff(a,S),0])
        for ss in combinations(range(self.p),self.m-1):
            H=sum(1<<a for a in ss)
            a=max(self.labels(self.full^H),key=lambda a:self.pay(a,H|1<<a))
            rows.append(np.r_[-self.coeff(a,H|1<<a),1])
        objective=np.r_[self.coeff(low_action,target),-1]
        res=linprog(objective,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),
                    bounds=[(-1,1)]*d+[(None,None)],method='highs')
        assert res.success,res.message
        return res

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--p',type=int,default=7)
    ap.add_argument('--m',type=int,default=4);ap.add_argument('--samples',type=int,default=1000)
    ap.add_argument('--lp-every',type=int,default=10);ap.add_argument('--seed',type=int,default=512)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    rng=random.Random(args.seed);d=args.p+args.p*(args.p-1)//2
    start=time.time();minimum=None;lp_best=0.;lp_count=0;failure=None
    for i in range(args.samples):
        x=[rng.randint(-3,3) for _ in range(d)]
        game=Fresh(args.p,args.m,x);out=game.outcomes();theta=game.theta()
        low,a,S=min((game.pay(a,S),a,S) for S in out for a in game.labels(S))
        gap=low-theta;minimum=gap if minimum is None else min(minimum,gap)
        if gap<-1e-8:
            failure={'x':x,'S':game.labels(S),'low_action':a,'theta':theta,'low':low,'sample':i};break
        if args.lp_every and i%args.lp_every==0:
            # Any selected low label belongs to a player, independent of its position.
            policy=game.policy(S)
            res=game.optimize_policy(policy,a,S);lp_count+=1
            lp_best=max(lp_best,-res.fun)
            if res.fun<-1e-7:
                failure={'x':res.x[:-1].tolist(),'S':game.labels(S),'low_action':a,
                         'theta_bound':res.x[-1],'lp_gap':-res.fun,'sample':i,
                         'policy':{','.join(map(str,h)):b for h,b in policy.items()}}
                break
    report={'object':'signed quadratic fresh game, all-history pure SPE',
            'p':args.p,'m':args.m,'seed':args.seed,'samples_completed':i+1,
            'lp_count':lp_count,'minimum_sample_floor_gap':minimum,'lp_best_violation':lp_best,
            'failure':failure,'seconds':time.time()-start,
            'status':'finite exploratory evidence; no general floor theorem'}
    args.output.write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
