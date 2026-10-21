"""Definition-level exact check of the three-singleton CCE/security gap."""
from fractions import Fraction as F
from itertools import product, permutations
from collections import Counter

def u(a,z):
    return F(1,z.count(a))

def replacement(a,z,i):
    q=list(z);q[i]=a
    return u(a,q)

n=k=3
backgrounds=list(product(range(k),repeat=n-1))
query=F(1,k)
values={B:sum((query*F(1,1+B.count(a)) for a in range(k)),F()) for B in backgrounds}
assert min(values.values())==F(2,3)
pairs=list(__import__('itertools').combinations(range(k),2))
assert all(sum((F(1,len(pairs))*F(1,1+B.count(a)) for B in pairs),F())==F(2,3) for a in range(k))
rows={}
for z in product(range(k),repeat=n):
    typ=tuple(sorted(Counter(z).values(),reverse=True))
    W=len(set(z))
    # Average action labels, which is equivalent to a uniform label orbit.
    H=sum((sum((replacement(a,z,i) for i in range(n)),F()) for a in range(k)),F())/k
    assert W-F(9,10)*(W-H)>=F(21,10)
    assert all(sum((replacement(a,z,i) for i in range(n)),F()) == (n if z.count(a)==0 else F(n+1,z.count(a)+1)) for a in range(k))
    rows.setdefault(typ,set()).add((F(W),H))
assert rows=={(3,):{(F(1),F(7,3))},(2,1):{(F(2),F(19,9))},(1,1,1):{(F(3),F(2))}}
Q=[]
double=[z for z in product(range(k),repeat=n) if len(set(z))==2]
distinct=[z for z in product(range(k),repeat=n) if len(set(z))==3]
Q += [(z,F(9,10*len(double))) for z in double]
Q += [(z,F(1,10*len(distinct))) for z in distinct]
assert sum((p for z,p in Q),F())==1
EW=sum((p*len(set(z)) for z,p in Q),F())
assert EW==F(21,10)
for i in range(n):
    actual=sum((p*u(z[i],z) for z,p in Q),F())
    assert actual==F(7,10)
    for a in range(k):
        dev=sum((p*replacement(a,z,i) for z,p in Q),F())
        assert actual>=dev
print('PASS: v3=2/3; n*v3=2; minimum static CCE welfare=21/10; load-kernel identity exact on all 27 profiles.')
