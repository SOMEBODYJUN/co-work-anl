"""Seeded exact probe of rank-two customer incidence, not a universal proof."""
import argparse
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver

def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(total-first, parts-1):
                yield (first,)+rest

def theta(instance):
    result = None
    for prefix in compositions(instance.players-1, instance.topic_count):
        best = max(sum((Fraction(c.multiplicity,
                         1+sum(prefix[b] for b in c.topics))
                        for c in instance.customers if a in c.topics), Fraction())
                   for a in range(instance.topic_count))
        result = best if result is None else min(result,best)
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--cases',type=int,default=1000)
    p.add_argument('--seed',type=int,default=381097)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    rng=random.Random(args.seed)
    worst=Fraction(1)
    report={'seed':args.seed,'requested_cases':args.cases,'rank_bound':2,
            'weight_pool':[0,0,0,1,2,3,5,8,13,21], 'cases':0,
            'players_range':[3,5], 'topics_range':[3,6],
            'aggregate_theta_failures':[],'root_theta_failures':[],
            'half_failures':[]}
    for case in range(args.cases):
        topics=rng.randrange(3,7)
        players=rng.randrange(3,6)
        cs=[]
        for size in [1,2]:
            for support in combinations(range(topics),size):
                mass=rng.choice(report['weight_pool'])
                if mass:cs.append(CustomerType(frozenset(support),mass))
        instance=Instance(tuple(map(str,range(topics))),tuple(cs),players)
        solver=ExactSPESolver(instance)
        root=solver.outcomes()
        minimum=min(instance.welfare(q) for q in root)
        th=theta(instance)
        threshold=solver.threshold((0,)*topics)
        optimum=instance.optimal_welfare()
        ratio=Fraction(optimum,minimum) if minimum else Fraction(1)
        if ratio>worst:
            worst=ratio
            report['worst_ratio']={'ratio':str(ratio),'case':case,
                                   'instance':instance.to_dict(),
                                   'minimum_welfare':minimum,'optimum':optimum}
        if minimum<players*th:
            report['aggregate_theta_failures'].append({
                'case':case,'instance':instance.to_dict(),'theta':str(th),
                'minimum_welfare':minimum,'optimum':optimum,
                'outcomes':[list(q) for q in root
                            if instance.welfare(q)==minimum]})
        if threshold<th:
            report['root_theta_failures'].append({
                'case':case,'instance':instance.to_dict(),'theta':str(th),
                'root_threshold':str(threshold),'minimum_welfare':minimum,
                'optimum':optimum})
        if 2*minimum<optimum:
            report['half_failures'].append(report['worst_ratio'])
        report['cases']+=1
    result=json.dumps(report,indent=2)
    if args.output:
        with args.output.open('x') as f:f.write(result+'\n')
    else:print(result)

if __name__=='__main__':main()
