"""One existing full cone diagnostic of MIN-PI, not a theorem or main counterexample."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from math import lcm
import json
import argparse
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[6]
SOURCE=ROOT/'research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round2/global/pi_fixed_cone_counterexample.json'
old=json.loads(SOURCE.read_text())
k=6;m=3
masks=list(range(1,1<<k))
strategy={tuple(row['history']):row['action'] for row in old['strategy']['actions']}
def rollout(h):
    h=tuple(h)
    while len(h)<m:h=h+(strategy[h],)
    return h
def payfeatures(h,i):
    return [F(1,sum(bool(mask>>a&1) for a in h)) if mask>>h[i]&1 else F(0) for mask in masks]
def counts(tup):return tuple(tup.count(a) for a in range(k))
def potential(q):
    return [sum((F(1,j) for j in range(1,sum(q[a] for a in range(k) if mask>>a&1)+1)),F(0)) for mask in masks]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
profiles={s:[counts(tuple(t)) for t in combinations_with_replacement(range(k),s)] for s in range(m+2)}
features={s:[potential(q) for q in profiles[s]] for s in profiles}
wold=[0]*len(masks)
for x in old['instance']['customers']:
    mask=sum(1<<a for a in x['topics']);wold[mask-1]=x['multiplicity']
chosen={s:max(range(len(profiles[s])),key=lambda j:dot(features[s][j],wold)) for s in profiles}
root=payfeatures(rollout(()),0)
ic=[]
for depth in range(m):
    for h in product(range(k),repeat=depth):
        actual=payfeatures(rollout(h),depth)
        for a in range(k):
            dev=payfeatures(rollout(h+(a,)),depth)
            ic.append([x-y for x,y in zip(actual,dev)])
rows=[[-float(x) for x in row]+[0.] for row in ic]
for s in range(1,m+2):
    selected=features[s][chosen[s]]
    for previous in features[s-1]:
        rows.append([float(u-d+p) for u,d,p in zip(root,selected,previous)]+[1.])
objective=[0.]*len(masks)+[-1.]
result=linprog(objective,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),A_eq=np.array([[1.]*len(masks)+[0.]]),b_eq=[1.],bounds=[(0,None)]*len(masks)+[(None,None)],method='highs')
report={'scope':'One existing full strategy cone and one chosen potential-profile family; MIN-PI only, not half.','status':str(result.message),'objective':None if not result.success else float(result.x[-1]),'old_root':str(dot(root,wold)),'old_maximum_potentials':{str(s):str(dot(features[s][chosen[s]],wold)) for s in profiles}}
if result.success and result.x[-1]>1e-8:
    rational=[F(float(v)).limit_denominator(1000000) for v in result.x[:-1]]
    denominator=lcm(*(v.denominator for v in rational))
    weights=[int(v*denominator) for v in rational]
    min_ic=min(dot(row,weights) for row in ic)
    exact_p={s:max(dot(row,weights) for row in features[s]) for s in profiles}
    u=dot(root,weights);increments=[exact_p[s]-exact_p[s-1] for s in range(1,m+2)]
    distinct=all(any(w and bool(mask>>a&1)!=bool(mask>>b&1) for mask,w in zip(masks,weights)) for a in range(k) for b in range(a+1,k))
    actual=rollout(())
    covered=lambda t:sum(w for mask,w in zip(masks,weights) if any(mask>>a&1 for a in t))
    opt=max(covered(tuple(t)) for t in combinations_with_replacement(range(k),m))
    report.update({'integer_weights':{str(mask):w for mask,w in zip(masks,weights) if w},'strategy':old['strategy'],'number_of_unit_customers':sum(weights),'IC_comparisons_including_self':len(ic),'exact_minimum_IC':str(min_ic),'actual':actual,'actual_payoffs':[str(dot(payfeatures(actual,i),weights)) for i in range(m)],'actual_welfare':covered(actual),'actual_harmonic_potential':str(dot(potential(counts(actual)),weights)),'OPT':opt,'exact_root':str(u),'exact_potentials':{str(s):str(v) for s,v in exact_p.items()},'exact_potential_maximizers':{str(s):profiles[s][next(j for j,row in enumerate(features[s]) if dot(row,weights)==exact_p[s])] for s in profiles},'exact_increments':list(map(str,increments)),'exact_min_increment_minus_root':str(min(increments)-u),'distinct_coverage_topics':distinct,'verified_counterexample':bool(min_ic>=0 and min(increments)>u and distinct)})
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path)
args=parser.parse_args()
encoded=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
if args.output:
    with args.output.open('x') as handle:handle.write(encoded)
print(encoded,end='')
