"""Exact existential all-history SPE encoding; MILP numerics only generate candidates.

The certificate state is (prefix counts, requested terminal counts), not counts.
Shared hostile child targets do not restrict the full-history SPE outcome set.
See README.md for the two directions of the mathematical equivalence.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
import itertools
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'tests/audits'))
from customer_attraction import ExactSPESolver, StrategyCertificate, verify_certificate
from customer_attraction_strategy_lp import (StrategyCone, coverage_row,
    instance_from_clones, integer_clones, payoff_row, serializable)


@lru_cache(None)
def compositions(n, p):
    if p == 1:
        return ((n,),)
    return tuple((v,)+q for v in range(n+1) for q in compositions(n-v,p-1))


def inc(k,a):
    return k[:a]+(k[a]+1,)+k[a+1:]


def add_counts(k,f):
    return tuple(a+b for a,b in zip(k,f))


class FullHistoryMILP:
    def __init__(self,m,p,rootq,portfolio,*,fixed=None,minimum=None,first_action=None):
        assert len(rootq)==p and sum(rootq)==m and min(rootq)>=0
        self.m,self.p,self.rootq,self.portfolio=m,p,tuple(rootq),tuple(portfolio)
        self.n=(1<<p)-1
        self.first_action=first_action
        self.nodes=tuple(k for d in range(m) for k in compositions(d,p))
        self.targets={k:tuple(add_counts(k,f) for f in compositions(m-sum(k),p)) for k in self.nodes}
        self.y={};self.x={};self.by_pair=defaultdict(list);self.pair_actions=defaultdict(list);self.by_branch=defaultdict(list)
        idx=self.n
        self.T={k:idx+i for i,k in enumerate(self.nodes)};idx+=len(self.nodes)
        for k in self.nodes:
            for q in self.targets[k]:
                for a in range(p):
                    if q[a]>k[a]:
                        self.y[k,q,a]=idx;self.by_pair[k,q].append(idx);self.pair_actions[k,q].append((a,idx));idx+=1
        for k in self.nodes:
            if sum(k)==m-1:continue
            for b in range(p):
                child=inc(k,b)
                for d in self.targets[child]:
                    self.x[k,b,d]=idx;self.by_branch[k,b].append((d,idx));idx+=1
        self.lo=np.zeros(idx);self.hi=np.full(idx,m,dtype=float)
        self.integrality=np.zeros(idx,dtype=np.uint8)
        for j in itertools.chain(self.y.values(),self.x.values()):
            self.hi[j]=1;self.integrality[j]=1
        root=(0,)*p
        for (k,q,a),j in self.y.items():
            if k==root and q!=self.rootq:self.hi[j]=0
        if first_action is not None:
            chosen=self.y[root,self.rootq,first_action]
            self.lo[chosen]=self.hi[chosen]=1
        self.rowi=[];self.coli=[];self.data=[];self.lower=[];self.upper=[]
        self.add({j:float(z) for j,z in enumerate(coverage_row(p,[a for a,c in enumerate(rootq) if c])) if z},1,1)
        for a in range(p):
            self.add({j:1 for j in range(self.n) if (j+1)&(1<<a)},ub=m)
        if first_action is not None:
            rootpay=payoff_row(p,self.rootq,first_action)
            for a in range(p):
                self.add({j:float(bool((j+1)&(1<<a)))-m*float(rootpay[j]) for j in range(self.n)},ub=0)
        if fixed is not None:
            den=sum(fixed[j] for j,z in enumerate(coverage_row(p,[a for a,c in enumerate(rootq) if c])) if z)
            if not den:raise ValueError('cannot normalize fixed zero-root-welfare instance')
            for j,v in enumerate(fixed):self.lo[j]=self.hi[j]=float(Fraction(v,den))
        if minimum is not None:
            self.add({j:float(z) for j,z in enumerate(coverage_row(p,portfolio)) if z},lb=minimum)
        self.add({j:1 for j in self.by_pair[root,self.rootq]},1,1)
        for (k,q),js in self.by_pair.items():self.add({j:1 for j in js},ub=1)
        # Every certified target has a selected branch giving that target, and
        # its current mover beats every independently selected hostile branch.
        for (k,q,a),j in self.y.items():
            child=inc(k,a)
            if sum(child)<m:
                row={jj:1 for jj in self.by_pair[child,q]};row[j]=-1
                self.add(row,lb=0)
            row={jj:float(v) for jj,v in enumerate(payoff_row(p,q,a)) if v}
            row[self.T[k]]=-1;row[j]=-m
            self.add(row,lb=-m)
        # One hostile SPE terminal per current state/action, shared across the
        # target-indexed certificates. Sharing is valid by choosing true minima.
        for k in self.nodes:
            for b in range(p):
                child=inc(k,b)
                if sum(child)==m:
                    row={j:-float(v) for j,v in enumerate(payoff_row(p,child,b)) if v}
                    row[self.T[k]]=1;self.add(row,lb=0)
                    continue
                # Every continuation following b covers each b-customer with
                # at most k(B)+(m-|k|) players. This valid guard strengthens
                # the LP relaxation before any hostile endpoint is integral.
                row={j:-1/(sum(k[a] for a in range(p) if (j+1)&(1<<a))+m-sum(k))
                    for j in range(self.n) if (j+1)&(1<<b)}
                row[self.T[k]]=1;self.add(row,lb=0)
                self.add({j:1 for d,j in self.by_branch[k,b]},1,1)
                for d,j in self.by_branch[k,b]:
                    row={jj:1 for jj in self.by_pair[child,d]};row[j]=-1
                    self.add(row,lb=0)
                    row={jj:-float(v) for jj,v in enumerate(payoff_row(p,d,b)) if v}
                    row[self.T[k]]=1;row[j]=-m
                    self.add(row,lb=-m)
        self.matrix=coo_matrix((self.data,(self.rowi,self.coli)),shape=(len(self.lower),idx)).tocsc()
        self.objective=np.zeros(idx)
        self.objective[:self.n]=-np.array(coverage_row(p,portfolio),dtype=float)

    def add(self,row,lb=-np.inf,ub=np.inf):
        i=len(self.lower)
        for j,v in row.items():
            if v:self.rowi.append(i);self.coli.append(j);self.data.append(v)
        self.lower.append(lb);self.upper.append(ub)

    def solve(self,seconds):
        start=time.monotonic()
        res=milp(self.objective,integrality=self.integrality,
            bounds=Bounds(self.lo,self.hi),
            constraints=LinearConstraint(self.matrix,self.lower,self.upper),
            options={'time_limit':seconds,'mip_rel_gap':0.0,'presolve':True})
        info={'status':int(res.status),'message':res.message,'seconds':time.monotonic()-start,
            'variables':len(self.lo),'binary_variables':len(self.x)+len(self.y),
            'rows':len(self.lower),'nonzeros':self.matrix.nnz,
            'floating_objective':float(-res.fun) if res.fun is not None else None,
            'floating_mip_bound':float(-res.mip_dual_bound) if getattr(res,'mip_dual_bound',None) is not None else None,
            'numerical_status_is_not_mathematical_certificate':True}
        return res,info

    def expand(self,values):
        actions={}
        def rec(h,k,q):
            if len(h)==self.m:
                if k!=q:raise AssertionError('wrong certified endpoint')
                return
            choices=[(values[j],a) for a,j in self.pair_actions[k,q]]
            score,a=max(choices)
            if score<.5:raise ValueError('no integral target witness')
            actions[h]=a
            for b in range(self.p):
                child=inc(k,b)
                if b==a:d=q
                elif len(h)==self.m-1:d=child
                else:
                    d,j=max(self.by_branch[k,b],key=lambda z:values[z[1]])
                    if values[j]<.5:raise ValueError('no integral hostile witness')
                rec(h+(b,),child,d)
        rec((),(0,)*self.p,self.rootq)
        return actions


def certify(model,res):
    if res.x is None:return None
    actions=model.expand(res.x)
    cone=StrategyCone(model.p,model.m,actions)
    if cone.root!=model.rootq:raise AssertionError('root endpoint mismatch')
    out=cone.optimize(model.portfolio)
    if not out['certified']:return {'certified':False,'status':out['status']}
    clones=integer_clones(out['values'])
    instance=instance_from_clones(model.p,model.m,clones)
    cert=StrategyCertificate(actions,model.rootq)
    report=verify_certificate(instance,cert)
    if not report.valid:raise AssertionError(str(report))
    welfare=instance.welfare(model.rootq);optimum=instance.optimal_welfare()
    different_targets=defaultdict(set)
    for h,a in actions.items():
        k=tuple(h.count(t) for t in range(model.p));different_targets[k].add(a)
    signatures=[tuple(mask for mask,c in enumerate(clones,1) if c and mask&(1<<a)) for a in range(model.p)]
    catalog_distinct=len(set(signatures))==model.p
    return {'certified':True,'integer_clones':clones,'root_welfare':welfare,'OPT':optimum,
        'ratio':str(Fraction(optimum,welfare)),'portfolio_ratio':str(out['value']),
        'catalog_has_distinct_subsets':catalog_distinct,
        'labelled_game_exceeds_two':optimum>2*welfare,
        'counterexample':catalog_distinct and optimum>2*welfare,'full_ordered_nodes':len(actions),
        'non_markov_count_states':sum(len(v)>1 for v in different_targets.values()),
        'strategy':cert.to_dict()}


def small_test():
    cases=[]
    for m,p,r in [(2,2,[2,1,0]),(3,2,[3,1,0]),(2,3,[1,2,0,2,1,0,3])]:
        instance=instance_from_clones(p,m,r)
        expected=ExactSPESolver(instance).outcomes()
        for q in compositions(m,p):
            if not instance.welfare(q):continue
            model=FullHistoryMILP(m,p,q,tuple(range(min(m,p))),fixed=r)
            out,info=model.solve(10)
            actual=out.x is not None
            assert actual==(q in expected),(m,p,r,q,info,expected)
            if actual:
                actions=model.expand(out.x)
                report=verify_certificate(instance,StrategyCertificate(actions,q))
                assert report.valid,str(report)
            cases.append({'m':m,'p':p,'q':q,'realizable':actual})
    # An independent last-mover calculation gives OPT/W=5/3 for an all-A
    # root with three topics and three movers (attained by disjoint 3,1,1).
    model=FullHistoryMILP(3,3,(3,0,0),(0,1,2),first_action=0)
    out,meta=model.solve(20)
    proof=certify(model,out)
    assert proof and proof['certified'] and proof['ratio']=='5/3',(meta,proof)
    return {'scope':'implementation equivalence checks only; no universal efficiency claim','cases':cases,
        'exact_extraction_regression':{k:v for k,v in proof.items() if k not in ('strategy','integer_clones')}}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--players',type=int,default=5);ap.add_argument('--topics',type=int,default=7)
    ap.add_argument('--root',default='2,3,0,0,0,0,0');ap.add_argument('--portfolio',default='2,3,4,5,6')
    ap.add_argument('--seconds',type=float,default=60);ap.add_argument('--minimum',type=float)
    ap.add_argument('--first-action',type=int)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--self-test',action='store_true')
    args=ap.parse_args()
    if args.self_test:report=small_test()
    else:
        root=tuple(map(int,args.root.split(',')));portfolio=tuple(map(int,args.portfolio.split(',')))
        start=time.monotonic();model=FullHistoryMILP(args.players,args.topics,root,portfolio,minimum=args.minimum,first_action=args.first_action)
        print(json.dumps({'built_seconds':time.monotonic()-start,'variables':len(model.lo),'rows':len(model.lower),'nonzeros':model.matrix.nnz}),flush=True)
        out,meta=model.solve(args.seconds)
        print(json.dumps(meta),flush=True)
        report={'scope':'full arbitrary-history SPE outcome encoding for this fixed m,p,root; floating MILP bounds excluded',
            'universal_half_coverage_status':'OPEN','players':args.players,'topics':args.topics,'root':root,'portfolio':portfolio,'first_action':args.first_action,
            'milp':meta,'certificate':certify(model,out)}
    args.out.write_text(json.dumps(serializable(report),indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='certificate'}),flush=True)
    if report.get('certificate'):print(json.dumps({k:v for k,v in report['certificate'].items() if k not in ('strategy','integer_clones')}),flush=True)


if __name__=='__main__':main()
