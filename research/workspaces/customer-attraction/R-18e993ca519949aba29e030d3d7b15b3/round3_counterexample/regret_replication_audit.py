"""Fraction state audit and full ordered-history regression for the replication family.

Canonical protocol is independently audited on every ordered history for k<=2.
Its general k proof is the induction in regret_replication.md, not finite evidence.
"""
from __future__ import annotations
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, ExactSPESolver

STATES = {'E': (0,0,0), 'Y': (0,1,0), 'XY': (1,1,0),
          'Z': (0,0,1), 'ZZ': (0,0,2)}
REV = {v:k for k,v in STATES.items()}
SETS = ({0,1}, {2,3}, {1,2,3})

def local_pay(action, q):
    return sum((F(1, sum(q[t] for t,S in enumerate(SETS) if x in S))
                for x in SETS[action]), F())

def add(q,a):
    return q[:a]+(q[a]+1,)+q[a+1:]

def classify(q):
    names = tuple(REV.get(tuple(q[j:j+3])) for j in range(0,len(q),3))
    return names if None not in names else None

def choose(names):
    for name,action in [('E',1),('Y',0),('Z',2)]:
        if name in names:
            return 3*names.index(name)+action
    return None

def make_instance(k):
    return Instance.from_topic_sets(
        [{4*j+x for x in S} for j in range(k) for S in SETS], 2*k,
        labels=tuple(f'{t}{j+1}' for j in range(k) for t in 'XYZ'))

def canonical_terminal(q):
    q=tuple(q)
    while (a:=choose(classify(q))) is not None:
        q=add(q,a)
    return q

def expand_strategy(g):
    """BI fallback owns its entire ordered subtree; canonical never overwrites it."""
    solver=ExactSPESolver(g)
    actions={}
    def bi(h,q,target):
        if len(h)==g.players:
            assert q==target
            return
        floor=solver.threshold(q)
        admissible=[a for a in range(g.topic_count)
                    if target in solver.outcomes(add(q,a))
                    and g.topic_payoff(a,target)>=floor]
        chosen=min(admissible)
        actions[h]=chosen
        for a in range(g.topic_count):
            child=add(q,a)
            if a==chosen:
                dest=target
            else:
                dest=min(solver.outcomes(child),
                         key=lambda t:(g.topic_payoff(a,t), t))
            bi(h+(a,),child,dest)
    def canonical(h,q):
        if len(h)==g.players:
            assert choose(classify(q)) is None
            return
        chosen=choose(classify(q)); actions[h]=chosen
        for a in range(g.topic_count):
            child=add(q,a)
            if classify(child) is not None:
                canonical(h+(a,),child)
            else:
                bi(h+(a,),child,min(solver.outcomes(child)))
    canonical((),(0,)*g.topic_count)
    return actions

def full_ordered_audit(k):
    g=make_instance(k); acts=expand_strategy(g)
    clients=[S for j in range(k) for x in range(4)
             for S in [{3*j+t for t,A in enumerate(SETS) if x in A}]]
    def finish(h,first=None):
        p=list(h)
        if first is not None:p.append(first)
        while len(p)<g.players:p.append(acts[tuple(p)])
        return tuple(p)
    def own(path,i):
        return sum((F(1,sum(a in C for a in path)) for C in clients
                    if path[i] in C),F())
    nodes=0;checks=0
    for d in range(g.players):
        for h in itertools.product(range(g.topic_count),repeat=d):
            assert h in acts
            actual=own(finish(h),d)
            for a in range(g.topic_count):
                assert actual>=own(finish(h,a),d),(k,h,a)
                checks+=1
            nodes+=1
    path=finish(())
    assert path==tuple(3*j+1 for j in range(k))+tuple(3*j for j in range(k))
    q=g.counts(path,terminal=True);U=g.player_payoffs(path)
    assert U==(F(2),)*(2*k)
    regrets=[]
    for i in range(g.players):
        gain=max(own(path[:i]+(a,)+path[i+1:],i)-U[i]
                 for a in range(g.topic_count))
        regrets.append(max(F(),gain))
    assert sum(regrets)==F(k,2)
    assert g.welfare(q)==g.optimal_welfare()==4*k
    return {'k':k,'players':2*k,'topics':3*k,'ordered_histories':nodes,
            'deviation_checks':checks,'welfare':4*k,
            'payoffs':list(map(str,U)),'positive_regret':str(sum(regrets)),
            'all_checks_passed':True}

def symbolic_state_audit():
    tables={}
    for name,q in STATES.items():
        tables[name]={t:str(local_pay(a,add(q,a))) for a,t in enumerate('XYZ')}
    assert tables=={
        'E':{'X':'2','Y':'2','Z':'3'},
        'Y':{'X':'2','Y':'1','Z':'2'},
        'XY':{'X':'1','Y':'1','Z':'3/2'},
        'Z':{'X':'3/2','Y':'1','Z':'3/2'},
        'ZZ':{'X':'4/3','Y':'2/3','Z':'1'}}
    cases=0
    for k in range(1,6):
        for names in itertools.product(STATES,repeat=k):
            q=tuple(v for name in names for v in STATES[name])
            chosen=choose(names)
            if chosen is None:continue
            target=canonical_terminal(q)
            # The mover's prescribed payoff is exactly its phase value.
            value=local_pay(chosen%3,target[3*(chosen//3):3*(chosen//3)+3])
            assert value==(F(3,2) if names[chosen//3]=='Z' else F(2))
            for a in range(3*k):
                child=add(q,a)
                j,t=divmod(a,3)
                immediate=local_pay(t,child[3*j:3*j+3])
                if classify(child) is not None:
                    final=canonical_terminal(child)
                    received=local_pay(t,final[3*j:3*j+3])
                    assert received<=value
                else:
                    assert immediate<=value
                cases+=1
    return {'five_state_instantaneous_payoffs':tables,
            'canonical_state_action_cases_k1_through_k5':cases,
            'all_checks_passed':True,
            'scope':'Finite state regression plus exact local table; general k uses written induction.'}

if __name__=='__main__':
    out={'status':'PASS','general_target':'Q-CAG-HALF remains OPEN',
         'symbolic_states':symbolic_state_audit(),
         'full_ordered_regressions':[full_ordered_audit(k) for k in (1,2)],
         'k5_exact_parameters':{'m':10,'W':20,'OPT':20,'R':'5/2','W_over_m':'2'}}
    dest=Path(__file__).with_suffix('.json')
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False,indent=2))
