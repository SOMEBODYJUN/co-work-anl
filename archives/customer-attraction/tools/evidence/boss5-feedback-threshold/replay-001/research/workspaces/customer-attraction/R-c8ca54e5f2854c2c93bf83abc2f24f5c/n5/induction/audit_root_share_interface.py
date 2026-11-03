#!/usr/bin/env python3
"""Exact, self-contained local audit for root_share_interface.md."""
from fractions import Fraction as F
from itertools import product
from math import prod

def sh(n,d): return F(n,d) if n else F(0)
def rho(p,v,z):
    a,b,c,d=v; q,r,s=z
    n=sum(v); t=d+q+r+s
    ua=[sh(i,p+n) for i in v]; zz=[sh(i,p+t) for i in (d,q,r,s)]
    den=prod(p+i for i in (1,2,3,4))
    tax=lambda j:F(1,p+1)-F(1,p+j+1)
    delta2=tax(a+b)+(F(2*p*p,3*den) if a+b==2 else 0)
    delta3=tax(a+b+c)+(F(p*p+p,den) if a+b+c==3 else 0)
    K=lambda bit:ua[1]-F(bit,p+a+3)
    H=ua[2]+ua[3]+F(c,(p+a+b+1)*(p+a+b+2))
    P=2*H+delta2; E=4*ua[3]+delta3
    root=ua[0]-zz[0]
    Lqs=zz[1]-F(s,p+d+3)
    Lrc=zz[2]-F(c,p+d+q+2)
    Lrs=zz[2]-F(s,p+d+q+2)
    Lsb=zz[3]-F(b,p+d+q+r+1)
    G=F(1,1000)*(341*K(c)+302*K(d)+306*K(q)+302*K(r)+355*K(s)
       +354*E+646*P+1267*root+24*Lqs+8*Lrc+17*Lrs+108*Lsb)
    return F(1499,750)*sh(n,p+n)-G

raw0=['0','0','1/750','1/1500','1/1500','39/500','1/1000','623/3000',
      '2747/12000','691/6000','47/1500','1919/12000','0','77/750','1/4000','1169/6000']
raw1=['0','133/750','2003/12000','61853/180000','251/3000','6331/22500',
      '7363/36000','26047/60000','239/1200','14579/45000','22183/90000','5177/12000',
      '15767/90000','63893/180000','43349/180000','41143/90000']
vs=list(product((0,1),repeat=4)); table={}
for p,raw in enumerate((raw0,raw1)):
    for v,expected in zip(vs,raw):
        values=[rho(p,v,z) for z in product((0,1),repeat=3)]
        assert min(values)>=0
        assert min(values)==F(expected),(p,v,min(values),expected)
        table[p,v]=min(values)
gamma=F(20233,24000)
values={v:(F(1,2)-F(5,4)*table[1,v])*(1+sum(v)) for v in vs}
assert max(values.values())==gamma
assert [v for v,z in values.items() if z==gamma]==[(1,1,0,0)]
for a in (0,1):
    for ts in product((0,1),repeat=5):
        j=sum(ts)
        direct=sum(sh(j-t,a+j-t) for t in ts)
        expected=F(0) if j==0 else (F(4) if a==0 and j==1 else F(5) if a==0 else F(j-1)+F((5-j)*j,1+j))
        assert direct==expected
        delta=direct/4-int(j>0)+F(a,2)*int(j>0)
        assert delta>=0
beta5=F(1499,600); coefficient=beta5-gamma
assert coefficient==F(39727,24000)
assert (beta5-2)/coefficient==F(11960,39727)
# Check the per-customer algebra between (2) and (5), retaining all credits.
for a,v,ts in product((0,1),vs,product((0,1),repeat=5)):
    k=sum(v); j=sum(ts); opt=int(j>0); w=int(a+k>0)
    u=sh(a,a+k); V=sh(k,a+k)
    f=sum(sh(j-t,a+j-t) for t in ts)
    delta=f/4-opt+F(a,2)*opt
    eta=gamma/F(1+k)-F(1,2)+F(5,4)*table[1,v]
    D=F(a,2)*(1-opt)+(eta if a else F(5,4)*table[0,v])+delta
    assert D>=0
    rhs2=beta5*V+F(a,2)*opt-F(5,4)*table[a,v]-delta
    rhs5=beta5*w-coefficient*u-D
    assert rhs2==rhs5,(a,v,ts,rhs2,rhs5)
print('PASS: 256 rho states; 32 minima; exact gamma; 64 optimum membership states; 1024 full interface identities')
print('Conditional half threshold u1/W >=',F(11960,39727),float(F(11960,39727)))
