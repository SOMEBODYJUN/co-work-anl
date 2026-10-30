"""Independent exact reconstruction; never imports the canonical implementation.

Finite named parameter checks, not a proof of the universal statements.
"""
from fractions import Fraction as F
from itertools import product
import json

# Four-machine family independently reconstructed from the exact claim.
def family(c,d,q):
    s=(1-d)/2
    jobs=[(0,1,c/2,s),(0,1,c/2,s),(1,0,c/2,s),(1,0,c/2,s),
          (2,0,F(1),d),(2,3,c-1,q),(3,1,F(1),d),(3,2,c-1,q)]
    return jobs,s

def loads(jobs,mask,m=4):
    ans=[F(0)]*m
    for k,(u,v,a,b) in enumerate(jobs):
        ans[v if mask>>k&1 else u] += b if mask>>k&1 else a
    return ans

def greedy_terminals(jobs,U,kind,guard=False):
    S=loads(jobs,0)
    Q=[sum((b for u,v,a,b in jobs if v==i),F(0)) for i in range(4)]
    h=[max(F(0),S[i]+Q[i]-U) for i in range(4)]
    seen=set()
    terms=[]
    def rec(mask,path):
        if mask in seen:return
        seen.add(mask)
        L=loads(jobs,mask)
        D=[sum((a for k,(u,v,a,b) in enumerate(jobs) if u==i and mask>>k&1),F(0)) for i in range(4)]
        cand=[]
        for k,(u,v,a,b) in enumerate(jobs):
            if mask>>k&1:continue
            if guard and D[u]>=h[u]:continue
            if L[v]+b<=U:
                cand.append(k)
        if not cand:
            terms.append((mask,path,max(L)))
            return
        best=max(jobs[k][2] if kind=='source' else jobs[k][2]/jobs[k][3] for k in cand)
        for k in cand:
            score=jobs[k][2] if kind=='source' else jobs[k][2]/jobs[k][3]
            if score==best:rec(mask|1<<k,path+[k])
    rec(0,[])
    return terms

rows=[]
for c,d,q in product([F(8,5),F(7,4),F(19,10)],[F(1,100),F(1,5),F(8,25)],[F(51,100),F(3,4),F(1)]):
    jobs,s=family(c,d,q); U=c+F(1,2)
    assert loads(jobs,0)==[c]*4
    assert max(loads(jobs,255))==1
    assert 2/d>3 # loose source-independent test
    assert 1/d>c/(1-d)
    # Any schedule with makespan < 1 must move both bait jobs, and then core
    # total is at least 4*s+2*d=2, so OPT >= 1 analytically. Check all 2^8.
    opt=min(max(loads(jobs,mask)) for mask in range(256))
    assert opt==1
    for kind in ('source','ratio'):
        terms=greedy_terminals(jobs,U,kind)
        assert terms and all(mask==0b11110000 for mask,path,peak in terms)
        assert all(peak==c+d for mask,path,peak in terms)
        # Full safe direct-move graph confirms the terminal has no remaining step.
        L=loads(jobs,0b11110000)
        assert all(L[v]+b>U for k,(u,v,a,b) in enumerate(jobs) if k<4)
        guarded=greedy_terminals(jobs,U,kind,True)
        assert all(mask==0b01010000 for mask,path,peak in guarded)
    order=[0,2,1,3,4,6,5,7]
    mask=0; peak=c
    for k in order:
        mask|=1<<k
        peak=max(peak,max(loads(jobs,mask)))
    assert mask==255 and peak==c+s<U
    rows.append({'c':str(c),'d':str(d),'q':str(q),'opt':str(opt),'good_peak':str(peak)})

# Activation inequality and exact uniform coefficient interval boundaries.
for c in [F(1),F(5,4),F(3,2),F(7,4),F(2)]:
    U=max(F(2),c+F(1,2))
    for S,f,Q in product([F(k,8) for k in range(17)],repeat=3):
        if S>c or f>S or f+Q>1:continue
        A=S-f; h=max(F(0),S+Q-U)
        assert 0<=h<=A/3
        for lam in (F(1,3),F(2,5),F(1,2)):
            assert lam*A>=h
            assert lam*Q<=U-S
assert (F(3,2)+1-F(2))/F(3,2)==F(1,3)
assert (F(5,2)-2)/1==F(1,2)

# Simpler static cover/packing obstruction with a fixed fourth-machine job.
jobs=[(0,1,F(1),F(3,5)),(0,2,F(1),F(3,5)),
      (1,0,F(1),F(3,10)),(1,2,F(1),F(1,5)),
      (2,0,F(1),F(3,10)),(2,1,F(1),F(1,5))]
