"""Independent rank-one obstruction audit; no author/canonical imports.

Uses an online state-machine parser and rank-pruned breadth-first traversal,
rather than the author's first-departure-plan node generator.
"""
from fractions import Fraction as F
from math import lcm
import json

M=9
L=lcm(*range(1,(M+1)//2+1))
SIZES=[L//((M-i+1)//2) for i in range(M)]+[L]*M

def next_action(history):
    mode='root'; schedule=None; previous=None
    for pos,seen in enumerate(history):
        expected=pos if mode=='root' else (schedule[pos] if mode=='plan' else previous)
        if seen!=expected:
            if mode=='root':
                prefix=list(range(pos)); remain=M-pos
                old=prefix.count(seen); denominator=L//SIZES[seen]
                target=max(old+1,(remain+old+1)//(denominator+1))
                schedule=prefix+[seen]*(target-old)
                fresh=[b for b in range(M,2*M) if b not in schedule]
                schedule=(schedule+fresh)[:M]
                assert len(schedule)==M
                mode='plan'
            else:
                mode='repeat'
        previous=seen
    return len(history) if mode=='root' else (schedule[len(history)] if mode=='plan' else previous)

def finish(prefix):
    h=list(prefix)
    while len(h)<M:h.append(next_action(h))
    return tuple(h)

def utility(outcome,pos):
    action=outcome[pos]
    return F(SIZES[action],outcome.count(action))

nodes=[((),0)]
for depth in range(M-1):
    layer=[(h,rank) for h,rank in nodes if len(h)==depth]
    for h,rank in layer:
        chosen=next_action(h)
        for action in range(2*M):
            childrank=rank+(action!=chosen)
            if childrank<=1:nodes.append((h+(action,),childrank))

rows=0; genuine=0; smallest=None
for h,rank in nodes:
    prescribed=next_action(h)
    actual=utility(finish(h),len(h))
    for action in range(2*M):
        payoff=utility(finish(h+(action,)),len(h))
        slack=actual-payoff
        assert slack>=0,(h,action,actual,payoff)
        rows+=1; genuine+=action!=prescribed
        smallest=slack if smallest is None else min(smallest,slack)

root=finish(())
assert root==tuple(range(M))
welfare=sum(SIZES[a] for a in set(root)); optimum=M*max(SIZES)
history=(M,M+1); chosen=next_action(history); alternative=M+2
u=utility(finish(history),2); v=utility(finish(history+(alternative,)),2)
assert chosen==M+1 and u==F(15,2) and v==F(60,7)
assert len(nodes)==M+(2*M-1)*M*(M-1)//2==621
assert rows==11178 and genuine==10557
assert welfare==262 and optimum==540 and optimum-2*welfare==16

result={'status':'passed independent exact audit; formal policy is not SPE',
        'players':M,'themes':2*M,'customers':sum(SIZES),'W':welfare,'OPT':optimum,
        'retained_histories':len(nodes),'rank0':sum(rank==0 for _,rank in nodes),
        'rank1':sum(rank==1 for _,rank in nodes),'all_action_rows':rows,
        'genuine_alternative_rows':genuine,'minimum_retained_slack':str(smallest),
        'rank2_prescribed_payoff':str(u),'rank2_deviating_payoff':str(v),
        'rank2_row':str(u-v)}
print(json.dumps(result,indent=2))
