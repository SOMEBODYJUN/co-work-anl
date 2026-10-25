"""Independent polynomial reconstruction of the n5 root-share interface.

Uses four_remaining_profit_bound.md (13),(14), rather than the author's
fractional slack implementation. Complete local algebra audit, not an SPE scan.
"""
from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path
import json


def rho(p,v,z):
    a,b,c,d=v; q,r,s=z
    den=prod(p+i for i in range(1,5))
    def P(j):return F(den,p+j) if j else F(0)
    def Q(j):return F(den,(p+j)*(p+j+1))
    k=sum(v); t=d+q+r+s
    K=lambda l:b*P(k)-l*P(a+3)
    H=(c+d)*P(k)+c*Q(a+b+1)
    PP=2*H+P(1)-P(a+b+1)+(F(2,3)*p*p if a+b==2 else 0)
    E=4*d*P(k)+P(1)-P(a+b+c+1)+(p*p+p if a+b+c==3 else 0)
    FF=a*P(k)-d*P(t)
    L1=q*P(t)-s*P(d+3)
    L2=r*P(t)-c*P(d+q+2)
    L3=r*P(t)-s*P(d+q+2)
    L4=s*P(t)-b*P(d+q+r+1)
    N=23984*k*P(k)-12*(341*K(c)+302*K(d)+306*K(q)+302*K(r)+355*K(s)+354*E+646*PP+1267*FF+24*L1+8*L2+17*L3+108*L4)
    return N/(12000*den)


def main():
    vs=list(product((0,1),repeat=4)); zs=list(product((0,1),repeat=3))
    table={(p,v):min(rho(p,v,z) for z in zs) for p in (0,1) for v in vs}
    assert all(x>=0 for x in table.values())
    gamma=max((F(1,2)-F(5,4)*table[1,v])*(1+sum(v)) for v in vs)
    assert gamma==F(20233,24000)
    maxima=[v for v in vs if (F(1,2)-F(5,4)*table[1,v])*(1+sum(v))==gamma]
    assert maxima==[(1,1,0,0)]
    count=0
    for a,v,ts in product((0,1),vs,product((0,1),repeat=5)):
        k=sum(v); j=sum(ts); o=int(j>0); w=int(a+k>0)
        current=F(a,a+k) if a else F(0)
        tail=F(k,a+k) if k else F(0)
        f=sum((F(j-t,a+j-t) if j-t else F(0)) for t in ts)
        delta=f/4-o+F(a,2)*o
        eta=gamma/F(1+k)-F(1,2)+F(5,4)*table[1,v]
        credit=F(a,2)*(1-o)+(eta if a else F(5,4)*table[0,v])+delta
        assert delta>=0 and credit>=0
        lhs=F(1499,600)*tail+F(a,2)*o-F(5,4)*table[a,v]-delta
        rhs=F(1499,600)*w-F(39727,24000)*current-credit
        assert lhs==rhs
        count+=1
    out={'status':'pass','scope':'complete local polynomial identities; no full half theorem',
         'rho_states':256,'root_table_entries':32,'membership_identities':count,
         'gamma':str(gamma),'gamma_maximizer':maxima,
         'root_share_coefficient':'39727/24000','sufficient_share_threshold':'11960/39727',
         'table':{str(p)+':'+''.join(map(str,v)):str(x) for (p,v),x in table.items()}}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__':main()
