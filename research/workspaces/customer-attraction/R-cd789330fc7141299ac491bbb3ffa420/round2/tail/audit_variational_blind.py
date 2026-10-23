#!/usr/bin/env python3
"""Independent exact KKT/credit audit, prepared before reading author code.

Every optimizer supplied below is certified by exact box KKT conditions, not a
numerical optimization run. Logarithms use rational artanh bounds. Irrational
greedy endpoints are bounded with Fraction intervals.
"""
from fractions import Fraction as F
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def log_bounds(q,N=100):
    assert q>=1
    if q==1:return F(),F()
    z=(q-1)/(q+1)
    s=2*sum((z**(2*k+1)/F(2*k+1) for k in range(N)),F())
    tail=2*z**(2*N+1)/((2*N+1)*(1-z*z))
    return s,s+tail

def audit_case(name,b,A,S,t,w):
    n=len(S);N=len(b);w=tuple(map(F,w));t=F(t)
    c1=[sum(x in s for s in S) for x in range(N)]
    c=[sum((w[j] for j,s in enumerate(S) if x in s),F()) for x in range(N)]
    L1=[F(b[x]+int(x in A)+c1[x]) for x in range(N)]
    L=[F(b[x]+int(x in A))+c[x] for x in range(N)]
    K=[x for x in range(N) if L1[x]>0]
    assert all(L[x]>0 for x in K)
    u=[sum((1/L1[x] for x in s),F()) for s in S]
    U=[sum((1/L[x] for x in s),F()) for s in S]
    for j in range(n):
        assert 0<=w[j]<=1
        if w[j]==0:assert U[j]<=t
        elif w[j]==1:assert U[j]>=t
        else:assert U[j]==t
        if u[j]>=t:assert w[j]==1
    D=sum((max(F(),t-v) for v in u),F())
    H=sum((1/(F(b[x]+1)+c[x])-1/F(b[x]+1+c1[x]) for x in range(N)),F())
    gain=sum((U[j]-u[j] for j in range(n) if w[j]<1),F())
    assert 0<=H<=gain<=D
    R=sum((1/L[x] for x in A),F());R1=sum((1/L1[x] for x in A),F())
    B=sum((F(b[x])/L[x] for x in K),F());B1=sum((F(b[x])/L1[x] for x in K),F())
    V=sum((c[x]/L[x] for x in K),F());V1=sum((F(c1[x])/L1[x] for x in K),F())
    G=(R-R1)+(B-B1);M=sum(w,F())
    assert V1-V==G and V>=t*M
    seat=sum(((1-w[j])*U[j] for j in range(n)),F())
    ratios=sum((L1[x]/L[x]-1 for x in K),F())
    assert seat==ratios<=t*(n-M)
    assert all(L[x]>=L1[x]/(1+t*(n-M)) for x in K)
    logs=[log_bounds(L1[x]/L[x]) for x in K]
    lo=sum((v[0] for v in logs),F());hi=sum((v[1] for v in logs),F())
    Flo=t*(n-M)-hi;Fhi=t*(n-M)-lo
    assert 0<=Flo<=Fhi<=D
    assert max(H,G)<=lo
    assert max(H,G)+Fhi+t*M<=t*n
    return {"name":name,"weights":[str(x) for x in w],"M":str(M),"D":str(D),
            "H":str(H),"G":str(G),"credit_sum":str(gain),
            "energy_interval":[str(Flo),str(Fhi)],"t":str(t),
            "load_signature":[str(x) for x in c]},(H,G,M,c,Flo,Fhi,D)

