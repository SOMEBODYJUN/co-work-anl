"""Independent exact audit of a finite-layer DR mechanism counterexample.
This is a larger potential-game class, explicitly NOT a CAG instance.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import json

base=Path(__file__).parents[1]
raw=json.loads((base/'fullslots/dr_counterexample_exact.json').read_text())
P={tuple(map(int,k.split(','))):F(v) for k,v in raw['potential'].items()}
pi={tuple(map(int,k.split(','))) if k else ():v for k,v in raw['strategy'].items()}
def add(q,a):return tuple(v+int(i==a) for i,v in enumerate(q))
def count(z):return tuple(z.count(i) for i in range(4))
mono=dr=ic=0
for q,v in P.items():
    if sum(q)<4:
        for a in range(4):assert P[add(q,a)]>=v;mono+=1
    if sum(q)<3:
        for a,b in combinations_with_replacement(range(4),2):
            assert P[add(add(q,a),b)]-P[add(q,a)]-P[add(q,b)]+v<=0
            dr+=1
def end(h):
    while len(h)<3:h+=(pi[h],)
    return h
def utility(z,i):return P[count(z)]-P[count(z[:i]+z[i+1:])]
for n in range(3):
    for h in product(range(4),repeat=n):
        for a in range(4):
            assert utility(end(h),n)>=utility(end(h+(a,)),n);ic+=1
B=end(());U=[utility(B,i) for i in range(3)]
assert B==(0,1,2) and U==[F(2),F(3),F(3)]
menus=[]
for i in range(3):
    row=[]
    for a in range(4):
        z=end(B[:i]+(a,));q=count(z)
        row.append(sum((P[add(q,t)]-P[q] for t in range(4)),F())/4)
    assert row==[F(11,4)]*4
    menus.append(min(row))
assert sum(menus)-sum(U)==F(1,4)
# Fixed-m terminal utility already contradicts CAG's naked load lower bound.
stack_u=P[(3,0,0,0)]-P[(2,0,0,0)]
theme_size=3*stack_u
assert stack_u==3 and U[0]==2<theme_size/3
out={'scope':'Finite layers |q|<=4 only; no infinite-domain extension claimed; NOT CAG.',
 'potential_states':len(P),'monotonic_edges':mono,'DR_squares':dr,'ordered_history_IC':ic,
 'actual':B,'utilities':list(map(str,U)),'full_menu_minima':list(map(str,menus)),
 'full_SUMmin_gap':str(sum(menus)-sum(U)),
 'CAG_impossible':{'inferred_theme0_size':str(theme_size),'required_minimum':str(theme_size/3),'observed':'2'}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
