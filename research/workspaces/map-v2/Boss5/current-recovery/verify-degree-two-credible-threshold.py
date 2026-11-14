from fractions import Fraction
from functools import cache
from math import lcm

for q,a,b in [(2,0,1),(3,0,1),(4,0,1),(5,0,1),(2,1,2),(3,1,2),(4,1,2),(5,3,4),(2,1,1),(3,1,1),(4,1,1),(5,2,2)]:
    m=q+1
    p=2*q
    scale=lcm(*range(1,m+1))
    floor=Fraction(q*b,2)+(q-1)*a
    optimum=q*q*b+Fraction((q-1)*(q+2)*a,2)
    def weight(i,j):
        return a if i//q==j//q else b
    @cache
    def u(z,i):
        return sum(weight(i,j)*(scale//(z[i]+z[j])) for j in range(p) if j!=i)
    @cache
    def R(h):
        if sum(h)==m:
            return frozenset([h])
        kids=[R(h[:i]+(h[i]+1,)+h[i+1:]) for i in range(p)]
        values=[min(u(z,i) for z in k) for i,k in enumerate(kids)]
        for i in range(p):
            if not h[i]:
                assert values[i]>=scale*floor
        theta=max(values)
        return frozenset(z for i,k in enumerate(kids) for z in k if u(z,i)>=theta)
    def W(z):
        return sum(weight(i,j) for i in range(p) for j in range(i+1,p) if z[i] or z[j])
    root=R((0,)*p)
    assert all(min(u(z,i) for z in R(tuple(int(j==i) for j in range(p))))==scale*floor for i in range(p))
    assert all(2*q*W(z)>=(q+1)*optimum for z in root)
    assert all(W(z)==optimum for z in root)
    if a:
        assert all(max(z)==1 for z in root)
    print(q,a,b,R.cache_info().currsize,len(root),min(map(W,root)),str(floor))
