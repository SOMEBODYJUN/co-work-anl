#!/usr/bin/env python3
"""Self-contained exact fine three-tail interface and two-prefix payment."""
from fractions import Fraction as F
from itertools import product
from math import comb
import json
from pathlib import Path

P=((0,0,0),(6,5,1),(3,4,1),(2,3,1))
def numerator(p,v,q,r,d,ell):
    a,b,c=v; s=sum(v)
    def ev(j): return sum(F(z)*p**i for i,z in enumerate(P[j]))
    return ((50*s-29*a-36*b-57*c)*ev(s)-30*d*ev(d)
       +(6*q+9*r)*ev(3)+(17*d+2*ell)*ev(a+b+1)+12*d*ev(a+1)
       -4*d*ell*(3-2*a+p)+(14*c-3*r)*ev(c+q+r)+d*ev(c+q+1))
def remainder(p,v,q,r,d,ell):
    return numerator(p,v,q,r,d,ell)/(30*(p+1)*(p+2)*(p+3))
def r3(p,v,d):
    return min(remainder(p,v,q,r,d,ell) for q,r in product((0,1),repeat=2) for ell in range(4))
def H3(p,v,j):
    return sum(comb(j,d)*comb(5-j,3-d)*(F(d,p+d) if d else 0)+
               comb(j,d)*comb(5-j,3-d)*r3(p,v,d)
               for d in range(4) if d<=j and 3-d<=5-j)

def run():
    vs=list(product((0,1),repeat=3)); data={}; states=0
    for p,v,d in product(range(3),vs,range(4)):
        vals=[remainder(p,v,q,r,d,ell) for q,r in product((0,1),repeat=2) for ell in range(4)]
        assert min(vals)>=0
        data[f'{p}:'+''.join(map(str,v))+f':{d}']=str(min(vals)); states+=len(vals)
    gamma=F(59,72); maxima={}
    for p in (1,2):
        vals={(v,j):(int(j>0)-H3(p,v,j)/6)*F(p+sum(v),p) for v,j in product(vs,range(6))}
        maximum=max(vals.values()); maxima[str(p)]=str(maximum)
        assert maximum==(F(401,540) if p==1 else gamma)
        assert [(v,j) for (v,j),z in vals.items() if z==maximum]==[((0,0,1),1)]
    for p,v,j in product(range(3),vs,range(6)):
        k=sum(v); Pold=F(p,p+k) if p else F(0)
        S=H3(p,v,j)/6; opt=int(j>0)
        D=gamma*Pold-opt+S
        assert D>=0,(p,v,j,D)
        V=F(k,p+k) if k else F(0); w=int(p+k>0)
        assert F(25,9)*V+opt-S==F(25,9)*w-F(47,24)*Pold-D
    assert (F(25,9)-2)/F(47,24)==F(56,141)
    # Recover all original remainder values from the expanded slack combination.
    # This independently checks the numerator transcription against Fraction payoffs.
    def sh(n,d): return F(n,d) if n else F(0)
    for p,v,q,r,d,ell in product(range(3),vs,(0,1),(0,1),range(4),range(4)):
        a,b,c=v; s=sum(v)
        alpha,beta,gamma0=[sh(z,p+s) for z in v]
        G=(29*alpha+36*beta+57*gamma0-F(6*q+9*r,p+3)
           -F(17*d+2*ell,p+a+b+1)-F(12*d,p+a+1)
           +F(4*d*ell,(p+a+1)*(p+a+2))-14*sh(c,p+c+q+r)
           +3*sh(r,p+c+q+r)-F(d,p+c+q+1))
        assert remainder(p,v,q,r,d,ell)==F(5,3)*sh(s,p+s)-sh(d,p+d)-G/30
    out={'status':'exact_local_identity_audit_passed','r3_minima':data,'gamma_by_background':maxima,
         'gamma':'59/72','prefix_profit_coefficient':'47/24','half_threshold':'56/141',
         'local_remainder_states':states,'profile_states':3*8*6}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(f'PASS: {states} exact remainder states; 96 minima; 144 profile states; gamma59/72; threshold56/141')
    print('| p,v | r3 d0 | r3 d1 | r3 d2 | r3 d3 |')
    print('| --- | ---: | ---: | ---: | ---: |')
    for p,v in product(range(3),vs):
        print('| '+str(p)+','+''.join(map(str,v))+' | '+' | '.join(str(r3(p,v,d)) for d in range(4))+' |')
if __name__=='__main__': run()
