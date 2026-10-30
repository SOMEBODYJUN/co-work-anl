#!/usr/bin/env python3
"""一般群组奇环实际阈值：作者逐资源有理审计。
No repository imports; inline inputs and deterministic seed below.
"""
from fractions import Fraction as Q
from itertools import product
from random import Random
import json, hashlib, platform
from pathlib import Path
RNG=Random(520261015)
COUNTS={k:0 for k in ['instances','count_states','literal_player_deviations','light_intervals','single_defects','LR_comparisons','center_states','full_equilibria','forward_reductions','reverse_reductions','nonexistence_instances']}
def poly(coeff,x): return sum((a*x**j for j,a in enumerate(coeff)),Q(0))
def literal(n,u,v,F,G,h,k):
    m=len(n); players=[('H',i,0,u[i]) for i in range(m)]+[('L',i,j,v[i]) for i in range(m) for j in range(n[i])]
    bits=[h[i] for i in range(m)]+[h[i] if j<k[i] else 1-h[i] for i in range(m) for j in range(n[i])]
    def strategy(p,b):
        typ,i,j,w=p
        return [('A',i,0,b)]+[('B',(i-1)%m,jj,b) for jj in range(n[(i-1)%m])] if typ=='H' else [('A',i,0,b),('B',i,j,1-b)]
    S=[strategy(p,b) for p,b in zip(players,bits)]
    loads={}
    for p,ss in zip(players,S):
        for e in ss: loads[e]=loads.get(e,Q(0))+p[3]
    def fee(e,x): return poly(F[e[1]] if e[0]=='A' else G[e[1]],x)
    result=[]
    for p,b,ss in zip(players,bits,S):
        new=strategy(p,1-b); oldcost=sum((fee(e,loads[e]) for e in ss),Q(0)); newcost=Q(0)
        for e in new: newcost+=fee(e,loads.get(e,Q(0))+(Q(0) if e in ss else p[3]))
        result.append((oldcost,newcost)); COUNTS['literal_player_deviations']+=1
    return result

