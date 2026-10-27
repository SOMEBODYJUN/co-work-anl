from fractions import Fraction as F
from itertools import combinations_with_replacement
N=6; S=7
B=[F(1,21),F(2,37),F(1,16),F(2,27),F(1,11),F(7,72)]
PAIRS=list(combinations_with_replacement(range(S),2)); PAIRS.sort()
# variables are M0..M5,L0..L6,T00..T66

def lam_for(kind):
    lam=[F(0)]*41
    if kind=='with_final':
        for i in range(4): lam[i]=F(133,207)
        lam[7]=F(4,23)
        for i in range(8,13):lam[i]=F(2,23)
        for idx,val in {14:F(31,207),15:F(19,207),16:F(4,69),17:F(19,207),18:F(19,207),19:F(19,207),22:F(7,207)}.items():lam[idx]=val
    elif kind=='without_final':
        lam[0]=F(416,635);lam[1]=F(833,1270);lam[2]=F(167,254);lam[3]=F(84,127)
        lam[7]=F(10,127)
        for i in range(8,13):lam[i]=F(16,127)
        for idx in (14,15):lam[idx]=F(25,127)
        for idx in (16,17,18,19,22,23,24,30):lam[idx]=F(3,127)
    else: raise ValueError(kind)
    return lam

def rows(I,E):
    # true final maximal action is B0, hence final membership iff 0 in I
    J=E | ((I&1>0)<<5); z=J.bit_count()
    share=[F((J>>t)&1,z) if z else F(0) for t in range(N)]
    M=[share[t]-B[t] for t in range(N)]
    L=[share[-1]-F((I>>j)&1,E.bit_count()+1) for j in range(S)]
    h=(E&15).bit_count(); d=(E>>4)&1; T=[]
    for j,k in PAIRS:
        v=((I>>j)&1)+((I>>k)&1)
        T.append(share[-2]+share[-1]-(F(v,h+v) if v else F(0))+F(d,(h+1)*(h+2)))
    return J,[*M,*L,*T]

def audit(kind,singletons):
    lam=lam_for(kind); count=0; minimum=None; arg=None
    for I in range(1,1<<S):
        if I.bit_count()<2 and I not in [1<<j for j in singletons]: continue
        for E in range(1<<5):
            J,coeff=rows(I,E)
            target=F(int(bool(J)),1)-(F(1,2) if I!=(1<<6) else F(0))
            residual=target-sum(a*b for a,b in zip(lam,coeff))
            if residual<0: raise AssertionError((kind,I,E,J,residual))
            if minimum is None or residual<minimum:minimum,arg=residual,(I,E,J)
            count+=1
    print(kind, {'columns':count,'minimum':str(minimum),'arg':arg})

if __name__=='__main__':
    audit('with_final',[0,1])
    audit('without_final',[1,2])