specs=[
 ("empty_universe",[],set(),[set(),set()],F(1),(0,0)),
 ("no_tail",[0],{0},[],F(1),()),
 ("private_positive_stop",[0],set(),[{0}],F(2),(F(1,2),)),
 ("private_initial_high",[0],set(),[{0}],F(1,2),(1,)),
 ("root_shared_zero_equal",[0],{0},[{0}],F(1),(0,)),
 ("root_shared_positive",[0],{0},[{0}],F(2,3),(F(1,2),)),
 ("background_zero_equal",[3],set(),[{0}],F(1,3),(0,)),
 ("large_background",[100],set(),[{0}],F(1,100),(0,)),
 ("duplicate_decomposition_1",[0],{0},[{0},{0}],F(1,2),(F(1,2),F(1,2))),
 ("duplicate_decomposition_2",[0],{0},[{0},{0}],F(1,2),(1,0)),
 ("initial_equal_must_stay",[0],set(),[{0}],F(1),(1,)),
 ("empty_plus_shared",[0],{0},[set(),{0}],F(2,3),(0,F(1,2))),
 ("greedy_reentry_canonical",[0,3,2],{0},[{0,2},{0,1}],F(16,15),(F(1,2),0)),
 ("high_full_low_fraction",[0]*4,set(),[{0,1,2},{3}],F(2),(1,F(1,2))),
]
rows=[];metrics=[]
for spec in specs:
    row,metric=audit_case(*spec);rows.append(row);metrics.append(metric)
assert metrics[8][:4]==metrics[9][:4]  # same canonical load and mass, different weights
assert [F(rows[i]["M"]) for i in (10,2)]==[F(1),F(1,2)]
assert metrics[4][0]+metrics[4][4]>metrics[4][6] # H+energy cannot both be charged to D

# Greedy order deletes the wrong player: canonical optimum is exact rational.
t=F(16,15);lo=F();hi=F(1)
for _ in range(90):
    mid=(lo+hi)/2
    if 1/(1+mid)+1/(3+mid)>t:lo=mid
    else:hi=mid
assert 1/(1+lo)+1/(3+lo)>=t>=1/(1+hi)+1/(3+hi)
assert 1/(1+hi)+F(1,2)>t

def solve(A,b):
    rows=[list(map(F,r))+[F(v)] for r,v in zip(A,b)]
    n=len(rows)
    for k in range(n):
        j=next(j for j in range(k,n) if rows[j][k])
        rows[k],rows[j]=rows[j],rows[k]
        d=rows[k][k];rows[k]=[v/d for v in rows[k]]
        for j in range(n):
            if j!=k:
                d=rows[j][k];rows[j]=[v-d*u for v,u in zip(rows[j],rows[k])]
    return [rows[i][-1] for i in range(n)]

# Independently reconstruct the supplied nonmonotone root-credit example.
Y=tuple(range(3,208));b=[F(1),F(1),F(99)]+[F(401)]*205
A={2};S=({0,1,2},set(Y)|{1},set(Y)|{0});w=(F(1,2),)*3
L=[b[x]+int(x in A)+sum((w[j] for j in range(3) if x in S[j]),F()) for x in range(208)]
U=[sum((1/L[x] for x in s),F()) for s in S]
assert U==[F(203,201)]*3
M=[[sum((1/(L[x]*L[x]) for x in S[i]&S[j]),F()) for j in range(3)] for i in range(3)]
wp=solve(M,[-1]*3)
gradient=[-sum((1/(L[x]*L[x]) for x in A&S[j]),F()) for j in range(3)]
derivative=sum((v*u for v,u in zip(gradient,wp)),F())
assert derivative==F(-159964,8445449)<0

out={"scope":"independent exact KKT certificates and rational logarithm brackets; general proof in blind reconstruction",
     "KKT_cases":rows,"greedy_zero_reentry_interval":[str(lo),str(hi)],
     "duplicate_weights_have_same_load_and_mass":True,
     "H_plus_free_energy_can_exceed_D":True,
     "root_credit_nonmonotonicity":{"customers":208,"t":"203/201","weights":["1/2"]*3,
                                     "weight_derivative":[str(x) for x in wp],
                                     "root_credit_derivative":str(derivative)},
     "not_claimed":"fractional SPE or monotonicity of each weight/load/root refund"}
(HERE/"variational_blind_exact.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"KKT_cases":len(rows),"all_exact_checks":True,
                  "root_credit_derivative":str(derivative)},indent=2))
