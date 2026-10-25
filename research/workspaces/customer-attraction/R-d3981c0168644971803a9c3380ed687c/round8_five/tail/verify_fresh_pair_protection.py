"""Fraction-only local QA for the analytic fresh-pair protection lemma.
No BI, equilibrium solver, or LP is imported. It checks every prescribed
pair deviation and every possible terminal best reply at the named prefix.
"""
from fractions import Fraction as F
from itertools import combinations
import json

edges=list(combinations(range(5),2))
bank=[((2,8),5),((0,1,2,6),12),((3,7),19),((1,2,3,6),9),
      ((0,1,2,3,6),9),((0,1,2,3,7),11),((0,1,2,3,8),12),
      ((4,5),30),((4,9),30)]
base=bank+[((5+i,)+tuple(10+k for k,e in enumerate(edges) if i in e),30) for i in range(5)]

def check(specialist=False):
    data=[(set(t),w) for t,w in base]
    n=20
    if specialist:
        n=25
        # Five H_i: one omission plus one half of the A4 bank.
        for i in range(5):
            data[9+i][0].add(20+i)
            data[7 if i<3 else 8][0].add(20+i)
        data.append(({0,6},8))
    def value(topic,h,bank_only=False):
        return sum((F(w,1+sum(a in t for a in h)) for t,w in data
                    if topic in t and (not bank_only or any(a<5 for a in t))),F(0))
    h=(0,1,4)
    bankA=[value(a,h,True) for a in range(5)]
    single_topics=list(range(5,10))+(list(range(20,25)) if specialist else [])
    bank_single=[value(a,h,True) for a in single_topics]
    assert max(bankA)<60 and max(bank_single)<30
    num=0
    for e in range(10,20):
        vals=[value(a,h+(e,)) for a in range(n)]
        br=[a for a in range(n) if vals[a]==max(vals)]
        assert max(vals)==60
        assert all(10<=a<20 and set(edges[e-10]).isdisjoint(edges[a-10]) for a in br)
        for a in br:
            # Every terminal tie preserves the bank and both economic blocks.
            full=h+(e,a)
            assert value(e,tuple(x for j,x in enumerate(full) if j!=3))==60
            assert sum((F(w,sum(x in t for x in full)) for t,w in data if 4 in t),F(0))==60
        num+=n
    # At position four the last reply is also necessarily an insurer.
    h4=(0,1,2,4)
    vals=[value(a,h4) for a in range(n)]
    br=[a for a in range(n) if vals[a]==max(vals)]
    assert max(vals)==60 and all(10<=a<20 for a in br)
    return {'specialist_extension':specialist,'unit_clients':sum(w for t,w in data),
            'bank_A_prices':[str(x) for x in bankA],
            'single_omission_bank_prices':[str(x) for x in bank_single],
            'pair_branch_terminal_action_comparisons':num,
            'position3_forced_A4_payoff':'60','position4_forced_A4_payoff':'60',
            'scope':'definition-level local QA; universal implication is analytic'}

def threshold_example():
    # Action 0 is pure B; actions 1..10 are lex K5 pairs. R01 is action 1.
    data=[({0,1},3)]
    data += [({1+k for k,e in enumerate(edges) if i in e},1) for i in range(5)]
    def value(a,other):
        return sum((F(w,1+sum(x in t for x in other)) for t,w in data if a in t),F(0))
    n=11
    # Fixed prefix B, actual current R01 and prescribed terminal R01 everywhere.
    for a in range(n):
        assert value(1,(0,a))>=max(value(b,(0,a)) for b in range(n))
        assert value(1,(0,1))>=value(a,(0,1))
    actual=(0,1,1)
    old=sum((F(w,sum(a in t for a in actual)) for t,w in data if 0 in t),F(0))
    assert old==1 and value(1,(0,1))==2
    return {'local_threshold_example':'bank size b=3ell, ell=1',
            'unit_clients':8,'fixed_prefix':[0],'actual_tail':[1,1],
            'old_bank_profit':'1 = b/3','tail_profits':['2','2'],
            'scope':'complete two-player subgame SPE; no five-player root-realizability claim'}

if __name__=='__main__':
    print(json.dumps([check(),check(True),threshold_example()],indent=2))
