"""Definition-level audit in Q[s]/(7s^2+23s-5), without other audits."""
from fractions import Fraction as F
from itertools import product
import json

ZERO=(F(0),F(0)); ONE=(F(1),F(0)); S=(F(0),F(1))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def scale(a,c):return (c*a[0],c*a[1])
def sub(a,b):return add(a,scale(b,-1))
def mul(a,b):
    c=a[1]*b[1]
    return (a[0]*b[0]+5*c/7,a[0]*b[1]+a[1]*b[0]-23*c/7)
def total(items):
    a=ZERO
    for b in items:a=add(a,b)
    return a
LO=F(2046453,10**7); HI=F(2046454,10**7)
def P(x):return 7*x*x+23*x-5
assert P(LO)<0<P(HI)
def sign(a):
    if a==ZERO:return 0
    low,high=sorted([a[0]+a[1]*LO,a[0]+a[1]*HI])
    assert low*high>0, a
    return 1 if low>0 else -1

themes=({0,1},{2,3,4,5},{0,1,6},{0,1,7})
last=((1,1,1,1),(1,2,3,2),(1,3,1,1),(1,2,1,1))
def play(h):
    a=list(h)
    if not a:a.append(0)
    if len(a)==1:a.append(1)
    if len(a)==2:a.append(last[a[0]][a[1]])
    return tuple(a)
def pay(path,i):
    return sum((F(1,sum(x in themes[a] for a in path)) for x in themes[path[i]]),F())
comparisons=0
for n in range(3):
    for h in product(range(4),repeat=n):
        equilibrium=play(h); base=pay(equilibrium,n)
        for a in range(4):
            assert base>=pay(play(h+(a,)),n)
            comparisons+=1
assert comparisons==84 and sum(pay(play(()),i) for i in range(3))==6
q=(ZERO,sub(ONE,scale(S,2)),S,S)
assert total(q)==ONE and all(sign(a)>=0 for a in q)
expected=[ZERO]*3; deviations=[[ZERO]*4 for _ in range(3)]; coverage=ZERO
for path in product(range(4),repeat=3):
    probability=ONE
    for a in path:probability=mul(probability,q[a])
    covered=len(set().union(*(themes[a] for a in path)))
    coverage=add(coverage,scale(probability,covered))
    for i in range(3):
        expected[i]=add(expected[i],scale(probability,pay(path,i)))
        for a in range(4):
            alternate=path[:i]+(a,)+path[i+1:]
            deviations[i][a]=add(deviations[i][a],scale(probability,pay(alternate,i)))
for i in range(3):
    for a in range(4):assert sign(sub(expected[i],deviations[i][a]))>=0
assert expected[0]==expected[1]==expected[2]
assert coverage==total(expected)==(F(108,7),F(-312,7))
assert sign(sub(coverage,scale(ONE,6)))==1
# The agent's sqrt(669) expression is the same after sqrt(669)=14s+23.
assert coverage==(F(4344-156*23,49),F(-156*14,49))
result={'status':'exact_pass','histories':21,'SPE_comparisons':comparisons,
        'iid_profiles':64,'static_individual_constraints':12,
        's_polynomial':[7,23,-5], 's_isolating_interval':[str(LO),str(HI)],
        'Z_in_basis_1_s':[str(x) for x in coverage],
        'strict_gap':'Z_3>6=W',
        'scope':'iid Nash welfare dominance refuted; genuine security bridge not refuted'}
print(json.dumps(result,ensure_ascii=False,indent=2))
