"""Exact attainable-outcome DP, then export one complete ordered-history strategy.

All client weights are integers. Utilities are multiplied by lcm(1,...,6)=60.
The certificate format has one action for each history of length 0,...,5.
"""
import argparse
import functools
import itertools
import json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('instance',type=Path)
p.add_argument('certificate',type=Path)
a=p.parse_args()
obj=json.loads(a.instance.read_text())
assert obj['players']==6
A=obj['actions']; w=obj['weights']; assert len(w)==1<<A
assert all(isinstance(v,int) and v>=0 for v in w)

def compositions(total, slots):
    if slots==1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(total-first,slots-1):
                yield (first,)+rest

def child(q,action):
    z=list(q);z[action]+=1;return tuple(z)

@functools.lru_cache(None)
def payoff(y,action):
    ans=0
    for mask in range(1,1<<A):
        if w[mask] and (mask>>action)&1:
            load=sum(y[b] for b in range(A) if (mask>>b)&1)
            assert load>0
            ans+=60*w[mask]//load
    return ans

@functools.lru_cache(None)
def feasible(q):
    if sum(q)==6:return frozenset([q])
    children=[feasible(child(q,b)) for b in range(A)]
    threshold=max(min(payoff(y,b) for y in children[b]) for b in range(A))
    return frozenset(y for b in range(A) for y in children[b] if payoff(y,b)>=threshold)

root=(0,)*A
wanted=tuple(obj['root_terminal_counts'])
assert wanted in feasible(root)
rows=[]
def export(history,q,target):
    if len(history)==6:
        assert q==target
        return
    children=[feasible(child(q,b)) for b in range(A)]
    minimizers=[min(children[b],key=lambda y:(payoff(y,b),y)) for b in range(A)]
    threshold=max(payoff(minimizers[b],b) for b in range(A))
    chosen=next(b for b in range(A) if target in children[b] and payoff(target,b)>=threshold)
    rows.append((''.join(map(str,history)) or '_',chosen))
    for b in range(A):
        export(history+(b,),child(q,b),target if b==chosen else minimizers[b])
assert A<=10,'single digit certificate format'
export((),root,wanted)
a.certificate.write_text('history,action\n'+''.join(f'{h},{b}\n' for h,b in rows))
print(json.dumps({'states':feasible.cache_info().currsize,'root_feasible_terminal_counts':len(feasible(root)),'decision_nodes':len(rows),'root_terminal_counts':wanted,'certificate':str(a.certificate)},sort_keys=True))
