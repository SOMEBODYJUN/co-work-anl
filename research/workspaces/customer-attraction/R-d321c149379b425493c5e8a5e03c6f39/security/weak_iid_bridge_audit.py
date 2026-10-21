"""Independent exact arithmetic for the full-history petal family. Stdlib only."""
from fractions import Fraction as F
from math import comb, factorial

m,J=20,100
S=({0,1},set(range(2,2*m)))+tuple({0,1,2*m+j} for j in range(J))
A,B=0,1
assert len(set(map(frozenset,S)))==J+2
assert len(set().union(*S))==2*m+J

def action(h):
    if not h:return A
    if len(h)<m-1:return B
    small=[a for a in h if a!=B]
    if not small:return 2
    if len(small)==1:
        if small[0]==A:return B
        return 3 if small[0]==2 else 2
    return B

def continuation(h):
    while len(h)<m:h=h+(action(h),)
    return h

def payoff(z,i):
    return sum((F(1,sum(x in S[a] for a in z)) for x in S[z[i]]),F(0))

def node(h,alternatives):
    d=len(h);base=payoff(continuation(h),d)
    for a in alternatives:assert payoff(continuation(h+(a,)),d)<=base
    return len(alternatives)

checks=node((),range(J+2));class_nodes=1
# s<=1: any order of B and the unique small action has identical continuation/payoffs.
for t in range(m):
    if t:checks+=node((B,)*t,(A,B,2));class_nodes+=1
    if t+1<m:
        checks+=node((B,)*t+(A,),(A,B,2));class_nodes+=1
        checks+=node((B,)*t+(2,),(A,B,2,3));class_nodes+=1
# s>=2: queried core sees only s and queried petal sees only its own q count.
# The remaining s-q small entries can be A without changing compared payoffs.
for s in range(2,m):
    for t in range(m-s):
        for q in range(s+1):
            h=(B,)*t+(2,)*q+(A,)*(s-q)
            checks+=node(h,(A,B,2));class_nodes+=1
z=continuation(())
assert z==(A,)+(B,)*(m-1)
assert all(payoff(z,i)==2 for i in range(m))
W=len(set().union(*(S[a] for a in z)))
assert W==2*m
OPT=2*m+min(J,m-1)
assert OPT==59

# Valid static opponent tuple, all 102 legal queries independently evaluated.
bg=(B,)*(m-2)+(2,)
cap=[payoff((a,)+bg,0) for a in range(J+2)]
assert cap==[F(1),F(2),F(3,2)]+[F(2)]*(J-1)

def g(n,t):return sum(((1-t)**i for i in range(n)),F(0))/n

def g_binomial(n,t):
    return sum((F(comb(n-1,k),k+1)*t**k*(1-t)**(n-1-k) for k in range(n)),F(0))
for t in (F(0),F(1),F(25,27),F(2,27),F(1,1350)):
    assert g(m,t)==g_binomial(m,t)

def UB(r):return 2*(m-1)*g(m,r)
def UQ(r):return 2*g(m,1-r)+g(m,(1-r)/J)
def gap(r):return UB(r)-UQ(r)
rbar=F(25,27)
assert 135*25**20<29*27**20
assert 2*g(m,F(2,27))>F(53,50)
assert g(m,F(1,1350))>=F(2681,2700)
assert F(53,50)+F(2681,2700)==F(5543,2700)
assert F(513,250)-F(5543,2700)==F(-13,13500)
assert gap(rbar)<F(-13,13500)
epsilon=F(2,27)**20
assert UB(rbar)==F(513,250)*(1-epsilon)
assert F(39,2)*UB(rbar)-40==(7-20007*epsilon)/500>0
assert gap(F(0))>0 and gap(F(1))<0
lo,hi=F(0),rbar
for _ in range(45):
    mid=(lo+hi)/2
    if gap(mid)>0:lo=mid
    else:hi=mid
Zlo,Zhi=m*UB(hi),m*UB(lo)
assert F(39,40)*Zlo>W

# Exact constants in the analytic all-m>=41 proof.
assert sum((F(3,2)**j/factorial(j) for j in range(6)),F(0))==F(5711,1280)>F(40,9)
assert F(31,30)+F(397,400)==F(2431,1200)
assert 2+F(2,79)<F(2431,1200)
for n in (41,42,100,1000):
    Am=F(2*(n-1),1)/F(2*n-3,2)
    threshold=F(2*n,1)/F(2*n-1,2)
    assert Am-threshold==1/(F(2*n-3,2)*F(2*n-1,2))>F(1,n*n)
    assert Am<3 and 3*F(81,16*n**4)<F(1,n*n)
print({'unit_customers':2*m+J,'topics':J+2,'m':m,'SPE_state_classes':class_nodes,
       'SPE_action_comparisons':checks,'W':W,'OPT':OPT,'security_upper':2,
       'iid_root_bracket':[float(lo),float(hi)],'iid_Z_bracket':[float(Zlo),float(Zhi)],
       'weak_iid_gap_lower':float(F(39,2)*UB(rbar)-W),
       'weak_iid_gap_bracket':[float(F(39,40)*Zlo-W),float(F(39,40)*Zhi-W)],
       'all_m_ge_41':'analytic proof; constants audited'})
