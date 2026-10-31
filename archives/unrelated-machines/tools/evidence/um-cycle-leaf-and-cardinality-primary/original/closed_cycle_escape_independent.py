from fractions import Fraction as F
from heapq import heappush,heappop
from itertools import product
import json

# Independent endpoint reconstruction; no imports from other audit programs.
def run(k,d):
    scale=4*k*k; a=4*k*(k-1); delta=4*(k-1); c=4
    p=[]; names=[]; chain_tails=[]; next_machine=1
    for g in range(k+1):
        h=d if g<k else d+k-1
        home=list(range(next_machine,next_machine+h));next_machine+=h
        gr=len(p);p.append(((0,delta+1 if g==0 else delta if g<k else a),(home[0],scale)));names.append((g,0))
        e_ids=[]
        for q,i in enumerate(home):
            j=len(p);e_ids.append(j);names.append((g,q+1))
            dest=home[q+1] if q+1<h else 0
            pv=scale if dest else 2 if g==0 else c
            p.append(((i,a),(dest,pv)))
        chain_tails.append((gr,e_ids))
    n=len(p);m=next_machine
    def cap(mask):
        load=[0]*m
        for j,e in enumerate(p):
            i,t=e[(mask>>j)&1];load[i]+=t
        return max(load)
    bad=0
    for j,(g,q) in enumerate(names):
        if g==0:bad|=1<<j
    B=cap(bad)
    assert F(B,scale)==2-F(3,k)+F(3,2*k*k)
    goalmask=bad;path=[bad]
    for g in range(1,k):
        gr,es=chain_tails[g]
        for j in reversed(es):
            goalmask|=1<<j;path.append(goalmask)
        goalmask|=1<<gr;path.append(goalmask)
    assert len(path)-1==(k-1)*(d+1)
    assert all((s^t).bit_count()==1 for s,t in zip(path,path[1:]))
    assert max(map(cap,path))==B+c and cap(goalmask)==scale
    values=[cap(mask) for mask in range(1<<n)]
    # Bottleneck shortest path in the full labeled assignment hypercube.
    peak={bad:B};heap=[(B,bad)];settled=0;optpeak=None
    while heap:
        value,s=heappop(heap)
        if value!=peak[s]:continue
        settled+=1
        if values[s]==scale:
            optpeak=value;break
        for j in range(n):
            t=s^(1<<j);new=max(value,values[t])
            if new<peak.get(t,10**20):
                peak[t]=new;heappush(heap,(new,t))
    assert optpeak==B+c
    assert min(values)==scale
    return dict(k=k,d=d,n=n,all_states=1<<n,settled_minimax_states=settled,B=str(F(B,scale)),escape_minimum_peak=str(F(optpeak,scale)),peak_increase=str(F(c,scale)),explicit_steps=len(path)-1)

if __name__=='__main__':
    print(json.dumps([run(k,d) for k,d in ((3,1),(3,2),(4,1))],indent=2))