S=loads(jobs,0); U=F(5,2)
Q=[sum((b for u,v,a,b in jobs if v==i),F(0)) for i in range(4)]
h=[max(F(0),S[i]+Q[i]-U) for i in range(4)]
assert h[:3]==[F(1,10),F(3,10),F(3,10)]
feasible=[]
for mask in range(64):
    D=[sum((a for k,(u,v,a,b) in enumerate(jobs) if u==i and mask>>k&1),F(0)) for i in range(4)]
    incoming=[sum((b for k,(u,v,a,b) in enumerate(jobs) if v==i and mask>>k&1),F(0)) for i in range(4)]
    if all(D[i]>=h[i] and incoming[i]<=U-S[i] for i in range(4)):feasible.append(mask)
assert not feasible
mask=0; peak=F(2)
for k in [2,0,3,4,1,5]:
    mask|=1<<k
    peak=max(peak,max(loads(jobs,mask)))
assert peak==F(23,10)
negative_result={'four_machine_cases':len(rows),'all_checks':'passed','static_integer_R_count':len(feasible),'simple_path_peak':str(peak),'cases':rows}

def synthesize(jobs,m,T,C):
    S=[sum((a for u,v,a,b in jobs if u==i),F(0)) for i in range(m)]
    Q=[sum((b for u,v,a,b in jobs if v==i),F(0)) for i in range(m)]
    U=max(2*T,C+T/2)
    h=[max(F(0),S[i]+Q[i]-U) for i in range(m)]
    H={i for i in range(m) if h[i]>0}
    E={i:[k for k,(u,v,a,b) in enumerate(jobs) if u==i and a>=h[i]] for i in H}
    G={i for i in H if any(jobs[k][1] not in H or jobs[k][3]<=U-S[jobs[k][1]] for k in E[i])}
    dist={i:0 for i in G}
    while True:
        fresh={i:1+min(dist[jobs[k][1]] for k in E[i] if jobs[k][1] in dist) for i in H-dist.keys() if any(jobs[k][1] in dist for k in E[i])}
        if not fresh:break
        dist.update(fresh)
    if len(dist)<len(H):
        assert not all(len(E[i])>=2 for i in H)
        return None
    choice={}
    for i in H:
        if i in G: cand=[k for k in E[i] if jobs[k][1] not in H or jobs[k][3]<=U-S[jobs[k][1]]]
        else: cand=[k for k in E[i] if jobs[k][1] in dist and dist[jobs[k][1]]<dist[i]]
        choice[i]=min(cand)
    active=set(range(m))-H
    order=[]
    remaining=set(H)
    while remaining:
        fresh=sorted(i for i in remaining if jobs[choice[i]][1] in active)
        if fresh:
            for i in fresh:
                order.append(choice[i]);active.add(i);remaining.remove(i)
            continue
        # Every remaining component has a directed cycle. Trace one.
        seq=[];position={};i=min(remaining)
        while i not in position:
            position[i]=len(seq);seq.append(i);i=jobs[choice[i]][1]
        cyc=seq[position[i]:]
        anchors=[i for i in cyc if jobs[choice[i]][3]<=U-S[jobs[choice[i]][1]]]
        assert anchors
        root=min(anchors)
        pred={jobs[choice[i]][1]:i for i in cyc}
        j=root
        for _ in cyc:
            order.append(choice[j]);active.add(j);remaining.remove(j);j=pred[j]
    assert len(set(order))==len(order)
    order += [k for k in range(len(jobs)) if k not in set(order)]
    L=S[:];peak=max(L,default=F(0))
    for k in order:
        u,v,a,b=jobs[k]
        L[u]-=a;L[v]+=b
        assert min(L)>=0 and max(L)<=U
        peak=max(peak,max(L))
    assert L==Q
    return order,peak

# Validate the positive certificate on the previous exact families and the
# static no-integral-R example. No reliance on root's path algorithm.
cases=[]
for c,d,q in product([F(8,5),F(7,4),F(19,10)],[F(1,100),F(1,5),F(8,25)],[F(51,100),F(3,4),F(1)]):
    s=(1-d)/2
    jobs=[(0,1,c/2,s),(0,1,c/2,s),(1,0,c/2,s),(1,0,c/2,s),(2,0,F(1),d),(2,3,c-1,q),(3,1,F(1),d),(3,2,c-1,q)]
    assert synthesize(jobs,4,F(1),c)
    cases.append(1)
jobs=[(0,1,F(1),F(3,5)),(0,2,F(1),F(3,5)),(1,0,F(1),F(3,10)),(1,2,F(1),F(1,5)),(2,0,F(1),F(3,10)),(2,1,F(1),F(1,5))]
assert synthesize(jobs,3,F(1),F(2))

assert synthesize([(0,1,F(0),F(0))],2,F(0),F(0))
print(json.dumps({'negative_and_window':negative_result,'independent_selector':{'status':'passed','priority_families':len(cases),'static_case':True,'zero_case':True}},ensure_ascii=False,indent=2))
