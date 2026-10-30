"""Exact ordered-tree audit of one proposed general theta monotonicity relation.
No normative solver import. Customer multiplicities expand distinct unit clients.
This refutes only the stated auxiliary monotonicity, not TB, SM or HALF.
"""
from fractions import Fraction as Q
from functools import cache
from pathlib import Path
import json

TYPES = [([0],2),([0,1],4),([2],3),([0,2],1),([1,2],5),
         ([3],8),([0,3],1),([1,3],6),([0,1,3],1),([0,1,2,3],8)]
CLIENTS = tuple(frozenset(A) for A,n in TYPES for _ in range(n))
P=5 # topic 4 is empty

def audit(m):
    @cache
    def pay(z):
        load=[sum(a in C for a in z) for C in CLIENTS]
        return tuple(sum((Q(1,c) for C,c in zip(CLIENTS,load) if a in C and c),Q(0)) if a in z else Q(0) for a in range(P))
    floors={}
    @cache
    def R(h):
        if len(h)==m:return frozenset([h])
        children=[R(h+(a,)) for a in range(P)]
        minima=[min(pay(z)[a] for z in zs) for a,zs in enumerate(children)]
        t=max(minima);floors[h]=t
        return frozenset(z for a,zs in enumerate(children) for z in zs if pay(z)[a]>=t)
    R(())
    def strategy(h,target,actions):
        if len(h)==m:return
        t=floors[h]
        a=next(a for a in range(P) if target in R(h+(a,)) and pay(target)[a]>=t)
        actions[h]=a
        for b in range(P):
            child=R(h+(b,))
            z=target if b==a else min(child,key=lambda z:(pay(z)[b],z))
            strategy(h+(b,),z,actions)
    target=min((z for z in R(()) if pay(z)[z[0]]==floors[()]),key=lambda z:z)
    actions={};strategy((),target,actions)
    def leaf(h):
        while len(h)<m:h=h+(actions[h],)
        return h
    checks=0
    for h,a in actions.items():
        chosen=pay(leaf(h))[a]
        for b in range(P):
            assert chosen>=pay(leaf(h+(b,)))[b]
            checks+=1
    root_minima=[min(pay(z)[a] for z in R((a,))) for a in range(P)]
    return {'m':m,'theta':str(floors[()]),'root_L':list(map(str,root_minima)),
            'minimum_leader_path':list(target),'path_payoffs':list(map(str,(pay(target)[a] for a in target))),
            'policy':{'/'.join(map(str,h)):a for h,a in actions.items()},
            'histories':len(actions),'exact_IC_checks':checks,
            'outcome_count':len(R(()))}

if __name__=='__main__':
    data={'scope':'Auxiliary corrected-monotonicity counterexample only; TB/SM/HALF not refuted.',
          'customer_count':len(CLIENTS),'topics':['A','B','C','D','empty'],
          'customers':[{'topics':A,'multiplicity':n} for A,n in TYPES],
          'audits':[audit(m) for m in range(1,5)]}
    vals=[Q(x['theta']) for x in data['audits']]
    assert vals==[Q(24),Q(33,2),Q(19,2),Q(65,6)]
    assert vals[3]-vals[2]==Q(4,3)
    path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='audits'}))
    print(json.dumps([{k:v for k,v in row.items() if k!='policy'} for row in data['audits']],indent=2))
