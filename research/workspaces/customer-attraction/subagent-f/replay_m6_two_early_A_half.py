from fractions import Fraction as F
from itertools import product

M=6
L1=F(5,4); L2=F(5,4); MU=F(1)
mins=(F(999),None); count=0; bad=[]
for a in (0,1):
    for es in product((0,1), repeat=4):
        # last two early topics contain A whenever a=1
        if a and not (es[2]==es[3]==1):
            continue
        p=sum(es)
        for b in (0,1):
            den=p+a+b
            for d in range(M+1):
                for ell in range(M+1):
                    count += 1
                    alpha=F(a,den) if den else F(0)
                    beta=F(b,den) if den else F(0)
                    G=(M*alpha + beta/F(2) - F(d,p+1)
                       - F(ell,2*M*(p+a+1))
                       + F(d*ell,M*(p+1)*(p+2)))
                    H1=(F(es[0],den) if den else F(0))-F(a,M)
                    H2=(F(es[1],den) if den else F(0))-F(a,M)
                    L=(F(b,den) if den else F(0))-F(a,p+a+1)
                    Q=F(2*(den>0)-(d>0))-G-L1*H1-L2*H2-MU*L
                    if Q<mins[0]: mins=(Q,(a,es,p,b,d,ell,G,H1,H2,L))
                    if Q<0: bad.append((Q,(a,es,p,b,d,ell)))
assert not bad, bad[:5]
print({'states':count,'minimum_residual':str(mins[0]),'argmin':mins[1], 'negative_states':len(bad)})
