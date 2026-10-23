"""Variable-player robust floor using common static follower profiles.

This tests a precise sufficient combinatorial bridge. It uses no SPE solver.
Failures of the bridge are NOT SPE counterexamples.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import random
import sys

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/"tests/audits"))
from customer_attraction import CustomerType, Instance
from customer_attraction_strategy_lp import instance_from_clones, serializable


@lru_cache(None)
def compositions(total,places):
    if places==0:
        return ((),) if total==0 else ()
    return tuple((first,)+suffix for first in range(total+1)
                 for suffix in compositions(total-first,places-1))


def maximal_instance(ins):
    n=ins.topic_count
    signatures=[frozenset(i for i,c in enumerate(ins.customers) if a in c.topics)
                for a in range(n)]
    keep=[a for a in range(n) if not any(signatures[a]<signatures[b] for b in range(n))
          and not any(signatures[a]==signatures[b] for b in range(a))]
    weights={}
    for c in ins.customers:
        mask=frozenset(j for j,a in enumerate(keep) if a in c.topics)
        if mask:weights[mask]=weights.get(mask,0)+c.multiplicity
    return Instance(tuple(ins.topics[a] for a in keep),
                    tuple(CustomerType(mask,w) for mask,w in sorted(weights.items(),key=lambda e:tuple(e[0]))),
                    ins.players)


class JointCopyFloor:
    def __init__(self,ins):
        self.ins=maximal_instance(ins)
        self.s=self.ins.topic_count;self.m=self.ins.players

    def add(self,p,j,q=None):
        if q is None:q=(0,)*self.s
        return tuple(p[a]+q[a]+(a==j) for a in range(self.s))

    @lru_cache(None)
    def no_copy(self,p,j):
        r=self.m-sum(p)
        menu=[]
        for short in compositions(r-1,self.s-1):
            q=short[:j]+(0,)+short[j:]
            menu.append(self.ins.topic_payoff(j,self.add(p,j,q)))
        return min(menu) if menu else None  # +infinity: no no-copy continuation

    @lru_cache(None)
    def floor(self,p):
        r=self.m-sum(p)
        if r<=0:raise ValueError("terminal floor undefined")
        values=[]
        for j in range(self.s):
            menu=[]
            f=self.no_copy(p,j)
            if f is not None:menu.append(f)
            for t in range(r-1):
                for short in compositions(t,self.s-1):
                    q=short[:j]+(0,)+short[j:]
                    menu.append(self.floor(self.add(p,j,q)))
            if not menu:raise AssertionError("copy/no-copy partition empty")
            values.append(min(menu))
        return max(values)

    @lru_cache(None)
    def budget(self,p):
        if sum(p)==self.m:return Fraction(0),()
        candidates=[]
        for j in range(self.s):
            rest,path=self.budget(self.add(p,j))
            candidates.append((rest,(j,)+path))
        rest,path=min(candidates)
        return self.floor(p)+rest,path

    def report(self):
        value,path=self.budget((0,)*self.s)
        p=(0,)*self.s;floors=[]
        for j in path:
            floors.append(self.floor(p));p=self.add(p,j)
        optimum=self.ins.optimal_welfare()
        return {"instance":self.ins.to_dict(),"optimum":optimum,"budget":value,
                "ratio":Fraction(optimum,value) if value else None,"route":path,
                "floors":floors,"half_bridge":2*value>=optimum,
                "floor_states":self.floor.cache_info().currsize}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--topics",type=int,default=5)
    parser.add_argument("--players",type=int,default=4)
    parser.add_argument("--count",type=int,default=50)
    parser.add_argument("--seed",type=int,default=5811)
    parser.add_argument("--instance",type=Path)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    if args.instance:
        report=JointCopyFloor(Instance.from_dict(json.loads(args.instance.read_text()))).report()
    else:
        rng=random.Random(args.seed);worst=None
        for index in range(args.count):
            density=rng.choice([.2,.4,.6,1.])
            clones=[rng.randint(1,10) if rng.random()<density else 0 for _ in range((1<<args.topics)-1)]
            if not any(clones):continue
            ins=instance_from_clones(args.topics,args.players,clones)
            report=JointCopyFloor(ins).report()
            report.update(source=index,seed=args.seed,search_topics=args.topics,search_players=args.players)
            if worst is None or report["ratio"]>worst["ratio"]:
                worst=report
                print(json.dumps(serializable({k:v for k,v in report.items() if k!="instance"})),flush=True)
            if not report["half_bridge"]:break
        report=worst
    args.output.write_text(json.dumps(serializable(report),indent=2)+"\n")
    print(json.dumps(serializable({k:v for k,v in report.items() if k!="instance"})),flush=True)


if __name__=="__main__":main()
