"""Definition-level audit, independent of the BI discovery implementation.

Literal 179 unit customers, literal full strategy, Fraction payoffs. No imported
solver, model, discovery function, optimization result or saved action record.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import json

names='ABTQRSP'
raw=[('A',21),('B',18),('T',26),('Q',16),('AR',2),('BR',8),('QR',10),
     ('AS',2),('BS',8),('QS',10),('ARS',10),('TRS',10),('BTRS',2),('BQRS',2),('P',34)]
customers=[frozenset(labels) for labels,count in raw for _ in range(count)]
topics={a:frozenset(i for i,c in enumerate(customers) if a in c) for a in names}
assert len(customers)==179 and len(set(topics.values()))==7
second=dict(zip(names,'RRRRPPA'))
third=dict(zip(names,['BTQTPPB','TTQTPPR','QQQBPPQ','TTBTPPT','PPPPPPS','PPPPPPR','BRRRSRR']))
actions={(): 'P',**{(a,):second[a] for a in names},
         **{(a,b):third[a][names.index(b)] for a,b in product(names,repeat=2)}}
def finish(h):
    while len(h)<3:h=h+(actions[h],)
    return h
def pay(z):
    load=[sum(i in topics[a] for a in z) for i in range(len(customers))]
    return tuple(sum((F(1,load[x]) for x in topics[a]),F(0)) for a in z)
histories=[h for d in range(3) for h in product(names,repeat=d)]
assert set(actions)==set(histories)
comparisons=0;min_slack=None
for h in histories:
    current=pay(finish(h))[len(h)]
    for a in names:
        slack=current-pay(finish(h+(a,)))[len(h)]
        assert slack>=0,(h,a,slack)
        min_slack=slack if min_slack is None else min(min_slack,slack)
        comparisons+=1
base=finish(())
cover=lambda z:frozenset().union(*(topics[a] for a in z))
C=cover(base);tuples=list(combinations_with_replacement(names,3))
opt=max(len(cover(z)) for z in tuples)
optimal=[z for z in tuples if len(cover(z))==opt]
assert optimal==[('A','T','Q')]
O=cover(optimal[0]);D=O-C;outside=C-O
f=[0]+[max(len(D&cover(z)) for z in combinations_with_replacement(names,r)) for r in range(1,4)]
u=pay(base);e=tuple(sum((F(1,sum(x in topics[a] for a in base)) for x in topics[b]-O),F(0)) for b in base)
g=tuple(f[3-i]-f[2-i] for i in range(3))
assert base==('P','A','B') and u==(34,35,38)
assert e==(34,0,34) and sum(e)==len(outside)==68
assert f==[0,36,72,72] and g==(0,36,36)
assert g[1]>u[1]+e[1] and opt<=2*len(C)
result={'claim':'UNIQUE-OPT-ONCE-REFUND-FLOOR is false; HALF not refuted',
        'customers':len(customers),'topic_sizes':{a:len(topics[a]) for a in names},
        'histories':len(histories),'comparisons_including_self':comparisons,
        'minimum_IC_slack':str(min_slack),'path':base,'profits':list(map(str,u)),
        'welfare':len(C),'OPT3':opt,'unique_optimal_multiset':optimal,
        'second_best_values':{a:str(pay(finish((a,)))[1]) for a in names},
        'root_deviation_values':{a:str(pay(finish((a,)))[0]) for a in names},
        'last_best_values':{a:[str(pay((a,b,actions[(a,b)]))[2]) for b in names] for a in names},
        'L':len(D),'E':len(outside),'outside_refunds':list(map(str,e)),
        'missed_cover_profile':f,'position_gaps':g,
        'bad_position_one_based':2,'failure_margin':str(g[1]-u[1]-e[1])}
Path(__file__).with_name('unique_refund_audit.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