def run(n,u,v,F,G,alpha):
    m=len(n); COUNTS['instances']+=1
    ints=[]; c=[]
    def local(i,z,k):
        nn=n[i]; uu=u[i]; vv=v[i]; q=poly(G[i],vv); V=poly(G[i],vv+u[(i+1)%m]); D=V-q
        aligned=poly(F[i],uu+k*vv)+q+z*D
        adevi=poly(F[i],(nn-k+1)*vv)+q+(1-z)*D
        anti=poly(F[i],(nn-k)*vv)+q+(1-z)*D
        bdevi=poly(F[i],uu+(k+1)*vv)+q+z*D
        return (aligned,adevi),(anti,bdevi)
    for i in range(m):
        iz=[]
        for z in (0,1):
            good=[k for k in range(n[i]+1) if (k==0 or local(i,z,k)[0][0]<=alpha*local(i,z,k)[0][1]) and (k==n[i] or local(i,z,k)[1][0]<=alpha*local(i,z,k)[1][1])]
            assert good and good==list(range(min(good),max(good)+1)); iz.append(good); COUNTS['light_intervals']+=1
        ints.append(iz); c.append(min(iz[1])); assert c[-1]<=n[i]//2 and c[-1]<=min(iz[0])
        if min(iz[0])>n[i]/2: assert c[-1]<=n[i]-min(iz[0])
    def state(z,k):
        assert sum(z)%2==0
        h=[0]
        for j in range(m-1): h.append(h[-1]^z[j])
        assert (h[-1]^h[0])==z[-1]
        costs=literal(n,u,v,F,G,h,k)
        for i in range(m):
            pp=(i-1)%m; r=z[pp]*k[pp]+(1-z[pp])*(n[pp]-k[pp]); W=poly(G[pp],u[i]); V=poly(G[pp],u[i]+v[pp])
            expected=(poly(F[i],u[i]+k[i]*v[i])+r*V+(n[pp]-r)*W,poly(F[i],u[i]+(n[i]-k[i])*v[i])+(n[pp]-r)*V+r*W)
            assert costs[i]==expected
        p=m
        for i in range(m):
            loc=local(i,z[i],k[i])
            for j in range(n[i]): assert costs[p]==loc[0 if j<k[i] else 1]; p+=1
        return costs
    equilibria=0
    for z in product((0,1),repeat=m):
        if sum(z)%2: continue
        for k in product(*(range(nn+1) for nn in n)):
            costs=state(z,k); COUNTS['count_states']+=1
            if all(a<=alpha*b for a,b in costs): equilibria+=1
    if alpha>=max(2,len(F[0])-1): assert equilibria # safe all-class d bound, not the proof target
    if alpha>=2:
        # d<=5 has T_d<=2 from elementary f_d envelope, checked independently below.
        if max(map(len,F+G))-1<=5: assert equilibria
    if alpha>=Q(6,5) and max(map(len,F+G))-1<=2: assert equilibria
    COUNTS['full_equilibria']+=equilibria
    labels=[]; endpoints=[]
    for i in range(m):
        a,b=min(ints[i][0]),max(ints[i][0]); nn=n[i]
        if nn%2==0 and nn//2 in ints[i][0]:
            if alpha>=1:
                z=[1]*m;z[i]=0;k=c.copy();k[i]=nn//2
                assert all(x<=alpha*y for x,y in state(z,k)); COUNTS['center_states']+=1
            labels.append([]);endpoints.append({});continue
        labs={}
        if b<nn/2: labs['L']=b
        if a>nn/2: labs['R']=a
        if nn%2==1 and nn//2 in ints[i][0] and nn//2+1 in ints[i][0]: labs={'L':nn//2,'R':nn//2+1}
        labels.append(list(labs));endpoints.append(labs)
        for typ,count in labs.items():
            z=[1]*m;z[i]=0;k=c.copy();k[i]=count;cost=state(z,k)
            possible=(i+1)%m if typ=='L' else i
            assert all(x<=alpha*y for j,(x,y) in enumerate(cost) if j!=possible);COUNTS['single_defects']+=1
    for i in range(m):
        j=(i+1)%m
        if 'L' not in endpoints[i] or 'R' not in endpoints[j]:continue
        z=[1]*m;z[i]=0;k=c.copy();k[i]=endpoints[i]['L'];S=state(z,k)
        z=[1]*m;z[j]=0;k=c.copy();k[j]=endpoints[j]['R'];T=state(z,k)
        assert T[j][0]<=S[j][1] and S[j][0]<=T[j][1]
        assert not(S[j][0]>alpha*S[j][1] and T[j][0]>alpha*T[j][1]);COUNTS['LR_comparisons']+=1
    if equilibria==0:
        COUNTS['nonexistence_instances']+=1
        assert all(len(labs)==1 for labs in labels)
        assert len({labs[0] for labs in labels})==1
        if labels[0][0]=='L':
            b=[max(iz[0]) for iz in ints];nn=[n[i]-2*b[i] for i in range(m)]
            for i in range(m):
                pp=(i-1)%m;U=u[(i+1)%m]
                assert poly(F[i],u[i]+(b[i]+1)*v[i])+poly(G[i],v[i])>alpha*(poly(F[i],(n[i]-b[i])*v[i])+poly(G[i],v[i]+U))
                assert poly(F[i],u[i]+b[i]*v[i])+nn[pp]*poly(G[pp],u[i]+v[pp])>alpha*(poly(F[i],u[i]+(n[i]-b[i])*v[i])+nn[pp]*poly(G[pp],u[i]))
            COUNTS['forward_reductions']+=1
        else:
            a=[min(iz[0]) for iz in ints];r=[n[i]-a[i] for i in range(m)];nn=[n[i]-2*r[i] for i in range(m)]
            NF=[poly(F[i],u[i]+a[i]*v[i])-alpha*poly(F[i],u[i]+r[i]*v[i]) for i in range(m)]
            MF=[alpha*poly(F[i],u[i]+a[i]*v[i])-poly(F[i],(r[i]+1)*v[i]) for i in range(m)]
            NG=[poly(G[i],v[i]+u[(i+1)%m])-alpha*poly(G[i],v[i]) for i in range(m)]
            MG=[alpha*poly(G[i],v[i]+u[(i+1)%m])-poly(G[i],u[(i+1)%m]) for i in range(m)]
            assert all(NG[i]>MF[i]>0 and NF[i]>nn[i-1]*MG[i-1]>0 for i in range(m))
            gain=Q(1)
            for i in range(m):gain*=NF[i]*NG[i]/(nn[i]*MF[i]*MG[i])
            assert gain>1;COUNTS['reverse_reductions']+=1

