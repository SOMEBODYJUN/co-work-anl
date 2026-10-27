"""Exact Farkas obstruction for the n=6, seven-maxima U<=2W row family.

Rows: six mixed-floor slacks M_t (t=0..5), seven final-response slacks L_j,
and 28 repeated-pair tax slacks T_{j,l}.  The script constructs all 4064
literal incidence/actual-membership columns, averages a sparse dual witness
under permutations of labels 1..6, and verifies every row coefficient exactly.
It proves only that this row family cannot yield a nonnegative customer
residual certificate for U<=2W; it is not a Q-CAG-HALF-6 counterexample.
"""
from fractions import Fraction as F
from collections import defaultdict

N = 6

def floors(n=N):
    A=[]; B=[]
    for t in range(n-1):
        A.append(F(n+t,(t+1)*(7*n-5*t)))
        B.append(F(2,7*n-5*t))
    A.append(F(1,n+6)); B.append(F(n+1,n*(n+6)))
    return [min(A[t:]) for t in range(n)], [min(B[t:]) for t in range(n)]

ALPHA,BETA=floors()

def columns():
    # I is maximal-theme incidence; E is actual membership in first five
    # positions. Actual last membership equals f=1_{0 in I}.
    for im in range(1,1<<7):
        I=tuple(j for j in range(7) if (im>>j)&1)
        f=int(0 in I); m=len(I)
        for em in range(1<<(N-1)):
            E=tuple(j for j in range(N-1) if (em>>j)&1)
            J=E+((N-1,) if f else ())
            p=sum(j<N-2 for j in J); d=int(N-2 in J); den=len(J)
            yield I,J,f,m,p,d,den

def rows(c):
    I,J,f,m,p,d,den=c; I=set(I); J=set(J)
    out=[]
    for t in range(N):
        share=F(1,den) if den and t in J else F(0)
        floor=F(1,N) if m==7 else ALPHA[t] if m==1 else BETA[t]
        out.append(share-floor)                         # M_t
    for j in range(7):
        # L_j = u_last - value of B_j as a last reply to the actual prefix
        out.append((F(f,den) if den else F(0)) - (F(1,p+d+1) if j in I else F(0)))
    for j in range(7):
        for l in range(j,7):
            num=int(j in I)+int(l in I); q=p+num
            cmp=F(num,q) if q else F(0)
            out.append((F(d+f,den) if den else F(0))
                       + F(d,(p+1)*(p+2)) - cmp)       # T_{j,l}
    assert len(out)==41
    return out

# Group columns by the S_6 action on labels 1,...,6.  The exact average of
# each row over a group is the coefficient used by the symmetrized dual.
cols=list(columns()); groups=defaultdict(list)
for idx,c in enumerate(cols):
    I,J,f,m,p,d,den=c
    E=tuple(j for j in J if j<N-1)
    groups[(f,m,E)].append(idx)

group_items=list(groups.items())
# Exact sparse dual masses (sum over each whole orbit/group).
# These are the unique rational solution to the active dual equalities.
support={
 (1,1,()): F(7017572,321392367),
 (1,1,(3,)): F(3133900,321392367),
 (0,1,()): F(111186481,214261578),
 (0,1,(4,)): F(2017043,71420526),
 (1,2,(2,3)): F(42350,3967807),
 (1,2,(1,2,3)): F(387200,35710263),
 (1,2,(0,1,2,3)): F(3573215,71420526),
 (1,2,(0,1,2,3,4)): F(8325175,23806842),
}
assert sum(support.values(),F(0))==1

# Average each row exactly over every literal column in the orbit.
row_dual=[F(0)]*41
for sig,idcs in group_items:
    mass=support.get(sig,F(0))
    if not mass: continue
    avg=[sum((rows(cols[i])[j] for i in idcs),F(0))/len(idcs) for j in range(41)]
    for j in range(41): row_dual[j] += mass*avg[j]

# Every row's averaged slack is nonnegative.  The M_5 and T_00 rows are
# strictly positive; the others are zero or positive.
assert min(row_dual) >= 0

# Base coefficient is h-1/2, with h=1 iff actual terminal union covers the
# customer. The exact averaged base is negative.
base=F(0)
for sig,idcs in group_items:
    mass=support.get(sig,F(0))
    if mass:
        h=1 if cols[idcs[0]][-1]>0 else 0
        base += mass*(F(h)-F(1,2))
assert base == F(-2027846,107130789)
print('columns',len(cols),'groups',len(groups))
print('dual_mass_sum',sum(support.values(),F(0)))
print('minimum_row_average',min(row_dual))
print('base_average',base,float(base))
print('row_averages',row_dual)
