"""Floating fixed-policy attack on weak optimal static matching.

Full ordered-history SPE rows are retained (deduplicating identical numerical
rows only). Output is evidence about finitely many policy cones, not a proof.
Any positive candidate still needs integer recovery and complete exact audit.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path
import random
import sys
import time

import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import CustomerType,ExactSPESolver,Instance,StrategyCertificate
from customer_attraction_strategy_lp import StrategyCone,coverage_row,payoff_row
from cone_attack_credible_variants import credible_cone


def optimize(cone,target,unique_margin,query_mode='full'):
    p,m=cone.topics,cone.players;n=(1<<p)-1
    rows=[np.r_[-row,0.] for row in cone.matrix]
    rhs=[0.]*len(rows)
    optimum=np.array(coverage_row(p,target),dtype=float)
    # It suffices to test size-min(p,m) supports: smaller supports extend to one.
    for other in combinations(range(p),min(p,m)):
        if other==target:continue
        rows.append(np.r_[np.array(coverage_row(p,other),dtype=float)-optimum,0.])
        rhs.append(-unique_margin)
    actual=cone.terminals[()]
    path=[];h=()
    while len(h)<m:
        a=cone.actions[h];path.append(a);h=h+(a,)
    # Target is a support with m labels (no repetitions); p>=m is required.
    for assignment in permutations(target):
        query=np.zeros(n)
        if query_mode=='full':
            for old,new in zip(path,assignment):
                counts=list(actual);counts[old]-=1;counts[new]+=1
                query+=np.array(payoff_row(p,tuple(counts),new),dtype=float)
        elif query_mode=='partition':
            for mask in range(1,1<<p):
                owners=[i for i,new in enumerate(assignment) if mask>>new&1]
                if not owners:continue
                c=sum(mask>>old&1 for old in path)
                query[mask-1]=min(1/(c+1-(mask>>path[i]&1)) for i in owners)
        else:raise ValueError(query_mode)
        rows.append(np.r_[-query,1.]);rhs.append(0.)
    objective=np.r_[np.zeros(n),-1.]
    result=linprog(objective,A_ub=np.array(rows),b_ub=rhs,
                   A_eq=[np.r_[np.array(cone.welfare,dtype=float),0.]],
                   b_eq=[1.],bounds=[(0,None)]*n+[(None,None)],method='highs')
    return result,tuple(path)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--topics',type=int,default=6);ap.add_argument('--players',type=int,default=4)
    ap.add_argument('--games',type=int,default=30);ap.add_argument('--seed',type=int,default=104211)
    ap.add_argument('--active-types',type=int,default=10)
    ap.add_argument('--unique-margin',type=float,default=1e-6)
    ap.add_argument('--source',type=Path)
    ap.add_argument('--examples',action='store_true',help='sample canonical example instances rather than random games')
    ap.add_argument('--max-example-topics',type=int,default=7)
    ap.add_argument('--targets',type=int,default=3)
    ap.add_argument('--query-mode',choices=['full','partition'],default='full')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if not 1<=args.players<=args.topics:raise ValueError('require 1<=players<=topics')
    if args.output.exists():raise FileExistsError(args.output)
    rng=random.Random(args.seed);best=None;records=[];seen=set();started=time.monotonic()
    source=json.loads(args.source.read_text()) if args.source else None
    examples=[]
    if args.examples:
        for fp in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
            try:
                instance=Instance.from_dict(json.loads(fp.read_text()))
                if instance.players<=instance.topic_count<=args.max_example_topics:examples.append((fp.name,instance))
            except (KeyError,ValueError,TypeError):pass
        if not examples:raise ValueError('no usable canonical instances')
    for game in range(args.games):
        if source is not None and game==0:
            ins=Instance.from_dict(source['instance']);p,m=ins.topic_count,ins.players
            cert=StrategyCertificate.from_dict(source['certificate'])
            cone=StrategyCone(p,m,dict(cert.actions));mode='source_complete_policy'
        else:
            if examples:
                label,ins=examples[game%len(examples)];p,m=ins.topic_count,ins.players
            else:
                p,m=args.topics,args.players
                masks=rng.sample(range(1,1<<p),min(args.active_types,(1<<p)-1))
                customers=tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),rng.randrange(1,16)) for mask in masks)
                ins=Instance(tuple(map(str,range(p))),customers,m)
            solver=ExactSPESolver(ins)
            target=rng.choice(sorted(solver.worst_outcomes()))
            mode=('max_credible_payoff','max_credible_welfare','min_credible_welfare','uniform_credible')[game%4]
            cone,stats=credible_cone(solver,target,rng,mode)
            cert=StrategyCertificate(cone.actions,cone.root)
        key=tuple(sorted(cone.actions.items()))
        if key in seen:continue
        seen.add(key)
        targets=[t for t in combinations(range(p),m) if ins.welfare(ins.counts(t))==ins.optimal_welfare()]
        rng.shuffle(targets)
        if len(targets)<args.targets:
            extra=[t for t in combinations(range(p),m) if t not in targets]
            rng.shuffle(extra);targets+=extra[:args.targets-len(targets)]
        for target in targets[:args.targets]:
            result,path=optimize(cone,target,args.unique_margin,args.query_mode)
            item={'game':game,'mode':mode,'target':target,'success':result.success,
                  'rows':len(cone.rows),'actual':path}
            if result.success:
                value=float(result.x[-1]);item['min_matching_ratio']=value
                if best is None or value>best['min_matching_ratio']:
                    best=item|{'weights':result.x[:-1].tolist(),'instance':ins.to_dict(),
                               'certificate':cert.to_dict()}
                threshold=1+1/m if args.query_mode=='full' else 1
                if value>threshold+1e-7:
                    records.append(item)
                    report={'status':'floating_candidate_requires_exact_audit','parameters':vars(args)|{'output':str(args.output),'source':str(args.source)},
                            'records':records,'best':best,'elapsed_seconds':time.monotonic()-started}
                    args.output.write_text(json.dumps(report,indent=2)+'\n')
                    print(json.dumps(item),flush=True);return
            records.append(item)
        print(json.dumps({'game':game,'policy_cones':len(seen),'best_ratio':None if best is None else best['min_matching_ratio']}),flush=True)
        checkpoint={'status':'in_progress_finite_policy_sample','parameters':vars(args)|{'output':str(args.output),'source':str(args.source)},
                    'policy_cones':len(seen),'records':records,'best':best,'elapsed_seconds':time.monotonic()-started}
        args.output.write_text(json.dumps(checkpoint,indent=2)+'\n')
    report={'status':'no_floating_separator_in_finite_policy_sample','parameters':vars(args)|{'output':str(args.output),'source':str(args.source)},
            'policy_cones':len(seen),'records':records,'best':best,'elapsed_seconds':time.monotonic()-started}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'records','best','parameters'}}),flush=True)

if __name__=='__main__':main()
