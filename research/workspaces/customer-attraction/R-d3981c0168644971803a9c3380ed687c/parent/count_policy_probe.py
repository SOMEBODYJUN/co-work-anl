"""Exact finite CSP for count-only SPE realization of a terminal multiset.

This probes a general reduction, never assumes it. Count state k carries a
terminal target q(k). A local witness action a must realize q(k+e_a)=q(k), and
its terminal payoff must dominate every alternative child's payoff. Generalized
arc consistency is exact per relation; DFS resolves remaining dependencies.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
from random import Random
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver


def inc(q, a):
    return q[:a]+(q[a]+1,)+q[a+1:]


class CountPolicyCSP:
    def __init__(self, instance):
        self.I=instance
        self.solver=ExactSPESolver(instance)
        self.solver.outcomes()
        self.k=instance.topic_count
        self.states=sorted(self.solver._outcomes, key=lambda q:(-sum(q),q))
        self.nodes=[q for q in self.states if sum(q)<instance.players]
        self.children={q:tuple(inc(q,a) for a in range(self.k)) for q in self.nodes}
        self.pay={q:instance.topic_payoffs(q) for q in self.states if sum(q)==instance.players}
        self.visited=0
        self.rejected=0

    def propagate(self, domains):
        changed=True
        while changed:
            changed=False
            for h in self.nodes:
                children=self.children[h]
                supported_parent=set()
                supported_children=[set() for _ in children]
                minima=[min(self.pay[q][a] for q in domains[c]) for a,c in enumerate(children)]
                for q in domains[h]:
                    for a,c in enumerate(children):
                        if q not in domains[c]:continue
                        threshold=self.pay[q][a]
                        if any(v>threshold for v in minima):continue
                        supported_parent.add(q)
                        for b,cb in enumerate(children):
                            if b==a:supported_children[b].add(q)
                            else:supported_children[b].update(t for t in domains[cb] if self.pay[t][b]<=threshold)
                if not supported_parent:return False
                if supported_parent!=domains[h]:
                    domains[h]=supported_parent;changed=True
                for cb,support in zip(children,supported_children):
                    if not support:return False
                    if support!=domains[cb]:domains[cb]=support;changed=True
        return True

    def search(self, domains):
        self.visited+=1
        if not self.propagate(domains):
            self.rejected+=1
            return None
        undecided=[h for h in self.states if len(domains[h])>1]
        if not undecided:return {h:next(iter(v)) for h,v in domains.items()}
        h=min(undecided, key=lambda h:(len(domains[h]),sum(h),h))
        for q in sorted(domains[h]):
            child={h:set(v) for h,v in domains.items()}
            child[h]={q}
            found=self.search(child)
            if found is not None:return found
        return None

    def realize(self, target):
        z=(0,)*self.k
        if target not in self.solver.outcomes():return None
        domains={h:set(self.solver.outcomes(h)) for h in self.states}
        domains[z]={target}
        terminal=self.search(domains)
        if terminal is None:return None
        actions={}
        for h in self.nodes:
            q=terminal[h]
            good=[a for a,c in enumerate(self.children[h]) if terminal[c]==q and
                  all(self.pay[q][a]>=self.pay[terminal[cb]][b] for b,cb in enumerate(self.children[h]))]
            assert good
            actions[h]=good[0]
        self.verify(actions,target)
        return actions

    def verify(self, actions, target):
        # Independent forward replay from EVERY count state, then all local IC.
        out={}
        for h in self.states:
            q=h
            while sum(q)<self.I.players:q=inc(q,actions[q])
            out[h]=q
        for h in self.nodes:
            a=actions[h]
            assert self.I.topic_payoff(a,out[h])>=max(
                self.I.topic_payoff(b,out[inc(h,b)]) for b in range(self.k))
        assert out[(0,)*self.k]==target


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--cases',type=int,default=80)
    p.add_argument('--players',type=int,default=4)
    p.add_argument('--topics',type=int,default=4)
    p.add_argument('--seed',type=int,default=20261023)
    p.add_argument('--output')
    a=p.parse_args();R=Random(a.seed);tested=0;start=time.time();dfs=0
    for it in range(a.cases):
        weights=[R.choice([0,0,1,1,2,3,4]) for _ in range(1,(1<<a.topics))]
        I=Instance(tuple(map(str,range(a.topics))),tuple(CustomerType(
            frozenset(j for j in range(a.topics) if mask>>j&1),w)
            for mask,w in enumerate(weights,1) if w),a.players)
        csp=CountPolicyCSP(I)
        for q in sorted(csp.solver.outcomes()):
            found=csp.realize(q);tested+=1
            if found is None:
                obj={'status':'EXACT_SEPARATION','iteration':it,'instance':I.to_dict(),
                     'target':q,'full_certificate':csp.solver.certificate(q).to_dict() if hasattr(csp.solver.certificate(q),'to_dict') else None,
                     'dfs_nodes':csp.visited,'rejections':csp.rejected,'seed':a.seed}
                print(json.dumps(obj,ensure_ascii=False));
                if a.output:Path(a.output).write_text(json.dumps(obj,indent=2)+'\n')
                return
        dfs+=csp.visited
    obj={'status':'finite_no_separation','cases':a.cases,'players':a.players,'topics':a.topics,'seed':a.seed,
         'terminal_targets':tested,'dfs_nodes':dfs,'seconds':time.time()-start,
         'scope':'Only this finite diagnostic. Does not prove full-history/count-policy equivalence.'}
    print(json.dumps(obj));
    if a.output:Path(a.output).write_text(json.dumps(obj,indent=2)+'\n')

if __name__=='__main__':main()
