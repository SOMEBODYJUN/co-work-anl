#!/usr/bin/env python3
"""Independent actual-literal audit of the repaired C2-prefix existential witness.

Only finite evidence; the parity completion argument supplies the general identity.
No restriction on algorithmic recoupling is inferred from source nonidentifiability.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform

SELF=Path(__file__).resolve()
T=F(2)
# Jobs zero based. Machine A=0, B=1, C=2. Unlisted endpoints unavailable.
P=[{0:F(0),1:F(0)} for _ in range(4)]+[
    {0:F(1),1:F(1)}, {0:F(0),1:F(0)}, {2:F(2)}]
E=tuple((j,i) for j,row in enumerate(P) for i in row)
def support(parity):
    ans=[]
    for z in product((0,1),repeat=5):
        if sum(z)%2==parity:
            sigma=tuple(0 if z[j] else 1 for j in range(4))+(z[4],0,2)
            ans.append((z,sigma))
    return ans
SUP={r:support(r) for r in (0,1)}
assert [len(SUP[r]) for r in (0,1)]==[16,16]
def val(sigma,S):
    return int(all(sigma[j]==i for j,i in S))
def mom(r,S):
    return sum((F(val(sig,S),16) for z,sig in SUP[r]),F(0))
def loads(sigma):
    return tuple(sum((P[j][i] for j,i in enumerate(sigma) if i==a),F(0)) for a in range(3))
def compatible(S):
    return len({j for j,i in S})==len(S)
ALL=[tuple(S) for d in range(5) for S in combinations(E,d)]
COMP=[S for S in ALL if compatible(S)]
for S in ALL:
    assert mom(0,S)==mom(1,S)
    if not compatible(S): assert mom(0,S)==0
for r in (0,1):
    for z,sig in SUP[r]:
        assert len(sig)==7 and all(i in P[j] for j,i in enumerate(sig))
        assert max(loads(sig))==T
# Forced job 7 -> C gives lower bound 2, all support schedules attain it.
# Independently enumerate every legal full schedule, not merely supports.
SIGMA=tuple(product(*(tuple(row) for row in P)))
opt=min(max(loads(sig)) for sig in SIGMA)
assert opt==T
Fprefix=tuple((j,0) for j in range(4))
prefix=[]
for r in (0,1):
    prob=mom(r,Fprefix)
    selected=[(z,sig) for z,sig in SUP[r] if val(sig,Fprefix)]
    assert prob==F(1,16) and len(selected)==1
    conditional=tuple(sum((loads(sig)[i] for z,sig in selected),F(0))/len(selected) for i in range(3))
    assert conditional==(F(1-r),F(r),F(2))
    fifth=mom(r,Fprefix+((4,1),))
    assert fifth==F(r,16)
    prefix.append({'parity':r,'probability':str(prob),'full_conditional_loads':[str(x) for x in conditional],
                   'fifth_B5_moment':str(fifth),'conditional_actual_schedule':list(selected[0][1])})
# Exact Gram matrices from full actual one-hot monomials.
B1=[S for S in COMP if len(S)<=1]
B2=[S for S in COMP if len(S)<=2]
def union(S,U): return tuple(set(S)|set(U))
M2=[[mom(0,union(S,U)) for U in B2] for S in B2]
for i,S in enumerate(B2):
    for j,U in enumerate(B2):
        assert M2[i][j]==sum((F(val(sig,S)*val(sig,U),16) for z,sig in SUP[0]),F(0))
        assert M2[i][j]==mom(1,union(S,U))
def exact_psd_rank(A):
    A=[list(row) for row in A]; n=len(A); rank=0
    for k in range(n):
        assert A[k][k]>=0
        if A[k][k]==0:
            assert all(A[k][j]==0 for j in range(k,n))
            continue
        rank+=1
        p=A[k][k]
        for i in range(k+1,n):
            for j in range(i,n):
                A[i][j]-=A[i][k]*A[k][j]/p
                A[j][i]=A[i][j]
    return rank
rank_M2=exact_psd_rank(M2)
localizers=[]
for machine in range(3):
    K=[]
    for S in B1:
        row=[]
        for U in B1:
            V=union(S,U)
            from_mom=T*mom(0,V)-sum((P[j][machine]*mom(0,union(V,((j,machine),))) for j in range(7) if machine in P[j]),F(0))
            gram=sum(((T-loads(sig)[machine])*F(val(sig,S)*val(sig,U),16) for z,sig in SUP[0]),F(0))
            assert from_mom==gram
            gram_odd=sum(((T-loads(sig)[machine])*F(val(sig,S)*val(sig,U),16) for z,sig in SUP[1]),F(0))
            assert gram_odd==gram
            row.append(gram)
        K.append(row)
    localizers.append({'machine':machine,'dimension':len(B1),'exact_psd_rank':exact_psd_rank(K)})
# All task conservations with all compatible multipliers degree <=3.
recurrences=0
for S in COMP:
    if len(S)>3: continue
    for j,row in enumerate(P):
        assert sum((mom(0,union(S,((j,i),))) for i in row),F(0))==mom(0,S)
        recurrences+=1
result={
    'status':'passed', 'python':platform.python_version(),
    'script_sha256':hashlib.sha256(SELF.read_bytes()).hexdigest(),
    'input':{'machines':['A','B','C'],'processing_times_by_job':[{str(i):str(p) for i,p in row.items()} for row in P],'T':str(T)},
    'actual_endpoint_literals':len(E),'all_actual_literal_subsets_degree_le4':len(ALL),
    'compatible_actual_literal_subsets_degree_le4':len(COMP),
    'incompatible_zero_subsets_degree_le4':len(ALL)-len(COMP),
    'compatible_subsets_by_degree':{str(d):sum(len(S)==d for S in COMP) for d in range(5)},
    'source_sizes':{str(r):len(SUP[r]) for r in SUP},
    'actual_legal_schedules_enumerated':len(SIGMA),'actual_OPT':str(opt),
    'all_sources_are_true_OPT_schedules':True,
    'all_degree_le4_actual_onehot_moments_equal':True,
    'M2':{'dimension':len(B2),'exact_psd_rank':rank_M2},
    'load_localizers':localizers,'onehot_conservation_checks':recurrences,
    'prefix_and_fifth_moments':prefix,
    'scope':'Same fourth-order data fail to identify the specified source conditional full B load. No algorithmic impossibility or restriction on choosing another coupling follows.'}
print(json.dumps(result,indent=2,ensure_ascii=False))