# Explicit boundary families: all zero, constant, n=1 flexible, n=3 center,
# and mixed zero/nonzero shapes and extreme rational weights.
for nn in ((1,1,1),(2,2,2),(3,3,3),(1,2,3)):
    for degree in (2,3,5):
        for kind in range(4):
            n=list(nn);u=[Q(1,8),Q(1),Q(8)];v=[Q(2),Q(1,4),Q(3)]
            if kind==0:F=G=[[Q(0)]*(degree+1) for _ in n]
            elif kind==1:F=[[Q(1)]+[Q(0)]*degree for _ in n];G=[[Q(2)]+[Q(0)]*degree for _ in n]
            elif kind==2:F=[[Q(0)]*degree+[Q(1)] for _ in n];G=[[Q(0)]*(degree+1) for _ in n]
            else:F=[[Q(0)]*(degree+1) for _ in n];G=[[Q(0)]*degree+[Q(1)] for _ in n]
            run(n,u,v,F,G,Q(2))
for case in range(72):
    n=[RNG.randint(1,3) for _ in range(3)];degree=RNG.choice([2,3,5]);u=[RNG.choice([Q(1,8),Q(1,2),Q(1),Q(3),Q(8)]) for _ in n];v=[RNG.choice([Q(1,8),Q(1,2),Q(1),Q(3),Q(8)]) for _ in n]
    F=[[Q(RNG.randrange(4)) if RNG.randrange(3)==0 else Q(0) for _ in range(degree+1)] for _ in n]
    G=[[Q(RNG.randrange(4)) if RNG.randrange(3)==0 else Q(0) for _ in range(degree+1)] for _ in n]
    run(n,u,v,F,G,RNG.choice([Q(2),Q(3),Q(6,5)]))
# Known small nonexistence family, constructed independently from strict local intervals.
d=10;alpha=Q(11,10);u=[Q(32),Q(2),Q(8)];v=[Q(1),Q(4),Q(16)];n=[3,1,1];powers=[2,10,10]
N=[];M=[];P=[];QQ=[]
for i in range(3):
    x=v[i]/u[i];t=v[i]/u[(i+1)%3]
    N.append((1+x)**powers[i]-alpha*(n[i]*x)**powers[i]);M.append(alpha*(1+n[i]*x)**powers[i]-1)
    P.append(alpha*(1+t)**d-t**d);QQ.append((1+t)**d-alpha)
