"""Exact independent replay of the explicit broader-potential counterexample."""
from fractions import Fraction as Q
from itertools import product

A,B,C=range(3)
F={tuple(sorted(s)):Q(2 if C not in s else 4 if s==(C,C,C) else 1)
   for s in product(range(3),repeat=3)}
G={(A,A):Q(1),(A,B):Q(1),(A,C):Q(-2),
   (B,B):Q(1),(B,C):Q(0),(C,C):Q(1)}
policy={():B,(A,):C,(B,):C,(C,):B}
policy.update(dict(zip(product(range(3),repeat=2),[B,B,C,B,B,C,B,A,C])))

def outcome(h):
    h=tuple(h)
    while len(h)<3:h += (policy[h],)
    return h

def utility(a,h):
    return F[tuple(sorted(h+(a,)))]-G[tuple(sorted(h))]

def payoff(s,i):return utility(s[i],s[:i]+s[i+1:])

checked=0
for h,a0 in policy.items():
    z=outcome(h)
    for a in range(3):
        assert payoff(z,len(h))>=payoff(outcome(h+(a,)),len(h))
        checked+=1
actual=outcome(())
assert actual==(B,C,C)
pay=tuple(payoff(actual,i) for i in range(3))
assert pay==(0,1,1)
assert all(utility(a,h)>=0 for h in product(range(3),repeat=2) for a in range(3))
menus=[]
for i in range(3):
    menu=set()
    for a in range(3):
        branch=outcome(actual[:i]+(a,))
        menu.add(tuple(sorted(branch[:i]+branch[i+1:])))
    menus.append(menu)
assert menus==[{(C,C),(A,B)},{(B,B),(B,C)},{(B,C)}]
q={(C,C):Q(1,4),(B,B):Q(3,4)}
p={A:Q(3,4),C:Q(1,4)}
for a in range(3):assert sum(v*utility(a,h) for h,v in q.items())==Q(3,4)
for h in set.union(*menus):assert sum(v*utility(a,h) for a,v in p.items())>=Q(3,4)
assert Q(3,4)>sum(pay)/3
assert utility(C,(C,C))>utility(C,(B,C))
print({'ordered_histories':len(policy),'deviation_checks':checked,'actual':actual,
       'payoffs':pay,'W':sum(pay),'menu_cap':str(Q(3,4)),
       'cap_minus_W_over_m':str(Q(3,4)-sum(pay)/3),
       'scope':'broader symmetric exact-potential game; not CAG'})
