"""Exact Farkas witness for one specified local row cone.

This is a method obstruction, not a Q-CAG-HALF-6 counterexample.
Domain: m=6, actual penultimate A; exactly one fixed early theme E4 contains A
(a=1 implies e4=1), and every A customer has at least one further early cover
(p>=2 in total). Rows tested are the common G=(6S+V)t+qZ rows, all four
prefix-safe H_i, exception K_i=H_i^weak+L_Ei/5 for E1,E2,E3, L_A, and six
valid source-at-player-4 cuts querying A,B,E1,E2,E3,E4.
The rational y below certifies infeasibility of this entire row cone.
"""
from fractions import Fraction as F
from itertools import product

R = ["t", "z"] + [f"H{i}" for i in range(4)] + [f"K{i}" for i in range(3)] + ["LA"] + [f"SRC{i}" for i in range(6)]
Y = {
    (0,0,(0,0,0,0),1,0,0): F(5,361),
    (0,0,(0,0,0,0),1,1,0): F(180,361),
    (0,1,(0,0,0,0),1,0,0): F(6,361),
    (0,1,(0,0,1,0),1,0,0): F(44,361),
    (0,1,(0,1,1,0),1,0,0): F(6,361),
    (1,0,(0,1,0,1),1,0,0): F(60,361),
    (1,0,(1,0,0,1),1,0,0): F(60,361),
}

def rat(n,d):
    return F(n,d) if n else F(0)

def psi4(a,t,z,e1,e2,e3,e4):
    bg=e1+e2+e3; bp=e1+e2; ell=bg+e4
    vals=[]
    for p,q in product((0,1), repeat=2):
        den=bg+t+p+q
        vals.append(rat(t,den)+rat(4*q,7*(bp+4))+rat(9*q+7*p,35*(ell+1))
                    -rat(2*q,5*den)+rat(2*z,5*(bg+t+p+1)))
    return min(vals)

def row(state):
    a,b,es,d,ell,h=state
    e1,e2,e3,e4=es; p=sum(es); c=p+a+b
    S=6*rat(a,c)-F(d,p+1)+F(h,(p+1)*(p+2))
    Z=6*rat(b,c)-F(ell,p+a+1)
    V=F(d*ell-6*h,(p+1)*(p+2))
    coeff=[6*S+V, Z]
    # exact prefix-safe H_i
    coeff += [rat(es[i],c)-rat(a,sum(es[:i])+6-i) for i in range(4)]
    # three exception K_i: weak H_i plus final L_Ei / 5
    coeff += [(rat(es[i],c)-F(a,6)) + (rat(b,c)-rat(es[i],p+a+1))/5 for i in range(3)]
    coeff += [rat(b,c)-rat(a,p+a+1)] # L_A
    for z in (a,b,e1,e2,e3,e4):
        lhs=rat(e4,c)+rat(4*e3,7*c)+rat(16*b,35*c)
        rhs=F(d,6)*psi4(a,1,z,e1,e2,e3,e4)+F(6-d,6)*psi4(a,0,z,e1,e2,e3,e4)
        coeff.append(lhs-rhs)
    return coeff

assert sum(Y.values()) == 1
# Exact certificate: sum_y coefficient(row) is componentwise nonnegative,
# while sum_y rhs = -9/361.  Any nonnegative row multipliers would contradict this.
agg=[F(0)]*len(R)
for s,y in Y.items():
    c=row(s)
    for j,v in enumerate(c): agg[j] += y*v
print("support_mass",sum(Y.values()))
print("A^T y:")
for name,v in zip(R,agg): print(name,v)
print("b^T y",sum(y* (2*int(sum(s[2])+s[0]+s[1]>0)-int(s[3]>0)) for s,y in Y.items()))
assert all(v>=0 for v in agg)
assert sum(y* (2*int(sum(s[2])+s[0]+s[1]>0)-int(s[3]>0)) for s,y in Y.items()) == F(-9,361)
print("exact witness verified")
