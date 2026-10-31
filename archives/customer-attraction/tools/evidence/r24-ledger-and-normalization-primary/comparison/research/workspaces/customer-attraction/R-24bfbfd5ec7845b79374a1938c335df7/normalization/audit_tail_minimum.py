#!/usr/bin/env python3
"""Independent 36-unit-customer audit; no canonical implementation imports."""
from fractions import Fraction
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
import json

TOPICS=tuple(range(6))
X=frozenset(range(3)); Y=frozenset(range(3,6))
CLIENTS=tuple(frozenset((x,y)) for x in X for y in Y)+tuple(
    frozenset(i+j) for i in combinations(X,2) for j in combinations(Y,2) for _ in range(3))
assert len(CLIENTS)==36

def group(a): return X if a in X else Y

def payoff(path,position):
    return sum((Fraction(1,sum(a in c for a in path)) for c in CLIENTS
                if path[position] in c),Fraction())

def payoffs(path): return tuple(payoff(path,i) for i in range(3))
def welfare(path): return sum(any(a in c for a in path) for c in CLIENTS)

def last(a,b): return min(group(b)-{a,b})

def action(history,normalized):
    if not history: return 0
    if len(history)==1:
        a=history[0]
        if normalized and a==0: return 1
        return min((Y if a in X else X))
    return last(*history)

def terminal(prefix,normalized):
    path=prefix
    while len(path)<3: path=path+(action(path,normalized),)
    return path

report={'customers':len(CLIENTS),'menu_size':6,'players':3,'strategies':[]}
for normalized in (False,True):
    nodes=compares=nonself=0
    for length in range(3):
        for h in product(TOPICS,repeat=length):
            nodes+=1; selected=action(h,normalized)
            actual=terminal(h,normalized); value=payoff(actual,length)
            for a in TOPICS:
                compares+=1; nonself+=a!=selected
                deviated=terminal(h+(a,),normalized)
                assert value>=payoff(deviated,length),(h,a,actual,deviated)
    path=terminal((),normalized)
    report['strategies'].append({'kind':'tail_normalized' if normalized else 'mixed',
       'nodes':nodes,'comparisons_with_self':compares,'comparisons_nonself':nonself,
       'path':path,'payoffs':list(map(str,payoffs(path))),'welfare':welfare(path)})
    assert (nodes,compares,nonself)==(43,258,215)

last_values=[]
for h in product(TOPICS,repeat=2):
    values=[payoff(h+(a,),2) for a in TOPICS]
    best=max(values); last_values.append(best)
    assert best==(15 if h[0]==h[1] else 12)
    assert values[last(*h)]==best
assert min(last_values)==12
report['theta']='12'; report['last_prefixes']=len(last_values)

patterns={}
for path in product(TOPICS,repeat=3):
    counts={a:path.count(a) for a in set(path)}
    ps=tuple(sorted(payoffs(path)))
    if len(counts)==1:
        key='three_equal'; expected=(Fraction(7),)*3
    elif len(counts)==2:
        if len({a in X for a in counts})==1:
            key='same_group_repeat'; expected=(Fraction(9),Fraction(9),Fraction(15))
        else:
            key='cross_group_repeat'; expected=(Fraction(25,3),Fraction(25,3),Fraction(37,3))
    elif len({a in X for a in counts})==1:
        key='same_group_distinct'; expected=(Fraction(12),)*3
    else:
        key='cross_group_distinct'; expected=(Fraction(10),Fraction(12),Fraction(12))
    assert ps==expected,(path,ps,expected)
    assert sum(ps)==welfare(path)
    patterns[key]=patterns.get(key,0)+1
report['terminal_patterns']=patterns; assert sum(patterns.values())==216

@lru_cache(None)
def outcomes(h):
    if len(h)==3: return frozenset({h})
    position=len(h)
    children=[outcomes(h+(a,)) for a in TOPICS]
    floor=max(min(payoff(z,position) for z in child) for child in children)
    return frozenset(z for child in children for z in child if payoff(z,position)>=floor)

all_outcomes=outcomes(())
tail_min_outcomes=[z for z in all_outcomes
    if min(payoffs(z)) in payoffs(z)[1:]]
assert set(map(welfare,all_outcomes))=={34,36}
assert min(map(welfare,all_outcomes))==34
assert set(map(welfare,tail_min_outcomes))=={36}
assert min(map(welfare,tail_min_outcomes))==36
report['ordered_SPE_outcomes']=len(all_outcomes)
report['ordered_tail_min_SPE_outcomes']=len(tail_min_outcomes)
report['minimum_SPE_welfare']=34
report['minimum_tail_min_SPE_welfare']=36
report['exact_relocation_gap']=2

if __name__=='__main__':
    output=Path(__file__).with_name('audit_tail_minimum.json')
    output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