rates=[n[i-1]*QQ[i-1]*N[i]/(M[i]*P[i]) for i in range(3)];gain=rates[0]*rates[1]*rates[2];assert gain>1
delta=(gain-1)/(6*gain);B=[Q(1)]
for i in range(1,3):B.append((1-delta)*rates[i]*B[i-1])
AA=[(B[i]*P[i]/N[i]+n[i-1]*B[i-1]*QQ[i-1]/M[i])/2 for i in range(3)]
F=[[Q(0)]*powers[i]+[AA[i]/u[i]**powers[i]] for i in range(3)]
G=[[Q(0)]*d+[B[i]/u[(i+1)%3]**d] for i in range(3)]
run(n,u,v,F,G,alpha)
# Singleton positive certificate and exact role-reversed copy exercise both directions.
d=10;alpha=Q(21,20);u=[Q(4),Q(4),Q(8)];v=[Q(1),Q(1),Q(16)];n=[1,1,1];powers=[5,3,9]
N=[];M=[];P=[];QQ=[]
for i in range(3):
    x=v[i]/u[i];t=v[i]/u[(i+1)%3]
    N.append((1+x)**powers[i]-alpha*x**powers[i]);M.append(alpha*(1+x)**powers[i]-1)
    P.append(alpha*(1+t)**d-t**d);QQ.append((1+t)**d-alpha)
rates=[QQ[i-1]*N[i]/(M[i]*P[i]) for i in range(3)];gain=rates[0]*rates[1]*rates[2];assert gain>1
delta=(gain-1)/(6*gain);B=[Q(1)]
for i in range(1,3):B.append((1-delta)*rates[i]*B[i-1])
AA=[(B[i]*P[i]/N[i]+B[i-1]*QQ[i-1]/M[i])/2 for i in range(3)]
F=[[Q(0)]*powers[i]+[AA[i]/u[i]**powers[i]] for i in range(3)]
G=[[Q(0)]*d+[B[i]/u[(i+1)%3]**d] for i in range(3)]
run(n,u,v,F,G,alpha)
inds=[(-j)%3 for j in range(3)]
run(n,[v[i] for i in inds],[u[i] for i in inds],[F[i] for i in inds],[G[(i-1)%3] for i in inds],alpha)
# Exercise alpha below 2 in all zero, constant, and random quadratic inputs,
# for which T_2<=6/5 follows from the exact shifted polynomial below.
for case in range(24):
    n=[RNG.randint(1,3) for _ in range(3)];u=[RNG.choice([Q(1,4),Q(1),Q(4)]) for _ in n];v=[RNG.choice([Q(1,4),Q(1),Q(4)]) for _ in n]
    F=[[Q(RNG.randrange(3)) for _ in range(3)] for _ in n];G=[[Q(RNG.randrange(3)) for _ in range(3)] for _ in n]
    run(n,u,v,F,G,Q(6,5))
# Pure rational algebra check of T_d<=2 for d=2..5: 2den-num positive
# coefficient verification in shifted R=1+x is exact and stronger than sampling.
from math import comb
for degree in range(2,6):
    # 2(1+R)^d+2R^(d+1)-R(1+R)^d-1
    coeff=[Q(0)]*(degree+2)
    for j in range(degree+1): coeff[j]+=2*comb(degree,j); coeff[j+1]-=comb(degree,j)
    coeff[degree+1]+=2;coeff[0]-=1
    shifted=[sum(coeff[j]*comb(j,k) for j in range(k,degree+2)) for k in range(degree+2)]
    assert all(x>=0 for x in shifted) and shifted[0]>0
# 6 den - 5 num for d2 is R^3-4R^2+7R+1. At R=1+x it is x^3-x^2+2x+5 = x(x-1/2)^2+7x/4+5>0.
assert all(poly([Q(1),Q(7),Q(-4),Q(1)],Q(1)+Q(j,16))>0 for j in range(100)) # implementation check of identity, proof above exact
summary={'command':'python3 tests/audits/weighted_congestion/odd_ring_parameters/check_general_cohort_actual_upper.py','seed':520261015,'python':platform.python_version(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'counts':COUNTS,'arithmetic':'fractions.Fraction exact','scope':'Finite literal-resource audits only; proof remains separate. v2 uses odd central pairs as flexible labels.'}
print(json.dumps(summary,indent=2,ensure_ascii=False))
