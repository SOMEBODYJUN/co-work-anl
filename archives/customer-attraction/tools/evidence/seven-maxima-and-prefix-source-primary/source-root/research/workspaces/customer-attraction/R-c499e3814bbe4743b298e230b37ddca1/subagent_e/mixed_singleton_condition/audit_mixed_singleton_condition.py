"""Exact residual audit for the seven-maxima m=6 mixed singleton condition.

The row combination is the dense_shared_seven_n6 certificate.  It uses only
M_0..M_3, L_1..L_6 and T_{0j}; for t<=3 the shared B_t coefficient is
no larger than the valid private mixed-floor coefficient, so these rows remain
valid on singleton columns.  The comparator omits maximal index o.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement

N,S=6,7
B=[F(1,21),F(2,37),F(1,16),F(2,27),F(1,11),F(7,72)]
PAIRS=list(combinations_with_replacement(range(S),2)); PAIRS.sort()
LAM=[F(207,355),F(417,710),F(253,426),F(133,213),F(0),F(0)]
LAM += [F(0), *([F(8,71)]*6)]
LAM += [F(0), *([F(7,71)]*6)]
LAM += [F(0)]*21
assert len(LAM)==41

def residual(I,E,o):
    final=int(bool(I&1))
    J=E | (final<<5)
    z=J.bit_count()
    sh=[F((J>>t)&1,z) if z else F(0) for t in range(N)]
    coeff=[sh[t]-B[t] for t in range(N)]
    coeff += [sh[-1]-F((I>>j)&1,E.bit_count()+1) for j in range(S)]
    h=(E & ((1<<4)-1)).bit_count()
    d=(E>>4)&1
    for j,k in PAIRS:
        v=((I>>j)&1)+((I>>k)&1)
        tax=F(d,(h+1)*(h+2))
        coeff.append(sh[-2]+sh[-1]-(F(v,h+v) if v else F(0))+tax)
    # Six-maxima comparator omits B_o.  A singleton I={o} is outside OPT.
    target=F(int(bool(J)),1) if I==(1<<o) else F(int(bool(J)),1)-F(1,2)
    return target-sum(a*b for a,b in zip(LAM,coeff)),J

def main():
    dense_min=None
    singleton={}
    for o in range(S):
        singleton[o]={j:None for j in range(S)}
        for I in range(1,1<<S):
            for E in range(1<<(N-1)):
                r,J=residual(I,E,o)
                if I.bit_count()>=2:
                    dense_min = r if dense_min is None or r<dense_min else dense_min
                else:
                    j=I.bit_length()-1
                    old=singleton[o][j]
                    singleton[o][j]=r if old is None or r<old else old
    print({"dense_min":str(dense_min)})
    for o in range(S):
        print("omit",o,{j:str(singleton[o][j]) for j in range(S)})
    # Constants used by the stated sufficient condition.
    delta=F(15591089,238321440)
    d0=F(7905391,238321440)
    d=F(34758511,238321440)
    p0=F(111255329,238321440)
    p=F(84402209,238321440)
    assert dense_min==delta
    for o in range(S):
        for j in range(S):
            if j==o:
                assert singleton[o][j] >= (p0 if o==0 else p)
            elif j==0:
                assert singleton[o][j] >= -d0
            else:
                assert singleton[o][j] >= -d
    print({"constants":"verified","delta":str(delta),"d0":str(d0),"d":str(d),
           "p0":str(p0),"p":str(p)})
if __name__=="__main__":
    main()
