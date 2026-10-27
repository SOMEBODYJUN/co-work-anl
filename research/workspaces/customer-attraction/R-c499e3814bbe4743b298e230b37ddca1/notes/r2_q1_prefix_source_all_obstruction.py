"""Exact Farkas witness for the enriched q=1,p>=2 local row cone.

Method obstruction only. In addition to the rows in
r2_q1_prefix_source_obstruction.py, this version adds the reviewed source-at-3
and source-at-2 cuts (querying A). The witness below still separates the cone.
"""
from fractions import Fraction as F
from itertools import product

R = ["t", "z"] + [f"H{i}" for i in range(4)] + [f"K{i}" for i in range(3)] + ["LA"] + [f"SRC4_{i}" for i in range(6)] + ["SRC3_A", "SRC2_A"]
Y = {
    (0,0,(0,0,0,0),1,0,0): F(155,361),
    (0,0,(0,0,0,0),1,6,1): F(30,361),
    (0,1,(0,0,0,0),1,0,0): F(6,361),
    (0,1,(0,0,1,0),1,0,0): F(44,361),
    (0,1,(0,1,1,0),1,0,0): F(6,361),
    (1,0,(0,1,0,1),1,0,0): F(60,361),
    (1,0,(1,0,0,1),1,0,0): F(60,361),
}

def rat(n,d):
    return F(n,d) if n else F(0)

def psi4(a,t,z,e1,e2,e3,e4):
    bg=e1+e2+e3; bp=e1+e2; ell=bg+e4; vals=[]
    for p,q in product((0,1), repeat=2):
        den=bg+t+p+q
        vals.append(rat(t,den)+rat(4*q,7*(bp+4))+rat(9*q+7*p,35*(ell+1))
                    -rat(2*q,5*den)+rat(2*z,5*(bg+t+p+1)))
    return min(vals)

def psi3(a,t,x,e1,e2):
    bg=e1+e2; vals=[]
    for s,q in product((0,1), repeat=2):
        den=bg+t+s+q
        vals.append(rat(t,den)+rat(s,18)+rat(q,9)-rat(q,9*den)
                    +rat(x,9*(bg+t+s+1)))
    return min(vals)

def psi2(a,t,x,e1,p):
    bg=e1; ell=p+a; cp=F(1,64)+F(1,32*(ell+1)); vals=[]
    for s in range(4):
        for q in (0,1):
            den=bg+t+s+q
            vals.append(rat(t,den)+s*cp+rat(q,16)-rat(q,16*den)
                        +rat(x,16*(bg+t+s+1)))
    return min(vals)

def row(state):
    a,b,es,d,ell,h=state
    e1,e2,e3,e4=es; p=sum(es); c=p+a+b
    S=6*rat(a,c)-F(d,p+1)+F(h,(p+1)*(p+2))
    Z=6*rat(b,c)-F(ell,p+a+1)
    V=F(d*ell-6*h,(p+1)*(p+2))
    coeff=[6*S+V, Z]
    coeff += [rat(es[i],c)-rat(a,sum(es[:i])+6-i) for i in range(4)]
    coeff += [(rat(es[i],c)-F(a,6))+(rat(b,c)-rat(es[i],p+a+1))/5 for i in range(3)]
    coeff += [rat(b,c)-rat(a,p+a+1)]
    lhs4=rat(e4,c)+rat(4*e3,7*c)+rat(16*b,35*c)
    for z in (a,b,e1,e2,e3,e4):
        coeff.append(lhs4-(F(d,6)*psi4(a,1,z,e1,e2,e3,e4)
                           +F(6-d,6)*psi4(a,0,z,e1,e2,e3,e4)))
    lhs3=rat(e3,c)+F(2,9)
    coeff.append(lhs3-(F(d,6)*psi3(a,1,a,e1,e2)
                       +F(6-d,6)*psi3(a,0,a,e1,e2)))
    lhs2=rat(e2,c)+rat(3*b,32*c)+F(7,64)
    coeff.append(lhs2-(F(d,6)*psi2(a,1,a,e1,p)
                       +F(6-d,6)*psi2(a,0,a,e1,p)))
    return coeff

assert sum(Y.values()) == 1
agg=[F(0)]*len(R)
for s,y in Y.items():
    for j,v in enumerate(row(s)): agg[j] += y*v
rhs=sum(y*(2*int(sum(s[2])+s[0]+s[1]>0)-int(s[3]>0)) for s,y in Y.items())
print("support_mass",sum(Y.values()))
for name,v in zip(R,agg): print(name,v)
print("b^T y",rhs)
assert all(v>=0 for v in agg)
assert rhs == F(-9,361)
print("exact witness verified")
