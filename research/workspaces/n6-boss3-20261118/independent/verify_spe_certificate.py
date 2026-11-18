"""Replay every ordered history of a six-player pure strategy certificate.

This verifier does not use the attainable-outcome recursion or trust DP outputs.
It checks every off-path node against every action's actual recursively replayed
continuation in the single supplied complete strategy, with exact integer payoffs.
"""
import argparse
import csv
import hashlib
import itertools
import json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('instance',type=Path);p.add_argument('certificate',type=Path);a=p.parse_args()
obj=json.loads(a.instance.read_text());assert obj['players']==6
A=obj['actions'];w=obj['weights'];assert len(w)==1<<A
assert all(isinstance(v,int) and v>=0 for v in w)
rows=list(csv.DictReader(a.certificate.open()))
strategy={}
for row in rows:
    h=() if row['history']=='_' else tuple(map(int,row['history']))
    assert h not in strategy and len(h)<6 and all(0<=b<A for b in h)
    b=int(row['action']);assert 0<=b<A;strategy[h]=b
expected=sum(A**d for d in range(6));assert len(strategy)==expected
checks=0;leaves=0;min_slack=None

def utility(action,counts):
    z=0
    for mask in range(1,1<<A):
        if w[mask] and mask>>action&1:
            load=sum(counts[b] for b in range(A) if mask>>b&1)
            assert load>0
            z+=60*w[mask]//load
    return z

def replay(h):
    global checks,leaves,min_slack
    if len(h)==6:
        leaves+=1
        return tuple(h.count(b) for b in range(A))
    assert h in strategy
    suffix_outcomes=[replay(h+(b,)) for b in range(A)]
    b=strategy[h];actual=suffix_outcomes[b];u=utility(b,actual)
    for alt in range(A):
        deviation=utility(alt,suffix_outcomes[alt]);slack=u-deviation
        assert slack>=0,(h,b,alt,u,deviation)
        min_slack=slack if min_slack is None else min(min_slack,slack)
        checks+=1
    return actual

def welfare(counts):
    return sum(w[m] for m in range(1,1<<A) if any(counts[b]>0 and m>>b&1 for b in range(A)))

def compositions(total, slots):
    if slots==1:yield(total,)
    else:
        for v in range(total+1):
            for tail in compositions(total-v,slots-1):yield(v,)+tail
actual=replay(())
W=welfare(actual);opt=max(welfare(y) for y in compositions(6,A))
result={'decision_nodes':expected,'terminal_histories':leaves,'deviation_checks':checks,'all_history_SPE':True,'minimum_utility_slack_times_60':min_slack,'root_terminal_counts':actual,'W':W,'OPT_6':opt,'half_coverage_holds':2*W>=opt,'strategy_sha256':hashlib.sha256(a.certificate.read_bytes()).hexdigest()}
print(json.dumps(result,indent=2,sort_keys=True))
