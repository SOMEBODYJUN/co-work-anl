"""Exact diagnostic: the old seven-maxima n=6 Farkas witness survives every
legal aggregate order-statistic (ASR) row on route (0,0,0,0,1,0).

This is a mechanism obstruction only. It does not give a Q-CAG-HALF-6
counterexample. We use the 8-orbit dual support from R-4ba.../orderstat_obstruction;
for each prefix t and every H of r-1 seats we compute the exact orbit-average
of ASR(H), and minimize over H by sorting seat deltas. All minima are positive,
so adding any nonnegative ASR rows leaves the witness's negative base average.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import defaultdict

N,S=6,7
route=(0,0,0,0,1,0)
# Source mixed-floor suffix values, as in the old obstruction.
A=[]; B=[]
for t in range(N-1):
    A.append(F(N+t,(t+1)*(7*N-5*t))); B.append(F(2,7*N-5*t))
A.append(F(1,N+6)); B.append(F(N+1,N*(N+6)))
ALPHA=[min(A[t:]) for t in range(N)]
BETA=[min(B[t:]) for t in range(N)]
PAIRS=list(combinations(range(S),2))
# Orbit masses copied from the exact old Farkas witness.
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
assert sum(support.values(),F())==1
# Prefix routed counts p_j (the ASR q seats depend on these counts).
prefix=[]; p=[0]*S
for t in range(N): prefix.append(p.copy()); p[route[t]]+=1
# Enumerate all literal columns and group by old-witness orbit key. The target six-maxima optimum is K={1,2,3,4,5,6}, i.e. it omits the actual final maximum B_0.
cols=[]; groups=defaultdict(list)
for im in range(1,1<<S):
    I={j for j in range(S) if im>>j&1}; f=int(0 in I); m=len(I)
    for em in range(1<<(N-1)):
        E=tuple(j for j in range(N-1) if em>>j&1)
        J=set(E)|({N-1} if f else set())
        idx=len(cols); cols.append((I,J,f,m))
        groups[(f,m,E)].append(idx)
assert len(cols)==4064
# For each t, compute orbit-weighted E[q_seat] and E[U_seat].
mins=[]
for t in range(N):
    r=N-t; L=S*r-r+1
    seats=[(j,k) for j in range(S) for k in range(1,r+1)]
    eq={h:F() for h in seats}; eu={h:F() for h in seats}; es=F()
    for sig,idcs in groups.items():
        mass=support.get(sig,F())
        if not mass: continue
        n=len(idcs); avg_share=F()
        qsum={h:F() for h in seats}; usum={h:F() for h in seats}
        for idx in idcs:
            I,J,f,m=cols[idx]; den=len(J); pI=sum(prefix[t][j] for j in I)
            if t in J: avg_share += F(1,den)
            for j,k in seats:
                q=(F(1,prefix[t][j]+k) if m==1 and j in I
                   else F(1,pI+r) if m>=2 and j in I else F())
                u=F(1,prefix[t][j]+k) if j in I else F()
                qsum[(j,k)]+=q; usum[(j,k)]+=u
        es += mass*avg_share/n
        for h in seats:
            eq[h]+=mass*qsum[h]/n; eu[h]+=mass*usum[h]/n
    # ASR(H) avg = es - sum(eq)/L + sum_{h in H}(eu-eq)/L.
    base=es-sum(eq.values(),F())/L
    delta={h:(eu[h]-eq[h])/L for h in seats}
    H=sorted(seats,key=lambda h:delta[h])[:r-1]
    val=base+sum((delta[h] for h in H),F())
    mins.append(val)
    print(f"t={t} r={r} min={val} ~= {float(val):.12g} H={H}")
# Exact values are intentionally asserted for reproducibility.
expected=[F(10564271,1468088590),F(677380141,99631633770),
          F(3454574,599612625),F(495326117,122129099460),
          F(74904707,83562015420),F(19909061,3749577615)]
assert mins==expected
print('all ASR(H) orbit averages are >= the displayed positive minima')
# For target O_K with K={1,...,6}, the same orbit witness has this exact base.
K=set(range(1,7)); baseK=F()
for sig,idcs in groups.items():
    mass=support.get(sig,F())
    if not mass: continue
    av=F()
    for idx in idcs:
        I,J,*_=cols[idx]
        av += F(int(bool(J)))-F(int(bool(set(I)&K)),2)
    baseK += mass*av/len(idcs)
assert baseK==F(-12442,3967807)
print('target K={1,...,6} base average =',baseK)
print('union U base average = -2027846/107130789 (for comparison)')
